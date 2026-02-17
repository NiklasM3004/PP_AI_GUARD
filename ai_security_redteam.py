#!/usr/bin/env python3
"""
AI Security Red Team Tool - Data Leak Prevention
Demonstrates detection of sensitive data before sending to LLMs
"""

import re
import sys
from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class SecurityViolation:
    """Represents a detected security violation"""
    category: str
    matched_text: str
    severity: str
    position: int


class DataLeakDetector:
    """Detects potential data leaks in prompts"""
    
    def __init__(self):
        # Regex patterns for common sensitive data
        self.patterns = {
            'email': (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', 'HIGH'),
            'credit_card': (r'\b(?:\d{4}[-\s]?){3}\d{4}\b', 'CRITICAL'),
            'ssn': (r'\b\d{3}-\d{2}-\d{4}\b', 'CRITICAL'),
            'phone': (r'\b(?:\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b', 'MEDIUM'),
            'api_key': (r'\b(?:api[_-]?key|token)[:\s]*["\']?([a-zA-Z0-9_\-]{20,})["\']?', 'CRITICAL'),
            'password': (r'(?:password|passwd|pwd)[:\s]*["\']?([^\s"\']{6,})["\']?', 'CRITICAL'),
            'ip_address': (r'\b(?:\d{1,3}\.){3}\d{1,3}\b', 'MEDIUM'),
            'internal_path': (r'(?:[A-Z]:\\|/home/|/Users/)[\w\\/.-]+', 'LOW'),
        }
        
    def scan(self, text: str) -> List[SecurityViolation]:
        """Scan text for sensitive data patterns"""
        violations = []
        
        for category, (pattern, severity) in self.patterns.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                violations.append(SecurityViolation(
                    category=category,
                    matched_text=self._redact(match.group()),
                    severity=severity,
                    position=match.start()
                ))
        
        return violations
    
    def _redact(self, text: str) -> str:
        """Partially redact sensitive text for display"""
        if len(text) <= 4:
            return '*' * len(text)
        return text[:2] + '*' * (len(text) - 4) + text[-2:]


def print_banner():
    """Print tool banner"""
    print("\n" + "="*60)
    print("  AI SECURITY RED TEAM TOOL")
    print("  Data Leak Prevention Demo v1.0")
    print("="*60 + "\n")


def print_violations(violations: List[SecurityViolation]):
    """Pretty print security violations"""
    if not violations:
        print("✅ No sensitive data detected. Safe to send!\n")
        return
    
    print(f"\n⚠️  ALERT: {len(violations)} potential data leak(s) detected!\n")
    
    severity_order = {'CRITICAL': 3, 'HIGH': 2, 'MEDIUM': 1, 'LOW': 0}
    violations.sort(key=lambda v: severity_order[v.severity], reverse=True)
    
    for i, v in enumerate(violations, 1):
        severity_symbol = {
            'CRITICAL': '🔴',
            'HIGH': '🟠', 
            'MEDIUM': '🟡',
            'LOW': '🔵'
        }[v.severity]
        
        print(f"{i}. {severity_symbol} [{v.severity}] {v.category.upper()}")
        print(f"   Matched: {v.matched_text}")
        print(f"   Position: Character {v.position}\n")


def interactive_mode():
    """Run tool in interactive mode"""
    print_banner()
    print("Enter text to scan (type 'quit' to exit, 'test' for examples):\n")
    
    detector = DataLeakDetector()
    
    while True:
        try:
            print("-" * 60)
            user_input = input("\n📝 Prompt to scan: ").strip()
            
            if user_input.lower() == 'quit':
                print("\nExiting. Stay secure! 🛡️\n")
                break
                
            if user_input.lower() == 'test':
                test_prompts()
                continue
            
            if not user_input:
                continue
            
            violations = detector.scan(user_input)
            print_violations(violations)
            
        except KeyboardInterrupt:
            print("\n\nExiting. Stay secure! 🛡️\n")
            break


def test_prompts():
    """Run test cases with sample prompts"""
    print("\n" + "="*60)
    print("  RUNNING TEST CASES")
    print("="*60)
    
    detector = DataLeakDetector()
    
    test_cases = [
        "Can you help me with this report?",  # Clean
        "My email is john.doe@company.com and my phone is 555-123-4567",  # PII
        "Use this API key: sk_live_51HqR2jKkj3h4g5h6j7k8l9m0n to connect",  # Credentials
        "SSN: 123-45-6789, Credit Card: 4532-1234-5678-9010",  # Financial
    ]
    
    for i, prompt in enumerate(test_cases, 1):
        print(f"\nTest #{i}: {prompt[:50]}...")
        violations = detector.scan(prompt)
        print_violations(violations)


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        if sys.argv[1] == '--test':
            print_banner()
            test_prompts()
        else:
            # Scan text from command line
            detector = DataLeakDetector()
            text = ' '.join(sys.argv[1:])
            violations = detector.scan(text)
            print_violations(violations)
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
