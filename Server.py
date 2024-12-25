import socket
import subprocess
import sys
import threading
import os
import tempfile

class SimpleServer:
    def __init__(self, port):
        self.port = port
        self.is_busy = False
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("0.0.0.0", self.port))
        self.server_socket.listen(1)
        self.clients = []  # List to keep track of connected clients
        print(f"Serveur démarré sur le port {self.port}")
        print("Serveur en attente de connexions...")

    def detect_language(self, program):
        if "#include" in program:
            return "c" if ".h" in program else "cpp"
        elif "public class" in program:
            return "java"
        else:
            return "python"

    def handle_client(self, client_socket, addr):
        print(f"Client connecté : {addr}")
        self.clients.append(client_socket)

        if self.is_busy:
            print("Client rejeté : serveur occupé")
            client_socket.send("Occupé, veuillez essayer un autre serveur.".encode())
            client_socket.close()
            self.clients.remove(client_socket)
            return

        self.is_busy = True
        try:
            client_socket.send("Connecté au serveur. Envoyez votre programme.".encode())

            while True:
                program = client_socket.recv(4096).decode()
                if program.strip().lower() == "quit":
                    print(f"Client {addr} a fermé la connexion.")
                    break

                if not program:
                    raise ValueError("Aucun programme reçu")

                language = self.detect_language(program)
                print(f"Detected language: {language}")

                with tempfile.TemporaryDirectory() as temp_dir:
                    if language in ["c", "cpp"]:
                        file_ext = "c" if language == "c" else "cpp"
                        source_file = os.path.join(temp_dir, f"program.{file_ext}")
                        binary_file = os.path.join(temp_dir, "program")
                        with open(source_file, "w") as file:
                            file.write(program)

                        compiler = "gcc" if language == "c" else "g++"
                        compile_process = subprocess.run([compiler, source_file, "-o", binary_file],
                                                         capture_output=True, text=True, timeout=10)
                        if compile_process.returncode != 0:
                            output = compile_process.stderr
                        else:
                            exec_process = subprocess.run([binary_file], capture_output=True, text=True, timeout=10)
                            output = exec_process.stdout if exec_process.returncode == 0 else exec_process.stderr

                    elif language == "java":
                        class_name = None
                        for line in program.splitlines():
                            if line.strip().startswith("public class"):
                                class_name = line.split()[2]
                                break

                        if not class_name:
                            raise ValueError("No public class found in the Java program")

                        source_file = os.path.join(temp_dir, f"{class_name}.java")
                        with open(source_file, "w") as file:
                            file.write(program)

                        compile_process = subprocess.run(["javac", source_file], capture_output=True, text=True, timeout=10)
                        if compile_process.returncode != 0:
                            output = compile_process.stderr
                        else:
                            exec_process = subprocess.run(["java", "-cp", temp_dir, class_name],
                                                           capture_output=True, text=True, timeout=10)
                            output = exec_process.stdout if exec_process.returncode == 0 else exec_process.stderr

                    else:  # Python
                        exec_process = subprocess.run(["python3", "-c", program], capture_output=True, text=True, timeout=10)
                        output = exec_process.stdout if exec_process.returncode == 0 else exec_process.stderr

                print(f"Résultat envoyé au client {addr} :\n{output}")  # Log the result sent to the client
                client_socket.send(output.encode())

        except Exception as e:
            error_message = f"Erreur : {e}"
            print(f"Erreur envoyée au client {addr} : {error_message}")
            client_socket.send(error_message.encode())
        finally:
            self.is_busy = False
            client_socket.close()
            self.clients.remove(client_socket)
            print(f"Connexion fermée avec le client {addr}")
            print("En attente d'une nouvelle connexion...")

    def stop_server(self):
        print("Arrêt du serveur...")
        for client in self.clients:
            try:
                client.send("Le serveur a été arrêté. Déconnexion...".encode())
                client.close()
            except Exception as e:
                print(f"Erreur lors de la déconnexion du client : {e}")
        self.server_socket.close()
        print("Serveur arrêté.")

    def start(self):
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                threading.Thread(target=self.handle_client, args=(client_socket, client_address)).start()
        except KeyboardInterrupt:
            self.stop_server()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 12345
    server = SimpleServer(port)
    server.start()
