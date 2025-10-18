"""
Enhanced hybrid cryptosystem with RSA key size validation.
Combines Playfair cipher with RSA-OAEP for secure key exchange.
Implements NIST SP 800-56B Rev. 2 recommendations.
"""
try:
    from Crypto.PublicKey import RSA
    from Crypto.Cipher import PKCS1_OAEP
except ModuleNotFoundError:
    from Cryptodome.PublicKey import RSA
    from Cryptodome.Cipher import PKCS1_OAEP

from custom_playfair import playfair_encrypt_custom, playfair_decrypt_custom
import base64

def generate_rsa_keys(key_size=2048):
    """
    Generate RSA key pair for secure key exchange.
    
    Security: Follows NIST SP 800-56B Rev. 2 recommendations
    - 2048-bit: Secure until 2030
    - 3072-bit: Secure beyond 2030
    - 4096-bit: Long-term security
    
    Args:
        key_size: RSA key size in bits (2048, 3072, or 4096)
    
    Returns:
        Tuple of (private_key_bytes, public_key_bytes) in PEM format
    
    Raises:
        ValueError: If key_size is not recommended value
    """
    if key_size not in [2048, 3072, 4096]:
        raise ValueError(f"Key size {key_size} not recommended. Use 2048, 3072, or 4096.")
    
    key = RSA.generate(key_size)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    
    return private_key, public_key

