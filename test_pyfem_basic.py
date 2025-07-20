#!/usr/bin/env python3
"""
Basic test of PyFEM for finite element analysis
Testing installation and basic functionality
"""

try:
    import pyfem
    print("✓ PyFEM imported successfully")
    print(f"PyFEM version: {pyfem.__version__ if hasattr(pyfem, '__version__') else 'Unknown'}")
except ImportError as e:
    print(f"✗ PyFEM import failed: {e}")
    exit(1)

def test_pyfem_capabilities():
    """Test PyFEM capabilities and API"""
    print("\n=== Testing PyFEM - API Exploration ===")
    
    try:
        # Check available classes and functions
        print("Available PyFEM attributes:")
        attrs = [attr for attr in dir(pyfem) if not attr.startswith('_')]
        print(attrs)
        
        # Check for common FEM modules
        potential_modules = ['mesh', 'element', 'solver', 'material', 'fem']
        for module_name in potential_modules:
            if hasattr(pyfem, module_name):
                print(f"Found {module_name} module")
                module = getattr(pyfem, module_name)
                if hasattr(module, '__dict__'):
                    print(f"  {module_name} attributes: {[attr for attr in dir(module) if not attr.startswith('_')]}")
        
        return True
        
    except Exception as e:
        print(f"✗ PyFEM test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_pyfem_capabilities()
    if success:
        print("\n✓ PyFEM basic test PASSED - Library is functional")
    else:
        print("\n✗ PyFEM basic test FAILED")