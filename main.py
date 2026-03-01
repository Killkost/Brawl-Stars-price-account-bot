import requests,json,telebot,time
from bs4 import BeautifulSoup
from telebot import TeleBot,types
from translate import Translator
# здесь мы реализуем обработку получения запроса по тегу для продажи аккаунта
getUserToken = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImNiZmE0MzZkLTM5NTEtNDlmOC1iMTBiLWFlMjZlNjZkMzA2NiIsImlhdCI6MTcxMDI2OTg2NSwic3ViIjoiZGV2ZWxvcGVyL2E4ZDY5YjZmLWY3NWUtZDYxZS0wMzc5LTM4ZWM2YzgwZTVlYyIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiNDUuNzkuMjE4Ljc5Il0sInR5cGUiOiJjbGllbnQifV19.8VvHF6GLKmX19etMgBHQNyoIUfcpBbZYn3bLnUK--cDGqXZ8UPvCNBQo654I_QQgwYJnGOd7rWsZSKmgS1Lldw'
data=0
lan="en"
def getuserinfo(url,token):
    headers = {
        'Accept': 'application/json',
        'authorization': f'Bearer {token}'
    }

    playerInfo = requests.get(url,headers=headers)

    if playerInfo.status_code == 200:
        data = playerInfo.json()
    else:
        #print(f"Ошибка: {playerInfo.status_code}")
        #print(playerInfo.text)
        
        return False
    return data

def calculateprice(coins,powpoints,blings,gems,datadict):
    result = 0 # in dollars
    result+=(coins/500*0.1)+(powpoints/200*0.1)+(blings/400*0.1)+(gems/20*0.1)
    result+=int(datadict['trophies'])/150*0.1
    
    for i in datadict['brawlers']:

        result+=list(i.values())[2]/100
        result+=list(i.values())[3]/100
        if len(list(i.values())[6]) > 0:
            result += len(list(i.values())[6])/100
        if len(list(i.values())[7]) > 0:
            result += len(list(i.values())[7])/100
        if len(list(i.values())[8]) > 0:
            result += len(list(i.values())[8])/100
    return result

def translate(text, target_language='en'):
    translator= Translator(to_lang=target_language)
    translation = translator.translate(text)
    return translation


tgToken = '6880510908:AAG6M6orlQNXRuPTAPh9TMDSJlkJYpZoXIA'
bot = TeleBot(tgToken)
state = {}
tag=""
coins=0
powpoints=0
gems=0
blings=0
@bot.message_handler(commands=['start'])
def startfunc(message):
    firstMenu = types.InlineKeyboardMarkup()
    buttonStartCalculate = types.InlineKeyboardButton(translate("Calculate Your Price💰",lan), callback_data="calculate")
    button_choose_language=types.InlineKeyboardButton(translate("change the language",lan), callback_data="changelan")
    firstMenu.add(buttonStartCalculate)
    firstMenu.add(button_choose_language)
    bot.send_message(message.chat.id, translate("Hi, it is a bot to calculate the price of your Brawl Stars account",lan), reply_markup=firstMenu)

@bot.callback_query_handler(func=lambda call: True)
def checkbuttons(call):
    global lan
    mesid = call.message.chat.id
    if call.data == "calculate":
        reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttonToMainMenu = types.KeyboardButton(translate("back to main menu",lan).lower())
        reply_markup.add(buttonToMainMenu)
        bot.send_message(mesid, translate("Okay, let's start",lan))
        bot.send_message(mesid, translate("Tag(with # in the begin):",lan),reply_markup=reply_markup)
        state[mesid] = "tag"
        call.data=''
    elif call.data=="changelan":
        languageMenu = types.InlineKeyboardMarkup()
        if lan == "uk":
            ukrainianbutton =types.InlineKeyboardButton("Українська мова🇺🇦", callback_data="changelantoua")
        else:
            ukrainianbutton =types.InlineKeyboardButton(translate("Ukrainian language🇺🇦",lan), callback_data="changelantoua")

        languageMenu.add(ukrainianbutton)
        englishbutton = types.InlineKeyboardButton(translate("English language🇬🇧",lan),callback_data="changelantoen")
        languageMenu.add(englishbutton)
        bot.send_message(mesid,translate("choose the language",lan),reply_markup=languageMenu)
    elif call.data == "changelantoua":
        lan="uk"
        reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttonToMainMenu = types.KeyboardButton(translate("back to main menu",lan).lower())
        reply_markup.add(buttonToMainMenu)
        firstMenu = types.InlineKeyboardMarkup()
        buttonStartCalculate = types.InlineKeyboardButton(translate("Calculate Your Price💰",lan), callback_data="calculate")
        button_choose_language=types.InlineKeyboardButton(translate("change the language",lan), callback_data="changelan")
        firstMenu.add(buttonStartCalculate)
        firstMenu.add(button_choose_language)
        bot.send_message(mesid,translate("changes were applied",lan),reply_markup=reply_markup)
        bot.send_message(mesid, translate("Hi, it is a bot to calculate the price of your Brawl Stars account",lan), reply_markup=firstMenu)
        call.data=''
    elif call.data == "changelantoen":
        lan="en"
        reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttonToMainMenu = types.KeyboardButton(translate("back to main menu",lan).lower())
        reply_markup.add(buttonToMainMenu)
        firstMenu = types.InlineKeyboardMarkup()
        buttonStartCalculate = types.InlineKeyboardButton(translate("Calculate Your Price💰",lan), callback_data="calculate")
        button_choose_language=types.InlineKeyboardButton(translate("change the language",lan), callback_data="changelan")
        firstMenu.add(buttonStartCalculate)
        firstMenu.add(button_choose_language)
        bot.send_message(mesid,translate("changes were applied",lan),reply_markup=reply_markup)
        bot.send_message(mesid, translate("Hi, it is a bot to calculate the price of your Brawl Stars account",lan), reply_markup=firstMenu)
        call.data=''



