from tkinter import *
from datetime import datetime
import serial
from tkinter import ttk
import crcmod.predefined
from ttkthemes import ThemedTk
from connection_parameters import *

#Тестовая функция формирования запросов
def read_holding_test():
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
            print("отпрвка")
            ser.write(request)
            print("долбим")
            output_test.insert(END, f"[{current_time}] долбим долбим долбим\n")
 
        except Exception as e:
            error_message = f"[{current_time}]Error reading input Register: {e}"
            print(error_message)
            output_test.insert(END, error_message + "\n")
 
    except Exception as e:
        error_message = f"Error reading modbus rtu: {e}"
        print(error_message)
        output.insert(END, error_message + "\n")
 
    if is_testing:
        root.after(1000, read_holding_test)
 

#Функция чтения регистров с выводом в строку 
def read_holding():
    if not is_logging:
        return
 
    register_address = int(starting_adress_entry.get())
    numbers_to_read = int(numbers_to_read_entry.get())
 
    try:
        ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            parity=parity,
            stopbits=stopbits,
            bytesize=bytesize,
        )
        ser.timeout = timeout
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
            ser.write(request)
            try:
                response = ser.read(5 + numbers_to_read * 2)
                print(response)
                byte_count = response[2]
                data_index = 3
                registers = []
                for i in range(numbers_to_read):
                    value = (response[data_index] << 8) + response[data_index + 1]
                    registers.append(value)
                    data_index += 2
                ser.close()
                register_type = "Input Register"
                for i in range(numbers_to_read):
                    output.insert(
                        END,
                        f"[{current_time}] {register_type} -  Register {register_address + i} - value {registers[i]}\n",
                    )
            except serial.SerialTimeoutException:
                error_message = (
                    f"[{current_time}] Timeout occurred while reading response"
                )
                print(error_message)
                output.insert(END, error_message + "\n")
        except Exception as e:
            error_message = f"[{current_time}]Error reading input Register: {e}"
            print(error_message)
            output.insert(END, error_message + "\n")
    except Exception as e:
        error_message = f"Error reading modbus rtu: {e}"
        print(error_message)
        output.insert(END, error_message + "\n")
 
    if is_logging:
        root.after(500, read_holding)
 

#Запись значения в определенный регистр
def write_holding():
    register_address = int(register_address_entry.get())
    value = int(value_entry.get())
 
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
            ser.close()
            output.insert(
                END,
                f"[{current_time}] Successfully written to Holding Register {register_address} - value {value}\n",
            )
        except Exception as e:
            error_message = f"[{current_time}] Error writing to Holding Register: {e}"
            print(error_message)
            output.insert(END, error_message + "\n")
    except Exception as e:
        error_message = f"Error reading Modbus RTU: {e}"
        print(error_message)
        output.insert(END, error_message + "\n")
 

#Чтение регистров с выводом на основной экран
def read_holding_30001_30014():
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
        )
        ser.timeout = timeout
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
            ser.write(request)
            try:
                response = ser.read(5 + numbers_to_read * 2)
                print(response)
                data_index = 3
                registers = []
                percentage_outputs = [
                    output_30005_percent,
                    output_30006_percent,
                    output_30007_percent,
                    output_30008_percent,
                ]
                for i in range(numbers_to_read):
                    value = (response[data_index] << 8) + response[data_index + 1]
                    registers.append(value)
                    data_index += 2
                    if i >= 4 and i <= 7:
                        output_percent = percentage_outputs[i - 4]
                        percentage = convert_to_percentage(value)
                        output_percent.delete(1.0, END)
                        output_percent.insert(END, f"{percentage}%")
                    
                    if i == 9 and moment_of_inertia:
                        kinetic_energy = accumulated_kinetic_energy(moment_of_inertia, value)
                        accumulated_kinetic_energy_output.delete(1.0, END)
                        accumulated_kinetic_energy_output.insert(END, f"{kinetic_energy}J")
                    if i ==  10:
                        update_indicator_color(value)
                ser.close()
                output_fields = [
                    output_30001,
                    output_30002,
                    output_30003,
                    output_30004,
                    output_30005,
                    output_30006,
                    output_30007,
                    output_30008,
                    output_30009,
                    output_30010,
                    output_30011, 
                    output_30012,
                    output_30013,
                    output_30014
                ]
                for i in range(numbers_to_read):
                    output_fields[i].delete(1.0, END)
                    output_fields[i].insert(END, f"{registers[i]}")
            except serial.SerialTimeoutException:
                error_message = (
                    f"[{current_time}] Timeout occurred while reading response"
                )
                print(error_message)
                output.insert(END, error_message + "\n")
        except Exception as e:
            error_message = f"[{current_time}]Error reading input Register: {e}"
            print(error_message)
            output.insert(END, error_message + "\n")
    except Exception as e:
        error_message = f"Error reading modbus rtu: {e}"
        print(error_message)
        output.insert(END, error_message + "\n")
 
    if is_reading:
        root.after(500, read_holding_30001_30014)
 

