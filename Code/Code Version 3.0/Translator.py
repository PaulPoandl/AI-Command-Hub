import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QTextEdit, QPushButton, QComboBox 
from PyQt5 import QtGui
from translate import Translator

class TranslateApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Translator')
        self.setGeometry(100, 100, 400, 300)
        icon = QtGui.QIcon("ICO Icons/Translator.ico")
        self.setWindowIcon(icon)

        self.input_text = QLineEdit(self)
        self.output_text = QTextEdit(self)
        self.translate_button = QPushButton('Translate', self)
        self.clear_button = QPushButton('Clear Output', self)
        self.input_lang_combo = QComboBox(self)
        self.output_lang_combo = QComboBox(self)

        # Language code and name pairs
        languages = {
            'en': 'English',
            'fr': 'French',
            'es': 'Spanish',
            'de': 'German',
            'it': 'Italian',
            'ja': 'Japanese',
            'ko': 'Korean',
            'zh-CN': 'Chinese (Simplified)',
            'zh-TW': 'Chinese (Traditional)',
            'ar': 'Arabic',
            'hi': 'Hindi',
            'ru': 'Russian',
            'pt': 'Portuguese',
            'nl': 'Dutch',
            'tr': 'Turkish',
            'vi': 'Vietnamese',
            'pl': 'Polish',
            'sv': 'Swedish',
            'el': 'Greek',
            'th': 'Thai',
            'uk': 'Ukrainian',
            'cs': 'Czech',
            'fi': 'Finnish',
            'da': 'Danish',
            'ro': 'Romanian',
            'hu': 'Hungarian',
            'no': 'Norwegian',
            'he': 'Hebrew',
            'id': 'Indonesian',
            'ms': 'Malay',
            'bn': 'Bengali',
            'ta': 'Tamil',
            'gu': 'Gujarati',
            'ml': 'Malayalam',
            'kn': 'Kannada',
            # Add more languages as needed
        }

        for lang_code, lang_name in languages.items():
            self.input_lang_combo.addItem(lang_name, lang_code)
            self.output_lang_combo.addItem(lang_name, lang_code)

        layout = QVBoxLayout()
        layout.addWidget(self.input_text)
        layout.addWidget(self.input_lang_combo)
        layout.addWidget(self.output_text)
        layout.addWidget(self.output_lang_combo)
        layout.addWidget(self.translate_button)
        layout.addWidget(self.clear_button)

        self.translate_button.clicked.connect(self.perform_translation)
        self.clear_button.clicked.connect(self.clear_output)

        self.setLayout(layout)

    def perform_translation(self):
        text_to_translate = self.input_text.text()
        input_lang = self.input_lang_combo.currentData()
        output_lang = self.output_lang_combo.currentData()

        # Ensure consistent capitalization for the input text
        text_to_translate = text_to_translate.lower().capitalize()

        translator = Translator(to_lang=output_lang, from_lang=input_lang)
        try:
            translated = translator.translate(text_to_translate)
            self.output_text.setPlainText(translated)
        except Exception as e:
            self.output_text.setPlainText("An error occurred during translation. Please try again.")
            print("Translation Error:", str(e))
        
    def clear_output(self):
        self.output_text.setPlainText("")  # Clear the output text

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TranslateApp()
    window.show()
    sys.exit(app.exec_())
