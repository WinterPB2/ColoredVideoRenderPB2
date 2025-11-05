# PB2 Video to Map Converter - With Color Palette

![preview](https://github.com/WinterPB2/ColoredVideoRenderPB2/blob/main/assets/map_preview_jpg.jpg?raw=true)

This project converts a video file (originally "bad_apple.mp4") into a series of frames and generates a map file for Plazma Burst 2 (PB2) based on the pixel data from these frames. The project includes scripts for frame extraction, pixel categorization, and XML map generation.

## Video Showcase

Check out the YouTube video showcasing the "Bad Apple" animation in Plazma Burst 2 side by side with the original:

[Watch the Bad Apple Animation by BLAST3R](https://youtu.be/9Aqt_xMsmT4)  
[Watch the AMV Animation by Winter](https://www.youtube.com/watch?v=GkzCzspNSyc)
## Features

- Extract frames from a video at your desired FPS.
- Categorize pixels in each frame based on configurable color palette (will use a LOT of triggers and timers).
- Generate a PB2-compatible map in XML format based on the pixel data.
- Customizable color palette, aspect ratio and frame rate for the frame extraction and mapping process.

## Files

- `create_frames.py`: Script to extract frames from the video and categorize pixels.
- `create_pb2_map.py`: Script to generate the PB2 map from categorized pixel data.
- `config.py`: Configuration file to set the aspect ratio, pixel size, and frame rate.
- `bad_apple.mp4`: Input video file for frame extraction.

## Installation

1. Clone this repository and navigate into the directory:
   ```bash
   git clone https://github.com/WinterPB2/ColoredVideoRenderPB2
   cd ColoredVideoRenderPB2
   ```
2. Create a virtual environment (Optional - Recommended)
   ```bash
   python -m venv env  
   pip install --upgrade pip

   # Windows
   cd env/Scripts  
   activate.bat
   # Linux
   source env/bin/activate  
   ```
3. Ensure you have OpenCV installed. You can install it via pip:
   ```bash
   pip install opencv-python
   pip install moviepy
   ```

## Usage

1. Extract frames from the video:
   ```bash
   python create_frames.py
   ```

2. Generate the PB2 map:
   ```bash
   python create_pb2_map.py
   ```

The extracted frames will be saved in the `frames` directory, and the categorized pixel frames will be in the `pixel_categorized_frames` directory. The final map will be saved as `bad_apple_map.xml`.

## Configuration

You can adjust the aspect ratio in the `config.py` file:

```python
SCREEN_SIZE = 12
PIXEL_SIZE = 8
FRAME_RATE = 30 # frames per second

ASPECT_RATIO_WIDTH = 4 * SCREEN_SIZE
ASPECT_RATIO_HEIGHT = 3 * SCREEN_SIZE
```

#### Note: 

From my experience, due to PB2's limitations, it's only possible to load & play maps up to **25MB** in size.
The map will fail to load and the game will throw an error if the `bad_apple_map.xml` file is too large.

Large maps may not load in HTML5 version of the game because of automatic failure after 15 seconds.

## Contributing

Feel free to contribute to this project by submitting issues or pull requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.






