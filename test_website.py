#!/usr/bin/env python3
"""
Gynecologist Website Testing and Benchmarking Suite
Validates file structure, syntax, and performance
"""

import os
import sys
import json
import time
import re
from pathlib import Path
from typing import List, Dict, Tuple
import argparse
from html.parser import HTMLParser

# ANSI Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_colored(text, color, bold=False):
    """Print colored text"""
    prefix = f"{Colors.BOLD}" if bold else ""
    print(f"{prefix}{color}{text}{Colors.RESET}")

def print_header(title):
    """Print section header"""
    print("\n" + "="*80)
    print_colored(f"  {title}", Colors.CYAN, bold=True)
    print("="*80)

def print_success(message):
    """Print success message"""
    print(f"{Colors.GREEN}✓{Colors.RESET} {message}")

def print_error(message):
    """Print error message"""
    print(f"{Colors.RED}✗{Colors.RESET} {message}")

def print_warning(message):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠{Colors.RESET} {message}")

def print_info(message):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ{Colors.RESET} {message}")

class TestResults:
    """Store test results"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.errors = []
        self.warnings_list = []

    def add_pass(self):
        self.passed += 1

    def add_fail(self, error):
        self.failed += 1
        self.errors.append(error)

    def add_warning(self, warning):
        self.warnings += 1
        self.warnings_list.append(warning)

    def print_summary(self):
        """Print test summary"""
        print("\n" + "-"*80)
        print(f"Results: {Colors.GREEN}{self.passed} passed{Colors.RESET}, " +
              f"{Colors.RED}{self.failed} failed{Colors.RESET}, " +
              f"{Colors.YELLOW}{self.warnings} warnings{Colors.RESET}")
        
        if self.errors:
            print(f"\n{Colors.RED}Errors:{Colors.RESET}")
            for i, error in enumerate(self.errors, 1):
                print(f"  {i}. {error}")
        
        if self.warnings_list:
            print(f"\n{Colors.YELLOW}Warnings:{Colors.RESET}")
            for i, warning in enumerate(self.warnings_list, 1):
                print(f"  {i}. {warning}")

class HTMLValidator(HTMLParser):
    """Basic HTML structure validator"""
    def __init__(self):
        super().__init__()
        self.tags = []
        self.has_doctype = False
        self.lang_attr = None
        self.charset = False

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        if tag == "html":
            attrs_dict = dict(attrs)
            self.lang_attr = attrs_dict.get('lang')

    def handle_startendtag(self, tag, attrs):
        if tag == "meta":
            attrs_dict = dict(attrs)
            if attrs_dict.get('charset') == 'UTF-8':
                self.charset = True

def test_file_structure(results: TestResults) -> None:
    """Test if all required files exist"""
    print_header("File Structure Test")
    
    required_files = [
        'index.html',
        'styles.css',
        'script.js',
        'README.md',
        'SETUP_INSTRUCTIONS.txt',
    ]
    
    required_images = [
        'images/logo.svg',
        'images/hero-banner.svg',
        'images/doctor-profile.svg',
        'images/service-1.svg',
        'images/service-2.svg',
        'images/service-3.svg',
        'images/service-4.svg',
    ]
    
    # Check main files
    for filename in required_files:
        if os.path.isfile(filename):
            size = os.path.getsize(filename)
            print_success(f"{filename} ({size} bytes)")
            results.add_pass()
        else:
            print_error(f"{filename} - NOT FOUND")
            results.add_fail(f"Missing file: {filename}")
    
    # Check images
    for image in required_images:
        if os.path.isfile(image):
            size = os.path.getsize(image)
            print_success(f"{image} ({size} bytes)")
            results.add_pass()
        else:
            print_error(f"{image} - NOT FOUND")
            results.add_fail(f"Missing image: {image}")

def test_html_validity(results: TestResults) -> None:
    """Test HTML validity"""
    print_header("HTML Validation Test")
    
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Basic structure checks
        checks = [
            ('<!DOCTYPE html>' in html_content, 'DOCTYPE declaration'),
            ('<html' in html_content, 'HTML tag'),
            ('<head>' in html_content, 'HEAD tag'),
            ('<body>' in html_content, 'BODY tag'),
            ('<meta charset="UTF-8">' in html_content, 'UTF-8 charset'),
            ('lang="el"' in html_content, 'Greek language attribute'),
            ('<title>' in html_content, 'Title tag'),
            ('index.html' not in html_content.lower() or '<title>' in html_content, 'Has title'),
        ]
        
        for check, name in checks:
            if check:
                print_success(f"HTML has {name}")
                results.add_pass()
            else:
                print_warning(f"HTML missing {name}")
                results.add_warning(f"HTML missing {name}")
        
        # Check for required sections
        sections = [
            ('<nav', 'Navigation'),
            ('<section id="home"', 'Home section'),
            ('<section id="about"', 'About/Biography section'),
            ('<section id="services"', 'Services section'),
            ('<section id="contact"', 'Contact section'),
            ('<footer', 'Footer'),
        ]
        
        for tag, name in sections:
            if tag in html_content:
                print_success(f"HTML contains {name}")
                results.add_pass()
            else:
                print_error(f"Missing {name} section")
                results.add_fail(f"Missing {name} section")
        
    except Exception as e:
        print_error(f"Error reading HTML: {e}")
        results.add_fail(f"HTML reading error: {e}")

def test_css_validity(results: TestResults) -> None:
    """Test CSS file validity"""
    print_header("CSS Validation Test")
    
    try:
        with open('styles.css', 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        # Check for common CSS features
        checks = [
            ('body {' in css_content, 'Body styles'),
            ('media' in css_content.lower(), 'Media queries'),
            ('@media' in css_content, 'Responsive design'),
            ('max-width' in css_content, 'Max-width declarations'),
            ('color' in css_content, 'Color declarations'),
            ('background' in css_content, 'Background styling'),
            ('flex' in css_content or 'grid' in css_content, 'Modern layout'),
        ]
        
        for check, name in checks:
            if check:
                print_success(f"CSS contains {name}")
                results.add_pass()
            else:
                print_warning(f"CSS missing {name}")
                results.add_warning(f"CSS missing {name}")
        
        # Count CSS rules
        rule_count = len(re.findall(r'\{', css_content))
        print_info(f"CSS contains approximately {rule_count} rules")
        
        # Check for responsive breakpoints
        if '768px' in css_content or 'tablet' in css_content.lower():
            print_success("Contains tablet breakpoint")
            results.add_pass()
        else:
            print_warning("No tablet breakpoint found")
            results.add_warning("No tablet breakpoint (768px) found")
        
        if '480px' in css_content or 'mobile' in css_content.lower():
            print_success("Contains mobile breakpoint")
            results.add_pass()
        else:
            print_warning("No mobile breakpoint found")
            results.add_warning("No mobile breakpoint (480px) found")
        
    except Exception as e:
        print_error(f"Error reading CSS: {e}")
        results.add_fail(f"CSS reading error: {e}")

def test_javascript_validity(results: TestResults) -> None:
    """Test JavaScript file validity"""
    print_header("JavaScript Validation Test")
    
    try:
        with open('script.js', 'r', encoding='utf-8') as f:
            js_content = f.read()
        
        # Check for key JavaScript features
        checks = [
            ('document.addEventListener' in js_content, 'Event listeners'),
            ('function' in js_content or '=>' in js_content, 'Functions'),
            ('getElementById' in js_content or 'querySelector' in js_content, 'DOM selection'),
            ('form' in js_content.lower(), 'Form handling'),
            ('validation' in js_content.lower() or 'validate' in js_content.lower(), 'Form validation'),
            ('localStorage' in js_content, 'Data persistence'),
            ('IntersectionObserver' in js_content, 'Modern API usage'),
        ]
        
        for check, name in checks:
            if check:
                print_success(f"JavaScript contains {name}")
                results.add_pass()
            else:
                print_warning(f"JavaScript missing {name}")
                results.add_warning(f"JavaScript missing {name}")
        
        # Count functions/features
        function_count = len(re.findall(r'function\s+\w+|const\s+\w+\s*=\s*(?:function|\()', js_content))
        print_info(f"JavaScript contains approximately {function_count} functions/features")
        
        # Check for accessibility features
        if 'aria' in js_content.lower() or 'role=' in js_content.lower():
            print_success("Contains accessibility attributes")
            results.add_pass()
        else:
            print_warning("Limited accessibility features in JavaScript")
            results.add_warning("Limited ARIA/accessibility features")
        
    except Exception as e:
        print_error(f"Error reading JavaScript: {e}")
        results.add_fail(f"JavaScript reading error: {e}")

def test_content_validation(results: TestResults) -> None:
    """Test content validity (Greek text, etc.)"""
    print_header("Content Validation Test")
    
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Check for Greek content
        greek_words = [
            'Αρχική',
            'Βιογραφικό',
            'Υπηρεσίες',
            'Επικοινωνία',
            'Γυναικολογία',
            'Γυναικολόγος',
            'Υπερηχογραφίες',
        ]
        
        greek_found = sum(1 for word in greek_words if word in html_content)
        
        if greek_found >= len(greek_words) * 0.7:
            print_success(f"Found {greek_found}/{len(greek_words)} required Greek terms")
            results.add_pass()
        else:
            print_warning(f"Only found {greek_found}/{len(greek_words)} Greek terms")
            results.add_warning(f"Missing some Greek content: {greek_found}/{len(greek_words)} terms")
        
        # Check for contact information
        if '+30' in html_content or 'phone' in html_content.lower():
            print_success("Contains phone number")
            results.add_pass()
        else:
            print_warning("Missing phone number")
        
        if 'email' in html_content.lower() or '@' in html_content:
            print_success("Contains email")
            results.add_pass()
        else:
            print_warning("Missing email")
        
        if 'form' in html_content.lower() or '<input' in html_content:
            print_success("Contains contact form")
            results.add_pass()
        else:
            print_error("No contact form found")
            results.add_fail("No contact form in HTML")
        
    except Exception as e:
        print_error(f"Error validating content: {e}")
        results.add_fail(f"Content validation error: {e}")

def test_file_sizes(results: TestResults) -> None:
    """Test file sizes and performance"""
    print_header("File Size Analysis")
    
    files_to_check = [
        ('index.html', 100000),  # 100KB max
        ('styles.css', 100000),
        ('script.js', 100000),
    ]
    
    total_size = 0
    
    for filename, max_size in files_to_check:
        if os.path.isfile(filename):
            size = os.path.getsize(filename)
            total_size += size
            
            if size < max_size:
                print_success(f"{filename}: {size} bytes (within limit)")
                results.add_pass()
            else:
                print_warning(f"{filename}: {size} bytes (exceeds {max_size} bytes)")
                results.add_warning(f"{filename} exceeds recommended size")
    
    # Check images
    if os.path.isdir('images'):
        image_size = 0
        image_count = 0
        
        for img_file in Path('images').glob('*.svg'):
            size = img_file.stat().st_size
            image_size += size
            image_count += 1
        
        if image_count > 0:
            print_success(f"Images: {image_count} files, {image_size} bytes total")
            results.add_pass()
        
        total_size += image_size
    
    print_info(f"Total project size: {total_size} bytes ({total_size/1024:.2f} KB)")
    
    if total_size < 500000:  # 500KB
        print_success("Total size is within acceptable range (< 500KB)")
        results.add_pass()
    else:
        print_warning(f"Total size is {total_size/1024:.2f} KB (recommended < 500KB)")

def test_documentation(results: TestResults) -> None:
    """Test documentation files"""
    print_header("Documentation Test")
    
    # Check README
    if os.path.isfile('README.md'):
        with open('README.md', 'r', encoding='utf-8') as f:
            readme = f.read()
        
        required_sections = [
            'Overview',
            'Features',
            'Quick Start',
            'Installation',
            'Contact',
        ]
        
        for section in required_sections:
            if section.lower() in readme.lower():
                print_success(f"README contains '{section}' section")
                results.add_pass()
            else:
                print_warning(f"README missing '{section}' section")
                results.add_warning(f"README missing '{section}' section")
    
    # Check SETUP_INSTRUCTIONS
    if os.path.isfile('SETUP_INSTRUCTIONS.txt'):
        with open('SETUP_INSTRUCTIONS.txt', 'r', encoding='utf-8') as f:
            setup = f.read()
        
        required_sections = [
            'System Requirements',
            'Installation',
            'Running',
            'Troubleshooting',
        ]
        
        for section in required_sections:
            if section in setup:
                print_success(f"SETUP_INSTRUCTIONS contains '{section}' section")
                results.add_pass()
            else:
                print_warning(f"SETUP_INSTRUCTIONS missing '{section}' section")
                results.add_warning(f"SETUP_INSTRUCTIONS missing '{section}' section")

def benchmark_performance(results: TestResults) -> None:
    """Run performance benchmarks"""
    print_header("Performance Benchmarking")
    
    # Simulate page load timing
    times = {
        'HTML Parse': 0,
        'CSS Load': 0,
        'JavaScript Load': 0,
        'Images Load': 0,
        'Total': 0
    }
    
    start_time = time.time()
    
    # Simulate HTML parsing
    if os.path.isfile('index.html'):
        with open('index.html', 'r', encoding='utf-8') as f:
            f.read()
    times['HTML Parse'] = (time.time() - start_time) * 1000
    
    # Simulate CSS loading
    parse_start = time.time()
    if os.path.isfile('styles.css'):
        with open('styles.css', 'r', encoding='utf-8') as f:
            f.read()
    times['CSS Load'] = (time.time() - parse_start) * 1000
    
    # Simulate JS loading
    parse_start = time.time()
    if os.path.isfile('script.js'):
        with open('script.js', 'r', encoding='utf-8') as f:
            f.read()
    times['JavaScript Load'] = (time.time() - parse_start) * 1000
    
    # Simulate image loading
    parse_start = time.time()
    if os.path.isdir('images'):
        for img_file in Path('images').glob('*.svg'):
            with open(img_file, 'r', encoding='utf-8') as f:
                f.read()
    times['Images Load'] = (time.time() - parse_start) * 1000
    
    times['Total'] = time.time() - start_time
    
    # Print results
    for resource, timing in times.items():
        if resource == 'Total':
            print_info(f"{resource}: {timing*1000:.2f}ms")
        else:
            print_info(f"{resource}: {timing:.2f}ms")
        results.add_pass()
    
    # Recommendations
    if times['Total'] < 0.5:
        print_success("Excellent load time performance")
        results.add_pass()
    elif times['Total'] < 1.0:
        print_success("Good load time performance")
        results.add_pass()
    else:
        print_warning("Load time could be optimized")

def run_all_tests(verbose=False) -> TestResults:
    """Run all tests"""
    results = TestResults()
    
    print_colored("\n" + "="*80, Colors.CYAN, bold=True)
    print_colored("GYNECOLOGIST WEBSITE TEST SUITE", Colors.CYAN, bold=True)
    print_colored("="*80, Colors.CYAN)
    
    # Run tests
    test_file_structure(results)
    test_html_validity(results)
    test_css_validity(results)
    test_javascript_validity(results)
    test_content_validation(results)
    test_file_sizes(results)
    test_documentation(results)
    benchmark_performance(results)
    
    # Print summary
    results.print_summary()
    
    # Final status
    print("\n" + "="*80)
    if results.failed == 0:
        print_success("All tests passed! ✓")
    else:
        print_error(f"Tests failed with {results.failed} error(s)")
    print("="*80 + "\n")
    
    return results

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Gynecologist Website Testing Suite',
        epilog='Run with --help for more options'
    )
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--benchmark', '-b', action='store_true', help='Run benchmarks only')
    
    args = parser.parse_args()
    
    results = run_all_tests(verbose=args.verbose)
    
    # Exit with appropriate code
    sys.exit(0 if results.failed == 0 else 1)