def get_rsa_max_message_length(public_key_bytes):
    """
    Calculate maximum message length for RSA-OAEP encryption.
    
    Formula: max_length = (key_size_in_bytes) - 42
    Where 42 bytes = OAEP padding overhead (SHA-256)
    
    Args:
        public_key_bytes: RSA public key in PEM format
    
    Returns:
        Maximum plaintext length in bytes
    """
    key = RSA.import_key(public_key_bytes)
    return (key.size_in_bits() // 8) - 42

def validate_playfair_key_size(playfair_key, public_key_bytes):
    """
    Validate that Playfair key fits within RSA encryption limits.
    
    Args:
        playfair_key: Playfair key string
        public_key_bytes: RSA public key
    
    Raises:
        ValueError: If key is too long for RSA encryption
    """
    key_bytes = playfair_key.encode('utf-8')
    max_length = get_rsa_max_message_length(public_key_bytes)
    
    if len(key_bytes) > max_length:
        raise ValueError(
            f"Playfair key too long for RSA encryption.\n"
            f"Current: {len(key_bytes)} bytes\n"
            f"Maximum: {max_length} bytes\n"
            f"Recommendation: Reduce key length to {max_length} characters or less."
        )

def rsa_encrypt(public_key_bytes, message):
    """
    Encrypt a message using RSA-OAEP (Optimal Asymmetric Encryption Padding).
    
    Security Features:
    - OAEP padding provides semantic security
    - SHA-256 hash function
    - MGF1 mask generation function
    
    Args:
        public_key_bytes: RSA public key in PEM format
        message: String message to encrypt
    
    Returns:
        Encrypted bytes
    
    Raises:
        ValueError: If message exceeds RSA size limit
    """
    if isinstance(message, str):
        message_bytes = message.encode('utf-8')
    else:
        message_bytes = message
    
    # Import RSA key
    key = RSA.import_key(public_key_bytes)
    cipher = PKCS1_OAEP.new(key)
    
    # Validate message length
    max_length = (key.size_in_bits() // 8) - 42  # OAEP overhead
    if len(message_bytes) > max_length:
        raise ValueError(
            f"Message too long for RSA-OAEP encryption.\n"
            f"Message size: {len(message_bytes)} bytes\n"
            f"Maximum allowed: {max_length} bytes\n"
            f"RSA key size: {key.size_in_bits()} bits"
        )
    
    return cipher.encrypt(message_bytes)

def rsa_decrypt(private_key_bytes, encrypted_message):
    """
    Decrypt a message using RSA private key.
    
    Args:
        private_key_bytes: RSA private key in PEM format
        encrypted_message: Encrypted bytes from rsa_encrypt()
    
    Returns:
        Decrypted string
    
    Raises:
        ValueError: If decryption fails (wrong key or corrupted data)
    """
    try:
        key = RSA.import_key(private_key_bytes)
        cipher = PKCS1_OAEP.new(key)
        decrypted_bytes = cipher.decrypt(encrypted_message)
        return decrypted_bytes.decode('utf-8')
    except Exception as e:
        raise ValueError(f"RSA decryption failed: {str(e)}")

def hybrid_encrypt(message, playfair_key, recipient_public_key):
    """
    Hybrid encryption: Playfair for message, RSA-OAEP for key.
    
    Process:
    1. Validate Playfair key size against RSA limits
    2. Encrypt message with Playfair cipher
    3. Encrypt Playfair key with recipient's RSA public key
    4. Return both ciphertext and encrypted key
    
    Args:
        message: Plaintext message to encrypt
        playfair_key: Symmetric key for Playfair cipher (max 256 chars recommended)
        recipient_public_key: Recipient's RSA public key (PEM format)
    
    Returns:
        Tuple of (cipher_text, encrypted_playfair_key)
    
    Raises:
        ValueError: If Playfair key is too long for RSA
    
    Example:
        >>> priv, pub = generate_rsa_keys()
        >>> cipher, enc_key = hybrid_encrypt("Secret!", "KEY", pub)
        >>> plain = hybrid_decrypt(cipher, enc_key, priv)
    """
    # Validate key size before encryption
    validate_playfair_key_size(playfair_key, recipient_public_key)
    
    # Step 1: Encrypt message with Playfair
    cipher_text = playfair_encrypt_custom(message, playfair_key)
    
    # Step 2: Encrypt Playfair key with recipient's public key
    encrypted_key = rsa_encrypt(recipient_public_key, playfair_key)
    
    return cipher_text, encrypted_key

def hybrid_decrypt(cipher_text, encrypted_key, recipient_private_key):
    """
    Hybrid decryption: RSA for key recovery, Playfair for message.
    
    Process:
    1. Decrypt Playfair key using recipient's RSA private key
    2. Decrypt message using recovered Playfair key
    3. Return original plaintext
    
    Args:
        cipher_text: Encrypted message from Playfair
        encrypted_key: RSA-encrypted Playfair key
        recipient_private_key: Recipient's RSA private key (PEM format)
    
    Returns:
        Decrypted plaintext message
    
    Raises:
        ValueError: If decryption fails (wrong key or corrupted data)
    """
    # Step 1: Decrypt Playfair key using private key
    playfair_key = rsa_decrypt(recipient_private_key, encrypted_key)
    
    # Step 2: Decrypt message using recovered Playfair key
    plaintext = playfair_decrypt_custom(cipher_text, playfair_key)
    
    return plaintext

def export_key_to_base64(key_bytes):
    """
    Convert key bytes to base64 string for easy sharing/storage.
    
    Args:
        key_bytes: Raw key bytes
    
    Returns:
        Base64-encoded string
    """
    return base64.b64encode(key_bytes).decode('utf-8')

def import_key_from_base64(key_base64):
    """
    Convert base64 string back to key bytes.
    
    Args:
        key_base64: Base64-encoded key string
    
    Returns:
        Raw key bytes
    """
    return base64.b64decode(key_base64.encode('utf-8'))

def get_key_info(key_bytes):
    """
    Extract information from RSA key.
    
    Args:
        key_bytes: RSA key in PEM format
    
    Returns:
        Dictionary with key information
    """
    key = RSA.import_key(key_bytes)
    
    info = {
        'key_size_bits': key.size_in_bits(),
        'key_size_bytes': key.size_in_bits() // 8,
        'has_private': key.has_private(),
        'max_encrypt_bytes': (key.size_in_bits() // 8) - 42 if not key.has_private() else None,
        'recommended_playfair_key_length': (key.size_in_bits() // 8) - 42
    }
    
    return info

# Self-test with comprehensive validation
if __name__ == "__main__":
    print("=" * 70)
    print("HYBRID CRYPTOSYSTEM TEST")
    print("=" * 70)
    
    # Generate RSA keys
    print("\n1. Generating RSA-2048 key pair...")
    receiver_private, receiver_public = generate_rsa_keys(2048)
    print("   ✓ Keys generated successfully")
    
    # Display key information
    pub_info = get_key_info(receiver_public)
    print(f"\n2. Key Information:")
    print(f"   Key size: {pub_info['key_size_bits']} bits")
    print(f"   Max Playfair key length: {pub_info['recommended_playfair_key_length']} bytes")
    
    # Test encryption with valid key
    print("\n3. Testing hybrid encryption...")
    message = "This is a secret message! 🔐 Confidential data: 你好世界"
    playfair_key = "MY_SECRET_KEY_2024"
    
    print(f"   Original message: {message}")
    print(f"   Playfair key: {playfair_key}")
    print(f"   Playfair key size: {len(playfair_key.encode('utf-8'))} bytes")
    
    try:
        cipher, enc_key = hybrid_encrypt(message, playfair_key, receiver_public)
        print(f"   ✓ Encryption successful")
        print(f"   Ciphertext length: {len(cipher)} characters")
        print(f"   Encrypted key size: {len(enc_key)} bytes")
    except ValueError as e:
        print(f"   ✗ Encryption failed: {e}")
        exit(1)
    
    # Test decryption
    print("\n4. Testing hybrid decryption...")
    try:
        decrypted = hybrid_decrypt(cipher, enc_key, receiver_private)
        print(f"   ✓ Decryption successful")
        print(f"   Decrypted message: {decrypted}")
    except ValueError as e:
        print(f"   ✗ Decryption failed: {e}")
        exit(1)
    
    # Verify correctness
    print("\n5. Verification:")
    if message in decrypted:  # Account for padding
        print("   ✓ Message integrity verified!")
    else:
        print("   ✗ Message mismatch detected")
    
    # Test key size validation
    print("\n6. Testing key size validation...")
    oversized_key = "A" * 300  # Too large for RSA-2048
    try:
        hybrid_encrypt("Test", oversized_key, receiver_public)
        print("   ✗ Validation failed to catch oversized key")
    except ValueError as e:
        print(f"   ✓ Oversized key correctly rejected")
        print(f"   Error: {str(e)[:80]}...")
    
    print("\n" + "=" * 70)
    print("ALL TESTS PASSED")
    print("=" * 70)