@bot.message_handler(func=lambda message: state.get(message.chat.id) == "mainmenu")
def mainmenu(message):
    if message.text == translate("back to main menu",lan).lower():
        state[message.chat.id] = "mainmenu"
    firstMenu = types.InlineKeyboardMarkup()
    buttonStartCalculate = types.InlineKeyboardButton(translate("Calculate Your Price💰",lan), callback_data="calculate")
    button_choose_language=types.InlineKeyboardButton(translate("change the language",lan), callback_data="changelan")
    firstMenu.add(buttonStartCalculate)
    firstMenu.add(button_choose_language)
    bot.send_message(message.chat.id, translate("Hi, it is a bot to calculate the price of your Brawl Stars account",lan), reply_markup=firstMenu)
  

@bot.message_handler(func=lambda message: state.get(message.chat.id) == "tag")
def mes1(message):
    global tag
    if message.text == translate("back to main menu",lan).lower():
        state[message.chat.id] = "mainmenu" 
        firstMenu = types.InlineKeyboardMarkup()
        buttonStartCalculate = types.InlineKeyboardButton(translate("Calculate Your Price💰",lan), callback_data="calculate")
        button_choose_language=types.InlineKeyboardButton(translate("change the language",lan), callback_data="changelan")
        firstMenu.add(buttonStartCalculate)
        firstMenu.add(button_choose_language)
        bot.send_message(message.chat.id, translate("Hi, it is a bot to calculate the price of your Brawl Stars account",lan), reply_markup=firstMenu)
  
    if state[message.chat.id] != "mainmenu": 
        tag = message.text
    # print(tag)
        state[message.chat.id] = "blings"
        if lan=="uk":
            bot.send_message(message.chat.id, "Кількість блінгів💎:")
        else:
            bot.send_message(message.chat.id, "Blings amount💎:")
    
@bot.message_handler(func=lambda message: state.get(message.chat.id) == "blings")
def mes2(message):
    global blings
    if message.text == translate("back to main menu",lan).lower():
        state[message.chat.id] = "mainmenu" 
        firstMenu = types.InlineKeyboardMarkup()
        buttonStartCalculate = types.InlineKeyboardButton(translate("Calculate Your Price💰",lan), callback_data="calculate")
        button_choose_language=types.InlineKeyboardButton(translate("change the language",lan), callback_data="changelan")
        firstMenu.add(buttonStartCalculate)
        firstMenu.add(button_choose_language)
        bot.send_message(message.chat.id, translate("Hi, it is a bot to calculate the price of your Brawl Stars account",lan), reply_markup=firstMenu)
 
    if state[message.chat.id] != "mainmenu":
        try:
            if (message.text).count(".") > 0:
                bot.send_message(message.chat.id, translate("enter integer",lan))
                state[message.chat.id] = "blings"
            else:
                blings = int(message.text)
                state[message.chat.id] = "coins"
                if lan=="uk":
                    bot.send_message(message.chat.id, "Кількість монет🪙:")
                else:
                    bot.send_message(message.chat.id, "Coins amount🪙:")
                    
        
        except:
            bot.send_message(message.chat.id, translate("enter integer",lan))
            state[message.chat.id] = "blings"
    

    
