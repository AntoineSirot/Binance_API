import requests;
import json;
from datetime import datetime
import sqlite3


# Get a list of all available token and display it
def getTokens():
  response = requests.get("https://data.binance.com/api/v3/ticker/price")
  json_response = response.json()
  set_token = set()
  for i in json_response :
    if ('USDT' in i['symbol']) :
      set_token.add(i['symbol'].replace('USDT',''))
  set_token.add('USDT')
  print(sorted(set_token))
  
#getTokens()


# Get a function to display tthe 'ask' or 'bid' price of an asset
def getDepth(direction, pair):
    r = requests.get("https://data.binance.com/api/v3/depth",params=dict(symbol=pair))
    results = r.json()
    print(results[direction])

#getDepth("asks", "BTCUSDT")


#Get Order book for an asset
def getOrderBook(pair):
    r = requests.get("https://data.binance.com/api/v3/depth",params=dict(symbol=pair))
    results = r.json()
    print(results)

#getOrderBook("BTCUSDT")

# Get candles for a specific pair with a specific time 
def refreshDataCandle (pair, duration) :

  d = requests.get('https://data.binance.com/api/v3/klines?symbol='+pair+'&interval='+duration).json()
  L2=[]
  L3=[]
  for i in range (len(d)):
      L2.append(i)
      L2.append(datetime.fromtimestamp(d[i][0]/1000).strftime("%A, %B %d, %Y %I:%M:%S"))
      for j in range (1,6) :
              L2.append(d[i][j])
      L3.append(L2)
      L2=[]

  print(["id","date ","Open price","High price","Low price","Close price","Volume"])
  for i in L3 :
    print(i)

#refreshDataCandle('BTCUSDT','1h')


# First implementation of candles table :

# connecting to the database
connection = sqlite3.connect("candles.db")
crsr = connection.cursor()
 
# sql_command = """CREATE TABLE candles (id INTEGER PRIMARY KEY,date INT,high REAL,low REAL,open REAL,close REAL,volume REAL);"""
# crsr.execute(sql_command)

def refreshDataCandle (pair, duration) :

  d = requests.get('https://data.binance.com/api/v3/klines?symbol='+pair+'&interval='+duration).json()
  L2=[]
  L3=[]
  for i in range (len(d)):
      L2.append(i+1)
      for j in range (0,6) :
              L2.append(d[i][j])
      sql_command = """INSERT INTO candles (id, date, high, low, open, close, volume) VALUES (""" + str(L2)[1:len(str(L2))-1] + """);"""
      crsr.execute(sql_command)
      L2=[]

# You can choose a pair here
# refreshDataCandle('BTCUSDT','1h')
# connection.commit()
connection.close()


# Print previous database :

connection = sqlite3.connect("candles.db")
crsr = connection.cursor()


def get_posts():

  crsr.execute("SELECT * FROM candles")
  print(crsr.fetchall())

get_posts()
connection.close()
