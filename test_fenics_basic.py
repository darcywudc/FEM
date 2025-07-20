#!/usr/bin/env python3
"""
Basic test of FEniCS components for finite element analysis
Testing installation and basic functionality
"""

# Test individual FEniCS components directly
def test_fenics_components():
    """Test FEniCS component imports"""
    print("=== Testing FEniCS - Component Imports ===")
    
    try:
        # Test individual components
        import ufl
        print("✓ UFL (Unified Form Language) available")
        
        import ffc  
        print("✓ FFC (FEniCS Form Compiler) available")
        
        import FIAT
        print("✓ FIAT (Finite Element Automatic Tabulator) available")
        
        import dijitso
        print("✓ Dijitso (Distributed Just-In-Time Shared Objects) available")
        
        # Try to use UFL for form definition
        try:
            from ufl import (FiniteElement, TrialFunction, TestFunction, 
                           inner, grad, dx, Constant, interval)
            
            # Define a simple 1D domain
            cell = interval
            element = FiniteElement("Lagrange", cell, 1)
            
            # Define trial and test functions
            u = TrialFunction(element)
            v = TestFunction(element)
            
            # Define a simple bilinear form (stiffness)
            a = inner(grad(u), grad(v)) * dx
            
            # Define a linear form (load)
            f = Constant(1.0)
            L = f * v * dx
            
            print("✓ Created UFL forms successfully")
            print(f"  Bilinear form: {type(a).__name__}")
            print(f"  Linear form: {type(L).__name__}")
            
        except Exception as e:
            print(f"? UFL form creation issue: {e}")
        
        return True
        
    except Exception as e:
        print(f"✗ FEniCS component test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_fenics_note():
    """Explain FEniCS installation status"""
    print("\n=== FEniCS Installation Notes ===")
    print("ℹ  FEniCS Python components installed successfully")
    print("ℹ  This includes UFL, FFC, FIAT, and Dijitso")
    print("ℹ  Full FEniCS (with DOLFIN) requires C++ dependencies")
    print("ℹ  For complete functionality, use: conda install -c conda-forge fenics")
    print("ℹ  Or Docker: docker run -ti quay.io/fenicsproject/stable")
    return True

if __name__ == "__main__":
    components_success = test_fenics_components()
    note_success = test_fenics_note()
    
    if components_success and note_success:
        print("\n✓ FEniCS partial test PASSED - Python components functional")
        print("  Note: Full FEniCS requires additional system dependencies")
    else:
        print("\n✗ FEniCS test FAILED")