@bot.message_handler(func=lambda message: state.get(message.chat.id) == "coins")
def mes3(message):
    global coins
    if message.text == translate("back to main menu",lan).lower():
        state[message.chat.id] = "mainmenu" 
        firstMenu = types.InlineKeyboardMarkup()
        buttonStartCalculate = types.InlineKeyboardButton(translate("Calculate Your Price💰",lan), callback_data="calculate")
        button_choose_language=types.InlineKeyboardButton(translate("change the language",lan), callback_data="changelan")
        firstMenu.add(buttonStartCalculate)
        firstMenu.add(button_choose_language)
        bot.send_message(message.chat.id, translate("Hi, it is a bot to calculate the price of your Brawl Stars account",lan), reply_markup=firstMenu)
 
    if state[message.chat.id] != "mainmenu":
        try:
            if (message.text).count(".") > 0:
                bot.send_message(message.chat.id, translate("enter integer",lan))
                state[message.chat.id] = "coins"
            else:
                coins = int(message.text)
                state[message.chat.id] = "gems"

                if lan == "uk":
                    bot.send_message(message.chat.id, "Кількість гемів🟢💎:")
                else:
                    bot.send_message(message.chat.id, "Gems amount🟢💎:")
        except:
            bot.send_message(message.chat.id, translate("enter integer",lan))
            state[message.chat.id] = "coins"

@bot.message_handler(func=lambda message: state.get(message.chat.id) == "gems")
def mes4(message):
    global gems
    if message.text == translate("back to main menu",lan).lower():
        state[message.chat.id] = "mainmenu" 
        firstMenu = types.InlineKeyboardMarkup()
        buttonStartCalculate = types.InlineKeyboardButton(translate("Calculate Your Price💰",lan), callback_data="calculate")
        button_choose_language=types.InlineKeyboardButton(translate("change the language",lan), callback_data="changelan")
        firstMenu.add(buttonStartCalculate)
        firstMenu.add(button_choose_language)
        bot.send_message(message.chat.id, translate("Hi, it is a bot to calculate the price of your Brawl Stars account",lan), reply_markup=firstMenu)
 
    if state[message.chat.id] != "mainmenu":
        try:
            if (message.text).count(".") > 0:
                bot.send_message(message.chat.id, translate("enter integer",lan))
                state[message.chat.id] = "gems"
            else:
                gems = int(message.text)
                state[message.chat.id] = "powpoints"
                if lan == "uk":
                    bot.send_message(message.chat.id, "Кількість очок сили🟣💎: ")
                else:
                    bot.send_message(message.chat.id, "Power Points amount🟣💎: ")
        except:
            bot.send_message(message.chat.id, translate("enter integer",lan))
            state[message.chat.id] = "gems"
@bot.message_handler(func=lambda message: state.get(message.chat.id) == "powpoints")
def mes5(message):
    global powpoints,state
    if message.text == translate("back to main menu",lan).lower():
        state[message.chat.id] = "mainmenu" 
        firstMenu = types.InlineKeyboardMarkup()
        buttonStartCalculate = types.InlineKeyboardButton(translate("Calculate Your Price💰",lan), callback_data="calculate")
        button_choose_language=types.InlineKeyboardButton(translate("change the language",lan), callback_data="changelan")
        firstMenu.add(buttonStartCalculate)
        firstMenu.add(button_choose_language)
        bot.send_message(message.chat.id, translate("Hi, it is a bot to calculate the price of your Brawl Stars account",lan), reply_markup=firstMenu)
 
    if state[message.chat.id] != "mainmenu":
        if True:
            if (message.text).count(".") > 0:
                bot.send_message(message.chat.id, translate("enter integer",lan))
                state[message.chat.id] = "powpoints"
            else:
                powpoints = int(message.text)
                data = getuserinfo(f'https://bsproxy.royaleapi.dev/v1/players/%23{tag[1:].upper()}',getUserToken)
                if data == False:
                    bot.send_message(message.chat.id,translate("please, enter the valid tag and try again",lan))
                    state[message.chat.id] = "tag"
                else:
                    bot.send_message(message.chat.id, translate("Price of this account is: ",lan))
                    bot.send_message(message.chat.id,translate(f"{round(calculateprice(coins,powpoints,blings,gems,getuserinfo(f'https://bsproxy.royaleapi.dev/v1/players/%23{tag[1:].upper()}',getUserToken)),2)} $",lan))
                    state[message.chat.id] = "mainmenu" 
                    firstMenu = types.InlineKeyboardMarkup()
                    buttonStartCalculate = types.InlineKeyboardButton(translate("Calculate Your Price💰",lan), callback_data="calculate")
                    button_choose_language=types.InlineKeyboardButton(translate("change the language",lan), callback_data="changelan")
                    firstMenu.add(buttonStartCalculate)
                    firstMenu.add(button_choose_language)
                    bot.send_message(message.chat.id, translate("Hi, it is a bot to calculate the price of your Brawl Stars account",lan), reply_markup=firstMenu)
 
                    state[message.chat.id] = "tag"

bot.polling()


