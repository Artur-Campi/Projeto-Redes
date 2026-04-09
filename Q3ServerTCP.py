import socket
import threading
from datetime import datetime


DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 26000
BUFFER_SIZE = 1024


class SmartRoomServer:
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = {}
        self.lock = threading.Lock()
        self.running = True
        self.devices = {
            "lampada": "desligada",
            "ventilador": "desligado",
            "porta": "fechada",
            "alarme": "desligado",
        }

    def log(self, message: str) -> None:
        now = datetime.now().strftime("%H:%M:%S")
        print(f"[{now}] {message}")

    def format_state(self) -> str:
        with self.lock:
            snapshot = dict(self.devices)
        return " | ".join(f"{name}: {status}" for name, status in snapshot.items())

    def send_line(self, conn: socket.socket, message: str) -> None:
        conn.sendall(f"{message}\n".encode("utf-8"))

    def broadcast(self, message: str, ignore_conn: socket.socket | None = None) -> None:
        with self.lock:
            recipients = [conn for conn in self.clients if conn is not ignore_conn]

        dead_clients = []
        for conn in recipients:
            try:
                self.send_line(conn, message)
            except OSError:
                dead_clients.append(conn)

        for conn in dead_clients:
            self.remove_client(conn)

    def remove_client(self, conn: socket.socket) -> None:
        with self.lock:
            client_name = self.clients.pop(conn, None)
        try:
            conn.close()
        except OSError:
            pass

        if client_name:
            self.log(f"{client_name} saiu da sala.")
            self.broadcast(f"EVENTO {client_name} desconectou.")

    def process_command(self, conn: socket.socket, command: str) -> bool:
        command = command.strip()
        if not command:
            return True

        parts = command.split()
        action = parts[0].upper()
        args = parts[1:]
        client_name = self.clients.get(conn, "Cliente")

        if action == "HELP":
            self.send_line(
                conn,
                "COMANDOS HELP | ESTADO | USUARIOS | LIGAR <dispositivo> | DESLIGAR <dispositivo> | ABRIR porta | FECHAR porta | SAIR",
            )
            return True

        if action == "ESTADO":
            self.send_line(conn, f"ESTADO {self.format_state()}")
            return True

        if action == "USUARIOS":
            with self.lock:
                users = ", ".join(self.clients.values())
            self.send_line(conn, f"USUARIOS {users}")
            return True

        if action == "SAIR":
            self.send_line(conn, "INFO Encerrando conexao.")
            return False

        if not args:
            self.send_line(conn, "ERRO Comando incompleto. Digite HELP para ver as opcoes.")
            return True

        target = args[0].lower()
        if target not in self.devices:
            self.send_line(conn, "ERRO Dispositivo invalido. Use lampada, ventilador, porta ou alarme.")
            return True

        if action == "LIGAR":
            if target == "porta":
                self.send_line(conn, "ERRO Para porta, use ABRIR ou FECHAR.")
                return True
            with self.lock:
                self.devices[target] = "ligada" if target == "lampada" else "ligado"
        elif action == "DESLIGAR":
            if target == "porta":
                self.send_line(conn, "ERRO Para porta, use ABRIR ou FECHAR.")
                return True
            with self.lock:
                self.devices[target] = "desligada" if target == "lampada" else "desligado"
        elif action == "ABRIR" and target == "porta":
            with self.lock:
                self.devices[target] = "aberta"
        elif action == "FECHAR" and target == "porta":
            with self.lock:
                self.devices[target] = "fechada"
        else:
            self.send_line(conn, "ERRO Comando invalido para este dispositivo.")
            return True

        self.log(f"{client_name} executou: {command}")
        self.send_line(conn, f"OK Estado atualizado: {self.format_state()}")
        self.broadcast(
            f"EVENTO {client_name} alterou o ambiente. Novo estado: {self.format_state()}",
            ignore_conn=conn,
        )
        return True

    def handle_client(self, conn: socket.socket, addr: tuple[str, int]) -> None:
        file_obj = conn.makefile("r", encoding="utf-8")
        try:
            self.send_line(conn, "BEMVINDO Digite seu nome:")
            client_name = file_obj.readline().strip()
            if not client_name:
                self.send_line(conn, "ERRO Nome invalido.")
                return

            with self.lock:
                self.clients[conn] = client_name

            self.log(f"{client_name} conectado de {addr[0]}:{addr[1]}")
            self.send_line(conn, f"INFO Conexao aceita. Estado atual: {self.format_state()}")
            self.send_line(conn, "INFO Digite HELP para ver os comandos.")
            self.broadcast(f"EVENTO {client_name} entrou na sala.", ignore_conn=conn)

            while self.running:
                data = file_obj.readline()
                if not data:
                    break
                should_continue = self.process_command(conn, data)
                if not should_continue:
                    break
        except (ConnectionError, OSError):
            pass
        finally:
            try:
                file_obj.close()
            except OSError:
                pass
            self.remove_client(conn)

    def start(self) -> None:
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(10)
        self.log(f"Servidor da sala inteligente ativo em {self.host}:{self.port}")

        try:
            while self.running:
                conn, addr = self.server_socket.accept()
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(conn, addr),
                    daemon=True,
                )
                client_thread.start()
        except KeyboardInterrupt:
            self.log("Servidor encerrado manualmente.")
        finally:
            self.running = False
            with self.lock:
                active_clients = list(self.clients.keys())
            for conn in active_clients:
                self.remove_client(conn)
            self.server_socket.close()


if __name__ == "__main__":
    host = input(f"Host do servidor [{DEFAULT_HOST}]: ").strip() or DEFAULT_HOST
    port_text = input(f"Porta do servidor [{DEFAULT_PORT}]: ").strip()
    port = int(port_text) if port_text else DEFAULT_PORT
    SmartRoomServer(host, port).start()
