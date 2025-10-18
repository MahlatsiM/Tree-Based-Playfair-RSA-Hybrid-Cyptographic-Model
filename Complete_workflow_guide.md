# 🔄 Complete Workflow Guide

## Step-by-Step Instructions for Sending and Receiving Encrypted Messages

---

## 📋 Overview: Three Dashboards

Your system now has **3 dashboards**:

1. **key_generation_dashboard.py** - Receiver generates RSA keys
2. **encryption_dashboard.py** - Sender encrypts messages
3. **decryption_dashboard.py** - Receiver decrypts messages

---

## 👥 Scenario: Alice wants to send Bob an encrypted message

### **Bob (Receiver) - Step 1: Generate Keys**

**Dashboard:** `key_generation_dashboard.py`

```bash
streamlit run key_generation_dashboard.py
```

**Actions:**
1. Open the Key Generation Dashboard
2. Select RSA key size (2048 recommended)
3. Click **"Generate RSA Key Pair"**
4. Download **BOTH keys**:
   - `my_public_key.pem` ✅ Share this
   - `my_private_key.pem` 🔐 Keep secret!

**Result:** Bob now has two files:
- ✅ Public key (to share)
- 🔐 Private key (keep secure)

---

### **Bob (Receiver) - Step 2: Share Public Key**

