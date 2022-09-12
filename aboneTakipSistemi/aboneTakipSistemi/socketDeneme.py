import socket


UDP_IP = "169.254.119.36"
UDP_PORT = 8888
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
sock.bind((UDP_IP, UDP_PORT))
while True:
    data,addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print("data: ",data)
    print("addr: ",addr)
