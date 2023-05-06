import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QTextEdit, QVBoxLayout, QHBoxLayout, QCheckBox


class WebhookControlPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.url_label = QLabel('Webhook URL:', self)
        self.url_edit = QLineEdit(self)
        self.url_edit.setMinimumWidth(300)

        self.name_label = QLabel('Webhook Name:', self)
        self.name_edit = QLineEdit(self)
        self.name_edit.setMinimumWidth(300)

        self.message_label = QLabel('Message:', self)
        self.message_edit = QTextEdit(self)

        self.embed_check = QCheckBox('Send as Embed', self)
        self.embed_name_label = QLabel('Embed Name:', self)
        self.embed_name_edit = QLineEdit(self)
        self.embed_name_edit.setMaximumWidth(200)
        self.embed_name_label.setVisible(False)
        self.embed_name_edit.setVisible(False)

        self.send_button = QPushButton('Send Message', self)
        self.quit_button = QPushButton('Quit', self)

        url_layout = QHBoxLayout()
        url_layout.addWidget(self.url_label)
        url_layout.addWidget(self.url_edit)

        name_layout = QHBoxLayout()
        name_layout.addWidget(self.name_label)
        name_layout.addWidget(self.name_edit)

        message_layout = QVBoxLayout()
        message_layout.addWidget(self.message_label)
        message_layout.addWidget(self.message_edit)
        message_layout.addWidget(self.embed_check)
        embed_name_layout = QHBoxLayout()
        embed_name_layout.addWidget(self.embed_name_label)
        embed_name_layout.addWidget(self.embed_name_edit)
        message_layout.addLayout(embed_name_layout)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.send_button)
        button_layout.addWidget(self.quit_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(url_layout)
        main_layout.addLayout(name_layout)
        main_layout.addLayout(message_layout)
        main_layout.addLayout(button_layout)

        self.send_button.clicked.connect(self.send_message)
        self.quit_button.clicked.connect(self.quit_app)
        self.embed_check.stateChanged.connect(self.toggle_embed_name_input)

        self.setLayout(main_layout)
        self.setWindowTitle('Webhook Control Panel')
        self.show()

    def send_message(self):
        url = self.url_edit.text()
        name = self.name_edit.text()
        message = self.message_edit.toPlainText()
        embed = self.embed_check.isChecked()
        embed_name = self.embed_name_edit.text() if embed else ''

        if embed:
            data = {
                'embeds': [
                    {
                        'title': embed_name,
                        'description': message
                    }
                ]
            }
        else:
            data = {'content': message}

        if name:
            data['username'] = name

        response = requests.post(url, json=data)

        if response.status_code == 204:
            print('Message sent successfully.')
        else:
            print(f'Error sending message: {response.status_code} {response.reason}')

    def quit_app(self):
        QApplication.quit()

    def toggle_embed_name_input(self, state):
        if state == 2:
            self.embed_name_label.setVisible(True)
            self.embed_name_edit.setVisible(True)
        else:
            self.embed_name_label.setVisible(False)
            self.embed_name_edit.setVisible(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WebhookControlPanel()
    sys.exit(app.exec_())
