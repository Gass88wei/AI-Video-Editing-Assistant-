# 智能视频剪辑助手

一个基于Python的智能视频剪辑工具，支持文案驱动剪辑和智能生成剪辑功能。通过AI技术，将文字文案转化为专业视频内容，大幅提高视频制作效率。

![版本](https://img.shields.io/badge/版本-1.0.0-blue)
![Python版本](https://img.shields.io/badge/Python-3.8%2B-brightgreen)
![许可证](https://img.shields.io/badge/许可证-MIT-green)

## 功能特点

### 核心功能

- **文案驱动剪辑**：根据输入文案自动生成视频，智能匹配视觉素材
- **智能生成剪辑**：AI辅助的智能视频生成，自动分析素材主题和风格
- **多媒体素材支持**：支持多种格式的图片和视频素材
- **自动语音合成**：集成多种TTS引擎，支持多种语言和音色
- **现代化UI界面**：基于PyQt5和FluentUI的用户友好界面

### 高级特性

- **智能素材匹配**：根据文案语义自动选择合适的视觉素材
- **自动转场效果**：根据内容节奏自动添加专业转场效果
- **字幕自动生成**：基于语音内容自动生成同步字幕
- **多语言支持**：界面和语音合成支持多种语言
- **批量处理功能**：支持批量处理多个文案生成多个视频

## 系统要求

- **操作系统**：Windows 10/11
- **Python版本**：3.8+
- **内存**：8GB+ RAM
- **存储空间**：2GB+ 可用磁盘空间
- **处理器**：建议多核CPU，支持并行处理
- **显示器**：1080p分辨率以上，支持色彩校准

## 安装步骤

### 方法一：使用pip安装

```bash
# 安装智能视频剪辑助手包
pip install video-editor-assistant

# 启动应用
video-editor-assistant
```

### 方法二：从源码安装

1. 克隆或下载项目代码

```bash
git clone https://github.com/yourusername/video-editor-assistant.git
cd video-editor-assistant
```

2. 创建并激活虚拟环境（推荐）

```bash
# Windows系统
python -m venv venv
venv\Scripts\activate

# Linux/MacOS系统
python -m venv venv
source venv/bin/activate
```

3. 安装依赖包

```bash
pip install -r requirements.txt
```

4. 配置TTS服务
   - 确保TTS服务运行在本地7860端口（默认配置）
   - 或修改config.json中的tts_server配置为实际TTS服务信息

5. 启动应用

```bash
python main.py
```

## 配置说明

在`config.json`中可以配置以下参数：

```json
{
    "context_length": 2048,      // 文本上下文长度
    "temperature": 0.7,         // 生成温度
    "tts_server": {
        "type": "azure",       // TTS服务类型：azure, google, local
        "url": "https://eastus.tts.speech.microsoft.com/",  // 服务地址
        "key": "your_key_here",  // API密钥
        "region": "eastus"      // 服务区域
    },
    "voice_settings": {
        "name": "zh-CN-XiaoxiaoNeural",  // 默认语音角色
        "speed": 1.0,        // 语音速度(0.5-2.0)
        "pitch": 0,          // 音调调整(-10到10)
        "style": "general"   // 语音风格
    },
    "video_settings": {
        "resolution": "1080p",  // 输出视频分辨率
        "fps": 30,              // 帧率
        "format": "mp4"         // 输出格式
    },
    "paths": {
        "output": "output",    // 输出目录
        "temp": "temp",        // 临时文件目录
        "logs": "logs"         // 日志目录
    },
    "ui": {
        "theme": "light",      // 界面主题：light, dark, system
        "language": "zh_CN"    // 界面语言
    }
}
```

## 使用说明

### 文案驱动剪辑

1. 启动应用后，切换到"文案驱动"选项卡
2. 在文案输入区域粘贴或输入文案内容
3. 选择图片素材文件夹和视频素材文件夹
4. 配置语音参数（角色、语速等）
5. 点击"生成视频"按钮开始处理
6. 处理完成后，可以在预览窗口查看视频效果
7. 满意后点击"导出"按钮保存视频

### 智能生成剪辑

1. 切换到"智能生成"选项卡
2. 选择素材文件夹（包含图片和视频）
3. 设置视频主题和风格
4. 调整生成参数（视频时长、创造性程度等）
5. 点击"智能生成"按钮
6. 系统会先生成文案，然后根据文案生成视频
7. 在结果页面可以编辑生成的文案和预览视频
8. 点击"导出"按钮保存视频

### 高级设置

在设置界面中，您可以：

- 配置TTS服务参数
- 调整视频输出参数（分辨率、帧率等）
- 设置默认输出路径
- 选择界面主题和语言
- 配置转场效果和字幕样式

## 项目结构

```
├── config.json          # 配置文件
├── logger.py           # 日志模块
├── main.py            # 主程序入口
├── requirements.txt    # 依赖包列表
├── static/            # 静态资源
├── tests/             # 测试文件
├── tts.py             # TTS模块
├── tts_factory.py     # TTS工厂类
├── video_generator.py # 视频生成器
├── video_processor.py # 视频处理器
└── video_strategy.py  # 视频策略模式
```

## 常见问题

### 1. TTS服务连接失败

- **问题**：启动应用后提示无法连接到TTS服务
- **解决方案**：
  - 检查TTS服务是否正常运行
  - 确认config.json中的tts_server配置是否正确
  - 检查网络连接是否正常
  - 如果使用云服务，确认API密钥是否有效

### 2. 视频生成失败

- **问题**：生成过程中断或生成的视频无法播放
- **解决方案**：
  - 检查素材文件夹权限
  - 确保有足够的磁盘空间
  - 查看日志文件了解详细错误信息
  - 尝试使用较小的素材集合

### 3. 内存不足错误

- **问题**：处理大型视频时出现内存错误
- **解决方案**：
  - 关闭其他占用内存的应用
  - 减少同时处理的素材数量
  - 在config.json中调低视频分辨率
  - 升级系统内存

## 日志说明

系统会自动记录运行日志，保存在`logs`目录下：

- **app.log**：应用程序主日志，记录主要操作和状态
- **tts.log**：TTS服务相关日志，记录语音合成过程
- **video.log**：视频处理相关日志，记录视频生成过程
- **error.log**：错误信息日志，记录所有异常和错误

日志级别可在config.json中配置，支持DEBUG、INFO、WARNING、ERROR四个级别。

## 性能优化

1. 素材预处理
- 建议使用标准格式的图片和视频文件
- 图片建议预先调整到合适的分辨率

2. 内存管理
- 处理大量素材时，建议分批进行
- 及时清理临时文件

## 开发说明

1. 代码结构
- 采用工厂模式管理TTS服务
- 使用策略模式处理不同类型的媒体文件
- MVVM架构设计UI部分

2. 扩展开发
- 可以通过继承MediaProcessor添加新的媒体处理器
- 在tts_factory.py中添加新的TTS引擎支持
- 通过修改video_strategy.py添加新的视频处理策略

## 许可证

MIT License
