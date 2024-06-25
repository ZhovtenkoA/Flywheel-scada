from tkinter import *
from datetime import datetime, timedelta
import serial
from tkinter import ttk
import crcmod.predefined
from ttkthemes import ThemedTk

from connection_parameters import *
from serial_functions import *
from secondary_functions import *
from tab4_widget import *
from tab3_widget import *
from tab2_widget import *
from tab1_widget import *

import time


pwm = None


# Тестовая функция формирования запросов
def read_holding_test():
    current_time = datetime.now().strftime("%H:%M:%S")
    if not is_testing:
        return

    register_address = 30001
    numbers_to_read = 1
    try:
        ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            parity=parity,
            stopbits=stopbits,
            bytesize=bytesize,
            timeout=timeout,
        )

        try:
            request = bytearray(
                [
                    slave_id,
                    function_number_for_reading,
                    (register_address >> 8) & 0xFF,
                    register_address & 0xFF,
                    0x00,
                    numbers_to_read,
                ]
            )
            print("отпрвка")
            crc_v = calc_crc16_modbus(request)
            request += crc_v
            print(f"Request - {request}")
            ser.write(request)
            print("долбим")
            tab3_widgets.output_test.insert(
                END, f"[{current_time}] долбим долбим долбим\n"
            )
        except Exception as e:
            error_message = f"[{current_time}]Ошибка тестовой отправки запросов: {e}"
            print(error_message)
            tab3_widgets.output_test.insert(END, error_message + "\n")
    except Exception as e:
        error_message = f"[{current_time}]Ошибка тестовой отправки запросов: {e}"
        print(error_message)
        tab3_widgets.output_test.insert(END, error_message + "\n")

    if is_testing:
        root.after(1000, read_holding_test)


# Функция чтения регистров с выводом в строку
def read_holding():
    current_time = datetime.now().strftime("%H:%M:%S")
    if not is_logging:
        return

    register_address = int(tab1_widgets.starting_adress_entry.get())
    numbers_to_read = int(tab1_widgets.numbers_to_read_entry.get())

    try:
        ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            parity=parity,
            stopbits=stopbits,
            bytesize=bytesize,
            timeout=timeout,
        )
        try:
            request = bytearray(
                [
                    slave_id,
                    function_number_for_reading,
                    (register_address >> 8) & 0xFF,
                    register_address & 0xFF,
                    0x00,
                    numbers_to_read,
                ]
            )
            crc_v = calc_crc16_modbus(request)
            request += crc_v
            print(f"Request - {request}")
            ser.write(request)
            try:
                response = ser.read(5 + numbers_to_read * 2)
                print(response)
                response_data = response[:-2]
                response_crc = response[-2:]
                print(f"slave_id[0]: {response[0]}")
                print(f"func number[1]: {response[1]}")
                print(f"byte counter[2]: {response[2]}")
                print(f"data upper[3]: {response[3]}")
                print(f"data lower[4]: {response[4]}")
                print(f" crc upper[5]: {response[4]}")
                print(f"crc lower[5]: {response[4]}")
                if check_crc(response_crc, response_data):
                    data_index = 3
                    byte_count = response[2]
                    data_index = 3
                    registers = []
                    for i in range(numbers_to_read):
                        value = (response[data_index] << 8) + response[data_index + 1]
                        registers.append(value)
                        data_index += 2
                    register_type = "Input Register"
                    for i in range(numbers_to_read):
                        tab1_widgets.holding_output.insert(
                            END,
                            f"[{current_time}] {register_type} -  Register {register_address + i} - value {registers[i]}\n",
                        )
                else:
                    error_message = f"[{current_time}]Ошибка контрольной суммы в ответе"
                    print(error_message)
                    tab1_widgets.holding_output.insert(END, error_message + "\n")
            except Exception as e:
                error_message = f"[{current_time}] Ошибка получения ответа: {e}"
                print(error_message)
                tab1_widgets.holding_output.insert(END, error_message + "\n")
        except Exception as e:
            error_message = f"[{current_time}]Ошибка отправки запроса: {e}"
            print(error_message)
            tab1_widgets.holding_output.insert(END, error_message + "\n")
    except Exception as e:
        error_message = f"[{current_time}]Ошибка подключения: {e}"
        print(error_message)
        tab1_widgets.holding_output.insert(END, error_message + "\n")
    if is_logging:
        root.after(1000, read_holding)


