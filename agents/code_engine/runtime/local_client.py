#!/usr/bin/env python3
"""
Local LLM Client for Ollama
Handles communication with local Qwen models
"""

import json
import requests
from typing import Optional
from dataclasses import dataclass


@dataclass
class GenerationResult:
    """Result of code generation."""
    success: bool
    code: str
    model: str
    tokens_used: int
    error: Optional[str] = None


class LocalClient:
    """Client for local Ollama models."""
    
    def __init__(
        self,
        endpoint: str = "http://localhost:11434",
        timeout: int = 120
    ):
        self.endpoint = endpoint
        self.timeout = timeout
    
    def generate(
        self,
        prompt: str,
        model: str = "qwen2.5-coder:7b",
        system: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: int = 4096
    ) -> GenerationResult:
        """
        Generate code using local model.
        
        Args:
            prompt: The user prompt
            model: Model name (qwen2.5-coder:7b or qwen2.5-coder:14b)
            system: Optional system prompt
            temperature: Sampling temperature (0.1 for deterministic)
            max_tokens: Maximum tokens to generate
            
        Returns:
            GenerationResult with generated code
        """
        try:
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens
                }
            }
            
            if system:
                payload["system"] = system
            
            response = requests.post(
                f"{self.endpoint}/api/generate",
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            
            return GenerationResult(
                success=True,
                code=data.get("response", ""),
                model=model,
                tokens_used=data.get("eval_count", 0)
            )
            
        except requests.exceptions.Timeout:
            return GenerationResult(
                success=False,
                code="",
                model=model,
                tokens_used=0,
                error="Request timed out"
            )
        except requests.exceptions.RequestException as e:
            return GenerationResult(
                success=False,
                code="",
                model=model,
                tokens_used=0,
                error=str(e)
            )
    
    def chat(
        self,
        messages: list[dict],
        model: str = "qwen2.5-coder:7b",
        temperature: float = 0.1,
        max_tokens: int = 4096
    ) -> GenerationResult:
        """
        Chat-style generation (for multi-turn).
        
        Args:
            messages: List of {"role": "user/assistant", "content": "..."}
            model: Model name
            temperature: Sampling temperature
            max_tokens: Maximum tokens
            
        Returns:
            GenerationResult
        """
        try:
            payload = {
                "model": model,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens
                }
            }
            
            response = requests.post(
                f"{self.endpoint}/api/chat",
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            message = data.get("message", {})
            
            return GenerationResult(
                success=True,
                code=message.get("content", ""),
                model=model,
                tokens_used=data.get("eval_count", 0)
            )
            
        except Exception as e:
            return GenerationResult(
                success=False,
                code="",
                model=model,
                tokens_used=0,
                error=str(e)
            )
    
    def health_check(self) -> bool:
        """Check if Ollama server is running."""
        try:
            response = requests.get(
                f"{self.endpoint}/api/tags",
                timeout=5
            )
            return response.status_code == 200
        except:
            return False
    
    def list_models(self) -> list[str]:
        """List available models."""
        try:
            response = requests.get(
                f"{self.endpoint}/api/tags",
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            return [m["name"] for m in data.get("models", [])]
        except:
            return []


# CLI usage
if __name__ == "__main__":
    import sys
    
    client = LocalClient()
    
    if not client.health_check():
        print("ERROR: Ollama server not running")
        print("Start with: ollama serve")
        sys.exit(1)
    
    print("Available models:", client.list_models())
    
    # Test generation
    result = client.generate(
        prompt="Write a Python function to check if a number is prime",
        model="qwen2.5-coder:7b",
        temperature=0.1
    )
    
    if result.success:
        print(f"\n--- Generated ({result.tokens_used} tokens) ---")
        print(result.code)
    else:
        print(f"ERROR: {result.error}")