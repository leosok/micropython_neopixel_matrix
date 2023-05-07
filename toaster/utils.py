# utils.py

def format_ticks(ticks_diff):
    seconds = ticks_diff // 1000
    minutes, seconds = divmod(seconds, 60)

    if minutes > 0:
        return "{:02d}{:02d}".format(minutes, seconds)
    else:
        return "{:02d}".format(seconds)
