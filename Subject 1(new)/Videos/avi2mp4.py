import cv2

# Input and output video paths
input_video_path = "/Users/soham/Desktop/Grand Finale/DOP(Amalin Sir)/Subject 1/Videos/vid.avi"
output_video_path = "/Users/soham/Desktop/Grand Finale/DOP(Amalin Sir)/Subject 1/Videos/vid.mp4"

# Open the input video file
cap = cv2.VideoCapture(input_video_path)

# Get video properties
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Create VideoWriter object for MP4 output
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

# Read frames from the input video and write to the output video
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Write the frame to the output video
    out.write(frame)

# Release video capture and writer objects
cap.release()
out.release()

print("Conversion from AVI to MP4 completed successfully.")
