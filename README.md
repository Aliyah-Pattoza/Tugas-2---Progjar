# Time Server

Time server sederhana yang menggunakan TCP socket dengan dukungan multithreading untuk melayani multiple client secara bersamaan.

## Fitur

- **Port**: 45000 (TCP)
- **Protocol**: Custom time protocol
- **Concurrent**: Mendukung multiple client
- **Format Waktu**: hh:mm:ss (24-jam)

## Cara Menjalankan

```bash
python time_server.py
```

Server akan berjalan di port 45000 dan siap menerima koneksi.

## Protocol

### Request Format
- `TIME\r\n` - Meminta waktu saat ini
- `QUIT\r\n` - Menutup koneksi

### Response Format
- `JAM hh:mm:ss\r\n` - Response waktu
- `ERROR: ...\r\n` - Response error

## Testing

### Menggunakan Telnet
```bash
telnet localhost 45000
TIME
QUIT
```

### Menggunakan Netcat
```bash
echo "TIME" | nc localhost 45000
```

### Menggunakan Python
```python
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 45000))
client.send(b"TIME\r\n")
response = client.recv(1024)
print(response.decode('utf-8'))
client.send(b"QUIT\r\n")
client.close()
```

## Log Output

![Screenshot 2025-06-23 214101](https://github.com/user-attachments/assets/5c97e5b2-c2f8-4ceb-8ba7-497bdcda1099)

## Author

Program ini dibuat untuk memenuhi tugas pemrograman jaringan.
