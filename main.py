from machine import Pin, I2C
import time
from pn532_i2c import PN532_I2C

# I2C設定
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)

# PN532初期化
pn532 = PN532_I2C(i2c, debug=False)

# ファームウェア確認
ic, ver, rev, support = pn532.firmware_version
print("PN532 Firmware:", ver, ".", rev)

# RFID読み取り開始
pn532.SAM_configuration()

print("カードをかざしてください...")

while True:
    uid = pn532.read_passive_target(timeout=0.5)
    
    if uid is not None:
        print("UID:", [hex(i) for i in uid])
        time.sleep(2)
