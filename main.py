import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFileDialog
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from qfluentwidgets import FluentWindow, NavigationInterface, NavigationItemPosition, FluentIcon
from qfluentwidgets import SubtitleLabel, setTheme, Theme, PushButton, LineEdit, ComboBox, ImageLabel
from qfluentwidgets import MessageBox, StateToolTip, ScrollArea, CardWidget, BodyLabel, PrimaryPushButton, ProgressBar
from video_processor_viewmodel import VideoProcessorViewModel

class AutoEditApp(FluentWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('智能视频剪辑助手')
        self.resize(900, 700)
        
        # 初始化导航栏
        self.init_navigation()
        
        # 设置主题
        setTheme(Theme.LIGHT)
        
    def init_navigation(self):
        self.navigation_interface = NavigationInterface(self, showMenuButton=True)
        self.navigation_interface.setExpandWidth(200)
        
        # 添加导航项
        self.add_sub_interface(
            interface=TextDrivenEditInterface(self),
            icon=FluentIcon.DOCUMENT,
            text='文案驱动剪辑',
            position=NavigationItemPosition.TOP
        )
        
        self.add_sub_interface(
            interface=AutoGenerateInterface(self),
            icon=FluentIcon.ROBOT,
            text='智能生成剪辑',
            position=NavigationItemPosition.TOP
        )
        
        self.add_sub_interface(
            interface=SettingsInterface(self),
            icon=FluentIcon.SETTING,
            text='设置',
            position=NavigationItemPosition.BOTTOM
        )

class TextDrivenEditInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setup_ui()
        self.processor = None
    
    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(30, 30, 30, 30)
        
        # 标题
        title = SubtitleLabel('文案驱动剪辑', self)
        self.layout.addWidget(title)
        
        # 文案输入区域
        script_card = CardWidget(self)
        script_layout = QVBoxLayout(script_card)
        script_label = BodyLabel('文案输入', self)
        self.script_edit = LineEdit(self)
        self.script_edit.setPlaceholderText('请输入或粘贴文案内容')
        script_layout.addWidget(script_label)
        script_layout.addWidget(self.script_edit)
        self.layout.addWidget(script_card)
        
        # 素材选择区域
        material_card = CardWidget(self)
        material_layout = QVBoxLayout(material_card)
        
        # 图片文件夹选择
        image_layout = QHBoxLayout()
        self.image_path_edit = LineEdit(self)
        self.image_path_edit.setPlaceholderText('选择图片文件夹')
        self.image_select_btn = PrimaryPushButton('浏览', self)
        self.image_select_btn.clicked.connect(self.select_image_folder)
        image_layout.addWidget(self.image_path_edit)
        image_layout.addWidget(self.image_select_btn)
        
        # 视频文件夹选择
        video_layout = QHBoxLayout()
        self.video_path_edit = LineEdit(self)
        self.video_path_edit.setPlaceholderText('选择视频文件夹')
        self.video_select_btn = PrimaryPushButton('浏览', self)
        self.video_select_btn.clicked.connect(self.select_video_folder)
        video_layout.addWidget(self.video_path_edit)
        video_layout.addWidget(self.video_select_btn)
        
        material_layout.addLayout(image_layout)
        material_layout.addLayout(video_layout)
        self.layout.addWidget(material_card)
        
        # 进度显示区域
        progress_card = CardWidget(self)
        progress_layout = QVBoxLayout(progress_card)
        
        # 状态标签
        self.status_label = BodyLabel('等待开始...', self)
        progress_layout.addWidget(self.status_label)
        
        # 进度条
        self.progress_bar = ProgressBar(self)
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_bar)
        
        self.layout.addWidget(progress_card)
        
        # 生成按钮
        self.generate_btn = PrimaryPushButton('开始生成', self)
        self.generate_btn.clicked.connect(self.start_generation)
        self.layout.addWidget(self.generate_btn)
        
        # 添加弹性空间
        self.layout.addStretch()
    
    def select_image_folder(self):
        folder = QFileDialog.getExistingDirectory(self, '选择图片文件夹')
        if folder:
            self.image_path_edit.setText(folder)
    
    def select_video_folder(self):
        folder = QFileDialog.getExistingDirectory(self, '选择视频文件夹')
        if folder:
            self.video_path_edit.setText(folder)
    
    def start_generation(self):
        script = self.script_edit.text()
        image_path = self.image_path_edit.text()
        video_path = self.video_path_edit.text()
        
        if not all([script, image_path, video_path]):
            MessageBox('提示', '请填写完整的文案和素材路径', self).exec_()
            return
        
        # 禁用生成按钮
        self.generate_btn.setEnabled(False)
        
        # 创建并启动处理线程
        self.processor = VideoProcessorViewModel()
        self.processor.initialize_generator(script, image_path, video_path)
        self.processor.progress_updated.connect(self.update_progress)
        self.processor.processing_status.connect(self.update_status)
        self.processor.error_occurred.connect(self.handle_error)
        self.processor.generation_finished.connect(self.handle_completion)
        self.processor.start()
    
    def update_progress(self, value):
        self.progress_bar.setValue(value)
    
    def update_status(self, status):
        self.status_label.setText(status)
    
    def handle_error(self, error_msg):
        self.generate_btn.setEnabled(True)
        MessageBox('错误', error_msg, self).exec_()
        self.status_label.setText('生成失败')
    
    def handle_completion(self, msg):
        self.generate_btn.setEnabled(True)
        MessageBox('完成', msg, self).exec_()
        self.status_label.setText('生成完成')

class AutoGenerateInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setup_ui()
        self.processor = None
    
    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(30, 30, 30, 30)
        
        # 标题
        title = SubtitleLabel('智能生成剪辑', self)
        self.layout.addWidget(title)
        
        # 素材上传区域
        material_card = CardWidget(self)
        material_layout = QVBoxLayout(material_card)
        
        # 素材文件夹选择
        material_label = BodyLabel('素材选择', self)
        material_layout.addWidget(material_label)
        
        material_path_layout = QHBoxLayout()
        self.material_path_edit = LineEdit(self)
        self.material_path_edit.setPlaceholderText('选择素材文件夹')
        self.material_select_btn = PrimaryPushButton('浏览', self)
        self.material_select_btn.clicked.connect(self.select_material_folder)
        material_path_layout.addWidget(self.material_path_edit)
        material_path_layout.addWidget(self.material_select_btn)
        material_layout.addLayout(material_path_layout)
        
        self.layout.addWidget(material_card)
        
        # 文案预览和编辑区域
        script_card = CardWidget(self)
        script_layout = QVBoxLayout(script_card)
        
        script_label = BodyLabel('智能生成文案', self)
        script_layout.addWidget(script_label)
        
        self.script_edit = LineEdit(self)
        self.script_edit.setPlaceholderText('点击生成按钮自动生成文案')
        script_layout.addWidget(self.script_edit)
        
        self.generate_script_btn = PrimaryPushButton('生成文案', self)
        self.generate_script_btn.clicked.connect(self.generate_script)
        script_layout.addWidget(self.generate_script_btn)
        
        self.layout.addWidget(script_card)
        
        # 进度显示区域
        progress_card = CardWidget(self)
        progress_layout = QVBoxLayout(progress_card)
        
        self.status_label = BodyLabel('等待开始...', self)
        progress_layout.addWidget(self.status_label)
        
        self.progress_bar = ProgressBar(self)
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_bar)
        
        self.layout.addWidget(progress_card)
        
        # 生成按钮
        self.generate_video_btn = PrimaryPushButton('开始生成视频', self)
        self.generate_video_btn.clicked.connect(self.start_generation)
        self.layout.addWidget(self.generate_video_btn)
        
        # 添加弹性空间
        self.layout.addStretch()
    
    def select_material_folder(self):
        folder = QFileDialog.getExistingDirectory(self, '选择素材文件夹')
        if folder:
            self.material_path_edit.setText(folder)
    
    def generate_script(self):
        material_path = self.material_path_edit.text()
        if not material_path:
            MessageBox('错误', '请先选择素材文件夹', self).exec_()
            return
        
        # TODO: 实现智能文案生成逻辑
        self.script_edit.setText('这是一个自动生成的示例文案')
        MessageBox('成功', '文案生成完成', self).exec_()
    
    def start_generation(self):
        material_path = self.material_path_edit.text()
        script = self.script_edit.text()
        
        if not all([material_path, script]):
            MessageBox('提示', '请确保已选择素材文件夹并生成文案', self).exec_()
            return
        
        # 禁用生成按钮
        self.generate_video_btn.setEnabled(False)
        
        # 创建并启动处理线程
        self.processor = VideoProcessorViewModel()
        self.processor.initialize_generator(script, material_path, material_path)
        self.processor.progress_updated.connect(self.update_progress)
        self.processor.processing_status.connect(self.update_status)
        self.processor.error_occurred.connect(self.handle_error)
        self.processor.generation_finished.connect(self.handle_completion)
        self.processor.start()
    
    def update_progress(self, value):
        self.progress_bar.setValue(value)
    
    def update_status(self, status):
        self.status_label.setText(status)
    
    def handle_error(self, error_msg):
        self.generate_video_btn.setEnabled(True)
        MessageBox('错误', error_msg, self).exec_()
        self.status_label.setText('生成失败')
    
    def handle_completion(self, msg):
        self.generate_video_btn.setEnabled(True)
        MessageBox('完成', msg, self).exec_()
        self.status_label.setText('生成完成')

class SettingsInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(30, 30, 30, 30)
        
        # 标题
        title = SubtitleLabel('设置', self)
        self.layout.addWidget(title)
        
        # 模型配置卡片
        model_card = CardWidget(self)
        model_layout = QVBoxLayout(model_card)
        
        # GGUF模型配置
        gguf_label = BodyLabel('GGUF模型配置', self)
        model_layout.addWidget(gguf_label)
        
        gguf_path_layout = QHBoxLayout()
        self.gguf_path_edit = LineEdit(self)
        self.gguf_path_edit.setPlaceholderText('选择GGUF模型文件路径')
        self.gguf_select_btn = PrimaryPushButton('浏览', self)
        self.gguf_select_btn.clicked.connect(self.select_gguf_model)
        gguf_path_layout.addWidget(self.gguf_path_edit)
        gguf_path_layout.addWidget(self.gguf_select_btn)
        model_layout.addLayout(gguf_path_layout)
        
        # 模型参数配置
        params_label = BodyLabel('模型参数配置', self)
        model_layout.addWidget(params_label)
        
        # 上下文长度
        context_layout = QHBoxLayout()
        context_label = BodyLabel('上下文长度:', self)
        self.context_length_edit = LineEdit(self)
        self.context_length_edit.setPlaceholderText('默认: 2048')
        context_layout.addWidget(context_label)
        context_layout.addWidget(self.context_length_edit)
        model_layout.addLayout(context_layout)
        
        # 温度参数
        temp_layout = QHBoxLayout()
        temp_label = BodyLabel('温度:', self)
        self.temperature_edit = LineEdit(self)
        self.temperature_edit.setPlaceholderText('默认: 0.7')
        temp_layout.addWidget(temp_label)
        temp_layout.addWidget(self.temperature_edit)
        model_layout.addLayout(temp_layout)
        
        # Ollama配置
        ollama_label = BodyLabel('Ollama配置', self)
        model_layout.addWidget(ollama_label)
        
        self.ollama_url_edit = LineEdit(self)
        self.ollama_url_edit.setPlaceholderText('Ollama服务器地址 (例如: http://localhost:11434)')
        model_layout.addWidget(self.ollama_url_edit)
        
        # 模型选择
        model_type_label = BodyLabel('模型类型', self)
        model_layout.addWidget(model_type_label)
        
        self.model_type_combo = ComboBox(self)
        self.model_type_combo.addItems(['GGUF本地模型', 'Ollama服务'])
        self.model_type_combo.currentTextChanged.connect(self.on_model_type_changed)
        model_layout.addWidget(self.model_type_combo)
        
        # 测试按钮
        button_layout = QHBoxLayout()
        self.test_btn = PrimaryPushButton('测试模型连接', self)
        self.test_btn.clicked.connect(self.test_model_connection)
        self.save_btn = PrimaryPushButton('保存设置', self)
        self.save_btn.clicked.connect(self.save_settings)
        button_layout.addWidget(self.test_btn)
        button_layout.addWidget(self.save_btn)
        model_layout.addLayout(button_layout)
        
        self.layout.addWidget(model_card)
        
        # 语音配置卡片
        voice_card = CardWidget(self)
        voice_layout = QVBoxLayout(voice_card)
        
        # 语音模式选择
        voice_mode_label = BodyLabel('语音模式', self)
        voice_layout.addWidget(voice_mode_label)
        
        self.voice_mode_combo = ComboBox(self)
        self.voice_mode_combo.addItems(['本地语音', '外部API'])
        self.voice_mode_combo.currentTextChanged.connect(self.on_voice_mode_changed)
        voice_layout.addWidget(self.voice_mode_combo)
        
        # API配置
        api_config_label = BodyLabel('API配置', self)
        voice_layout.addWidget(api_config_label)
        
        self.api_key_edit = LineEdit(self)
        self.api_key_edit.setPlaceholderText('API密钥')
        voice_layout.addWidget(self.api_key_edit)
        
        self.api_url_edit = LineEdit(self)
        self.api_url_edit.setPlaceholderText('API服务器地址')
        voice_layout.addWidget(self.api_url_edit)
        
        # 语音参数配置
        voice_params_label = BodyLabel('语音参数', self)
        voice_layout.addWidget(voice_params_label)
        
        # 音色选择
        voice_type_layout = QHBoxLayout()
        voice_type_label = BodyLabel('音色:', self)
        self.voice_type_combo = ComboBox(self)
        self.voice_type_combo.addItems(['标准女声', '标准男声', '温柔女声', '磁性男声'])
        voice_type_layout.addWidget(voice_type_label)
        voice_type_layout.addWidget(self.voice_type_combo)
        voice_layout.addLayout(voice_type_layout)
        
        # 语速调节
        speed_layout = QHBoxLayout()
        speed_label = BodyLabel('语速:', self)
        self.speed_edit = LineEdit(self)
        self.speed_edit.setPlaceholderText('默认: 1.0')
        speed_layout.addWidget(speed_label)
        speed_layout.addWidget(self.speed_edit)
        voice_layout.addLayout(speed_layout)
        
        # 情感程度
        emotion_layout = QHBoxLayout()
        emotion_label = BodyLabel('情感程度:', self)
        self.emotion_edit = LineEdit(self)
        self.emotion_edit.setPlaceholderText('默认: 0.5')
        emotion_layout.addWidget(emotion_label)
        emotion_layout.addWidget(self.emotion_edit)
        voice_layout.addLayout(emotion_layout)
        
        self.layout.addWidget(voice_card)
        
        # 添加弹性空间
        self.layout.addStretch()
    
    def select_gguf_model(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            '选择GGUF模型文件',
            '',
            'GGUF Files (*.gguf)'
        )
        if file_path:
            self.gguf_path_edit.setText(file_path)
    
    def on_model_type_changed(self, model_type):
        is_gguf = model_type == 'GGUF本地模型'
        self.gguf_path_edit.setEnabled(is_gguf)
        self.gguf_select_btn.setEnabled(is_gguf)
        self.ollama_url_edit.setEnabled(not is_gguf)
    
    def test_model_connection(self):
        model_type = self.model_type_combo.currentText()
        
        if model_type == 'GGUF本地模型':
            model_path = self.gguf_path_edit.text()
            if not model_path:
                MessageBox('错误', '请选择GGUF模型文件', self).exec_()
                return
            if not os.path.exists(model_path):
                MessageBox('错误', 'GGUF模型文件不存在', self).exec_()
                return
            MessageBox('成功', 'GGUF模型文件验证成功', self).exec_()
        else:
            ollama_url = self.ollama_url_edit.text()
            if not ollama_url:
                MessageBox('错误', '请输入Ollama服务器地址', self).exec_()
                return
            # TODO: 实现Ollama服务器连接测试
            MessageBox('提示', 'Ollama服务器连接测试待实现', self).exec_()
    
    def on_voice_mode_changed(self, mode):
        is_api = mode == '外部API'
        self.api_key_edit.setEnabled(is_api)
        self.api_url_edit.setEnabled(is_api)

    def save_settings(self):
        try:
            settings = {
                'model_type': self.model_type_combo.currentText(),
                'gguf_path': self.gguf_path_edit.text(),
                'ollama_url': self.ollama_url_edit.text(),
                'context_length': int(self.context_length_edit.text() or '2048'),
                'temperature': float(self.temperature_edit.text() or '0.7'),
                'voice_mode': self.voice_mode_combo.currentText(),
                'api_key': self.api_key_edit.text(),
                'api_url': self.api_url_edit.text(),
                'voice_type': self.voice_type_combo.currentText(),
                'voice_speed': float(self.speed_edit.text() or '1.0'),
                'voice_emotion': float(self.emotion_edit.text() or '0.5')
            }
            
            # 保存到配置文件
            import json
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=4)
            
            MessageBox('成功', '设置已保存', self).exec_()
        except Exception as e:
            MessageBox('错误', f'保存设置失败: {str(e)}', self).exec_()
    
    def load_settings(self):
        try:
            if os.path.exists('config.json'):
                with open('config.json', 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                
                self.model_type_combo.setCurrentText(settings.get('model_type', 'GGUF本地模型'))
                self.gguf_path_edit.setText(settings.get('gguf_path', ''))
                self.ollama_url_edit.setText(settings.get('ollama_url', ''))
                self.context_length_edit.setText(str(settings.get('context_length', '2048')))
                self.temperature_edit.setText(str(settings.get('temperature', '0.7')))
                self.voice_mode_combo.setCurrentText(settings.get('voice_mode', '本地语音'))
                self.api_key_edit.setText(settings.get('api_key', ''))
                self.api_url_edit.setText(settings.get('api_url', ''))
                self.voice_type_combo.setCurrentText(settings.get('voice_type', '标准女声'))
                self.speed_edit.setText(str(settings.get('voice_speed', '1.0')))
                self.emotion_edit.setText(str(settings.get('voice_emotion', '0.5')))
        except Exception as e:
            MessageBox('错误', f'加载设置失败: {str(e)}', self).exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AutoEditApp()
    window.show()
    sys.exit(app.exec_())