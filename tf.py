import os
import sys
import time
import threading
import numpy as np
import tensorflow as tf

# Turn off annoying TensorFlow logging, only show errors
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Define path to store logs inside OKD container (/tmp is always writable)
LOG_FILE_PATH = "/mnt/stress.log"

def log_and_print(message):
    """Prints to console and appends to the log file simultaneously."""
    print(message)
    try:
        with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
            f.write(message + "\n")
    except Exception as e:
        print(f"⚠️ Failed to write to log file: {e}")

def print_hardware_info():
    log_and_print("=" * 50)
    log_and_print(f"Python Version: {sys.version.split()[0]}")
    log_and_print(f"NumPy Version: {np.__version__}")
    log_and_print(f"TensorFlow Version: {tf.__version__}")
    
    # Check for physical devices (CPUs / GPUs)
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        log_and_print(f"🎯 GPUs Detected: {len(gpus)} available for TensorFlow.")
        for i, gpu in enumerate(gpus):
            log_and_print(f"   -> GPU {i}: {gpu.name}")
    else:
        log_and_print("💻 No GPU found. TensorFlow will stress your CPU cores instead.")
    log_and_print("=" * 50)

def numpy_cpu_stress(duration, thread_id):
    """Stresses CPU cores and RAM using heavy NumPy dot products."""
    log_and_print(f"[NumPy Thread {thread_id}] Started matrix math stress...")
    end_time = time.time() + duration
    
    # Allocate large matrices (uses ~500MB - 1GB RAM)
    matrix_size = 12000 
    
    while time.time() < end_time:
        # Generate random floats using NumPy
        a = np.random.rand(matrix_size, matrix_size).astype(np.float32)
        b = np.random.rand(matrix_size, matrix_size).astype(np.float32)
        # Force heavy CPU linear algebra calculation
        _ = np.dot(a, b)
        
    log_and_print(f"[NumPy Thread {thread_id}] Finished.")

def tensorflow_stress(duration):
    """Stresses the system using heavy TensorFlow matrix operations."""
    log_and_print("[TensorFlow] Started massive tensor multiplications...")
    end_time = time.time() + duration
    
    # 16000x16000 tensor multiplication uses significant computing power
    tensor_size = 16000
    
    # Determine execution device context
    device = '/GPU:0' if tf.config.list_physical_devices('GPU') else '/CPU:0'
    
    with tf.device(device):
        while time.time() < end_time:
            # Create large random constant tensors
            x = tf.random.normal([tensor_size, tensor_size], dtype=tf.float32)
            y = tf.random.normal([tensor_size, tensor_size], dtype=tf.float32)
            # Perform matrix multiplication
            _ = tf.matmul(x, y)
            
    log_and_print("[TensorFlow] Finished.")

def run_stress_test(duration=30):
    # Clear out any older log entries before starting
    if os.path.exists(LOG_FILE_PATH):
        os.remove(LOG_FILE_PATH)
        
    print_hardware_info()
    log_and_print(f"🔥 Commencing 100% stress test for {duration} seconds... 🔥\n")
    
    threads = []
    
    # 1. Spawn multiple NumPy CPU threads based on core allocation
    num_cpu_threads = os.cpu_count() or 2
    log_and_print(f"[System] Spawning {num_cpu_threads} CPU worker threads for NumPy...")
    for i in range(num_cpu_threads):
        t = threading.Thread(target=numpy_cpu_stress, args=(duration, i))
        threads.append(t)
        t.start()
        
    # 2. Spawn a separate TensorFlow processing thread
    tf_thread = threading.Thread(target=tensorflow_stress, args=(duration,))
    threads.append(tf_thread)
    tf_thread.start()
    
    # Wait for all workers to wrap up execution safely
    for t in threads:
        t.join()
        
    log_and_print(f"\n✅ Stress test completed successfully. Log saved to {LOG_FILE_PATH}")

if __name__ == "__main__":
    # Adjust number inside run_stress_test() to change runtime in seconds
    run_stress_test(duration=45)
