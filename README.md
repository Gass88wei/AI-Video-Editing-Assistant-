# 智能视频剪辑助手

一个基于Python的智能视频剪辑工具，支持文案驱动剪辑和智能生成剪辑功能。模型MiniCPM-o-2.6多模态

## 功能特点

- 文案驱动剪辑：根据输入文案自动生成视频
- 智能生成剪辑：AI辅助的智能视频生成
- 支持多种媒体素材：图片和视频
- 自动语音合成：支持多种语音角色
- 现代化UI界面：基于PyQt5和FluentUI的用户界面

## 系统要求

- Python 3.8+
- Windows 10/11 操作系统
- 8GB+ RAM
- 2GB+ 可用磁盘空间

## 安装步骤

1. 克隆或下载项目代码

2. 创建并激活虚拟环境（推荐）
```bash
python -m venv venv
venv\Scripts\activate
```

3. 安装依赖包
```bash
pip install -r requirements.txt
```

4. 配置TTS服务
- 确保TTS服务运行在本地7860端口（默认配置）
- 或修改config.json中的tts_server_url为实际TTS服务地址

## 配置说明

在config.json中可以配置以下参数：

```json
{
    "context_length": 2048,      // 文本上下文长度
    "temperature": 0.7,         // 生成温度
    "tts_server_url": "http://localhost:7860",  // TTS服务地址
    "voice_name": "am_adam",  // 默认语音角色
    "voice_speed": 1.0,        // 语音速度
    "output_path": "output"   // 输出目录
}
```

## 使用说明

1. 启动应用
```bash
python main.py
```

2. 文案驱动剪辑
- 在文案输入区域粘贴或输入文案内容
- 选择图片素材文件夹
- 选择视频素材文件夹
- 点击生成按钮开始处理

3. 智能生成剪辑
- 选择素材文件夹
- 设置生成参数
- 点击生成按钮

4. 设置
- 可以在设置界面调整TTS参数
- 配置输出路径
- 选择界面主题

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

1. TTS服务连接失败
- 检查TTS服务是否正常运行
- 确认config.json中的tts_server_url配置是否正确

2. 视频生成失败
- 检查素材文件夹权限
- 确保有足够的磁盘空间
- 查看日志文件了解详细错误信息

## 日志说明

系统会自动记录运行日志，包括：
- 视频处理日志
- TTS生成日志
- 错误信息

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
