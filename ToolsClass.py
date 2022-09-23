# encoding: utf-8

"""
    @Author
        noise131
    @Desc
        prometheus 系统命令执行 exporter
        工具类
            :class YamlHandle: yaml 配置读取工具类
            :class MetricItem: 命令执行及指标更新工具类
    @Date
        2022-09-22 14:32:25
    @Ver
        v1.0
    @PyVer
        3.10.x (3.10.5)
    @Github
        https://github.com/noise131
"""

import logging
from subprocess import Popen, PIPE
from ruamel import yaml
from prometheus_client import Gauge


logger = logging.getLogger('logger.ToolsClass')


class YamlHandle():
    def __init__(self, file_path) -> None:
        self.file_path = file_path
        self.__yaml_read()

    def __yaml_read(self) -> None:
        self.__yaml_content: list = []
        with open(self.file_path) as fp:
            for i in yaml.safe_load_all(fp):
                self.__yaml_content.append(i)

    @property
    def get_content(self) -> list:
        return self.__yaml_content


class MetricItem():
    def __init__(self, item: str, command: str,
                    describe: str, metrics_gauge: Gauge) -> None:
        self.item = item
        self.command = command
        self.describe = describe
        self.__metrics_gauge = metrics_gauge

    def command_exec(self) -> None:
        r = Popen(self.command, shell=True, stdout=PIPE, stderr=PIPE)
        self.update_metrics(r.wait())
        if r.returncode != 0:
            logger.error('命令执行返回值不为 0, item: {}, command: {}, return: {}, describe: {}, stdout: {}, stderr: {}'.
                format(self.item, self.command, r.returncode, self.describe, r.stdout.readlines(), r.stderr.readlines()))
            return
        logger.info('命令执行成功, item: {}, command: {}, describe: {}'.
                        format(self.item, self.command, self.describe))

    def update_metrics(self, return_value) -> None:
        self.__metrics_gauge.labels(item=self.item, command=self.command,
                                    describe=self.describe).set(return_value)

def str_to_int(str, info: str) -> int:
    try:
        return int(str)
    except Exception as e:
        logger.error('{} : {}'.format(info, str(e)))
        raise
