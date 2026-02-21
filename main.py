from machine import Pin, I2C
import time

PN532_ADDR = 0x24

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)

def write_command(cmd):
    length = len(cmd) + 1
    lcs = (~length + 1) & 0xFF
    frame = b'\x00\x00\xFF' + bytes([length, lcs]) + b'\xD4' + cmd
    dcs = (~(0xD4 + sum(cmd)) + 1) & 0xFF
    frame += bytes([dcs, 0x00])
    i2c.writeto(PN532_ADDR, frame)

def read_response(length=32):
    time.sleep(0.2)
    return i2c.readfrom(PN532_ADDR, length)

def sam_configuration():
    write_command(b'\x14\x01\x14\x01')
    read_response()

def read_passive_target():
    write_command(b'\x4A\x01\x00')
    data = read_response()
    return data

print("PN532 初期化中...")
time.sleep(1)

sam_configuration()
print("カードをかざしてください")

while True:
    data = read_passive_target()

    if data and len(data) > 20:
        # UID長さ取得
        uid_length = data[19]
        uid = data[20:20+uid_length]

        if uid_length > 0:
            uid_hex = ''.join('{:02X}'.format(b) for b in uid)
            print("UID:", uid_hex)
            time.sleep(2)