# Запись значения в определенный регистр
def write_holding():
    register_address = int(tab2_widgets.register_address_entry.get())
    value = int(tab2_widgets.value_entry.get())
    try:
        ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            parity=parity,
            stopbits=stopbits,
            bytesize=bytesize,
            timeout=timeout,
        )
        current_time = datetime.now().strftime("%H:%M:%S")
        try:
            request = bytearray(
                [
                    slave_id,
                    0x10,
                    (register_address >> 8) & 0xFF,
                    register_address & 0xFF,
                    0x00,
                    0x01,
                    0x02,
                    (value >> 8) & 0xFF,
                    value & 0xFF,
                ]
            )
            crc16 = crcmod.predefined.mkCrcFun("modbus")
            crc_value = crc16(request)
            request += crc_value.to_bytes(2, byteorder="big")
            ser.write(request)
            tab1_widgets.holding_output.insert(
                END,
                f"[{current_time}] Successfully written to Holding Register {register_address} - value {value}\n",
            )
        except Exception as e:
            error_message = f"[{current_time}] Ошибка отправки запроса на запись: {e}"
            print(error_message)
            tab1_widgets.holding_output.insert(END, error_message + "\n")
    except Exception as e:
        error_message = f"[{current_time}] Ошибка отправки запроса на запись: {e}"
        print(error_message)
        tab1_widgets.holding_output.insert(END, error_message + "\n")


# Чтение регистров с выводом на основной экран
def read_holding_30001_30014():
    global pwm
    if not is_reading:
        return

    register_address = 30001
    numbers_to_read = 14
    try:
        ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            parity=parity,
            stopbits=stopbits,
            bytesize=bytesize,
            timeout=timeout,
        )
        current_time = datetime.now().strftime("%H:%M:%S")
        try:
            request = bytearray(
                [
                    slave_id,
                    function_number_for_reading,
                    (register_address >> 8) & 0xFF,
                    register_address & 0xFF,
                    0x00,
                    numbers_to_read,
                ]
            )
            crc_v = calc_crc16_modbus(request)
            request += crc_v
            print(f"Request - {request}")
            ser.write(request)
            try:
                response = ser.read(5 + numbers_to_read * 2)
                print(f"Response - {response}")
                response_data = response[:-2]
                response_crc = response[-2:]
                if check_crc(response_crc, response_data):
                    data_index = 3
                    registers = []
                    percentage_outputs = [
                        tab4_widgets.output_30005_percent,
                        tab4_widgets.output_30006_percent,
                        tab4_widgets.output_30007_percent,
                        tab4_widgets.output_30008_percent,
                    ]
                    for i in range(numbers_to_read):
                        value = (response[data_index] << 8) + response[data_index + 1]
                        registers.append(value)
                        data_index += 2
                        if i >= 4 and i <= 7:
                            update_pwm_indicator_color(i, value)
                            output_percent = percentage_outputs[i - 4]
                            percentage = convert_to_percentage(value)
                            output_percent.delete(1.0, END)
                            output_percent.insert(END, f"{percentage}%")

                        if i == 8 and moment_of_inertia:
                            kinetic_energy = accumulated_kinetic_energy(
                                moment_of_inertia, value
                            )
                            tab4_widgets.accumulated_kinetic_energy_output.delete(
                                1.0, END
                            )
                            tab4_widgets.accumulated_kinetic_energy_output.insert(
                                END, f"{kinetic_energy}J"
                            )
                        if i == 10:
                            update_indicator_color(value)
                    output_fields = [
                        tab4_widgets.output_30001,
                        tab4_widgets.output_30002,
                        tab4_widgets.output_30003,
                        tab4_widgets.output_30004,
                        tab4_widgets.output_30005,
                        tab4_widgets.output_30006,
                        tab4_widgets.output_30007,
                        tab4_widgets.output_30008,
                        tab4_widgets.output_30009,
                        tab4_widgets.output_30010,
                        tab4_widgets.output_30011,
                        tab4_widgets.output_30012,
                        tab4_widgets.output_30013,
                        tab4_widgets.output_30014,
                    ]
                    for i in range(numbers_to_read):

                        if i == 4:
                            pwm = i
                            output_fields[i].delete(1.0, END)
                            output_fields[i].insert(END, f"{registers[i]}")

                        elif i == 12:
                            converted_vdc = convert_VDC(vdc=registers[i])
                            output_fields[i].delete(1.0, END)
                            output_fields[i].insert(END, f"{converted_vdc}")

                        elif i == 13:
                            converted_adc = convert_ADC(adc=registers[i])
                            power = make_P(adc=converted_adc, vdc=converted_vdc)
                            tab4_widgets.P_output.delete(1.0, END)
                            tab4_widgets.P_output.insert(END, f"{power} W")
                            output_fields[i].delete(1.0, END)
                            output_fields[i].insert(END, f"{converted_adc}")

                        else:
                            output_fields[i].delete(1.0, END)
                            output_fields[i].insert(END, f"{registers[i]}")
                else:
                    error_message = f"[{current_time}]Ошибка контрольной суммы в ответе"
                    print(error_message)
                    tab1_widgets.holding_output.insert(END, error_message + "\n")
            except Exception as e:
                error_message = f"[{current_time}] Ошибка получения ответа "
                print(error_message)
                tab1_widgets.holding_output.insert(END, error_message + "\n")
        except Exception as e:
            error_message = f"[{current_time}] Ошибка отправки запроса "
            print(error_message)
            tab1_widgets.holding_output.insert(END, error_message + "\n")
    except Exception as e:
        error_message = f" Ошибка подключения: {e}"
        print(error_message)
        tab1_widgets.holding_output.insert(END, error_message + "\n")

    if is_reading:
        root.after(1000, read_holding_30001_30014)


