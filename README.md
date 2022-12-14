# commands-exporter

Prometheus 命令执行导出器 [![Release-1.0](https://img.shields.io/badge/Release-1.0-green)](##)

执行系统命令将返回码作为指标进行导出

# 基本环境

## 测试环境软件版本

- [![Python-3.10.5](https://img.shields.io/badge/Python-3.10.5-blue)](https://www.python.org/)
- [![Prometheus-2.37.0](https://img.shields.io/badge/Prometheus-2.37.0-orange)](https://prometheus.io/)

## python 依赖模块版本

使用 二进制 程序无需安装模块

```
Package           Version
----------------- -------
prometheus-client 0.14.1
ruamel.yaml       0.17.21
ruamel.yaml.clib  0.2.6
```

### 安装所需模块

项目提供了模块清单，可以直接使用清单进行安装

```shell
]# git clone https://github.com/noise131/commands-exporter.git

]# cd commands-exporter

]# pip install -r requirements.txt
```

# 启动应用

## 使用源码启动

安装好依赖模块之后使用以下指令启动

```shell
]# python main.py 
2022-09-24 21:27:45,758 - [INFO] - logger - 406248 - 140590740010816 - <module> - 程序导入配置完成
2022-09-24 21:27:45,870 - [INFO] - logger.main - 406248 - 140590740010816 - <module> - 程序工作目录 : /root/command-exporter
2022-09-24 21:27:46,044 - [INFO] - logger.ToolsClass - 406248 - 140590596486912 - command_exec - 命令执行成功, item: test_command_2, command: test -e /tmp/command_test.txt, describe: This metrics is not describe.
2022-09-24 21:27:46,049 - [INFO] - logger.ToolsClass - 406248 - 140590385723136 - command_exec - 命令执行成功, item: test_command_3, command: ls /tmp/command_test.txt, describe: 测试命令3
2022-09-24 21:27:46,080 - [INFO] - logger.ToolsClass - 406248 - 140590604879616 - command_exec - 命令执行成功, item: test_command_1, command: ls -la, describe: 测试命令1
......
```

## 使用二进制文件启动

```shell
]# ./commands-exporter_linux-amd64_v1.0 
2022-09-25 10:47:39,107 - [INFO] - logger - 34708 - 140202858040192 - <module> - 程序导入配置完成
2022-09-25 10:47:39,220 - [INFO] - logger.main - 34708 - 140202858040192 - <module> - 程序工作目录 : /root
2022-09-25 10:47:39,396 - [INFO] - logger.ToolsClass - 34708 - 140202722895616 - command_exec - 命令执行成功, item: test_command_1, command: ls -la, describe: 测试命令1
2022-09-25 10:47:39,397 - [ERROR] - logger.ToolsClass - 34708 - 140202714502912 - command_exec - 命令执行返回值不为 0, item: test_command_2, command: test -e /tmp/command_test.txt, return: 1, describe: This metrics is not describe., stdout: [], stderr: []
2022-09-25 10:47:39,400 - [ERROR] - logger.ToolsClass - 34708 - 140202714502912 - command_exec - 命令执行返回值不为 0, item: test_command_3, command: ls /tmp/command_test.txt, return: 2, describe: 测试命令3, stdout: [], stderr: [b"ls: cannot access '/tmp/command_test.txt': No such file or directory\n"]
```

> 二进制执行之前删除了 `/tmp/command_test.txt` 文件

## 注册为 systemd 服务进行管理

项目中附带了 systemd service 文件 : `support-files/systemd-unit/commands-exporter.service` 将其复制到 `/usr/lib/systemd/system/` 中即可

```shell
]# cp /usr/local/commands-exporter_linux-amd64/support-files/systemd-unit/commands-exporter.service /usr/lib/systemd/system/

]# systemctl daemon-reload

]# systemctl start commands-exporter.service 
]# systemctl status commands-exporter.service 
● commands-exporter.service - Commands Exporter
   Loaded: loaded (/usr/lib/systemd/system/commands-exporter.service; disabled; vendor preset: disabled)
   Active: active (running) since Sun 2022-09-25 15:57:01 CST; 6s ago
     Docs: https://github.com/noise131/commands-exporter
 Main PID: 36240 (commands-export)
    Tasks: 3 (limit: 4722)
   Memory: 56.3M
   CGroup: /system.slice/commands-exporter.service
           ├─36240 /usr/local/commands-exporter_linux-amd64/commands-exporter
           └─36241 /usr/local/commands-exporter_linux-amd64/commands-exporter
```

查看导出器的端口

```shell
]# netstat -tlnp |grep 8100
tcp        0      0 0.0.0.0:8100            0.0.0.0:*               LISTEN      36241/commands-expo
```

查看导出器的 web 数据

```shell
]# curl -s 172.5.1.11:8100
# HELP python_gc_objects_collected_total Objects collected during gc
# TYPE python_gc_objects_collected_total counter
python_gc_objects_collected_total{generation="0"} 463.0
python_gc_objects_collected_total{generation="1"} 7.0
python_gc_objects_collected_total{generation="2"} 0.0
......
# HELP commands_exec_status 命令执行指标
# TYPE commands_exec_status gauge
commands_exec_status{command="test -e /tmp/command_test.txt",describe="This metrics is not describe.",item="test_command_2"} 1.0
commands_exec_status{command="ls /tmp/command_test.txt",describe="测试命令3",item="test_command_3"} 2.0
commands_exec_status{command="ls -la",describe="测试命令1",item="test_command_1"} 0.0
```

# 配置文件

配置文件默认读取位置 : 主程序所在目录中的 commands.yaml

```shell
---
port: 8100
interval: 30
commands:
  - item: test_command_1
    command: "ls -la"
    describe: "测试命令1"
  - item: test_command_2
    command: "test -e /tmp/command_test.txt"
    # describe: "测试命令2"
  - item: test_command_3
    command: "ls /tmp/command_test.txt"
    describe: "测试命令3"
...
```

> **port** : 暴露指标的 web 端口号。default : 8100
>
> **interval** : 命令的执行间隔，单位 s(秒)。default : 30
>
> **commands** : 数组类型，存储多个要执行命令的项目。每个元素 (项目) 是一个字典，有以下三个字段 :
>
> - `item` : 项目名，会作为标签出现在指标中。必须
> - `command` : 要执行的命令，会作为标签出现在指标中。必须
> - `describe` : 执行命令的项目描述，会作为标签出现在指标中。default : 无描述

# prometheus 配置

```shell
]# cat prometheus.yml
scrape_configs:
......
  - job_name: "commands"
    # metrics_path: /   ## 指定指标暴露的 url, 使用任意 url 都可以获取到指标
    # file_sd_configs:
    #   - files:
    #   - /etc/prometheus/file_sd/commands.yaml
    static_configs:
      - targets:
        - 172.5.1.75:8100
        - 172.5.1.11:8100
    metric_relabel_configs:
      # 删除无用指标
      - source_labels:
        - __name__
        regex: "python.*|process.*"
        action: drop
```
