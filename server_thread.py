from socket import *
import socket
import threading
import logging
from datetime import datetime

# Konfigurasi logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)

    def run(self):
        while True:
            try:
                data = self.connection.recv(1024)
                if data:
                    if not data.endswith(b'\r\n'):
                        self.connection.sendall(b"ERROR: Format tidak valid.\r\n")
                        continue

                    try:
                        request = data.decode('utf-8', errors='ignore').strip()
                    except Exception as e:
                        logging.warning(f"Gagal mendekode data dari {self.address}: {e}")
                        continue

                    if request == "TIME":
                        logging.info(f"Menerima request TIME dari {self.address}")
                        now = datetime.now()
                        formatted_time = now.strftime("%H:%M:%S")
                        response = f"JAM {formatted_time}\r\n"
                        self.connection.sendall(response.encode('utf-8'))

                    elif request == "QUIT":
                        logging.info(f"Menerima request QUIT dari {self.address}. Menutup koneksi.")
                        break

                    else:
                        logging.warning(f"Perintah tidak dikenal dari {self.address}: {request}")
                        response = "ERROR: Perintah tidak dikenali.\r\n"
                        self.connection.sendall(response.encode('utf-8'))
                else:
                    logging.info(f"Koneksi ditutup oleh {self.address}")
                    break

            except Exception as e:
                logging.error(f"Terjadi error pada koneksi dengan {self.address}: {e}")
                break

        self.connection.close()

class Server(threading.Thread):
    def __init__(self, port):
        self.the_clients = []
        self.port = port
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        threading.Thread.__init__(self)

    def run(self):
        self.my_socket.bind(('0.0.0.0', self.port))
        self.my_socket.listen(5)
        logging.info(f"Server berjalan di port {self.port}")

        while True:
            try:
                self.connection, self.client_address = self.my_socket.accept()
                logging.info(f"Koneksi diterima dari {self.client_address}")
                clt = ProcessTheClient(self.connection, self.client_address)
                clt.start()
                self.the_clients.append(clt)
            except KeyboardInterrupt:
                logging.info("Server dihentikan secara manual.")
                break
            except Exception as e:
                logging.error(f"Error saat menerima koneksi: {e}")

def main():
    svr = Server(45000)
    svr.start()

if __name__ == "__main__":
    main()
