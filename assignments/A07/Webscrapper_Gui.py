""" 
Description:
    This is an example gui that allows you to enter the appropriate parameters to get the weather from wunderground.
TODO:
    - You will need to change the text input boxes to drop down boxes and add the appropriate values to the drop down boxes.
    - For example the month drop down box should have the values 1-12.
    - The day drop down box should have the values 1-31.
    - The year drop down box should have the values ??-2023.
    - The filter drop down box should have the values 'daily', 'weekly', 'monthly'.
"""
import PySimpleGUI as sg 
import pandas as pd
import random     
import json

def currentDate(returnType='tuple'):
    """ Get the current date and return it as a tuple, list, or dictionary.
    Args:
        returnType (str): The type of object to return.  Valid values are 'tuple', 'list', or 'dict'.
    """
    from datetime import datetime
    if returnType == 'tuple':
        return (datetime.now().month, datetime.now().day, datetime.now().year)
    elif returnType == 'list':
        return [datetime.now().month, datetime.now().day, datetime.now().year]

    return {
        'day':datetime.now().day,
        'month':datetime.now().month,
        'year':datetime.now().year
    }

def buildWeatherURL(month=None, day=None, year=None, airport=None, filter=None):
    """ A gui to pass parameters to get the weather from the web.
    Args:
        month (int): The month to get the weather for.
        day (int): The day to get the weather for.
        year (int): The year to get the weather for.
    Returns:
        Should return a URL like this, but replace the month, day, and year, filter, and airport with the values passed in.
        https://www.wunderground.com/history/daily/KCHO/date/2020-12-31
    """
    current_month,current_day,current_year = currentDate('tuple')
    
    if not month:
        month = current_month
    if not day:
        day = current_day
    if not year:
        year = current_year

    # months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
    #           'October', 'November', 'December']
    months = ['1', '2', '3', '4', '5', '6', '7', '8', '9',
              '10', '11', '12']
    choices = ['Daily', 'Weekly','Monthly']
    
    # Create the gui's layout using text boxes that allow for user input without checking for valid input
    # Need to have months return as an index int value
    layout = [
        [sg.Text('Month')],[sg.Combo(months, readonly = True)],
        [sg.Text('Day')],[sg.InputText(day)],
        [sg.Text('Year')],[sg.InputText(year)],
        [sg.Text('Code')],[sg.InputText()],
        [sg.Text('Daily / Weekly / Monthly')],[sg.Combo(choices, readonly = True)],
        [sg.Submit(), sg.Cancel()]
    ]      

    window = sg.Window('Get The Weather', layout)    

    event, values = window.read()
    window.close()
        
        
    month = int(values[0])
    day = values[1]
    year = values[2]
    code = values[3]
    filter = values[4]

    sg.popup('You entered', f"Month: {month}, Day: {day}, Year: {year}, Code: {code}, Filter: {filter}")

    # return the URL to pass to wunderground to get appropriate weather data
    builtUrl = 'http://www.wunderground.com/history/daily/{}/date/{}-{}-{}'.format(code, year, month, day)
    print(builtUrl)
    return builtUrl

def tableGUI(month=None, day=None, year=None, airport=None, filter=None):
    max_rows = 10
    max_cols = 5

    with open('parsed.json', 'r') as infile:
        data = json.load(infile)

    table_data = []
    for item in data:
        row = [item.get('Time'), item.get('Temperature'), item.get('Humidity'), item.get('Wind'), item.get('WindSpeed'), item.get('Condition')]
        table_data.append(row)
    table_headings = ['Time', 'Temperature','Humidity', 'Wind', 'Wind Speed', 'Condition']

    layout = [
        [sg.Text('Airport: ')],
        [sg.Text('Date: ')],
        [sg.Table(values=table_data, headings = table_headings,
                  justification = 'center',
                  auto_size_columns= True,
                  display_row_numbers = True,
                  col_widths =[10, 10, 15], alternating_row_color='lightgreen')],
                  [sg.Button('Exit')]
    ]
    #create window
    window = sg.Window('Weather', layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break
    
    window.close()


if __name__=='__main__':
    buildWeatherURL()
    #tableGUI()