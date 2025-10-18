"""
Extended Playfair cipher implementation (16x16 = 256 character matrix).
DEPRECATED: This module is kept for backward compatibility but is not used
in the main hybrid cryptosystem. Use custom_playfair.py instead.
"""

import warnings

warnings.warn(
    "extended_playfair.py is deprecated. Use custom_playfair.py for the 545x545 matrix instead.",
    DeprecationWarning,
    stacklevel=2
)

# Note: The build_playfair_matrix_extended function referenced here
# would need to be implemented separately if this legacy code is needed.
# For now, this file is provided as a placeholder to maintain file structure.

def format_plaintext_extended(text):
    """Format plaintext for 16x16 Playfair encryption."""
    if len(text) % 2 != 0:
        text += '\x00'
    return text

def find_position_extended(matrix, char):
    """Find character position in 16x16 matrix."""
    for i, row in enumerate(matrix):
        for j, c in enumerate(row):
            if c == char:
                return i, j
    return None

def playfair_encrypt_extended(plaintext, key):
    """
    DEPRECATED: Use playfair_encrypt_custom instead.
    This function is for 16x16 matrix only.
    """
    raise NotImplementedError(
        "Extended Playfair (16x16) is deprecated. "
        "Use custom_playfair.playfair_encrypt_custom() for 545x545 matrix."
    )

def playfair_decrypt_extended(cipher_text, key):
    """
    DEPRECATED: Use playfair_decrypt_custom instead.
    This function is for 16x16 matrix only.
    """
    raise NotImplementedError(
        "Extended Playfair (16x16) is deprecated. "
        "Use custom_playfair.playfair_decrypt_custom() for 545x545 matrix."
    )

if __name__ == "__main__":
    print("⚠️  This module is deprecated.")
    print("Use custom_playfair.py for the main 545x545 Playfair implementation.")