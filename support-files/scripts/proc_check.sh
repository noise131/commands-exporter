#!/bin/bash

# 进程检查脚本
#
#   返回码:
#     进程存在返回 0
#     进程不存在返回 1
#     脚本异常 10
#
#   示例:
#     ]# bash proc_check.sh "prometheus"; echo $?
#     进程存在
#     0
#
#     ]# bash proc_check.sh "prometheus1"; echo $?
#     进程不存在
#     1
# 
#     # 完整匹配
#     ]# bash proc_check.sh "\<prometheus\>"; echo $?
#     进程存在
#     0
#
#     ]# bash proc_check.sh "\<prometh\>"; echo $?
#     进程不存在
#     1

if [ -z "$1" ]; then
    echo 'error: 参数不能为空' >&2
    exit 10
fi

if which pgrep &>/dev/null; then
    if [ "$(pgrep -c "$1")" -gt "0" ]; then
        echo '进程存在'
        exit 0
    fi
    echo '进程不存在'
    exit 1
fi

echo "系统中没有 pgrep 工具 (软件包: procps-ng)" >&2
exit 10
