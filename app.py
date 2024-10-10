from PyQt5 import QtCore, QtGui, QtWidgets
import os
import json
from revised_rsa import dosya_sifrele, dosya_coz  # RSA işlevlerinin bulunduğu dosya 

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(608, 449)
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(150, 100, 351, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.label_header = QtWidgets.QLabel(Form)
        self.label_header.setGeometry(QtCore.QRect(130, 30, 311, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_header.setFont(font)
        self.label_header.setAlignment(QtCore.Qt.AlignCenter)
        self.label_header.setObjectName("label_header")
        self.label_file_path = QtWidgets.QLabel(Form)
        self.label_file_path.setGeometry(QtCore.QRect(50, 90, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_file_path.setFont(font)
        self.label_file_path.setObjectName("label_file_path")
        self.pushButton_encrypt = QtWidgets.QPushButton(Form)
        self.pushButton_encrypt.setGeometry(QtCore.QRect(190, 150, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_encrypt.setFont(font)
        self.pushButton_encrypt.setObjectName("pushButton_encrypt")
        self.pushButton_decrypt = QtWidgets.QPushButton(Form)
        self.pushButton_decrypt.setGeometry(QtCore.QRect(300, 150, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_decrypt.setFont(font)
        self.pushButton_decrypt.setObjectName("pushButton_decrypt")
        self.pushButton_view_original = QtWidgets.QPushButton(Form)
        self.pushButton_view_original.setGeometry(QtCore.QRect(170, 250, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_view_original.setFont(font)
        self.pushButton_view_original.setObjectName("pushButton_view_original")
        self.label_view = QtWidgets.QLabel(Form)
        self.label_view.setGeometry(QtCore.QRect(60, 260, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_view.setFont(font)
        self.label_view.setObjectName("label_view")
        self.pushButton_view_encrypted_file = QtWidgets.QPushButton(Form)
        self.pushButton_view_encrypted_file.setGeometry(QtCore.QRect(170, 290, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_view_encrypted_file.setFont(font)
        self.pushButton_view_encrypted_file.setObjectName("pushButton_view_encrypted_file")
        self.pushButton_view_decrypted_file = QtWidgets.QPushButton(Form)
        self.pushButton_view_decrypted_file.setGeometry(QtCore.QRect(140, 330, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_view_decrypted_file.setFont(font)
        self.pushButton_view_decrypted_file.setObjectName("pushButton_view_decrypted_file")
        self.textEdit_file_content = QtWidgets.QTextEdit(Form)
        self.textEdit_file_content.setGeometry(QtCore.QRect(310, 200, 261, 231))
        self.textEdit_file_content.setReadOnly(True)
        self.textEdit_file_content.setObjectName("textEdit_file_content")

        # ComboBox (Açılır liste) ekle
        self.comboBox_extension = QtWidgets.QComboBox(Form)
        self.comboBox_extension.setGeometry(QtCore.QRect(150, 200, 150, 31))
        self.comboBox_extension.setObjectName("comboBox_extension")
        self.comboBox_extension.addItems(["txt", "png", "xlsx"])  # Uzantı seçeneklerini ekle

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        # Butonlara işlevleri bağla
        self.pushButton_encrypt.clicked.connect(self.encrypt_file)
        self.pushButton_decrypt.clicked.connect(self.decrypt_file)
        self.pushButton_view_original.clicked.connect(self.view_original_file)
        self.pushButton_view_encrypted_file.clicked.connect(self.view_encrypted_file)
        self.pushButton_view_decrypted_file.clicked.connect(self.view_decrypted_file)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "RSA Şifreleme Arayüzü"))
        self.label_header.setText(_translate("Form", "RSA Şifreleme Algoritması"))
        self.label_file_path.setText(_translate("Form", "Dosya Yolu : "))
        self.pushButton_encrypt.setText(_translate("Form", "Şifrele"))
        self.pushButton_decrypt.setText(_translate("Form", "Şifre Çöz"))
        self.pushButton_view_original.setText(_translate("Form", "Orjinal Dosya"))
        self.label_view.setText(_translate("Form", "Görüntüle :"))
        self.pushButton_view_encrypted_file.setText(_translate("Form", "Şifreli Dosya"))
        self.pushButton_view_decrypted_file.setText(_translate("Form", "Çözülmüş Dosya"))

    def encrypt_file(self):
        dosya_yolu = self.lineEdit.text()
        if os.path.exists(dosya_yolu):
            dosya_sifrele(dosya_yolu, "enc", "anahtarlar.json")
        else:
            self.textEdit_file_content.setPlainText("Dosya bulunamadı.")

    def decrypt_file(self):
        sifreli_dosya_yolu = "sifreli_dosya.enc"
        selected_extension = self.comboBox_extension.currentText()  # ComboBox'tan seçilen uzantıyı al
        if os.path.exists(sifreli_dosya_yolu):
            dosya_coz(sifreli_dosya_yolu, selected_extension, "anahtarlar.json")
        else:
            self.textEdit_file_content.setPlainText("Şifreli dosya bulunamadı.")

    def view_original_file(self):
        dosya_yolu = self.lineEdit.text()
        if os.path.exists(dosya_yolu):
            with open(dosya_yolu, "r") as file:
                content = file.read()
                self.textEdit_file_content.setPlainText(content)
        else:
            self.textEdit_file_content.setPlainText("Dosya bulunamadı.")

    def view_encrypted_file(self):
        sifreli_dosya_yolu = "sifreli_dosya.enc"
        if os.path.exists(sifreli_dosya_yolu):
            with open(sifreli_dosya_yolu, "r") as file:
                content = file.read()
                self.textEdit_file_content.setPlainText(content)
        else:
            self.textEdit_file_content.setPlainText("Şifreli dosya bulunamadı.")

    def view_decrypted_file(self):
        selected_extension = self.comboBox_extension.currentText()  # ComboBox'tan seçilen uzantıyı al
        cozulmus_dosya_yolu = f"cozulmus_dosya.{selected_extension}"
        if os.path.exists(cozulmus_dosya_yolu):
            with open(cozulmus_dosya_yolu, "rb") as file:  # Binary modda açıyoruz
                content = file.read().decode("latin1")  # Binary veriyi stringe çeviriyoruz
                self.textEdit_file_content.setPlainText(content)
        else:
            self.textEdit_file_content.setPlainText("Çözülmüş dosya bulunamadı.")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
