"""
Pure Playfair Benchmark Dashboard
Tests ONLY the 545×545 Playfair cipher (no RSA overhead)
For comparison with hybrid system performance.
"""

import streamlit as st
import time
import statistics
from custom_playfair import playfair_encrypt_custom, playfair_decrypt_custom
from tree_playfair_custom import build_playfair_matrix_custom

# Page configuration
st.set_page_config(
    page_title="Pure Playfair Benchmark",
    page_icon="📊",
    layout="wide"
)
    
# Header
st.title("📊 Pure Playfair Cipher Benchmark")
st.markdown("### 545×545 Matrix - Symmetric Encryption Only (No RSA)")
st.divider()

st.info("""
**Purpose:** Measure pure Playfair performance WITHOUT RSA overhead.

This isolates the symmetric encryption component to compare against:
- Hybrid system (Playfair + RSA)
- Pure RSA (slower, size-limited)

**Use this data for:** Tables 1, 2, 3 in your research paper.
""")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Benchmark Configuration")
    
    # Playfair key
    st.subheader("Playfair Key")
    playfair_key = st.text_input(
        "Encryption Key",
        value="BENCHMARK_KEY_2024_TESTING",
        max_chars=256,
        help="Key for Playfair matrix generation"
    )
    
    st.divider()
    
    # Message size selection
    st.subheader("Message Sizes to Test")
    test_100b = st.checkbox("100 bytes", value=True)
    test_1kb = st.checkbox("1 KB (1,024 bytes)", value=True)
    test_10kb = st.checkbox("10 KB (10,240 bytes)", value=True)
    test_100kb = st.checkbox("100 KB (102,400 bytes)", value=True)
    test_1mb = st.checkbox("1 MB (1,048,576 bytes)", value=False, 
                           help="May take several minutes")
    
    st.divider()
    
    # Iterations
    st.subheader("Test Parameters")
    iterations = st.number_input(
        "Iterations per test",
        min_value=0,
        max_value=1000,
        value=100,
        help="More iterations = more accurate averages"
    )
    
    warmup_iterations = st.number_input(
        "Warmup iterations",
        min_value=0,
        max_value=50,
        value=10,
        help="Discarded runs to warm up CPU cache"
    )

