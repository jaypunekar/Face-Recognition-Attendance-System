from flask import Blueprint, Response, render_template, request
import cv2
import face_recognition
import numpy as np
import os
from datetime import datetime
from database.sqlite_operations import save_attendance
from pathlib import Path

# Create blueprint for video stream
video_stream_bp = Blueprint('video_stream_bp', __name__)

# Initialize video capture and known faces list
#video_capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
known_face_encodings = []
known_face_names = []
detected_faces = {}  

detected : bool = 0

# Directory paths
Images_dir = os.path.join(os.getcwd(), 'Images')
unknownFaces_dir = os.path.join(os.getcwd(), 'unknownFaces')

# Load known faces from the 'Images' folder
def load_Images():
    global known_face_encodings, known_face_names
    known_face_encodings = []
    known_face_names = []

    # Ensure the 'unknownFaces' directory exists
    if not os.path.exists(unknownFaces_dir):
        os.makedirs(unknownFaces_dir)

    for filename in os.listdir(Images_dir):
        if filename.endswith(".jpg") or filename.endswith(".jpeg"):
            image = face_recognition.load_image_file(os.path.join(Images_dir, filename))
            encoding = face_recognition.face_encodings(image)
            if encoding:
                known_face_encodings.append(encoding[0])
                known_face_names.append(filename.split('.')[0])  # Use filename (without extension) as name
load_Images()

# Function to generate video frames with face recognition
def gen_frames():
    video_capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    global detected_faces
    # Set desired width and height for the webcam capture (medium size)
    width = 800   # Medium width (you can adjust this if needed)
    height = 600  # Medium height (you can adjust this as well)

    # Set the resolution for the webcam capture
    video_capture.set(3, 1280)  # Set width
    video_capture.set(4, 720)  # Set height

    while True:
        ret, frame = video_capture.read(0)

        if not ret:
            break

        # Optionally, you can resize the frame here if needed
        frame = cv2.resize(frame, (width, height))

        # Face recognition logic here...
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)
        face_names = []

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, )
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

        # Draw rectangles and labels on faces
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            current_time = datetime.now()

            if name == 'Unknown':
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                accuracy = int(100 - (min(face_distances) * 100))
                cv2.putText(frame, f"{name}, {accuracy}%", (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            else:
                if name not in detected_faces:
                    save_attendance(name, current_time.strftime("%Y-%m-%d %H:%M:%S"))
                    detected_faces[name] = current_time  # Store the timestamp
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                accuracy = int(100 - (min(face_distances) * 100))
                detected = 1
                cv2.putText(frame, f"{name}, {accuracy}%", (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Convert the frame to JPEG for streaming
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


# Route to handle video feed
@video_stream_bp.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Route to register unknown faces
@video_stream_bp.route('/register-unknown-face', methods=['GET', 'POST'])
def register_unknown_face():
    if request.method == 'POST':
        student_name = request.form['name']

        # Capture an unknown face image from the webcam
        image_path = os.path.join(unknownFaces_dir, f"{student_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")

        # Capture the image from webcam and save it
        video_capture = cv2.VideoCapture(0)
        ret, frame = video_capture.read()
        if ret:
            cv2.imwrite(image_path, frame)

        video_capture.release()

        # Load and encode the new face
        image = face_recognition.load_image_file(image_path)
        #encoding = face_recognition.face_encodings(image)
        encodings = face_recognition.face_encodings(image)
        if not encodings:
            return render_template('register_new.html', message="No face detected. Please try again.")


        # Add the new face encoding to the known faces list
        known_face_encodings.append(encodings)
        known_face_names.append(student_name)

        # Save attendance to the database
        save_attendance(student_name, datetime.now())

        return render_template('register_new.html', message="Unknown face registered successfully!")

    return render_template('register_new.html')
