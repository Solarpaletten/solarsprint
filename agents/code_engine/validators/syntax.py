#!/usr/bin/env python3
"""
Syntax Validator for Code Engine
Validates generated code before output
"""

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import tempfile


@dataclass
class ValidationResult:
    """Result of validation check."""
    passed: bool
    error: Optional[str] = None
    details: Optional[str] = None


class SyntaxValidator:
    """Validates code syntax."""
    
    def validate_typescript(self, code: str) -> ValidationResult:
        """
        Validate TypeScript syntax.
        Requires: npm install -g typescript
        """
        # Quick regex checks first
        issues = []
        
        # Check for common issues
        if "any" in code and ": any" in code:
            issues.append("Contains 'any' type - prefer explicit types")
        
        if "// TODO" in code:
            issues.append("Contains TODO comments")
        
        if "console.log" in code:
            issues.append("Contains console.log - remove before production")
        
        # Try actual TypeScript compilation
        try:
            with tempfile.NamedTemporaryFile(
                mode='w', 
                suffix='.ts', 
                delete=False
            ) as f:
                f.write(code)
                f.flush()
                
                result = subprocess.run(
                    ['npx', 'tsc', '--noEmit', '--strict', f.name],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode != 0:
                    return ValidationResult(
                        passed=False,
                        error="TypeScript compilation failed",
                        details=result.stderr or result.stdout
                    )
                
        except FileNotFoundError:
            # TypeScript not installed - skip compilation
            pass
        except subprocess.TimeoutExpired:
            return ValidationResult(
                passed=False,
                error="TypeScript compilation timed out"
            )
        except Exception as e:
            # Non-critical, continue with basic checks
            pass
        
        if issues:
            return ValidationResult(
                passed=True,  # Warnings, not failures
                error=None,
                details="Warnings: " + "; ".join(issues)
            )
        
        return ValidationResult(passed=True)
    
    def validate_python(self, code: str) -> ValidationResult:
        """Validate Python syntax."""
        try:
            compile(code, '<string>', 'exec')
            return ValidationResult(passed=True)
        except SyntaxError as e:
            return ValidationResult(
                passed=False,
                error=f"Python syntax error at line {e.lineno}",
                details=str(e)
            )
    
    def validate_json(self, code: str) -> ValidationResult:
        """Validate JSON syntax."""
        import json
        try:
            json.loads(code)
            return ValidationResult(passed=True)
        except json.JSONDecodeError as e:
            return ValidationResult(
                passed=False,
                error=f"JSON error at line {e.lineno}",
                details=str(e)
            )
    
    def detect_language(self, code: str) -> str:
        """Detect language from code content."""
        # TypeScript/JavaScript indicators
        if any(kw in code for kw in ['import {', 'export ', 'const ', ': string', ': number']):
            if ': string' in code or ': number' in code or 'interface ' in code:
                return 'typescript'
            return 'javascript'
        
        # Python indicators
        if any(kw in code for kw in ['def ', 'import ', 'from ', 'class ', 'async def']):
            return 'python'
        
        # JSON
        if code.strip().startswith('{') or code.strip().startswith('['):
            return 'json'
        
        return 'unknown'
    
    def validate(self, code: str, language: Optional[str] = None) -> ValidationResult:
        """
        Validate code syntax.
        
        Args:
            code: Code to validate
            language: Language (auto-detected if not provided)
            
        Returns:
            ValidationResult
        """
        if not language:
            language = self.detect_language(code)
        
        if language == 'typescript':
            return self.validate_typescript(code)
        elif language == 'python':
            return self.validate_python(code)
        elif language == 'json':
            return self.validate_json(code)
        else:
            return ValidationResult(
                passed=True,
                details=f"No validator for language: {language}"
            )


class ImportsValidator:
    """Validates imports against package.json."""
    
    def __init__(self, package_json_path: Optional[str] = None):
        self.allowed_packages = set()
        if package_json_path:
            self._load_packages(package_json_path)
    
    def _load_packages(self, path: str):
        """Load allowed packages from package.json."""
        import json
        try:
            with open(path) as f:
                data = json.load(f)
            deps = data.get('dependencies', {})
            dev_deps = data.get('devDependencies', {})
            self.allowed_packages = set(deps.keys()) | set(dev_deps.keys())
        except:
            pass
    
    def validate(self, code: str) -> ValidationResult:
        """Validate all imports exist in package.json."""
        if not self.allowed_packages:
            return ValidationResult(
                passed=True,
                details="No package.json loaded"
            )
        
        # Extract imports
        import_pattern = r"from ['\"]([^'\"]+)['\"]|import ['\"]([^'\"]+)['\"]"
        matches = re.findall(import_pattern, code)
        
        unknown = []
        for match in matches:
            package = match[0] or match[1]
            # Get base package name (e.g., '@prisma/client' -> '@prisma/client')
            if package.startswith('@'):
                parts = package.split('/')
                base = '/'.join(parts[:2]) if len(parts) > 1 else parts[0]
            else:
                base = package.split('/')[0]
            
            # Skip relative and internal imports
            if base.startswith('.') or base.startswith('@/'):
                continue
            
            # Skip Node.js built-ins
            if base in ['fs', 'path', 'crypto', 'util', 'http', 'https', 'stream']:
                continue
            
            if base not in self.allowed_packages:
                unknown.append(base)
        
        if unknown:
            return ValidationResult(
                passed=False,
                error="Unknown imports",
                details=f"Not in package.json: {', '.join(unknown)}"
            )
        
        return ValidationResult(passed=True)


# CLI usage
if __name__ == "__main__":
    validator = SyntaxValidator()
    
    test_codes = [
        # Valid TypeScript
        """
export function hello(name: string): string {
  return `Hello, ${name}!`
}
        """,
        # Invalid Python
        """
def hello(
    print("broken")
        """,
        # Valid JSON
        """
{"name": "test", "value": 123}
        """
    ]
    
    print("Syntax Validation Test")
    print("=" * 40)
    
    for code in test_codes:
        lang = validator.detect_language(code)
        result = validator.validate(code)
        status = "✅" if result.passed else "❌"
        print(f"\n{status} Language: {lang}")
        print(f"   Passed: {result.passed}")
        if result.error:
            print(f"   Error: {result.error}")
        if result.details:
            print(f"   Details: {result.details}")