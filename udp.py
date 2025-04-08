import socket
import threading
import time

#settings
IP = "127.0.0.1"  #Localhost broadcast
BROADCAST_PORT = 7500  #Port for broadcasting
RECEIVE_PORT = 7501  #Port where receiver listens

tagged_callback = None

def set_tagged_callback(callback):
    global tagged_callback
    tagged_callback = callback


def udp_receiver():
    """Here to receive UDP messages on port 7501."""
    recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    recv_socket.bind((IP, RECEIVE_PORT))
    
    print(f"Receiver listening on {IP}:{RECEIVE_PORT}...")

    while True:
        data, addr = recv_socket.recvfrom(1024)
        message = data.decode()
        print(f"Received message: {message} from {addr}")

        if ':' in message:
            try:
                tagger, tagged = message.split(':')
                print(tagger + " tagged " + tagged)
                
                #Send tagged to keep traffic going
                udp_sender(tagged)

                #send to first_screen
                if tagged_callback:
                    tagged_callback(tagger, tagged)
            except ValueError:
                print("Invalid message format. Expected tagger:tagged.")

def udp_sender(equipment_id):
    """Send UDP message to 7500"""
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = str(equipment_id)
    send_socket.sendto(message.encode(), (IP, BROADCAST_PORT))  #sending to 7500
    print(f"Sent equipment ID: {message} to {IP}:{BROADCAST_PORT}")

def start_services():
    """Start receiver thread"""
    threading.Thread(target=udp_receiver, daemon=True).start()
    print("Receiver started")

if __name__ == "__main__":
    start_services()
    
    #Wait for messages to be processed before script exits
    time.sleep(2000)
