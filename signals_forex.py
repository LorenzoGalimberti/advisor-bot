import yfinance as yf
import csv
from datetime import datetime
import pandas as pd
import talib
from functions import incrocio
import requests
import settings  #settings file 


# chat id --->  https://api.telegram.org/bot5073927089:AAE_GYuX7CVMfcUAiYv9FNYG52fFkJbajIQ/getUpdates
def telegram_bot_sendtext(bot_message):
    
    bot_token = settings.BOT_TOKEN
    bot_chatID = settings.CHAT_ID
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()




test=telegram_bot_sendtext('I work ')
start_time=datetime.now()
symbols=[]
with open('forex.csv') as f:  # open the csv file of the companies 
        for row in csv.reader(f):
            symbols.append(row[0])


for symbol in symbols:
    try:
        print(f'processing {symbol}')
        ticker= yf.Ticker(symbol)
        data= ticker.history (period="3d" ,interval="15m")
        try:
            del data['Dividends']
            del data['Stock Splits']
        except: None
        df=pd.DataFrame(data,columns=['Date','Open','High','Low','Close','Volume'])
        slowk, slowd = talib.STOCH(df['High'],df['Low'], df['Close'], fastk_period=10, slowk_period=6, slowk_matype=0, slowd_period=3, slowd_matype=0)
        upper, middle, lower = talib.BBANDS(df['Close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
        macd, macdsignal, macdhist = talib.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
        ema=talib.EMA(df['Close'],timeperiod=100)
        ema200=talib.EMA(df['Close'],timeperiod=200)
        ema=list(ema)
        ema200=list(ema200)
        macd=list(macd)
        macdsignal=list(macdsignal)
        rsi=list(talib.RSI(df['Close']))
        slowk=list(slowk)
        slowd=list(slowd)
        upper=list(upper)
        lower=list(lower)
        df['slowK']=slowk
        df['slowD']=slowd
        df['Upper']=upper 
        df['Lower']=lower
        df['rsi']=rsi
        df['ema200']=ema200 # and (rsi[-1]>50) is True and el[-1]<es[-1]
        #incrocio(ef,es)==1 and rsi[-1]>50 and el[-1]<es[-1]
        #  
        print(df)
        #incrocio(slowk,slowd)==-1 and slowk[-1]>=80 and
        #incrocio(slowk,slowd)==1 and slowk[-1]<=20  and
        if  incrocio(slowk,slowd)==-1 and slowk[-1]>=80 and ema200[-2]>list(df['High'])[-2]:
        
            test=telegram_bot_sendtext(f'{symbol} signal BEARISH STOCHASTIC')
            #
        elif  incrocio(slowk,slowd)==1 and slowk[-1]<=20  and ema200[-2]<list(df['Low'])[-2] :
                
            test=telegram_bot_sendtext(f'{symbol} signal BULLISH STOCHASTIC')
        
        else:
            pass
    # rsi signal
        if  rsi[-1]>=90  :
        
            test=telegram_bot_sendtext(f'{symbol} signal BEARISH RSI')
            #
        elif rsi[-1]<=10:  
                
            test=telegram_bot_sendtext(f'{symbol} signal BULLISH RSI')
        
        else:
            pass
    # macd signal
        if  incrocio(macd,macdsignal)==-1   and macd[-2]>0 and ema[-2]>list(df['High'])[-2]:
        
            test=telegram_bot_sendtext(f'{symbol} signal BEARISH MACD')
            #
        elif incrocio(macd,macdsignal)==1 and macd[-2]<0 and ema[-2]<list(df['Low'])[-2]:  
                
            test=telegram_bot_sendtext(f'{symbol} signal BULLISH MACD')
        
        else:
            pass

    except:
        pass
end_time=datetime.now()
print(f'totale : {end_time-start_time}')
