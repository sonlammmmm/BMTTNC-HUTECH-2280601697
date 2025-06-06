import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.railfence import Ui_RailFenceMainWindow
import requests

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_RailFenceMainWindow()
        self.ui.setupUi(self)
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)
        
    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/railfence/encrypt"
        plain_text = self.ui.txt_plain_text.toPlainText()
        try:
            key = int(self.ui.txt_key.text())
            if key <= 1:
                QMessageBox()
                return
        except ValueError:
            QMessageBox()
            return

        payload = {
            "plain_text": plain_text,
            "key": key
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_cipher_text.setPlainText(data.get("encrypted_text", "Không có dữ liệu mã hóa"))
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Mã hóa thành công!")
                msg.setWindowTitle("Thông báo")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e.message)
    
    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/railfence/decrypt"
        cipher_text = self.ui.txt_cipher_text.toPlainText()
        try:
            key = int(self.ui.txt_key.text())
            if key <= 1:
                QMessageBox.warning(self, "Lỗi khoá", "Số rails (Key) phải là một số nguyên lớn hơn 1.")
                return
        except ValueError:
            QMessageBox.warning(self, "Lỗi khoá", "Key phải là một số nguyên hợp lệ.")
            return

        payload = {
            "cipher_text": cipher_text,
            "key": key
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_plain_text.setPlainText(data.get("decrypted_text"))
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Giải mã thành công!")
                msg.setWindowTitle("Thông báo")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e.message)
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())