#Функции управления PWM (разгон, торможение, стоп)
def acceleration():
    register_address = 30005
    numbers_to_read = 1
 
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
                    0x4,
                    (register_address >> 8) & 0xFF,
                    register_address & 0xFF,
                    0x00,
                    numbers_to_read,
                ]
            )
            ser.write(request)
            response = ser.read(5 + numbers_to_read * 2)
            print(response)
            data_index = 3
            value = (response[data_index] << 8) + response[data_index + 1]
            register_to_write = 1
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
                    ser.close()
                except Exception as e:
                    error_message = (
                        f"[{current_time}] Error writing to Holding Register: {e}"
                    )
                    print(error_message)
                    output.insert(END, error_message + "\n")
            except Exception as e:
                error_message = f"Error reading Modbus RTU: {e}"
                print(error_message)
                output.insert(END, error_message + "\n")
        except Exception as e:
            error_message = f"[{current_time}]Error reading input Register: {e}"
            print(error_message)
            output.insert(END, error_message + "\n")
    except Exception as e:
        error_message = f"Error reading modbus rtu: {e}"
        print(error_message)
        output.insert(END, error_message + "\n")
 
def slowdown():
    register_address = 30005
    numbers_to_read = 1
 
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
                    0x4,
                    (register_address >> 8) & 0xFF,
                    register_address & 0xFF,
                    0x00,
                    numbers_to_read,
                ]
            )
            ser.write(request)
            response = ser.read(5 + numbers_to_read * 2)
            print(response)
            data_index = 3
            value = (response[data_index] << 8) + response[data_index + 1]
            register_to_write = 1
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
                    ser.close()
                except Exception as e:
                    error_message = (
                        f"[{current_time}] Error writing to Holding Register: {e}"
                    )
                    print(error_message)
                    output.insert(END, error_message + "\n")
            except Exception as e:
                error_message = f"Error reading Modbus RTU: {e}"
                print(error_message)
                output.insert(END, error_message + "\n")
        except Exception as e:
            error_message = f"[{current_time}]Error reading input Register: {e}"
            print(error_message)
            output.insert(END, error_message + "\n")
    except Exception as e:
        error_message = f"Error reading modbus rtu: {e}"
        print(error_message)
        output.insert(END, error_message + "\n")
 
def shutdown():
    register_address = 1
    value = 0
 
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
            ser.close()
            output.insert(
                END,
                f"[{current_time}] Successfully written to Holding Register {register_address} - value {value}\n",
            )
        except Exception as e:
            error_message = f"[{current_time}] Error writing to Holding Register: {e}"
            print(error_message)
            output.insert(END, error_message + "\n")
    except Exception as e:
        error_message = f"Error reading Modbus RTU: {e}"
        print(error_message)
        output.insert(END, error_message + "\n")
 
 
