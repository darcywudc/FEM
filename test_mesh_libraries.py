#!/usr/bin/env python3
"""
Test mesh generation and I/O libraries
Testing meshio, pygmsh, and gmsh
"""

def test_meshio():
    """Test meshio for mesh I/O operations"""
    print("=== Testing meshio - Mesh I/O Library ===")
    
    try:
        import meshio
        import numpy as np
        print("✓ meshio imported successfully")
        print(f"meshio version: {meshio.__version__}")
        
        # Create a simple 1D mesh
        points = np.array([[0.0], [1.0], [2.0], [3.0], [4.0], [5.0]])
        cells = [("line", [[i, i+1] for i in range(5)])]
        
        mesh = meshio.Mesh(points, cells)
        print(f"✓ Created 1D mesh with {len(points)} points, {len(cells[0][1])} elements")
        
        # Test supported formats
        print(f"✓ Supported formats: {len(meshio.extension_to_filetype)} formats available")
        
        return True
        
    except Exception as e:
        print(f"✗ meshio test failed: {e}")
        return False

def test_pygmsh():
    """Test pygmsh for mesh generation"""
    print("\n=== Testing pygmsh - Python interface to Gmsh ===")
    
    try:
        import pygmsh
        print("✓ pygmsh imported successfully")
        print(f"pygmsh version: {pygmsh.__version__}")
        
        # Create a simple geometry
        with pygmsh.geo.Geometry() as geom:
            # Create a rectangle (for 2D beam cross-section)
            poly = geom.add_polygon([
                [0.0, 0.0],
                [1.0, 0.0], 
                [1.0, 0.5],
                [0.0, 0.5],
            ])
            geom.add_physical(poly.surface, "beam_section")
        
        print("✓ Created rectangular geometry")
        
        # Generate mesh
        mesh = pygmsh.generate_mesh(geom, dim=2)
        print(f"✓ Generated 2D mesh with {len(mesh.points)} points")
        
        return True
        
    except Exception as e:
        print(f"✗ pygmsh test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_gmsh():
    """Test gmsh directly"""
    print("\n=== Testing Gmsh - Direct API ===")
    
    try:
        import gmsh
        print("✓ Gmsh imported successfully")
        
        # Initialize gmsh
        gmsh.initialize()
        
        # Create a simple 1D model
        gmsh.model.add("beam_1d")
        
        # Add points
        p1 = gmsh.model.geo.addPoint(0, 0, 0)
        p2 = gmsh.model.geo.addPoint(1, 0, 0)
        p3 = gmsh.model.geo.addPoint(2, 0, 0)
        
        # Add lines
        l1 = gmsh.model.geo.addLine(p1, p2)
        l2 = gmsh.model.geo.addLine(p2, p3)
        
        # Synchronize
        gmsh.model.geo.synchronize()
        
        # Generate 1D mesh
        gmsh.model.mesh.generate(1)
        
        # Get mesh info
        node_tags, coords, _ = gmsh.model.mesh.getNodes()
        element_tags, element_types, element_nodes = gmsh.model.mesh.getElements()
        
        print(f"✓ Generated 1D mesh with {len(node_tags)} nodes")
        print(f"✓ Mesh has {len(element_tags[0]) if element_tags else 0} elements")
        
        # Clean up
        gmsh.finalize()
        
        return True
        
    except Exception as e:
        print(f"✗ Gmsh test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    meshio_success = test_meshio()
    pygmsh_success = test_pygmsh()
    gmsh_success = test_gmsh()
    
    successes = [meshio_success, pygmsh_success, gmsh_success]
    
    if all(successes):
        print("\n✅ ALL mesh library tests PASSED")
    elif any(successes):
        passed = sum(successes)
        print(f"\n⚠️  PARTIAL SUCCESS: {passed}/3 mesh libraries working")
    else:
        print("\n❌ ALL mesh library tests FAILED")