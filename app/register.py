import cv2
import os

# Path where datasets will be saved
DATASET_DIR = "../dataset"

def register_user(user_name, num_images=20):
    # Create a folder for the user if not exists
    user_folder = os.path.join(DATASET_DIR, user_name)
    os.makedirs(user_folder, exist_ok=True)

    # Initialize webcam
    cap = cv2.VideoCapture(0)
    count = 0

    print(f"[INFO] Capturing images for {user_name}. Press 'q' to quit early.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Register User", frame)

        # Save every nth frame until required number of images
        if count < num_images:
            img_path = os.path.join(user_folder, f"{count+1}.jpg")
            cv2.imwrite(img_path, frame)
            print(f"[INFO] Saved {img_path}")
            count += 1

        # Exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q') or count >= num_images:
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"[INFO] Finished capturing {count} images for {user_name} ✅")

if __name__ == "__main__":
    name = input("Enter the name of the person to register: ")
    register_user(name)
