# coding:utf-8

""" 根据config.json文件中的create项，创建iscsi共享存储 """

from sshcmds import Ssh
from sshcmds import start_exec
from sshcmds import read_config


def init_env(conf):
    svr = conf["server"]
    ssh = Ssh(svr["ip"], svr["port"], svr["user"], svr["passwd"])
    # 创建共享存储保存路径
    basedir = ssh.getres("ls " + conf["server"]["basedir"])
    if len(basedir) == 1:
        if basedir[0].find("No such file or directory") != -1:
            ssh.getres("mkdir -p " + conf["server"]["basedir"])
    print "##### %s has been created\n" % conf["server"]["basedir"]

    # 检查是否安装targetcli，如果没有则安装
    target = ssh.getres("ls /usr/lib/systemd/system | grep target.service")
    if len(target) == 0:
        print "##### Cannot found targetcli on {0} !!!".format(svr["ip"])
        print "##### Prepare to install targetcli !!!"
        yum = raw_input("##### Is yum available on {0} ? (Y/N): ".format(svr["ip"]))
        if yum != "Y":
            exit()
        cmds = [["yum install -y targetcli"]]
        ssh.exec_cmds(cmds)
    print "##### targetcli already installed\n"

    # 检查是否enable target，如果没有则start并enable
    enable = ssh.getres("ls /etc/systemd/system/multi-user.target.wants | grep target.service")
    if len(enable) == 0:
        cmds = [
            ["systemctl start target"],
            ["systemctl enable target"]
        ]
        ssh.exec_cmds(cmds)
    print "##### target.service has been started and enabled\n"

    # 检查firewalld是否disable，如果没有，则stop并disable
    firewalld = ssh.getres("ls /etc/systemd/system/basic.target.wants | grep firewalld")
    if len(firewalld) != 0:
        cmds = [
            ["systemctl stop firewalld"],
            ["systemctl disable firewalld"]
        ]
        ssh.exec_cmds(cmds)
    print "##### firewalld has benn stop and disabled\n"


def get_iqns(clients):
    """ 获取所有客户端的iqn号 """
    iqns = {}
    for c in clients:
        ssh = Ssh(c["ip"], c["port"], c["user"], c["passwd"])
        iqnss = ssh.getres("cat /etc/iscsi/initiatorname.iscsi")
        for iqn in iqnss:
            if iqn.startswith("InitiatorName"):
                break
        print "##### get client {ip} iqn: {iqn}".format(ip=c["ip"], iqn=iqn)
        iqns[c["ip"]] = iqn.strip().split("=")[-1]
    return iqns


def create_iscsis(conf):
    cmds = [
        {
            "host": conf["server"]["ip"],
            "port": conf["server"]["port"],
            "username": conf["server"]["user"],
            "password": conf["server"]["passwd"],
            "cmds": [
                ["targetcli"]
            ]
        }
    ]
    iqns = get_iqns(conf["clients"])
    for target in conf["targets"]:
        iscsi_cmds = [
            ["cd /backstores/fileio"],
            ["create {1} {0}/{1}.img {2}".format(conf["server"]["basedir"], target["name"], target["size"])],
            ["cd /iscsi"],
            ["create iqn.2017-11.com.h3c:{0}".format(target["name"])],
            ["cd /iscsi/iqn.2017-11.com.h3c:{0}/tpg1/luns".format(target["name"])],
            ["create /backstores/fileio/{0}".format(target["name"])],
            ["cd /iscsi/iqn.2017-11.com.h3c:{0}/tpg1/acls".format(target["name"])]
        ]
        for allow in target["allowed"]:
            iscsi_cmds.append(["create {0}".format(iqns[allow])])
        cmds[0]["cmds"].extend(iscsi_cmds)
    cmds[0]["cmds"].extend([["cd /"], ["saveconfig"], ["exit"]])
    start_exec(cmds)


if __name__ == "__main__":
    conf = read_config("./config.json")["create"]
    init_env(conf)
    create_iscsis(conf)
