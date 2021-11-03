# coding: utf8
# 使用之前已将 /home/ceaqw/.local/lua 加入LUA_PATH 环境变量： export LUA_PATH=$LUA_PATH:/home/ceaqw/.local/lua/lua.lua
# 个人临时临时测试
import subprocess
import sys
import os

SCRIPT = None

def runOnce(task):
    outPath = sys.argv[2]
    result = subprocess.getoutput(r"""lua -l %s -e "print(run('%s'))" """ % (SCRIPT, task.strip()))
    with open(outPath, 'a+', encoding='utf8') as f:
        f.write(result + "\n")

def run():
    tasks = None
    taskPath = sys.argv[1]
    with open(taskPath, 'r', encoding='utf8') as f:
        tasks = f.readlines()
    if tasks is None:
        print("No tasks")
        return
    taskCount = len(tasks)
    currentTask = 1
    for task in tasks:
        print("Task: {}·····".format(task[:100].strip()))
        print("taskProcessing: {}/{}".format(currentTask, taskCount))
        runOnce(task)
        currentTask += 1

def main():
    if len(sys.argv) < 4:
        print("\033[32mTest args format: {} $taskPath $outPath $luaName\033[0m".format(sys.argv[0]))
    else:
        global SCRIPT
        SCRIPT = sys.argv[3].split('.')[0].split('/')[-1]
        os.system("cp ./{}.lua /home/ceaqw/.local/lua/{}.lua".format(SCRIPT, SCRIPT))
        run()
        os.system("rm /home/ceaqw/.local/lua/{}.lua".format(SCRIPT))

if __name__ == '__main__':
    main()