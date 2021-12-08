"""
Víctor Ferrer
SCAV - S2

"""

import os
import json
import subprocess
from youtube_transcript_api import YouTubeTranscriptApi


# First function translates 3 values in RGB into the 3 YUV values

class FFMPEG:

    @staticmethod
    def motion_vectors(x):
        """ Exercise 1. Shows the Motion vectors. We've found out that since Oct2017 FFmpeg removed the option of
            showing macros.
            We let the user choose between overlaping the mv into the BBB video (option 0)
            Or create a new video with only the mv (option 1)
        """
        if x == 0:
            cmd = str(
                "ffmpeg -flags2 +export_mvs -i BBB.mp4 -vf codecview=mv=pf+bf+bb BBB_mv.mp4")
            os.system(cmd)

        elif x == 1:
            cmd = str(
                "ffmpeg -flags2 +export_mvs -i BBB.mp4 -vf 'split[original], codecview=mv=pf+bf+bb[vectors],[vectors]["
                "original]blend=all_mode=difference128, eq=contrast=7:brightness=-0.3,scale=720:-2' BBB_onlymv.mp4")
            os.system(cmd)

    @staticmethod
    def container():
        """
            Exercise 2.
        """
        # Cutting 1 min of the BBB video from sec 36 by default
        cmd = str("ffmpeg -ss 00:00:36 -i BBB.mp4 -ss 00:01:00 -t 00:01:00 -c copy -an 1m_BBB.mp4")
        os.system(cmd)

        # Export 1m_BBB.mp4 audio as MP3 stereo track
        cmd2 = str("ffmpeg -i BBB.mp4 -ss 00:00:36 -t 00:01:00 -ac 2 -q:a 0 -map a 1m_BBB.mp3")
        os.system(cmd2)

        # Export 1m_BBB.mp4 audio as AAC with lower bitrate
        cmd3 = str("ffmpeg -i BBB.mp4 -ss 00:00:36 -t 00:01:00 -ac 2 -acodec aac -b:a 128k -q:a 0 -map a 1m_BBB.aac")
        os.system(cmd3)

        cmd4 = str("ffmpeg -i 1m_BBB.mp4 -i 1m_BBB.mp3 -i 1m_BBB.aac -map 0 -map 1 -map 2 -codec copy container.mp4")
        os.system(cmd4)

    @staticmethod
    def mp4_track_reader(file="container.mp4"):
        """
        Exercise 3. We read the different tracks from an mp4 container. And evaluate which broadcasting standard would fit
        :param file:
        :return:
        """
        cmd = str("ffprobe -loglevel 0 -print_format json -show_format -show_streams " + file)

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output = json.loads(process.communicate()[0])

        dvb = False
        isdb = False
        atsc = False
        dtmb = False

        for stream in output["streams"]:

            print(" ", stream['codec_type'], stream['codec_name'])
            name = stream['codec_name']
            type = stream['codec_type']

            if type == 'video':
                if name == 'h264' or name == 'MPEG2':
                    dvb = True
                    isdb = True
                    atsc = True
                    dtmb = True
                elif name == 'avs' or name == 'avs+':
                    dtmb = True

            if type == 'audio':
                if name == 'aac':
                    dvb = True
                    isdb = True
                    atsc = False
                    dtmb = True

                elif name == 'ac-3':
                    dvb = True
                    isdb = False
                    atsc = True
                    dtmb = True

                elif name == 'mp3':
                    dvb = True
                    isdb = False
                    atsc = False
                    dtmb = True
                elif name == 'dra' or name == 'mp2':
                    dtmb = True

        print("\n")
        if dvb:
            print(" DVB would fit\n")
        if isdb:
            print(" ISDB would fit\n")
        if atsc:
            print(" ATSC would fit\n")
        if dtmb:
            print(" DTMB would fit\n\n")

    @staticmethod
    def subtitle():
        """
        Exercise 4. In this method we integrate a video with printed subtitles
        """
        cmd = "ffmpeg -i 1m_BBB.mp4 -vf subtitles=subtitle.srt BBB_subtitled.mp4"
        os.system(cmd)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    option = int(input("Choose your action:\n\n  "
                       "1. Motion vector on BBB\n  "
                       "2. Container\n  "
                       "3. MP4 track reader\n  "
                       "4. Subtitle\n  "
                       "exit. To end the program\n\n Your action: "))
    while option != 'exit':

        if option == 1:
            x_ = int(input(' Enter 0 if you want to overlap BBB video and mv \n Enter 1 if you want to generate a '
                           'video with only mv.\n  Your option: '))
            if x_ == 0 or x_ == 1:
                FFMPEG.motion_vectors(x_)
            else:
                print("\n You have introduced a wrong option.\n\n")

        elif option == 2:
            FFMPEG.container()

        elif option == 3:
            file = input(
                "Enter the name of your file (within this directory). \n Otherwise, BBB video by default. (press "
                "enter) "
                "\n\n Your file: ")
            if file != "":
                FFMPEG.mp4_track_reader(file)
            else:
                FFMPEG.mp4_track_reader()

        elif option == 4:
            print("Press enter and the subtitles of the last Spiderman Trailer will be added to the 1m_BBB.mp4 "
                  "video.")
            FFMPEG.subtitle()

        else:
            print("\n The option introduced is not valid. Try again.\n\n")

        option = int(input("\n\nChoose your action:\n\n  "
                           "1. Motion vector on BBB\n  "
                           "2. Container\n  "
                           "3. MP4 track reader\n  "
                           "4. Subtitle\n  "
                           "exit. To end the program\n\n Your action: "))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
