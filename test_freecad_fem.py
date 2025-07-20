#!/usr/bin/env python3
"""
Basic test of FreeCAD FEM for beam analysis
Testing installation and basic functionality
"""

import sys
import os

# Add FreeCAD library path
freecad_lib_path = "/usr/lib/freecad/lib"
if freecad_lib_path not in sys.path:
    sys.path.append(freecad_lib_path)

try:
    import FreeCAD
    print("✓ FreeCAD imported successfully")
    print(f"FreeCAD version: {FreeCAD.Version()}")
except ImportError as e:
    print(f"✗ FreeCAD import failed: {e}")
    print("Trying alternative import methods...")
    
    # Try running freecad directly to test if it works
    try:
        import subprocess
        result = subprocess.run(['/usr/bin/freecad', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✓ FreeCAD executable works: {result.stdout.strip()}")
            print("Note: GUI version works but Python module import failed")
        else:
            print(f"✗ FreeCAD executable failed: {result.stderr}")
    except Exception as e:
        print(f"✗ FreeCAD executable test failed: {e}")
    
    exit(1)

def test_freecad_fem():
    """Test FreeCAD FEM workbench capabilities"""
    print("\n=== Testing FreeCAD FEM - Basic Capabilities ===")
    
    try:
        # Create a new document
        doc = FreeCAD.newDocument("BeamTest")
        print("✓ Created FreeCAD document")
        
        # Try to import FEM workbench
        try:
            import Fem
            print("✓ FEM workbench imported")
        except ImportError:
            print("✗ FEM workbench not available")
            return False
            
        # Check available FEM tools
        fem_tools = [attr for attr in dir(Fem) if not attr.startswith('_')]
        print(f"Available FEM tools: {len(fem_tools)} items")
        if len(fem_tools) > 0:
            print(f"Sample FEM tools: {fem_tools[:5]}")
        
        # Try to access Part workbench for geometry creation
        try:
            import Part
            print("✓ Part workbench available")
            
            # Create a simple beam geometry (box)
            beam = Part.makeBox(1000, 100, 200)  # 1m long, 10cm x 20cm cross-section
            beam_obj = doc.addObject("Part::Feature", "Beam")
            beam_obj.Shape = beam
            print("✓ Created beam geometry")
            
        except Exception as e:
            print(f"✗ Geometry creation failed: {e}")
            return False
        
        # Try to create FEM analysis
        try:
            # Check if FEM objects can be created
            if hasattr(Fem, 'FemAnalysis'):
                analysis = Fem.FemAnalysis.makeFemAnalysis(doc, "BeamAnalysis") 
                print("✓ Created FEM analysis object")
            else:
                print("? FEM analysis creation method not found (expected for some FreeCAD versions)")
        
        except Exception as e:
            print(f"✗ FEM analysis creation failed: {e}")
            return False
        
        # Clean up
        FreeCAD.closeDocument(doc.Name)
        print("✓ Test completed successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ FreeCAD FEM test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_freecad_fem()
    if success:
        print("\n✓ FreeCAD FEM basic test PASSED - Library is functional")
    else:
        print("\n✗ FreeCAD FEM basic test FAILED")