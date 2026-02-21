from machine import Pin, I2C
import time

# I2C設定
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)

PN532_ADDR = 0x24

def wakeup():
    i2c.writeto(PN532_ADDR, b'\x00\x00\xFF\x00\xFF\x00')
    time.sleep(0.1)

def get_firmware():
    cmd = b'\x00\x00\xFF\x02\xFE\xD4\x02\x2A\x00'
    i2c.writeto(PN532_ADDR, cmd)
    time.sleep(0.1)
    return i2c.readfrom(PN532_ADDR, 12)

def read_passive_target():
    cmd = b'\x00\x00\xFF\x04\xFC\xD4\x4A\x01\x00\xE1\x00'
    i2c.writeto(PN532_ADDR, cmd)
    time.sleep(0.3)
    data = i2c.readfrom(PN532_ADDR, 24)
    return data

print("PN532 起動中...")
wakeup()

print("カードをかざしてください")

while True:
    try:
        data = read_passive_target()

        # UID抽出（位置固定）
        uid = data[13:17]

        if len(uid) == 4:
            uid_hex = ''.join('{:02X}'.format(b) for b in uid)
            print("UID:", uid_hex)
            time.sleep(2)

    except:
        pass
