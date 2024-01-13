import cv2
import dlib
from moviepy.editor import VideoFileClip, VideoClip
from moviepy.editor import ImageSequenceClip

# Load the pre-trained face detector from dlib
detector = dlib.get_frontal_face_detector()

# Function to detect cheeks in a frame and draw bounding boxes
def detect_cheeks_with_boxes(frame):
    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    faces = detector(gray)

    for face in faces:
        x, y, w, h = face.left(), face.top(), face.width(), face.height()

        left_cheek = frame[y + h//2:y + h, x:x + w//2]
        right_cheek = frame[y + h//2:y + h, x + w//2:x + w]

        # Draw bounding boxes around cheeks
        cv2.rectangle(frame, (x, y + h//2), (x + w//2, y + h), (0, 255, 0), 2)  # Left cheek
        cv2.rectangle(frame, (x + w//2, y + h//2), (x + w, y + h), (0, 255, 0), 2)  # Right cheek

    return frame

# Open the video file
video_path = '' #Enter the video file path
video_clip = VideoFileClip(video_path)

# Process each frame of the video and save the frames with bounding boxes
frames_with_boxes = [detect_cheeks_with_boxes(frame) for frame in video_clip.iter_frames(fps=video_clip.fps)]

# Create a new video clip from the processed frames
output_clip = ImageSequenceClip(frames_with_boxes, fps=video_clip.fps)

# Save the output video with bounding boxes
output_path = 'output_with_boxes.mp4'
output_clip.write_videofile(output_path, codec='libx264', audio=False)

# Release resources
cv2.destroyAllWindows()