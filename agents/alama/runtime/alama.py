#!/usr/bin/env python3
"""
Alama — Reasoning Engine CLI

A reasoning and analysis assistant for the Solar Sprint project.
Powered by LLaMA via Ollama.

Usage:
    python alama.py analyze --repo /path/to/repo
    python alama.py gitkeeper --repo /path/to/repo --output gitkeeper/
    python alama.py report --type daily --project solar-sprint
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

import requests


# =============================================================================
# Configuration
# =============================================================================

DEFAULT_MODEL = "llama3:8b"
FALLBACK_MODEL = "llama3:8b"
OLLAMA_HOST = "http://localhost:11434"
CONTEXT_LENGTH = 8192
TEMPERATURE = 0.3  # Lower for consistent analysis

BASE_DIR = Path(__file__).parent.parent
PROMPTS_DIR = BASE_DIR / "prompts"
GITKEEPER_DIR = BASE_DIR / "gitkeeper"
REPORTS_DIR = BASE_DIR / "reports"
LOGS_DIR = BASE_DIR / "logs"


# =============================================================================
# Ollama Client
# =============================================================================

class OllamaClient:
    """Client for Ollama LLM server."""
    
    def __init__(self, model: str = DEFAULT_MODEL, host: str = OLLAMA_HOST):
        self.model = model
        self.host = host
    
    def is_available(self) -> bool:
        """Check if Ollama server is running."""
        try:
            response = requests.get(f"{self.host}/", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def has_model(self, model: str) -> bool:
        """Check if model is available."""
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=10)
            models = response.json().get("models", [])
            return any(m["name"].startswith(model.split(":")[0]) for m in models)
        except:
            return False
    
    def chat(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = TEMPERATURE
    ) -> str:
        """Send a chat request to Ollama."""
        try:
            response = requests.post(
                f"{self.host}/api/chat",
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_ctx": CONTEXT_LENGTH
                    }
                },
                timeout=300  # 5 minutes for long responses
            )
            
            data = response.json()
            return data.get("message", {}).get("content", "")
            
        except Exception as e:
            return f"ERROR: {str(e)}"


# =============================================================================
# Repository Analysis
# =============================================================================

def get_directory_tree(path: str, max_depth: int = 3) -> str:
    """Get directory tree structure."""
    try:
        result = subprocess.run(
            ["find", path, "-maxdepth", str(max_depth), "-type", "f", "-o", "-type", "d"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Format as tree-like structure
        lines = result.stdout.strip().split("\n")
        base = Path(path).name
        
        formatted = [base + "/"]
        for line in lines[1:]:  # Skip base path
            rel_path = os.path.relpath(line, path)
            if rel_path == ".":
                continue
            depth = rel_path.count(os.sep)
            indent = "  " * depth
            name = os.path.basename(line)
            if os.path.isdir(line):
                name += "/"
            formatted.append(f"{indent}├── {name}")
        
        return "\n".join(formatted[:100])  # Limit output
        
    except Exception as e:
        return f"Error getting tree: {e}"


def get_key_files(path: str) -> str:
    """Identify key project files."""
    key_patterns = [
        "package.json", "requirements.txt", "Cargo.toml",
        "README.md", "LICENSE", ".env.example",
        "prisma/schema.prisma", "docker-compose.yml"
    ]
    
    found = []
    for pattern in key_patterns:
        file_path = Path(path) / pattern
        if file_path.exists():
            found.append(f"- {pattern}")
    
    return "\n".join(found) if found else "- None identified"


def analyze_repo(repo_path: str, client: OllamaClient) -> str:
    """Analyze a repository and return insights."""
    
    # Load prompt template
    prompt_file = PROMPTS_DIR / "analyze_repo.md"
    if not prompt_file.exists():
        return "ERROR: analyze_repo.md prompt not found"
    
    # Gather repo info
    tree = get_directory_tree(repo_path)
    key_files = get_key_files(repo_path)
    
    # Read package.json or requirements if exists
    deps = ""
    pkg_json = Path(repo_path) / "package.json"
    if pkg_json.exists():
        try:
            with open(pkg_json) as f:
                data = json.load(f)
                deps = json.dumps(data.get("dependencies", {}), indent=2)
        except:
            deps = "Could not parse package.json"
    
    # Build prompt
    system_prompt = """You are Alama, a senior software architect assistant.
