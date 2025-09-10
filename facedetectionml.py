import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
import numpy as np


class FaceDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Detection App")

        self.label = tk.Label(root)
        self.label.pack(pady=10)

        self.webcam_button = tk.Button(
            root, text="Use Webcam", command=self.use_webcam)
        self.webcam_button.pack(pady=5)

        self.upload_button = tk.Button(
            root, text="Upload Photo", command=self.upload_photo)
        self.upload_button.pack(pady=5)

        self.stop_button = tk.Button(
            root, text="Stop Webcam", command=self.stop_webcam, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        self.capture = None
        self.is_webcam_running = False

    def use_webcam(self):
        if not self.is_webcam_running:
            self.is_webcam_running = True
            self.capture = cv2.VideoCapture(1)

            self.stop_button.config(state=tk.NORMAL)
            self.show_webcam()

    def stop_webcam(self):
        if self.is_webcam_running:
            self.is_webcam_running = False
            if self.capture:
                self.capture.release()
            self.label.config(image=None)

            self.stop_button.config(state=tk.DISABLED)

    def upload_photo(self):
        self.stop_webcam()
        file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[
                                               ("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.show_uploaded_photo(file_path)

    def show_webcam(self):
        if self.is_webcam_running:
            ret, frame = self.capture.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                faces = self.detect_faces_haar(frame)

                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

                image = Image.fromarray(frame)
                photo = ImageTk.PhotoImage(image=image)

                self.label.config(image=photo)
                self.label.image = photo

                self.root.after(10, self.show_webcam)
            else:
                self.is_webcam_running = False
                self.capture.release()

    def show_uploaded_photo(self, file_path):

        self.stop_button.config(state=tk.DISABLED)

        image = Image.open(file_path)
        image = image.resize((400, 300), resample=Image.LANCZOS)

        image_np = np.array(image)

        image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        faces = self.detect_faces_haar(image_np)

        draw = ImageDraw.Draw(image)

        for (x, y, w, h) in faces:
            draw.rectangle([x, y, x+w, y+h], outline="blue", width=2)

        photo = ImageTk.PhotoImage(image=image)

        self.label.config(image=photo)
        self.label.image = photo

    def detect_faces_haar(self, image):
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
        return faces


if __name__ == "__main__":
    root = tk.Tk()
    app = FaceDetectionApp(root)
    root.mainloop()
