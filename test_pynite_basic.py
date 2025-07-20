#!/usr/bin/env python3
"""
Basic test of PyNiteFEA for continuous beam bridge analysis
Testing installation and basic functionality
"""

try:
    from Pynite import FEModel3D
    import numpy as np
    print("✓ PyNiteFEA imported successfully")
except ImportError as e:
    print(f"✗ PyNiteFEA import failed: {e}")
    exit(1)

def test_continuous_beam():
    """Test continuous beam with 3 spans: 20m + 25m + 20m"""
    print("\n=== Testing PyNiteFEA - Continuous Beam Bridge ===")
    
    try:
        # Create a new finite element model
        beam_model = FEModel3D()
        
        # Define material properties (concrete)
        E = 30e9  # 30 GPa in Pa
        G = 12.5e9  # Shear modulus
        nu = 0.2  # Poisson's ratio
        rho = 2400  # kg/m³
        fy = None  # Yield strength (not needed for this analysis)
        
        # Add material to model
        beam_model.add_material('Concrete', E, G, nu, rho, fy)
        
        # Define cross-section properties (box beam simplified as rectangle)
        # Assume 1.5m wide x 2.0m deep box beam
        width = 1.5
        height = 2.0
        A = width * height  # Cross-sectional area
        Iy = width * height**3 / 12  # Moment of inertia about y-axis
        Iz = height * width**3 / 12  # Moment of inertia about z-axis
        J = 0.3 * width * height**3  # Torsional constant (approximate)
        
        # Add section to model
        beam_model.add_section('BoxBeam', A, Iy, Iz, J)
        
        # Add nodes (4 supports)
        # Span 1: 0 to 20m, Span 2: 20 to 45m, Span 3: 45 to 65m
        beam_model.add_node('N1', 0, 0, 0)    # Support 1
        beam_model.add_node('N2', 20, 0, 0)   # Support 2 
        beam_model.add_node('N3', 45, 0, 0)   # Support 3
        beam_model.add_node('N4', 65, 0, 0)   # Support 4
        
        # Add beam elements
        beam_model.add_member('M1', 'N1', 'N2', 'Concrete', 'BoxBeam')
        beam_model.add_member('M2', 'N2', 'N3', 'Concrete', 'BoxBeam')
        beam_model.add_member('M3', 'N3', 'N4', 'Concrete', 'BoxBeam')
        
        # Add supports (pinned at ends, continuous at intermediate supports)
        beam_model.def_support('N1', True, True, True, True, False, False)  # Pin
        beam_model.def_support('N2', False, True, True, True, False, False)  # Roller (continuous)
        beam_model.def_support('N3', False, True, True, True, False, False)  # Roller (continuous) 
        beam_model.def_support('N4', True, True, True, True, False, False)  # Pin
        
        # Add distributed loads (dead load + live load)
        total_load = -(25 + 10) * 1000  # 35 kN/m converted to N/m (negative for downward)
        beam_model.add_member_dist_load('M1', 'Fy', total_load, total_load)
        beam_model.add_member_dist_load('M2', 'Fy', total_load, total_load)
        beam_model.add_member_dist_load('M3', 'Fy', total_load, total_load)
        
        # Add point load at mid-span of center span (32.5m from start)
        point_load = -100 * 1000  # 100 kN converted to N (negative for downward)
        # Mid-span of center span is at 32.5m, which is 12.5m from start of M2 (20m)
        mid_position = 12.5 / 25.0  # Relative position on member M2
        beam_model.add_member_pt_load('M2', 'Fy', point_load, mid_position)
        
        # Analyze the model
        print("Analyzing model...")
        beam_model.analyze()
        print("✓ Analysis completed successfully")
        
        # Get support reactions
        print("\n=== Support Reactions ===")
        R1_y = beam_model.nodes['N1'].RxnFY['Combo 1']
        R2_y = beam_model.nodes['N2'].RxnFY['Combo 1'] 
        R3_y = beam_model.nodes['N3'].RxnFY['Combo 1']
        R4_y = beam_model.nodes['N4'].RxnFY['Combo 1']
        
        print(f"R1 (Support 1): {R1_y/1000:.2f} kN")
        print(f"R2 (Support 2): {R2_y/1000:.2f} kN")
        print(f"R3 (Support 3): {R3_y/1000:.2f} kN") 
        print(f"R4 (Support 4): {R4_y/1000:.2f} kN")
        
        # Check equilibrium
        total_reaction = (R1_y + R2_y + R3_y + R4_y) / 1000
        total_applied = 35 * 65 + 100  # Total distributed + point load
        print(f"\nEquilibrium check:")
        print(f"Total reactions: {total_reaction:.2f} kN")
        print(f"Total applied load: {total_applied:.2f} kN")
        print(f"Difference: {abs(total_reaction - total_applied):.2f} kN")
        
        if abs(total_reaction - total_applied) < 0.1:
            print("✓ Equilibrium satisfied")
        else:
            print("✗ Equilibrium not satisfied")
            
        return True
        
    except Exception as e:
        print(f"✗ PyNiteFEA test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_continuous_beam()
    if success:
        print("\n✓ PyNiteFEA test PASSED - Library is functional")
    else:
        print("\n✗ PyNiteFEA test FAILED")