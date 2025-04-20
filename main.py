from machine import Pin, ADC, PWM
from utime import sleep

print("Modules initialized")

pot = ADC(28) # potentiometer - from 0-65535
pos = 0 # position - needs to be clamped from 1802 to 7864 for servo

servo = PWM(Pin(0, mode=Pin.OUT))
servo.freq(50)

target_threshold = 600 # how close something needs to be before acquisition begins
acq_threshold = 10 # how many consecutive sleep cycles where enemy needs targeted before target is acquired
acq_clock = 0 # used in while loop to track

green1 = Pin(1, mode=Pin.OUT)
green2 = Pin(2, mode=Pin.OUT)
yellow1 = Pin(3, mode=Pin.OUT)
yellow2 = Pin(4, mode=Pin.OUT)
red1 = Pin(5, mode=Pin.OUT)
red2 = Pin(6, mode=Pin.OUT)

jam_indicator = Pin(26, mode=Pin.OUT)
is_jammed = 0

win_indicator = Pin(21, mode=Pin.OUT)

# simulated enemy position
enemy_pos = 3236

def check_jam():
    # placeholder to see if signal strength is too great, indicating jam
    return 0

def check_track(enemy_pos, pos, target_threshold):
    delta_pos = abs(enemy_pos-pos)
    is_acquiring_target = 0
    if delta_pos < target_threshold:
        is_acquiring_target = 1

    if delta_pos < 2500:
        red2.on()
        if delta_pos < 1750:
            red1.on()
            if delta_pos < 1250:
                yellow2.on()
                if delta_pos < 900:
                    yellow1.on()
                    if delta_pos < 600:
                        green2.on()
                        if delta_pos < 300:
                            green1.on()
                        else:
                            green1.off()
                    else:
                        green1.off()
                        green2.off()
                else:
                    green1.off()
                    green2.off()
                    yellow1.off()
            else:
                green1.off()
                green2.off()
                yellow1.off()
                yellow2.off()
        else:
            green1.off()
            green2.off()
            yellow1.off()
            yellow2.off()
            red1.off()
    else:
        green1.off()
        green2.off()
        yellow1.off()
        yellow2.off()
        red1.off()
        red2.off()
    return is_acquiring_target


while True:
    pos = round(((pot.read_u16()/65535) * 5802) + 1802)
    print(f"Position: {pos}")
    servo.duty_u16(pos)
    
    is_jammed = check_jam()
    if is_jammed == 0:
        track_bool = check_track(enemy_pos, pos, target_threshold)
        if track_bool == 1:
            acq_clock += 1
        else:
            acq_clock = 0;

    if acq_clock >= acq_threshold:
        print("Target acquired! Victory!!")
        win_indicator.on()

    sleep(0.3)