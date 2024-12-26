from flask import Flask, render_template, request
from database.sqlite_operations import fetch_all_attendance, save_attendance
from video_stream import video_stream_bp  # Import the video stream blueprint
import face_recognition
import os
from datetime import datetime
import numpy as np

# Create the Flask app instance
app = Flask(__name__)

# Register the video stream blueprint
app.register_blueprint(video_stream_bp)

# Define the directory for images of registered faces
Images_dir = os.path.join(os.getcwd(), 'Images')
unknownFaces_dir = os.path.join(os.getcwd(), 'unknownFaces')  # Directory for saving new faces

# Load known faces and names
known_face_encodings = []
known_face_names = []

def load_Images():
    global known_face_encodings, known_face_names
    known_face_encodings = []
    known_face_names = []

    for filename in os.listdir(Images_dir):
        if filename.endswith(".jpg") or filename.endswith(".jpeg"):
            image = face_recognition.load_image_file(os.path.join(Images_dir, filename))
            encoding = face_recognition.face_encodings(image)
            if encoding:
                known_face_encodings.append(encoding[0])
                known_face_names.append(filename.split('.')[0])  # Use filename (without extension) as name

load_Images()  # Load known faces when the app starts

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/video-stream', methods=['GET'])
def video_stream():
    return render_template('video_player.html')

@app.route('/attendance', methods=['GET'])
def attendance():
    attendance_records = fetch_all_attendance()
    return render_template("attendance.html", attendance=attendance_records)

# Add the missing register_student route
@app.route('/register-student', methods=['GET', 'POST'])
def register_student():
    if request.method == 'POST':
        student_name = request.form['name']
        image_file = request.files['image']
        image_path = os.path.join(Images_dir, f"{student_name}.jpg")

        # Save image to the 'Images' folder
        image_file.save(image_path)

        # Load and encode the new face
        image = face_recognition.load_image_file(image_path)
        encoding = face_recognition.face_encodings(image)

        # Save face encoding and name for future recognition
        known_face_encodings.append(encoding)
        known_face_names.append(student_name)

        # Optionally, save attendance to the database
        save_attendance(student_name, datetime.now())

        return render_template('register_new.html', message="Student registered successfully!")

    return render_template('register_new.html')

#newadd-20.12.2024
@app.route('/mark-attendance', methods=['GET', 'POST'])
def mark_attendance():
    if request.method == 'POST':
        # Get the uploaded photo
        uploaded_file = request.files['photo']
        
        # Ensure the photo is saved temporarily for processing
        temp_file_path = os.path.join(os.getcwd(), 'temp.jpg')
        uploaded_file.save(temp_file_path)

        # Load the uploaded photo and encode the face
        image = face_recognition.load_image_file(temp_file_path)
        encodings = face_recognition.face_encodings(image)

        if not encodings:
            return render_template('mark_attendance.html', message="No face detected. Please try again.")

        # Compare the uploaded face with known faces
        face_encoding = encodings[0]
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        if matches and len(face_distances) > 0:
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

        # Mark attendance if the person is recognized
        if name != "Unknown":
            save_attendance(name, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            message = f"Attendance marked for {name}."
        else:
            message = "Face not recognized. Please register first."

        # Remove the temporary file
        os.remove(temp_file_path)

        return render_template('mark_attendance.html', message=message)

    return render_template('mark_attendance.html')


if __name__ == '__main__':
    app.run(debug=True)