#Функции управления Trashhold
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
            ser.write(request)
            response = ser.read(5 + numbers_to_read * 2)
            print(response)
            data_index = 3
            value = (response[data_index] << 8) + response[data_index + 1]
            register_to_write = 2
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
                    ser.close()
                except Exception as e:
                    error_message = (
                        f"[{current_time}] Error writing to Holding Register: {e}"
                    )
                    print(error_message)
                    output.insert(END, error_message + "\n")
            except Exception as e:
                error_message = f"Error reading Modbus RTU: {e}"
                print(error_message)
                output.insert(END, error_message + "\n")
        except Exception as e:
            error_message = f"[{current_time}]Error reading input Register: {e}"
            print(error_message)
            output.insert(END, error_message + "\n")
    except Exception as e:
        error_message = f"Error reading modbus rtu: {e}"
        print(error_message)
        output.insert(END, error_message + "\n")
 
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
            ser.write(request)
            response = ser.read(5 + numbers_to_read * 2)
            print(response)
            data_index = 3
            value = (response[data_index] << 8) + response[data_index + 1]
            register_to_write = 2
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
                    ser.close()
                except Exception as e:
                    error_message = (
                        f"[{current_time}] Error writing to Holding Register: {e}"
                    )
                    print(error_message)
                    output.insert(END, error_message + "\n")
            except Exception as e:
                error_message = f"Error reading Modbus RTU: {e}"
                print(error_message)
                output.insert(END, error_message + "\n")
        except Exception as e:
            error_message = f"[{current_time}]Error reading input Register: {e}"
            print(error_message)
            output.insert(END, error_message + "\n")
    except Exception as e:
        error_message = f"Error reading modbus rtu: {e}"
        print(error_message)
        output.insert(END, error_message + "\n")
 
def trh_write():
    register_address = 2
    value = int(value_trh_entry.get())
 
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
            ser.close()
            output.insert(
                END,
                f"[{current_time}] Successfully written to Holding Register {register_address} - value {value}\n",
            )
        except Exception as e:
            error_message = f"[{current_time}] Error writing to Holding Register: {e}"
            print(error_message)
            output.insert(END, error_message + "\n")
    except Exception as e:
        error_message = f"Error reading Modbus RTU: {e}"
        print(error_message)
        output.insert(END, error_message + "\n")
 
 
#Функции управления логированием в строку
def start_logging():
    global is_logging
    is_logging = True
    read_holding()
 
def stop_loging():
    global is_logging
    is_logging = False
 

#Функции управления чтением на основной экран
def start_reading():
    global is_reading
    is_reading = True
    start_button.config(
        background="green", font=("Arial", 10, "bold"), foreground="white"
    )
    read_holding_30001_30014()
 
def stop_reading():
    global is_reading
    is_reading = False
    start_button.config(
        background="#f0f0f0", font=("Arial", 10, "bold"), foreground="black"
    )
 

#Функции управления тестовыми запросами
def start_test_reading():
    global is_testing
    is_testing = True
    read_holding_test()
 
def stop_test_reading():
    global is_testing
    is_testing = False
 

#Очистка поля вывода
def clear_output():
    output.delete(1.0, END)
 

#Преобразование в процент 
def convert_to_percentage(value):
    return (value * 100) / 2000

#Расчет накопленной кинетической энергии
def accumulated_kinetic_energy(moment_of_innertion, rpm):
    kinetic_energy = (moment_of_innertion **2)/2 * rpm
    return kinetic_energy

def write_moment_of_inertia():
    global moment_of_inertia
    moment_of_inertia = int(inertia_value_entry.get())
    return moment_of_inertia
 
