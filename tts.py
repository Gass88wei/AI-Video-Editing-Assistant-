from gradio_client import Client
import asyncio
import os
from logger import tts_logger

voice_list = ["am_puck", "af_bella", "am_adam"]

async def text_to_audio(text, voice_name, speed, output_file):
    try:
        tts_logger.info('Starting TTS generation with voice: %s', voice_name)
        client = Client(os.getenv("TTS_SERVER_URL", "http://localhost:7860/"))
        
        tts_logger.debug('Sending TTS request with text length: %d', len(text))
        result = client.predict(
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
        tts_logger.error('TTS generation failed: %s', str(e))
        return False