### **Smart Video Editing Assistant**  

An intelligent video editing tool based on Python, supporting text-driven editing and AI-assisted smart video generation. Uses the MiniCPM-o-2.6 multimodal model.  

## **Features**  

- **Text-Driven Editing**: Automatically generates videos based on input text.  
- **AI-Assisted Video Generation**: Smart video creation with AI assistance.  
- **Supports Multiple Media Formats**: Works with both images and videos.  
- **Automatic Speech Synthesis**: Supports multiple voice roles.  
- **Modern UI**: Built with PyQt5 and FluentUI.  

## **System Requirements**  

- Python 3.8+  
- Windows 10/11 operating system  
- 8GB+ RAM  
- 2GB+ available disk space  

## **Installation Steps**  

1. Clone or download the project repository.  

2. Create and activate a virtual environment (recommended):  
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```  

3. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```  

4. Configure the TTS service:  
   - Ensure the TTS service is running on port 7860 (default).  
   - Alternatively, modify `tts_server_url` in `config.json` to match the actual TTS service address.  

## **Configuration Guide**  

The following parameters can be configured in `config.json`:  

```json
{
    "context_length": 2048,      // Text context length
    "temperature": 0.7,         // Generation temperature
    "tts_server_url": "http://localhost:7860",  // TTS service address
    "voice_name": "am_adam",  // Default voice role
    "voice_speed": 1.0,        // Voice speed
    "output_path": "output"   // Output directory
}
```  

## **Usage Guide**  

1. **Launch the Application**  
   ```bash
   python main.py
   ```  

2. **Text-Driven Editing**  
   - Paste or enter text in the input area.  
   - Select an image folder.  
   - Select a video folder.  
   - Click the "Generate" button to start processing.  

3. **AI-Assisted Video Generation**  
   - Select a media folder.  
   - Set generation parameters.  
   - Click the "Generate" button.  

4. **Settings**  
   - Adjust TTS parameters in the settings panel.  
   - Configure the output directory.  
   - Choose a UI theme.  

## **Project Structure**  

```
├── config.json          # Configuration file  
├── logger.py           # Logging module  
├── main.py            # Main entry point  
├── requirements.txt    # Dependency list  
├── static/            # Static assets  
├── tests/             # Test files  
├── tts.py             # TTS module  
├── tts_factory.py     # TTS factory class  
├── video_generator.py # Video generator  
├── video_processor.py # Video processor  
└── video_strategy.py  # Video strategy module  
```  

## **Common Issues**  

1. **TTS Service Connection Failure**  
   - Check if the TTS service is running properly.  
   - Ensure `tts_server_url` in `config.json` is correctly configured.  

2. **Video Generation Failure**  
   - Check folder permissions.  
   - Ensure there is enough disk space.  
   - Review log files for detailed error messages.  

## **Logging Information**  

The system automatically logs key events, including:  
- Video processing logs  
- TTS generation logs  
- Error reports  

## **Performance Optimization**  

1. **Media Preprocessing**  
   - Use standard-format images and videos.  
   - Pre-adjust image resolutions for optimal performance.  

2. **Memory Management**  
   - For large datasets, process in batches.  
   - Clean up temporary files regularly.  

## **Development Guide**  

1. **Code Structure**  
   - Factory pattern for TTS service management.  
   - Strategy pattern for handling different media file types.  
   - MVVM architecture for UI design.  

2. **Extensibility**  
   - Add new media processors by extending `MediaProcessor`.  
   - Support additional TTS engines by modifying `tts_factory.py`.  
   - Implement new video processing strategies in `video_strategy.py`.  

## **License**  

MIT License