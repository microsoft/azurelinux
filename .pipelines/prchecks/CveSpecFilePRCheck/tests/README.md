# CveSpecFilePRCheck Test Suite

This directory contains the comprehensive test suite for the CVE Spec File PR Check pipeline.

## Test Organization

## Running Tests

### Using the Test Runner Script

From the CveSpecFilePRCheck directory:

```bash
# Run all tests
python tests/run_all_tests.py

# Or make it executable and run directly
chmod +x tests/run_all_tests.py
./tests/run_all_tests.py
```
# Run all tests
python -m unittest discover tests

# Run specific test file
python -m unittest tests.test_antipattern_detector

# Run specific test class
python -m unittest tests.test_antipattern_detector.TestAntiPatternDetector

# Run specific test method
python -m unittest tests.test_antipattern_detector.TestAntiPatternDetector.test_missing_patch_file

# Run with verbose output
python -m unittest discover tests -v