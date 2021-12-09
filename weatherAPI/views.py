import requests
from django.shortcuts import render
from configuration.models import ConfigurationFieldModel
from .models import HistoricWeatherModel
from .forms import HistoricWeatherForm
import requests
import datetime

def realTimeWeather(request):
    daily_weather_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=65af3b064c12ac4914679061cdd62db8&lang=es'


    city = ConfigurationFieldModel.objects.get(id=1)

    weather_data = requests.get(daily_weather_url.format(city)).json()

    weather = {
        'city' : city.ciudad,
        'temperature' : weather_data['main']['temp'],
        'temperature_min': weather_data['main']['temp_min'],
        'temperature_max': weather_data['main']['temp_max'],
        'humidity' : weather_data['main']['humidity'],
        'description' : weather_data['weather'][0]['description'],
        'icon' : weather_data['weather'][0]['icon'],
    }

    if weather_data['weather'][0]['main'] == "rain":
        weather["precipitation"] = 1
    else:
        weather["precipitation"] = 0

    HistoricWeatherValues=HistoricWeatherForm(data=weather)
    HistoricWeatherValues.save()

    forecast_weather_url = 'http://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&appid=65af3b064c12ac4914679061cdd62db8&lang=es'

    a = forecast_weather_url.format(city)
    #accessing the API json data
    full = requests.get(a).json()

    # today's date taking as int
    day = datetime.datetime.today()
    today_date = int(day.strftime('%d'))


    forcast_data_list = {} # dictionary to store json data

    #looping to get value and put it in the dictionary
    for c in range(0, full['cnt']):
        date_var1 = full['list'][c]['dt_txt']
        date_time_obj1 = datetime.datetime.strptime(date_var1, '%Y-%m-%d %H:%M:%S')
        # print the json data and analyze the data coming to understand the structure. I couldn't find the better way
        # to process date
        if int(date_time_obj1.strftime('%d')) == today_date or int(date_time_obj1.strftime('%d')) == today_date+1:
            # print(date_time_obj1.strftime('%d %a'))
            if int(date_time_obj1.strftime('%d')) == today_date+1:
                today_date += 1
            forcast_data_list[today_date] = {}
            forcast_data_list[today_date]['day'] = date_time_obj1.strftime('%A')
            forcast_data_list[today_date]['date'] = date_time_obj1.strftime('%d %b, %Y')
            forcast_data_list[today_date]['time'] = date_time_obj1.strftime('%I:%M %p')
            forcast_data_list[today_date]['humidity'] = full['list'][c]['main']['humidity']

            forcast_data_list[today_date]['temperature'] = full['list'][c]['main']['temp']
            forcast_data_list[today_date]['temperature_max'] = full['list'][c]['main']['temp_max']
            forcast_data_list[today_date]['temperature_min'] = full['list'][c]['main']['temp_min']

            forcast_data_list[today_date]['description'] = full['list'][c]['weather'][0]['description']
            forcast_data_list[today_date]['icon'] = full['list'][c]['weather'][0]['icon']

            today_date += 1
        else:
            pass
    #returning the context with all the data to the index.html    
    
    context = {
        'weather':weather, 'forcast_data_list':forcast_data_list
    }

    return render(request, 'weatherAPI/realTimeWeather.html', context)

