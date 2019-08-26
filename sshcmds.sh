# coding:utf-8

""" 通过ssh登陆服务器并执行命令 """


import sys
import os
import time
import json

try:
    import paramiko
except ImportError:
    print '##### Not found "paramiko" on localhost, prepare to install !'
    yum = raw_input("##### Is yum available ? (Y/N): ")
    if yum != "Y":
        exit()
    os.system("yum install -y gcc python-devel python-pip")
    pipcmd = "pip install --index-url http://10.153.3.130/pypi/web/simple"
    pipcmd += " --trusted-host 10.153.3.130 paramiko"
    os.system(pipcmd)
    import paramiko


class Ssh(object):
    def __init__(self, ip, port, usr, pwd):
        self.ip = ip
        self.port = port
        self.username = usr
        self.password = pwd
        self.trans = None
        self.channel = None
        self.ends = ["]# ", "# ", "$ ", "> "]
        self.cmds = {
            "reboot": self.__reboot
        }

    def __connection(self):
        self.trans = paramiko.Transport((self.ip, self.port))
        self.trans.connect(username=self.username, password=self.password)
        self.channel = self.trans.open_session()
        self.channel.get_pty(width=150)
        self.channel.invoke_shell()

    def __defaultend(self, s):
        for end in self.ends:
            if s.endswith(end):
                return True
        return False

    def getres(self, cmd):
        self.__connection()
        s = paramiko.SSHClient()
        s._transport = self.trans
        stdin, stdout, stderr = s.exec_command(cmd, get_pty=True)
        res = stderr.readlines() or stdout.readlines()
        self.__close()
        return res

    def __exec_cmd(self, cmd):
        outputs = [None]
        inputs = [cmd[0]]
        for i in range(1, len(cmd)):
            outputs.append(cmd[i][0])
            inputs.append(cmd[i][1])

        i = 0
        while i < len(cmd):
            if inputs[i] in self.cmds:
                self.cmds[inputs[i]]()
                i += 1
                continue

            self.channel.send('{0}\n'.format(inputs[i]))
            time.sleep(1)
            i += 1
            while True:
                data = self.channel.recv(4096)
                sys.stdout.write(data)
                sys.stdout.flush()

                flag = False
                if i == len(cmd) and self.__defaultend(data):
                    flag = True
                elif i < len(cmd):
                    for j in range(i, len(cmd)):
                        if data.endswith(outputs[j]):
                            i = j
                            flag = True
                            break

                if flag:
                    break

    def __close(self):
        self.trans.close()

    def __reboot(self):
        print "reboot system"
        self.channel.send('reboot\n')
        time.sleep(1)

    def exec_cmds(self, cmds):
        self.__connection()
        time.sleep(1)
        for cmd in cmds:
            self.__exec_cmd(cmd)
        self.__close()
        print "\n"


def start_exec(hosts):
    for host in hosts:
        ipaddr = host["host"]
        port = host["port"]
        username = host["username"]
        password = host["password"]
        cmds = host["cmds"]
        ssh = Ssh(ipaddr, port, username, password)
        ssh.exec_cmds(cmds)


def read_config(fp):
    conf = None
    with open(fp, "r") as f:
        conf = json.load(f)
    return conf
