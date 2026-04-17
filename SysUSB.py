import socket
import time
import random
import cv2
import numpy as np
import pyautogui
import sys
import requests  # NEW

# ======================
# CONFIG
# ======================
SWITCH_IP = "192.168.40.107"   # CHANGE TO YOUR SWITCH IP
PORT = 6000
RTSP_URL = "rtsp://192.168.40.107:6666"  # CHANGE TO YOUR RTSP URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1337242155600842762/Hx5q6P3zD7xHmp9R8dpVapxqTVvzCLnK9mtsM6UHZblAkjh0_Jd_7x1nLpbnO_f5qRLV"  # ADD YOUR WEBHOOK

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SWITCH_IP, PORT))

print("Connected!")

def send(cmd):
    sock.sendall((cmd + "\r\n").encode())
    time.sleep(0.05)

def click(btn):
    send(f"click {btn}")

# ======================
# DISCORD NOTIFICATION
# ======================
def send_discord_notification(message=""):
    try:
        if message:
            response = requests.post(
                WEBHOOK_URL,
                json={"content": message}
            )
        else:
            response = requests.post(
                WEBHOOK_URL,
                json={"content": "✨ Shiny Pokémon detected! ✨"}
            )

        if response.status_code in (200, 204):
            print("Discord notification sent!")
        else:
            print(f"Failed to send Discord notification: {response.status_code}")

    except Exception as e:
        print(f"Error sending Discord notification: {e}")

# ======================
# BLUE BORDER DETECTION
# ======================
def has_blue_border(frame):
    x, y, w, h = 150, 100, 150, 180  # Adjust if needed
    roi = frame[y:y+h, x:x+w]

    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([90, 100, 150])
    upper_blue = np.array([120, 255, 255])

    mask = cv2.inRange(hsv_roi, lower_blue, upper_blue)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return len(contours) > 0

# ======================
# SOFT RESET
# ======================
def soft_reset():
    print("No blue border detected. Pressing ABXY for soft reset.")
    pyautogui.press('a')
    pyautogui.press('b')
    pyautogui.press('x')
    pyautogui.press('y')
    time.sleep(1)

# ======================
# VIDEO STREAM
# ======================
cap = cv2.VideoCapture(RTSP_URL)

if not cap.isOpened():
    print("Error: Could not open RTSP stream.")
    send_discord_notification("Bot crashed: Could not open RTSP stream.")
    exit()

# ======================
# MAIN LOOP
# ======================
try:
    while True:
        send("press A")
        send("press B")
        send("press X")
        send("press Y")
        time.sleep(0.2)
        send("release A")
        send("release B")
        send("release X")
        send("release Y")

        time.sleep(random.uniform(7, 10))
        click("A")
        time.sleep(random.uniform(4, 9))
        click("A")
        time.sleep(random.uniform(4, 12))
        click("A")
        time.sleep(4)
        click("B")
        time.sleep(random.uniform(8, 12))
        click("A")
        time.sleep(3)
        click("A")
        time.sleep(2)
        click("A")
        time.sleep(1)
        click("A")
        time.sleep(4)
        click("B")

        for _ in range(8):
            click("B")
            time.sleep(1.5)

        click("X")
        time.sleep(1)
        click("A")
        click("A")
        time.sleep(2)
        click("A")
        time.sleep(1)
        click("A")
        time.sleep(5)

        print("Loop complete — checking for blue border...")

        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to grab frame from RTSP stream.")
            send_discord_notification("Bot crashed: Failed to grab frame from RTSP stream.")
            break

        if has_blue_border(frame):
            print("Shiny Pokémon found! Blue border detected.")

            # 🔔 SEND DISCORD ALERT WITH IMAGE
            send_discord_notification("Shiny Pokémon found! Blue border detected.")

            cap.release()
            cv2.destroyAllWindows()
            sys.exit()

        else:
            print("No shiny found. Blue border not detected.")
            soft_reset()

except Exception as e:
    print(f"An error occurred: {e}")
    send_discord_notification(f"Bot crashed: {str(e)}")
    cap.release()
    cv2.destroyAllWindows()
    sys.exit()