# Build message size list
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
    
    if not message_sizes:
        st.warning("⚠️ Select at least one message size to test")
    else:
        st.info(f"Will test {len(message_sizes)} message size(s) with {iterations} iterations each")
        
        # Run benchmark button
        if st.button("🚀 Run Benchmark", type="primary", use_container_width=True):
            results = {}
            keygen_results = {}
            
            def safe_progress(bar, value):
                """Clamps progress between 0.0 and 1.0 before updating."""
                bar.progress(max(0.0, min(float(value), 1.0)))
            
            # Verify key is valid
            if not playfair_key:
                st.error("❌ Please enter a Playfair key")
            else:
                # Progress tracking
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                total_tests = len(message_sizes) * 2  # Encryption + Decryption
                current_test = 0
                
                # === KEY GENERATION BENCHMARK ===
                st.subheader("🔑 Key Generation Performance")
                
                key_lengths = [8, 32, 128, 256]
                for length in key_lengths:
                    current_test += 1
                    status_text.text(f"Testing Playfair Matrix ({length}-char key) generation... ({current_test}/{total_tests})")
                    
                    keygen_times = []
                    with st.spinner(f"Generating Playfair Matrix ({length}-char key) ({iterations} iterations)..."):
                        for i in range(iterations):
                            start = time.perf_counter()
                            _ = build_playfair_matrix_custom(playfair_key[:length])
                            end = time.perf_counter()
                            keygen_times.append((end - start) * 1000)
                            
                            if i % 10 == 0:
                                progress = current_test / total_tests
                                progress_bar.progress(min(progress, 1.0))
                    
                    keygen_results[length] = {
                        'mean': statistics.mean(keygen_times),
                        'stdev': statistics.stdev(keygen_times) if len(keygen_times) > 1 else 0,
                        'median': statistics.median(keygen_times),
                        'min': min(keygen_times),
                        'max': max(keygen_times)
                    }
                
                # Display key generation results
                keygen_data = []
                for length in key_lengths:
                    if length in keygen_results:
                        kg = keygen_results[length]
                        keygen_data.append({
                            'Operation': f"Playfair Matrix ({length}-char key)",
                            'Time (ms)': f"{kg['mean']:.2f}",
                            'Time (s)': f"{(kg['mean'] / 1000):.2f}",
                            'Mean ± Std Dev (ms)': f"{kg['mean']:.2f} ± {kg['stdev']:.2f}"
                        })
                for key_size in [2048, 3072, 4096]:
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
                for idx, size in enumerate(message_sizes):
                    label = size_labels[idx]
                    
                    # Generate test message
                    message = "A" * size
                    
                    # === ENCRYPTION BENCHMARK ===
                    current_test += 1
                    status_text.text(f"Testing {label} encryption... ({current_test}/{total_tests})")
                    
                    # Warmup
                    for _ in range(warmup_iterations):
                        _ = playfair_encrypt_custom(message, playfair_key)
                    
                    # Actual benchmark
                    enc_times = []
                    with st.spinner(f"Encrypting {label} ({iterations} iterations)..."):
                        for i in range(iterations):
                            start = time.perf_counter()
                            cipher = playfair_encrypt_custom(message, playfair_key)
                            end = time.perf_counter()
                            enc_times.append((end - start) * 1000)  # Convert to ms
                            
                            # Update progress
                            if i % 10 == 0:
                                # inside loops
                                progress = (current_test - 1 + (i / iterations)) / total_tests
                                safe_progress(progress_bar, progress)

                    
                    # === DECRYPTION BENCHMARK ===
                    current_test += 1
                    status_text.text(f"Testing {label} decryption... ({current_test}/{total_tests})")
                    
                    # Pre-encrypt for decryption test
                    cipher = playfair_encrypt_custom(message, playfair_key)
                    
                    # Warmup
                    for _ in range(warmup_iterations):
                        _ = playfair_decrypt_custom(cipher, playfair_key)
                    
                    # Actual benchmark
                    dec_times = []
                    with st.spinner(f"Decrypting {label} ({iterations} iterations)..."):
                        for i in range(iterations):
                            start = time.perf_counter()
                            decrypted = playfair_decrypt_custom(cipher, playfair_key)
                            end = time.perf_counter()
                            dec_times.append((end - start) * 1000)
                            
                            # Update progress
                            if i % 10 == 0:
                                progress = current_test / total_tests
                                safe_progress(progress_bar, progress)
                    
                    # Store results
                    results[label] = {
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
                
                safe_progress(progress_bar, 1.0)
                status_text.text("✅ Benchmark complete!")
                st.success("🎉 All tests completed successfully!")
                
                # === DISPLAY RESULTS ===
                st.divider()
                st.header("📈 Results Summary")
                
                # Table 1: Encryption Times
                st.subheader("Encryption Performance")
                
                table1_data = []
                for label in size_labels:
                    if label in results:
                        enc = results[label]['encryption']
                        table1_data.append({
                            'Message Size': label,
                            'Mean (ms)': f"{enc['mean']:.2f}",
                            'Std Dev (ms)': f"{enc['stdev']:.2f}",
                            'Median (ms)': f"{enc['median']:.2f}",
                            'Min (ms)': f"{enc['min']:.2f}",
                            'Max (ms)': f"{enc['max']:.2f}"
                        })
                
                st.dataframe(table1_data, use_container_width=True)
                
                # Table 2: Decryption Times
                st.subheader("Decryption Performance")
                
                table2_data = []
                for label in size_labels:
                    if label in results:
                        dec = results[label]['decryption']
                        table2_data.append({
                            'Message Size': label,
                            'Mean (ms)': f"{dec['mean']:.2f}",
                            'Std Dev (ms)': f"{dec['stdev']:.2f}",
                            'Median (ms)': f"{dec['median']:.2f}",
                            'Min (ms)': f"{dec['min']:.2f}",
                            'Max (ms)': f"{dec['max']:.2f}"
                        })
                
                st.dataframe(table2_data, use_container_width=True)
                
                # Table 3: Throughput
                st.subheader("Throughput Analysis")
                
                table3_data = []
                for label in size_labels:
                    if label in results:
                        size_kb = results[label]['size_bytes'] / 1024
                        enc = results[label]['encryption']
                        dec = results[label]['decryption']
                        
                        enc_throughput = size_kb / (enc['mean'] / 1000)  # KB/s
                        dec_throughput = size_kb / (dec['mean'] / 1000)  # KB/s
                        
                        table3_data.append({
                            'Message Size': label,
                            'Size (KB)': f"{size_kb:.2f}",
                            'Encryption (KB/s)': f"{enc_throughput:,.2f}",
                            'Decryption (KB/s)': f"{dec_throughput:,.2f}",
                            'Time per KB (ms)': f"{enc['mean'] / size_kb:.2f}"
                        })
                
                st.dataframe(table3_data, use_container_width=True)

with col2:
    st.header("ℹ️ About This Test")
    
    st.markdown("""
    ### What's Being Tested
    
    **Pure Playfair Cipher:**
    - 545×545 matrix (297,025 characters)
    - Tree-based matrix generation
    - O(1) dictionary lookup
    - NO RSA overhead
    
    ### Metrics Captured
    
    1. **Encryption Time**
       - Mean, median, std dev
       - Min/max values
       
    2. **Decryption Time**
       - Mean, median, std dev
       - Min/max values
       
    3. **Throughput**
       - KB/s for encryption
       - KB/s for decryption
       - Time per KB
       
    4. **Key Generation**
       - Time for matrix generation
       - Time for RSA key pair generation
    
    ### Why This Matters
    
    Pure Playfair results establish the **baseline symmetric performance**.
    
    Compare against:
    - Hybrid system (adds RSA overhead)
    - Pure RSA (slower, size-limited)
    - AES-256 (industry standard)
    """)
    
    st.divider()
    
    st.markdown("""
    ### Tips for Accurate Results
    
    ✅ **Do:**
    - Close other applications
    - Use consistent key length
    - Run multiple iterations (100+)
    - Test during low system load
    
    ❌ **Don't:**
    - Run while downloading/streaming
    - Test on battery power (laptops)
    - Mix different message types
    - Interrupt running tests
    """)

# Footer
st.divider()

with st.expander("🔬 Technical Details"):
    st.markdown("""
    ### Algorithm Complexity
    
    **Matrix Generation:** O(n) where n = 297,025
    - BFS tree construction: O(n)
    - DFS traversal: O(n)
    - Position map building: O(n²) one-time cost
    
    **Per-Character Encryption:** O(1)
    - Dictionary lookup: O(1)
    - Matrix indexing: O(1)
    - Total for message of length m: O(m)
    
    **Expected Performance:**
    - Small messages (<1KB): Matrix generation dominates
    - Large messages (>10KB): Encryption time dominates
    - Throughput should stabilize for messages >100KB
    
    ### Memory Footprint
    
    - Matrix: ~8-12 MB (Python objects)
    - Position map: ~2-3 MB (dictionary)
    - Total: ~10-15 MB constant overhead
    """)

with st.expander("📊 How to Use These Results"):
    st.markdown("""
    ### For Your Research Paper
    
    **Table 1 (Section 5.2.1):**
    ```
    Copy the "Pure Playfair" column values into your 
    encryption time comparison table.
    ```
    
    **Table 2 (Section 5.2.2):**
    ```
    Copy the "Pure Playfair" column values into your 
    decryption time comparison table.
    ```
    
    **Table 3 (Section 5.2.3):**
    ```
    Copy the throughput values for analysis of 
    performance scaling with message size.
    ```
    
    ### Analysis Questions to Answer
    
    1. Does encryption time scale linearly with message size?
    2. Is decryption time approximately equal to encryption time?
    3. At what message size does throughput stabilize?
    4. What's the overhead of matrix generation vs. encryption?
    5. How does this compare to your hybrid system?
    """)

st.caption("📊 Pure Playfair Benchmark v1.0 | Symmetric Component Only")