import cv2
import dlib
from moviepy.editor import VideoFileClip, ImageSequenceClip

detector = dlib.get_frontal_face_detector()

# File to store green channel information
green_channel_file_path = '/Users/soham/Desktop/Grand Finale/DOP(Amalin Sir)/Subject 1/Green Channel Information/greenChannelInformation.txt'  

video_path = '/Users/soham/Desktop/Grand Finale/DOP(Amalin Sir)/Subject 1/Videos/vid.avi'  # Enter the video file path
video_clip = VideoFileClip(video_path)

# Open the output file for writing
with open(green_channel_file_path, 'w') as green_channel_file:
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

            green_left_cheek = left_cheek[:, :, 1]  # Green channel is at index 1
            green_right_cheek = right_cheek[:, :, 1]

            green_channel_file.write(f"Frame {frame_num + 1}, Green Left Cheek: {green_left_cheek.mean()}, "
                                     f"Green Right Cheek: {green_right_cheek.mean()}\n")

            cv2.rectangle(frame, (x, y + h//2), (x + w//2, y + h), (0, 255, 0), 2)  # Left cheek
            cv2.rectangle(frame, (x + w//2, y + h//2), (x + w, y + h), (0, 255, 0), 2)  # Right cheek

        frames_with_boxes.append(frame)

output_clip = ImageSequenceClip(frames_with_boxes, fps=video_clip.fps)

output_video_path = '/Users/soham/Desktop/Grand Finale/DOP(Amalin Sir)/Subject 1/Videos/output_with_boxes_and_green_info.mp4'  # Replace with the desired output video path
output_clip.write_videofile(output_video_path, codec='libx264', audio=False)

cv2.destroyAllWindows()
