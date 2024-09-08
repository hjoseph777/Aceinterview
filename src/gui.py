# gui.py
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QTextEdit, QFileDialog
from PyQt5.QtCore import Qt
from settings import save_settings, load_settings
from openai_client import OpenAIClient
import speech_recognition as sr
import whisper
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aceinterview")
        self.setGeometry(100, 100, 600, 400)
        
        self.api_key = ""
        self.model = None
        
        self.initUI()
        self.load_settings()

    def initUI(self):
        layout = QVBoxLayout()
        
        self.api_key_input = QLineEdit(self)
        self.api_key_input.setPlaceholderText("Enter OpenAI API Key")
        layout.addWidget(self.api_key_input)
        
        self.model_select = QLineEdit(self)
        self.model_select.setPlaceholderText("Enter model type (fast, whisper, small, medium)")
        layout.addWidget(self.model_select)
        
        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_button)
        
        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start_conversation)
        layout.addWidget(self.start_button)
        
        self.output_text = QTextEdit(self)
        layout.addWidget(self.output_text)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def save_settings(self):
        self.api_key = self.api_key_input.text()
        model_type = self.model_select.text()
        
        settings = {
            "api_key": self.api_key,
            "model_type": model_type
        }
        
        save_settings(settings)
        
        if not os.path.exists(f"models/{model_type}"):
            self.download_model(model_type)
        
    def load_settings(self):
        settings = load_settings()
        self.api_key = settings.get("api_key", "")
        model_type = settings.get("model_type", "")
        
        self.api_key_input.setText(self.api_key)
        self.model_select.setText(model_type)
        
        if model_type and os.path.exists(f"models/{model_type}"):
            self.model = whisper.load_model(model_type)
        
    def download_model(self, model_type):
        self.output_text.append("Downloading model...")
        self.model = whisper.load_model(model_type)
        self.output_text.append("Model downloaded and loaded.")
        
    def start_conversation(self):
        recognizer = sr.Recognizer()
        mic = sr.Microphone()
        
        with mic as source:
            self.output_text.append("Listening...")
            audio = recognizer.listen(source)
        
        self.output_text.append("Processing...")
        text = recognizer.recognize_google(audio)
        self.output_text.append(f"User: {text}")
        
        client = OpenAIClient(self.api_key)
        response = client.fetch_response(text)
        self.output_text.append(f"AI: {response}")