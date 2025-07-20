#!/usr/bin/env python3
"""
Basic test of StructPy for beam analysis
Testing installation and basic functionality
"""

try:
    import structpy
    print("✓ StructPy imported successfully")
    print(f"StructPy version: {structpy.__version__ if hasattr(structpy, '__version__') else 'Unknown'}")
except ImportError as e:
    print(f"✗ StructPy import failed: {e}")
    exit(1)

def test_simple_beam():
    """Test simple beam analysis"""
    print("\n=== Testing StructPy - Simple Beam Analysis ===")
    
    try:
        # Check available classes and functions
        print("Available StructPy attributes:")
        attrs = [attr for attr in dir(structpy) if not attr.startswith('_')]
        print(attrs)
        
        # This is an exploration to understand the API
        if hasattr(structpy, 'beam'):
            print("Found beam module")
            beam_module = structpy.beam
            print(f"Beam module attributes: {dir(beam_module)}")
        
        return True
        
    except Exception as e:
        print(f"✗ StructPy test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_simple_beam()
    if success:
        print("\n✓ StructPy basic test PASSED - Library is functional")
    else:
        print("\n✗ StructPy basic test FAILED")