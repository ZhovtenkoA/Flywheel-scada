from datetime import datetime

adc0 = 1171

#Преобразование в процент 
def convert_to_percentage(value):
    return (value * 100) / 2000

#Расчет накопленной кинетической энергии
def accumulated_kinetic_energy(moment_of_innertia, rpm):
    axillar_speed = (rpm*3.14)/30
    kinetic_energy = float(moment_of_innertia)*(axillar_speed **2/2)
    kinetic_energy = round(kinetic_energy, 2)
    return kinetic_energy


#Функция конвертации VDC -> V
def convert_VDC(vdc):
    V = (vdc*24.4*3.3) / 4096 
    #0.01893310546
    V = round(V, 2)
    return V

#Функция конвертации ADC -> A
def convert_ADC(adc):
    A = ((adc - adc0) * 3.3) / 4096 * 10/6.4 * 1/0.0133
    # A = (adc - adc0) * 330 / 33.775
    A = round(A, 2)
    return A

#Функция получения мощности
def make_P(adc, vdc):
    P = adc * vdc
    # A = (adc - adc0) * 330 / 33.775
    P = round(P, 2)
    return P
