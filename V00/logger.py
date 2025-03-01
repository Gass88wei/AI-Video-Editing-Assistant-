import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name, log_file='app.log', level=logging.INFO):
    """设置日志系统
    
    Args:
        name: 日志记录器名称
        log_file: 日志文件路径
        level: 日志级别
    
    Returns:
        logger: 配置好的日志记录器
    """
    # 创建日志目录
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, log_file)
    
    # 创建日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 创建文件处理器
    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(level)
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    # 设置日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # 添加处理器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# 创建主日志记录器
main_logger = setup_logger('main')
# 创建视频处理日志记录器
video_logger = setup_logger('video_processor', 'video_processor.log')
# 创建TTS日志记录器
tts_logger = setup_logger('tts', 'tts.log')