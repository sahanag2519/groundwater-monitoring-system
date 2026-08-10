def check_water_level(water_level, critical_level=2.0):

    if water_level <= critical_level:
        return "CRITICAL"

    elif water_level <= critical_level + 0.5:
        return "WARNING"

    else:
        return "NORMAL"


def check_tds(tds):

    if tds <= 500:
        return "NORMAL"

    elif tds <= 800:
        return "WARNING"

    else:
        return "CRITICAL"


def check_overall_status(water_level, tds):

    water_status = check_water_level(water_level)
    tds_status = check_tds(tds)

    if water_status == "CRITICAL" or tds_status == "CRITICAL":
        return "CRITICAL"

    elif water_status == "WARNING" or tds_status == "WARNING":
        return "WARNING"

    else:
        return "NORMAL"
print(check_water_level(1.8))
print(check_tds(900))
print(check_overall_status(1.8, 900))