"""
Hybrid Benchmark Dashboard
Tests the full hybrid system: Tree-Based Playfair + RSA-OAEP
For complete system performance measurement.
"""

import streamlit as st
import time
import statistics
import secrets
from hybrid_crypto import generate_rsa_keys, hybrid_encrypt, hybrid_decrypt
from custom_unicode import CHAR_SET

# Page configuration
st.set_page_config(
    page_title="Hybrid Benchmark",
    page_icon="📈",
    layout="wide"
)

# Header
st.title("📈 Hybrid Cryptosystem Benchmark")
st.markdown("### Tree-Based Playfair (545×545) + RSA-OAEP")
st.divider()

st.info("""
**Purpose:** Measure full hybrid performance: Playfair for message + RSA for key exchange.

This combines both components to show real-world usage.
Compare against pure Playfair and pure RSA benchmarks.

**Note:** This test is CPU-intensive. Close other apps for best results.
""")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Benchmark Configuration")
    
    # RSA key sizes
    st.subheader("RSA Key Sizes")
    test_rsa_2048 = st.checkbox("RSA-2048", value=True)
    test_rsa_3072 = st.checkbox("RSA-3072", value=True)
    test_rsa_4096 = st.checkbox("RSA-4096", value=True)
    
    # Playfair key length
    playfair_key_length = st.slider(
        "Playfair Key Length",
        min_value=8,
        max_value=128,
        value=32,
        help="Must fit in RSA max (auto-validated)"
    )
    
    st.divider()
    
    # Message sizes
    st.subheader("Message Sizes to Test")
    test_100b = st.checkbox("100 bytes", value=True)
    test_1kb = st.checkbox("1 KB", value=True)
    test_10kb = st.checkbox("10 KB", value=True)
    test_100kb = st.checkbox("100 KB", value=True)
    test_1mb = st.checkbox("1 MB", value=False)
    
    st.divider()
    
    # Test parameters
    st.subheader("Test Parameters")
    iterations = st.number_input(
        "Iterations per test",
        min_value=1,
        max_value=1000,
        value=100
    )
    
    warmup_iterations = st.number_input(
        "Warmup iterations",
        min_value=0,
        max_value=50,
        value=10
    )

# Build configurations
rsa_key_sizes = []
if test_rsa_2048: rsa_key_sizes.append(2048)
if test_rsa_3072: rsa_key_sizes.append(3072)
if test_rsa_4096: rsa_key_sizes.append(4096)

message_sizes = []
size_labels = []
if test_100b:
    message_sizes.append(100)
    size_labels.append("100B")
if test_1kb:
    message_sizes.append(1024)
    size_labels.append("1KB")
if test_10kb:
    message_sizes.append(10240)
    size_labels.append("10KB")
if test_100kb:
    message_sizes.append(102400)
    size_labels.append("100KB")
