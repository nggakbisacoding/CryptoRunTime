import PySimpleGUI as sg
import json
import datetime
import crypto
import webbrowser
import dashboard
from json import (load as jsonload, dump as jsondump)
import os
from currency_converter import CurrencyConverter

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), r'settings_file.cfg')
DEFAULT_SETTINGS = {'theme': sg.theme()}
SETTINGS_KEYS_TO_ELEMENT_KEYS = {'theme': '-THEME-'}
PATH_DATA = os.path.join(os.path.dirname(__file__), r'data.json')
PATH_ANALYSIS = os.path.join(os.path.dirname(__file__), r'analysis.py')
PATH_DASHBOARD = os.path.join(os.path.dirname(__file__), r'dashboard.py')
#change above if you change script file
crypto.main()

def tim():
    tim = datetime.datetime.now()
    return (tim.strftime("%H:%M:%S %d-%m-%Y"))
    
def load_json(path_data):
    try:
        with open(path_data, 'r') as f:
            data = json.load(f)
    except Exception as e:
        sg.popup_quick_message(f'exception {e}', 'File database tidak ditemukan', keep_on_top=True, background_color='red', text_color='white')
        data = {}
    return data
    

def load_settings(settings_file, default_settings):
    try:
        with open(settings_file, 'r') as f:
            settings = jsonload(f)
    except Exception as e:
        sg.popup_quick_message(f'exception {e}', 'File setting tidak ditemukan... file baru akan dibuat', keep_on_top=True, background_color='red', text_color='white')
        settings = default_settings
        save_settings(settings_file, settings, None)
    return settings

def load_coins(path_data, coins):
    try:
        with open(path_data, 'r') as f:
            data = json.load(f)
            data = data['data'][coins.upper()]
    except Exception as e:
        sg.popup_quick_message(f'exception {e}', 'File database tidak ditemukan', keep_on_top=True, background_color='red', text_color='white')
        data = {"data": "None"}
    return data
    
def onclick_event(coins):
    data = load_coins('data.json', coins.upper())
    
    

def save_settings(settings_file, settings, values):
    if values:      
        for key in SETTINGS_KEYS_TO_ELEMENT_KEYS:
            try:
                settings[key] = values[SETTINGS_KEYS_TO_ELEMENT_KEYS[key]]
            except Exception as e:
                print(f'Problem updating settings from window values. Key = {key}')

    with open(settings_file, 'w') as f:
        jsondump(settings, f)

    sg.popup('Settings saved')
    
def run(runfile):
    with open(runfile,"r") as rnf:
        exec(rnf.read())

def create_settings_window(settings):
    sg.theme(settings['theme'])

    def TextLabel(text): return sg.Text(text+':', justification='r', size=(15,1))

    layout = [  [sg.Text('Settings', font='Any 15')],
                [TextLabel('Theme'),sg.Combo(sg.theme_list(), size=(20, 20), key='-THEME-')],
                [sg.Button('Save'), sg.Button('Exit')]  ]

    window = sg.Window('Settings', layout, keep_on_top=True, finalize=True)

    for key in SETTINGS_KEYS_TO_ELEMENT_KEYS:
        try:
            window[SETTINGS_KEYS_TO_ELEMENT_KEYS[key]].update(value=settings[key])
        except Exception as e:
            print(f'Terdapat masalah ketika melakukan update tema. Key = {key}')

    return window

