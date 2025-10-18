"""
Key Generation Dashboard - Hybrid Cryptosystem
For RECEIVERS to generate their RSA key pairs.
"""

import streamlit as st
from hybrid_crypto import generate_rsa_keys, get_key_info

# Page configuration
st.set_page_config(
    page_title="Key Generation",
    page_icon="🔑",
    layout="wide"
)

# Header
st.title("🔑 RSA Key Generation Dashboard")
st.markdown("### Step 1: Receiver Generates Keys")
st.divider()

# Explanation
st.info("""
**👤 Who uses this?** RECEIVERS (people who want to receive encrypted messages)

**🎯 What it does:**
1. Generates a pair of RSA keys (Public + Private)
2. **Public Key** → Share with senders (safe to share publicly)
3. **Private Key** → Keep SECRET! Only you should have this (used to decrypt messages)

**📋 Workflow:**
1. Generate keys here
2. Download BOTH keys
3. Share PUBLIC key with sender
4. Keep PRIVATE key secure for decryption
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
    
    if 'public_key' in st.session_state:
        info = get_key_info(st.session_state.public_key)
        
        st.metric("Key Size", f"{info['key_size_bits']} bits")
        st.metric("Key Bytes", f"{info['key_size_bytes']} bytes")
        st.metric("Max Playfair Key", f"{info['recommended_playfair_key_length']} chars")
        
        st.success("✅ Keys ready!")
    else:
        st.info("Generate keys to see statistics")

# Download section
if 'public_key' in st.session_state and 'private_key' in st.session_state:
    st.divider()
    st.header("💾 Download Your Keys")
    
    col_dl1, col_dl2 = st.columns(2)
    
    with col_dl1:
        st.subheader("🔓 Public Key")
        st.success("✅ **SAFE TO SHARE** - Give this to people who want to send you encrypted messages")
        
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
            help="Share this file with senders",
            type="primary"
        )
        
        st.info("💡 Send this file via email, cloud storage, or any channel")
    
    with col_dl2:
        st.subheader("🔐 Private Key")
        st.error("⚠️ **NEVER SHARE THIS** - Keep it secret and secure!")
        
        # Preview private key (partially hidden)
        st.text_area("Private Key (Hidden)", value="********** CONFIDENTIAL **********", height=150, disabled=True)
        
        # Download button with warning
        st.download_button(
            label="📥 Download Private Key",
            data=st.session_state.private_key,
            file_name="my_private_key.pem",
            mime="text/plain",
            use_container_width=True,
            help="Store securely - NEVER share this!",
            type="secondary"
        )
        
        st.warning("⚠️ Store in encrypted folder or password manager")

    # Next steps
    st.divider()
    st.success("""
    ### ✅ Next Steps:
    
    **As a RECEIVER:**
    1. ✅ Download BOTH keys (done above)
    2. 📧 Send **PUBLIC key** to sender (via email, cloud, etc.)
    3. 🔐 Keep **PRIVATE key** secure (encrypted storage)
    4. 🔓 Use **Decryption Dashboard** when you receive encrypted messages
    
    **For the SENDER:**
    - Use the **PUBLIC key** you received in the **Encryption Dashboard**
    - They will encrypt messages that only YOU can decrypt
    """)

# Footer
st.divider()

with st.expander("🔒 Security Best Practices"):
    st.markdown("""
    ### Public Key (Safe to Share)
    - ✅ Can be sent via email
    - ✅ Can be posted publicly
    - ✅ Can be stored in cloud
    - ✅ Anyone can have a copy
    
    ### Private Key (Keep Secret!)
    - ❌ NEVER send via email
    - ❌ NEVER share with anyone
    - ❌ NEVER post online
    - ✅ Store in encrypted folder
    - ✅ Use password manager
    - ✅ Backup securely
    - ✅ If compromised, generate new keys
    
    ### Key Storage Recommendations
    1. **Password Manager** (1Password, LastPass, Bitwarden)
    2. **Encrypted USB Drive**
    3. **Encrypted Cloud Storage** (with strong password)
    4. **Hardware Security Module (HSM)** for enterprise
    """)

with st.expander("❓ Frequently Asked Questions"):
    st.markdown("""
    **Q: What if I lose my private key?**  
    A: You won't be able to decrypt any messages encrypted with your public key. Generate a new key pair and distribute the new public key.
    
    **Q: Can I use the same keys for multiple senders?**  
    A: Yes! Multiple people can use your public key to send you encrypted messages.
    
    **Q: How do I send my public key?**  
    A: Any method: email attachment, cloud link (Dropbox, Drive), USB, messaging apps, etc.
    
    **Q: What if someone gets my public key?**  
    A: That's fine! Public keys are meant to be shared. They can only encrypt, not decrypt.
    
    **Q: Should I generate new keys regularly?**  
    A: For high security, yes. For normal use, generate new keys if you suspect compromise or every 1-2 years.
    """)

st.caption("🔑 Hybrid Cryptosystem v1.0 | Key Generation for Receivers")