Your role is to analyze repository structures and provide clear, actionable insights.
Be concise and structured. Focus on architecture, not implementation details.
Output in Markdown format. Do NOT write code, only analyze."""
    
    user_prompt = f"""Analyze the following repository:

**Repository:** {os.path.basename(repo_path)}
**Path:** {repo_path}

**Directory Structure:**
{tree}

**Key Files Identified:**
{key_files}

**Dependencies (if available):**
{deps}

---

Provide analysis with these sections:
1. Project Overview
2. Architecture Pattern
3. Directory Structure Analysis
4. Dependencies
5. Strengths
6. Concerns
7. Recommendations (top 3)"""

    return client.chat(system_prompt, user_prompt)


# =============================================================================
# GitKeeper Generation
# =============================================================================

def generate_gitkeeper(
    repo_path: str,
    project_name: str,
    client: OllamaClient,
    context: str = ""
) -> str:
    """Generate a GitKeeper document for a project."""
    
    # Gather repo info
    tree = get_directory_tree(repo_path)
    
    system_prompt = """You are Alama, a documentation specialist for software projects.
Your task is to generate a GitKeeper document that serves as the canonical source of truth.
Be precise and unambiguous. Use FREEZE markers for locked decisions.
Output clean Markdown."""

    user_prompt = f"""Generate a GitKeeper document for:

**Project:** {project_name}
**Path:** {repo_path}

**Directory Structure:**
{tree}

**Additional Context:**
{context if context else "None provided"}

---

Generate GitKeeper with these sections:
0) Meta (Owner, Supervisor, Engineer, Status, Date)
1) Mission
2) Non-Negotiable Principles (FREEZE)
3) Current Sprint Scope (Included / Excluded)
4) Domain Model
5) Technical Stack (FREEZE)
6) API Contracts (FREEZE) if applicable
7) Acceptance Criteria
8) Engineering Checklist
9) Change Control
10) Next Releases (Future)

Use proper Markdown formatting with ## headers."""

    return client.chat(system_prompt, user_prompt)


# =============================================================================
# Report Generation
# =============================================================================

def generate_report(
    report_type: str,
    project_name: str,
    client: OllamaClient,
    notes: str = ""
) -> str:
    """Generate a report."""
    
    date = datetime.now().strftime("%Y-%m-%d")
    
    system_prompt = """You are Alama, a project management assistant.
Your task is to generate clear, actionable reports.
Be concise, use bullet points, highlight blockers prominently."""

    if report_type == "daily":
        user_prompt = f"""Generate a daily report for:

**Date:** {date}
**Project:** {project_name}

**Notes:**
{notes if notes else "No specific notes provided"}

---

Generate report with:
- ✅ Completed
- 🔄 In Progress
- 🚫 Blockers
- 📌 Decisions Made
- 📋 Tomorrow's Focus
- 📊 Sprint Progress
- 💡 Notes for Supervisor"""

    elif report_type == "standup":
        user_prompt = f"""Generate a standup summary for:

**Date:** {date}
**Project:** {project_name}

**Notes:**
{notes if notes else "No specific notes provided"}

---

Generate brief standup with:
1. What I did yesterday
2. What I'm doing today
3. Blockers"""

    else:
        user_prompt = f"Generate a {report_type} report for {project_name}. Notes: {notes}"

    return client.chat(system_prompt, user_prompt)


# =============================================================================
# Logging
# =============================================================================

