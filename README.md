# Light alarm
This project makes possible to have an LED strip WS2812B as a light alarm.

## Components
Very simple project. Just three components
- Raspberry Pi 3 or above
- LED strip of type WS2812B + it own external power supply
- Jumper wires

## Configuration
It relies all configuration on a hjson file. 
In the future a configuration via API will be attempted. But for the time being, via configuration file it is. 
For a full reference of the configuration possibilities, please visit the [example configuration file](https://github.com/Johan3F/lightalarm/blob/master/config_example.hjson)

## References
- Heavily used [this tutorial](https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage) from adafruit