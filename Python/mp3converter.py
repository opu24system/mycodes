#!/usr/bin/env python3

from pathlib import Path
import sys, subprocess, csv, os, os.path, glob, shutil

def convertToMp3(inputFile, root):
    fileName = inputFile.split(".")[0];
    fileType = inputFile.split(".")[1];
    if fileType == "m4a" or fileType == "wma":
        if not (os.path.isdir("mp3Folder" + root[1:])):
            os.makedirs("mp3Folder" + root[1:])
        if fileType == "m4a":
            subprocess.call(["faad", "." + inputFile , "-o",  "tmp.wav"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            subprocess.call(["lame", "--preset", "cbr", "192", "tmp.wav",  "mp3Folder" + fileName + ".mp3"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT);
        else:
            subprocess.call(["mplayer", "." + inputFile, "-ao", "pcm:file=tmp.wav"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT);
            subprocess.call(["lame", "--preset", "cbr", "192", "tmp.wav",  "mp3Folder" + fileName + ".mp3"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        os.remove("tmp.wav")

    elif fileType == "mp3" or fileType == "jpg":
        if not (os.path.isdir("mp3Folder" + root[1:])):
            os.makedirs("mp3Folder" + root[1:])
        shutil.copy("." + inputFile, "mp3Folder" + inputFile)

def main():
    pathList = []
    for root, dirs, files in os.walk('./'):
        for fname in files:
            pathList.append([os.path.join(root, fname)[1:], root])

    count = 1
    for path in pathList:
        print("Now proceeding " + str(count) + "/" + str(len(pathList)))
        convertToMp3(path[0], path[1])
        count += 1
    print("done.")

if __name__ == '__main__':
    main()


#glob.glob("*.*")