def create_main_window(settings):
    sg.theme(settings['theme'])

    menu_def = [['&Menu',['Settings', 'E&xit']],
                ['&Crypto',['Dashboard', 'Analysis']],
                ['&Help','&About']]

    right_click_menu = ['Unused', ['Settings', 'E&xit']]
    
    layout =   [[sg.Menu(menu_def)],
                [sg.Text('', size=(28,1), font=('Helvetica', 11), key='_DATE_'),
                 sg.Text('1 USD =', font=('Helvetica', 11)), sg.Text('', size=(9,1), font=('Helvetica', 11), key='idrusd'),sg.Push(),
                 sg.InputText(key='-IN-', size=(7, 2), font=('Helvetica', 9),),
                 sg.Button('OK', key='submit', size=(4,1), font=('Helvetica', 9), button_color="Blue")],
                
                [sg.Text('')],
                [sg.Text('#', font=('Helvetica', 11, 'bold'), size=(2,1)), sg.Text('Name', font=('Helvetica', 11, 'bold'), size=(23,1)),
                 sg.Text('Price IDR', size=(9,1), font=('Helvetica', 11, 'bold')), sg.Text('Price USD', size=(9,1), font=('Helvetica', 11, 'bold')),
                 sg.Text('Price GBP', visible=False,  key='prices', size=(9,1), font=('Helvetica', 11, 'bold'))],
                
                [sg.Text('1', font=('Helvetica', 11, 'bold'), size=(2,1)), sg.Image('png/bit.png', size=(30, 30)),
                 sg.Text('Bitcoin (BTC)', font=('Helvetica', 11), size=(18,1)), sg.Text('', size=(9,1), font=('Helvetica', 11),  key='btcidr'),
                 sg.Text('', size=(9,1), font=('Helvetica', 11),  key='btcusd'), sg.Text('', size=(9,1), font=('Helvetica', 11),  key='btcgb', visible=False)],
                
                [sg.Text('2', font=('Helvetica', 11, 'bold'), size=(2,1)), sg.Image('png/eth.png', size=(30, 30)),
                 sg.Text('Ethereum (ETH)', font=('Helvetica', 11), size=(18,1)), sg.Text('', size=(9,1), font=('Helvetica', 11),  key='ethidr'),
                 sg.Text('', size=(9,1), font=('Helvetica', 11),  key='ethusd'), sg.Text('', size=(9,1), font=('Helvetica', 11),  key='ethgb', visible=False)],
                
                [sg.Text('3', font=('Helvetica', 11, 'bold'), size=(2,1)), sg.Image('png/xrp.png', size=(30, 30)),
                 sg.Text('Ripple (XRP)', font=('Helvetica', 11), size=(18,1)), sg.Text('', size=(9,1), font=('Helvetica', 11),  key='xrpidr'),
                 sg.Text('', size=(9,1), font=('Helvetica', 11),  key='xrpusd'), sg.Text('', size=(9,1), font=('Helvetica', 11),  key='xrpgb', visible=False)],
                
                [sg.Text('4', font=('Helvetica', 11, 'bold'), size=(2,1)), sg.Image('png/lite.png', size=(30, 30)),
                 sg.Text('Litecoin (LTC)', font=('Helvetica', 11), size=(18,1)), sg.Text('', size=(9,1), font=('Helvetica', 11),  key='ltcidr'),
                 sg.Text('', size=(9,1), font=('Helvetica', 11),  key='ltcusd'), sg.Text('', size=(9,1), font=('Helvetica', 11),  key='ltcgb', visible=False)],
                
                [sg.Text('5', font=('Helvetica', 11, 'bold'), size=(2,1)), sg.Image('png/bch.png', size=(30, 30)),
                 sg.Text('Bitcoin Cash (BCH)', font=('Helvetica', 11), size=(18,1)), sg.Text('', size=(9,1), font=('Helvetica', 11),  key='bchidr'),
                 sg.Text('', size=(9,1), font=('Helvetica', 11),  key='bchusd'), sg.Text('', size=(9,1), font=('Helvetica', 11),  key='bchgb', visible=False)],
                
                [sg.Text('6', font=('Helvetica', 11, 'bold'), size=(2,1)), sg.Image('png/pax.png', size=(30, 30)),
                 sg.Text('Paxos Standard (USDP)', font=('Helvetica', 11), size=(18,1)), sg.Text('', size=(9,1), font=('Helvetica', 11),  key='paxidr'),
                 sg.Text('', size=(9,1), font=('Helvetica', 11),  key='paxusd'), sg.Text('', size=(9,1), font=('Helvetica', 11),  key='paxgb', visible=False)],
                
                [sg.Text('7', font=('Helvetica', 11, 'bold'), size=(2,1)), sg.Image('png/stellar.png', size=(30, 30)),
                 sg.Text('Stellar (XLM)', font=('Helvetica', 11), size=(18,1)), sg.Text('', size=(9,1), font=('Helvetica', 11),  key='xlmidr'),
                 sg.Text('', size=(9,1), font=('Helvetica', 11),  key='xlmusd'), sg.Text('', size=(9,1), font=('Helvetica', 11),  key='xlmgb', visible=False)],

                [sg.Text('8', font=('Helvetica', 11, 'bold'), size=(2,1)), sg.Image('png/link.png', size=(30, 30)),
                 sg.Text('Chainlink (LINK)', font=('Helvetica', 11), size=(18,1)), sg.Text('', size=(9,1), font=('Helvetica', 11),  key='linkidr'),
                 sg.Text('', size=(9,1), font=('Helvetica', 11),  key='linkusd'), sg.Text('', size=(9,1), font=('Helvetica', 11),  key='linkgb', visible=False)],

                [sg.Text('9', font=('Helvetica', 11, 'bold'), size=(2,1)), sg.Image('png/omg.png', size=(30, 30)),
                 sg.Text('OMG Network(OMG)', font=('Helvetica', 11), size=(18,1)), sg.Text('', size=(9,1), font=('Helvetica', 11),  key='omgidr'),
                 sg.Text('', size=(9,1), font=('Helvetica', 11),  key='omgusd'), sg.Text('', size=(9,1), font=('Helvetica', 11),  key='omggb', visible=False)],

                [sg.Text('10', font=('Helvetica', 11, 'bold'), size=(2,1)), sg.Image('png/knc.png', size=(30, 30)),
                 sg.Text('Kyber Network(KNC)', font=('Helvetica', 11), size=(18,1)), sg.Text('', size=(9,1), font=('Helvetica', 11),  key='kncidr'),
                 sg.Text('', size=(9,1), font=('Helvetica', 11),  key='kncusd'), sg.Text('coming soon', size=(9,1), font=('Helvetica', 11),  key='kncgb', visible=False)],

                [sg.Text('11', font=('Helvetica', 11, 'bold'), size=(2,1)), sg.Image('png/mkr.png', size=(30, 30)),
                 sg.Text('Maker(MKR)', font=('Helvetica', 11), size=(18,1)), sg.Text('', size=(9,1), font=('Helvetica', 11),  key='mkridr'),
                 sg.Text('', size=(9,1), font=('Helvetica', 11),  key='mkrusd'), sg.Text('coming soon', size=(9,1), font=('Helvetica', 11),  key='mkrgb', visible=False)],

                [sg.Text('12', font=('Helvetica', 11, 'bold'), size=(2,1)), sg.Image('png/zrx.png', size=(30, 30)),
                 sg.Text('0x (ZRX)', font=('Helvetica', 11), size=(18,1)), sg.Text('', size=(9,1), font=('Helvetica', 11),  key='zrxidr'),
                 sg.Text('', size=(9,1), font=('Helvetica', 11),  key='zrxusd'), sg.Text('coming soon', size=(9,1), font=('Helvetica', 11),  key='zrxgb', visible=False)],
                
                [sg.Text('Last Sync: ', size=(8,1), font=('Helvetica', 11)), sg.Text('None', size=(15,1), font=('Helvetica', 11),  key='sync')]]

    return sg.Window('Crypto Currencies', layout=layout,
                     right_click_menu=right_click_menu)

