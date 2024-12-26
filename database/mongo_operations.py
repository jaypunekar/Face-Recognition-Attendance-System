from pymongo import MongoClient

class MongoOperations:
    def __init__(self, uri="your_mongodb_atlas_uri", db_name="attendance_system"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def insert_user(self, name, roll_number, image_path, face_encoding):
        """Insert a new user into MongoDB."""
        self.db.users.insert_one({
            "name": name,
            "roll_number": roll_number,
            "image_path": image_path,
            "face_encoding": face_encoding
        })

    def fetch_user_by_encoding(self, encoding):
        """Fetch user data by face encoding (pseudo example)."""
        # Implement a similarity matching logic for the encoding
        user = self.db.users.find_one({"face_encoding": encoding})
        return user

    def fetch_all_users(self):
        """Fetch all users."""
        return list(self.db.users.find())