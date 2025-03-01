import os
from PyQt5.QtCore import QThread, pyqtSignal
import json
from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips, CompositeVideoClip, TextClip, AudioFileClip
from PIL import Image
import numpy as np
from tts import text_to_audio
import asyncio
from logger import video_logger

class VideoProcessor(QThread):
    progress_updated = pyqtSignal(int)
    error_occurred = pyqtSignal(str)
    processing_status = pyqtSignal(str)
    generation_finished = pyqtSignal(str)
    
    def __init__(self, script, image_path, video_path):
        super().__init__()
        self.script = script
        self.image_path = image_path
        self.video_path = video_path
        self.is_running = False
        self.output_path = 'output'
        self.load_config()
        self.voice_name = 'am_adam'
        self.voice_speed = 1.0
        self.memory_manager = MemoryManager()
        video_logger.info('VideoProcessor initialized with script length: %d', len(script))
    
    def load_config(self):
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                self.config = json.load(f)
                video_logger.info('Configuration loaded successfully')
        except Exception as e:
            video_logger.error('Failed to load config: %s', str(e))
            self.config = {
                'context_length': 2048,
                'temperature': 0.7
            }
    
    def process_images(self):
        self.processing_status.emit('正在处理图片素材...')
        image_clips = []
        
        for root, _, files in os.walk(self.image_path):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    img_path = os.path.join(root, file)
                    try:
                        img = Image.open(img_path)
                        img_array = np.array(img)
                        clip = ImageClip(img_array).set_duration(3)  # 设置每张图片显示3秒
                        image_clips.append(clip)
                        video_logger.debug('Processed image: %s', file)
                    except Exception as e:
                        video_logger.error('Error processing image %s: %s', file, str(e))
        
        video_logger.info('Processed %d images', len(image_clips))
        return image_clips
    
    def process_videos(self):
        self.processing_status.emit('正在处理视频素材...')
        video_clips = []
        
        for root, _, files in os.walk(self.video_path):
            for file in files:
                if file.lower().endswith(('.mp4', '.avi', '.mov')):
                    video_path = os.path.join(root, file)
                    try:
                        # 检查内存使用情况
                        if not self.memory_manager.check_memory_usage():
                            self.processing_status.emit('内存不足，正在清理...')
                            continue
                            
                        # 大文件分块处理
                        chunks = self.memory_manager.split_large_file(video_path)
                        if not chunks:
                            video_logger.error('Failed to process video: %s', file)
                            continue
                            
                        for chunk in chunks:
                            clip = VideoFileClip(chunk)
                            video_clips.append(clip)
                            if chunk != video_path:  # 如果是临时分块文件
                                self.memory_manager.register_temp_file(chunk)
                                
                        video_logger.debug('Processed video: %s', file)
                    except Exception as e:
                        video_logger.error('Error processing video %s: %s', file, str(e))
                        continue
        
        video_logger.info('Processed %d videos', len(video_clips))
        return video_clips
    
    def run(self):
        try:
            video_logger.info('Starting video processing')
            self.is_running = True
            self.progress_updated.emit(10)
            
            # 检查路径是否存在
            if not os.path.exists(self.image_path):
                video_logger.error('Image directory does not exist: %s', self.image_path)
                raise Exception('图片文件夹不存在')
            if not os.path.exists(self.video_path):
                video_logger.error('Video directory does not exist: %s', self.video_path)
                raise Exception('视频文件夹不存在')
            
            # 确保输出目录存在
            os.makedirs(self.output_path, exist_ok=True)
            video_logger.info('Output directory created: %s', self.output_path)
            
            # 处理图片和视频素材
            image_clips = self.process_images()
            self.progress_updated.emit(40)
            
            video_clips = self.process_videos()
            self.progress_updated.emit(70)
            
            # 生成语音
            self.processing_status.emit('正在生成语音...')
            audio_file = os.path.join(self.output_path, 'temp_audio.wav')
            video_logger.info('Generating audio file: %s', audio_file)
            success = asyncio.run(text_to_audio(self.script, self.voice_name, self.voice_speed, audio_file))
            if not success:
                video_logger.error('Audio generation failed')
                raise Exception('语音生成失败')
            
            # 合并所有素材
            self.processing_status.emit('正在合成最终视频...')
            video_logger.info('Starting final video composition')
            final_clips = image_clips + video_clips
            if not final_clips:
                raise Exception('没有找到可用的素材')
            
            final_video = concatenate_videoclips(final_clips)
            
            # 添加字幕
            txt_clip = TextClip(self.script, fontsize=24, color='white')
            txt_clip = txt_clip.set_pos('center').set_duration(final_video.duration)
            
            # 添加音频
            audio_clip = AudioFileClip(audio_file)
            
            # 合成最终视频
            final_video = CompositeVideoClip([final_video, txt_clip])
            final_video = final_video.set_audio(audio_clip)
            
            # 导出最终视频
            output_file = os.path.join(self.output_path, 'final_video.mp4')
            final_video.write_videofile(
                output_file,
                fps=24,
                codec='libx264',
                audio_codec='aac'
            )
            
            # 清理资源
            final_video.close()
            for clip in final_clips:
                clip.close()
            
            self.progress_updated.emit(100)
            self.generation_finished.emit(f'视频生成完成！\n保存路径：{output_file}')
            
        except Exception as e:
            video_logger.error('Error during video processing: %s', str(e))
            self.error_occurred.emit(str(e))
        finally:
            self.is_running = False
            video_logger.info('Video processing completed')
    
    def stop(self):
        self.is_running = False