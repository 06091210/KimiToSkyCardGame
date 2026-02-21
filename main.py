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

def read_ack():
    time.sleep(0.05)
    return i2c.readfrom(PN532_ADDR, 7)

def read_response():
    time.sleep(0.2)
    return i2c.readfrom(PN532_ADDR, 32)

def sam_configuration():
    write_command(b'\x14\x01\x14\x01')
    read_ack()
    read_response()

def read_passive_target():
    write_command(b'\x4A\x01\x00')
    read_ack()
    return read_response()

print("PN532 初期化中...")
time.sleep(1)

sam_configuration()
print("カードをかざしてください")

while True:
    data = read_passive_target()

    # 正しいレスポンスか確認
    if data and len(data) > 20 and data[6] == 0xD5 and data[7] == 0x4B:
        uid_length = data[12]
        uid = data[13:13+uid_length]

        uid_hex = ''.join('{:02X}'.format(b) for b in uid)
        print("UID:", uid_hex)
        time.sleep(2)











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

def read_ack():
    time.sleep(0.05)
    return i2c.readfrom(PN532_ADDR, 7)

def read_response():
    time.sleep(0.2)
    return i2c.readfrom(PN532_ADDR, 32)

def sam_config():
    write_command(b'\x14\x01\x14\x01')
    read_ack()
    read_response()

def read_uid():
    write_command(b'\x4A\x01\x00')
    read_ack()
    data = read_response()

    if len(data) > 20 and data[6] == 0xD5 and data[7] == 0x4B:
        uid_len = data[12]
        uid = data[13:13+uid_len]
        return ''.join('{:02X}'.format(b) for b in uid)

    return None

print("初期化中...")
time.sleep(1)
sam_config()
print("カードをかざしてください")

while True:
    uid = read_uid()
    if uid:
        print("UID:", uid)
        time.sleep(2)
