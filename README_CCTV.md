# 🎥 CCTV Security System

A continuous monitoring CCTV system with intelligent intruder detection and real-time alerts.

## 🚀 **Features**

### **Continuous Monitoring**
- ✅ **24/7 Camera Feed** - Always-on surveillance like real CCTV
- ✅ **Intelligent Detection** - Automatically identifies verified users vs intruders
- ✅ **Real-time Alerts** - Instant notifications when intruders are detected
- ✅ **Intruder Tracking** - Counts and timestamps all intruder detections
- ✅ **Image Capture** - Automatically saves intruder images with timestamps

### **Security Features**
- 🔒 **Face Recognition** - Identifies verified users with high confidence
- 🚨 **Intruder Alerts** - Immediate detection and alerting
- 📸 **Evidence Collection** - Saves intruder images for investigation
- 📊 **Statistics Dashboard** - Real-time monitoring statistics
- 📝 **System Logs** - Complete audit trail of all events

### **User Interface**
- 🎨 **Modern Dashboard** - Beautiful, responsive web interface
- 📱 **Mobile Responsive** - Works on all devices
- 🔄 **Real-time Updates** - Live status and video feed
- 📈 **Statistics Panel** - Intruder count and timing information

## 🛠️ **Installation**

### **1. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2. Update File Paths**
Edit `app.py` and update these paths to match your system:
```python
HAAR_CASCADE_PATH = r'C:/Users/kisho/OneDrive/Desktop/face/haarcascade_frontalface_default.xml'
MODEL_PATH = r'C:\Users\kisho\OneDrive\Desktop\face\Kishore_model.yml'
INTRUDER_IMAGE_PATH = r'C:\Users\kisho\OneDrive\Desktop\face\intruder.jpg'
```

## 🎯 **Quick Start**

### **Method 1: Manual Start**
```bash
# Start the CCTV system
python app.py

# Open in browser
http://localhost:5000

# Click "Start Monitoring" to begin surveillance
```

### **Method 2: Auto-Start (Recommended)**
```bash
# Install requests if not already installed
pip install requests

# Run auto-start script
python start_cctv.py
```

## 📊 **How It Works**

### **Continuous Monitoring Mode**
1. **Camera Always On** - Camera runs continuously like real CCTV
2. **Background Processing** - Face detection runs in background
3. **Silent Monitoring** - No alerts until intruder detected
4. **Instant Alerts** - Immediate notification when intruder found
5. **Evidence Collection** - Automatically saves intruder images

### **Detection Logic**
- **Verified User** (Confidence > 85%): Green status, no alert
- **Intruder** (Confidence ≤ 85%): Red alert, image saved
- **No Face**: Yellow monitoring status

### **Intruder Response**
- 🚨 **Immediate Alert** - Visual and system notification
- 📸 **Image Capture** - Saves timestamped image
- 📊 **Statistics Update** - Increments intruder count
- 📝 **Log Entry** - Records event in system logs

## 🎛️ **Controls**

### **Web Interface**
- **Start Monitoring** - Begin continuous CCTV surveillance
- **Stop Monitoring** - Stop the surveillance system
- **Test Camera** - Check camera availability
- **Live Feed** - Real-time video stream
- **Statistics** - View intruder count and timing

### **System Status**
- **🟢 Active** - CCTV monitoring is running
- **🔴 Inactive** - System is stopped
- **🟡 Error** - Camera or system issue

## 📈 **Statistics Dashboard**

### **Real-time Metrics**
- **Total Intruders** - Count of detected intruders
- **Last Alert** - Timestamp of most recent intruder
- **Monitoring Status** - Current system state
- **Confidence Level** - Detection accuracy percentage

### **System Logs**
- Camera start/stop events
- Intruder detection alerts
- System errors and warnings
- Timestamped activity log

## 🔧 **Troubleshooting**

### **Camera Issues**
```bash
# Test camera directly
python test_camera.py

# Check camera permissions
# Windows: Settings → Privacy & Security → Camera
```

### **Common Problems**
1. **Camera not found** - Check connections and drivers
2. **Permission denied** - Allow camera access in settings
3. **Model not found** - Verify file paths in app.py
4. **Server not responding** - Check if app.py is running

### **Performance Tips**
- Close other camera applications
- Ensure good lighting
- Use USB webcam for better performance
- Check system resources

## 📁 **File Structure**

```
intrudeFaceDetection/
├── app.py                 # Main CCTV application
├── start_cctv.py         # Auto-start script
├── test_camera.py        # Camera testing utility
├── Detect.py             # Original face detection
├── requirements.txt      # Python dependencies
├── README_CCTV.md       # This file
├── TROUBLESHOOTING.md   # Detailed troubleshooting
└── templates/
    └── index.html       # CCTV web interface
```

## 🔒 **Security Features**

### **Intruder Detection**
- **Automatic Recognition** - Identifies unknown faces
- **Confidence Scoring** - Measures detection accuracy
- **Image Evidence** - Saves intruder photos
- **Timestamp Logging** - Records exact detection time

### **System Monitoring**
- **Real-time Status** - Live system health monitoring
- **Error Detection** - Automatic issue identification
- **Logging** - Complete audit trail
- **Statistics** - Performance metrics

## 🎯 **Use Cases**

### **Home Security**
- Monitor entry points
- Detect unauthorized access
- Collect evidence for incidents
- Track visitor patterns

### **Office Security**
- Monitor building access
- Track employee attendance
- Detect unauthorized personnel
- Maintain security logs

### **Surveillance**
- Continuous area monitoring
- Intruder detection
- Evidence collection
- Remote monitoring

## 🚀 **Advanced Features**

### **Auto-Start Script**
```bash
python start_cctv.py
```
- Automatically starts monitoring
- Tests camera before starting
- Provides status updates
- Graceful shutdown handling

### **Statistics API**
```bash
# Get intruder statistics
GET /get_intruder_stats

# Get system status
GET /get_status

# Test camera
GET /test_camera
```

## 📞 **Support**

### **Getting Help**
1. Check the troubleshooting guide
2. Run camera test script
3. Verify file paths
4. Check system requirements

### **System Requirements**
- Python 3.7+
- Working webcam
- Trained face recognition model
- Sufficient system resources

## 🔄 **Updates & Maintenance**

### **Regular Maintenance**
- Check camera connections
- Verify model files
- Monitor system logs
- Update dependencies

### **Performance Optimization**
- Close unnecessary applications
- Ensure good lighting
- Use dedicated camera
- Monitor system resources

---

**🎯 Ready to deploy your CCTV security system!**

Start with: `python start_cctv.py` 