# Функции управления PWM (разгон, торможение, стоп)
def acceleration():
    current_time = datetime.now().strftime("%H:%M:%S")
    register_address = 30005
    numbers_to_read = 1
    try:
        ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            parity=parity,
            stopbits=stopbits,
            bytesize=bytesize,
            timeout=timeout,
        )
        current_time = datetime.now().strftime("%H:%M:%S")
        try:
            request = bytearray(
                [
                    slave_id,
                    0x4,
                    (register_address >> 8) & 0xFF,
                    register_address & 0xFF,
                    0x00,
                    numbers_to_read,
                ]
            )
            crc_v = calc_crc16_modbus(request)
            request += crc_v
            ser.write_timeout = timeout
            ser.write(request)
            try:
                response = ser.read(5 + numbers_to_read * 2)
                print(f"Response - {response}")
                response_data = response[:-2]
                response_crc = response[-2:]
                if check_crc(response_crc, response_data):
                    data_index = 3
                    value = (response[data_index] << 8) + response[data_index + 1]
                    register_to_write = 1
                    if value >= 1995:
                        new_value = 2000
                    else:
                        new_value = value + 5
                    try:
                        ser = serial.Serial(
                            port=port,
                            baudrate=baudrate,
                            parity=parity,
                            stopbits=stopbits,
                            bytesize=bytesize,
                        )
                        current_time = datetime.now().strftime("%H:%M:%S")
                        try:
                            request = bytearray(
                                [
                                    slave_id,
                                    0x10,
                                    (register_to_write >> 8) & 0xFF,
                                    register_to_write & 0xFF,
                                    0x00,
                                    0x01,
                                    0x02,
                                    (new_value >> 8) & 0xFF,
                                    new_value & 0xFF,
                                ]
                            )
                            crc16 = crcmod.predefined.mkCrcFun("modbus")
                            crc_value = crc16(request)
                            request += crc_value.to_bytes(2, byteorder="big")
                            ser.write(request)
                        except Exception as e:
                            error_message = f"[{current_time}] Ошибка записи: {e}"
                            print(error_message)
                            tab1_widgets.holding_output.insert(
                                END, error_message + "\n"
                            )
                    except Exception as e:
                        error_message = f"Ошибка чтения: {e}"
                        print(error_message)
                        tab1_widgets.holding_output.insert(END, error_message + "\n")
            except Exception as e:
                error_message = f"[{current_time}]Ошибка получения ответа: {e}"
                print(error_message)
                tab1_widgets.holding_output.insert(END, error_message + "\n")
        except Exception as e:
            error_message = f"[{current_time}]Ошибка получения ответа: {e}"
            print(error_message)
            tab1_widgets.holding_output.insert(END, error_message + "\n")
    except Exception as e:
        error_message = f"[{current_time}] Ошибка отправки запроса на чтение: {e}"
        print(error_message)
        tab1_widgets.holding_output.insert(END, error_message + "\n")


