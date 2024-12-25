import sys
import socket
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton,
    QTextEdit, QVBoxLayout, QWidget, QFileDialog
)
from PyQt6.QtGui import QColor


class Client(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Client de Compilation")
        self.setGeometry(100, 100, 400, 350)

        self.client_socket = None  # Placeholder for the socket

        # Main layout
        layout = QVBoxLayout()

        # IP and Port inputs
        self.ip_label = QLabel("Adresse IP du serveur :")
        self.ip_input = QLineEdit("127.0.0.1")
        self.port_label = QLabel("Port du serveur :")
        self.port_input = QLineEdit("10000")

        # Connect button and status
        self.connect_button = QPushButton("Se connecter")
        self.connect_button.clicked.connect(self.connect_to_server)

        self.disconnect_button = QPushButton("Se déconnecter")
        self.disconnect_button.clicked.connect(self.disconnect_from_server)
        self.disconnect_button.setEnabled(False)

        self.connection_status = QLabel("Déconnecté")
        self.connection_status.setStyleSheet("color: red;")  # Red for disconnected

        # File selection
        self.file_label = QLabel("Programme à envoyer :")
        self.file_path = QLineEdit()
        self.browse_button = QPushButton("Parcourir")
        self.browse_button.clicked.connect(self.browse_file)

        # Send button
        self.send_button = QPushButton("Envoyer")
        self.send_button.clicked.connect(self.send_program)
        self.send_button.setEnabled(False)  # Disable until connected

        # Result display
        self.result_label = QLabel("Résultat :")
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)

        # Add widgets to the layout
        layout.addWidget(self.ip_label)
        layout.addWidget(self.ip_input)
        layout.addWidget(self.port_label)
        layout.addWidget(self.port_input)
        layout.addWidget(self.connect_button)
        layout.addWidget(self.disconnect_button)
        layout.addWidget(self.connection_status)
        layout.addWidget(self.file_label)
        layout.addWidget(self.file_path)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.send_button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.result_output)
        layout.addWidget(self.disconnect_button)

        # Set central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def connect_to_server(self):
        ip = self.ip_input.text()
        port = int(self.port_input.text())

        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((ip, port))

            # Check if the server is busy
            server_response = self.client_socket.recv(1024).decode()
            if "Occupé" in server_response:
                self.result_output.setText("Serveur occupé. Essayez une autre adresse IP ou un autre port.")
                self.connection_status.setText("Déconnecté")
                self.connection_status.setStyleSheet("color: red;")
                self.client_socket.close()
                self.client_socket = None
            else:
                self.result_output.setText("Connexion établie avec le serveur.")
                self.connection_status.setText("Connecté")
                self.connection_status.setStyleSheet("color: green;")
                self.send_button.setEnabled(True) # Enable the send button
                self.disconnect_button.setEnabled(True) 
        except Exception as e:
                self.result_output.setText(f"Erreur de connexion : {e}")
                self.connection_status.setText("Déconnecté")
                self.connection_status.setStyleSheet("color: red;")

    def disconnect_from_server(self):
        if self.client_socket:
            try:
                self.client_socket.sendall("quit".encode())  # Inform the server to close the connection
                self.client_socket.close()
                self.client_socket = None
                self.result_output.setText("Déconnecté du serveur.")
                self.connection_status.setText("Déconnecté")
                self.connection_status.setStyleSheet("color: red;")
                self.send_button.setEnabled(False)
            except Exception as e:
                self.result_output.setText(f"Erreur lors de la déconnexion : {e}")

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Choisir un fichier", "", "Code Files (*.py *.c *.cpp *.java)")
        if file_path:
            self.file_path.setText(file_path)

    def send_program(self):
        if not self.client_socket:
            self.result_output.setText("Veuillez d'abord vous connecter au serveur.")
            return

        program_path = self.file_path.text()
        try:
            with open(program_path, "r") as file:
                program_code = file.read()

            self.client_socket.sendall(program_code.encode())
            response = self.client_socket.recv(4096).decode()
            self.result_output.setText(response)

        except Exception as e:
                 self.result_output.setText(f"Erreur : {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Client()
    window.show()
    sys.exit(app.exec())

