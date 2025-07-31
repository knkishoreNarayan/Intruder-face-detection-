from flask import Flask, render_template, Response, jsonify, request
from flask_cors import CORS
import cv2
import os
import threading
import time
import base64
from io import BytesIO
from PIL import Image
import numpy as np
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Define paths
HAAR_CASCADE_PATH = r'C:/Users/kisho/OneDrive/Desktop/face/haarcascade_frontalface_default.xml'
MODEL_PATH = r'C:\Users\kisho\OneDrive\Desktop\face\Kishore_model.yml'
INTRUDER_IMAGE_PATH = r'C:\Users\kisho\OneDrive\Desktop\face\intruder.jpg'

# Global variables
camera = None
face_classifier = None
Kishore_model = None
camera_active = False
current_status = "No Face Detected"
current_confidence = 0
camera_error = None
last_intruder_time = None
intruder_count = 0
continuous_monitoring = False

def initialize_models():
    global face_classifier, Kishore_model
    # Load HAAR face classifier
    face_classifier = cv2.CascadeClassifier(HAAR_CASCADE_PATH)
    
    # Load pre-trained model
    if os.path.exists(MODEL_PATH):
        Kishore_model = cv2.face.LBPHFaceRecognizer_create()
        Kishore_model.read(MODEL_PATH)
    else:
        raise FileNotFoundError("Trained model not found. Please train the model first.")

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

def find_working_camera():
    """Try different camera indices to find a working camera"""
    for i in range(4):  # Try camera indices 0-3
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                cap.release()
                print(f"Found working camera at index {i}")
                return i
            cap.release()
    return None

def continuous_monitoring_thread():
    """Continuous CCTV-style monitoring thread"""
    global camera, camera_active, current_status, current_confidence, camera_error, last_intruder_time, intruder_count
    
    # Try to find a working camera
    camera_index = find_working_camera()
    if camera_index is None:
        camera_error = "No camera found. Please check your webcam connection."
        print("Error: No working camera found.")
        return
    
    camera = cv2.VideoCapture(camera_index)
    if not camera.isOpened():
        camera_error = "Unable to access the webcam. Please check permissions."
        print("Error: Unable to access the webcam.")
        return
    
    print(f"Camera opened successfully at index {camera_index}")
    camera_error = None
    camera_active = True
    
    while camera_active:
        ret, frame = camera.read()
        if not ret:
            print("Error: Unable to read from webcam.")
            camera_error = "Unable to read from webcam."
            break

        image, face = face_detector(frame)
        try:
            if face is not None:
                result = Kishore_model.predict(face)
                confidence = int(100 * (1 - (result[1]) / 400))
                current_confidence = confidence

                if confidence > 85:  # Verified User
                    current_status = "Verified User"
                    cv2.putText(image, "Verified User", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                    # Reset intruder count for verified users
                    intruder_count = 0
                else:  # Intruder Alert
                    current_status = "Intruder Detected"
                    cv2.putText(image, "INTRUDER ALERT!", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                    
                    # Save intruder image with timestamp
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    intruder_filename = f"intruder_{timestamp}.jpg"
                    intruder_path = os.path.join(os.path.dirname(INTRUDER_IMAGE_PATH), intruder_filename)
                    cv2.imwrite(intruder_path, frame)
                    
                    # Update intruder tracking
                    last_intruder_time = datetime.now()
                    intruder_count += 1
                    
                    print(f"🚨 INTRUDER DETECTED! Confidence: {confidence}% - Saved: {intruder_filename}")
            else:
                current_status = "No Face Detected"
                current_confidence = 0
                cv2.putText(frame, "Monitoring...", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 2)

        except Exception as e:
            print(f"Error during detection: {str(e)}")
            current_status = "Detection Error"
            current_confidence = 0

        time.sleep(0.1)  # Small delay to prevent excessive CPU usage

    if camera:
        camera.release()
        print("Camera released")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_monitoring')
def start_monitoring():
    global camera_active, continuous_monitoring, camera_error
    if not camera_active:
        camera_active = True
        continuous_monitoring = True
        camera_error = None
        thread = threading.Thread(target=continuous_monitoring_thread)
        thread.daemon = True
        thread.start()
        return jsonify({"status": "success", "message": "Continuous monitoring started"})
    return jsonify({"status": "error", "message": "Monitoring already active"})

@app.route('/stop_monitoring')
def stop_monitoring():
    global camera_active, continuous_monitoring, camera
    camera_active = False
    continuous_monitoring = False
    if camera:
        camera.release()
    return jsonify({"status": "success", "message": "Monitoring stopped"})

@app.route('/get_status')
def get_status():
    return jsonify({
        "status": current_status,
        "confidence": current_confidence,
        "camera_active": camera_active,
        "camera_error": camera_error,
        "last_intruder_time": last_intruder_time.isoformat() if last_intruder_time else None,
        "intruder_count": intruder_count,
        "continuous_monitoring": continuous_monitoring
    })

@app.route('/capture_frame')
def capture_frame():
    global camera, camera_error
    if camera and camera.isOpened():
        ret, frame = camera.read()
        if ret:
            # Convert frame to base64
            _, buffer = cv2.imencode('.jpg', frame)
            frame_base64 = base64.b64encode(buffer).decode('utf-8')
            return jsonify({
                "status": "success",
                "frame": frame_base64,
                "detection_status": current_status,
                "confidence": current_confidence
            })
    return jsonify({"status": "error", "message": camera_error or "Camera not available"})

@app.route('/test_camera')
def test_camera():
    """Test endpoint to check camera availability"""
    camera_index = find_working_camera()
    if camera_index is not None:
        return jsonify({"status": "success", "message": f"Camera found at index {camera_index}"})
    else:
        return jsonify({"status": "error", "message": "No camera found"})

@app.route('/get_intruder_stats')
def get_intruder_stats():
    """Get intruder detection statistics"""
    return jsonify({
        "intruder_count": intruder_count,
        "last_intruder_time": last_intruder_time.isoformat() if last_intruder_time else None,
        "monitoring_active": camera_active
    })

if __name__ == '__main__':
    try:
        initialize_models()
        print("Models initialized successfully")
        print("Starting continuous CCTV monitoring system...")
    except Exception as e:
        print(f"Error initializing models: {e}")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 