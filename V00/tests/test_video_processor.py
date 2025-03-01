import unittest
import os
import shutil
from video_processor import VideoProcessor
from PIL import Image
import numpy as np

class TestVideoProcessor(unittest.TestCase):
    def setUp(self):
        # 创建测试用的临时目录
        self.test_dir = 'test_data'
        self.image_dir = os.path.join(self.test_dir, 'images')
        self.video_dir = os.path.join(self.test_dir, 'videos')
        self.output_dir = os.path.join(self.test_dir, 'output')
        
        os.makedirs(self.image_dir, exist_ok=True)
        os.makedirs(self.video_dir, exist_ok=True)
        
        # 创建测试用的图片
        self.create_test_image()
        
        # 初始化VideoProcessor
        self.processor = VideoProcessor(
            script='测试文案',
            image_path=self.image_dir,
            video_path=self.video_dir
        )
        self.processor.output_path = self.output_dir
    
    def tearDown(self):
        # 清理测试数据
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def create_test_image(self):
        # 创建一个测试用的图片
        img = Image.new('RGB', (100, 100), color='red')
        img.save(os.path.join(self.image_dir, 'test.jpg'))
    
    def test_process_images(self):
        # 测试图片处理功能
        image_clips = self.processor.process_images()
        self.assertEqual(len(image_clips), 1)
        self.assertEqual(image_clips[0].duration, 3)
    
    def test_load_config(self):
        # 测试配置加载功能
        self.processor.load_config()
        self.assertIsNotNone(self.processor.config)
        self.assertIn('context_length', self.processor.config)
        self.assertIn('temperature', self.processor.config)
    
    def test_invalid_paths(self):
        # 测试无效路径处理
        processor = VideoProcessor(
            script='测试文案',
            image_path='invalid_path',
            video_path='invalid_path'
        )
        with self.assertRaises(Exception):
            processor.run()

if __name__ == '__main__':
    unittest.main()