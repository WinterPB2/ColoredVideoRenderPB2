# create_frames.py
import os
import cv2
import numpy as np
import config

FRAMES_DIR = "frames"
CATEG_DIR = "pixel_categorized_frames"

# ---------- helpers ----------
def hex_to_bgr(hexstr: str) -> np.ndarray:
    r = int(hexstr[0:2], 16)
    g = int(hexstr[2:4], 16)
    b = int(hexstr[4:6], 16)
    return np.array([b, g, r], dtype=np.uint8)

# build palette arrays once (BGR -> Lab) — SAFE VERSION
PALETTE_BGR = np.stack([hex_to_bgr(h) for h in config.PALETTE], axis=0).astype(np.uint8)  # (K,3)
palette_lab = []
for bgr in PALETTE_BGR:
    lab = cv2.cvtColor(bgr.reshape(1, 1, 3), cv2.COLOR_BGR2Lab)[0, 0]
    palette_lab.append(lab)
palette_lab = np.array(palette_lab, dtype=np.float32)  # (K,3)
K = len(config.PALETTE)

# favor chroma slightly over lightness, but stay subtle
W_L, W_A, W_B = 0.8, 1.15, 1.15

def quantize_frame_to_palette_idxs(img_bgr: np.ndarray) -> np.ndarray:
    lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2Lab).astype(np.float32)   # (H,W,3)
    H, W, _ = lab.shape
    lab_flat = lab.reshape(-1, 3)                                       # (N,3)

    # palette_lab is already float32 from your code
    diffs = lab_flat[:, None, :] - palette_lab[None, :, :]              # (N,K,3)
    d2 = (W_L * diffs[:, :, 0]**2) + (W_A * diffs[:, :, 1]**2) + (W_B * diffs[:, :, 2]**2)
    idx = np.argmin(d2, axis=1).astype(np.uint8)
    return idx.reshape(H, W)

# Optional: tiny ordered dithering on L* to reduce banding
USE_DITHER = False
BAYER_4x4 = (1/17.0) * np.array([
    [ 0,  8,  2, 10],
    [12,  4, 14,  6],
    [ 3, 11,  1,  9],
    [15,  7, 13,  5],
], dtype=np.float32)

def dither_L_before_quantization(img_bgr):
    lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2Lab).astype(np.float32)
    H, W, _ = lab.shape
    tile = np.tile(BAYER_4x4, (H//4 + 1, W//4 + 1))[:H, :W]
    lab[..., 0] = np.clip(lab[..., 0] + 2.0 * (tile - 0.5), 0, 100)  # ±1 L*
    return cv2.cvtColor(lab.astype(np.float32), cv2.COLOR_Lab2BGR).astype(np.uint8)

# Optional: boost saturation to fight grayscale bias
USE_SAT_BOOST = False
SAT_AMOUNT = 1.3

def boost_saturation(img_bgr, amount=1.3):
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[..., 1] = np.clip(hsv[..., 1] * amount, 0, 255)
    return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

# ---------- STEP 1: extract PNG frames ----------
os.makedirs(FRAMES_DIR, exist_ok=True)

cap = cv2.VideoCapture(config.VIDEO_PATH)
if not cap.isOpened():
    raise RuntimeError(f"Cannot open video: {config.VIDEO_PATH}")

source_fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
sample_interval = max(1, int(round(source_fps / config.FRAME_RATE)))

target_w = config.ASPECT_RATIO_WIDTH
target_h = config.ASPECT_RATIO_HEIGHT

frame_count = 0
saved = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # slight blur + good downscale to prevent aliasing
    frame = cv2.GaussianBlur(frame, (3, 3), 0)

    if frame_count % sample_interval == 0:
        resized = cv2.resize(frame, (target_w, target_h), interpolation=cv2.INTER_AREA)
        out_path = os.path.join(FRAMES_DIR, f"frame_{saved:04d}.png")
        cv2.imwrite(out_path, resized)
        saved += 1

    frame_count += 1

cap.release()
print(f"Extracted {saved} frames to '{FRAMES_DIR}' at ~{config.FRAME_RATE} fps")

# ---------- STEP 2: categorize each pixel to palette index ----------
os.makedirs(CATEG_DIR, exist_ok=True)

print("Beginning color categorization...")
for fname in sorted(os.listdir(FRAMES_DIR)):
    if not fname.endswith(".png"):
        continue
    img = cv2.imread(os.path.join(FRAMES_DIR, fname))  # BGR
    if img is None:
        continue
    if img.shape[1] != target_w or img.shape[0] != target_h:
        img = cv2.resize(img, (target_w, target_h), interpolation=cv2.INTER_AREA)

    if USE_DITHER:
        img = dither_L_before_quantization(img)
    if USE_SAT_BOOST:
        img = boost_saturation(img, SAT_AMOUNT)

    out = quantize_frame_to_palette_idxs(img)  # HxW uint8 indices 0..K-1

    out_txt = os.path.join(CATEG_DIR, f"categorized_{os.path.splitext(fname)[0]}.txt")
    with open(out_txt, "w") as f:
        for r in range(out.shape[0]):
            f.write(" ".join(str(int(v)) for v in out[r]) + "\n")

print(f"Categorized frames saved to '{CATEG_DIR}' (indices 0..{K-1})")