def resize_window(event):
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    output.place(x=10, y=70, width=window_width - 30, height=window_height - 200)
    output_test.place(x=10, y=70, width=window_width - 30, height=window_height - 200)
 
    if root.attributes("-fullscreen"):
        clear_button.place(x=10, y=window_height - 130, width=100)
        start_button.place(x=120, y=window_height - 130, width=100)
        stop_button.place(x=230, y=window_height - 130, width=100)
        write_button.place(x=10, y=window_height - 130, width=100)
        start_button_test.place(x=100, y=window_height - 130, width=120)
        stop_button_test.place(x=230, y=window_height - 130, width=100)
        start_loging_button.place(x=120, y=window_height - 130, width=100)
        stop_loging_button.place(x=230, y=window_height - 130, width=100)
        acceleration_button.place(x=340, y=window_height - 130, width=100)
        slowdown_button.place(x=450, y=window_height - 130, width=100)
        shutdown_button.place(x=560, y=window_height - 130, width=100)

    else:
        clear_button.place(x=10, y=window_height - 70, width=100)
        start_button.place(x=120, y=window_height - 70, width=100)
        stop_button.place(x=230, y=window_height - 70, width=100)
        write_button.place(x=10, y=window_height - 70, width=100)
        start_button_test.place(x=100, y=window_height - 70, width=120)
        stop_button_test.place(x=230, y=window_height - 70, width=100)
        start_loging_button.place(x=120, y=window_height - 70, width=100)
        stop_loging_button.place(x=230, y=window_height - 70, width=100)
        acceleration_button.place(x=340, y=window_height - 70, width=100)
        slowdown_button.place(x=450, y=window_height - 70, width=100)
        shutdown_button.place(x=560, y=window_height - 70, width=100)

 
    scrollbar.place(x=window_width - 20, y=70, height=window_height - 200)
 
 
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
 
 
output = Text(tab1)
output.pack(fill=BOTH, expand=True)
 
output_test = Text(tab3)
output_test.pack(fill=BOTH, expand=True)
 
output_30001 = Text(tab4)
output_30001.place(x=150, y=10, width=50, height=25)
 
output_30002 = Text(tab4)
output_30002.place(x=150, y=50, width=50, height=25)
 
output_30003 = Text(tab4)
output_30003.place(x=150, y=90, width=50, height=25)
 
output_30004 = Text(tab4)
output_30004.place(x=150, y=130, width=50, height=25)
 
output_30005 = Text(tab4)
output_30005.place(x=350, y=10, width=50, height=25)
 
output_30006 = Text(tab4)
output_30006.place(x=350, y=50, width=50, height=25)
 
output_30007 = Text(tab4)
output_30007.place(x=350, y=90, width=50, height=25)
 
output_30008 = Text(tab4)
output_30008.place(x=350, y=130, width=50, height=25)
 
output_30009 = Text(tab4)
output_30009.place(x=150, y=400, width=50, height=25)
 
output_30010 = Text(tab4)
output_30010.place(x=150, y=200, width=50, height=25)
 
output_30011 = Text(tab4)
output_30011.place(x=150, y=240, width=50, height=25)

output_30012 = Text(tab4)
output_30012.place(x=150, y=280, width=50, height=25)

output_30013 = Text(tab4)
output_30013.place(x=150, y=320, width=50, height=25)

output_30014 = Text(tab4)
output_30014.place(x=150, y=360, width=50, height=25)
 
 
output_30005_percent = Text(tab4)
output_30005_percent.place(x=450, y=10, width=50, height=25)
 
output_30006_percent = Text(tab4)
output_30006_percent.place(x=450, y=50, width=50, height=25)
 
output_30007_percent = Text(tab4)
output_30007_percent.place(x=450, y=90, width=50, height=25)
 
output_30008_percent = Text(tab4)
output_30008_percent.place(x=450, y=130, width=50, height=25)

accumulated_kinetic_energy_output = Text(tab4)
accumulated_kinetic_energy_output.place(x=150, y=440, width=50, height=25)

