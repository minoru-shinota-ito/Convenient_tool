import PySimpleGUI as sg
import time

def get_current_date():
    current_date = time.strftime('%F')
    return current_date

def get_current_time():
    current_time = time.strftime('%I:%M:%S')
    return current_time

# Setting Theme 
sg.theme('DarkGray9')

# Setting Layout list
layout = [
          [sg.Text('TODO Management Tool')],
          [sg.Text(size=(12, 1), key='date')],
          [sg.Text(size=(8, 1), key='time')],
          [sg.InputText(default_text='input text',size = (15,1), key= 'inputText1')],
          [sg.Button('Exit',size = (15,1),key = 'Exit')]
         ] 

# Setting Window Title
window = sg.Window('TODO Management Tool', layout)

while True:
    # Read Events
    event , values = window.read(timeout=100,timeout_key='timeout')
    
    # Debug print
    print('イベント:',event ,', 値:',values)

    # Exit
    if event in (None ,'Exit'):
        print('end')
        break
    
    # Timer
    elif event in 'timeout':
        current_time = get_current_time()
        current_date = get_current_date()
        window['time'].update(current_time)
        window['date'].update(current_date)

# Close Window
window.close()