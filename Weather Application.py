import os
import tkinter as  tk
from tkinter import ttk
from tkinter import Tk
from tkinter import StringVar
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter import Text
from tkinter import INSERT
from datetime import datetime
from dotenv import load_dotenv
import requests

class WeatherApp:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("400x500")
        self.root.resizable(0, 0)
        self.root.title("Weather App")
        load_dotenv()
        #Functions to fetch and display weather info
        self.city_value = StringVar()

        city_head = Label(self.root, text='Enter City Name',
                          font='Arial 12 bold')
        city_head.pack(pady=10)

        inp_city = Entry(self.root, textvariable=self.city_value,
                         width=24,
                         font='Arial 14 bold')
        inp_city.pack()

        show_weather_btn = Button(self.root,
                                  command=self.show_weather,
                                  text="Check Weather",
                                  font="Arial 10",
                                  bg='lightblue',
                                  fg='black',
                                  activebackground="teal",
                                  padx=5, pady=5)
        show_weather_btn.pack(pady=20)
        show_weather_btn1 = Button(self.root,
                                   command=lambda:self.my_reset(),
                                   text="Reset",
                                   font=22,
                                   bg='pink',
                                   fg='black',
                                   padx=5, pady=5)
        show_weather_btn1.pack(pady=20)
        #to show output
        weather_now = Label(self.root, text="The Weather is:", font='Arial 12 bold')
        weather_now.pack(pady=10)

        self.tfield = Text(self.root, width=46, height=10)
        self.tfield.pack()

    def get_weather_data(self, city_name):
        api_key = os.getenv("API_KEY")  # Get API key from environment variable
        base_url = 'http://api.openweathermap.org/data/2.5/weather?q='
        # Construct the complete weather URL
        weather_url = f"{base_url}{city_name}&appid={api_key}"
       #Get the response from fetched url
        response = requests.get(weather_url,timeout=10)
        return response.json()

    def display_weather(self, weather_info, city_name):
        #to clear the text field for every new output
        self.tfield.delete("1.0", "end")
        #as per API documentation if the cod is 200
        #it means that weather data was successfully fetched
        if weather_info['cod'] == 200:
            kelvin = 273
            #Storing the fetched values of weather of a city
            temp = int(weather_info['main']['temp'] - kelvin)
            feels_like_temp = int(weather_info['main']['feels_like'] - kelvin)
            pressure = weather_info['main']['pressure']
            humidity = weather_info['main']['humidity']
            sunrise = weather_info['sys']['sunrise']
            sunset = weather_info['sys']['sunset']
            timezone = weather_info['timezone']
            cloudy = weather_info['clouds']['all']
            description = weather_info['weather'][0]['description']
            sunrise_time = self.time_format_for_location(sunrise + timezone)
            sunset_time = self.time_format_for_location(sunset + timezone)

            #assigning Values to our weather varaible, to display as output
            weather = f"Weather of:{city_name}\nTemperature (Celsius):{temp}°\nFeels like in (Celsius): {feels_like_temp}°\nPressure: {pressure} hPa\nHumidity: {humidity}%\nSunrise at {sunrise_time} and Sunset at {sunset_time}\nCloud: {cloudy}%\nInfo: {description}"
        else:
            weather = f"\n\tWeather for '{city_name}' not found!\n\tKindly Enter a valid City Name !!"
        #to insert or send value in our Text Field to display output
        self.tfield.insert(INSERT, weather)

    def time_format_for_location(self, utc_with_tz):
        local_time = datetime.utcfromtimestamp(utc_with_tz)
        return local_time.time()
    def show_weather(self):
        # Get city name from user from the input field.
        city_name = self.city_value.get()
        # Get city name from user from the input field.
        weather_info = self.get_weather_data(city_name)
        self.display_weather(weather_info, city_name)
    def my_reset(self):#for clearing the values
        for widget in self.root.winfo_children():
            if isinstance(widget,tk.Entry):
                widget.delete(0,'end')
            if isinstance(widget,ttk.Combobox):
                widget.delete(0,'end')
            if isinstance(widget,tk.Text):
                widget.delete(1.0,'end')
            if isinstance(widget,tk.Checkbutton):
                widget.deselect()

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = WeatherApp()
    app.run()
