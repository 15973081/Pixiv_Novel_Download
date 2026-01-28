import logging
import sys

# 配置日志格式
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# 设置日志级别
LOG_LEVEL = logging.INFO

def setup_logging(log_level: str = "INFO"):
    """
    设置日志配置
    """
    # 获取根日志器
    root_logger = logging.getLogger()
    
    # 清除现有处理器
    root_logger.handlers = []
    
    # 设置日志级别
    level = getattr(logging, log_level.upper(), LOG_LEVEL)
    root_logger.setLevel(level)
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # 创建格式化器
    formatter = logging.Formatter(LOG_FORMAT)
    console_handler.setFormatter(formatter)
    
    # 添加处理器
    root_logger.addHandler(console_handler)

def get_logger(name: str):
    """
    获取指定名称的日志器
    """
    return logging.getLogger(name)