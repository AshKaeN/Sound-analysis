# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 11:53:20 2019

@author: Admin
"""

# -*- coding: utf-8 -*-
# this module use FFmpeg https://ffmpeg.org/ for windows
# download link https://ffmpeg.zeranoe.com/builds/
# version 20190923-8c90bb8 Windows 64-bit Static
# -*- coding: utf-8 -*-
# this module use FFmpeg https://ffmpeg.org/ for windows
# download link https://ffmpeg.zeranoe.com/builds/
# version 20190923-8c90bb8 Windows 64-bit Static
import os
import subprocess
import re
from os import listdir
from os.path import isfile, join


class FFmpeg:
    cmds = os.getcwd() + '\\ffmpeg\\bin\\ffmpeg.exe'  # ffmpeg path
    cmds_probe = os.getcwd() + '\\ffmpeg\\bin\\ffprobe.exe'  # ffmpeg path

    def __init__(self, mypath=os.getcwd(), cut_duration=10, sex='male'):
        self.sex = sex
        self.mypath = mypath
        self.file = [
            _ for _ in listdir(self.mypath) if isfile(
                    join(self.mypath, _)) and (
                            _.endswith('mp3') or _.endswith('wav'))]
        self.range = len(self.file)
        self.cut_duration = cut_duration

    def rename(self):
        '''rename sound files'''
        os.chdir(self.mypath)
        for i, _ in enumerate(listdir(self.mypath)):
            if isfile(
                    join(self.mypath, _)) and (
                            _.endswith('mp3') or _.endswith('wav')):
                os.rename(_, _[:-4]+'_'+str(i)+_[-4:])

    def find_voice(self):
        '''find actual current list of voice file in directory -> []'''
        return [
            _ for _ in listdir(self.mypath) if isfile(join(
                self.mypath, _))and (_.endswith('mp3') or _.endswith('wav'))]

    def popen(self, arg):
        ''' use popen template '''
        return subprocess.Popen(
                arg, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, shell=True)

    def mp3_wav(self, file):
        '''convert mp3 to wav 16kHz mono
        ffmpeg -i 111.mp3 -acodec pcm_s16le -ac 1 -ar 16000 out.wav
        '''
        if file.endswith('mp3'):
            output = file[:-4] + ".wav"
            # self.silenceremove(file) uncomment if sound with silence
            p = self.popen(FFmpeg.cmds+" -i "+file+" -acodec pcm_s16le -ac 1 -ar 16000 "+output)
            p.communicate()
            os.remove(file)
            #print(type(output), output)
            return output
        else:
            #print(type(file), file)
            return file

    def duration(self, file):
        ''' find duration of sound file
        ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 input.mp4'''
        p = self.popen(
            FFmpeg.cmds_probe+" -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 " + file)
        output, _ = p.communicate()
        return output.decode('ascii')[:-4]

    def silenceremove(self, file):
        ''' remove silanca part from sound file
        ffmpeg -i input.mp3 -af silenceremove=1:0:-36dB output.mp3'''
        output = file
        p = self.popen(FFmpeg.cmds+' -i'+file+' -af silenceremove=1:0:-36dB '+output)
        p.communicate()

    def cut_file(self):
        '''ffmpeg -i source-file.foo -ss 0 -t 600 first-10-min.m4v'''
        self.file = self.find_voice()
        for _ in range(self.range):
            self.file[_] = self.mp3_wav(self.file[_])
            duration = float(self.duration(self.file[_]))
            print('Обработан файл', self.file[_], \
                  'продолжительностью', duration, 'секунд.')
            if duration <= self.cut_duration:
                times = 1
            else:
                times = int(duration / self.cut_duration)
            command_1 = FFmpeg.cmds+" -i "+self.file[_]+" -ss "
            for i in range(times):
                output = self.file[_][:-4] + "_" + str(i) + ".wav"
                p = self.popen(command_1+str(self.cut_duration*i)+" -t "+str(self.cut_duration)+" "+output)
                p.communicate()
            os.remove(self.file[_])


if __name__ == '__main__':
    path = os.getcwd() + '\\data\\voice\\clips\\'
    ff = FFmpeg(path, sex='male')
    ff.rename()
    ff.cut_file() 
