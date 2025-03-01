from abc import ABC, abstractmethod
from gradio_client import Client
import os
from logger import tts_logger

class TTSProvider(ABC):
    @abstractmethod
    async def generate_speech(self, text: str, voice_name: str, speed: float, output_file: str) -> bool:
        pass

class GradioTTSProvider(TTSProvider):
    def __init__(self, server_url: str = None):
        self.server_url = server_url or os.getenv("TTS_SERVER_URL", "http://localhost:7860/")
        self.client = Client(self.server_url)
    
    async def generate_speech(self, text: str, voice_name: str, speed: float, output_file: str) -> bool:
        try:
            tts_logger.info('Starting Gradio TTS generation with voice: %s', voice_name)
            tts_logger.debug('Sending TTS request with text length: %d', len(text))
            
            result = self.client.predict(
                text=text,
                voice=voice_name,
                speed=speed,
                api_name="/generate_speech"
            )
            
            progress, audio_path = result
            tts_logger.debug('TTS generation completed, saving to file: %s', output_file)
            
            with open(audio_path, "rb") as f:
                audio_data = f.read()
            with open(output_file, "wb") as out:
                out.write(audio_data)
            
            tts_logger.info('Audio file saved successfully')
            return True
        except Exception as e:
            tts_logger.error('Gradio TTS generation failed: %s', str(e))
            return False

class LocalTTSProvider(TTSProvider):
    async def generate_speech(self, text: str, voice_name: str, speed: float, output_file: str) -> bool:
        try:
            # 这里实现本地TTS逻辑
            tts_logger.info('Starting Local TTS generation')
            return True
        except Exception as e:
            tts_logger.error('Local TTS generation failed: %s', str(e))
            return False

class TTSFactory:
    _providers = {
        'gradio': GradioTTSProvider,
        'local': LocalTTSProvider
    }
    
    @classmethod
    def create_provider(cls, provider_type: str, **kwargs) -> TTSProvider:
        provider_class = cls._providers.get(provider_type)
        if not provider_class:
            raise ValueError(f'Unknown TTS provider type: {provider_type}')
        return provider_class(**kwargs)

# 支持的语音列表
voice_list = ["am_puck", "af_bella", "am_adam"]