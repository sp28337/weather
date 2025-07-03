from datetime import datetime, timedelta


def weekday_short(date: str) -> str:
    if not date:
        return ""
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    return date_obj.strftime("%a")


def weather_svg(code: int) -> str:
    svg = {
        1000: "../static/svg/sunny.svg",
        1003: "../static/svg/partly-cloudy.svg",
        1006: "../static/svg/cloudy.svg",
        1009: "../static/svg/cloudy.svg",
        1030: "../static/svg/fog.svg",
        1063: "../static/svg/patchy-rain.svg",
        1066: "../static/svg/snow.svg",
        1069: "../static/svg/sleet.svg",
        1072: "../static/svg/snow.svg",
        1087: "../static/svg/thunder.svg",
        1114: "../static/svg/snow.svg",
        1117: "../static/svg/blizzard.svg",
        1135: "../static/svg/fog.svg",
        1147: "../static/svg/fog.svg",
        1150: "../static/svg/rain.svg",
        1153: "../static/svg/rain.svg",
        1168: "../static/svg/rain.svg",
        1171: "../static/svg/rain.svg",
        1180: "../static/svg/patchy-rain.svg",
        1183: "../static/svg/rain.svg",
        1186: "../static/svg/rain.svg",
        1189: "../static/svg/rain.svg",
        1192: "../static/svg/rain.svg",
        1195: "../static/svg/rain.svg",
        1198: "../static/svg/rain.svg",
        1201: "../static/svg/rain.svg",
        1204: "../static/svg/sleet.svg",
        1207: "../static/svg/sleet.svg",
        1210: "../static/svg/snow.svg",
        1213: "../static/svg/snow.svg",
        1216: "../static/svg/snow.svg",
        1219: "../static/svg/snow.svg",
        1222: "../static/svg/snow.svg",
        1225: "../static/svg/snow.svg",
        1237: "../static/svg/snow.svg",
        1240: "../static/svg/rain.svg",
        1243: "../static/svg/rain.svg",
        1246: "../static/svg/rain.svg",
        1249: "../static/svg/sleet.svg",
        1252: "../static/svg/sleet.svg",
        1255: "../static/svg/snow.svg",
        1258: "../static/svg/snow.svg",
        1261: "../static/svg/snow.svg",
        1264: "../static/svg/snow.svg",
        1273: "../static/svg/thunder.svg",
        1276: "../static/svg/thunder.svg",
        1279: "../static/svg/thunder.svg",
        1282: "../static/svg/thunder.svg"
    }
    return svg.get(code, "../static/svg/partly-cloudy.svg")


def time_converter(time: str) -> str:
    if time == "No moonset":
        return time
    time_obj = datetime.strptime(time, "%I:%M %p")
    return time_obj.strftime("%H:%M")


def set_time(time: str) -> str:
    scheduled_time = datetime.strptime(time, "%Y-%m-%d %H:%M")
    current_time = datetime.now()
    if current_time.hour == scheduled_time.hour:
        return "Now"
    else:
        return scheduled_time.strftime("%H:%M")


def datetime_filter(time: str) -> str:
    time_obj = datetime.strptime(time, "%Y-%m-%d %H:%M")
    return time_obj.strftime("%A, %B %d")


def get_next_hours(hourly_weather_list: list) -> list:
    current_time = datetime.now()
    result = []
    for hourly_weather in hourly_weather_list:
        if len(result) > 5:
            break
        elif datetime.strptime(hourly_weather['time'], "%Y-%m-%d %H:%M") >= current_time - timedelta(hours=1):
            result.append(hourly_weather)
    return result
