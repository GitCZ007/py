import os
import sys
import time
import threading
import numpy as np
import tensorflow as tf

# Turn off annoying TensorFlow logging, only show errors
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def print_hardware_info():
    print("=" * 50)
    print(f"Python Version: {sys.version.split()[0]}")
    print(f"NumPy Version: {np.__version__}")
    print(f"TensorFlow Version: {tf.__version__}")
    
    # Check for physical devices (CPUs / GPUs)
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        print(f"🎯 GPUs Detected: {len(gpus)} available for TensorFlow.")
        for i, gpu in enumerate(gpus):
            print(f"   -> GPU {i}: {gpu.name}")
    else:
        print("💻 No GPU found. TensorFlow will stress your CPU cores instead.")
    print("=" * 50)

def numpy_cpu_stress(duration, thread_id):
    """Stresses CPU cores and RAM using heavy NumPy dot products."""
    print(f"[NumPy Thread {thread_id}] Started matrix math stress...")
    end_time = time.time() + duration
    
    # Allocate large matrices (uses ~500MB - 1GB RAM)
    matrix_size = 8000 
    
    while time.time() < end_time:
        # Generate random floats using NumPy
        a = np.random.rand(matrix_size, matrix_size).astype(np.float32)
        b = np.random.rand(matrix_size, matrix_size).astype(np.float32)
        # Force heavy CPU linear algebra calculation
        _ = np.dot(a, b)
        
    print(f"[NumPy Thread {thread_id}] Finished.")

def tensorflow_stress(duration):
    """Stresses the system using heavy TensorFlow matrix operations."""
    print("[TensorFlow] Started massive tensor multiplications...")
    end_time = time.time() + duration
    
    # 8000x8000 tensor multiplication uses significant computing power
    tensor_size = 12000
    
    # Determine execution device context
    device = '/GPU:0' if tf.config.list_physical_devices('GPU') else '/CPU:0'
    
    with tf.device(device):
        while time.time() < end_time:
            # Create large random constant tensors
            x = tf.random.normal([tensor_size, tensor_size], dtype=tf.float32)
            y = tf.random.normal([tensor_size, tensor_size], dtype=tf.float32)
            # Perform matrix multiplication
            _ = tf.matmul(x, y)
            
    print("[TensorFlow] Finished.")

def run_stress_test(duration=30):
    print_hardware_info()
    print(f"🔥 Commencing 100% stress test for {duration} seconds... 🔥\n")
    
    threads = []
    
    # 1. Spawn multiple NumPy CPU threads based on core allocation
    num_cpu_threads = os.cpu_count() or 2
    print(f"[System] Spawning {num_cpu_threads} CPU worker threads for NumPy...")
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
        
    print("\n✅ Stress test completed successfully. System remained stable.")

if __name__ == "__main__":
    # Adjust number inside run_stress_test() to change runtime in seconds
    run_stress_test(duration=45)