**Bob sends his PUBLIC key to Alice** via:
- 📧 Email attachment
- ☁️ Cloud storage (Dropbox, Google Drive)
- 💬 Messaging app
- 💾 USB drive
- 🌐 Any method (it's safe to share!)

**Important:** Bob keeps his PRIVATE key secret!

---

### **Alice (Sender) - Step 3: Encrypt Message**

**Dashboard:** `encryption_dashboard.py`

```bash
streamlit run encryption_dashboard.py
```

**Actions:**
1. **Upload Bob's public key** (received from Bob)
   - Sidebar → Upload PUBLIC Key File
   - Select `my_public_key.pem` that Bob sent
   
2. **Generate/Enter Playfair Key**
   - Sidebar → Click "Generate Random Playfair Key"
   - OR enter manually
   
3. **Enter Message**
   - Type message OR upload text file
   
4. **Encrypt**
   - Click "🔒 ENCRYPT MESSAGE"
   
5. **Download encrypted files:**
   - `encrypted_message.txt`
   - `encrypted_playfair_key.bin`

**Result:** Alice has two encrypted files to send to Bob

---

### **Alice (Sender) - Step 4: Send Encrypted Files**

**Alice sends to Bob:**
- 📄 `encrypted_message.txt`
- 🔑 `encrypted_playfair_key.bin`

**Methods:**
- Email attachments
- Cloud storage
- File transfer services
- USB drive

**Security:** These files are encrypted - safe to send through any channel!

---

### **Bob (Receiver) - Step 5: Decrypt Message**

**Dashboard:** `decryption_dashboard.py`

```bash
streamlit run decryption_dashboard.py
```

**Actions:**
1. **Upload YOUR private key**
   - Sidebar → Upload Your PRIVATE Key
   - Select `my_private_key.pem` (the one YOU generated)
   
2. **Upload encrypted message**
   - Sidebar → Upload Encrypted Message
   - Select `encrypted_message.txt` (from Alice)
   
3. **Upload encrypted key**
   - Sidebar → Upload Encrypted Key
   - Select `encrypted_playfair_key.bin` (from Alice)
   
4. **Decrypt**
   - Click "🔓 DECRYPT MESSAGE"
   
5. **Read message**
   - View decrypted message on screen
   - OR download as text file

**Result:** Bob can now read Alice's original message!

---

## 🎯 Quick Reference Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    STEP 1: KEY GENERATION                    │
│                    (Bob - Receiver)                          │
├─────────────────────────────────────────────────────────────┤
│  Run: key_generation_dashboard.py                           │
│                                                              │
│  1. Generate RSA Keys                                        │
│     ├── my_public_key.pem    [Share with Alice]            │
│     └── my_private_key.pem   [Keep SECRET]                  │
│                                                              │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   │ Bob sends public key to Alice
                   ↓
┌─────────────────────────────────────────────────────────────┐
│                    STEP 2: ENCRYPTION                        │
│                    (Alice - Sender)                          │
├─────────────────────────────────────────────────────────────┤
│  Run: encryption_dashboard.py                               │
│                                                              │
│  1. Upload Bob's public key (received from Bob)             │
│  2. Generate/Enter Playfair key                             │
│  3. Type/Upload message                                      │
│  4. Click "Encrypt"                                          │
│  5. Download:                                                │
│     ├── encrypted_message.txt                               │
│     └── encrypted_playfair_key.bin                          │
│                                                              │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   │ Alice sends encrypted files to Bob
                   ↓
┌─────────────────────────────────────────────────────────────┐
│                    STEP 3: DECRYPTION                        │
│                    (Bob - Receiver)                          │
├─────────────────────────────────────────────────────────────┤
│  Run: decryption_dashboard.py                               │
│                                                              │
│  1. Upload YOUR private key (my_private_key.pem)            │
│  2. Upload encrypted_message.txt (from Alice)               │
│  3. Upload encrypted_playfair_key.bin (from Alice)          │
│  4. Click "Decrypt"                                          │
│  5. Read original message                                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔑 Key Files Reference

### **Files Bob (Receiver) Has:**
| File | Generated By | Purpose | Share? |
|------|-------------|---------|--------|
| `my_public_key.pem` | Bob | For others to encrypt | ✅ YES |
| `my_private_key.pem` | Bob | To decrypt messages | ❌ NEVER |
| `encrypted_message.txt` | Alice | Received encrypted message | N/A |
| `encrypted_playfair_key.bin` | Alice | Received encrypted key | N/A |

### **Files Alice (Sender) Has:**
| File | Source | Purpose | Share? |
|------|--------|---------|--------|
| `my_public_key.pem` | From Bob | Encrypt messages for Bob | N/A |
| `encrypted_message.txt` | Generated | Send to Bob | ✅ YES |
| `encrypted_playfair_key.bin` | Generated | Send to Bob | ✅ YES |

---

## ❓ Frequently Asked Questions

### **Q: I'm testing alone. How do I simulate both sender and receiver?**

**A: Use Testing Mode**

1. Run `key_generation_dashboard.py`
   - Generate keys
   - Download BOTH keys
   
2. Run `encryption_dashboard.py`
   - Use "Testing Mode" to generate keys
   - OR upload the public key you just generated
   - Encrypt a message
   - Download encrypted files AND the private key
   
3. Run `decryption_dashboard.py`
   - Upload the private key
   - Upload encrypted files
   - Decrypt

---

### **Q: What if I lose my private key?**

**A:** You cannot decrypt any messages encrypted with your public key. You must:
1. Generate a NEW key pair
2. Distribute the NEW public key to everyone
3. Old encrypted messages are unrecoverable

---

### **Q: Can multiple people use my public key?**

**A:** Yes! Share your public key with everyone who wants to send you encrypted messages. Each person uses the same public key.

---

### **Q: Do I need to generate new keys for each message?**

**A:** No! 
- **RSA keys** (public/private) → Generate once, use for many messages
- **Playfair keys** → New key for each message (recommended for security)

---

### **Q: Someone sent me encrypted files but I don't have the private key**

**A:** You cannot decrypt. You need:
- Your own private key (that matches the public key used to encrypt)
- If they used someone else's public key, you cannot decrypt

---

### **Q: How do I know which public key to use?**

**A:** Always use the PUBLIC key of the person who will RECEIVE and DECRYPT the message.

Example:
- Alice encrypts for Bob → Use Bob's public key
- Bob encrypts for Alice → Use Alice's public key

---

## 🔒 Security Checklist

### **For Receivers (Key Holders):**
- ✅ Generate keys using Key Generation Dashboard
- ✅ Download and backup both keys
- ✅ Store private key in encrypted folder/password manager
- ✅ Share public key freely with senders
- ❌ NEVER share private key with anyone
- ✅ Generate new keys if private key is compromised

### **For Senders:**
- ✅ Get recipient's PUBLIC key directly from them
- ✅ Verify the public key is from the correct person
- ✅ Use a unique Playfair key for each message
- ✅ Send encrypted files through any channel
- ✅ Delete Playfair key after encryption (optional security)

---

## 🚀 Running All Dashboards

### **Option 1: Separate Terminals**

```bash
# Terminal 1 - Key Generation
streamlit run key_generation_dashboard.py --server.port 8501

# Terminal 2 - Encryption
streamlit run encryption_dashboard.py --server.port 8502

# Terminal 3 - Decryption
streamlit run decryption_dashboard.py --server.port 8503
```

Access:
- Key Generation: http://localhost:8501
- Encryption: http://localhost:8502
- Decryption: http://localhost:8503

### **Option 2: Run One at a Time**

```bash
# Step 1: Generate keys
streamlit run key_generation_dashboard.py

# Step 2: Encrypt (after getting public key)
streamlit run encryption_dashboard.py

# Step 3: Decrypt (after receiving encrypted files)
streamlit run decryption_dashboard.py
```

---

## 📊 Complete File Flow Diagram

```
RECEIVER (Bob)                SENDER (Alice)
══════════════                ══════════════

1. key_generation_dashboard.py
   │
   ├─→ my_public_key.pem ────────────→ 2. Receives public key
   │                                      │
   └─→ my_private_key.pem (keep)         │
                                          ↓
                                   3. encryption_dashboard.py
                                          │
                                          ├─→ encrypted_message.txt ─┐
                                          │                           │
                                          └─→ encrypted_playfair_key.bin ─┐
                                                                      │
4. Receives encrypted files ←─────────────────────────────────────────┘
   │
   ↓
5. decryption_dashboard.py
   │
   ├─→ Loads: my_private_key.pem (from step 1)
   ├─→ Loads: encrypted_message.txt (from Alice)
   ├─→ Loads: encrypted_playfair_key.bin (from Alice)
   │
   └─→ Result: Original message!
```

---

## ✅ Testing Checklist

### **Test 1: Full Workflow**
- [ ] Run key generation dashboard
- [ ] Generate RSA keys
- [ ] Download both keys
- [ ] Run encryption dashboard
- [ ] Upload public key
- [ ] Generate Playfair key
- [ ] Type test message
- [ ] Encrypt successfully
- [ ] Download encrypted files
- [ ] Run decryption dashboard
- [ ] Upload private key
- [ ] Upload encrypted files
- [ ] Decrypt successfully
- [ ] Verify original message matches

### **Test 2: Error Handling**
- [ ] Try decrypting with wrong private key (should fail)
- [ ] Try uploading corrupted files (should error gracefully)
- [ ] Try encrypting without public key (should warn)
- [ ] Try decrypting without all files (should warn)

---

## 🎓 Educational Use

This workflow demonstrates:
1. **Public Key Infrastructure (PKI)** - How public/private keys work
2. **Hybrid Cryptography** - Combining symmetric and asymmetric encryption
3. **Key Exchange** - How to securely share encryption keys
4. **End-to-End Encryption** - Messages encrypted by sender, decrypted by receiver

---

**Summary:** Three dashboards, clear workflow, secure messaging! 🔐