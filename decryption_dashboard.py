"""
Decryption Dashboard - Hybrid Cryptosystem
Decrypts messages using recipient's private key + RSA-encrypted Playfair key.
"""

import streamlit as st
import time
from hybrid_crypto import hybrid_decrypt

# Page configuration
st.set_page_config(
    page_title="Decryption Dashboard",
    page_icon="🔓",
    layout="wide"
)

# Header
st.title("🔓 Decryption Dashboard")
st.markdown("### Hybrid Cryptosystem: Tree-Based Playfair (545×545) + RSA")
st.divider()

# Initialize session state
if 'encrypted_message' not in st.session_state:
    st.session_state.encrypted_message = None
if 'encrypted_key' not in st.session_state:
    st.session_state.encrypted_key = None
if 'private_key' not in st.session_state:
    st.session_state.private_key = None

# Sidebar for key and file uploads
with st.sidebar:
    st.header("🔐 Decryption Requirements")
    
    st.subheader("1. Your Private Key")
    st.info("Upload YOUR private RSA key to decrypt the Playfair key.")
    
    # Upload private key
    uploaded_priv_key = st.file_uploader(
        "Upload Your PRIVATE Key (.pem)",
        type=['pem', 'txt'],
        help="This is YOUR secret key - never share it!"
    )
    
    if uploaded_priv_key:
        st.session_state.private_key = uploaded_priv_key.read()
        st.success("✅ Private key loaded!")
    
    # Option to paste private key
    with st.expander("Or paste PRIVATE key here"):
        pasted_priv = st.text_area(
            "Your Private Key (PEM format)",
            height=200,
            placeholder="-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----"
        )
        if pasted_priv and st.button("Load Pasted Private Key"):
            st.session_state.private_key = pasted_priv.encode('utf-8')
            st.success("✅ Private key loaded from text!")
    
    st.divider()
    
    st.subheader("2. Encrypted Files")
    
    # Upload encrypted message
    uploaded_message = st.file_uploader(
        "Upload Encrypted Message (.txt)",
        type=['txt'],
        help="The encrypted message file from sender"
    )
    
    if uploaded_message:
        st.session_state.encrypted_message = uploaded_message.read().decode('utf-8', errors='replace')
        st.success("✅ Encrypted message loaded!")
    
    # Upload encrypted key
    uploaded_enc_key = st.file_uploader(
        "Upload Encrypted Key (.bin)",
        type=['bin'],
        help="The RSA-encrypted Playfair key file"
    )
    
    if uploaded_enc_key:
        st.session_state.encrypted_key = uploaded_enc_key.read()
        st.success("✅ Encrypted key loaded!")

# Main content area
col1, col2 = st.columns([3, 2])

with col1:
    st.header("📋 Encrypted Data")
    
    # Display encrypted message preview
    st.subheader("Encrypted Message")
    if st.session_state.encrypted_message:
        msg_preview = st.session_state.encrypted_message[:500]
        st.text_area(
            "Message Preview",
            value=msg_preview + ("..." if len(st.session_state.encrypted_message) > 500 else ""),
            height=200,
            disabled=True
        )
        st.caption(f"Total length: {len(st.session_state.encrypted_message)} characters")
    else:
        st.info("No encrypted message loaded. Upload in sidebar.")
    
    st.divider()
    
    # Display encrypted key info
    st.subheader("Encrypted Key")
    if st.session_state.encrypted_key:
        st.success(f"✅ Encrypted key loaded ({len(st.session_state.encrypted_key)} bytes)")
        
        # Show hex preview
        hex_preview = st.session_state.encrypted_key[:32].hex()
        st.code(f"{hex_preview}...", language=None)
    else:
        st.info("No encrypted key loaded. Upload in sidebar.")

with col2:
    st.header("⚙️ Decryption Status")
    
    # Validation checks
    checks_passed = True
    
    with st.container():
        if st.session_state.private_key:
            st.success("✅ Private key loaded")
        else:
            st.error("❌ No private key")
            checks_passed = False
        
        if st.session_state.encrypted_message:
            st.success("✅ Encrypted message loaded")
        else:
            st.error("❌ No encrypted message")
            checks_passed = False
        
        if st.session_state.encrypted_key:
            st.success("✅ Encrypted key loaded")
        else:
            st.error("❌ No encrypted key")
            checks_passed = False
    
    st.divider()
    
    # Decryption button
    decrypt_button = st.button(
        "🔓 DECRYPT MESSAGE",
        type="primary",
        disabled=not checks_passed,
        use_container_width=True
    )

