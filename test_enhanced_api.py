"""
Test script for Enhanced 3D Geometry Analysis API
"""
import requests
import json
import os

# Configuration
BASE_URL = "http://localhost:5000"
SAMPLE_FILE = "sample_files/420-21634.STEP"

def test_upload():
    """Test file upload"""
    print("=" * 70)
    print("TEST 1: File Upload")
    print("=" * 70)
    
    with open(SAMPLE_FILE, 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{BASE_URL}/api/upload", files=files)
    
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Response: {json.dumps(data, indent=2)}")
    
    if data.get('success'):
        print("✓ Upload successful!")
        return data['filepath']
    else:
        print("✗ Upload failed!")
        return None

def test_enhanced_analyze(filepath):
    """Test enhanced analysis"""
    print("\n" + "=" * 70)
    print("TEST 2: Enhanced Analysis")
    print("=" * 70)
    
    payload = {'filepath': filepath}
    response = requests.post(
        f"{BASE_URL}/api/enhanced-analyze",
        json=payload,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"Status Code: {response.status_code}")
    data = response.json()
    
    if data.get('success'):
        print("✓ Analysis successful!")
        print("\nParser Used:", data.get('parser_used'))
        
        # Geometry info
        geometry = data.get('geometry', {})
        print("\nGeometry Information:")
        print(f"  Dimensions: {geometry.get('dimensions')}")
        print(f"  Volume: {geometry.get('volume')} mm³")
        print(f"  Surface Area: {geometry.get('surface_area')} mm²")
        print(f"  Vertices: {geometry.get('vertex_count')}")
        print(f"  Faces: {geometry.get('face_count')}")
        
        # Mesh quality
        mesh_quality = data.get('mesh_quality', {})
        print("\nMesh Quality:")
        print(f"  Rating: {mesh_quality.get('quality_rating')}")
        print(f"  Watertight: {mesh_quality.get('is_watertight')}")
        print(f"  Manifold: {mesh_quality.get('is_manifold')}")
        print(f"  Avg Triangle Quality: {mesh_quality.get('avg_triangle_quality')}")
        print(f"  Degenerate Faces: {mesh_quality.get('degenerate_faces')}")
        
        # Quality report
        quality_report = data.get('quality_report', '')
        if quality_report:
            print("\nQuality Report:")
            print(quality_report)
        
        return True
    else:
        print("✗ Analysis failed!")
        print(f"Error: {data.get('error')}")
        return False

def main():
    """Run all tests"""
    print("\n🔬 Enhanced 3D Geometry Analysis API Test")
    print("=" * 70)
    print(f"Sample File: {SAMPLE_FILE}")
    print(f"File Size: {os.path.getsize(SAMPLE_FILE)} bytes")
    print()
    
    # Test 1: Upload
    filepath = test_upload()
    if not filepath:
        print("\n❌ Tests failed at upload stage")
        return
    
    # Test 2: Enhanced Analysis
    success = test_enhanced_analyze(filepath)
    
    if success:
        print("\n" + "=" * 70)
        print("✅ ALL TESTS PASSED!")
        print("=" * 70)
        print("\n🌐 Open your browser to test the UI:")
        print(f"   {BASE_URL}/enhanced-test")
        print()
    else:
        print("\n❌ Tests failed at analysis stage")

if __name__ == '__main__':
    main()
