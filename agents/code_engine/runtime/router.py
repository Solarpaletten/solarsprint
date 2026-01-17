#!/usr/bin/env python3
"""
Task Router for Code Engine
Decides whether to use local or API model based on task complexity
"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class TaskType(Enum):
    """Type of coding task."""
    IMPLEMENT = "implement"
    REFACTOR = "refactor"
    FIX = "fix"
    TEST = "test"
    DOCUMENT = "document"


class ModelTier(Enum):
    """Which model tier to use."""
    LOCAL_JUNIOR = "local_junior"   # Qwen 7B - fast, simple tasks
    LOCAL_SENIOR = "local_senior"   # Qwen 14B - medium tasks
    API = "api"                      # Claude/DeepSeek - complex tasks


@dataclass
class TaskAnalysis:
    """Analysis of a coding task."""
    task_type: TaskType
    estimated_lines: int
    files_affected: int
    complexity: str  # low, medium, high
    requires_api: bool
    recommended_tier: ModelTier
    reason: str


@dataclass
class RoutingConfig:
    """Configuration for routing decisions."""
    local_threshold_lines: int = 200
    local_threshold_files: int = 1
    prefer_local: bool = True
    api_available: bool = False


class TaskRouter:
    """Routes tasks to appropriate model tier."""
    
    def __init__(self, config: Optional[RoutingConfig] = None):
        self.config = config or RoutingConfig()
        
        # Patterns that indicate complexity
        self.complex_patterns = [
            r"refactor.*multiple.*files",
            r"architecture.*change",
            r"migrate.*to",
            r"security.*critical",
            r"auth.*system",
            r"payment.*integration",
            r"database.*migration",
        ]
        
        # Patterns that indicate simple tasks
        self.simple_patterns = [
            r"add.*comment",
            r"fix.*typo",
            r"rename.*variable",
            r"format.*code",
            r"add.*import",
            r"simple.*crud",
            r"boilerplate",
        ]
    
    def analyze(self, task: str, context: Optional[dict] = None) -> TaskAnalysis:
        """
        Analyze a task and determine routing.
        
        Args:
            task: Task description
            context: Optional context (files, gitkeeper, etc.)
            
        Returns:
            TaskAnalysis with routing recommendation
        """
        task_lower = task.lower()
        
        # Detect task type
        task_type = self._detect_task_type(task_lower)
        
        # Estimate scope
        estimated_lines = self._estimate_lines(task_lower, context)
        files_affected = self._estimate_files(task_lower, context)
        
        # Determine complexity
        complexity = self._assess_complexity(task_lower, estimated_lines, files_affected)
        
        # Decide routing
        requires_api, tier, reason = self._decide_routing(
            task_lower, complexity, estimated_lines, files_affected
        )
        
        return TaskAnalysis(
            task_type=task_type,
            estimated_lines=estimated_lines,
            files_affected=files_affected,
            complexity=complexity,
            requires_api=requires_api,
            recommended_tier=tier,
            reason=reason
        )
    
    def _detect_task_type(self, task: str) -> TaskType:
        """Detect the type of task."""
        if any(w in task for w in ["implement", "create", "add", "build", "write"]):
            return TaskType.IMPLEMENT
        elif any(w in task for w in ["refactor", "restructure", "reorganize"]):
            return TaskType.REFACTOR
        elif any(w in task for w in ["fix", "bug", "error", "issue", "debug"]):
            return TaskType.FIX
        elif any(w in task for w in ["test", "spec", "coverage"]):
            return TaskType.TEST
        elif any(w in task for w in ["document", "comment", "readme", "jsdoc"]):
            return TaskType.DOCUMENT
        return TaskType.IMPLEMENT
    
    def _estimate_lines(self, task: str, context: Optional[dict]) -> int:
        """Estimate lines of code to generate."""
        # Check for explicit mentions
        if "single function" in task or "small" in task:
            return 30
        elif "endpoint" in task or "api" in task:
            return 80
        elif "component" in task:
            return 100
        elif "feature" in task:
            return 200
        elif "refactor" in task:
            return 300
        elif "system" in task or "module" in task:
            return 500
        return 100  # default
    
    def _estimate_files(self, task: str, context: Optional[dict]) -> int:
        """Estimate number of files affected."""
        if "single file" in task:
            return 1
        elif "multiple files" in task or "refactor" in task:
            return 5
        elif "system" in task:
            return 10
        
        # Count file mentions
        file_patterns = [
            r"\.tsx?",
            r"\.jsx?", 
            r"\.py",
            r"\.prisma",
            r"\.md"
        ]
        file_count = sum(1 for p in file_patterns if re.search(p, task))
        return max(1, file_count)
    
    def _assess_complexity(self, task: str, lines: int, files: int) -> str:
        """Assess overall complexity."""
        # Check for complex patterns
        for pattern in self.complex_patterns:
            if re.search(pattern, task):
                return "high"
        
        # Check for simple patterns
        for pattern in self.simple_patterns:
            if re.search(pattern, task):
                return "low"
        
        # Assess by scope
        if lines > 300 or files > 3:
            return "high"
        elif lines > 100 or files > 1:
            return "medium"
        return "low"
    
    def _decide_routing(
        self, 
        task: str, 
        complexity: str, 
        lines: int, 
        files: int
    ) -> tuple[bool, ModelTier, str]:
        """Decide which tier to route to."""
        
        # Force API for certain tasks
        for pattern in self.complex_patterns:
            if re.search(pattern, task):
                if self.config.api_available:
                    return True, ModelTier.API, f"Complex task: matches '{pattern}'"
                else:
                    return False, ModelTier.LOCAL_SENIOR, "Complex task but API unavailable"
        
        # Simple tasks -> Junior
        if complexity == "low" and lines < 50 and files == 1:
            return False, ModelTier.LOCAL_JUNIOR, "Simple single-file task"
        
        # Medium tasks -> Senior
        if complexity == "medium" or (lines <= self.config.local_threshold_lines and files <= self.config.local_threshold_files):
            return False, ModelTier.LOCAL_SENIOR, "Medium complexity, within local limits"
        
        # Complex tasks -> API (if available)
        if self.config.api_available:
            return True, ModelTier.API, "High complexity task"
        
        # Fallback to Senior
        return False, ModelTier.LOCAL_SENIOR, "Complex but using local (API unavailable)"


# CLI usage
if __name__ == "__main__":
    router = TaskRouter()
    
    test_tasks = [
        "Add a comment to the function",
        "Create a simple CRUD endpoint for users",
        "Implement authentication system with JWT",
        "Refactor multiple files to use new pattern",
        "Fix typo in variable name",
        "Build payment integration with Stripe",
    ]
    
    print("Task Routing Analysis")
    print("=" * 60)
    
    for task in test_tasks:
        analysis = router.analyze(task)
        print(f"\nTask: {task}")
        print(f"  Type: {analysis.task_type.value}")
        print(f"  Complexity: {analysis.complexity}")
        print(f"  Est. Lines: {analysis.estimated_lines}")
        print(f"  Files: {analysis.files_affected}")
        print(f"  → Route: {analysis.recommended_tier.value}")
        print(f"  Reason: {analysis.reason}")