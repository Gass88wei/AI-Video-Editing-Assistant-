from PyQt5.QtCore import QThread, pyqtSignal
import json
import os
from tts_factory import TTSFactory
from video_strategy import ImageProcessor, VideoProcessor, SubtitleGenerator, VideoComposer
from logger import video_logger

class VideoGenerator(QThread):
    progress_updated = pyqtSignal(int)
    error_occurred = pyqtSignal(str)
    processing_status = pyqtSignal(str)
    generation_finished = pyqtSignal(str)
    
    def __init__(self, script: str, image_path: str, video_path: str):
        super().__init__()
        self.script = script
        self.image_path = image_path
        self.video_path = video_path
        self.is_running = False
        self.output_path = 'output'
        self.load_config()
        
        # 初始化处理器
        self.image_processor = ImageProcessor()
        self.video_processor = VideoProcessor()
        self.subtitle_generator = SubtitleGenerator()
        self.video_composer = VideoComposer(self.output_path)
        
        video_logger.info('VideoGenerator initialized with script length: %d', len(script))
    
    def load_config(self):
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                self.config = json.load(f)
                self.tts_provider = TTSFactory.create_provider(
                    self.config.get('voice_mode', 'gradio').lower(),
                    server_url=self.config.get('api_url')
                )
                self.voice_name = self.config.get('voice_type', 'am_adam')
                self.voice_speed = float(self.config.get('voice_speed', 1.0))
                video_logger.info('Configuration loaded successfully')
        except Exception as e:
            video_logger.error('Failed to load config: %s', str(e))
            self.config = {}
            self.tts_provider = TTSFactory.create_provider('gradio')
            self.voice_name = 'am_adam'
            self.voice_speed = 1.0
    
    def run(self):
        try:
            video_logger.info('Starting video generation')
            self.is_running = True
            self.progress_updated.emit(10)
            
            # 检查路径是否存在
            if not os.path.exists(self.image_path):
                video_logger.error('Image directory does not exist: %s', self.image_path)
                raise Exception('图片文件夹不存在')
            if not os.path.exists(self.video_path):
                video_logger.error('Video directory does not exist: %s', self.video_path)
                raise Exception('视频文件夹不存在')
            
            # 处理图片和视频素材
            self.processing_status.emit('正在处理图片素材...')
            image_clips = self.image_processor.process(self.image_path)
            self.progress_updated.emit(40)
            
            self.processing_status.emit('正在处理视频素材...')
            video_clips = self.video_processor.process(self.video_path)
            self.progress_updated.emit(70)
            
            # 生成语音
            self.processing_status.emit('正在生成语音...')
            audio_file = os.path.join(self.output_path, 'temp_audio.wav')
            video_logger.info('Generating audio file: %s', audio_file)
            success = await self.tts_provider.generate_speech(
                self.script,
                self.voice_name,
                self.voice_speed,
                audio_file
            )
            if not success:
                video_logger.error('Audio generation failed')
                raise Exception('语音生成失败')
            
            # 生成字幕
            self.processing_status.emit('正在生成字幕...')
            clips = image_clips + video_clips
            total_duration = sum(clip.duration for clip in clips)
            subtitle = self.subtitle_generator.generate(self.script, total_duration)
            
            # 合成视频
            self.processing_status.emit('正在合成最终视频...')
            output_file, success = self.video_composer.compose(clips, subtitle, audio_file)
            
            if not success:
                raise Exception('视频合成失败')
            
            self.progress_updated.emit(100)
            self.generation_finished.emit(f'视频生成完成！\n保存路径：{output_file}')
            
        except Exception as e:
            video_logger.error('Error during video generation: %s', str(e))
            self.error_occurred.emit(str(e))
        finally:
            self.is_running = False
            video_logger.info('Video generation completed')
    
    def stop(self):
        self.is_running = False