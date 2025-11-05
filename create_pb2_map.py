# build_map_xml.py
import os
import config

FILE_NAME = f"generated_map_{config.ASPECT_RATIO_WIDTH}x{config.ASPECT_RATIO_HEIGHT}_{config.FRAME_RATE}FPS.xml"

# ---- geometry ----
width_pixels  = config.ASPECT_RATIO_WIDTH
height_pixels = config.ASPECT_RATIO_HEIGHT

x_offset = -(width_pixels // 2) * config.PIXEL_SIZE
y_offset = -(height_pixels // 2) * config.PIXEL_SIZE

PLAYER_NAME = getattr(config, "PLAYER_NAME", "Winter")
ZOOM_VALUE  = 100

player_x = width_pixels//2 * config.PIXEL_SIZE + 50
player_y = height_pixels//2 * config.PIXEL_SIZE + 50
ground_x = -(width_pixels//2 * config.PIXEL_SIZE) - 550
ground_y = player_y
ground_width  = -2 * ground_x
ground_height = 500

xml_parts = []

player_block = (
    f'<player uid="#player*1" x="{player_x}" y="{player_y}" tox="0" toy="0" hea="500" hmax="500" '
    f'team="0" side="1" char="77" incar="-1" botaction="0" ondeath="-1" /> '
    f'<box x="{ground_x}" y="{ground_y}" w="{ground_width}" h="{ground_height}" m="0" /> '
    f'<trigger uid="#trigger*9999999" x="310" y="20" enabled="true" maxcalls="1" '
    f'actions_1_type="51" actions_1_targetA="{ZOOM_VALUE}" actions_1_targetB="0" '
    f'actions_2_type="52" actions_2_targetA="#player*1" actions_2_targetB="{PLAYER_NAME}"/> '
    f'<timer uid="#timer*9999999" x="310" y="-10" enabled="true" maxcalls="1" '
    f'target="#trigger*9999999" delay="0" />'
)
xml_parts.append(player_block)

# ---- short id encoding ----
def number_to_letters(n):
    chars = [chr(i) for i in range(ord('a'), ord('z')+1)] + [chr(i) for i in range(ord('A'), ord('Z')+1)]
    if n <= 0:
        return "a"
    base = len(chars)
    res = ""
    while n > 0:
        n -= 1
        res = chars[n % base] + res
        n //= base
    return res

# ---- STEP 1: doors + triggers ----
K = len(config.PALETTE)
door_uid = 1
trigger_uid = 1
bank_start_uid = []

for i in range(height_pixels):
    for j in range(width_pixels):
        x = j * config.PIXEL_SIZE + x_offset
        y = i * config.PIXEL_SIZE + y_offset

        xml_parts.append(
            f'<door uid="#*{number_to_letters(door_uid)}" x="{x}" y="{y}" '
            f'w="{config.PIXEL_SIZE}" h="{config.PIXEL_SIZE}" tarx="0" tary="0" vis="true"/>'
        )

        bank_start_uid.append(trigger_uid)
        for k in range(K):
            hexcol = "#" + config.PALETTE[k]
            xml_parts.append(
                f'<trigger uid="#{number_to_letters(trigger_uid)}" enabled="true" maxcalls="-1" '
                f'actions_1_type="71" '
                f'actions_1_targetA="#*{number_to_letters(door_uid)}" '
                f'actions_1_targetB="{hexcol}"/>'
            )
            trigger_uid += 1

        door_uid += 1

with open(FILE_NAME, "w") as f:
    f.write("".join(xml_parts))

# ---- STEP 2: timers ----
def read_flat_indices(path):
    with open(path, "r") as fh:
        return fh.read().split()

frames_dir = "pixel_categorized_frames"
frame_files = sorted(fn for fn in os.listdir(frames_dir) if fn.endswith(".txt"))

timer_elems = []
timer_delay_delta = max(1, int(round(30 / config.FRAME_RATE)))
timer_delay_value = timer_delay_delta
expected_pixels = width_pixels * height_pixels
old_idx = [-1] * expected_pixels

for fname in frame_files:
    flat = read_flat_indices(os.path.join(frames_dir, fname))
    if len(flat) != expected_pixels:
        raise RuntimeError(f"{fname}: {len(flat)} indices, expected {expected_pixels}")

    for p in range(expected_pixels):
        new_pi = int(flat[p])
        if new_pi != old_idx[p]:
            bank_start = bank_start_uid[p]
            target_trigger_num = bank_start + new_pi
            target_trigger = "#" + number_to_letters(target_trigger_num)
            timer_elems.append(
                f'<timer enabled="true" maxcalls="1" target="{target_trigger}" delay="{timer_delay_value}"/>'
            )
            old_idx[p] = new_pi

    timer_delay_value += timer_delay_delta

with open(FILE_NAME, "a") as f:
    f.write("".join(timer_elems))

print(f"Map {FILE_NAME} created successfully.")

# ---- info ----
info_pixels = width_pixels * height_pixels
info_frames = len(frame_files)
info_len_sec = info_frames // config.FRAME_RATE
info_len_minsec = f"{int(info_len_sec // 60)}:{int(info_len_sec % 60):02d}"

with open("video_info.txt", "w") as info:
    info.write(
        "Video information:\n\n"
        f"{width_pixels}x{height_pixels} = {info_pixels} pixels\n"
        "4:3 aspect ratio\n"
        f"{config.FRAME_RATE} FPS\n"
        f"{info_frames} frames\n"
        f"Video Length: {info_frames}/{config.FRAME_RATE} = {info_len_sec}s = {info_len_minsec}\n"
        f"Palette size: {K}\n"
    )
print("Video information saved to video_info.txt")
