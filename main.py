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
import json

PN532_ADDR = 0x24
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)

# =============================
# PN532 基本関数
# =============================

def write_command(cmd):
    length = len(cmd) + 1
    lcs = (~length + 1) & 0xFF
    frame = b'\x00\x00\xFF' + bytes([length, lcs]) + b'\xD4' + cmd
    dcs = (~(0xD4 + sum(cmd)) + 1) & 0xFF
    frame += bytes([dcs, 0x00])
    i2c.writeto(PN532_ADDR, frame)

def read_ack():
    time.sleep(0.05)
    i2c.readfrom(PN532_ADDR, 7)

def read_response(size=32):
    time.sleep(0.2)
    return i2c.readfrom(PN532_ADDR, size)

def detect_card():
    write_command(b'\x4A\x01\x00')
    read_ack()
    data = read_response()
    return len(data) > 20 and data[6] == 0xD5

def write_block(block, data4):
    cmd = b'\x40\x01\xA2' + bytes([block]) + data4
    write_command(cmd)
    read_ack()
    read_response()

# =============================
# 書き込み処理
# =============================

card_data = {
    "name": "FIRE",
    "hp": 50
}

json_str = json.dumps(card_data)
json_bytes = json_str.encode("utf-8")

# 先頭にデータ長を追加
payload = bytes([len(json_bytes)]) + json_bytes

# 4バイト単位に分割
blocks = []
for i in range(0, len(payload), 4):
    chunk = payload[i:i+4]
    if len(chunk) < 4:
        chunk += b'\x00' * (4 - len(chunk))
    blocks.append(chunk)

print("カードをかざしてください（書き込み）")

while True:
    if detect_card():
        print("カード検出、書き込み開始")

        block_num = 4
        for chunk in blocks:
            write_block(block_num, chunk)
            block_num += 1

        print("書き込み完了:", json_str)
        break

    time.sleep(0.5)














from machine import Pin, I2C
import time
import json

PN532_ADDR = 0x24
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)

led = Pin(25, Pin.OUT)

def write_command(cmd):
    length = len(cmd) + 1
    lcs = (~length + 1) & 0xFF
    frame = b'\x00\x00\xFF' + bytes([length, lcs]) + b'\xD4' + cmd
    dcs = (~(0xD4 + sum(cmd)) + 1) & 0xFF
    frame += bytes([dcs, 0x00])
    i2c.writeto(PN532_ADDR, frame)

def read_ack():
    time.sleep(0.05)
    i2c.readfrom(PN532_ADDR, 7)

def read_response(size=32):
    time.sleep(0.2)
    return i2c.readfrom(PN532_ADDR, size)

def read_block(block):
    cmd = b'\x40\x01\x30' + bytes([block])
    write_command(cmd)
    read_ack()
    return read_response()

print("カードをかざしてください（読み取り）")

while True:
    data_bytes = b''
    
    # まずブロック4読む
    data = read_block(4)
    raw = data[13:17]
    
    data_length = raw[0]
    data_bytes += raw[1:]

    # 必要ブロック数計算
    remaining = data_length - len(data_bytes)
    block_num = 5

    while remaining > 0:
        data = read_block(block_num)
        raw = data[13:17]
        data_bytes += raw
        remaining -= 4
        block_num += 1

    json_str = data_bytes[:data_length].decode("utf-8")

    try:
        card = json.loads(json_str)
        print("読み取り成功:", card)

        # 分岐例
        if card["name"] == "FIRE":
            print("🔥 FIRE 発動")
            led.on()
            time.sleep(1)
            led.off()

    except:
        print("JSON解析失敗")

    time.sleep(3)
