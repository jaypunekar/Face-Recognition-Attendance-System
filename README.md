# **Face Recognition Attendance System**

A real-time **Face Recognition Attendance System** built as a web application using Flask, Python, SQLite, and OpenCV. This project automates the attendance process by detecting and recognizing faces through a live webcam feed and logging attendance records into an SQLite database. Users can register via a web interface by uploading their profile images.

---

## **Features**
- **Web-Based User Registration**:  
  A Flask-powered web interface allows users to register their names and upload profile images.

- **Real-Time Face Recognition**:  
  Detects and recognizes faces in real-time using the **Face Recognition** library via a webcam feed.

- **Attendance Logging**:  
  Automatically logs attendance with the user’s name, timestamp, and recognition accuracy into an **SQLite database**.

- **Local Image Storage**:  
  Profile images are saved locally for face recognition and validation.

- **Dynamic Bounding Box**:  
  Displays bounding boxes around detected faces:
  - Green for recognized faces (visible for 5 seconds).
  - Red for unrecognized faces.

---

## **Technologies Used**
- **Programming Language**: Python
- **Framework**: Flask
- **Database**: SQLite
- **Libraries**:
  - `face_recognition` for face detection and recognition.
  - `sqlite3` for database management.
  - `OpenCV (cv2)` for video feed and bounding box visualization.

---

## **Setup Instructions**

### Prerequisites:
- Python 3.x installed.
- SQLite (pre-installed with Python).

### Steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repository-name.git
   cd your-repository-name
   ```
2. **Install all requirements**
  ```bash
  pip install -r requirements.txt
  ```
3. **Run the Application Locally**
   ```bash
   python app.py
   ```

Feel free to reach out for any questions or suggestions. Happy coding!
