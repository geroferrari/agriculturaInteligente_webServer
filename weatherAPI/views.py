import requests
from django.shortcuts import render
from configuration.models import ConfigurationFieldModel
import datetime

def weatherAPI(request):

    if ConfigurationFieldModel.objects.exists() == 1:
        configurationFieldValues = ConfigurationFieldModel.objects.get(id=1)

        forecast_weather_url = 'http://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&appid=65af3b064c12ac4914679061cdd62db8&lang=es'

        a = forecast_weather_url.format(configurationFieldValues.ciudad)
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
        
        context = { 'forcast_data_list':forcast_data_list , "city" : configurationFieldValues.ciudad}

    else:
        context = { 'forcast_data_list':'' , "city" : ''}

    return render(request, 'weatherAPI/weatherAPI.html', context)

def temperatureAPIData():

    configurationFieldValues = ConfigurationFieldModel.objects.get(id=1)
    
    # today's date taking as int
    day = datetime.datetime.today()
    today_date = int(day.strftime('%d'))

    #traigo la data del clima actual 
    current_weather_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=65af3b064c12ac4914679061cdd62db8&lang=es'

    weather_data = requests.get(current_weather_url.format(configurationFieldValues.ciudad)).json()

    current_temperature_data = {
        'date' :  datetime.date.strftime(day, '%Y-%m-%d'),
        'temperature' : weather_data['main']['temp'],
        'temperature_min': weather_data['main']['temp_min'],
        'temperature_max': weather_data['main']['temp_max'],
        'sunrise': weather_data['sys']['sunrise'],
        'sunset': weather_data['sys']['sunset'],
    }

    return (current_temperature_data)

def rainAPIData(max_days):

    configurationFieldValues = ConfigurationFieldModel.objects.get(id=1)
    
    # today's date taking as int
    day = datetime.datetime.today()
    today_date = int(day.strftime('%d'))

    #traigo la data del clima actual 
    current_weather_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=65af3b064c12ac4914679061cdd62db8&lang=es'

    weather_data = requests.get(current_weather_url.format(configurationFieldValues.ciudad)).json()

    if weather_data['weather'][0]['main'] == "rain" or weather_data['weather'][0]['main'] == "snow":
        return True
    
    #traigo datos extendidos una semana
    forecast_weather_url = 'http://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&appid=65af3b064c12ac4914679061cdd62db8&lang=es'

    a = forecast_weather_url.format(configurationFieldValues.ciudad)

    #accessing the API json data
    full = requests.get(a).json()

    #looping to get value and put it in the dictionary

    for c in range(0, max_days*8):
        date_var1 = full['list'][c]['dt_txt']
        date_time_obj1 = datetime.datetime.strptime(date_var1, '%Y-%m-%d %H:%M:%S')
        # print the json data and analyze the data coming to understand the structure. I couldn't find the better way
        # to process date
        if int(date_time_obj1.strftime('%d')) == today_date or int(date_time_obj1.strftime('%d')) == today_date+1:
            # print(date_time_obj1.strftime('%d %a'))
             # dictionary to store json data            
            if int(date_time_obj1.strftime('%d')) == today_date+1:
                today_date +=1
            if full['list'][c]['weather'][0]['main'] == "Rain" or full['list'][c]['weather'][0]['main'] == "Snow"  or weather_data['weather'][0]['main'] == "Clouds":
                return True
            today_date +=1
        else:
            pass

    return False


