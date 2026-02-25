/**
 * Unit Tests for Form Submission Functionality
 * Tests the storeFormSubmission function and localStorage handling
 */

// Mock localStorage for testing
class MockLocalStorage {
    constructor() {
        this.data = {};
    }

    getItem(key) {
        return this.data[key] || null;
    }

    setItem(key, value) {
        this.data[key] = value;
    }

    removeItem(key) {
        delete this.data[key];
    }

    clear() {
        this.data = {};
    }
}

// Replace the global localStorage with our mock
let localStorage = new MockLocalStorage();

/**
 * Fixed version of storeFormSubmission function
 * This is the corrected version that properly handles the null case
 */
function storeFormSubmission(data) {
    let submissions = JSON.parse(localStorage.getItem('formSubmissions') || '[]');
    submissions.push(data);
    localStorage.setItem('formSubmissions', JSON.stringify(submissions));
}

/**
 * Buggy version of storeFormSubmission function
 * This version has the bug: JSON.parse(null) will throw an error
 */
function storeFormSubmissionBuggy(data) {
    let submissions = JSON.parse(localStorage.getItem('formSubmissions')) || [];
    submissions.push(data);
    localStorage.setItem('formSubmissions', JSON.stringify(submissions));
}

// Test suite
class TestSuite {
    constructor() {
        this.passedTests = 0;
        this.failedTests = 0;
        this.tests = [];
    }

    test(name, testFn) {
        this.tests.push({ name, testFn });
    }

    run() {
        console.log('===================================');
        console.log('Form Submission Unit Tests');
        console.log('===================================\n');

        this.tests.forEach(test => {
            try {
                test.testFn();
                this.passedTests++;
                console.log(`✓ PASS: ${test.name}`);
            } catch (error) {
                this.failedTests++;
                console.log(`✗ FAIL: ${test.name}`);
                console.log(`  Error: ${error.message}\n`);
            }
        });

        console.log('\n===================================');
        console.log(`Results: ${this.passedTests} passed, ${this.failedTests} failed`);
        console.log('===================================\n');

        return this.failedTests === 0;
    }

    assert(condition, message) {
        if (!condition) {
            throw new Error(message);
        }
    }

    assertEqual(actual, expected, message) {
        if (actual !== expected) {
            throw new Error(`${message}: expected ${expected}, got ${actual}`);
        }
    }
}

// Create test suite
const suite = new TestSuite();

// Test 1: Buggy version should throw error on first submission
suite.test('Buggy version throws error on first submission (demonstrates the bug)', () => {
    const mockStorage = new MockLocalStorage();
    
    // Override localStorage temporarily
    const originalStorage = global.localStorage;
    global.localStorage = mockStorage;
    
    const testData = {
        name: 'Test User',
        email: 'test@example.com',
        message: 'Test message',
        timestamp: '2024-01-01'
    };
    
    try {
        storeFormSubmissionBuggy(testData);
        // If we get here, the test failed because we expected an error
        global.localStorage = originalStorage;
        throw new Error('Expected TypeError to be thrown but none was thrown');
    } catch (error) {
        global.localStorage = originalStorage;
        // We expect a TypeError here
        suite.assert(
            error instanceof TypeError || error.message.includes('SyntaxError'),
            'Expected TypeError or SyntaxError when calling JSON.parse(null)'
        );
    }
});

// Test 2: Fixed version should succeed on first submission
suite.test('Fixed version succeeds on first submission', () => {
    localStorage.clear();
    
    const testData = {
        name: 'Test User',
        email: 'test@example.com',
        message: 'Test message',
        timestamp: '2024-01-01'
    };
    
    // This should not throw an error
    storeFormSubmission(testData);
    
    // Verify data was stored
    const stored = localStorage.getItem('formSubmissions');
    suite.assert(stored !== null, 'Data should be stored in localStorage');
    
    const submissions = JSON.parse(stored);
    suite.assert(Array.isArray(submissions), 'Stored data should be an array');
    suite.assertEqual(submissions.length, 1, 'Should have 1 submission');
    suite.assertEqual(submissions[0].name, 'Test User', 'Name should match');
});

// Test 3: Fixed version handles multiple submissions
suite.test('Fixed version correctly appends multiple submissions', () => {
    localStorage.clear();
    
    const testData1 = {
        name: 'User One',
        email: 'user1@example.com',
        message: 'First message',
        timestamp: '2024-01-01'
    };
    
    const testData2 = {
        name: 'User Two',
        email: 'user2@example.com',
        message: 'Second message',
        timestamp: '2024-01-02'
    };
    
    storeFormSubmission(testData1);
    storeFormSubmission(testData2);
    
    const stored = localStorage.getItem('formSubmissions');
    const submissions = JSON.parse(stored);
    
    suite.assertEqual(submissions.length, 2, 'Should have 2 submissions');
    suite.assertEqual(submissions[0].name, 'User One', 'First submission name should match');
    suite.assertEqual(submissions[1].name, 'User Two', 'Second submission name should match');
});

// Test 4: Fixed version preserves existing submissions
suite.test('Fixed version preserves existing submissions when adding new ones', () => {
    localStorage.clear();
    
    // Pre-populate with existing submission
    const existingSubmissions = [
        {
            name: 'Existing User',
            email: 'existing@example.com',
            message: 'Existing message',
            timestamp: '2023-12-31'
        }
    ];
    localStorage.setItem('formSubmissions', JSON.stringify(existingSubmissions));
    
    // Add new submission
    const newData = {
        name: 'New User',
        email: 'new@example.com',
        message: 'New message',
        timestamp: '2024-01-01'
    };
    
    storeFormSubmission(newData);
    
    const stored = localStorage.getItem('formSubmissions');
    const submissions = JSON.parse(stored);
    
    suite.assertEqual(submissions.length, 2, 'Should have 2 submissions');
    suite.assertEqual(submissions[0].name, 'Existing User', 'Existing submission should be preserved');
    suite.assertEqual(submissions[1].name, 'New User', 'New submission should be added');
});

// Test 5: Fixed version handles empty/null scenario correctly
suite.test('Fixed version creates empty array when localStorage is empty', () => {
    localStorage.clear();
    
    // Verify localStorage is empty
    suite.assert(
        localStorage.getItem('formSubmissions') === null,
        'localStorage should be empty initially'
    );
    
    // Add first submission
    const testData = {
        name: 'First User',
        email: 'first@example.com',
        message: 'First message',
        timestamp: '2024-01-01'
    };
    
    storeFormSubmission(testData);
    
    const stored = localStorage.getItem('formSubmissions');
    suite.assert(stored !== null, 'Data should now be stored');
    
    const submissions = JSON.parse(stored);
    suite.assertEqual(submissions.length, 1, 'Should have exactly 1 submission');
});

// Run all tests
suite.run();
