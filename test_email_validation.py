#!/usr/bin/env python3
"""
Unit Tests for Email Validation Function
Tests the isValidEmail() function from script.js

This test suite validates that the email validation properly:
1. Rejects emails with consecutive dots (the bug being fixed)
2. Rejects other invalid email formats
3. Accepts valid standard email formats
4. Handles edge cases appropriately

To run: python test_email_validation.py
"""

import re
import sys

# ANSI color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_colored(text, color, bold=False):
    """Print colored text to terminal"""
    prefix = f"{Colors.BOLD}" if bold else ""
    print(f"{prefix}{color}{text}{Colors.RESET}")

def is_valid_email(email):
    """
    Email validation function that matches the fixed implementation in script.js
    
    Pattern explanation:
    ^[^\s@.]      - Start with character that's not space, @, or dot
    [^\s@]*       - Followed by zero or more characters that aren't space or @
    @             - Literal @ symbol
    [^\s@.]       - Domain starts with character that's not space, @, or dot
    [^\s@.]*      - Followed by zero or more characters that aren't space or @
    (\.[^\s@.][^\s@.]*)+  - One or more groups of: dot followed by chars not space/@/dot
    $             - End of string
    
    This pattern prevents consecutive dots and other invalid formats.
    """
    email_regex = r'^[^\s@.][^\s@]*@[^\s@.][^\s@.]*(\.[^\s@.][^\s@.]*)+$'
    return bool(re.match(email_regex, email))

class TestResults:
    """Track and report test results"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []

    def add_pass(self, test_name):
        """Record a passing test"""
        self.passed += 1
        self.tests.append({'name': test_name, 'status': 'PASS'})
        print(f"{Colors.GREEN}✓ PASS:{Colors.RESET} {test_name}")

    def add_fail(self, test_name, reason):
        """Record a failing test"""
        self.failed += 1
        self.tests.append({'name': test_name, 'status': 'FAIL', 'reason': reason})
        print(f"{Colors.RED}✗ FAIL:{Colors.RESET} {test_name}")
        print(f"  {Colors.YELLOW}Reason: {reason}{Colors.RESET}")

    def print_summary(self):
        """Print final test summary"""
        print('\n' + '='*70)
        print_colored('TEST SUMMARY', Colors.CYAN, bold=True)
        print('='*70)
        total = self.passed + self.failed
        print(f"Total: {total} | {Colors.GREEN}Passed: {self.passed}{Colors.RESET} | {Colors.RED}Failed: {self.failed}{Colors.RESET}")
        
        if self.failed == 0:
            print_colored('\n✓ All tests passed!', Colors.GREEN, bold=True)
            return True
        else:
            print_colored(f'\n✗ {self.failed} test(s) failed', Colors.RED, bold=True)
            return False

# Initialize test results
results = TestResults()

# ============================================================
# VALID EMAIL TESTS
# ============================================================
print_colored('\n' + '='*70, Colors.CYAN)
print_colored('TESTING VALID EMAILS', Colors.CYAN, bold=True)
print_colored('='*70, Colors.CYAN)

valid_emails = [
    'user@example.com',
    'john.doe@example.com',
    'jane@company.co.uk',
    'test.email@domain.org',
    'firstname.lastname@example.com',
    'user+tag@example.com',
    'admin@subdomain.example.com',
    'test123@test.example.com',
]

for email in valid_emails:
    if is_valid_email(email):
        results.add_pass(f'Valid email accepted: "{email}"')
    else:
        results.add_fail(
            f'Valid email rejected: "{email}"',
            'Expected to be valid but was rejected'
        )

# ============================================================
# INVALID EMAIL TESTS - CONSECUTIVE DOTS BUG (CRITICAL)
# ============================================================
print_colored('\n' + '='*70, Colors.CYAN)
print_colored('TESTING INVALID EMAILS - CONSECUTIVE DOTS (BUG FIX)', Colors.CYAN, bold=True)
print_colored('='*70, Colors.CYAN)

invalid_emails = [
    ('user@domain..com', 'Double dots in domain'),
    ('user@domain...com', 'Triple dots in domain'),
    ('user..name@domain.com', 'Double dots in local part'),
    ('user@domain.co..m', 'Double dots in TLD'),
    ('.user@domain.com', 'Leading dot in local part'),
    ('user.@domain.com', 'Trailing dot in local part'),
    ('user@.domain.com', 'Leading dot in domain'),
    ('user@domain.com.', 'Trailing dot in domain'),
    ('user@domain', 'Missing TLD'),
    ('user@.com', 'Missing domain name'),
    ('@domain.com', 'Missing local part'),
    ('user name@domain.com', 'Space in local part'),
    ('user@dom ain.com', 'Space in domain'),
    ('user@@domain.com', 'Double @ symbol'),
    ('user@domain@example.com', 'Multiple @ symbols'),
]

for email, description in invalid_emails:
    if not is_valid_email(email):
        results.add_pass(f'Invalid email rejected: "{email}" ({description})')
    else:
        results.add_fail(
            f'Invalid email accepted: "{email}" ({description})',
            f'Expected to be invalid but was accepted'
        )

# ============================================================
# EDGE CASES
# ============================================================
print_colored('\n' + '='*70, Colors.CYAN)
print_colored('TESTING EDGE CASES', Colors.CYAN, bold=True)
print_colored('='*70, Colors.CYAN)

edge_cases = [
    ('a@b.c', True, 'Single character parts'),
    ('test@localhost.localdomain', True, 'Valid localhost format'),
    ('user+filter@domain.com', True, 'Email with plus addressing'),
    ('test@123.com', True, 'Domain starting with number'),
    ('', False, 'Empty string'),
    ('   ', False, 'Only spaces'),
]

for email, expected_valid, description in edge_cases:
    is_valid = is_valid_email(email)
    if is_valid == expected_valid:
        status = 'accepted' if expected_valid else 'rejected'
        results.add_pass(f'Edge case {status}: "{email}" ({description})')
    else:
        expected_str = 'valid' if expected_valid else 'invalid'
        actual_str = 'valid' if is_valid else 'invalid'
        results.add_fail(
            f'Edge case: "{email}" ({description})',
            f'Expected {expected_str} but was {actual_str}'
        )

# ============================================================
# PRINT FINAL RESULTS
# ============================================================
all_passed = results.print_summary()
print('='*70 + '\n')

# Exit with appropriate code
sys.exit(0 if all_passed else 1)
