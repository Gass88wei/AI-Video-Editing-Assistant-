import os
import shutil
import psutil
from logger import video_logger

class MemoryManager:
    def __init__(self, temp_dir='temp', threshold_mb=1000):
        self.temp_dir = temp_dir
        self.threshold_mb = threshold_mb
        self.temp_files = set()
        os.makedirs(temp_dir, exist_ok=True)
        video_logger.info('MemoryManager initialized with temp directory: %s', temp_dir)
    
    def check_memory_usage(self):
        """检查系统内存使用情况"""
        memory = psutil.virtual_memory()
        available_mb = memory.available / (1024 * 1024)
        if available_mb < self.threshold_mb:
            video_logger.warning('Low memory warning: %d MB available', available_mb)
            self.clean_temp_files()
            return False
        return True
    
    def register_temp_file(self, file_path):
        """注册临时文件以便后续清理"""
        self.temp_files.add(file_path)
        video_logger.debug('Registered temp file: %s', file_path)
    
    def clean_temp_files(self):
        """清理所有注册的临时文件"""
        for file_path in self.temp_files.copy():
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    self.temp_files.remove(file_path)
                    video_logger.info('Cleaned temp file: %s', file_path)
            except Exception as e:
                video_logger.error('Failed to clean temp file %s: %s', file_path, str(e))
    
    def split_large_file(self, file_path, chunk_size_mb=100):
        """将大文件分割成小块处理"""
        chunk_size = chunk_size_mb * 1024 * 1024  # 转换为字节
        if not os.path.exists(file_path):
            video_logger.error('File not found: %s', file_path)
            return []
        
        file_size = os.path.getsize(file_path)
        if file_size <= chunk_size:
            return [file_path]
        
        chunks = []
        try:
            base_name = os.path.basename(file_path)
            name, ext = os.path.splitext(base_name)
            
            with open(file_path, 'rb') as f:
                chunk_num = 0
                while True:
                    chunk_data = f.read(chunk_size)
                    if not chunk_data:
                        break
                    
                    chunk_path = os.path.join(
                        self.temp_dir,
                        f'{name}_chunk_{chunk_num}{ext}'
                    )
                    with open(chunk_path, 'wb') as chunk_file:
                        chunk_file.write(chunk_data)
                    
                    chunks.append(chunk_path)
                    self.register_temp_file(chunk_path)
                    chunk_num += 1
                    video_logger.debug('Created chunk file: %s', chunk_path)
            
            video_logger.info('Split %s into %d chunks', file_path, len(chunks))
            return chunks
        except Exception as e:
            video_logger.error('Failed to split file %s: %s', file_path, str(e))
            return []
    
    def __del__(self):
        """析构时清理所有临时文件"""
        self.clean_temp_files()
        if os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
                video_logger.info('Cleaned temp directory: %s', self.temp_dir)
            except Exception as e:
                video_logger.error('Failed to clean temp directory: %s', str(e))