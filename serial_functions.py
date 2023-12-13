from connection_parameters import *
import serial


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


