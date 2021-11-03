# coding: utf8

import os
import re
import sys
import json
import subprocess
from datetime import date

class OptionSshProxy:
    def __init__(self):
        self.call_map = {
            'create': self.create_proxy,
            'add': self.add_proxy,
            'del': self.del_proxy,
            'update': self.update_proxy,
            'find': self.find_proxy,
            'kill': self.kill_proxy,
            'help': self.help,
            'version': self.version,
        }
        self.proxy_dict = None
        user = subprocess.getoutput('whoami')
        data_path = '/home/{}/.create_ssh_proxy/'.format(user.strip())
        if not os.path.exists(data_path):
            os.mkdir(data_path)
        self.config_path = data_path + 'config.json'
        self.json_path = data_path + 'ssh_proxy.json'
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r+') as f:
                self.proxy_conf = json.load(f)
        else:
            self.proxy_conf = {"vsesion": "1.0.1", "is_rsa_path": "", "user_host": ""}
        if os.path.exists(self.json_path):
            with open(self.json_path, 'r+') as f:
                self.proxy_dict = json.load(f)
        else:
            self.proxy_dict = {}

        if not self.proxy_dict:
            print("Empty proxy list, please add proxy")

    def run(self):
        if len(sys.argv) < 2:
            self.help()
            raise ("Invaild Params")
        if sys.argv[1] not in self.call_map and sys.argv[1] != 'init':
            self.help()
            raise ("Invaild command")
        else:
            if sys.argv[1] == 'init':
                print ("Init start, Add the corresponding configuration and run the help command to view the details")
            else:
                self.call_map[sys.argv[1]]()

    def create_proxy(self):
        if len(sys.argv) < 3:
            self.help('create')
            raise("Error param format")
        arg = sys.argv[2]
        if arg not in self.proxy_dict:
            print("create fail no exists {}".format(arg))
        else:
            os.system("ssh -NCPf -i {} {} -L {}".format(
                self.proxy_conf['is_rsa_path'],
                self.proxy_conf['user_host'],
                self.proxy_dict[arg]
            ))
            print("create ssh proxy success")

    def add_proxy(self):
        if len(sys.argv) < 4:
            self.help('add')
            raise("Error param format")
        key = None
        value = None
        for arg in sys.argv[2: 4]:
            if ':' in arg:
                value = arg
            else:
                key = arg
        if key is None or value is None:
            print('add fail, invaild params')
        else:
            if key in self.proxy_dict:
                print("{} existed".format(key))
            else:
                self.proxy_dict[key] = value
                print("add {}: {} success".format(key, value))
    
    def del_proxy(self):
        if len(sys.argv) < 3:
            self.help('del')
            raise("Error param format")
        arg = sys.argv[2]
        if arg in self.proxy_dict:
            self.proxy_dict.pop(arg)
            self.kill_proxy(arg)
            print("del success")
        else:
            print("No exists proxy {}".format(arg))
    
    def update_proxy(self):
        if len(sys.argv) < 4:
            self.help('update')
            raise("Error param format")
        for arg in sys.argv[3: 7]:
            if 'id_rsa' in  arg:
                self.proxy_conf["is_rsa_path"] = arg
                print("update is_rsa_path success")
            elif '@' in arg:
                self.proxy_conf['user_host'] = arg
                print("update user_name@host success")
            elif ':' in arg:
                self.proxy_dict[sys.argv[2]] = arg
                print("update local_port:proxy_host:proxy_port success")
            else:
                self.proxy_dict[arg] = self.proxy_dict.pop(sys.argv[2])
                print("update proxy_aliase success")

    def find_proxy(self):
        if len(sys.argv) < 3:
            self.help('find')
            raise("Error param format")
        arg = sys.argv[2]
        print("="*30)
        if arg == 'all':
            for key in self.proxy_dict:
                print("{}: {}".format(key, self.proxy_dict[key]))
            print("Count: {}".format(len(self.proxy_dict)))
        elif arg == "help":
            self.help('find')
        elif arg in self.proxy_dict:
            print("{}: {}".format(arg, self.proxy_dict[arg]))
        else:
            print("No exists proxy {}".format(arg))
        print("="*30)
        
    def kill_proxy(self, port = ''):
        if len(sys.argv) < 3:
            self.help('kill')
            raise("Error param format")
        if port:
            arg = port
        else:
            arg = sys.argv[2]
        if arg == 'help':
            self.help('kill')
        elif arg in self.proxy_dict:
            pid_info = subprocess.getoutput("lsof -i :{}".format(self.proxy_dict[arg].split(":")[0]))
        else:
            pid_info = subprocess.getoutput("lsof -i :{}".format(arg))
        if "COMMAND" in pid_info:
            pid = pid_info.split("\n")[1].split(" ")[5]
        else:
            print("No exists {} no kill".format(arg))
            return
        os.system("kill -9 {}".format(pid))
        print("kill success")
        
    def close(self):
        if sys.argv[1] in ['add', 'del', 'update', 'init']:
            with open(self.config_path, 'w') as f:
                json.dump(self.proxy_conf, f)
            with open(self.json_path, 'w') as f:
                json.dump(self.proxy_dict, f)

    def help(self, print_select = 'all'):
        print_map = {
            'create': "\tcreate:\n\t\tCreate an SSH tunnel agent\n\t\t[args]: proxy_aliase",
            'add': "\tadd:\n\t\tAdd an SSH tunnel agent\n\t\t[args]: proxy_aliase local_port:proxy_host:proxy_port\n\t\t\tuser_name@host: default chen.chen@3.115.15.140\n\t\t\tid_rsa_path: default /home/ceaqw/.ssh/id_rsa",
            'del': "\tdel:\n\t\tDel an SSH tunnel agent\n\t\t[args]: proxy_aliase",
            'update': "\tupdate:\n\t\tUpdate an SSH tunnel agent\n\t\t[args]: proxy_aliase [proxy_aliase] [local_port:proxy_host:proxy_port] [user_name@host] [id_rsa_path]",
            'find': "\tfind:\n\t\tFind SSH tunnel agent\n\t\t[args]: [proxy_aliase | all]",
            'kill': "\tkill:\n\t\tKill an SSH tunnel agent\n\t\t[args]: proxy_aliase | local_port",
        }
        if print_select == 'all':
            print("The default parameters can be modified./data/config.json Manually")
            print("option the proxy command format:")
            print("\tcreate_proxy command [args...]")
            print("Commands:")
            print("\thelp:")
            print("\t\tViewing Help Information")
            for key in print_map:
                print(print_map[key])
            print("\tversion: Viewing version Information")
        else:
            print(print_map[print_select])
    
    def version(self):
        print("Version: " + self.proxy_conf['version'])
        print("©CEAQW. All rights reserved " + date.today().year)

def main():
    init = OptionSshProxy()
    init.run()
    init.close()

if __name__ == '__main__':
    main()
