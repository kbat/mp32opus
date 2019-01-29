#! /usr/bin/python3
#
# An mp3 to opus converter
#
# File: mp32opus.py
#
# Copyright (c) 2017-2018 by Konstantin Batkov
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>. 
#

import os
import sys
import eyed3
import argparse
import tempfile
import subprocess

class Image:
    def __init__(self,mime_type,picture_type,description,image_data):
        self.mime_type = mime_type
        self.picture_type = picture_type
        self.description = description
        self.image_data = image_data
        self.save()

    def save(self):
        self.fb = tempfile.NamedTemporaryFile()
        self.fname = self.fb.name
        self.fb.write(self.image_data)

    def Print(self):
        print(" MIME: ",self.mime_type)
        print(" picture_type: ", self.picture_type)
        print(" description: ",self.description)
        print(" filename: ",self.fname)

    def __str__(self):
        return " --picture '" + str(self.picture_type) + "|" + self.mime_type + "|" + self.description + "||" + self.fname + "'"

def main():
    """
    MP3 -> Opus converter
    """
    parser = argparse.ArgumentParser(description=main.__doc__, epilog="Homepage: https://github.com/kbat/mp32opus")
    parser.add_argument('mp3', type=str, help='MP3 input file name.')
    parser.add_argument('opus', type=str, nargs='?', help="Opus output file name. If not specified, the MP3 file name with the .opus extension is used.",default="")
    parser.add_argument('--bitrate', dest='bitrate', type=int, help='Opus bitrate. If not specivied, set to min(48kbit/sec,half of MP3 bitrate). 48 kbit/sec is a reasonable bitrate for audiobooks, which approximately corresponds to MP3 96. More details are here: https://auphonic.com/blog/2012/09/26/opus-revolutionary-open-audio-codec-podcasts-and-internet-audio and here: https://wiki.xiph.org/index.php?title=Opus_Recommended_Settings&mobileaction=toggle_view_desktop', default=0, required=False)
    args = parser.parse_args()

    if args.opus == "":
        args.opus = os.path.splitext(os.path.basename(args.mp3))[0] + ".opus"

    audiofile = eyed3.load(args.mp3)

    if args.bitrate == 0:
        args.bitrate = min(audiofile.info.bit_rate[1]/2.0, 48)
        if args.bitrate<20:
            print("Calculated bitrate of %g can cause significant quality reduction. Set it explicitly with '--bitrate' argument." % args.bitrate)
            exit(1)

    print("Bitrate: ", args.bitrate, audiofile.info.bit_rate)
    print("Duration: ", audiofile.info.time_secs)

    picture = ""
    if audiofile.tag is not None:
        print("Images:")
        for imageinfo in audiofile.tag.images:
            img = Image(imageinfo.mime_type, imageinfo.picture_type, imageinfo.description, imageinfo.image_data)
            img.Print()
            picture = picture + str(img)

    # screen double quotes in the file names before using them in BASH:
    args.mp3  =  args.mp3.replace("\"", "\\\"")
    args.opus = args.opus.replace("\"", "\\\"")

    cmd = "avconv -i \"%s\" -f flac - | opusenc --bitrate %.3f %s - \"%s\"" % (args.mp3, args.bitrate, picture, args.opus)
# This looks more elegant, but it's yet unstable with current avconv:
#    cmd = "avconv -i %s -map 0:a -codec:a opus -b:a %dk -vbr on -strict -2 %s" % (args.mp3, args.bitrate, args.opus)
    print(cmd)

    if not os.path.isfile(args.opus):
        subprocess.call(cmd, shell=True)
    else:
        sys.exit("Error: %s exists" % args.opus)
        


if __name__=="__main__":
    sys.exit(main())
