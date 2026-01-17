#!/usr/bin/env python3
"""
Clean Output Validator
Blocks terminal artifacts, markdown, and control characters
"""

import re
from dataclasses import dataclass


@dataclass
class CleanResult:
    clean: bool
    errors: list[str]


class CleanOutputValidator:
    FORBIDDEN_PATTERNS = [
        r"\^R",
        r"\^M",
        r"\x00",
        r"\u0000",
        r"^Here is",
        r"^Sure[,!]",
        r"Explanation:",
    ]

    CONTROL_CHARS = re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F]")

    MARKDOWN_FENCE = re.compile(r"^```[a-zA-Z]*\n?|```$", re.MULTILINE)

    def strip_markdown_fences(self, code: str) -> str:
        """
        Remove markdown fences like ``` or ```ts from output
        """
        if not code:
            return code
        return self.MARKDOWN_FENCE.sub("", code).strip()

    def validate(self, code: str) -> CleanResult:
        errors = []

        for pattern in self.FORBIDDEN_PATTERNS:
            if re.search(pattern, code):
                errors.append(f"Forbidden pattern detected: {pattern}")

        if self.CONTROL_CHARS.search(code):
            errors.append("Control characters detected")

        if code.strip() == "":
            errors.append("Empty output")

        return CleanResult(
            clean=len(errors) == 0,
            errors=errors
        )
