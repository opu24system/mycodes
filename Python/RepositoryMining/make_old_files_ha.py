#!usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime,re,os,sys,subprocess, shutil, os.path, excounter #モジュールをインポート

#f = open("javafiles.txt","r")

def process_command(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, universal_newlines=True, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        return "error"

    #return subprocess.check_output(cmd, shell=True, universal_newlines=True, stderr=errmsg)

comcount = []
methodcount = 0

a = []

count = 0
checknum = 0

oldestPath = "/Users/lab-6/mining/hadoop_old_versions"
remjav = re.compile(u"/([^/]+\.java)")
fer = open("/Users/lab-6/mining/hadoop_old_versions/nofile.txt", "w")
dexfile = []

print("Now Processing")

#for line in a:
for line in open("javafiles_ha.txt", "r"):
    count += 1
    if count % 500 == 0:
        checknum += 1
        print(str(checknum * 500) + " files are proceeded")

    line = line.strip()

    #1つのjavaファイルに対する履歴を閲覧
    result = process_command("git log --oneline " + line)
    results = []
    results = str(result).splitlines()

    #コピー先のパスの指定
    dstline = oldestPath + line.replace("./", "/")
    #ファイルパスからファイル名のみを削除
    jav = remjav.search(dstline)
    filename = jav.group(1)
    pathOnly = dstline.replace(filename, "")

    #ファイルごとに全バージョンを入れるためのフォルダを作成
    folpass = pathOnly + "!files!" + filename.replace(".java", "") + "/"
    dstline = folpass + filename
    #print(dstline)

    if os.path.isdir(folpass) == False:
        os.makedirs(folpass)

    for i in range(len(results)):
        CommitId = results[i].split(" ")[0]

        #ファイルをその時の状態に
        err = process_command("git checkout " + CommitId + " " + line)

        #ファイルが存在しないバージョンの場合，記録した後，飛ばして進める
        if err == "error":
            dexfile.append(line + " " + CommitId + "\n")
            continue

        #とりあえずコピー
        shutil.copy(line, dstline)

        #コピーしたもののファイル名に，番号をつけてリネーム
        if i == len(results) - 1:
            os.rename(dstline, folpass + str(i) + "-oldest-" + CommitId + "-" + filename)
        else:
            os.rename(dstline, folpass + str(i) + "-" + CommitId + "-" + filename)

    #ファイルを最新の状態に戻す
    process_command("git checkout head " + line)

for outstr in dexfile:
    fer.write(outstr)

fer.close()