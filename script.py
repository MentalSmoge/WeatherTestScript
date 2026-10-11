import json
import os
import urllib.parse
import urllib.request
from datetime import datetime


class WeatherData:
    def __init__(self, city: str, temp_c: int, country: str,
                 humidity: int, wind_kmph: int):
        self.city = city
        self.temp_c = temp_c
        self.country = country
        self.humidity = humidity
        self.wind_kmph = wind_kmph


def load_cities(filename: str):
    with open(filename, encoding="utf-8-sig") as f:
        return [line.strip() for line in f if line.strip()]


def get_weather(city: str) -> WeatherData:
    url = f"https://wttr.in/{urllib.parse.quote(city)}?format=j1"

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.load(response)

    current = data["current_condition"][0]

    temp_c   = int(current["temp_C"])
    humidity = int(current["humidity"])
    wind     = int(current["windspeedKmph"])
    country  = data["nearest_area"][0]["country"][0]["value"]

    return WeatherData(city, temp_c, country, humidity, wind)


def build_report() -> str:
    lines = []

    now = datetime.now()
    lines.append(f"Date:  {now.strftime('%d.%m.%Y %H:%M:%S')}")
    lines.append("")

    cities = []
    seen = set()
    for city in load_cities("Cities.txt"):
        if city not in seen:
            seen.add(city)
            cities.append(city)

    lines.append("Cities:")
    city_header = (
        f"{'City':<20}"
        f"{'Country':<18}"
        f"{'Temp':>8}"
        f"{'Humidity':>10}"
        f"{'Wind':>8}"
    )
    city_line = "-" * len(city_header)
    lines.append(city_header)
    lines.append(city_line)

    weather_data = []
    for city in cities:
        try:
            weather = get_weather(city)
            weather_data.append(weather)
            lines.append(
                f"{weather.city:<20}"
                f"{weather.country:<18}"
                f"{f'{weather.temp_c:+d} °C':>8}"
                f"{f'{weather.humidity} %':>10}"
                f"{f'{weather.wind_kmph} km/h':>8}"
            )
        except Exception as e:
            lines.append(f"{city:<20}{'-':<18}{'error':>8}  ({e})")

    lines.append(city_line)

    countries = {}
    for weather in weather_data:
        countries.setdefault(weather.country, []).append(weather)

    rows = []
    for country in sorted(countries):
        items = countries[country]
        temps = [w.temp_c for w in items]
        hums = [w.humidity for w in items]
        winds = [w.wind_kmph for w in items]

        count = len(items)
        avg_temp = round(sum(temps) / count)
        min_temp = min(temps)
        max_temp = max(temps)
        avg_hum = round(sum(hums) / count)
        avg_wind = round(sum(winds) / count)

        rows.append((country, count, avg_temp, min_temp, max_temp, avg_hum, avg_wind))

    w_country = max(len("Country"), max(len(r[0]) for r in rows)) + 2
    w_count   = max(len("Cities"), max(len(str(r[1])) for r in rows)) + 2
    w_avg     = len("Avg") + 4
    w_min     = len("Min") + 4
    w_max     = len("Max") + 4
    w_hum     = len("Humidity") + 4
    w_wind    = len("Wind") + 4

    header = (
        f"{'Country':<{w_country}}"
        f"{'Cities':>{w_count}}"
        f"{'Avg':>{w_avg}}"
        f"{'Min':>{w_min}}"
        f"{'Max':>{w_max}}"
        f"{'Humidity':>{w_hum}}"
        f"{'Wind':>{w_wind}}"
    )
    line = "-" * len(header)

    lines.append("")
    lines.append("Grouped by country:")
    lines.append(header)
    lines.append(line)

    for country, count, avg_temp, min_temp, max_temp, avg_hum, avg_wind in rows:
        lines.append(
            f"{country:<{w_country}}"
            f"{count:>{w_count}}"
            f"{f'{avg_temp:+d} °C':>{w_avg}}"
            f"{f'{min_temp:+d} °C':>{w_min}}"
            f"{f'{max_temp:+d} °C':>{w_max}}"
            f"{f'{avg_hum} %':>{w_hum}}"
            f"{f'{avg_wind} km/h':>{w_wind}}"
        )
    lines.append(line)

    return "\n".join(lines) + "\n"


def main():
    report = build_report()

    print(report, end="")

    os.makedirs("results", exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = os.path.join("results", f"weather_{stamp}.txt")

    with open(path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\nResults saved to: {path}")


if __name__ == "__main__":
    main()