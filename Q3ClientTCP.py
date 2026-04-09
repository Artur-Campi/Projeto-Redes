import socket
import threading


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 26000


def receive_messages(sock: socket.socket) -> None:
    buffer = ""
    try:
        while True:
            data = sock.recv(1024)
            if not data:
                print("\nConexao encerrada pelo servidor.")
                break
            buffer += data.decode("utf-8")
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                if line.strip():
                    print(f"\n{line.strip()}")
    except (ConnectionError, OSError):
        print("\nFalha na recepcao de mensagens.")


def main() -> None:
    host = input(f"IP do servidor [{DEFAULT_HOST}]: ").strip() or DEFAULT_HOST
    port_text = input(f"Porta do servidor [{DEFAULT_PORT}]: ").strip()
    port = int(port_text) if port_text else DEFAULT_PORT

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
    except ConnectionRefusedError:
        print(f"Nao foi possivel conectar em {host}:{port}.")
        print("Verifique se o servidor foi iniciado antes do cliente e se a porta esta correta.")
        client_socket.close()
        return
    except OSError as exc:
        print(f"Erro ao conectar: {exc}")
        client_socket.close()
        return

    receiver = threading.Thread(target=receive_messages, args=(client_socket,), daemon=True)
    receiver.start()

    print("Cliente da sala inteligente conectado.")
    print("Comandos: HELP, ESTADO, USUARIOS, LIGAR lampada, DESLIGAR ventilador, ABRIR porta, FECHAR porta, SAIR")

    try:
        while True:
            command = input("> ").strip()
            if not command:
                continue

            client_socket.sendall(f"{command}\n".encode("utf-8"))
            if command.upper() == "SAIR":
                break
    except KeyboardInterrupt:
        client_socket.sendall(b"SAIR\n")
    finally:
        client_socket.close()


if __name__ == "__main__":
    main()
