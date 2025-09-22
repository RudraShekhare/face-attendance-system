import os
import cv2
import face_recognition
import pickle

# Paths
DATASET_DIR = "../dataset"
ENCODINGS_PATH = "../models/encodings.pkl"

def encode_faces():
    known_encodings = []
    known_names = []

    # Loop over each person in the dataset
    for person_name in os.listdir(DATASET_DIR):
        person_dir = os.path.join(DATASET_DIR, person_name)
        if not os.path.isdir(person_dir):
            continue

        print(f"[INFO] Processing images for {person_name}...")

        # Loop over each image of the person
        for image_name in os.listdir(person_dir):
            image_path = os.path.join(person_dir, image_name)

            # Load image
            image = cv2.imread(image_path)
            if image is None:
                print(f"[WARNING] Could not read {image_path}")
                continue

            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Detect face locations
            boxes = face_recognition.face_locations(rgb, model="hog")  # use "cnn" if GPU
            encodings = face_recognition.face_encodings(rgb, boxes)

            for encoding in encodings:
                known_encodings.append(encoding)
                known_names.append(person_name)

    # Save encodings and names to pickle file
    print(f"[INFO] Saving encodings to {ENCODINGS_PATH}...")
    data = {"encodings": known_encodings, "names": known_names}

    with open(ENCODINGS_PATH, "wb") as f:
        pickle.dump(data, f)

    print("[INFO] Encoding complete ✅")

if __name__ == "__main__":
    encode_faces()