def slowdown():
    current_time = datetime.now().strftime("%H:%M:%S")
    register_address = 30005
    numbers_to_read = 1
    try:
        ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            parity=parity,
            stopbits=stopbits,
            bytesize=bytesize,
            timeout=timeout,
        )
        try:
            request = bytearray(
                [
                    slave_id,
                    0x4,
                    (register_address >> 8) & 0xFF,
                    register_address & 0xFF,
                    0x00,
                    numbers_to_read,
                ]
            )
            crc_v = calc_crc16_modbus(request)
            request += crc_v
            ser.write_timeout = timeout
            ser.write(request)
            try:
                response = ser.read(5 + numbers_to_read * 2)
                print(f"Response - {response}")
                response_data = response[:-2]
                response_crc = response[-2:]
                if check_crc(response_crc, response_data):
                    data_index = 3
                    value = (response[data_index] << 8) + response[data_index + 1]
                    register_to_write = 1
                    if value < 5:
                        new_value = 0
                    else:
                        new_value = value - 5
                    try:
                        ser = serial.Serial(
                            port=port,
                            baudrate=baudrate,
                            parity=parity,
                            stopbits=stopbits,
                            bytesize=bytesize,
                        )
                        current_time = datetime.now().strftime("%H:%M:%S")
                        try:
                            request = bytearray(
                                [
                                    slave_id,
                                    0x10,
                                    (register_to_write >> 8) & 0xFF,
                                    register_to_write & 0xFF,
                                    0x00,
                                    0x01,
                                    0x02,
                                    (new_value >> 8) & 0xFF,
                                    new_value & 0xFF,
                                ]
                            )
                            crc16 = crcmod.predefined.mkCrcFun("modbus")
                            crc_value = crc16(request)
                            request += crc_value.to_bytes(2, byteorder="big")
                            ser.write(request)
                        except Exception as e:
                            error_message = f"[{current_time}] Error writing to Holding Register: {e}"
                            print(error_message)
                            tab1_widgets.holding_output.insert(
                                END, error_message + "\n"
                            )
                    except Exception as e:
                        error_message = f"Error reading Modbus RTU: {e}"
                        print(error_message)
                        tab1_widgets.holding_output.insert(END, error_message + "\n")
            except Exception as e:
                error_message = f"Error reading Modbus RTU: {e}"
                print(error_message)
                tab1_widgets.holding_output.insert(END, error_message + "\n")
        except Exception as e:
            error_message = f"[{current_time}]Error reading input Register: {e}"
            print(error_message)
            tab1_widgets.holding_output.insert(END, error_message + "\n")
    except Exception as e:
        error_message = f"Error reading modbus rtu: {e}"
        print(error_message)
        tab1_widgets.holding_output.insert(END, error_message + "\n")


def shutdown():
    current_time = datetime.now().strftime("%H:%M:%S")
    register_address = 1
    value = 0
    try:
        ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            parity=parity,
            stopbits=stopbits,
            bytesize=bytesize,
            timeout=timeout,
        )

        try:
            request = bytearray(
                [
                    slave_id,
                    0x10,
                    (register_address >> 8) & 0xFF,
                    register_address & 0xFF,
                    0x00,
                    0x01,
                    0x02,
                    (value >> 8) & 0xFF,
                    value & 0xFF,
                ]
            )
            crc16 = crcmod.predefined.mkCrcFun("modbus")
            crc_value = crc16(request)
            request += crc_value.to_bytes(2, byteorder="big")
            ser.write(request)
            tab1_widgets.holding_output.insert(
                END,
                f"[{current_time}] Successfully written to Holding Register {register_address} - value {value}\n",
            )
        except Exception as e:
            error_message = f"[{current_time}] Error writing to Holding Register: {e}"
            print(error_message)
            tab1_widgets.holding_output.insert(END, error_message + "\n")
    except Exception as e:
        error_message = f"[{current_time}] Error writing to Holding Register: {e}"
        print(error_message)
        tab1_widgets.holding_output.insert(END, error_message + "\n")


