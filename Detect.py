
import cv2
import os

# Define paths
HAAR_CASCADE_PATH = r'C:/Users/kisho/OneDrive/Desktop/face/haarcascade_frontalface_default.xml'
MODEL_PATH = r'C:\Users\kisho\OneDrive\Desktop\face\Kishore_model.yml'
INTRUDER_IMAGE_PATH = r'C:\Users\kisho\OneDrive\Desktop\face\intruder.jpg'

# Load HAAR face classifier
face_classifier = cv2.CascadeClassifier(HAAR_CASCADE_PATH)

# Load pre-trained model
if os.path.exists(MODEL_PATH):
    Kishore_model = cv2.face.LBPHFaceRecognizer_create()
    Kishore_model.read(MODEL_PATH)
else:
    raise FileNotFoundError("Trained model not found. Please train the model first.")

# Initialize webcam
camera = cv2.VideoCapture(0)

# Face detector function
def face_detector(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
    if len(faces) == 0:
        return img, None
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
        roi = gray[y:y + h, x:x + w]
        roi = cv2.resize(roi, (200, 200))
    return img, roi

# Start the detection process
def start_detection():
    while True:
        ret, frame = camera.read()
        if not ret:
            print("Error: Unable to access the webcam.")
            break

        image, face = face_detector(frame)
        try:
            if face is not None:
                result = Kishore_model.predict(face)
                confidence = int(100 * (1 - (result[1]) / 400))

                if confidence > 85:  # Verified User
                    cv2.putText(image, "Verified User", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                else:  # Intruder Alert
                    cv2.putText(image, "Intruder Detected", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                    cv2.imwrite(INTRUDER_IMAGE_PATH, frame)
            else:
                cv2.putText(frame, "No Face Detected", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

        except Exception as e:
            print(f"Error during detection: {str(e)}")

        cv2.imshow('Face Recognition', image)

        # Stop detection on Enter key press (key 13)
        if cv2.waitKey(1) == 13:
            break

    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("Starting detection...")
    start_detection()
