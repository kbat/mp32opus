# mp32opus
An MP3 to Opus converter

Converts MP3 files into the Opus format and saves ID3 tags and images in the Opus file.

## Depends
- python >= 3
- python3-eyed3 >= 0.8
- libav-tools >= 7:3.4
- opus-tools >= 0.1.10

## Usage
- `mp32opus -h` displays help
- Example: `mp32opus --bitrate 64 file.mp3 file.opus` converts `file.mp3` into `file.opus` with 64 kbit/sec bitrate
