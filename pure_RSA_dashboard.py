"""
Pure RSA Benchmark Dashboard
Tests ONLY RSA-OAEP encryption (no Playfair)
For comparison with hybrid system performance.
LIMITED TO SMALL MESSAGES due to RSA size constraints.
"""

import streamlit as st
import time
import statistics
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP

def generate_rsa_keys(key_size=2048):
    key = RSA.generate(key_size)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def rsa_encrypt(public_key_bytes, message):
    if isinstance(message, str):
        message_bytes = message.encode('utf-8')
    else:
        message_bytes = message
    key = RSA.import_key(public_key_bytes)
    cipher = PKCS1_OAEP.new(key)
    max_length = (key.size_in_bits() // 8) - 42
    if len(message_bytes) > max_length:
        raise ValueError(f"Message exceeds RSA-OAEP capacity")
    return cipher.encrypt(message_bytes)

def rsa_decrypt(private_key_bytes, encrypted_message):
    key = RSA.import_key(private_key_bytes)
    cipher = PKCS1_OAEP.new(key)
    return cipher.decrypt(encrypted_message)

def get_rsa_max_message_length(public_key_bytes):
    key = RSA.import_key(public_key_bytes)
    return (key.size_in_bits() // 8) - 42

# Page configuration
st.set_page_config(
    page_title="Pure RSA Benchmark",
    page_icon="🔐",
    layout="wide"
)

# Header
st.title("🔐 Pure RSA-OAEP Benchmark")
st.markdown("### Asymmetric Encryption Only (No Playfair)")
st.divider()

st.warning("""
⚠️ **Size Limitation:** RSA can only encrypt small messages directly.

**Maximum Message Sizes:**
- RSA-2048: 214 bytes max
- RSA-3072: 342 bytes max  
- RSA-4096: 470 bytes max

For larger messages, hybrid systems (like yours) are necessary.
""")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Benchmark Configuration")
    
    # RSA key sizes to test
    st.subheader("RSA Key Sizes")
    test_rsa_2048 = st.checkbox("RSA-2048 (214 bytes max)", value=True)
    test_rsa_3072 = st.checkbox("RSA-3072 (342 bytes max)", value=True)
    test_rsa_4096 = st.checkbox("RSA-4096 (470 bytes max)", value=True)
    
    st.divider()
    
    # Message sizes (constrained by RSA limits)
    st.subheader("Message Sizes to Test")
    st.caption("⚠️ Limited by RSA-OAEP padding overhead")
    
    test_50b = st.checkbox("50 bytes", value=True)
    test_100b = st.checkbox("100 bytes", value=True)
    test_200b = st.checkbox("200 bytes", value=True, 
                            help="Only works with RSA-2048+")
    test_300b = st.checkbox("300 bytes", value=False,
                            help="Only works with RSA-3072+")
    test_400b = st.checkbox("400 bytes", value=False,
                            help="Only works with RSA-4096 only")
    
    st.divider()
    
    # Iterations
    st.subheader("Test Parameters")
    iterations = st.number_input(
        "Iterations per test",
        min_value=1,
        max_value=500,
        value=100,
        help="RSA is slow - fewer iterations than Playfair"
    )
    
    warmup_iterations = st.number_input(
        "Warmup iterations",
        min_value=0,
        max_value=20,
        value=5,
        help="Warmup runs (discarded)"
    )
    
    st.divider()
    
    # Key generation timing
    st.subheader("Additional Tests")
    test_keygen = st.checkbox(
        "Include key generation timing",
        value=True,
        help="Measure RSA key pair generation time"
    )

# Build test configuration
rsa_key_sizes = []
if test_rsa_2048:
    rsa_key_sizes.append(2048)
if test_rsa_3072:
    rsa_key_sizes.append(3072)
if test_rsa_4096:
    rsa_key_sizes.append(4096)

message_sizes = []
size_labels = []
if test_50b:
    message_sizes.append(50)
    size_labels.append("50B")
if test_100b:
    message_sizes.append(100)
    size_labels.append("100B")
if test_200b:
    message_sizes.append(200)
    size_labels.append("200B")
if test_300b:
    message_sizes.append(300)
    size_labels.append("300B")
if test_400b:
    message_sizes.append(400)
    size_labels.append("400B")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🎯 Benchmark Results")
    
    if not rsa_key_sizes:
        st.warning("⚠️ Select at least one RSA key size to test")
    elif not message_sizes:
        st.warning("⚠️ Select at least one message size to test")
    else:
        st.info(f"Will test {len(rsa_key_sizes)} key size(s) × {len(message_sizes)} message size(s) with {iterations} iterations each")
        
        # Run benchmark button
        if st.button("🚀 Run Benchmark", type="primary", use_container_width=True):
            results = {}
            keygen_results = {}
            
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Calculate total tests
            valid_combinations = 0
            for key_size in rsa_key_sizes:
                max_msg_size = (key_size // 8) - 42
                for msg_size in message_sizes:
                    if msg_size <= max_msg_size:
                        valid_combinations += 1
            
            total_tests = valid_combinations * 2  # Encryption + Decryption
            if test_keygen:
                total_tests += len(rsa_key_sizes)  # Key generation tests
            
            current_test = 0
            
            # === KEY GENERATION BENCHMARK (if enabled) ===
            if test_keygen:
                st.subheader("🔑 Key Generation Performance")
                
                for key_size in rsa_key_sizes:
                    current_test += 1
                    status_text.text(f"Testing RSA-{key_size} key generation... ({current_test}/{total_tests})")
                    
                    keygen_times = []
                    with st.spinner(f"Generating RSA-{key_size} keys ({iterations} iterations)..."):
                        for i in range(iterations):
                            start = time.perf_counter()
                            priv, pub = generate_rsa_keys(key_size)
                            end = time.perf_counter()
                            keygen_times.append((end - start) * 1000)
                            
                            if i % 10 == 0:
                                progress = current_test / total_tests
                                progress_bar.progress(min(progress, 1.0))
                    
                    keygen_results[key_size] = {
                        'mean': statistics.mean(keygen_times),
                        'stdev': statistics.stdev(keygen_times) if len(keygen_times) > 1 else 0,
                        'median': statistics.median(keygen_times),
                        'min': min(keygen_times),
                        'max': max(keygen_times)
                    }
                
                # Display key generation results
                keygen_data = []
                for key_size in rsa_key_sizes:
                    if key_size in keygen_results:
                        kg = keygen_results[key_size]
                        keygen_data.append({
                            'Operation': f"RSA-{key_size} Key Pair",
                            'Time (ms)': f"{kg['mean']:.2f}",
                            'Time (s)': f"{(kg['mean'] / 1000):.2f}",
                            'Mean ± Std Dev (ms)': f"{kg['mean']:.2f} ± {kg['stdev']:.2f}"
                        })
                
                st.dataframe(keygen_data, use_container_width=True)
                st.divider()
            
            # === ENCRYPTION/DECRYPTION BENCHMARK ===
            for key_size in rsa_key_sizes:
                # Generate key pair once for this size
                status_text.text(f"Generating RSA-{key_size} keys for testing...")
                priv_key, pub_key = generate_rsa_keys(key_size)
                max_msg_size = get_rsa_max_message_length(pub_key)
                
                results[key_size] = {}
                
                for idx, size in enumerate(message_sizes):
                    label = size_labels[idx]
                    
                    # Check if message fits in RSA capacity
                    if size > max_msg_size:
                        st.warning(f"⚠️ Skipping {label} for RSA-{key_size} (exceeds {max_msg_size} byte limit)")
                        continue
                    
                    # Generate test message
                    message_bytes = b"A" * size
                    
                    # === ENCRYPTION BENCHMARK ===
                    current_test += 1
                    status_text.text(f"RSA-{key_size}: Encrypting {label}... ({current_test}/{total_tests})")
                    
                    # Warmup
                    for _ in range(warmup_iterations):
                        _ = rsa_encrypt(pub_key, message_bytes)
                    
                    # Actual benchmark
                    enc_times = []
                    with st.spinner(f"RSA-{key_size} encrypting {label} ({iterations} iterations)..."):
                        for i in range(iterations):
                            start = time.perf_counter()
                            encrypted = rsa_encrypt(pub_key, message_bytes)
                            end = time.perf_counter()
                            enc_times.append((end - start) * 1000)
                            
                            # Update progress
                            if i % 10 == 0:
                                progress = (current_test - 1 + (i / iterations)) / total_tests
                                progress_bar.progress(min(progress, 1.0))
                    
                    # === DECRYPTION BENCHMARK ===
                    current_test += 1
                    status_text.text(f"RSA-{key_size}: Decrypting {label}... ({current_test}/{total_tests})")
                    
                    # Pre-encrypt for decryption test
                    encrypted = rsa_encrypt(pub_key, message_bytes)
                    
                    # Warmup
                    for _ in range(warmup_iterations):
                        _ = rsa_decrypt(priv_key, encrypted)
                    
                    # Actual benchmark
                    dec_times = []
                    with st.spinner(f"RSA-{key_size} decrypting {label} ({iterations} iterations)..."):
                        for i in range(iterations):
                            start = time.perf_counter()
                            decrypted = rsa_decrypt(priv_key, encrypted)
                            end = time.perf_counter()
                            dec_times.append((end - start) * 1000)
                            
                            if i % 10 == 0:
                                progress = current_test / total_tests
                                progress_bar.progress(progress)
                    
                    # Store results
                    results[key_size][label] = {
                        'size_bytes': size,
                        'encryption': {
                            'mean': statistics.mean(enc_times),
                            'stdev': statistics.stdev(enc_times) if len(enc_times) > 1 else 0,
                            'median': statistics.median(enc_times),
                            'min': min(enc_times),
                            'max': max(enc_times)
                        },
                        'decryption': {
                            'mean': statistics.mean(dec_times),
                            'stdev': statistics.stdev(dec_times) if len(dec_times) > 1 else 0,
                            'median': statistics.median(dec_times),
                            'min': min(dec_times),
                            'max': max(dec_times)
                        }
                    }
            
            progress_bar.progress(1.0)
            status_text.text("✅ Benchmark complete!")
            st.success("🎉 All tests completed successfully!")
            
            # === DISPLAY RESULTS ===
            st.divider()
            st.header("📈 Results Summary")
            
            # Table 1: Encryption Times
            st.subheader("Encryption Performance (milliseconds)")
            
            table1_data = []
            for label in size_labels:
                row = {'Message Size': label}
                for key_size in rsa_key_sizes:
                    if key_size in results and label in results[key_size]:
                        enc = results[key_size][label]['encryption']
                        row[f'RSA-{key_size}'] = f"{enc['mean']:.2f} ± {enc['stdev']:.2f}"
                    else:
                        row[f'RSA-{key_size}'] = "N/A"
                table1_data.append(row)
            
            st.dataframe(table1_data, use_container_width=True)
            
            # Table 2: Decryption Times
            st.subheader("Decryption Performance (milliseconds)")
            
            table2_data = []
            for label in size_labels:
                row = {'Message Size': label}
                for key_size in rsa_key_sizes:
                    if key_size in results and label in results[key_size]:
                        dec = results[key_size][label]['decryption']
                        row[f'RSA-{key_size}'] = f"{dec['mean']:.2f} ± {dec['stdev']:.2f}"
                    else:
                        row[f'RSA-{key_size}'] = "N/A"
                table2_data.append(row)
            
            st.dataframe(table2_data, use_container_width=True)
            
            # Table 3: Throughput
            st.subheader("Throughput Analysis (KB/s)")
            
            table3_data = []
            for label in size_labels:
                row = {'Message Size': label}
                for key_size in rsa_key_sizes:
                    if key_size in results and label in results[key_size]:
                        size_kb = results[key_size][label]['size_bytes'] / 1024
                        enc_mean = results[key_size][label]['encryption']['mean'] / 1000
                        throughput = size_kb / enc_mean if enc_mean > 0 else 0
                        row[f'RSA-{key_size}'] = f"{throughput:.2f}"
                    else:
                        row[f'RSA-{key_size}'] = "N/A"
                table3_data.append(row)
            
            st.dataframe(table3_data, use_container_width=True)

with col2:
    st.header("ℹ️ About This Test")
    
    st.markdown("""
    ### What's Being Tested
    
    **Pure RSA-OAEP:**
    - Asymmetric encryption only
    - OAEP padding with SHA-256
    - Multiple key sizes
    - NO Playfair symmetric component
    
    ### Metrics Captured
    
    1. **Encryption Time**
       - Mean, median, std dev
       - Min/max values
       
    2. **Decryption Time**
       - Mean, median, std dev
       - Min/max values
       
    3. **Throughput**
       - KB/s for encryption
       
    4. **Key Generation** (optional)
       - Time to generate key pairs
    
    ### Why This Matters
    
    Pure RSA results show asymmetric performance limits.
    
    Compare against:
    - Pure Playfair (fast, scalable)
    - Hybrid system (combines both)
    - Demonstrates why hybrid is necessary
    """)
    
    st.divider()
    
    st.markdown("""
    ### Tips for Accurate Results
    
    ✅ **Do:**
    - Test small iterations first (RSA slow)
    - Use consistent message patterns
    - Run during low system load
    - Test keygen separately if needed
    
    ❌ **Don't:**
    - Select sizes exceeding RSA limits
    - Run too many iterations (time-consuming)
    - Compare directly to Playfair (different scales)
    """)

# Footer
st.divider()

with st.expander("🔬 Technical Details"):
    st.markdown("""
    ### RSA Complexity
    
    **Encryption:** O(k^2) where k = key size bits
    - Public exponent operations
    
    **Decryption:** O(k^3)
    - Private exponent (slower)
    
    **Key Generation:** Variable
    - Prime number finding dominates
    
    **Limitations:**
    - Direct encryption: max < key_bytes - 42
    - Slow for repeated operations
    - Not suitable for bulk data
    
    **Expected Patterns:**
    - Decryption 5-20× slower than encryption
    - Larger keys: exponentially slower
    - Small messages: constant time per operation
    """)

with st.expander("📊 How to Use These Results"):
    st.markdown("""
    ### For Your Research Paper
    
    **Table 1 (Section 5.2.1):**
    ```
    Copy the "Pure RSA" column values into your 
    encryption time comparison table.
    ```
    
    **Table 2 (Section 5.2.2):**
    ```
    Copy the "Pure RSA" column values into your 
    decryption time comparison table.
    ```
    
    **Table 3 (Section 5.2.3):**
    ```
    Copy the throughput values for analysis of 
    performance scaling with message size.
    ```
    
    ### Analysis Questions to Answer
    
    1. How does RSA time scale with key size?
    2. What's the enc/dec time ratio?
    3. At what point does hybrid become necessary?
    4. Compare RSA-2048 to Playfair for 100B
    5. Why is RSA alone impractical for large data?
    """)

st.caption("🔐 Pure RSA Benchmark v1.0 | Asymmetric Component Only")
