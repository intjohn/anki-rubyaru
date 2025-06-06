from __init__ import get_rubied_kanji

def run_test(test_input: str, expected_output: str) -> bool:
    result = get_rubied_kanji(test_input)
    passed = result == expected_output
    print(f"Test: {test_input!r}")
    print(f"Expected: {expected_output!r}")
    print(f"Got: {result!r}")
    print(f"{'✓ PASS' if passed else '✗ FAIL'}\n")
    return passed

# Test cases
tests = [
    # Basic cases
    ("多[た]分[ぶん]", "多分"),              # Basic ruby annotation
    ("たぶん", ""),                         # No ruby, only hiragana
    ("多分", ""),                          # No ruby, kanji without annotation
    
    # Mixed cases
    ("今日[きょう]はたぶんいい天気[てんき]です", "今日はたぶんいい天気です"),  # Mixed ruby and plain text
    ("漢[かん]字[じ]と仮[か]名[な]", "漢字と仮名"),  # Multiple ruby annotations with plain text
    
    # Edge cases
    ("", ""),                             # Empty string
    ("漢字[かんじ", ""),                    # Incomplete ruby
    ("漢字]かんじ[", ""),                   # Malformed ruby
    ("漢[かん]字[じ]送[おく]り[り]仮[か]名[な]", "漢字送り仮名"),  # Consecutive ruby
    ("今日[きょう] は 明日[あした]", "今日 は 明日"),  # Spaces between ruby
]

# Run tests
passed = 0
total = len(tests)

print("Running tests for detect_kana function...\n")
for input_text, expected in tests:
    if run_test(input_text, expected):
        passed += 1

print(f"Test summary: {passed}/{total} tests passed") 