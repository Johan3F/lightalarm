import time
import asyncio
import logging
import datetime
from dateutil.rrule import *

import hjson
import argparse
import board
import neopixel

LED_AMOUNT = 40
PIN = board.D18
PIXEL_ORDER = neopixel.RGB
YELLOW = (10, 255 , 110) # With RGB mode, Neopixel works as BRG


def setup_arguments():
    parser = argparse.ArgumentParser(prog = 'Light alarm', description = 'A Program to wake you up via an LED strip')
    parser.add_argument('config_file', type=str, default="config.yml", help='path to the configuration file. Must be a yml file')
    args = parser.parse_args()
    return args

def parse_config(path):
    with open(path) as file:
        alarm_config = hjson.loads(file.read())
        return alarm_config

def turn_off_led(led_strip):
    led_strip.brightness = 0

def initialize_led():
    led_strip = neopixel.NeoPixel(PIN, LED_AMOUNT, pixel_order=PIXEL_ORDER, auto_write=True, brightness=0)
    led_strip.fill(YELLOW)
    turn_off_led(led_strip)
    return led_strip

async def run_at(dt, coro):
    now = datetime.datetime.now()
    await asyncio.sleep((dt - now).total_seconds())
    return await coro

def day_string_to_number(day_str):
    DAYS = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6,
    }
    return DAYS[day_str.lower()]

async def ring_alarm(led_strip, minutes_to_run, last_for_minutes_after_alarm):
    steps = (minutes_to_run*60)*24
    step_time = (minutes_to_run/steps)*60 # Seconds
    brightness_step_size = 1/steps
    start = datetime.datetime.now()


    logging.info(f"Starts ringing alarm at {start} for {minutes_to_run} minutes incrementing {brightness_step_size} every {step_time} seconds")
    brightness = 0
    while datetime.datetime.now() < (start + datetime.timedelta(minutes=minutes_to_run)):
        brightness += brightness_step_size
        led_strip.brightness = brightness

        logging.debug(f"Step: brightness = {brightness}")
        time.sleep(step_time)
    
    logging.info(f"Fade in done. Waiting now {last_for_minutes_after_alarm} minutes ")
    time.sleep(last_for_minutes_after_alarm*60)
    turn_off_led(led_strip)

async def setup_alarms(led_stripe, alarm_config):
    now = datetime.datetime.now()
    raw_alarm = datetime.datetime.strptime(alarm_config['time'], '%H:%M')

    days = [day_string_to_number(day) for day in alarm_config['days']]

    alarm = list(rrule(freq=DAILY, count=10, dtstart=now, byweekday=days, byhour=raw_alarm.hour, byminute=raw_alarm.minute, bysecond=raw_alarm.second))[0]
    logging.info(f"Next alarm to ring: {alarm}")

    await run_at(alarm, ring_alarm(led_stripe, alarm_config['fade_in_minutes'], alarm_config['last_for_minutes_after_alarm']))


async def main():
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    args = setup_arguments()
    led_stripe = initialize_led()

    alarm_config = parse_config(args.config_file)
    logging.debug(f"Running with configuration: {alarm_config}")
    while True:
        await setup_alarms(led_stripe, alarm_config)
        turn_off_led(led_stripe)

if __name__ == "__main__":
    asyncio.run(main())