# Decryption process
if decrypt_button:
    try:
        with st.spinner("🔄 Decrypting message..."):
            start_time = time.time()
            
            # Perform hybrid decryption
            decrypted_message = hybrid_decrypt(
                st.session_state.encrypted_message,
                st.session_state.encrypted_key,
                st.session_state.private_key
            )
            
            decryption_time = time.time() - start_time
        
        st.success("✅ Message decrypted successfully!")
        
        # Display results
        st.divider()
        st.header("📖 Decrypted Message")
        
        col_metrics1, col_metrics2 = st.columns(2)
        
        with col_metrics1:
            st.metric("Decryption Time", f"{decryption_time:.4f} sec")
        
        with col_metrics2:
            st.metric("Message Length", f"{len(decrypted_message)} chars")
        
        # Display decrypted message
        st.subheader("Decrypted Content")
        st.text_area(
            "Your Message",
            value=decrypted_message,
            height=300,
            disabled=False
        )
        
        # Download decrypted message
        st.divider()
        st.subheader("💾 Download Decrypted Message")
        
        col_dl1, col_dl2 = st.columns([2, 1])
        
        with col_dl1:
            st.download_button(
                label="📄 Download Decrypted Message",
                data=decrypted_message.encode('utf-8', errors='replace'),
                file_name="decrypted_message.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col_dl2:
            # Copy to clipboard helper
            st.info("Message decrypted and ready to use!")
        
        # Success message
        st.divider()
        st.success("""
        ✅ **Decryption Complete!**
        
        Your message has been successfully decrypted. You can now:
        - Read the message above
        - Download it as a text file
        - Copy the content for use elsewhere
        """)
        
    except ValueError as ve:
        st.error("❌ Decryption failed: Invalid key or corrupted data")
        st.error(f"Error details: {str(ve)}")
        
        with st.expander("🔍 Troubleshooting"):
            st.markdown("""
            **Common issues:**
            - ❌ Wrong private key (doesn't match the public key used for encryption)
            - ❌ Corrupted encrypted key file
            - ❌ Corrupted encrypted message file
            - ❌ Files from different encryption sessions mixed up
            
            **Solutions:**
            - Verify you're using the correct private key
            - Re-download the encrypted files from sender
            - Ensure files weren't modified during transfer
            """)
    
    except Exception as e:
        st.error(f"❌ Unexpected error during decryption: {str(e)}")
        st.exception(e)

# Footer
st.divider()
with st.expander("ℹ️ How This Works"):
    st.markdown("""
    ### Hybrid Decryption Process
    
    1. **RSA Decryption**: Your private key decrypts the RSA-encrypted Playfair key
    2. **Playfair Decryption**: The recovered Playfair key decrypts the actual message
    3. **Message Recovery**: You get the original plaintext message
    
    ### Security Notes
    - 🔒 Your private key is NEVER sent anywhere - it stays on your device
    - 🔒 Only YOU can decrypt messages encrypted with your public key
    - 🔒 The Playfair key is unique to each message
    - 🔒 Without your private key, the message cannot be decrypted
    
    ### Key Safety
    - ⚠️ **NEVER share your private key**
    - ⚠️ Store it securely (encrypted storage, password manager)
    - ⚠️ Back it up in a secure location
    - ⚠️ If compromised, generate new keys immediately
    """)

# Additional info section
with st.expander("📚 File Format Guide"):
    st.markdown("""
    ### Expected File Formats
    
    **Private Key (.pem)**
    ```
    -----BEGIN RSA PRIVATE KEY-----
    [Base64 encoded key data]
    -----END RSA PRIVATE KEY-----
    ```
    
    **Encrypted Message (.txt)**
    - Text file containing the Playfair-encrypted message
    - May contain Unicode characters
    
    **Encrypted Key (.bin)**
    - Binary file containing RSA-encrypted Playfair key
    - Typically 256 bytes for RSA-2048
    """)

st.caption("🔓 Hybrid Cryptosystem v1.0 | Tree-Based Playfair + RSA")