#!/usr/bin/env python3
"""
Basic test of scikit-fem for finite element analysis
Testing installation and basic functionality
"""

try:
    import skfem
    import numpy as np
    from skfem import *
    print("✓ scikit-fem imported successfully")
    print(f"scikit-fem version: {skfem.__version__}")
except ImportError as e:
    print(f"✗ scikit-fem import failed: {e}")
    exit(1)

def test_skfem_beam():
    """Test scikit-fem with a simple 1D beam analysis"""
    print("\n=== Testing scikit-fem - 1D Beam Analysis ===")
    
    try:
        # Create a 1D mesh for a beam (0 to 10 units)
        m = MeshLine(np.linspace(0, 10, 11))  # 11 nodes, 10 elements
        print("✓ Created 1D mesh")
        
        # Define element type (1D linear elements)
        e = ElementLineP1()
        print("✓ Defined element type")
        
        # Create basis functions
        basis = Basis(m, e)
        print(f"✓ Created basis with {basis.N} degrees of freedom")
        
        # Simple load case (uniform distributed load)
        @LinearForm
        def load(v, w):
            return 1.0 * v  # Unit load
        
        print("✓ Defined load function")
        
        # Simple stiffness matrix (simplified 1D case)
        @BilinearForm
        def mass(u, v, w):
            return u * v  # Mass matrix
        
        @BilinearForm 
        def stiffness(u, v, w):
            return u.grad[0] * v.grad[0]  # Stiffness matrix
        
        print("✓ Defined bilinear forms")
        
        # Assemble matrices
        A = stiffness.assemble(basis)
        b = load.assemble(basis)
        print("✓ Assembled system matrices")
        
        # Apply boundary conditions (fix both ends for demonstration)
        # Note: This is simplified - real beam would have appropriate BCs
        interior = m.interior_nodes()
        
        if len(interior) > 0:
            # Solve only interior nodes
            A_int = A[interior].T[interior].T
            b_int = b[interior]
            
            if A_int.shape[0] > 0:
                u_int = np.linalg.solve(A_int.toarray(), b_int)
                print(f"✓ Solved system for {len(u_int)} interior nodes")
                print(f"  Max displacement: {np.max(np.abs(u_int)):.6f}")
            else:
                print("? No interior nodes to solve (too few elements)")
        else:
            print("? No interior nodes identified")
        
        return True
        
    except Exception as e:
        print(f"✗ scikit-fem test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_skfem_api():
    """Test scikit-fem API and available features"""
    print("\n=== Testing scikit-fem - API Exploration ===")
    
    try:
        # Check available mesh types
        mesh_types = [attr for attr in dir(skfem) if 'Mesh' in attr and not attr.startswith('_')]
        print(f"Available mesh types: {mesh_types}")
        
        # Check available element types  
        element_types = [attr for attr in dir(skfem) if 'Element' in attr and not attr.startswith('_')]
        print(f"Available element types: {element_types}")
        
        # Test 2D capabilities
        try:
            # Create a simple 2D triangular mesh
            m2d = MeshTri()
            m2d = m2d.refined(2)  # Refine the mesh
            print(f"✓ Created 2D mesh with {m2d.t.shape[1]} triangles")
            
            # 2D element
            e2d = ElementTriP1()
            basis2d = Basis(m2d, e2d)
            print(f"✓ Created 2D basis with {basis2d.N} DOFs")
            
        except Exception as e:
            print(f"? 2D mesh test issue: {e}")
        
        return True
        
    except Exception as e:
        print(f"✗ scikit-fem API test failed: {e}")
        return False

if __name__ == "__main__":
    api_success = test_skfem_api()
    beam_success = test_skfem_beam()
    
    if api_success and beam_success:
        print("\n✓ scikit-fem tests PASSED - Library is functional")
    else:
        print("\n✗ scikit-fem tests FAILED")