import cv2
import sys

def test_camera():
    """Test camera access and list available cameras"""
    print("Testing camera access...")
    
    # Try different camera indices
    for i in range(4):
        print(f"\nTesting camera index {i}...")
        cap = cv2.VideoCapture(i)
        
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"✅ Camera {i} is working!")
                print(f"   Frame size: {frame.shape}")
                print(f"   Frame type: {frame.dtype}")
                
                # Try to display the frame
                cv2.imshow(f'Camera {i}', frame)
                print("   Press any key to continue...")
                cv2.waitKey(3000)  # Wait 3 seconds
                cv2.destroyAllWindows()
            else:
                print(f"❌ Camera {i} opened but can't read frames")
            cap.release()
        else:
            print(f"❌ Camera {i} not available")
    
    print("\nCamera test completed!")

if __name__ == "__main__":
    test_camera() 