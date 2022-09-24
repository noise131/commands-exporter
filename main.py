# encoding: utf-8

"""
    @Author
        noise131
    @Desc
        prometheus 系统命令执行导出器 command-exporter
        主程序
            执行系统命令, 将返回值作为指标导出
            :metrics: "commands_exec_status"
            :label item: 指标的 item
            :label command: 指标执行的系统命令
            :label describe: 指定命令指标的描述
    @Date
        2022-09-12 15:09:32
    @Ver
        v1.0
    @PyVer
        3.10.x (3.10.5)
    @Github
        https://github.com/noise131
"""

import logging
import os
import sys
import time
from GlobalConfig import GlobalConfig
from ToolsClass import YamlHandle, MetricItem, str_to_int
from threading import Thread
from prometheus_client import start_http_server, Gauge


logger = logging.getLogger('logger.main')
os.chdir(os.path.dirname(sys.argv[0]))


if __name__ == '__main__':
    yaml_config = YamlHandle(GlobalConfig.yaml_config_path)
    port = yaml_config.get_content[0].get('port')
    if not port:
        port = GlobalConfig.default_port
    port = str_to_int(port, '获取端口号出现异常')
    interval = yaml_config.get_content[0].get('interval')
    if not interval:
        interval = GlobalConfig.default_interval
    interval = str_to_int(interval, '获取间隔时间出现异常')
    start_http_server(port)
    metrics_gauge = Gauge(GlobalConfig.metrics_name, GlobalConfig.metric_describe, ['item', 'command', 'describe'])
    metrics_list = []
    try:
        for i in yaml_config.get_content[0].get('commands'):
            if not (i.get('item') and i.get('command')):
                raise Exception('命令配置中 \'item\' 或 \'command\' 字段不能为空')
            # print('"{}" "{}" "{}"'.format(i.get('item'), i.get('command'), i.get('describe')))
            if not i.get('describe'):
                i['describe'] = 'This metrics is not describe.'
            metrics_list.append(MetricItem(i.get('item'), i.get('command'), i.get('describe'), metrics_gauge))
    except Exception as e:
        logger.error('处理命令配置时出现异常 : {}'.format(str(e)))
        raise
    metrics: MetricItem
    m_t: Thread
    while True:
        metrics_thread_list = []
        for metrics in metrics_list:
            metrics_thread_list.append(Thread(target=metrics.command_exec))
        for m_t in metrics_thread_list:
            m_t.start()
        for m_t in metrics_thread_list:
            m_t.join()
        time.sleep(interval)
