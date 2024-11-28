import socket
import subprocess
import sys
import threading


class SimpleServer:
    def __init__(self, port):
        self.port = port
        self.is_busy = False  # Pour vérifier si un programme est en cours d'exécution
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("0.0.0.0", self.port))
        self.server_socket.listen(1)
        print(f"Serveur démarré sur le port {self.port}")
        print("Serveur en attente de connexions...")

    def handle_client(self, client_socket, addr):
        print(f"Client connecté : {addr}")

        if self.is_busy:
            print("Client rejeté : serveur occupé")
            client_socket.send("Occupé, veuillez essayer un autre serveur.".encode())
            client_socket.close()
            return

        self.is_busy = True
        try:
            program = client_socket.recv(1024).decode()  # Réception du programme
            if not program:
                raise ValueError("Aucun programme reçu")

            # Exécution du programme
            result = subprocess.run(["python3", "-c", program], capture_output=True, text=True)
            output = result.stdout if result.returncode == 0 else result.stderr

            client_socket.send(output.encode())  # Envoi du résultat au client
        except Exception as e:
            client_socket.send(f"Erreur : {e}".encode())
        finally:
            self.is_busy = False
            client_socket.close()
            print(f"Connexion fermée avec le client {addr}")
            print("En attente d'une nouvelle connexion...")

    def start(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket, client_address)).start()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 12345
    server = SimpleServer(port)
    server.start()
