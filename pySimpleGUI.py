import PySimpleGUI as sg
import time

# Get Date
def get_current_date():
    current_date = time.strftime('%F')
    return current_date

# Get time
def get_current_time():
    current_time = time.strftime('%I:%M:%S')
    return current_time

def time_as_int():
    return int(round(time.time() * 100))

# Setting GUI Theme 
sg.theme('DarkGray9')

# Setting layout of main tab
main_layout = [
    # Title
    [sg.Text('Support Tool')],
    [sg.Text(size=(12, 1), key='date')],
    [sg.Text(size=(8, 1), key='time')],
    [sg.Text('', size=(10,1), font=('Bauhaus 93',80), justification='c', pad=((30,30),(20,0)), key='Display_timer')],
    
    # Button
    [sg.Button('Run', button_color=('white', 'Blue'), key='-RUN-PAUSE-'),
     sg.Button('Reset', button_color=('white', 'Green'), key='-RESET-'),
     sg.Exit(button_color=('white', 'Darkred'), key='-QUIT1-')]
]

# Setting layout of settings tab
Setting_layout = [
    [sg.Text('*OPTIONAL*\nInput the time title:',size=(15,2), justification='c', pad=((0,0),(10,10)))],
    [sg.Combo([i for i in range(0,60)] + [''], default_value='3',size=(5,7) , font=('Helvetica', 10), pad=((125,0),(0,0)), key='min'),
    sg.Text('min.', font=('Helvetica', 10)),
    sg.Combo([i for i in range(0,60)] + [''], default_value='0',size=(5,7), font=('Helvetica', 10), key='sec'),
    sg.Text('sec.', font=('Helvetica', 10))]
]

# Setting layout
layout = [[sg.TabGroup([[sg.Tab('Main', main_layout), sg.Tab('Settings', Setting_layout)]])]]

# Setting Window Title
window = sg.Window('Support Tool', layout,
    no_titlebar=True,
    auto_size_buttons=False,
    keep_on_top=True,
    grab_anywhere=True,
    element_padding=(0, 0)
)

# Setting Varilable
start_time, paused_time, paused = 0, 0, True
first_flag = True
add_word = ''
hold_time, hold_flag = 0, True


while True:
    # Read Events
    event , values = window.read(timeout=100,timeout_key='timeout')
    
    # Debug print
    #print('イベント:',event ,', 値:',values)

    # Exit
    if event in (sg.WIN_CLOSED, '-QUIT1-'):
        print('end')
        break
    if event in (sg.WIN_CLOSED, '-QUIT2-'):
        print('end')
        break
    
    # Reset
    if event == '-RESET-':  # RESET押下
        paused_time = start_time = time_as_int()
        current_time = values['min'] * 100 * 60 + values['sec'] * 100

    # Run /Pause
    if event == '-RUN-PAUSE-':    # 0秒 or Run/Pause押下
        if first_flag: # 起動時の諸々を処理
            paused_time = time_as_int()
            window['-RUN-PAUSE-'].update('Pause')
            paused = not paused
            first_flag = not first_flag
            start_time = time_as_int()
            continue

        paused = not paused

        if paused:
            paused_time = time_as_int()
        else:
            start_time += time_as_int() - paused_time
        window['-RUN-PAUSE-'].update('Run' if paused else 'Pause')

    # Time & date
    if event in 'timeout':
        window['time'].update(get_current_time())
        window['date'].update(get_current_date())

    if not paused:  # Run状態 10msで読み込み、与えた時間とその変化を記述・追加時間がある場合の制御
        event, values = window.read(timeout=10)
        current_time = values['min'] * 100 * 60 + values['sec'] * 100
        current_time += start_time - time_as_int()
        if current_time < 0: # 監視している時間変数が0を下回ると追加時間を加算
            if hold_flag:
                hold_time = current_time
                hold_flag = not hold_flag
            if current_time > 0: # 追加時間があれば時間説明の書き換え
                current_time = 0
            else: # 追加時間がなければ0とする
                event = '-RUN-PAUSE-'
                current_time = 0

    else:   # 待機（pause）状態 起動時の諸々を処理
        event, values = window.read(timeout=10)
        if first_flag:
            current_time = values['min'] * 100 * 60 + values['sec'] * 100
            window['Display_timer'].update('{:02d}:{:02d}'.format((current_time // 100) // 60, (current_time // 100) % 60))

    window['Display_timer'].update('{:02d}:{:02d}'.format((current_time // 100) // 60, (current_time // 100) % 60))



# Close Window
window.close()