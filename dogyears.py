# -*- coding: utf-8 -*-
"""
Updated on Fri Jun 26, 2020

@author: oktl

Dogs don't age at the same rate as humans. Historically the ratio has
been 7:1 - 7 dog years to 1 human year. The American Kennel Club(AKC)
has studied dog aging and come up with new information. They found that
dogs age much more rapidly in the first two years and then slow down
some.  They also discovered that the general size and weight of the dog
has a factor in aging.

This script takes a dog's birth date, gets the number of human years plus
months the dog has been alive today and converts that to dog years.
The script started out of curiosity as I was teaching myself Python.
My daughter mentioned that her puppy had it's one year birthday and I
told her that he was no longer a child but a teenager.

"""

import PySimpleGUI as sg
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
import math

# print(sg)
# print(sg.version)

# ----------------------- Set up the data ---------------------------- #
SMALL = {0: 0, 1: 15, 2: 24, 3: 28, 4: 32, 5: 36, 6: 40, 7: 44, 8: 48,
         9: 52, 10: 56, 11: 60, 12: 64, 13: 68, 14: 72, 15: 76, 16: 80}
MEDIUM = {0: 0, 1: 15, 2: 24, 3: 28, 4: 32, 5: 36, 6: 42, 7: 47, 8: 51,
          9: 56, 10: 60, 11: 65, 12: 69, 13: 74, 14: 78, 15: 83, 16: 87}
LARGE = {0: 0, 1: 15, 2: 24, 3: 28, 4: 32, 5: 36, 6: 45, 7: 50, 8: 55,
         9: 61, 10: 66, 11: 72, 12: 77, 13: 82, 14: 88, 15: 93, 16: 99}
GIANT = {0: 0, 1: 12, 2: 22, 3: 31, 4: 38, 5: 45, 6: 49, 7: 56, 8: 64,
         9: 71, 10: 79, 11: 86, 12: 93, 13: 100, 14: 107, 15: 114, 16: 121}
# AKC classifies dogs by general size determined by weight.
# Small <= 20 lbs, Medium > 20 to <= 50 lbs, Large > 50 to <=100 lbs,
# Giant > 100 lbs.
SIZES = {'-SMALL-': SMALL, '-MEDIUM-': MEDIUM, '-LARGE-': LARGE, '-GIANT-': GIANT}

# Averages of how many years a dog grows in one month depending on size.
year_one_age_factor = {'-SMALL-': 1.25, '-MEDIUM-': 1.25, '-LARGE-': 1.25, '-GIANT-': 1.0}
year_two_age_factor = {'-SMALL-': 0.75, '-MEDIUM-': 0.75, '-LARGE-': 0.75, '-GIANT-': 0.83}
average_age_factor = {'-SMALL-': 0.33, '-MEDIUM-': 0.38, '-LARGE-': 0.45, '-GIANT-': 0.59}

keys_to_clear = ['-BIRTHDATE-', '-HUMAN_YEARS-', '-DOG_YEARS-']

about_text = ('Dogs do not age at the same  as humans.\n'
              'Historically, the ratio has been 7 to 1,\n'
              '7 dog years to 1 human year.\n'
              'The American Kennel Club (AKC) has studied dog\n'
              'aging and come up with new information.\n\n'
              'They found that dogs age much more rapidly in\n'
              'the first two years and then slow down.\n'
              'They also discovered that the general size and\n'
              'weight of the dog has a factor in aging.\n\n'
              'The sizes are:\n'
              'Small - 20 pounds or less,\n'
              'Medium - 21 to 50 pounds\n'
              'Large - 51 to 100 pounds\n'
              'Giant - over 100 pounds.\n\n'
              'This app takes a date and calculates the number\n'
              "of years and months a dog is using the AKC's data.\n\n")

