"""
Encryption Dashboard - Hybrid Cryptosystem
Encrypts messages using Playfair cipher + RSA key exchange.
"""

import streamlit as st
import time
import secrets
from hybrid_crypto import generate_rsa_keys, hybrid_encrypt
from custom_unicode import CHAR_SET

# Page configuration
st.set_page_config(
    page_title="Encryption Dashboard",
    page_icon="🔒",
    layout="wide"
)

# Header
st.title("🔒 Encryption Dashboard")
st.markdown("### Hybrid Cryptosystem: Tree-Based Playfair (545×545) + RSA")
st.divider()

# Initialize session state
if 'generated_playfair_key' not in st.session_state:
    st.session_state.generated_playfair_key = None
if 'recipient_public_key' not in st.session_state:
    st.session_state.recipient_public_key = None
if 'recipient_private_key' not in st.session_state:
    st.session_state.recipient_private_key = None

# Sidebar for key management
with st.sidebar:
    st.header("🔑 Key Management")
    
    st.subheader("1. Recipient's Public Key")
    st.info("""
    **Where to get it?**
    - Recipient generates keys using **Key Generation Dashboard**
    - They send you their PUBLIC key file
    - Upload it below
    """)
    
    # Important note
    st.warning("⚠️ **You need the RECIPIENT'S public key** (not your own!)")
    
    # Option 1: Generate test keys (for solo testing)
    with st.expander("🧪 Testing Mode (No Recipient Available)"):
        st.caption("Generate test keys if you don't have a recipient yet")
        if st.button("🎲 Generate Test RSA Keys", help="For testing only"):
            priv, pub = generate_rsa_keys()
            st.session_state.recipient_private_key = priv
            st.session_state.recipient_public_key = pub
            st.success("✅ Test keys generated!")
            st.info("💡 Download the private key below to test decryption later")
    
    # Option 2: Upload recipient's public key
    uploaded_pub_key = st.file_uploader(
        "Upload Recipient's PUBLIC Key (.pem)",
        type=['pem', 'txt'],
        help="Upload the recipient's public RSA key file"
    )
    
    if uploaded_pub_key:
        st.session_state.recipient_public_key = uploaded_pub_key.read()
        st.success("✅ Public key loaded!")
    
    # Option 3: Paste recipient's public key
    with st.expander("Or paste PUBLIC key here"):
        pasted_pub = st.text_area(
            "Recipient's Public Key (PEM format)",
            height=150,
            placeholder="-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----"
        )
        if pasted_pub and st.button("Load Pasted Key"):
            st.session_state.recipient_public_key = pasted_pub.encode('utf-8')
            st.success("✅ Public key loaded from text!")
    
    st.divider()
    
    # Playfair key section
    st.subheader("2. Playfair Key")
    
    key_length = st.slider(
        "Key Length",
        min_value=8,
        max_value=214,
        value=32,
        help="Length must be ≤256 for RSA encryption"
    )
    
    if st.button("🎲 Generate Random Playfair Key"):
        # Generate random key from safe character subset
        safe_chars = [c for c in CHAR_SET[:1000] if 32 <= ord(c) <= 126]
        random_key = ''.join(secrets.choice(safe_chars) for _ in range(key_length))
        st.session_state.generated_playfair_key = random_key
        st.success("✅ Random key generated!")
    
    # Display generated key
    if st.session_state.generated_playfair_key:
        st.text_area(
            "Generated Playfair Key",
            value=st.session_state.generated_playfair_key,
            height=100,
            disabled=True
        )

# Main content area
col1, col2 = st.columns([3, 2])

with col1:
    st.header("📝 Message Input")
    
    # Message input options
    input_method = st.radio(
        "Input Method",
        ["Type Message", "Upload File"],
        horizontal=True
    )
    
    message = ""
    
    if input_method == "Type Message":
        message = st.text_area(
            "Enter your message",
            height=200,
            placeholder="Type your secret message here..."
        )
    else:
        uploaded_file = st.file_uploader(
            "Upload text file",
            type=['txt'],
            help="Upload a .txt file containing your message"
        )
        if uploaded_file:
            message = uploaded_file.read().decode('utf-8', errors='replace')
            st.text_area("File Content Preview", value=message[:500], height=200, disabled=True)
    
    st.divider()
    
    # Playfair key input
    st.subheader("🔑 Playfair Key")
    
    key_input_method = st.radio(
        "Key Source",
        ["Use Generated Key", "Enter Manually"],
        horizontal=True
    )
    
    playfair_key = ""
    
    if key_input_method == "Use Generated Key":
        if st.session_state.generated_playfair_key:
            playfair_key = st.session_state.generated_playfair_key
            st.info(f"Using generated key ({len(playfair_key)} characters)")
        else:
            st.warning("⚠️ Generate a key in the sidebar first!")
    else:
        playfair_key = st.text_input(
            "Enter Playfair Key Manually",
            max_chars=256,
            placeholder="Enter your secret key (max 256 chars)"
        )

