from moviepy import VideoFileClip
import os
from config import VIDEO_PATH

# I/O
input_path = VIDEO_PATH
base, ext = os.path.splitext(input_path)
output_path = f"{base}_TRIMMED{ext}"

# Times (seconds)
START_TIME = 0
END_TIME = 85
with VideoFileClip(input_path) as clip:
    end_time = min(END_TIME, clip.duration)
    trimmed = clip.subclipped(START_TIME, end_time)  # v2.x name
    trimmed.write_videofile(
        output_path,
        codec="libx264",
        audio=False,     # drop audio to save size
        fps=clip.fps     # keep original fps
    )

print(f"Trimmed video saved to: {output_path}")
