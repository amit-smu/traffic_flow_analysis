from datetime import time

def decide_day_phase(time):
    """
    decides the phase of day (morning/noon/evening/night)
    :param time:
    :return:
    """

    hour = time.hour
    if hour >= 6 and hour <= 10: # till 10:59am 
        return 0
    elif hour >= 11 and hour <= 15:
        return 1
    elif hour >= 16 and hour <= 19:
        return 2
    else:
        return 3

DAY_PHASES = {
        0: "morning",  # 6am - 11 am
        1: "noon",  # 11am - 4 pm
        2: "evening",  # 4pm - 8 pm
        3: "night"  # 8 pm - 6 am
    }

t = time(hour=20, minute=30)
a = decide_day_phase(t)
print(t)
print(DAY_PHASES[a])