with col2:
    st.header("⚙️ Encryption Status")
    
    # Validation checks
    checks_passed = True
    
    with st.container():
        if st.session_state.recipient_public_key:
            st.success("✅ Recipient's public key loaded")
        else:
            st.error("❌ No recipient public key")
            checks_passed = False
        
        if message:
            st.success(f"✅ Message ready ({len(message)} chars)")
        else:
            st.error("❌ No message entered")
            checks_passed = False
        
        if playfair_key:
            st.success(f"✅ Playfair key ready ({len(playfair_key)} chars)")
        else:
            st.error("❌ No Playfair key")
            checks_passed = False
    
    st.divider()
    
    # Encryption button
    encrypt_button = st.button(
        "🔒 ENCRYPT MESSAGE",
        type="primary",
        disabled=not checks_passed,
        use_container_width=True
    )

# Encryption process
if encrypt_button:
    try:
        with st.spinner("🔄 Encrypting message..."):
            start_time = time.time()
            
            # Perform hybrid encryption
            cipher_text, encrypted_key = hybrid_encrypt(
                message,
                playfair_key,
                st.session_state.recipient_public_key
            )
            
            encryption_time = time.time() - start_time
        
        st.success("✅ Message encrypted successfully!")
        
        # Display results
        st.divider()
        st.header("📦 Encrypted Output")
        
        col_out1, col_out2 = st.columns(2)
        
        with col_out1:
            st.metric("Encryption Time", f"{encryption_time:.4f} sec")
            st.metric("Cipher Length", f"{len(cipher_text)} chars")
        
        with col_out2:
            st.metric("Original Length", f"{len(message)} chars")
            st.metric("Encrypted Key Size", f"{len(encrypted_key)} bytes")
        
        # Preview encrypted message
        st.subheader("Encrypted Message Preview")
        st.code(cipher_text[:200] + "..." if len(cipher_text) > 200 else cipher_text)
        
        # Download section
        st.divider()
        st.subheader("💾 Download Encrypted Data")
        
        col_dl1, col_dl2, col_dl3 = st.columns(3)
        
        with col_dl1:
            st.download_button(
                label="📄 Download Encrypted Message",
                data=cipher_text.encode('utf-8', errors='replace'),
                file_name="encrypted_message.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col_dl2:
            st.download_button(
                label="🔑 Download Encrypted Key",
                data=encrypted_key,
                file_name="encrypted_playfair_key.bin",
                mime="application/octet-stream",
                use_container_width=True
            )
        
        with col_dl3:
            # Download recipient's public key (for reference)
            if st.session_state.recipient_public_key:
                st.download_button(
                    label="🔓 Download Public Key",
                    data=st.session_state.recipient_public_key,
                    file_name="recipient_public_key.pem",
                    mime="text/plain",
                    use_container_width=True
                )
        
        # Optional: Download private key for testing
        if st.session_state.recipient_private_key:
            st.warning("⚠️ Testing Mode: Private key available")
            st.download_button(
                label="🔐 Download Private Key (TEST ONLY)",
                data=st.session_state.recipient_private_key,
                file_name="recipient_private_key.pem",
                mime="text/plain",
                help="In production, the recipient already has this!"
            )
        
        # Instructions
        st.divider()
        st.info("""
        **Next Steps:**
        1. Download the **Encrypted Message** and **Encrypted Key**
        2. Send both files to the recipient
        3. The recipient uses the **Decryption Dashboard** with their **Private Key**
        """)
        
    except Exception as e:
        st.error(f"❌ Encryption failed: {str(e)}")
        st.exception(e)

# Footer
st.divider()
with st.expander("ℹ️ How This Works"):
    st.markdown("""
    ### Hybrid Encryption Process
    
    1. **Playfair Encryption**: Your message is encrypted using a custom 545×545 Playfair cipher
    2. **RSA Key Exchange**: The Playfair key is encrypted with the recipient's RSA public key
    3. **Secure Delivery**: Send both the encrypted message and encrypted key to the recipient
    4. **Decryption**: Only the recipient (with their private key) can decrypt the Playfair key and then the message
    
    ### Security Features
    - ✅ 297,025 character Unicode set (545×545 matrix)
    - ✅ Tree-based key matrix generation (BFS/DFS)
    - ✅ RSA-2048 public key encryption for key exchange
    - ✅ Random padding for enhanced security
    - ✅ No key reuse between sessions
    """)

st.caption("🔒 Hybrid Cryptosystem v1.0 | Tree-Based Playfair + RSA")