if test_1mb:
    message_sizes.append(1048576)
    size_labels.append("1MB")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🎯 Benchmark Results")
    
    if not rsa_key_sizes or not message_sizes:
        st.warning("⚠️ Select at least one RSA size and message size")
    else:
        st.info(f"Will test {len(rsa_key_sizes)} RSA size(s) × {len(message_sizes)} message size(s) with {iterations} iterations each")
        
        if st.button("🚀 Run Benchmark", type="primary", use_container_width=True):
            results = {}
            
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            total_tests = len(rsa_key_sizes) * len(message_sizes) * 2  # Enc + Dec
            current_test = 0
            
            for rsa_size in rsa_key_sizes:
                # Generate key pair once per size
                priv, pub = generate_rsa_keys(rsa_size)
                
                results[rsa_size] = {}
                
                for idx, msg_size in enumerate(message_sizes):
                    label = size_labels[idx]
                    
                    # Generate test message
                    message = "A" * msg_size
                    
                    # Generate Playfair key (random, fixed length)
                    safe_chars = [c for c in CHAR_SET[:1000] if 32 <= ord(c) <= 126]
                    playfair_key = ''.join(secrets.choice(safe_chars) for _ in range(playfair_key_length))
                    
                    # === ENCRYPTION BENCHMARK ===
                    current_test += 1
                    status_text.text(f"RSA-{rsa_size}: Encrypting {label}... ({current_test}/{total_tests})")
                    
                    # Warmup
                    for _ in range(warmup_iterations):
                        _ = hybrid_encrypt(message, playfair_key, pub)
                    
                    # Actual benchmark
                    enc_times = []
                    for i in range(iterations):
                        start = time.perf_counter()
                        cipher, enc_key = hybrid_encrypt(message, playfair_key, pub)
                        end = time.perf_counter()
                        enc_times.append((end - start) * 1000)
                        
                        if i % 10 == 0:
                                progress = current_test / total_tests
                                progress_bar.progress(min(progress, 1.0))
                    
                    # === DECRYPTION BENCHMARK ===
                    current_test += 1
                    status_text.text(f"RSA-{rsa_size}: Decrypting {label}... ({current_test}/{total_tests})")
                    
                    # Pre-encrypt for dec test
                    cipher, enc_key = hybrid_encrypt(message, playfair_key, pub)
                    
                    # Warmup
                    for _ in range(warmup_iterations):
                        _ = hybrid_decrypt(cipher, enc_key, priv)
                    
                    # Actual benchmark
                    dec_times = []
                    for i in range(iterations):
                        start = time.perf_counter()
                        decrypted = hybrid_decrypt(cipher, enc_key, priv)
                        end = time.perf_counter()
                        dec_times.append((end - start) * 1000)
                        
                        # Update progress
                        if i % 10 == 0:
                            progress = (current_test - 1 + (i / iterations)) / total_tests
                            progress_bar.progress(min(progress, 1.0))
                    
                    # Store results
                    results[rsa_size][label] = {
                        'size_bytes': msg_size,
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
            
            # Display results
            st.divider()
            st.header("📈 Results Summary")
            
            # Table 1: Encryption Times
            st.subheader("Encryption Performance (milliseconds)")
            
            table1_data = []
            for label in size_labels:
                row = {'Message Size': label}
                for rsa_size in rsa_key_sizes:
                    if rsa_size in results and label in results[rsa_size]:
                        enc = results[rsa_size][label]['encryption']
                        row[f'Hybrid ({rsa_size})'] = f"{enc['mean']:.2f} ± {enc['stdev']:.2f}"
                    else:
                        row[f'Hybrid ({rsa_size})'] = "N/A"
                table1_data.append(row)
            
            st.dataframe(table1_data, use_container_width=True)
            
            # Table 2: Decryption Times
            st.subheader("Decryption Performance (milliseconds)")
            
            table2_data = []
            for label in size_labels:
                row = {'Message Size': label}
                for rsa_size in rsa_key_sizes:
                    if rsa_size in results and label in results[rsa_size]:
                        dec = results[rsa_size][label]['decryption']
                        row[f'Hybrid ({rsa_size})'] = f"{dec['mean']:.2f} ± {dec['stdev']:.2f}"
                    else:
                        row[f'Hybrid ({rsa_size})'] = "N/A"
                table2_data.append(row)
            
            st.dataframe(table2_data, use_container_width=True)
            
            # Table 3: Throughput
            st.subheader("Throughput Analysis (KB/s)")
            
            table3_data = []
            for label in size_labels:
                row = {'Message Size': label}
                for rsa_size in rsa_key_sizes:
                    if rsa_size in results and label in results[rsa_size]:
                        size_kb = results[rsa_size][label]['size_bytes'] / 1024
                        enc_mean = results[rsa_size][label]['encryption']['mean'] / 1000
                        throughput = size_kb / enc_mean if enc_mean > 0 else 0
                        row[f'Hybrid ({rsa_size})'] = f"{throughput:,.2f}"
                    else:
                        row[f'Hybrid ({rsa_size})'] = "N/A"
                table3_data.append(row)
            
            st.dataframe(table3_data, use_container_width=True)

with col2:
    st.header("ℹ️ About This Test")
    
    st.markdown("""
    ### What's Being Tested
    
    **Full Hybrid System:**
    - Playfair for message encryption
    - RSA for key exchange
    - Tree-based matrix
    - O(1) lookup
    
    ### Metrics Captured
    
    1. **Encryption Time**
    2. **Decryption Time**
    3. **Throughput (KB/s)**
    
    ### Why This Matters
    
    Shows real-world hybrid performance.
    Compare against pure components.
    """)
    
    st.divider()
    
    st.markdown("""
    ### Tips for Accurate Results
    
    ✅ 100+ iterations
    ✅ Close other apps
    ✅ Test during low load
    """)

# Footer
st.divider()

with st.expander("🔬 Technical Details"):
    st.markdown("""
    Hybrid adds constant RSA overhead to Playfair's linear scaling.
    """)

with st.expander("📊 How to Use Results"):
    st.markdown("""
    Fill Hybrid columns in paper tables.
    """)

st.caption("📈 Hybrid Benchmark v1.0")