import socket
import threading
import time

#settings
IP = "127.0.0.1"  #Localhost broadcast
BROADCAST_PORT = 7500  #Port for broadcasting
RECEIVE_PORT = 7501  #Port where receiver listens

def udp_receiver():
    """Here to receive UDP messages on port 7501."""
    recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    recv_socket.bind((IP, RECEIVE_PORT))
    
    print(f"Receiver listening on {IP}:{RECEIVE_PORT}...")

    while True:
        data, addr = recv_socket.recvfrom(1024)  #Buffer size= 1024 bytes
        message = data.decode()
        print(f"Received message: {message} from {addr}")

def udp_sender(equipment_id):
    """Send UDP message directly to 7501"""
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = str(equipment_id)
    send_socket.sendto(message.encode(), (IP, RECEIVE_PORT))  #sending to receiver
    print(f"Sent equipment ID: {message} to {IP}:{RECEIVE_PORT}")

def start_services():
    """Start receiver thread"""
    threading.Thread(target=udp_receiver, daemon=True).start()
    print("Receiver started")

if __name__ == "__main__":
    start_services()
    
    # Wait for messages to be processed before script exits
    time.sleep(200)