help_text = ('Help, I need somebody\n'
             'Help, not just anybody\n'
             'Help, you know I need someone, help\n\n'

             'When I was younger, so much younger than today\n'
             "I never needed anybody's help in any way\n"
             "But now these days are gone, I'm not so self assured\n"
             "Now I find I've changed my mind and opened up the doors\n\n"

             "Help me if you can, I'm feeling down\n"
             "And I do appreciate you being round\n"
             "Help me get my feet back on the ground\n"
             "Won't you please, please help me\n\n"

             "And now my life has changed in oh so many ways\n"
             "My independence seems to vanish in the haze\n"
             "But every now and then I feel so insecure\n"
             "I know that I just need you like I've never done before\n\n"

             "Help me if you can, I'm feeling down\n"
             "And I do appreciate you being round\n"
             "Help me get my feet back on the ground\n"
             "Won't you please, please help me\n\n"

             "When I was younger, so much younger than today\n"
             "I never needed anybody's help in any way\n"
             "But now these days are gone, I'm not so self assured\n"
             "Now I find I've changed my mind and opened up the doors\n\n"

             "Help me if you can, I'm feeling down\n"
             "And I do appreciate you being round\n"
             "Help me get my feet back on the ground\n"
             "Won't you please, please help me, help me, help me, ohohoh\n\n"

             "Written by John Lennon and Paul McCartney")


def check_inputs():
    '''
    Loop through inputs to see if any are empty.

    Returns
    -------
    empty_input : list
        List of empty inputs if any.

    '''
    no_values = {key: value for (key, value) in values.items() if value == ''}
    # Get a list for the error popup.
    empty_inputs = [*no_values]
    return empty_inputs


def convert_to_months(age):
    '''
    Separate the decimal from the integer of a float.
    Convert decimal part to months, then both to integer.

    Parameters
    ----------
    age : float
        **

    Returns
    -------
    years and months : tuple
        **
    '''
    months, years = math.modf(age)
    months = months * 12  # Convert decimal.
    return int(years), int(months)


# ---------------------- Do the magic --- ------------------ #
def calculate_dog_years(dog_size, human_years, human_months):
    '''
    Calculate a dogs age in dog years. Looks to see what size the dog
    is. Gets the age factor from the age in years, uses that with
    size and number of months to get the age.

    Parameters
    ----------
    dog_size : string
        General size of dog from SIZES dictionary.
   human_years : int
        Number of human years from dog's birthdate unitl today.
    human_months : int
        Number of additional months from last birthday.
    Returns
    -------
    dog_age : tuple
       Years and months calculated using AKC age factors.

    '''
    if dog_size in SIZES:
        # Get a list from the dog_size input to use the right one.
        size = SIZES[dog_size]
        if human_years < 1:
            age_factor = year_one_age_factor[dog_size]
            dog_age = human_months * age_factor
        elif human_years < 2:
            age_factor = year_two_age_factor[dog_size]
            dog_age = size.get(human_years) + (age_factor * human_months)
        else:
            age_factor = average_age_factor[dog_size]
            dog_age = size.get(human_years) + (age_factor * human_months)
        # Get years and months.
        dog_age = convert_to_months(dog_age)
        # print(dog_age)
        return dog_age


# Need some text.
def info_window(title, text):
    ''' Open a new window, show some information.'''

    layout = [
        [sg.Text(title, font='Calibri 12 bold')],
        [sg.Text(text, auto_size_text=True, font='Calibri 11')],
        [sg.Button('OK', bind_return_key=True)]]

    window = sg.Window(title, layout, no_titlebar=False,
                       text_justification='c', element_justification='c')
    event, values = window.read()
    window.close()


# User defined element. Shortcut for the output frames.
def output_frame(title, key):
    return [sg.Frame(layout=[[sg.Text('', size=(16, 1), justification='center', key=key)]],
                     title=title, title_location=sg.TITLE_LOCATION_TOP,
                     font='Calibri 12', pad=((0, 0), (5, 15)))]


# Opens the test harness and a debug window.
# sg.main()

