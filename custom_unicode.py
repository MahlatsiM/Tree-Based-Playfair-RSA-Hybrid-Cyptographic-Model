"""
Custom Unicode character set generator for Playfair cipher.
Creates a valid character set of exactly 297,025 characters (545x545 matrix).
"""

def is_valid_unicode(code_point):
    """Check if a Unicode code point is valid and safe to use."""
    # Exclude surrogate pairs (0xD800-0xDFFF)
    if 0xD800 <= code_point <= 0xDFFF:
        return False
    # Exclude private use areas that cause issues
    if 0xE000 <= code_point <= 0xF8FF:  # Private Use Area
        return False
    if 0xF0000 <= code_point <= 0xFFFFD:  # Supplementary Private Use Area-A
        return False
    if 0x100000 <= code_point <= 0x10FFFD:  # Supplementary Private Use Area-B
        return False
    # Exclude non-characters
    if code_point & 0xFFFE == 0xFFFE:  # Non-characters
        return False
    return True

# Build valid Unicode character set
unicode_chars = []
for i in range(0x110000):  # Full Unicode range
    if is_valid_unicode(i):
        try:
            char = chr(i)
            # Test if character can be encoded/decoded
            char.encode('utf-8').decode('utf-8')
            unicode_chars.append(char)
        except (ValueError, UnicodeEncodeError, UnicodeDecodeError):
            continue

# Remove problematic emoji ranges (Travel & Places)
travel_places = set(chr(i) for i in range(0x1F680, 0x1F700) if is_valid_unicode(i))

# Remove rarely used object/tool emojis
rare_objects_tools = {
    '🪕', '🛖', '🪙', '🪁', '🛷', '🧿', '🪄', '🪤', '⛽', '⚖️',
    '🛹', '🛶', '🛺', '🛻', '🪃'
}

# Filter out problematic characters
filtered_chars = [c for c in unicode_chars 
                  if c not in travel_places and c not in rare_objects_tools]

# Ensure basic ASCII is included and prioritized
basic_ascii = [chr(i) for i in range(128)]
final_chars = []

# Add ASCII first
for c in basic_ascii:
    if c in filtered_chars:
        final_chars.append(c)
        filtered_chars.remove(c)

# Add remaining characters
final_chars.extend(filtered_chars)

# Truncate to exactly 297,025 characters (545 * 545)
CHAR_SET = final_chars[:297025]

# Validate
assert len(CHAR_SET) == 297025, f"Character set size mismatch: {len(CHAR_SET)}"
assert len(CHAR_SET) == len(set(CHAR_SET)), "Duplicate characters found in CHAR_SET"

print(f"✓ Character set initialized: {len(CHAR_SET)} unique characters")
print(f"✓ Matrix size will be: 545x545")