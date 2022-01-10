import weather_wrapper
import os
import pycountry
from datetime import datetime, timedelta
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
if os.path.exists('env.py'):
    import env  # noqa

message = ""
data_message = ""
country_tuples = []

for i in pycountry.countries:
    country_tuples.append((i.name, i.alpha_2))


country_list = [y[0] for y in country_tuples]


def print_banner():
    print("☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ")
    print(" __          __        _   _   ")
    print(" \ \        / /       | | | |  ")
    print("  \ \  /\  / /__  __ _| |_| |__   ___ _ __   _ __  _   _ ")
    print("   \ \/  \/ / _ \/ _` | __| '_ \ / _ \ '__| | '_ \| | | |")
    print("    \  /\  /  __/ (_| | |_| | | |  __/ |    | |_) | |_| |")
    print("     \/  \/ \___|\__,_|\__|_| |_|\___|_|    | .__/ \__, |")
    print("                                            | |     __/ |")
    print("                                            |_|    |___/ \n")
    print("☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ☁ ")


def print_menu():
    print(message)
    print("1) Get Todays Weather")
    print("2) See the forecast for next 5 days")
    print("3) Get last 5 days weather")
    print("4) Number Four")
    print(data_message)


def get_selection_country():
    country_completer = WordCompleter(country_list)
    while True:
        os.system("clear")
        print_banner()
        print("Note: Auto completer is case sensitive")
        text = prompt("> Enter a country: ", completer=country_completer)
        if text in country_list:
            return text
        print("Please select a country using the auto completer")


def get_selection_town():
    return input("> Enter Town Name : ")


def get_todays_weather():
    country = get_selection_country()
    town = get_selection_town()
    current_weather = weather.get_current_weather(country, town)

    sunrise = datetime.utcfromtimestamp(
        int(current_weather['sys']['sunrise'])).strftime('%H:%M:%S')
    sunset = datetime.utcfromtimestamp(
        int(current_weather['sys']['sunset'])).strftime('%H:%M:%S')

    return (
        f"\nAt a temperature of {current_weather['main']['temp']}c "
        f"with lows of {round(current_weather['main']['temp_min'])}c "
        f"and highs of {round(current_weather['main']['temp_max'])}c\n"
        f"A {current_weather['main']['humidity']}% humidity and " 
        f"{current_weather['clouds']['all']}% cloud coverage\n"
        f"Sunrise at {sunrise} and Sunset at {sunset}"
    )


def get_forecast():
    country = get_selection_country()
    town = get_selection_town()
    full_forecast = weather.get_full_forecast(country, town)

    text = ""
    for forecast in full_forecast:
        text += f"{forecast['dt_txt']} {forecast['main']['temp']}\n"
    return text


def get_previous_weather():
    country = get_selection_country()
    town = get_selection_town()

    start_date = datetime.now().date()

    return_data = []

    # Loop for each of 5days from today
    for i in range(0, 6):
        date = start_date - timedelta(days=i)
        api_data = weather.get_historical_weather(country, town, str(date))

        # date - temp - humidity - wind speed
        avg = ["", 0, 0, 0]
        count = 0
        for item in api_data["hourly"]:
            count += 1
            avg[1] += item["temp"]
            avg[2] += item["humidity"]
            avg[3] += item["wind_speed"]

        avg[0] = date

        # Get averages and round
        avg[1] = round(avg[1] / count, 2)
        avg[2] = round(avg[2] / count, 2)
        avg[3] = round(avg[3] / count, 2)
        return_data.append(avg)

    print("Note: Values are averages.")
    text = ""
    for data in get_previous_weather():
        text += (
            f"{str(data[0])} - Temperature @ {data[1]}c - "
            f"Humidity @ {data[2]} -"
            f"Windspeed @ {data[3]}mps\n")
    return text


weather = weather_wrapper.Weather(os.environ.get("API_KEY"))

while True:
    os.system("clear")
    print_banner()
    print_menu()
    selection = input("> ")
    if not selection.isdigit():
        os.system("clear")
        message = "Please enter a number from the list below!"
        print_banner()
        print_menu()
        continue

    if int(selection) > 4:
        os.system("clear")
        message = "Please enter a number from the list below!"
        print_banner()
        print_menu()
        continue

    message = ""
    data_message = ""
    os.system("clear")
    print_banner()
    print_menu()
    selection = int(selection)

    if selection == 1:
        print(get_todays_weather())

    if selection == 2:
        print(get_forecast())

    if selection == 3:
        print(get_previous_weather())

    if selection == 4:
        pass

    input("Press Enter to continue!")