window_width = 800
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = int((screen_width - window_width) / 2)
y = int((screen_height - window_height) / 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")
 
scrollbar = Scrollbar(tab1, command=output.yview)
scrollbar.pack(side=RIGHT, fill=Y)
output.configure(yscrollcommand=scrollbar.set)
 
 
def auto_scroll():
    output.see("end")
    output.after(100, auto_scroll)
 
 
auto_scroll()
 
 
starting_adress_label = Label(
    tab1,
    text="Стартовый адрес",
    font=("Arial", 10, "bold"),
    foreground="white",
    background="#424242",
)
starting_adress_label.place(x=10, y=10)
 
starting_adress_entry = Entry(tab1)
starting_adress_entry.place(x=200, y=10)
 
numbers_to_read_label = Label(
    tab1,
    text="Количество регистров",
    font=("Arial", 10, "bold"),
    foreground="white",
    background="#424242",
)
numbers_to_read_label.place(x=10, y=40)
 
numbers_to_read_entry = Entry(tab1)
numbers_to_read_entry.place(x=200, y=40)
 
start_loging_button = Button(
    tab1,
    text="Пуск",
    command=start_logging,
    font=("Arial", 10, "bold"),
    foreground="black",
)
start_loging_button.pack()
 
stop_loging_button = Button(
    tab1,
    text="Стоп",
    command=stop_loging,
    font=("Arial", 10, "bold"),
    foreground="black",
)
stop_loging_button.pack()
 
start_button = Button(
    tab4,
    text="Пуск",
    command=start_reading,
    font=("Arial", 10, "bold"),
    foreground="black",
)
start_button.pack()
 
stop_button = Button(
    tab4,
    text="Стоп",
    command=stop_reading,
    font=("Arial", 10, "bold"),
    foreground="black",
)
start_button.pack()
 
 
#Кнопки управления PWM (разгон, торможение, стоп)
acceleration_button = Button(
    tab4,
    text="Разгон",
    command=acceleration,
    font=("Arial", 10, "bold"),
    foreground="black",
)
acceleration_button.pack()
slowdown_button = Button(
    tab4,
    text="Замедление",
    command=slowdown,
    font=("Arial", 10, "bold"),
    foreground="black",
)
slowdown_button.pack()
shutdown_button = Button(
    tab4,
    text="Остановка",
    command=shutdown,
    font=("Arial", 10, "bold"),
    foreground="black",
)
shutdown_button.pack()
 
#Кнопки управления Trashhold
trh_plus_button = Button(
    tab4,
    text="+",
    command=trh_plus,
    font=("Arial", 10, "bold"),
    foreground="black",
)
trh_plus_button.pack()
trh_plus_button.place(x=230, y=window_height - 360, width=40, height=25)
trh_minus_button = Button(
    tab4,
    text="-",
    command=trh_minus,
    font=("Arial", 10, "bold"),
    foreground="black",
)
trh_minus_button.pack()
trh_minus_button.place(x=280, y=window_height - 360, width=40, height=25)
value_trh_label = Label(
    tab4,
    text="Новый TRH",
    font=("Arial", 10, "bold"),
    foreground="white",
    background="#424242",
)
value_trh_label.place(x=340, y=240)
value_trh_entry = Entry(tab4)
value_trh_entry.place(x=430, y=240, width=60, height=25)
write_trh_button = Button(
    tab4,
    text="Отправить",
    command=trh_write,
    font=("Arial", 10, "bold"),
    foreground="black",
)
write_trh_button.pack()
write_trh_button.place(x=520, y=window_height - 360, width=100, height=25)

#Кнока расчета накопленной кинетической єнергии 
accumulated_kinetic_energy_label = Label(
    tab4,
    text="Момент иннерции",
    font=("Arial", 10, "bold"),
    foreground="white",
    background="#424242",
)
accumulated_kinetic_energy_label.place(x=300, y=440)
inertia_value_entry = Entry(tab4)
inertia_value_entry.place(x=430, y=440, width=60, height=25)
write_inertia_value_button = Button(
    tab4,
    text="Отправить",
    command=write_moment_of_inertia,
    font=("Arial", 10, "bold"),
    foreground="black",
)
write_inertia_value_button.pack()
write_inertia_value_button.place(x=520, y=window_height - 160, width=100, height=25)
 
 
 
clear_button = Button(
    tab1,
    text="Очистить",
    command=clear_output,
    font=("Arial", 10, "bold"),
    foreground="black",
)
clear_button.pack()
 
start_button_test = Button(
    tab3,
    text="Пуск для теста",
    command=start_test_reading,
    font=("Arial", 10, "bold"),
    foreground="black",
)
start_button.pack()
 
stop_button_test = Button(
    tab3,
    text="Стоп тест",
    command=stop_test_reading,
    font=("Arial", 10, "bold"),
    foreground="black",
)
start_button.pack()
 
register_address_label = Label(
    tab2,
    text="Адрес регистра",
    font=("Arial", 10, "bold"),
    foreground="white",
    background="#424242",
)
register_address_label.place(x=10, y=10)
 
register_address_entry = Entry(tab2)
register_address_entry.place(x=200, y=10)
 
value_label = Label(
    tab2,
    text="Значение",
    font=("Arial", 10, "bold"),
    foreground="white",
    background="#424242",
)
value_label.place(x=10, y=40)
 
value_entry = Entry(tab2)
value_entry.place(x=200, y=40)
 
write_button = Button(
    tab2,
    text="Отправить",
    command=write_holding,
    font=("Arial", 10, "bold"),
    foreground="black",
)
write_button.pack()
 

value_30001_label = Label(
    tab4,
    text="ADC(I1)",
    font=("Arial", 10, "bold"),
    foreground="white",
    background="#424242",
)
value_30001_label.place(x=10, y=10)
value_30002_label = Label(
    tab4,
    text="ADC(I2)",
    font=("Arial", 10, "bold"),
    foreground="white",
    background="#424242",
)
value_30002_label.place(x=10, y=50)
value_30003_label = Label(
    tab4,
    text="ADC(I3)",
    font=("Arial", 10, "bold"),
    foreground="white",
    background="#424242",
)
value_30003_label.place(x=10, y=90)
value_30004_label = Label(
    tab4,
    text="ADC(I4)",
    font=("Arial", 10, "bold"),
    foreground="white",
    background="#424242",
)
value_30004_label.place(x=10, y=130)
value_30005_label = Label(
    tab4,
    text="PWM1",
    font=("Arial", 10, "bold"),
    foreground="white",
    background="#424242",
)
value_30005_label.place(x=250, y=10)
value_30006_label = Label(
    tab4,
    text="PWM2",
    font=("Arial", 10, "bold"),
    foreground="white",
    background="#424242",
)
value_30006_label.place(x=250, y=50)
value_30007_label = Label(
    tab4,
    text="PWM3",
    font=("Arial", 10, "bold"),
    foreground="white",
    background="#424242",
)
value_30007_label.place(x=250, y=90)
value_30008_label = Label(
    tab4,
    text="PWM4",
    font=("Arial", 10, "bold"),
    foreground="white",
    background="#424242",
)
value_30008_label.place(x=250, y=130)
value_30009_label = Label(
    tab4,
    text="RPM",
    font=("Arial", 10, "bold"),
    foreground="white",
    background="#424242",
)
value_30009_label.place(x=10, y=400)
value_30010_label = Label(
    tab4,
    text="Frequency",
    font=("Arial", 10, "bold"),
    foreground="white",
    background="#424242",
)
value_30010_label.place(x=10, y=200)
value_30011_label = Label(
    tab4,
    text="Trashold",
    font=("Arial", 10, "bold"),
    foreground="white",
    background="#424242",
)
value_30011_label.place(x=10, y=240)
value_30012_label = Label(
    tab4,
    text="ADDR",
    font=("Arial", 10, "bold"),
    foreground="white",
    background="#424242",
)
value_30012_label.place(x=10, y=280)
value_30013_label = Label(
    tab4,
    text="VDC",
    font=("Arial", 10, "bold"),
    foreground="white",
    background="#424242",
)
value_30013_label.place(x=10, y=320)
value_30014_label = Label(
    tab4,
    text="ADC",
    font=("Arial", 10, "bold"),
    foreground="white",
    background="#424242",
)
value_30014_label.place(x=10, y=360)
accumulated_kinetic_energy_output_label = Label(
    tab4,
    text="Energy",
    font=("Arial", 10, "bold"),
    foreground="white",
    background="#424242",
)
accumulated_kinetic_energy_output_label.place(x=10, y=440) 

def update_indicator_color(value):
    register_value = value()

    if register_value >= 200 and register_value <=500: 
        indicator.config(circle, bg="green")
    else: 
        indicator.config(circle, bg="red")

indicator = Canvas(root, width=10, height=10, borderwidth=0, highlightthickness=0)
indicator.pack()
indicator.place(x=120, y=270)

center_x = 50
center_y = 50
radius = 40
circle = indicator.create_oval(
    center_x - radius, center_y - radius, center_x + radius, center_y + radius, fill="grey"
)

root.bind("<Configure>", resize_window)
 
root.mainloop()