def queue(window, coin, data_crypto, keys):
    cc = CurrencyConverter()
    for i in coin:
        try:
            convert = cc.convert(1, i, "IDR")
        except Exception as e:
            convert = cc.convert(1, "EUR", "IDR")
        window['prices'].update("Price "+i.upper(), visible=True)
        for key, value in keys.items():
            window.Element(key).Update(''+str(int(data_crypto[value]['quote']['IDR']['price'])/convert), visible=True)

def main():
    window, settings = None, load_settings(SETTINGS_FILE, DEFAULT_SETTINGS )
    while True:
        if window is None:
            window = create_main_window(settings)
        data = load_json(PATH_DATA)
        data_crypto = data['data']
        times = tim()
        splitx = data['status']['timestamp'].split(':')
        clock = splitx[0].split('T')
        sec = splitx[2].split('.')
        sync = clock[0]+" "+str(int(clock[1])+7)+":"+str(splitx[1])
        cc = CurrencyConverter()
        idrusd = cc.convert(1, 'USD', 'IDR')
        keys = {"btcgb":"BTC", "ethgb":"ETH", "xrpgb" : "XRP", "ltcgb" : "LTC", "bchgb" : "BCH", "paxgb":"USDP", "xlmgb":"XLM","linkgb":"LINK", "omggb":"OMG", "kncgb":"KNC", "mkrgb":"MKR", "zrxgb":"ZRX"}
        
        event, values = window.Read(timeout=10)
        window.Element('_DATE_').Update(str(times))
        window.Element('idrusd').Update('Rp. '+str(idrusd))
        window.Element('sync').Update(str(sync))
        window.Element('btcidr').Update('Rp. '+str(data_crypto['BTC']['quote']['IDR']['price']))
        window.Element('btcusd').Update('$ '+str(int(data_crypto['BTC']['quote']['IDR']['price'])/idrusd))
        window.Element('ethidr').Update('Rp. '+str(data_crypto['ETH']['quote']['IDR']['price']))
        window.Element('ethusd').Update('$ '+str(int(data_crypto['ETH']['quote']['IDR']['price'])/idrusd))
        window.Element('xrpidr').Update('Rp. '+str(data_crypto['XRP']['quote']['IDR']['price']))
        window.Element('xrpusd').Update('$ '+str(int(data_crypto['XRP']['quote']['IDR']['price'])/idrusd))
        window.Element('ltcidr').Update('Rp. '+str(data_crypto['LTC']['quote']['IDR']['price']))
        window.Element('ltcusd').Update('$ '+str(int(data_crypto['LTC']['quote']['IDR']['price'])/idrusd))
        window.Element('bchidr').Update('Rp. '+str(data_crypto['BCH']['quote']['IDR']['price']))
        window.Element('bchusd').Update('$ '+str(int(data_crypto['BCH']['quote']['IDR']['price'])/idrusd))
        window.Element('paxidr').Update('Rp. '+str(data_crypto['USDP']['quote']['IDR']['price']))
        window.Element('paxusd').Update('$ '+str(int(data_crypto['USDP']['quote']['IDR']['price'])/idrusd))
        window.Element('xlmusd').Update('$ '+str(int(data_crypto['XLM']['quote']['IDR']['price'])/idrusd))
        window.Element('xlmidr').Update('Rp. '+str(data_crypto['XLM']['quote']['IDR']['price']))
        window.Element('linkidr').Update('Rp. '+str(data_crypto['LINK']['quote']['IDR']['price']))
        window.Element('linkusd').Update('$. '+str(int(data_crypto['LINK']['quote']['IDR']['price'])/idrusd))
        window.Element('omgidr').Update('Rp. '+str(data_crypto['OMG']['quote']['IDR']['price']))
        window.Element('omgusd').Update('$. '+str(int(data_crypto['OMG']['quote']['IDR']['price'])/idrusd))
        window.Element('kncidr').Update('Rp. '+str(data_crypto['KNC']['quote']['IDR']['price']))
        window.Element('kncusd').Update('$. '+str(int(data_crypto['KNC']['quote']['IDR']['price'])/idrusd))
        window.Element('mkridr').Update('Rp. '+str(data_crypto['MKR']['quote']['IDR']['price']))
        window.Element('mkrusd').Update('$. '+str(int(data_crypto['MKR']['quote']['IDR']['price'])/idrusd))
        window.Element('zrxidr').Update('Rp. '+str(data_crypto['ZRX']['quote']['IDR']['price']))
        window.Element('zrxusd').Update('$. '+str(int(data_crypto['ZRX']['quote']['IDR']['price'])/idrusd))

        if event in (None, 'Exit'):
            break
        elif event == 'About':
            window.disappear()
            sg.popup('Created by TRPL_A2.', 'Crypto Market', 'Version 1.0')
            window.reappear()

        elif event == 'Settings':
            event, values = create_settings_window(settings).read(close=True)
            if event == 'Save':
                window.close()
                window = None
                save_settings(SETTINGS_FILE, settings, values)

        elif event == 'Dashboard':
            dashboard.main()
            os.system(r'streamlit run '+PATH_DASHBOARD)
            webbrowser.open_new_tab("http://localhost:8501/")
            
        elif event == 'Analysis':
            os.system(r'python.exe '+PATH_ANALYSIS)
            os.system(r'streamlit run '+PATH_ANALYSIS)
            webbrowser.open_new_tab("http://localhost:8501/")
        
        elif event == 'submit':
            coin = values['-IN-']
            if("," in coin):
                coin = coin.split(",")
                queue(window, coin, data_crypto, keys)
            else:
                try:
                    convert = cc.convert(1, coin, "IDR")
                except Exception as e:
                    convert = cc.convert(1, "EUR", "IDR")
                window['prices'].update("Price "+coin.upper(), visible=True)
                for key, value in keys.items():
                    window.Element(key).Update(''+str(int(data_crypto[value]['quote']['IDR']['price'])/convert), visible=True)
    window.Close()   

main()