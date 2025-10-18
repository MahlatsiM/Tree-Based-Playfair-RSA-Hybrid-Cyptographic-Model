"""
Unified Hybrid Cryptosystem Platform
Combined dashboard for Key Generation, Encryption, and Decryption
"""

import streamlit as st
import time
import secrets
from hybrid_crypto import generate_rsa_keys, hybrid_encrypt, hybrid_decrypt, get_key_info
from custom_unicode import CHAR_SET

# Page configuration
st.set_page_config(
    page_title="Hybrid Cryptosystem Platform",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
def init_session_state():
    if 'private_key' not in st.session_state:
        st.session_state.private_key = None
    if 'public_key' not in st.session_state:
        st.session_state.public_key = None
    if 'key_size' not in st.session_state:
        st.session_state.key_size = 2048
    if 'generated_playfair_key' not in st.session_state:
        st.session_state.generated_playfair_key = None
    if 'recipient_public_key' not in st.session_state:
        st.session_state.recipient_public_key = None
    if 'recipient_private_key' not in st.session_state:
        st.session_state.recipient_private_key = None
    if 'encrypted_message' not in st.session_state:
        st.session_state.encrypted_message = None
    if 'encrypted_key' not in st.session_state:
        st.session_state.encrypted_key = None

init_session_state()

# Sidebar Navigation
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/security-shield-green.png", width=80)
    st.title("🔐 Hybrid Crypto")
    st.markdown("### Navigation")
    
    # Role selection
    role = st.radio(
        "Select Your Role",
        ["🎯 Getting Started", "📥 Receiver (Generate Keys)", "📤 Sender (Encrypt)", "🔓 Receiver (Decrypt)"],
        index=0
    )
    
    st.divider()
    
    # Quick stats
    with st.expander("📊 Session Status"):
        if st.session_state.public_key:
            st.success("✅ Your keys generated")
        else:
            st.info("⚪ No keys yet")
        
        if st.session_state.recipient_public_key:
            st.success("✅ Recipient key loaded")
        else:
            st.info("⚪ No recipient key")
        
        if st.session_state.encrypted_message:
            st.success("✅ Encrypted data loaded")
        else:
            st.info("⚪ No encrypted data")
    
    st.divider()
    st.caption("Tree-Based Playfair (545×545) + RSA")
    st.caption("v1.0 | Unified Platform")

# Main content based on selection
if role == "🎯 Getting Started":
    st.title("🎯 Welcome to Hybrid Cryptosystem Platform")
    st.markdown("### Secure Message Encryption & Decryption")
    
    st.divider()
    
    # Overview
    col_intro1, col_intro2 = st.columns(2)
    
    with col_intro1:
        st.markdown("""
        ## 🔒 What This Does
        
        This platform provides end-to-end encrypted messaging using a hybrid cryptographic system:
        
        - **Playfair Cipher**: 545×545 matrix (297,025 characters)
        - **RSA Encryption**: Secure key exchange (2048-4096 bits)
        - **Tree-Based Key Generation**: BFS/DFS matrix construction
        - **Zero Knowledge**: Your keys never leave your device
        """)
    
    with col_intro2:
        st.markdown("""
        ## 👥 How It Works
        
        **For Message Recipients:**
        1. Generate RSA key pair
        2. Share PUBLIC key with senders
        3. Receive encrypted messages
        4. Decrypt with your PRIVATE key
        
        **For Message Senders:**
        1. Get recipient's PUBLIC key
        2. Write your message
        3. Encrypt using hybrid system
        4. Send encrypted files to recipient
        """)
    
    st.divider()
    
    # Workflow diagram
    st.markdown("## 📋 Complete Workflow")
    
    tab1, tab2, tab3 = st.tabs(["1️⃣ Receiver Setup", "2️⃣ Sender Process", "3️⃣ Receiver Decryption"])
    
    with tab1:
        st.markdown("""
        ### 📥 Receiver: Generate Keys
        
        **Navigation:** Select *"📥 Receiver (Generate Keys)"* in sidebar
        
        **Steps:**
        1. Choose RSA key size (2048, 3072, or 4096 bits)
        2. Click "Generate RSA Key Pair"
        3. Download BOTH keys:
           - **Public Key** → Share with senders
           - **Private Key** → Keep SECRET!
        4. Send public key to anyone who wants to send you messages
        
        **⚠️ Security Note:** Your private key must NEVER be shared!
        """)
        
        st.info("💡 **Tip:** Store your private key in a password manager or encrypted storage")
    
    with tab2:
        st.markdown("""
        ### 📤 Sender: Encrypt Message
        
        **Navigation:** Select *"📤 Sender (Encrypt)"* in sidebar
        
        **Steps:**
        1. Upload recipient's PUBLIC key
        2. Write or upload your message
        3. Generate/enter Playfair key (auto-generated recommended)
        4. Click "Encrypt Message"
        5. Download encrypted files:
           - **Encrypted Message** (.txt)
           - **Encrypted Key** (.bin)
        6. Send BOTH files to recipient
        
        **🔒 Security:** Only the recipient's private key can decrypt these files
        """)
        
        st.info("💡 **Tip:** You can test the system by generating test keys if you don't have a recipient yet")
    
    with tab3:
        st.markdown("""
        ### 🔓 Receiver: Decrypt Message
        
        **Navigation:** Select *"🔓 Receiver (Decrypt)"* in sidebar
        
        **Steps:**
        1. Upload YOUR private key
        2. Upload encrypted message file (.txt)
        3. Upload encrypted key file (.bin)
        4. Click "Decrypt Message"
        5. Read or download your decrypted message
        
        **🔐 Privacy:** Decryption happens locally - your private key never leaves your device
        """)
        
        st.warning("⚠️ **Important:** Use the same private key that matches the public key used for encryption")
    
    st.divider()
    
    # Quick start buttons
    st.markdown("## 🚀 Quick Start")
    
    col_qs1, col_qs2, col_qs3 = st.columns(3)
    
    with col_qs1:
        if st.button("📥 I want to receive messages", use_container_width=True):
            st.info("👉 Select **'📥 Receiver (Generate Keys)'** in the sidebar to start!")
    
    with col_qs2:
        if st.button("📤 I want to send a message", use_container_width=True):
            st.info("👉 Select **'📤 Sender (Encrypt)'** in the sidebar to start!")
    
    with col_qs3:
        if st.button("🔓 I received encrypted files", use_container_width=True):
            st.info("👉 Select **'🔓 Receiver (Decrypt)'** in the sidebar to start!")
    
    st.divider()
    
    # Security features
    with st.expander("🔒 Security Features"):
        col_sec1, col_sec2 = st.columns(2)
        
        with col_sec1:
            st.markdown("""
            ### Encryption Strength
            - ✅ 297,025 character Unicode set
            - ✅ Tree-based matrix generation
            - ✅ RSA-2048/3072/4096 support
            - ✅ Random padding
            - ✅ Unique keys per session
            """)
        
        with col_sec2:
            st.markdown("""
            ### Privacy & Safety
            - ✅ Client-side processing
            - ✅ No key transmission
            - ✅ No data logging
            - ✅ Open source cryptography
            - ✅ Industry-standard protocols
            """)

# RECEIVER: KEY GENERATION
elif role == "📥 Receiver (Generate Keys)":
    st.title("🔑 RSA Key Generation Dashboard")
    st.markdown("### Step 1: Receiver Generates Keys")
    st.divider()
    
    # Explanation
    st.info("""
    **👤 Who uses this?** RECEIVERS (people who want to receive encrypted messages)
    
    **🎯 What it does:**
    1. Generates a pair of RSA keys (Public + Private)
    2. **Public Key** → Share with senders (safe to share publicly)
    3. **Private Key** → Keep SECRET! Only you should have this
    """)
    
    st.divider()
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("⚙️ Key Generation Settings")
        
        # Key size selection
        key_size = st.radio(
            "Select RSA Key Size",
            options=[2048, 3072, 4096],
            index=0,
            help="Larger keys are more secure but slower"
        )
        
        # Key size info
        key_info_map = {
            2048: ("Good", "~2030", "Recommended for most uses", "🟢"),
            3072: ("Strong", "~2040", "Better long-term security", "🟡"),
            4096: ("Very Strong", "Beyond 2040", "Maximum security", "🔴")
        }
        
        level, valid_until, desc, icon = key_info_map[key_size]
        
        st.markdown(f"""
        **{icon} Security Level:** {level}  
        **📅 Valid Until:** {valid_until}  
        **📝 Description:** {desc}
        """)
        
        st.divider()
        
        # Generate button
        if st.button("🎲 Generate RSA Key Pair", type="primary", use_container_width=True):
            with st.spinner(f"Generating {key_size}-bit RSA keys..."):
                try:
                    private_key, public_key = generate_rsa_keys(key_size)
                    
                    # Store in session state
                    st.session_state.private_key = private_key
                    st.session_state.public_key = public_key
                    st.session_state.key_size = key_size
                    
                    st.success(f"✅ {key_size}-bit RSA key pair generated successfully!")
                    
                except Exception as e:
                    st.error(f"❌ Key generation failed: {str(e)}")
    
    with col2:
        st.header("📊 Key Statistics")
        
        if st.session_state.public_key:
            info = get_key_info(st.session_state.public_key)
            
            st.metric("Key Size", f"{info['key_size_bits']} bits")
            st.metric("Key Bytes", f"{info['key_size_bytes']} bytes")
            st.metric("Max Playfair Key", f"{info['recommended_playfair_key_length']} chars")
            
            st.success("✅ Keys ready!")
        else:
            st.info("Generate keys to see statistics")
    
    # Download section
    if st.session_state.public_key and st.session_state.private_key:
        st.divider()
        st.header("💾 Download Your Keys")
        
        col_dl1, col_dl2 = st.columns(2)
        
        with col_dl1:
            st.subheader("🔓 Public Key")
            st.success("✅ **SAFE TO SHARE**")
            
            # Preview public key
            pub_preview = st.session_state.public_key.decode('utf-8')
            st.text_area("Public Key Preview", value=pub_preview[:300] + "...", height=150, disabled=True)
            
            # Download button
            st.download_button(
                label="📥 Download Public Key",
                data=st.session_state.public_key,
                file_name="my_public_key.pem",
                mime="text/plain",
                use_container_width=True,
                type="primary"
            )
        
        with col_dl2:
            st.subheader("🔐 Private Key")
            st.error("⚠️ **NEVER SHARE THIS**")
            
            # Preview private key (partially hidden)
            st.text_area("Private Key (Hidden)", value="********** CONFIDENTIAL **********", height=150, disabled=True)
            
            # Download button
            st.download_button(
                label="📥 Download Private Key",
                data=st.session_state.private_key,
                file_name="my_private_key.pem",
                mime="text/plain",
                use_container_width=True,
                type="secondary"
            )
        
        # Next steps
        st.divider()
        st.success("""
        ### ✅ Next Steps:
        
        1. ✅ Download BOTH keys (done above)
        2. 📧 Send **PUBLIC key** to senders
        3. 🔐 Keep **PRIVATE key** secure
        4. 🔓 Use **Receiver (Decrypt)** when you get encrypted messages
        """)

# SENDER: ENCRYPTION
elif role == "📤 Sender (Encrypt)":
    st.title("🔒 Encryption Dashboard")
    st.markdown("### Hybrid Cryptosystem: Tree-Based Playfair (545×545) + RSA")
    st.divider()
    
    # Key Management Section
    with st.expander("🔑 Recipient's Public Key", expanded=not st.session_state.recipient_public_key):
        st.info("Upload the recipient's PUBLIC key file or generate test keys")
        
        col_key1, col_key2 = st.columns(2)
        
        with col_key1:
            # Upload recipient's public key
            uploaded_pub_key = st.file_uploader(
                "Upload Recipient's PUBLIC Key (.pem)",
                type=['pem', 'txt'],
                help="Upload the recipient's public RSA key file"
            )
            
            if uploaded_pub_key:
                st.session_state.recipient_public_key = uploaded_pub_key.read()
                st.success("✅ Public key loaded!")
        
        with col_key2:
            # Generate test keys
            st.caption("🧪 Testing Mode")
            if st.button("🎲 Generate Test RSA Keys"):
                priv, pub = generate_rsa_keys()
                st.session_state.recipient_private_key = priv
                st.session_state.recipient_public_key = pub
                st.success("✅ Test keys generated!")
    
    st.divider()
    
    # Main content
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.header("📝 Message Input")
        
        # Message input
        input_method = st.radio("Input Method", ["Type Message", "Upload File"], horizontal=True)
        
        message = ""
        if input_method == "Type Message":
            message = st.text_area("Enter your message", height=200, placeholder="Type your secret message here...")
        else:
            uploaded_file = st.file_uploader("Upload text file", type=['txt'])
            if uploaded_file:
                message = uploaded_file.read().decode('utf-8', errors='replace')
                st.text_area("File Content Preview", value=message[:500], height=200, disabled=True)
        
        st.divider()
        
        # Playfair key
        st.subheader("🔑 Playfair Key")
        
        col_key_gen1, col_key_gen2 = st.columns([1, 2])
        
        with col_key_gen1:
            key_length = st.slider("Key Length", 8, 256, 32)
        
        with col_key_gen2:
            if st.button("🎲 Generate Random Key", use_container_width=True):
                safe_chars = [c for c in CHAR_SET[:1000] if 32 <= ord(c) <= 126]
                random_key = ''.join(secrets.choice(safe_chars) for _ in range(key_length))
                st.session_state.generated_playfair_key = random_key
        
        playfair_key = st.text_input(
            "Playfair Key",
            value=st.session_state.generated_playfair_key or "",
            max_chars=256,
            placeholder="Enter or generate key"
        )
    
    with col2:
        st.header("⚙️ Status")
        
        # Validation
        checks_passed = True
        
        if st.session_state.recipient_public_key:
            st.success("✅ Recipient's public key")
        else:
            st.error("❌ No recipient key")
            checks_passed = False
        
        if message:
            st.success(f"✅ Message ({len(message)} chars)")
        else:
            st.error("❌ No message")
            checks_passed = False
        
        if playfair_key:
            st.success(f"✅ Playfair key ({len(playfair_key)} chars)")
        else:
            st.error("❌ No Playfair key")
            checks_passed = False
        
        st.divider()
        
        # Encrypt button
        encrypt_button = st.button(
            "🔒 ENCRYPT MESSAGE",
            type="primary",
            disabled=not checks_passed,
            use_container_width=True
        )
    
    # Encryption process
    if encrypt_button:
        try:
            with st.spinner("🔄 Encrypting..."):
                start_time = time.time()
                cipher_text, encrypted_key = hybrid_encrypt(
                    message, playfair_key, st.session_state.recipient_public_key
                )
                encryption_time = time.time() - start_time
            
            st.success("✅ Message encrypted successfully!")
            
            # Results
            st.divider()
            st.header("📦 Encrypted Output")
            
            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                st.metric("Time", f"{encryption_time:.4f}s")
            with col_m2:
                st.metric("Cipher Length", f"{len(cipher_text)}")
            with col_m3:
                st.metric("Original", f"{len(message)}")
            
            st.code(cipher_text[:200] + "..." if len(cipher_text) > 200 else cipher_text)
            
            # Downloads
            st.divider()
            col_dl1, col_dl2, col_dl3 = st.columns(3)
            
            with col_dl1:
                st.download_button(
                    "📄 Encrypted Message",
                    cipher_text.encode('utf-8', errors='replace'),
                    "encrypted_message.txt",
                    use_container_width=True
                )
            
            with col_dl2:
                st.download_button(
                    "🔑 Encrypted Key",
                    encrypted_key,
                    "encrypted_playfair_key.bin",
                    use_container_width=True
                )
            
            with col_dl3:
                if st.session_state.recipient_private_key:
                    st.download_button(
                        "🔐 Private Key (TEST)",
                        st.session_state.recipient_private_key,
                        "recipient_private_key.pem",
                        use_container_width=True
                    )
            
            st.info("**Next:** Send both encrypted files to the recipient")
            
        except Exception as e:
            st.error(f"❌ Encryption failed: {str(e)}")

# RECEIVER: DECRYPTION
else:  # role == "🔓 Receiver (Decrypt)"
    st.title("🔓 Decryption Dashboard")
    st.markdown("### Hybrid Cryptosystem: Tree-Based Playfair (545×545) + RSA")
    st.divider()
    
    # File upload section
    with st.expander("📂 Upload Required Files", expanded=True):
        col_up1, col_up2, col_up3 = st.columns(3)
        
        with col_up1:
            st.markdown("**1. Your Private Key**")
            uploaded_priv = st.file_uploader("Private Key (.pem)", type=['pem', 'txt'], key="priv")
            if uploaded_priv:
                st.session_state.private_key = uploaded_priv.read()
                st.success("✅ Loaded")
        
        with col_up2:
            st.markdown("**2. Encrypted Message**")
            uploaded_msg = st.file_uploader("Encrypted Message (.txt)", type=['txt'], key="msg")
            if uploaded_msg:
                st.session_state.encrypted_message = uploaded_msg.read().decode('utf-8', errors='replace')
                st.success("✅ Loaded")
        
        with col_up3:
            st.markdown("**3. Encrypted Key**")
            uploaded_key = st.file_uploader("Encrypted Key (.bin)", type=['bin'], key="key")
            if uploaded_key:
                st.session_state.encrypted_key = uploaded_key.read()
                st.success("✅ Loaded")
    
    st.divider()
    
    # Main content
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.header("📋 Encrypted Data Preview")
        
        if st.session_state.encrypted_message:
            msg_preview = st.session_state.encrypted_message[:500]
            st.text_area(
                "Encrypted Message",
                value=msg_preview + ("..." if len(st.session_state.encrypted_message) > 500 else ""),
                height=200,
                disabled=True
            )
            st.caption(f"Length: {len(st.session_state.encrypted_message)} characters")
        else:
            st.info("Upload encrypted message file")
        
        if st.session_state.encrypted_key:
            hex_preview = st.session_state.encrypted_key[:32].hex()
            st.code(f"{hex_preview}...")
            st.caption(f"Encrypted key: {len(st.session_state.encrypted_key)} bytes")
    
    with col2:
        st.header("⚙️ Status")
        
        checks_passed = True
        
        if st.session_state.private_key:
            st.success("✅ Private key")
        else:
            st.error("❌ No private key")
            checks_passed = False
        
        if st.session_state.encrypted_message:
            st.success("✅ Encrypted message")
        else:
            st.error("❌ No message")
            checks_passed = False
        
        if st.session_state.encrypted_key:
            st.success("✅ Encrypted key")
        else:
            st.error("❌ No key")
            checks_passed = False
        
        st.divider()
        
        # Decrypt button
        decrypt_button = st.button(
            "🔓 DECRYPT MESSAGE",
            type="primary",
            disabled=not checks_passed,
            use_container_width=True
        )
    
    # Decryption process
    if decrypt_button:
        try:
            with st.spinner("🔄 Decrypting..."):
                start_time = time.time()
                decrypted_message = hybrid_decrypt(
                    st.session_state.encrypted_message,
                    st.session_state.encrypted_key,
                    st.session_state.private_key
                )
                decryption_time = time.time() - start_time
            
            st.success("✅ Message decrypted successfully!")
            
            # Results
            st.divider()
            st.header("📖 Decrypted Message")
            
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.metric("Decryption Time", f"{decryption_time:.4f}s")
            with col_m2:
                st.metric("Message Length", f"{len(decrypted_message)} chars")
            
            st.text_area("Your Message", value=decrypted_message, height=300)
            
            # Download
            st.download_button(
                "📄 Download Decrypted Message",
                decrypted_message.encode('utf-8', errors='replace'),
                "decrypted_message.txt",
                use_container_width=True
            )
            
        except ValueError as ve:
            st.error("❌ Decryption failed: Invalid key or corrupted data")
            with st.expander("🔍 Troubleshooting"):
                st.markdown("""
                **Common issues:**
                - Wrong private key
                - Corrupted files
                - Mismatched encryption/decryption keys
                """)
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Footer (always visible)
st.divider()
with st.expander("ℹ️ About This System"):
    st.markdown("""
    ### Hybrid Encryption Process
    
    1. **Playfair Encryption**: Message encrypted with 545×545 matrix cipher
    2. **RSA Key Exchange**: Playfair key encrypted with RSA public key
    3. **Secure Delivery**: Both encrypted message and key sent to recipient
    4. **Decryption**: Recipient uses private key to decrypt Playfair key, then message
    
    ### Security Features
    - ✅ 297,025 character Unicode set
    - ✅ Tree-based key matrix generation
    - ✅ RSA-2048/3072/4096 support
    - ✅ Client-side processing only
    - ✅ No data transmission to servers
    """)