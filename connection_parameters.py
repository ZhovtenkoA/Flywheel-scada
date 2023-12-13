port = (
    "/dev/ttyUSB0"  # Порт, к которому подключено устройство (ваш порт может отличаться)
)
baudrate = 230400  # Скорость передачи данных
parity = "N"  # Четность: 'N' - нет, 'E' - четная, 'O' - нечетная
stopbits = 1  # Количество стоп-битов
bytesize = 8  # Размер байта
slave_id = 1
timeout = 2

ser = None

is_reading = False
is_testing = False
is_logging = False


moment_of_inertia = 0.3