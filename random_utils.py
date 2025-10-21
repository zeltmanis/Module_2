import random
import datetime

class SerialNumberGenerator:
    used_serials = set()

    @classmethod
    def generate_serial(cls):
        # Get current day of the week (Monday = 1, Sunday = 7)
        day_code = datetime.datetime.today().isoweekday()  # 1 to 7

        while True:
            random_part = f"{random.randint(0, 999):03d}"  # 3-digit random
            serial = f"{day_code}{random_part}"  # e.g. '3123'

            if serial not in cls.used_serials:
                cls.used_serials.add(serial)
                return serial