# encoding: utf-8

"""
    @Author
        noise131
    @Desc
        prometheus 系统命令执行导出器 command-exporter
        全局配置类
            :class GlobalConfig: 全局配置类
    @Date
        2022-09-12 15:13:21
    @Ver
        v1.0
    @PyVer
        3.10.x (3.10.5)
    @Github
        https://github.com/noise131
"""

import logging


class GlobalConfig():
    yaml_config_path: str = './commands.yaml'
    metrics_name = 'commands_exec_status'
    metric_describe = '命令执行指标'
    default_port = 8100
    default_interval = 30
logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)
log_sh = logging.StreamHandler()
logger.addHandler(log_sh)
log_format = logging.Formatter(fmt=r'%(asctime)s - [%(levelname)s] - %(name)s - %(process)s - %(thread)s - %(funcName)s - %(message)s')
log_sh.setFormatter(log_format)
logger.info('程序导入配置完成')
