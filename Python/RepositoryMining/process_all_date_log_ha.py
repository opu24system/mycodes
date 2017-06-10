#!usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime,re,os,sys,subprocess,excounter #モジュールをインポート

#f = open("javafiles.txt","r")
ferr = open("result_all_err_ha.txt", "w")
fres = open("result_all_date_log_ha.txt", "w")

def process_command(cmd):
    devnull = open(os.devnull, 'w')
    r = subprocess.check_output(cmd, shell=True, universal_newlines=True, stderr=devnull)
    devnull.close()
    return r

a = []

comcount = []
methodCount = 0
count = 0
checknum = 0
oldVerPath = "./hadoop_old_versions"
remJav = re.compile(u"/([^/]+\.java)")

print("Now Proceeding")
#for line in a:
for line in open("javafiles_ha.txt", "r"):
    count += 1
    print(str(count-1) + " files are proceeded")
    if count % 500 == 0:
        checknum += 1
        #print(str(checknum * 500) + " files are proceeded")

    line = line.strip()

    searchFile = oldVerPath + line.replace("./", "/")
    searchFilePath = searchFile.replace(".java", "") + "/"

    #コピー先のパスの指定
    dstLine = oldVerPath + line.replace("./", "/")
    #ファイルパスからファイル名のみを削除
    jav = remJav.search(dstLine)
    filename = jav.group(1)
    pathOnly = dstLine.replace(filename, "")

    #ファイルごとにフォルダを指定
    folPass = pathOnly + "!files!" + filename.replace(".java", "") + "/"

    #全バージョンのファイル名を列挙
    allfiles = os.listdir(folPass)

    allNames = []
    allResults = []

    nameDic = {}
    fileCount = 0

    if len(allfiles) <= 1:
        comcount.append("None" + "\t" + line + "\n")
        continue

    #文字列ソートになっているのでコミット順になるようにallfilesをソートする
    allfiles.sort(key = lambda x:int(x.split("-")[0]))

    for fileName in allfiles:
        names, results = excounter.get_result(folPass + fileName)
        fileCount += 1

        if len(names) == 0:
            continue

        hash = fileName.split("-")
        if hash[1] == "oldest":
            hashTag = hash[2]
        else:
            hashTag = hash[1]

        #辞書にそのメソッドが何回出現したか記録
        for i in range(len(names)):
            if names[i] in nameDic:
                num = nameDic[names[i]][0]
                nameDic[names[i]][0] += 1
                nameDic[names[i]][1] += "-" + str(num) + "-\t" + hashTag + "\t" + results[i] + "\n"
            else:
                nameDic[names[i]] = [1, line + "\n-0-\t" + hashTag + "\t" + results[i] + "\n"]

        allNames.append(names)
        allResults.append(results)

    #すべてのバージョンで存在するもののみ書き出すが，ここで各コミットに対し，日付とコミットログを追加する
    mCount = 0
    for k, v in nameDic.items():
        if v[0] == len(allfiles):
            resultStr = v[1].strip()
            path = resultStr.split("\n")[0]
            newResult = path + "\n"

            for spResult in resultStr.split("\n")[1:]:
                sp = spResult.split("\t")
                hash = sp[1]

                #日付とログ取得
                result = process_command('git log --date=short --pretty=format:\"%h\t%ad\t%s\" ' + hash + " " + path)
                results = str(result).splitlines()
                log = results[0].split("\t")
                comLog = log[2]
                comDate = log[1].split("-")

                spResult += "\t" + comDate[0] + ":" + comDate[1] + ":" + comDate[2] + "\t" + comLog + "\n"
                newResult += spResult

            comcount.append(newResult)
            mCount += 1

    if mCount == 0:
        comcount.append("None" + "\t" + line + "\n")
    else:
        methodCount += mCount

for outStr in comcount:
    fres.write(outStr)

print(str(methodCount) + " Methods are proceeded")

ferr.close()
fres.close()