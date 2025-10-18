"""
Tree-based Playfair matrix generation using BFS insertion and DFS traversal.
Optimized for performance with large character sets.
"""

from collections import deque
from custom_unicode import CHAR_SET
import math

class Node:
    """Binary tree node for character storage."""
    __slots__ = ['value', 'children']  # Memory optimization
    
    def __init__(self, value):
        self.value = value
        self.children = []

def build_key_tree_custom(key, char_set=CHAR_SET):
    """
    Build a tree using BFS insertion.
    Key characters are inserted first (without duplicates),
    then remaining charset characters fill the tree.
    
    Args:
        key: String key for Playfair cipher
        char_set: Character set to use (default: CHAR_SET)
    
    Returns:
        Root node of the constructed tree
    """
    # Deduplicate key while preserving order
    seen = set()
    key_chars = []
    for c in key:
        if c not in seen and c in char_set:
            key_chars.append(c)
            seen.add(c)
    
    if not key_chars:
        raise ValueError("Key must contain at least one valid character from CHAR_SET")
    
    # Get remaining characters (not in key)
    remaining_chars = [c for c in char_set if c not in seen]
    
    # Build tree using BFS
    root = Node(key_chars[0])
    queue = deque([root])
    idx = 1
    
    # Insert key characters first
    while idx < len(key_chars):
        parent = queue.popleft()
        child = Node(key_chars[idx])
        parent.children.append(child)
        queue.append(child)
        idx += 1
    
    # Insert remaining characters
    for ch in remaining_chars:
        if not queue:
            break
        parent = queue.popleft()
        child = Node(ch)
        parent.children.append(child)
        queue.append(child)
    
    return root

def dfs_traversal_custom(root):
    """
    Perform DFS traversal to extract characters in order.
    Uses iterative approach to avoid recursion depth issues.
    
    Args:
        root: Root node of the tree
    
    Returns:
        List of characters in DFS order
    """
    if not root:
        return []
    
    matrix_list = []
    stack = [root]
    
    while stack:
        node = stack.pop()
        matrix_list.append(node.value)
        # Push children in reverse to maintain left-to-right order
        for child in reversed(node.children):
            stack.append(child)
    
    return matrix_list

def build_playfair_matrix_custom(key):
    """
    Build a square Playfair matrix from the key.
    
    Args:
        key: String key for matrix generation
    
    Returns:
        2D list representing the Playfair matrix (545x545)
    """
    # Build tree and traverse
    root = build_key_tree_custom(key)
    chars = dfs_traversal_custom(root)
    
    # Calculate matrix size (should be 545)
    size = int(math.isqrt(len(chars)))
    
    # Ensure we have exactly size*size characters
    chars = chars[:size * size]
    
    # Create 2D matrix
    matrix = [chars[i:i+size] for i in range(0, size*size, size)]
    
    return matrix

def get_matrix_size():
    """Return the expected matrix dimensions."""
    return int(math.isqrt(len(CHAR_SET)))

# Self-test
if __name__ == "__main__":
    test_key = "HELLO_WORLD_123"
    try:
        matrix = build_playfair_matrix_custom(test_key)
        size = len(matrix)
        print(f"✓ Matrix generated successfully: {size}x{size}")
        print(f"✓ Total cells: {size * size}")
        print(f"✓ First row (first 10 chars): {matrix[0][:10]}")
    except Exception as e:
        print(f"✗ Error: {e}")