# Функции управления Trashhold
def trh_plus():

    register_address = 30011
    numbers_to_read = 1
    try:
        ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            parity=parity,
            stopbits=stopbits,
            bytesize=bytesize,
            timeout=timeout,
        )
        current_time = datetime.now().strftime("%H:%M:%S")
        try:
            request = bytearray(
                [
                    slave_id,
                    0x4,
                    (register_address >> 8) & 0xFF,
                    register_address & 0xFF,
                    0x00,
                    numbers_to_read,
                ]
            )
            crc_v = calc_crc16_modbus(request)
            request += crc_v
            ser.write_timeout = timeout
            ser.write(request)
            try:
                response = ser.read(5 + numbers_to_read * 2)
                print(f"Response - {response}")
                response_data = response[:-2]
                response_crc = response[-2:]
                if check_crc(response_crc, response_data):
                    data_index = 3
                    value = (response[data_index] << 8) + response[data_index + 1]
                    register_to_write = 2
                    if value >= 980:
                        new_value = 1000
                    else:
                        new_value = value + 20
                    try:
                        ser = serial.Serial(
                            port=port,
                            baudrate=baudrate,
                            parity=parity,
                            stopbits=stopbits,
                            bytesize=bytesize,
                        )
                        current_time = datetime.now().strftime("%H:%M:%S")
                        try:
                            request = bytearray(
                                [
                                    slave_id,
                                    0x10,
                                    (register_to_write >> 8) & 0xFF,
                                    register_to_write & 0xFF,
                                    0x00,
                                    0x01,
                                    0x02,
                                    (new_value >> 8) & 0xFF,
                                    new_value & 0xFF,
                                ]
                            )
                            crc16 = crcmod.predefined.mkCrcFun("modbus")
                            crc_value = crc16(request)
                            request += crc_value.to_bytes(2, byteorder="big")
                            ser.write(request)
                        except Exception as e:
                            error_message = f"[{current_time}] Error writing to Holding Register: {e}"
                            print(error_message)
                            tab1_widgets.holding_output.insert(
                                END, error_message + "\n"
                            )
                    except Exception as e:
                        error_message = f"Error reading Modbus RTU: {e}"
                        print(error_message)
                        tab1_widgets.holding_output.insert(END, error_message + "\n")
            except Exception as e:
                error_message = f"[{current_time}]Error reading input Register: {e}"
                print(error_message)
                tab1_widgets.holding_output.insert(END, error_message + "\n")

        except Exception as e:
            error_message = f"[{current_time}]Error reading input Register: {e}"
            print(error_message)
            tab1_widgets.holding_output.insert(END, error_message + "\n")
    except Exception as e:
        error_message = f"Error reading modbus rtu: {e}"
        print(error_message)
        tab1_widgets.holding_output.insert(END, error_message + "\n")


def trh_minus():

    register_address = 30011
    numbers_to_read = 1
    try:
        ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            parity=parity,
            stopbits=stopbits,
            bytesize=bytesize,
            timeout=timeout,
        )
        current_time = datetime.now().strftime("%H:%M:%S")
        try:
            request = bytearray(
                [
                    slave_id,
                    0x4,
                    (register_address >> 8) & 0xFF,
                    register_address & 0xFF,
                    0x00,
                    numbers_to_read,
                ]
            )
            crc_v = calc_crc16_modbus(request)
            request += crc_v
            ser.write_timeout = timeout
            ser.write(request)
            try:
                response = ser.read(5 + numbers_to_read * 2)
                print(f"Response - {response}")
                response_data = response[:-2]
                response_crc = response[-2:]
                if check_crc(response_crc, response_data):
                    data_index = 3
                    value = (response[data_index] << 8) + response[data_index + 1]
                    register_to_write = 2
                    if value < 20:
                        new_value = 0
                    else:
                        new_value = value - 20
                    try:
                        ser = serial.Serial(
                            port=port,
                            baudrate=baudrate,
                            parity=parity,
                            stopbits=stopbits,
                            bytesize=bytesize,
                        )
                        current_time = datetime.now().strftime("%H:%M:%S")
                        try:
                            request = bytearray(
                                [
                                    slave_id,
                                    0x10,
                                    (register_to_write >> 8) & 0xFF,
                                    register_to_write & 0xFF,
                                    0x00,
                                    0x01,
                                    0x02,
                                    (new_value >> 8) & 0xFF,
                                    new_value & 0xFF,
                                ]
                            )
                            crc16 = crcmod.predefined.mkCrcFun("modbus")
                            crc_value = crc16(request)
                            request += crc_value.to_bytes(2, byteorder="big")
                            ser.write(request)
                        except Exception as e:
                            error_message = f"[{current_time}] Error writing to Holding Register: {e}"
                            print(error_message)
                            tab1_widgets.holding_output.insert(
                                END, error_message + "\n"
                            )
                    except Exception as e:
                        error_message = f"Error reading Modbus RTU: {e}"
                        print(error_message)
                        tab1_widgets.holding_output.insert(END, error_message + "\n")
            except Exception as e:
                error_message = f"[{current_time}]Error reading input Register: {e}"
                print(error_message)
                tab1_widgets.holding_output.insert(END, error_message + "\n")
        except Exception as e:
            error_message = f"[{current_time}]Error reading input Register: {e}"
            print(error_message)
            tab1_widgets.holding_output.insert(END, error_message + "\n")
    except Exception as e:
        error_message = f"Error reading modbus rtu: {e}"
        print(error_message)
        tab1_widgets.holding_output.insert(END, error_message + "\n")


