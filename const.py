# -*- coding: utf-8 -*-

# 特权账户
PRIVILEGED_ACCOUNT = [
    "awk -F: '$3==0 {print $1}' /etc/passwd",
    'cat /etc/passwd | grep x:0',
    'stat /etc/passwd',
    'cat /etc/passwd | grep -v nologin',
    'cat /etc/passwd | grep /bin/bash',
]

# 特殊权限文件
SPECIAL_FILE = [
    'find / -perm /4000',  # SUID
    'find / -perm /2000',  # GUID
    'find / -perm /6000',  # SUID & GUID
]

# 进程信息
PROCESS_INFORMATION = [
    'ps aux --sort=pcpu | head -10',
    'ps -ef',
    'ps -U root -u root -N',
    'ps -u root',
    'ps -aef | grep inetd',
    "ps -ef | awk '{print}' | sort -n |uniq >1",
    'ls /proc | sort -n | uniq >2',
    'ls /etc/crontab',
]

HISTORY = [
    'history 5',
    'history',
]

DLL_HIJACKING = [
    'echo $LD_PRELOAD',
    'echo $LD_LIBRARY_PATH'
]

ALL = PRIVILEGED_ACCOUNT + SPECIAL_FILE + DLL_HIJACKING + PROCESS_INFORMATION + HISTORY
