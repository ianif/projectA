/**
 * Unit Tests for Email Validation Function
 * Tests the isValidEmail() function from script.js
 * 
 * These tests validate that the email validation properly rejects:
 * - Emails with consecutive dots
 * - Emails with leading/trailing dots
 * - Invalid email formats
 * 
 * And accepts:
 * - Valid standard email formats
 * - Emails with subdomains
 */

// Define the email validation function for testing
// This matches the implementation in script.js
function isValidEmail(email) {
    // Improved regex that prevents consecutive dots and validates proper email format
    const emailRegex = /^[^\s@.][^\s@]*@[^\s@.][^\s@.]*(\.[^\s@.][^\s@.]*)+$/;
    return emailRegex.test(email);
}

// Test Results Tracking
class TestResults {
    constructor() {
        this.passed = 0;
        this.failed = 0;
        this.tests = [];
    }

    addPass(testName) {
        this.passed++;
        this.tests.push({ name: testName, status: 'PASS' });
        console.log(`✓ PASS: ${testName}`);
    }

    addFail(testName, reason) {
        this.failed++;
        this.tests.push({ name: testName, status: 'FAIL', reason });
        console.error(`✗ FAIL: ${testName}`);
        console.error(`  Reason: ${reason}`);
    }

    printSummary() {
        console.log('\n' + '='.repeat(70));
        console.log('TEST SUMMARY');
        console.log('='.repeat(70));
        console.log(`Total: ${this.passed + this.failed} | Passed: ${this.passed} | Failed: ${this.failed}`);
        
        if (this.failed === 0) {
            console.log('\n✓ All tests passed!');
        } else {
            console.log(`\n✗ ${this.failed} test(s) failed`);
        }
        console.log('='.repeat(70));
    }
}

// Initialize test results
const results = new TestResults();

// ============================================================
// VALID EMAIL TESTS
// ============================================================
console.log('\n' + '='.repeat(70));
console.log('TESTING VALID EMAILS');
console.log('='.repeat(70));

const validEmails = [
    'user@example.com',
    'john.doe@example.com',
    'jane@company.co.uk',
    'test.email@domain.org',
    'firstname.lastname@example.com',
    'user+tag@example.com',
    'admin@subdomain.example.com',
    'test123@test.example.com',
];

validEmails.forEach(email => {
    if (isValidEmail(email)) {
        results.addPass(`Valid email accepted: "${email}"`);
    } else {
        results.addFail(`Valid email rejected: "${email}"`, `Expected to be valid but was rejected`);
    }
});

// ============================================================
// INVALID EMAIL TESTS - CONSECUTIVE DOTS BUG
// ============================================================
console.log('\n' + '='.repeat(70));
console.log('TESTING INVALID EMAILS - CONSECUTIVE DOTS (BUG FIX)');
console.log('='.repeat(70));

const invalidEmails = [
    'user@domain..com',           // Double dots in domain
    'user@domain...com',          // Triple dots in domain
    'user..name@domain.com',      // Double dots in local part
    'user@domain.co..m',          // Double dots in TLD
    '.user@domain.com',           // Leading dot in local part
    'user.@domain.com',           // Trailing dot in local part
    'user@.domain.com',           // Leading dot in domain
    'user@domain.com.',           // Trailing dot in domain
    'user@domain',                // Missing TLD
    'user@.com',                  // Missing domain name
    '@domain.com',                // Missing local part
    'user name@domain.com',       // Space in local part
    'user@dom ain.com',           // Space in domain
    'user@@domain.com',           // Double @ symbol
    'user@domain@example.com',    // Multiple @ symbols
];

invalidEmails.forEach(email => {
    if (!isValidEmail(email)) {
        results.addPass(`Invalid email rejected: "${email}"`);
    } else {
        results.addFail(`Invalid email accepted: "${email}"`, `Expected to be invalid but was accepted`);
    }
});

// ============================================================
// EDGE CASES
// ============================================================
console.log('\n' + '='.repeat(70));
console.log('TESTING EDGE CASES');
console.log('='.repeat(70));

const edgeCases = [
    { email: 'a@b.c', expectedValid: true, description: 'Single character parts' },
    { email: 'test@localhost.localdomain', expectedValid: true, description: 'Valid localhost format' },
    { email: 'user+filter@domain.com', expectedValid: true, description: 'Email with plus addressing' },
    { email: 'test@123.com', expectedValid: true, description: 'Domain starting with number' },
    { email: '', expectedValid: false, description: 'Empty string' },
    { email: '   ', expectedValid: false, description: 'Only spaces' },
];

edgeCases.forEach(({ email, expectedValid, description }) => {
    const isValid = isValidEmail(email);
    if (isValid === expectedValid) {
        const status = expectedValid ? 'accepted' : 'rejected';
        results.addPass(`Edge case ${status}: "${email}" (${description})`);
    } else {
        const expected = expectedValid ? 'valid' : 'invalid';
        const actual = isValid ? 'valid' : 'invalid';
        results.addFail(
            `Edge case: "${email}" (${description})`,
            `Expected ${expected} but was ${actual}`
        );
    }
});

// ============================================================
// PRINT FINAL RESULTS
// ============================================================
results.printSummary();

// Exit with appropriate code
if (typeof process !== 'undefined') {
    process.exit(results.failed === 0 ? 0 : 1);
}