def trh_write():

    register_address = 2
    current_time = datetime.now().strftime("%H:%M:%S")
    if tab4_widgets.value_trh_entry.get() != "":
        value = int(tab4_widgets.value_trh_entry.get())
        try:
            ser = serial.Serial(
                port=port,
                baudrate=baudrate,
                parity=parity,
                stopbits=stopbits,
                bytesize=bytesize,
                timeout=timeout,
            )

            try:
                request = bytearray(
                    [
                        slave_id,
                        0x10,
                        (register_address >> 8) & 0xFF,
                        register_address & 0xFF,
                        0x00,
                        0x01,
                        0x02,
                        (value >> 8) & 0xFF,
                        value & 0xFF,
                    ]
                )
                crc16 = crcmod.predefined.mkCrcFun("modbus")
                crc_value = crc16(request)
                request += crc_value.to_bytes(2, byteorder="big")
                ser.write(request)
                tab1_widgets.holding_output.insert(
                    END,
                    f"[{current_time}] Successfully written to Holding Register {register_address} - value {value}\n",
                )
            except Exception as e:
                error_message = (
                    f"[{current_time}] Error writing to Holding Register: {e}"
                )
                print(error_message)
                tab1_widgets.holding_output.insert(END, error_message + "\n")
        except Exception as e:
            error_message = f"[{current_time}] Error writing to Holding Register: {e}"
            print(error_message)
            tab1_widgets.holding_output.insert(END, error_message + "\n")


# Функции управления логированием в строку
def start_logging():
    global is_logging
    is_logging = True
    read_holding()


def stop_loging():
    global is_logging
    is_logging = False


# Функции управления чтением на основной экран
def start_reading():
    global is_reading
    is_reading = True
    tab4_widgets.start_button.config(
        background="green", font=("Arial", 10, "bold"), foreground="white"
    )
    read_holding_30001_30014()


def stop_reading():
    global is_reading
    is_reading = False
    tab4_widgets.start_button.config(
        background="#f0f0f0", font=("Arial", 10, "bold"), foreground="black"
    )


# Функции управления тестовыми запросами
def start_test_reading():
    print("Starting test requests...")
    global is_testing
    is_testing = True
    read_holding_test()


def stop_test_reading():
    global is_testing
    is_testing = False


# Очистка поля вывода
def clear_output():
    tab1_widgets.holding_output.delete(1.0, END)


# Запись момента иннерции
def write_moment_of_inertia():
    global moment_of_inertia
    moment_of_inertia = tab4_widgets.inertia_value_entry.get()
    return moment_of_inertia


# Время
def update_time():
    current_time = time.strftime("%H:%M:%S")
    tab4_widgets.time_label.config(text=current_time)
    tab4_widgets.time_label.after(1000, update_time)


# Изменение цвета индикатора TRH
def update_indicator_color(value):
    register_value = value
    if register_value >= 200 and register_value <= 500:
        tab4_widgets.indicator.itemconfig(tab4_widgets.circle, fill="green")
    else:
        tab4_widgets.indicator.itemconfig(tab4_widgets.circle, fill="red")


