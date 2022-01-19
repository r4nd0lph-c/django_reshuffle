from datetime import datetime
from time import sleep


def create():
    """
    :return: UNIQUE_KEY in format XXX-XXX-XXX
    """

    # declaration of the characters used to create the key
    DIGITS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    # creating a seed based on the current date and time
    sleep(0.01)
    seed = int(datetime.now().strftime('%Y%m%d%H%M%S%f')[2:-4])

    # converting a seed to a new number system (base = 36) using DIGITS
    key = []
    while seed:
        key.append(DIGITS[seed % len(DIGITS)])
        seed //= len(DIGITS)
    key = ''.join(reversed(key))

    # returning the key in a human-readable format
    return key[:3] + '-' + key[3:6] + '-' + key[6:]


if __name__ == '__main__':
    print(create())
