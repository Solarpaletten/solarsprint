#!/usr/bin/env python3
"""
Code Engine - Main Orchestrator
Coordinates code generation using local and API models
"""

from pathlib import Path
from dataclasses import dataclass
from typing import Optional
import yaml

from .local_client import LocalClient, GenerationResult
from .router import TaskRouter, TaskAnalysis, ModelTier, RoutingConfig
from ..validators.clean_output import CleanOutputValidator


# =========================
# CONFIG
# =========================

@dataclass
class EngineConfig:
    # Models
    junior_model: str = "qwen2.5-coder:7b"
    senior_model: str = "qwen2.5-coder:14b"
    ollama_endpoint: str = "http://localhost:11434"

    # Generation params
    temperature: float = 0.1
    junior_max_tokens: int = 4096
    senior_max_tokens: int = 8192

    # Routing
    local_threshold_lines: int = 200
    local_threshold_files: int = 1
    prefer_local: bool = True

    # API
    api_available: bool = False
    api_provider: str = "claude"

    @classmethod
    def from_yaml(cls, path: str) -> "EngineConfig":
        with open(path) as f:
            data = yaml.safe_load(f)

        models = data.get("models", {})
        local = models.get("local", {})
        routing = data.get("routing", {})

        return cls(
            junior_model=local.get("junior", {}).get("name", cls.junior_model),
            senior_model=local.get("senior", {}).get("name", cls.senior_model),
            ollama_endpoint=local.get("junior", {}).get("endpoint", cls.ollama_endpoint),
            temperature=local.get("junior", {}).get("temperature", 0.1),
            junior_max_tokens=local.get("junior", {}).get("max_tokens", 4096),
            senior_max_tokens=local.get("senior", {}).get("max_tokens", 8192),
            local_threshold_lines=routing.get("local_threshold_lines", 200),
            local_threshold_files=routing.get("local_threshold_files", 1),
            prefer_local=routing.get("prefer_local", True),
        )


# =========================
# ENGINE
# =========================

class CodeEngine:
    def __init__(
        self,
        config: Optional[EngineConfig] = None,
        config_path: Optional[str] = None
    ):
        if config_path:
            self.config = EngineConfig.from_yaml(config_path)
        else:
            self.config = config or EngineConfig()

        self.local_client = LocalClient(endpoint=self.config.ollama_endpoint)

        routing_config = RoutingConfig(
            local_threshold_lines=self.config.local_threshold_lines,
            local_threshold_files=self.config.local_threshold_files,
            prefer_local=self.config.prefer_local,
            api_available=self.config.api_available,
        )
        self.router = TaskRouter(routing_config)

        self.prompts_dir = Path(__file__).parent.parent / "prompts"
        self.system_prompt = self._load_prompt("system.md")

        self.clean_validator = CleanOutputValidator()

    # ---------------------

    def _load_prompt(self, name: str) -> str:
        path = self.prompts_dir / name
        return path.read_text() if path.exists() else ""

    # ---------------------

    def generate(
        self,
        task: str,
        context: Optional[dict] = None,
        force_tier: Optional[ModelTier] = None
    ) -> GenerationResult:

        analysis: TaskAnalysis = self.router.analyze(task, context)
        tier = force_tier or analysis.recommended_tier

        prompt = self._build_prompt(task, context, analysis)

        if tier == ModelTier.LOCAL_JUNIOR:
            return self._generate_local(
                prompt,
                self.config.junior_model,
                self.config.junior_max_tokens
            )

        if tier == ModelTier.LOCAL_SENIOR:
            return self._generate_local(
                prompt,
                self.config.senior_model,
                self.config.senior_max_tokens
            )

        # API fallback
        return self._generate_local(
            prompt,
            self.config.senior_model,
            self.config.senior_max_tokens
        )

    # ---------------------

    def _generate_local(
        self,
        prompt: str,
        model: str,
        max_tokens: int
    ) -> GenerationResult:

        result = self.local_client.generate(
            prompt=prompt,
            model=model,
            system=self.system_prompt,
            temperature=self.config.temperature,
            max_tokens=max_tokens
        )

        if not result.success:
            return result

        # Strip markdown fences / terminal junk
        cleaned_code = self.clean_validator.strip_markdown_fences(result.code)

        # Validate output
        clean_result = self.clean_validator.validate(cleaned_code)

        if not clean_result.clean:
            return GenerationResult(
                success=False,
                code="",
                model=model,
                tokens_used=result.tokens_used,
                error="CLEAN OUTPUT VALIDATION FAILED:\n" +
                      "\n".join(clean_result.errors)
            )

        result.code = cleaned_code
        return result

    # ---------------------

    def _build_prompt(
        self,
        task: str,
        context: Optional[dict],
        analysis: TaskAnalysis
    ) -> str:
        parts = []

        if context:
            if "gitkeeper" in context:
                parts.append("## PROJECT CONTEXT\n" + context["gitkeeper"])

            if "files" in context:
                parts.append("## RELEVANT FILES")
                for name, content in context["files"].items():
                    parts.append(f"\n### {name}\n{content[:2000]}")

            if "tree" in context:
                parts.append("## DIRECTORY STRUCTURE\n" + context["tree"])

        parts.append("## TASK\n" + task)
        parts.append("## CONSTRAINTS")
        parts.append(f"- Task type: {analysis.task_type.value}")
        parts.append(f"- Expected size: ~{analysis.estimated_lines} lines")
        parts.append(f"- Complexity: {analysis.complexity}")

        return "\n".join(parts)

    # ---------------------

    def health_check(self) -> dict:
        ollama_ok = self.local_client.health_check()
        models = self.local_client.list_models() if ollama_ok else []

        return {
            "ollama": ollama_ok,
            "models": models,
            "junior_available": self.config.junior_model in models,
            "senior_available": self.config.senior_model in models,
            "api_available": self.config.api_available,
        }


# =========================
# CLI
# =========================

if __name__ == "__main__":
    config_path = Path(__file__).parent.parent / "config.yaml"
    engine = CodeEngine(config_path=str(config_path)) if config_path.exists() else CodeEngine()

    print("Code Engine Health Check")
    print("=" * 40)

    health = engine.health_check()
    for k, v in health.items():
        if isinstance(v, list):
            print(f"{k}: {v}")
        else:
            print(f"{'✅' if v else '❌'} {k}: {v}")

    print("\nTest generation\n" + "=" * 40)
    task = "Write a TypeScript function that validates email addresses"

    result = engine.generate(task)

    if result.success:
        print(result.code)
    else:
        print("ERROR:", result.error)
