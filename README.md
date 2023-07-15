# Hand Gesture Video Control

This Python script allows you to control video playback on YouTube using hand gestures captured from your webcam. It utilizes computer vision techniques and the following libraries:

- OpenCV (cv2)
- Mediapipe
- Numpy
- comtypes
- pycaw
- Selenium

## Features

- Control video playback on YouTube by making hand gestures in front of your webcam.
- Adjust the volume by using hand gestures.
- Pause and resume video playback by closing and opening your hand.

## Installation

1. Clone the repository:

```shell
git clone https://github.com/rohitnitr/hand-gesture-video-control.git
```

2. Navigate to the project directory:

```shell
cd hand-gesture-video-control
```

3. Install the required dependencies using pip:

```shell
pip install -r requirements.txt
```

4. Download the ChromeDriver executable matching your Chrome browser version and place it in the project directory. You can download the ChromeDriver from the official website: [ChromeDriver Downloads](https://sites.google.com/a/chromium.org/chromedriver/downloads)

## Usage

1. Run the Python script:

```shell
python video-control.py
```

2. The script will start your webcam and open a browser window with a YouTube video.

3. Make hand gestures in front of your webcam to control video playback and adjust the volume.

## Configuration

- You can change the video URL by modifying the `video_url` variable in the script.
- The hand gesture control thresholds and settings can be adjusted within the code according to your preferences.

## License

This project is licensed under the [MIT License](LICENSE).

---


