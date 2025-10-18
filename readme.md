# Hybrid Cryptosystem Platform

A unified web-based encryption platform combining Tree-Based Playfair cipher (545×545 matrix) with RSA public-key cryptography for secure end-to-end messaging.

## What This Does

This is a complete cryptographic messaging system in a single interface. You generate keys, encrypt messages, and decrypt them without touching the command line or managing multiple tools.

The system uses hybrid encryption: your message gets encrypted with a custom Playfair cipher (supporting 297,025 Unicode characters), then the cipher key gets encrypted with RSA. Only the intended recipient's private key can unlock it.

## Installation

```bash
pip install streamlit cryptography
```

## Running the Platform

```bash
streamlit run combined.py
```

The app opens at `http://localhost:8501`

## How It Works

### For Receivers (People Getting Messages)

**Step 1: Generate Your Keys**

1. Open the sidebar, select **"📥 Receiver (Generate Keys)"**
2. Pick your RSA key size (2048-bit is fine for most uses)
3. Click **"Generate RSA Key Pair"**
4. Download both files:
   - `my_public_key.pem` - Share this with anyone who wants to message you
   - `my_private_key.pem` - **Never share this. Ever.**

Store your private key somewhere safe. Password manager, encrypted folder, whatever. If you lose it, you can't decrypt any messages encrypted for you.

**Step 2: Share Your Public Key**

Email it, upload it, post it publicly. It's designed to be shared. Anyone who has it can send you encrypted messages that only you can read.

**Step 3: Decrypt Messages**

When someone sends you encrypted files:

1. Select **"🔓 Receiver (Decrypt)"** in the sidebar
2. Upload your private key
3. Upload the two files they sent you:
   - `encrypted_message.txt`
   - `encrypted_playfair_key.bin`
4. Click **"Decrypt Message"**

Your original message appears. Save it or copy it.

### For Senders (People Sending Messages)

**Step 1: Get Recipient's Public Key**

Ask them for their `public_key.pem` file. They should have generated it using the platform.

**Step 2: Encrypt Your Message**

1. Select **"📤 Sender (Encrypt)"** in the sidebar
2. Upload their public key file
3. Type your message or upload a text file
4. Click **"Generate Random Key"** (or enter your own Playfair key)
5. Click **"Encrypt Message"**
6. Download both encrypted files:
   - `encrypted_message.txt`
   - `encrypted_playfair_key.bin`

**Step 3: Send Both Files**

Email them, upload them somewhere, whatever. Both files are encrypted. Without the recipient's private key, they're useless to anyone else.

## Testing Alone

Want to test the system without a second person?

1. Generate keys in **Receiver (Generate Keys)**
2. Download both keys
3. Switch to **Sender (Encrypt)**
4. Click **"Generate Test RSA Keys"** (or upload the public key you just made)
5. Encrypt a test message
6. Download everything including the test private key
7. Switch to **Receiver (Decrypt)**
8. Upload the private key and encrypted files
9. Decrypt

## File Reference

| File | What It Is | Share It? |
|------|------------|-----------|
| `my_public_key.pem` | Your public RSA key | ✅ Yes, share freely |
| `my_private_key.pem` | Your private RSA key | ❌ Never share this |
| `encrypted_message.txt` | Encrypted message ciphertext | ✅ Yes, send to recipient |
| `encrypted_playfair_key.bin` | RSA-encrypted cipher key | ✅ Yes, send to recipient |

## Security Features

- **297,025 character Unicode support** - Not limited to English alphabet
- **Tree-based matrix generation** - BFS/DFS algorithms for Playfair key expansion
- **RSA-2048/3072/4096** - Configurable key strength
- **Client-side only** - Nothing leaves your browser, no server storage
- **Random padding** - Makes frequency analysis harder

## Common Mistakes

**"I can't decrypt the message"**

Check:
- Are you using the correct private key? It must match the public key used for encryption
- Did you upload both encrypted files (message + key)?
- Are the files corrupted? Try downloading them again

**"I lost my private key"**

You're done. Generate new keys and redistribute your new public key. Old messages encrypted with your old public key are permanently unreadable.

**"Someone needs my private key to send me messages"**

No. They need your PUBLIC key. You keep the private key to yourself. That's the entire point of public-key cryptography.

**"Do I need new keys for every message?"**

No. Your RSA keys (public/private pair) are long-term. Generate once, use many times. The Playfair key should be unique per message for better security, but the platform auto-generates that.

## Technical Details

**Encryption Process:**
1. Message encrypted with Playfair cipher using 545×545 matrix
2. Playfair key encrypted with recipient's RSA public key
3. Two encrypted outputs sent to recipient

**Decryption Process:**
1. RSA private key decrypts the Playfair key
2. Decrypted Playfair key decrypts the message
3. Original message recovered

**Why Hybrid?**

RSA can't efficiently encrypt large messages. Playfair can't securely share keys. Combining them gives you both speed and security.

## Troubleshooting

**"The app won't start"**

Make sure you have the required files in the same directory:
- `combined.py`
- `hybrid_crypto.py`
- `custom_unicode.py`

**"KeyError or import errors"**

Install dependencies:
```bash
pip install streamlit cryptography
```

**"Encryption fails with 'key too long'"**

Your Playfair key is too long for your RSA key size. Either shorten the Playfair key or generate larger RSA keys.

## Limitations

This is an educational/demonstration platform. For production use:
- Add key authentication/verification
- Implement key signing
- Add message authentication codes (MAC)
- Use established protocols (PGP, Signal Protocol, etc.)

Don't use this for life-or-death secrets. It's solid for learning cryptography concepts and secure casual messaging, but it hasn't been audited by security experts.

## License

Do whatever you want with it.

---

**Bottom line:** One interface. Three workflows. End-to-end encryption.
