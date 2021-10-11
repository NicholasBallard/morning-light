from datetime import datetime, timedelta
from functools import wraps
import RPi.GPIO as GPIO
from typing import Callable, ParamSpec, TypeVar
import suntime

import config


# see: https://realpython.com/python310-new-features/#type-unions-aliases-and-guards
P = ParamSpec("P")  # Params
R = TypeVar("R")  # Return type

input_pin: int


""" optional but won't do to KISS
from functools import partial

light = partial(GPIO.output, input_pin)
"""


def exception_handler(f: Callable[P, R]) -> Callable[P, R]:
    @wraps(f)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            return f(*args, **kwargs)
        except KeyboardInterrupt:
            GPIO.cleanup()
    return wrapper


# set board configuration
def setup() -> None:
    global input_pin;
    input_pin = config.GPIO_LIGHT_PIN
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(input_pin, GPIO.OUT)
    GPIO.output(input_pin, False)  # send off signal


# get sunrise or sunset
def get_sun_time(sun_time: str, offset: int = None) -> datetime:
    try:
        sun = suntime.Sun(config.LONGITUDE, config.LATITUDE)
    except suntime.SunTimeException as e:
        print(f"Error: {e}")
    fn = sun.get_local_sunrise_time if sun_time == "sunrise" else sun.get_local_sunset_time
    if offset:
        date = datetime.today() + timedelta(days=offset)
    else:
        date = datetime.today()
    return fn(date)


# turn on lamp
def turn_on() -> None:
    ...


# main loop
@exception_handler
def main() -> None:
    setup()
    turn_on()


if __name__ == '__main__':
    main()
