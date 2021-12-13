'''
Date: 2021-11-16 10:16:24
LastEditTime: 2021-12-13 14:35:00
Author: ceaqw
'''
import os
import sys

def str2zip(content, zipPath):
    with open(zipPath, 'w', encoding='utf8') as f:
        f.write(content)
    os.system('zip -o {} {}'.format(zipPath, zipPath))
    os.system('rm {}'.format(zipPath))

def getContents(contentPath):
    with open(contentPath, 'r') as f:
        return f.read().split("\n")

def convert(contentPath, outPath):
    contents = getContents(contentPath)
    index = 0
    total = len(contents)
    for line in contents:
        print("Convert process {}/{}".format(index+1, total))
        str2zip(line, "{}/{}".format(outPath, index))
        index += 1

def main():
    if len(sys.argv) != 3:
        print("\033[32mTest args format: {} $contentPath $outPath\033[0m".format(sys.argv[0]))
    else:
        convert(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
    main()