from abc import ABC, abstractmethod
from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips, CompositeVideoClip, TextClip, AudioFileClip
from PIL import Image
import numpy as np
import os
from logger import video_logger
from typing import List, Tuple

class MediaProcessor(ABC):
    @abstractmethod
    def process(self, path: str) -> List[VideoFileClip]:
        pass

class ImageProcessor(MediaProcessor):
    def __init__(self, duration: float = 3.0):
        self.duration = duration
    
    def process(self, path: str) -> List[VideoFileClip]:
        image_clips = []
        for root, _, files in os.walk(path):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    try:
                        img_path = os.path.join(root, file)
                        img = Image.open(img_path)
                        img_array = np.array(img)
                        clip = ImageClip(img_array).set_duration(self.duration)
                        image_clips.append(clip)
                        video_logger.debug('Processed image: %s', file)
                    except Exception as e:
                        video_logger.error('Error processing image %s: %s', file, str(e))
        return image_clips

class VideoProcessor(MediaProcessor):
    def process(self, path: str) -> List[VideoFileClip]:
        video_clips = []
        for root, _, files in os.walk(path):
            for file in files:
                if file.lower().endswith(('.mp4', '.avi', '.mov')):
                    try:
                        video_path = os.path.join(root, file)
                        clip = VideoFileClip(video_path)
                        video_clips.append(clip)
                        video_logger.debug('Processed video: %s', file)
                    except Exception as e:
                        video_logger.error('Error processing video %s: %s', file, str(e))
        return video_clips

class SubtitleGenerator:
    def generate(self, text: str, duration: float) -> TextClip:
        return TextClip(text, fontsize=24, color='white')\
               .set_pos('center')\
               .set_duration(duration)

class VideoComposer:
    def __init__(self, output_path: str = 'output'):
        self.output_path = output_path
        os.makedirs(output_path, exist_ok=True)
    
    def compose(self, clips: List[VideoFileClip], subtitle: TextClip, audio_path: str) -> Tuple[str, bool]:
        try:
            if not clips:
                raise ValueError('No media clips available')
            
            # 合并视频片段
            final_video = concatenate_videoclips(clips)
            
            # 添加音频
            audio_clip = AudioFileClip(audio_path)
            
            # 合成最终视频
            final_video = CompositeVideoClip([final_video, subtitle])
            final_video = final_video.set_audio(audio_clip)
            
            # 导出视频
            output_file = os.path.join(self.output_path, 'final_video.mp4')
            final_video.write_videofile(
                output_file,
                fps=24,
                codec='libx264',
                audio_codec='aac'
            )
            
            # 清理资源
            final_video.close()
            for clip in clips:
                clip.close()
            
            return output_file, True
        except Exception as e:
            video_logger.error('Error during video composition: %s', str(e))
            return '', False