# Изменение цвета индикатора PWM
def update_pwm_indicator_color(i, value):
    register_value = value
    if i == 4:
        if register_value > 1000:
            tab4_widgets.indicator_pwm1.itemconfig(tab4_widgets.circle, fill="red")
        # else:
        #     indicator_pwm1.itemconfig(circle, fill="red")
    elif i == 5:
        if register_value > 1000:
            tab4_widgets.indicator_pwm2.itemconfig(tab4_widgets.circle, fill="red")
        # else:
        #     indicator_pwm2.itemconfig(circle, fill="red")
    elif i == 6:
        if register_value > 1000:
            tab4_widgets.indicator_pwm3.itemconfig(tab4_widgets.circle, fill="red")
        # else:
        #     indicator_pwm3.itemconfig(circle, fill="red")
    elif i == 7:
        if register_value > 1000:
            tab4_widgets.indicator_pwm4.itemconfig(tab4_widgets.circle, fill="red")
        # else:
        #     indicator_pwm4.itemconfig(circle, fill="red")


def update_power_output(power):
    tab4_widgets.kW_power_output.delete(1.0, END)
    tab4_widgets.kW_power_output.insert(END, f"{power} W*h")


def start_counting_w_h():
    global counting_in_progress, power_accumulated
    if counting_in_progress:
        counting_in_progress = False
        power_accumulated = 0
        tab4_widgets.kW_power_output.delete(1.0, END)
    else:
        counting_in_progress = True
        make_W_h()


# Черновик функции получения киловатт*ч
def make_W_h():
    global power_accumulated, counting_in_progress
    register_address = 30013
    numbers_to_read = 2
    try:
        ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            parity=parity,
            stopbits=stopbits,
            bytesize=bytesize,
            timeout=timeout,
        )

        request = bytearray(
            [
                slave_id,
                0x4,
                (register_address >> 8) & 0xFF,
                register_address & 0xFF,
                0x00,
                numbers_to_read,
            ]
        )
        crc_v = calc_crc16_modbus(request)
        request += crc_v
        ser.write(request)

        response = ser.read(5 + numbers_to_read * 2)
        response_data = response[:-2]
        response_crc = response[-2:]

        if check_crc(response_crc, response_data):
            data_index = 3
            registers = []

            for i in range(numbers_to_read):
                value = (response[data_index] << 8) + response[data_index + 1]
                registers.append(value)
                data_index += 2

                if i == 0:
                    converted_vdc = convert_VDC(vdc=value)
                elif i == 1:
                    converted_adc = convert_ADC(adc=value)
                    power = make_P(adc=converted_adc, vdc=converted_vdc)
                    power_accumulated += power * (1 / 3600)
                    power_accumulated = round(power_accumulated, 4)

            update_power_output(power_accumulated)
    except Exception as e:
        error_message = f"Error reading Modbus RTU: {e}"
        print(error_message)
        tab1_widgets.holding_output.insert(END, error_message + "\n")

    if counting_in_progress:
        root.after(5000, make_W_h)


# Черновик функции записи времени
def write_time():
    print("writing time")
    try:
        ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            parity=parity,
            stopbits=stopbits,
            bytesize=bytesize,
            timeout=timeout,
        )
        current_time = datetime.now()
        print(f"current_time {current_time}")
        current_hour = current_time.hour
        print(f"current_hour {current_hour}")
        current_minute = current_time.minute
        print(f"current_minute {current_minute}")
        current_second = current_time.second
        print(f"current_second {current_second}")
        combined_value = (current_hour << 8) | (current_minute & 0xFF)
        print(f"combined_value {combined_value}")

        try:
            # Запись часов и минут
            register_address_1 = 3
            request = bytearray(
                [
                    slave_id,
                    0x10,
                    (register_address_1 >> 8) & 0xFF,
                    register_address_1 & 0xFF,
                    0x00,
                    0x01,
                    0x04,
                    (combined_value >> 8) & 0xFF,
                    combined_value & 0xFF,
                ]
            )
            crc_v = calc_crc16_modbus(request)
            request += crc_v
            ser.write_timeout = timeout
            print("Request for time")
            ser.write(request)
            print("Request for time is done")

            # Запись секунд
            register_address_2 = 4
            request = bytearray(
                [
                    slave_id,
                    0x10,
                    (register_address_2 >> 8) & 0xFF,
                    register_address_2 & 0xFF,
                    0x00,
                    0x01,
                    0x02,
                    (current_second >> 8) & 0xFF,
                    current_second & 0xFF,
                ]
            )
            crc_v = calc_crc16_modbus(request)
            request += crc_v
            ser.write_timeout = timeout
            ser.write(request)
            print(" Второй Request for time is done")
        except serial.SerialException as e:
            error_message = f"[{current_time}] Serial port error: {e}"
            print(error_message)
            tab1_widgets.holding_output.insert(END, error_message + "\n")

        except Exception as e:
            error_message = f"[{current_time}] Error writing time: {e}"
            print(error_message)
            tab1_widgets.holding_output.insert(END, error_message + "\n")
    except serial.SerialException as e:
        error_message = f"Serial port error: {e}"
        print(error_message)
        tab1_widgets.holding_output.insert(END, error_message + "\n")

    except Exception as e:
        error_message = f"Error opening serial port: {e}"
        print(error_message)
        tab1_widgets.holding_output.insert(END, error_message + "\n")


