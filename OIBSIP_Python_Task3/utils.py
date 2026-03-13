import math

def extract_features(password):

    length = len(password)

    charset = 0

    if any(c.islower() for c in password):
        charset += 26

    if any(c.isupper() for c in password):
        charset += 26

    if any(c.isdigit() for c in password):
        charset += 10

    if any(not c.isalnum() for c in password):
        charset += 32

    entropy = length * math.log2(charset) if charset > 0 else 0

    strength = entropy / 100

    return strength, length, entropy


def convert_time(seconds):

    seconds = int(seconds)

    if seconds == 0:
        return "instant"

    minutes = seconds / 60

    if minutes < 60:
        return str(round(minutes,2)) + " minutes"

    hours = minutes / 60

    if hours < 24:
        return str(round(hours,2)) + " hours"

    days = hours / 24

    if days < 365:
        return str(round(days,2)) + " days"

    return "Practically Uncrackable"