# M3U Player

A simple M3U playlist player built with Python and Tkinter.

## Features

- Load M3U playlist files
- Display all tracks in the playlist
- Play/Pause/Stop controls
- Show currently playing track
- Navigate through playlist

## Requirements

- Python 3.6+
- pygame

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ahmedtawfick/m3u-player.git
cd m3u-player
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python main.py
```

### How to use:

1. Click **"Load M3U"** to select an M3U playlist file
2. The application will parse the playlist and display all tracks
3. Click **"Play"** to start playing the first track
4. Use **"Pause"** to pause/resume playback
5. Use **"Stop"** to stop playback
6. Click on any track in the playlist to select it before playing

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
- FLAC (with plugin)
- And other formats supported by pygame

## License

MIT License
