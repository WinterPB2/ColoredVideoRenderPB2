import cv2

PLAYER_NAME = "Winter Blood" # Change if needed
VIDEO_PATH = "amv_TRIMMED_TRIMMED.mp4"  # Change if needed

# === Read source video info ===
cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    raise RuntimeError(f"Cannot open video: {VIDEO_PATH}")

SOURCE_WIDTH  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
SOURCE_HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
SOURCE_FPS    = cap.get(cv2.CAP_PROP_FPS) or 30.0
cap.release()

# === Pixel grid parameters ===
# screen size controls overall downscale factor (bigger = more pixels)
SCREEN_SIZE = 11
PIXEL_SIZE  = 8

# keep the same aspect ratio but scaled by SCREEN_SIZE
ASPECT_RATIO_WIDTH  = int(SOURCE_WIDTH  / (SOURCE_HEIGHT / (3 * SCREEN_SIZE)))
ASPECT_RATIO_HEIGHT = 3 * SCREEN_SIZE

# match video fps
#FRAME_RATE = int(round(SOURCE_FPS))
FRAME_RATE = 15

# ====== 16-Color Anime / Cartoon Palette ======
PALETTE = [
    # ---- linework / shading ----
    "000000",  # 0 pure black (line art)
    "2B2B2B",  # 1 dark gray (deep shadow)
    "6B6B6B",  # 2 mid shadow / screen tone
    "E0E0E0",  # 3 light gray highlight

    # ---- skin & warm tones ----
    "8E3A20",  # 4 dark skin / shadow brown
    "D67B52",  # 5 mid skin
    "FFD6A5",  # 6 light skin / blush

    # ---- sky & water ----
    "1C3FAA",  # 7 deep blue sky / ocean shadow
    "3E8BFF",  # 8 bright sky blue
    "A6D8FF",  # 9 light sky / reflection

    # ---- vegetation & nature ----
    "285C2A",  # 10 deep green
    "54A24B",  # 11 mid green
    "A6E27C",  # 12 highlight green

    # ---- effects / accents ----
    "F5C211",  # 13 gold / light magic / glow
    "E03C31",  # 14 red / eyes / fire
    "C13CAD",  # 15 purple / night / neon
]
