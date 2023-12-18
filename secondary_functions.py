from datetime import datetime

adc0 = 1174

#Преобразование в процент 
def convert_to_percentage(value):
    return (value * 100) / 2000

#Расчет накопленной кинетической энергии
def accumulated_kinetic_energy(moment_of_innertia, rpm):
    axillar_speed = (rpm*3.14)/30
    kinetic_energy = float(moment_of_innertia)*(axillar_speed **2/2)
    kinetic_energy = round(kinetic_energy, 2)
    return kinetic_energy

#Расчет Accumulated Energy, кВт*ч
def accumulated_energy_kW_h(VDC, ADC, t2, t1):
    time_diff = datetime.combine(datetime.date.today(), t2) - datetime.combine(datetime.date.today(), t1)
    seconds = time_diff.total_seconds()
    kW_h = VDC * ADC * seconds/ 3600
    return kW_h

#Функция конвертации VDC -> V
def convert_VDC(vdc):
    V = (vdc*24.4*3.3) / 4096 
    #0.01893310546
    V = round(V, 2)
    return V

#Функция конвертации ADC -> A
def convert_ADC(adc):
    #A = ((adc - adc0) * 3.3) / 4096 * 10/6.2 * 1/0.00133
    A = (adc - adc0) * 330 / 33.775
    return A
