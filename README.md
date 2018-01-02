# mp32opus
An mp3 to opus converter

Converts MP3 files into the OPUS format and saves ID3 tags and images in the OPUS file.

## Depends
- python >= 3
- python3-eyed3 >= 0.8
- libav-tools >= 6:0.8

## Usage
- `mp32opus -h` displays help
- Example: `mp32opus --bitrate 64 file.mp3 file.opus` converts `file.mp3` into `file.opus` with 64 kbit/sec bitrate
