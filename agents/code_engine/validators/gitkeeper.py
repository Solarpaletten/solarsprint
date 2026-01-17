#!/usr/bin/env python3
"""
GitKeeper Compliance Validator
Ensures generated code follows GitKeeper contracts
"""

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class ComplianceResult:
    """Result of GitKeeper compliance check."""
    compliant: bool
    violations: list[str]
    warnings: list[str]


class GitKeeperValidator:
    """Validates code against GitKeeper contracts."""
    
    def __init__(self, gitkeeper_path: Optional[str] = None):
        self.rules = {}
        self.models = []
        self.api_contracts = []
        self.forbidden_patterns = []
        
        if gitkeeper_path:
            self._parse_gitkeeper(gitkeeper_path)
    
    def _parse_gitkeeper(self, path: str):
        """Parse GitKeeper document for validation rules."""
        try:
            content = Path(path).read_text()
            
            # Extract domain models
            model_section = re.search(
                r'## .*Domain Model.*?\n(.*?)(?=##|\Z)', 
                content, 
                re.DOTALL | re.IGNORECASE
            )
            if model_section:
                models = re.findall(r'(?:model\s+)?(\w+)', model_section.group(1))
                self.models = [m for m in models if m[0].isupper()]
            
            # Extract API contracts
            api_section = re.search(
                r'## .*API Contract.*?\n(.*?)(?=##|\Z)', 
                content, 
                re.DOTALL | re.IGNORECASE
            )
            if api_section:
                contracts = re.findall(
                    r'(GET|POST|PUT|DELETE|PATCH)\s+[|]?\s*(/[^\s|]+)',
                    api_section.group(1)
                )
                self.api_contracts = contracts
            
            # Extract non-negotiables / forbidden
            freeze_section = re.search(
                r'## .*Non-Negotiable.*?\n(.*?)(?=##|\Z)',
                content,
                re.DOTALL | re.IGNORECASE
            )
            if freeze_section:
                # Parse rules from freeze section
                pass
                
        except Exception as e:
            print(f"Warning: Could not parse GitKeeper: {e}")
    
    def validate(self, code: str, context: Optional[dict] = None) -> ComplianceResult:
        """
        Validate code against GitKeeper rules.
        
        Args:
            code: Generated code to validate
            context: Optional context (file path, task type, etc.)
            
        Returns:
            ComplianceResult with any violations
        """
        violations = []
        warnings = []
        
        # Check 1: No invented models
        if self.models:
            model_refs = re.findall(r'prisma\.(\w+)\.', code)
            for ref in model_refs:
                if ref.lower() not in [m.lower() for m in self.models]:
                    violations.append(f"Unknown model reference: prisma.{ref}")
        
        # Check 2: Multi-tenant rules
        if 'tenantId' in code:
            # Ensure tenantId comes from session, not request body
            if re.search(r'body\.tenantId|request\..*tenantId', code):
                violations.append(
                    "SECURITY: tenantId must come from session, not client request"
                )
        
        # Check 3: No solar energy references (project-specific)
        solar_patterns = [
            r'\bsolar\s+panel',
            r'\bsolar\s+energy',
            r'\benergy\s+tracking',
            r'\bweather\s+data',
        ]
        for pattern in solar_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                violations.append(
                    f"Invalid domain reference: matches '{pattern}' "
                    "(this is a task management system)"
                )
        
        # Check 4: Appropriate error handling
        if 'async' in code and 'await' in code:
            if 'try' not in code and 'catch' not in code:
                warnings.append(
                    "Async code without try/catch - consider adding error handling"
                )
        
        # Check 5: No hardcoded secrets
        secret_patterns = [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
            r'api[_-]?key\s*=\s*["\'][^"\']+["\']',
        ]
        for pattern in secret_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                violations.append(
                    "SECURITY: Hardcoded secret detected - use environment variables"
                )
        
        # Check 6: Proper Next.js patterns
        if 'NextResponse' in code:
            # Check for proper imports
            if 'import' in code and 'NextResponse' in code:
                if "from 'next/server'" not in code:
                    warnings.append(
                        "NextResponse should be imported from 'next/server'"
                    )
        
        return ComplianceResult(
            compliant=len(violations) == 0,
            violations=violations,
            warnings=warnings
        )


# CLI usage
if __name__ == "__main__":
    validator = GitKeeperValidator()
    
    # Test cases
    test_codes = [
        # Good code
        """
import { NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'
import { getCurrentSession } from '@/lib/session'

export async function GET() {
  const session = await getCurrentSession()
  if (!session) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }
  
  const projects = await prisma.project.findMany({
    where: { tenantId: session.user.tenantId }
  })
  
  return NextResponse.json(projects)
}
        """,
        # Bad code - tenantId from body
        """
export async function POST(request) {
  const { tenantId, name } = await request.json()
  
  const project = await prisma.project.create({
    data: { name, tenantId }
  })
  
  return NextResponse.json(project)
}
        """,
        # Bad code - hardcoded secret
        """
const API_KEY = "sk-1234567890abcdef"
const password = "admin123"
        """,
    ]
    
    print("GitKeeper Compliance Test")
    print("=" * 40)
    
    for i, code in enumerate(test_codes):
        result = validator.validate(code)
        status = "✅" if result.compliant else "❌"
        print(f"\n{status} Test {i + 1}")
        print(f"   Compliant: {result.compliant}")
        if result.violations:
            print("   Violations:")
            for v in result.violations:
                print(f"     - {v}")
        if result.warnings:
            print("   Warnings:")
            for w in result.warnings:
                print(f"     - {w}")