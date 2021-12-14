import configparser
import time
import sys

import co2_sensor
import servo_motor
from send_data import send_data, send_data_toggle
from get_data import get_data


# import ggf. Bewegungsmelder
# import Datenbank_util

def main():
    # Parameters:
    # t = terminate/test
    valid_args = ["-t"]
    args = sys.argv

    for arg in args:
        if arg in valid_args:
            if arg == "-t":
                print("Starte im Testmodus.")
                is_loop = False

    sensor_instanz = co2_sensor.Sensor()
    servo_instanz = servo_motor.Servo_Motor(25, 0)

    # Lade configdatei
    config = configparser.ConfigParser()
    config.read('config.ini')
    control_config = config["program_control"]
    sensor_interval = control_config["sensor_sleep"]

    sensor_val: float
    is_fenster_open = False
    is_raum_movement = False
    is_loop = True
    is_state_changed = False

    try:
        while True:

            app_control = get_data(control_config["url"])
            if app_control is not None:
                app_mode = app_control["auto_toggle"]
                fenster_mode = app_control["toggle"]
                change_ini(config, app_control["temp_threshold"], app_control["co2_threshold"])
            else:
                fenster_mode = False
                app_mode = True
            print("Auto Mouds =" + str(app_mode))
            print("\n***********Sensing co2 in the luft***********")
            co2, tvoc, temp = sensor_instanz.get_values(5)
            print("CO2: {} PPM, TVOC: {} PPM, Temp: {} C"
                  .format(co2, tvoc, temp))

            send_data(control_config["url"], co2, temp, tvoc)

            if app_mode:
                is_fenster_open = sensor_run(config, is_fenster_open, servo_instanz, temp, co2)
                send_data_toggle(control_config["url"], is_fenster_open)
            elif fenster_mode:
                is_fenster_open = fenster_auf_zu(is_fenster_open, servo_instanz)
                send_data_toggle(control_config["url"], is_fenster_open)

            if not is_loop:
                send_data_toggle(control_config["url"], is_fenster_open)
                servo_instanz.cleanup()
                return
            time.sleep(int(sensor_interval))  # das hier wahrscheinlich dann Müll
    except KeyboardInterrupt:
        send_data_toggle(control_config["url"], is_fenster_open)
        servo_instanz.cleanup()


def fenster_auf_zu(is_fenster_open: bool, servo_instanz: servo_motor):
    if is_fenster_open:
        print("Fenster geht zu!")
        servo_instanz.setdirection(0, -10)

    else:
        print("Fenster geht auf!")
        servo_instanz.setdirection(50, 10)

    return not is_fenster_open


def sensor_run(config: configparser, is_fenster_open: bool, servo_instanz: servo_motor, temp: float, co2: float):
    temp_config = config["Temperature"]
    co2_config = config["Co2_content"]
    higher_temp = temp_config["temperature_high"]
    higher_co2 = co2_config["co2_high"]  # dieser Block ist ugly af

    if not is_fenster_open:
        if co2 > float(higher_co2) or temp > float(higher_temp):
            print("Fenster geht auf!")
            servo_instanz.setdirection(50, 10)
            is_fenster_open = True
            is_state_changed = True

    if is_fenster_open:
        if co2 < float(higher_co2) and temp < float(higher_temp):
            print("Fenster geht zu!")
            servo_instanz.setdirection(0, -10)
            is_fenster_open = False

    return is_fenster_open


def change_ini(config: configparser, app_temp: bool, app_co2: bool):
    config.set('Temperature', 'temperature_high', str(app_temp))
    config.set('Co2_content', 'co2_high', str(app_co2))

    with open('config.ini', 'w') as configfile:
        config.write(configfile)


if __name__ == '__main__':
    main()
