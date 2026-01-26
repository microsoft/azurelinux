#!/usr/bin/env python3
"""
Simple test to validate HtmlReportGenerator JavaScript syntax.
Run this before committing to catch syntax errors early.
"""

import sys
import subprocess
import tempfile
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from HtmlReportGenerator import HtmlReportGenerator


def test_javascript_syntax():
    """Test that generated JavaScript has valid syntax."""
    print("🧪 Testing JavaScript syntax validation...")
    
    # Create a mock report generator with stub functions
    def mock_color(severity):
        return "#ff0000"
    
    def mock_emoji(severity):
        return "⚠️"
    
    generator = HtmlReportGenerator(
        severity_color_fn=mock_color,
        severity_emoji_fn=mock_emoji
    )
    
    # Generate JavaScript with a test PR number
    try:
        javascript = generator._get_javascript(pr_number=14946)
        print(f"✅ JavaScript generated ({len(javascript)} chars)")
    except Exception as e:
        print(f"❌ Failed to generate JavaScript: {e}")
        return False
    
    # Write to a temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
        f.write(javascript)
        js_file = f.name
    
    print(f"📝 Wrote JavaScript to: {js_file}")
    
    # Use Node.js to check syntax (if available)
    try:
        result = subprocess.run(
            ['node', '--check', js_file],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            print("✅ JavaScript syntax is valid!")
            return True
        else:
            print(f"❌ JavaScript syntax error:\n{result.stderr}")
            return False
            
    except FileNotFoundError:
        print("⚠️  Node.js not found - skipping syntax check")
        print("   Install Node.js to enable JavaScript validation")
        return True  # Don't fail if Node isn't available
        
    except subprocess.TimeoutExpired:
        print("❌ Syntax check timed out")
        return False
        
    except Exception as e:
        print(f"❌ Error running syntax check: {e}")
        return False


def test_html_generation():
    """Test that complete HTML page can be generated."""
    print("\n🧪 Testing full HTML generation...")
    
    # Create mock functions
    def mock_color(severity):
        return "#ff0000"
    
    def mock_emoji(severity):
        return "⚠️"
    
    generator = HtmlReportGenerator(
        severity_color_fn=mock_color,
        severity_emoji_fn=mock_emoji
    )
    
    # Create minimal report body
    report_body = """
    <div class="report-section">
        <h2>Test Report</h2>
        <p>This is a test.</p>
    </div>
    """
    
    try:
        html = generator.generate_complete_page(
            report_body=report_body,
            pr_number=14946
        )
        print(f"✅ HTML generated ({len(html)} chars)")
        
        # Basic sanity checks
        assert '<!DOCTYPE html>' in html, "Missing DOCTYPE"
        assert '<script>' in html, "Missing script tag"
        assert 'const pr_number = 14946;' in html, "PR number not injected correctly"
        assert 'RADAR_AUTH' in html, "Missing RADAR_AUTH module"
        
        print("✅ HTML structure looks good")
        return True
        
    except Exception as e:
        print(f"❌ Failed to generate HTML: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    print("=" * 60)
    print("HTML Report Generator - Validation Tests")
    print("=" * 60)
    
    success = True
    
    success &= test_javascript_syntax()
    success &= test_html_generation()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ ALL TESTS PASSED")
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED")
        sys.exit(1)
