import socket
import time
import random

# ======================
# CONFIG
# ======================
SWITCH_IP = "192.168.40.106"   # CHANGE TO YOUR SWITCH IP
PORT = 6000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SWITCH_IP, PORT))

print("Connected!")

def send(cmd):
    sock.sendall((cmd + "\r\n").encode())
    time.sleep(0.05)

def click(btn):
    send(f"click {btn}")

# ======================
# LOOP
# ======================
while True:

    # ABXY together
    send("press A")
    send("press B")
    send("press X")
    send("press Y")
    time.sleep(0.2)
    send("release A")
    send("release B")
    send("release X")
    send("release Y")

    # Wait 7–10 sec
    time.sleep(random.uniform(7,10))

    click("A")

    time.sleep(random.uniform(4,9))
    click("A")

    time.sleep(random.uniform(4,12))
    click("A")

    time.sleep(4)
    click("B")

    time.sleep(random.uniform(8,12))
    click("A")

    time.sleep(3)
    click("A")

    time.sleep(2)
    click("A")

    time.sleep(1)
    click("A")

    time.sleep(4)
    click("B")

    # B 10 times (1–2 sec random)
    for _ in range(10):
        click("B")
        time.sleep(random.uniform(1,2))

    # Menu actions
    click("X")

    time.sleep(1)
    click("A")

    click("A")

    time.sleep(2)
    click("A")

    time.sleep(1)
    click("A")

    time.sleep(5)

    print("Loop complete — restarting")