def resize_window(event):
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    tab1_widgets.holding_output.place(
        x=10, y=70, width=window_width - 30, height=window_height - 200
    )
    tab3_widgets.output_test.place(
        x=10, y=70, width=window_width - 30, height=window_height - 200
    )

    if root.attributes("-fullscreen"):
        tab1_widgets.clear_button.place(x=10, y=window_height - 130, width=100)
        tab4_widgets.start_button.place(x=120, y=window_height - 130, width=100)
        tab4_widgets.stop_button.place(x=230, y=window_height - 130, width=100)
        tab2_widgets.write_button.place(x=10, y=window_height - 130, width=100)
        tab3_widgets.start_button_test.place(x=100, y=window_height - 130, width=120)
        tab3_widgets.stop_button_test.place(x=230, y=window_height - 130, width=100)
        tab1_widgets.start_loging_button.place(x=120, y=window_height - 130, width=100)
        tab1_widgets.stop_loging_button.place(x=230, y=window_height - 130, width=100)
        tab4_widgets.acceleration_button.place(x=340, y=window_height - 130, width=100)
        tab4_widgets.slowdown_button.place(x=450, y=window_height - 130, width=100)
        tab4_widgets.shutdown_button.place(x=560, y=window_height - 130, width=100)

    else:
        tab1_widgets.clear_button.place(x=10, y=window_height - 70, width=100)
        tab4_widgets.start_button.place(x=120, y=window_height - 70, width=100)
        tab4_widgets.stop_button.place(x=230, y=window_height - 70, width=100)
        tab2_widgets.write_button.place(x=10, y=window_height - 70, width=100)
        tab3_widgets.start_button_test.place(x=100, y=window_height - 70, width=120)
        tab3_widgets.stop_button_test.place(x=230, y=window_height - 70, width=100)
        tab1_widgets.start_loging_button.place(x=120, y=window_height - 70, width=100)
        tab1_widgets.stop_loging_button.place(x=230, y=window_height - 70, width=100)
        tab4_widgets.acceleration_button.place(x=340, y=window_height - 70, width=100)
        tab4_widgets.slowdown_button.place(x=450, y=window_height - 70, width=100)
        tab4_widgets.shutdown_button.place(x=560, y=window_height - 70, width=100)

    tab1_widgets.scrollbar.place(x=window_width - 20, y=70, height=window_height - 200)


root = ThemedTk(theme="black")
root.title("Flywheel scada")

notebook = ttk.Notebook(root)
notebook.pack(fill=BOTH, expand=True)

tab4 = ttk.Frame(notebook)
notebook.add(tab4, text="Mainscreen")

tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Read Holding registers")

tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Write Holding registers")

tab3 = ttk.Frame(notebook)
notebook.add(tab3, text="Test request")


window_width = 1024
window_height = 720
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = int((screen_width - window_width) / 2)
y = int((screen_height - window_height) / 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")


def auto_scroll():
    tab1_widgets.holding_output.see("end")
    tab1_widgets.holding_output.after(100, auto_scroll)


tab1_widgets = Tab1Widget(tab1, clear_output, start_logging, stop_loging)
tab2_widgets = Tab2Widget(tab2, write_holding)
tab3_widgets = Tab3Widget(tab3, start_test_reading, stop_test_reading)
tab4_widgets = Tab4Widget(tab4, start_reading,
        stop_reading,
        acceleration,
        slowdown,
        shutdown,
        trh_plus,
        trh_minus,
        trh_write,
        write_moment_of_inertia,
        start_counting_w_h)

sliders = TestButtons(tab4)


auto_scroll()
root.bind("<Configure>", resize_window)
update_time()
root.mainloop()
