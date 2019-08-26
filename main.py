# coding:utf-8

""" 调用create.py和mount.py进行共享存储创建于挂载 """

import sshcmds
import create
import mount
import sys


def createiscsi(conf):
    create.init_env(conf)
    create.create_iscsis(conf)


def mountiscsi(conf):
    for c in conf:
        mount.mount(c)


def main(conf):
    createiscsi(conf["create"])
    mountiscsi(conf["mount"])


if __name__ == "__main__":
    try:
        confpath = sys.argv[1]
    except IndexError:
        print "Must specify config file, such as: python main.py configs/config.json"
        exit()
    print "########################################"
    print "######## CTT CentOS7 ISCSI Tool ########"
    print "########################################"
    print "  1. Create And Mount Shared Stroage"
    print "  2. Create Shared Stroage"
    print "  3. Mount Shared Stroage"
    s = raw_input("Select the option number above: ")
    conf = sshcmds.read_config(confpath)
    if s == "1":
        main(conf)
    elif s == "2":
        createiscsi(conf["create"])
    elif s == "3":
        mountiscsi(conf["mount"])
    else:
        print "输入有误!"
