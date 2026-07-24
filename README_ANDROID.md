# M3U Player - Android

A simple M3U playlist player built with Python and Kivy for Android devices.

## Features

- Load M3U playlist files
- Display all tracks in the playlist
- Play/Pause/Stop controls
- Show currently playing track
- Navigate through playlist

## Requirements

- Python 3.7+
- Kivy
- Pillow

## Installation

### For Development (Running on PC):

1. Clone the repository:
```bash
git clone https://github.com/ahmedtawfick/m3u-player.git
cd m3u-player
git checkout android
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
python main.py
```

### Build for Android:

Use **Buildozer** to compile the app for Android:

1. Install Buildozer:
```bash
pip install buildozer
```

2. Build the APK:
```bash
buildozer android debug
```

This will generate an APK file in the `bin/` directory that you can install on your Android device.

## Usage

1. Open the app on your Android device
2. Tap **"Load M3U"** to select an M3U playlist file
3. The app will parse the playlist and display all tracks
4. Tap **"Play"** to start playing the first track
5. Use **"Pause"** to pause/resume playback
6. Use **"Stop"** to stop playback

## M3U File Format

M3U files are simple text files containing a list of audio file paths. Example:

```
#EXTM3U
#EXTINF:-1, Artist - Song Title
/path/to/song1.mp3
#EXTINF:-1, Artist - Song Title 2
/path/to/song2.mp3
```

## Supported Audio Formats

- MP3
- WAV
- OGG
- FLAC
- And other formats supported by Kivy audio

## Permissions Required

The app requires the following Android permissions:
- `READ_EXTERNAL_STORAGE` - To read M3U files and audio files
- `WRITE_EXTERNAL_STORAGE` - For future features

## License

MIT License