# Make it whatever you want.
# sg.theme('DarkTeal10')
sg.theme('BrownBlue')
sg.set_options(tooltip_font=('Calibri 12'))

# Opens a debug window, delete this before making an .exe file
# sg.Print('This is the first line printed', do_not_reroute_stdout=False)

menu_def = [['&File', ['E&xit', '&Properties']],
            ['&Help', ['&Help', '&About...']], ]

layout = [
    [sg.Menu(menu_def)],
    [sg.Txt("Get A Dog's Age")],
    [sg.HorizontalSeparator(color='bostonblue', pad=((0, 0), (5, 15)))],
    [sg.Frame(layout=[
        [sg.R('Small', 'RADIOS', key='-SMALL-', tooltip='20 pounds or less'),
         sg.R('Medium', 'RADIOS', key='-MEDIUM-', default=True, tooltip='21- 50 pounds'),
         sg.R('Large', 'RADIOS', key='-LARGE-', tooltip='51 - 100 pounds'),
         sg.R('Giant', 'RADIOS', key='-GIANT-', tooltip='More than 100 pounds')]],
        title="Pick your dog'size", title_location=sg.TITLE_LOCATION_TOP,
        relief=sg.RELIEF_SUNKEN, key='-SIZE-', font='Calibri 12')],
    [sg.Txt('Pick Date')],
    [sg.CalendarButton('Date', target=('-BIRTHDATE-'), size=(11, 1),
                       font='Calibri 11', focus=False)],
    [sg.In(size=(9, 1), background_color='LightSkyBlue4', key='-BIRTHDATE-')],
    output_frame('Human Age', '-HUMAN_YEARS-'),
    output_frame('Dog Age', '-DOG_YEARS-'),
    [sg.B('Show', bind_return_key=True), sg.B('Clear'), sg.B('Exit')]]

window = sg.Window('Dog Years', layout, auto_size_buttons=False,
                   default_button_element_size=(10, 1), font='Calibri 14',
                   element_justification="center", return_keyboard_events=True)
window.SetIcon("dog2.ico")
about_window_active = False

while True:  # Event Loop
    event, values = window.read()

    if event in (sg.WIN_CLOSED, 'Exit', 'End:35'):
        break

    try:  # Catch blank inputs.
        if event == 'Show':
            print(f' This should be the Show event: {event}')
            empty_input = check_inputs()
            if empty_input:
                sg.popup_error(f'ValueError\nThere are empty entries:\n{empty_input}',
                               font=('Calibri', 14), no_titlebar=True,
                               text_color='orange')
            else:
                # Get the key that matches the value 'True' from the radio buttons.
                true_value = {key: value for (key, value) in values.items() if value is True}
                size = [*true_value]  # unpack the new dict to a list- PEP 448
                str_size = ''.join(size)  # Get a string from the list.
                bdate = values.get('-BIRTHDATE-')
                birthdate = datetime.strptime(bdate, '%Y-%m-%d %H:%M:%S').date()
                today = date.today()

                human_age = relativedelta(today, birthdate)
                human_years = human_age.years
                human_months = human_age.months
                dogs_age = calculate_dog_years(str_size, human_years, human_months)

                # Update the output
                window['-HUMAN_YEARS-'].update(f'{human_years} years, {human_months} months')
                window['-DOG_YEARS-'].update(f'{dogs_age[0]} years, {dogs_age[1]} months')

    except ValueError:  # this does nothing
        sg.Popup('ValueError\nCheck empty entries.')

    if event == 'About...' or event == 'F2:113':
        window.disappear()
        info_window('About', about_text)
        window.reappear()

    if event == 'Help' or event == 'F1:112':
        window.disappear()
        info_window('Help', help_text)
        window.reappear()

    if event == 'Clear' or event == 'Delete:46':
        print('Calling Clear')
        values.clear()
        for key in keys_to_clear:
            window[key].update('')

# Shut it all down.
window.close()