def log_request(action: str, input_data: str, output: str, model: str):
    """Log a request to the logs directory."""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = LOGS_DIR / f"{timestamp}_{action}.log"
    
    log_content = f"""# Alama Log: {action}
Timestamp: {datetime.now().isoformat()}
Model: {model}

## Input
{input_data[:500]}...

## Output
{output[:1000]}...
"""
    
    with open(log_file, "w") as f:
        f.write(log_content)


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Alama — Reasoning Engine for Solar Sprint"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze a repository")
    analyze_parser.add_argument("--repo", required=True, help="Path to repository")
    analyze_parser.add_argument("--output", help="Output file path")
    
    # GitKeeper command
    gitkeeper_parser = subparsers.add_parser("gitkeeper", help="Generate GitKeeper")
    gitkeeper_parser.add_argument("--repo", required=True, help="Path to repository")
    gitkeeper_parser.add_argument("--project", help="Project name")
    gitkeeper_parser.add_argument("--context", help="Additional context file")
    gitkeeper_parser.add_argument("--output", help="Output directory")
    
    # Report command
    report_parser = subparsers.add_parser("report", help="Generate report")
    report_parser.add_argument("--type", default="daily", help="Report type")
    report_parser.add_argument("--project", required=True, help="Project name")
    report_parser.add_argument("--notes", help="Notes file")
    report_parser.add_argument("--output", help="Output directory")
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Check Alama status")
    
    args = parser.parse_args()
    
    # Initialize client
    client = OllamaClient()
    
    # Handle status command
    if args.command == "status":
        print("Alama Status Check")
        print("=" * 40)
        
        if client.is_available():
            print("✓ Ollama server: Running")
        else:
            print("✗ Ollama server: Not running")
            print("  Start with: ollama serve")
            sys.exit(1)
        
        if client.has_model(DEFAULT_MODEL):
            print(f"✓ Model {DEFAULT_MODEL}: Available")
        else:
            print(f"✗ Model {DEFAULT_MODEL}: Not found")
            print(f"  Install with: ollama pull {DEFAULT_MODEL}")
            
            # Try fallback
            if client.has_model(FALLBACK_MODEL):
                print(f"✓ Fallback {FALLBACK_MODEL}: Available")
                client.model = FALLBACK_MODEL
            else:
                print(f"✗ Fallback {FALLBACK_MODEL}: Not found")
                sys.exit(1)
        
        print("=" * 40)
        print("Alama is ready!")
        sys.exit(0)
    
    # Check prerequisites
    if not client.is_available():
        print("ERROR: Ollama server not running. Start with: ollama serve")
        sys.exit(1)
    
    if not client.has_model(DEFAULT_MODEL):
        if client.has_model(FALLBACK_MODEL):
            print(f"Warning: Using fallback model {FALLBACK_MODEL}")
            client.model = FALLBACK_MODEL
        else:
            print(f"ERROR: Model not found. Install with: ollama pull {DEFAULT_MODEL}")
            sys.exit(1)
    
    # Execute command
    if args.command == "analyze":
        print(f"Analyzing repository: {args.repo}")
        result = analyze_repo(args.repo, client)
        
        if args.output:
            with open(args.output, "w") as f:
                f.write(result)
            print(f"Analysis saved to: {args.output}")
        else:
            print("\n" + result)
        
        log_request("analyze", args.repo, result, client.model)
    
    elif args.command == "gitkeeper":
        project_name = args.project or os.path.basename(args.repo)
        context = ""
        if args.context and os.path.exists(args.context):
            with open(args.context) as f:
                context = f.read()
        
        print(f"Generating GitKeeper for: {project_name}")
        result = generate_gitkeeper(args.repo, project_name, client, context)
        
        if args.output:
            output_dir = Path(args.output)
            output_dir.mkdir(parents=True, exist_ok=True)
            output_file = output_dir / f"{project_name}_gitkeeper.md"
            with open(output_file, "w") as f:
                f.write(result)
            print(f"GitKeeper saved to: {output_file}")
        else:
            print("\n" + result)
        
        log_request("gitkeeper", args.repo, result, client.model)
    
    elif args.command == "report":
        notes = ""
        if args.notes and os.path.exists(args.notes):
            with open(args.notes) as f:
                notes = f.read()
        
        print(f"Generating {args.type} report for: {args.project}")
        result = generate_report(args.type, args.project, client, notes)
        
        if args.output:
            output_dir = Path(args.output)
            output_dir.mkdir(parents=True, exist_ok=True)
            date = datetime.now().strftime("%Y-%m-%d")
            output_file = output_dir / f"{date}_{args.type}.md"
            with open(output_file, "w") as f:
                f.write(result)
            print(f"Report saved to: {output_file}")
        else:
            print("\n" + result)
        
        log_request("report", args.project, result, client.model)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
