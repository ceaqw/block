import os

def str2zip(content, zipPath):
    with open(zipPath, 'w', encoding='utf8') as f:
        f.write(content)
    os.system('zip -o {} {}'.format(zipPath, zipPath))
    os.system('rm {}'.format(zipPath))

index = 0
for line in a:
    str2zip(line, index)
    index += 1

def main():
    if len(sys.argv) < 4:
        print("\033[32mTest args format: {} $taskPath $outPath $luaName\033[0m".format(sys.argv[0]))
    else:
        pass

if __name__ == '__main__':
