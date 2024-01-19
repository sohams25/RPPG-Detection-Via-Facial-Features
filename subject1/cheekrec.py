import cv2
import dlib
from moviepy.editor import VideoFileClip, ImageSequenceClip

# Load the pre-trained face detector from dlib
detector = dlib.get_frontal_face_detector()

# File to store bounding box coordinates
output_file_path = 'boundingBoxesCoordinates.txt'  # Replace with the desired file path

# Open the video file
video_path = 'Videos/vid.avi'  # Enter the video file path
video_clip = VideoFileClip(video_path)

# Open the output file for writing
with open(output_file_path, 'w') as output_file:
    # Process each frame of the video and save the frames with bounding boxes
    frames_with_boxes = []
    for frame_num, frame in enumerate(video_clip.iter_frames(fps=video_clip.fps)):
        # Convert the frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale frame
        faces = detector(gray)

        for face_num, face in enumerate(faces):
            x, y, w, h = face.left(), face.top(), face.width(), face.height()

            left_cheek = frame[y + h//2:y + h, x:x + w//2]
            right_cheek = frame[y + h//2:y + h, x + w//2:x + w]

            # Write bounding box coordinates to the output file
            output_file.write(f"Frame {frame_num + 1}, Face {face_num + 1}, Left Cheek: ({x}, {y + h//2}), ({x + w//2}, {y + h}), "
                              f"Right Cheek: ({x + w//2}, {y + h//2}), ({x + w}, {y + h})\n")

            # Draw bounding boxes around cheeks on the frame
            cv2.rectangle(frame, (x, y + h//2), (x + w//2, y + h), (0, 255, 0), 2)  # Left cheek
            cv2.rectangle(frame, (x + w//2, y + h//2), (x + w, y + h), (0, 255, 0), 2)  # Right cheek

        frames_with_boxes.append(frame)

# Create a new video clip from the processed frames
output_clip = ImageSequenceClip(frames_with_boxes, fps=video_clip.fps)

# Save the output video with bounding boxes
output_video_path = 'Videos/output_with_boxes.mp4'  # Replace with the desired output video path
output_clip.write_videofile(output_video_path, codec='libx264', audio=False)

# Release resources
cv2.destroyAllWindows()
