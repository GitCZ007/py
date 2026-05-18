import sys
import time

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

def run_numpy_suite():
    print("=" * 50)
    print("🔢 NUMPY MODULE VERIFICATION SUITE")
    print("=" * 50)
    
    # 1. Immediate dependency validation check
    if not NUMPY_AVAILABLE:
        print("🔴 ERROR: NumPy is not installed or accessible in this context.")
        print(f"Current Executable: {sys.executable}")
        print("Please resolve your requirements layer or run: pip install numpy")
        print("=" * 50)
        return

    print(f"🟢 Success: NumPy imported successfully.")
    print(f"📦 Version Detected: {np.__version__}")
    print("=" * 50)

    try:
        # 2. Test Base Array Allocation and Data Typing
        print("👉 Test 1: Array Creation & Allocation...")
        test_array = np.array([1, 2, 3, 4, 5], dtype=np.float64)
        print(f"   • Array: {test_array}")
        print(f"   • Shape: {test_array.shape} | Type: {test_array.dtype}")
        
        # 3. Test Vectorised Mathematical Aggregations
        print("\n👉 Test 2: Mathematical Aggregations...")
        print(f"   • Mean:   {np.mean(test_array)}")
        print(f"   • StdDev: {np.std(test_array):.4f}")
        print(f"   • Sin:    {np.sin(test_array[:2])}")

        # 4. Test High-Performance Linear Algebra (Matrix Multiplication)
        print("\n👉 Test 3: Matrix Multiplication (Dot Product)...")
        matrix_a = np.random.rand(1000, 1000)
        matrix_b = np.random.rand(1000, 1000)
        
        start_time = time.time()
        dot_product = np.dot(matrix_a, matrix_b)
        duration = time.time() - start_time
        
        print(f"   • Scaled 1000x1000 operation executed in: {duration:.4f} seconds")
        print(f"   • Output Matrix Shape: {dot_product.shape}")
        
        print("=" * 50)
        print("✅ ALL NUMPY TEST CASES PASSED SUCCESSFULLY")
        print("=" * 50)

    except Exception as e:
        print(f"🔴 CRITICAL ERROR DURING FUNCTIONAL TESTING: {e}")
        print("=" * 50)

if __name__ == "__main__":
    run_numpy_suite()
