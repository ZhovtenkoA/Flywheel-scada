from connection_parameters import *
import serial


ser = None

def connection():
    print("Starting connection...")
    global ser
    try:
        ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            parity=parity,
            stopbits=stopbits,
            bytesize=bytesize,
            timeout = timeout
        )
        print("Соединение установлено")
    except Exception as e:
        print(f"Ошибка при установке соединения: {e}")


def close_connection():
    print("Closing connection...")
    if ser is not None:
        ser.close()

#Функция проверки контрольной суммы
def check_crc(response_crc, response_data):
    calculated_crc = calc_crc16_modbus(response_data)
    print(f"calculated_crc - {calculated_crc}")
    print(f"response_crc - {response_crc}")
    return response_crc == calculated_crc

def calc_crc16_modbus(buffer):
    crc = 0xFFFF
    for byte in buffer:
        crc ^= byte
        for _ in range(8):
            flag = crc & 0x0001
            crc >>= 1
            if flag:
                crc ^= 0xA001
    crc = ((crc & 0xFF) << 8) | ((crc & 0xFF00) >> 8)
    return crc.to_bytes(2, byteorder='big')

