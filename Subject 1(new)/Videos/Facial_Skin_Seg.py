import cv2
import numpy as np

input_video_path = "/Users/soham/Desktop/Grand Finale/DOP(Amalin Sir)/Subject 1/Videos/vid.mp4"
output_video_path = "/Users/soham/Desktop/Grand Finale/DOP(Amalin Sir)/Subject 1/Videos/video_face_skin_segmented_fixed_bounding_box.mp4"

cap = cv2.VideoCapture(input_video_path)

fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Video writer with mp4 format
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

# HaarCascade Detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Color range to HSV
lower_skin = np.array([0, 20, 70], dtype=np.uint8)
upper_skin = np.array([20, 255, 255], dtype=np.uint8)

# Extension of Bounding Box to static
ret, first_frame = cap.read()
gray_first_frame = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray_first_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
if len(faces) > 0:
    (x, y, w, h) = faces[0]
    x = max(0, x - int(0.3 * w))
    y = max(0, y - int(0.3 * h))
    w = min(width - x, int(1.6 * w))
    h = min(height - y, int(1.6 * h))
    face_mask = np.zeros_like(gray_first_frame)
    cv2.rectangle(face_mask, (x, y), (x+w, y+h), (255, 255, 255), thickness=cv2.FILLED)

# Video processing loop
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv_frame, lower_skin, upper_skin)

    # Thresholding
    _, thresholded = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Morpholgical Operations
    kernel = np.ones((5, 5), np.uint8)
    thresholded = cv2.morphologyEx(thresholded, cv2.MORPH_CLOSE, kernel)
    thresholded = cv2.morphologyEx(thresholded, cv2.MORPH_OPEN, kernel)

    # Static bounding box application
    thresholded = cv2.bitwise_and(thresholded, face_mask)

    # Contour-based filtering
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 1000]

    contour_mask = np.zeros_like(thresholded)
    cv2.drawContours(contour_mask, filtered_contours, -1, (255, 255, 255), thickness=cv2.FILLED)

    # Combining contour op with original
    result_frame = cv2.bitwise_and(frame, frame, mask=contour_mask)

    out.write(result_frame)

cap.release()
out.release()

print("Face-focused skin segmentation (fixed bounding box) video created and saved in MP4 format successfully.")
