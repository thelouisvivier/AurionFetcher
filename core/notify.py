"""
    Telegram Notifier
"""
# Credentials
from config import *

# Telegram
import telegram

# Datetime
from datetime import datetime
from dateutil.parser import parse


def telegramNotifier(trail,returnedStats):

    now = datetime.now()

    #If there are changes, or it's time for dayly notification
    if (returnedStats["countEdited"] != 0 or returnedStats["countAdded"] != 0 or returnedStats["countDeleted"] != 0) or now.hour ==23:

        #Init bot
        bot = telegram.Bot(token=telegram_token)
        msgCounter = 0

        #Summed informations/stats
        message = "📥{} ✔️{} ✏️{} 🗑{} ➕{}\n\n".format(returnedStats["countFetched"],returnedStats["countPassed"],returnedStats["countEdited"],returnedStats["countDeleted"],returnedStats["countAdded"])

        #Loop in edited events
        for editedEvent in returnedStats["editedEvents"]:
            #Check if message is not too long for telegram, else split it
            if (msgCounter > 25):
                bot.sendMessage(chat_id=telegram_chatid, text=message,parse_mode=telegram.ParseMode.HTML)
                message = ''
                msgCounter = 1
                message += "✏️<b>Edited</b>\n{}\n<i>{} à {}\n{}\n{}</i>\n\n".format(editedEvent.name,parse(str(editedEvent.begin)).strftime("%d/%m/%Y de %H:%M"),parse(str(editedEvent.end)).strftime("%H:%M"),editedEvent.location,editedEvent.description)
            else:
                msgCounter += 1
                message += "✏️<b>Edited</b>\n{}\n<i>{} à {}\n{}\n{}</i>\n\n".format(editedEvent.name,parse(str(editedEvent.begin)).strftime("%d/%m/%Y de %H:%M"),parse(str(editedEvent.end)).strftime("%H:%M"),editedEvent.location,editedEvent.description)

        #Loop in added events
        for addedEvent in returnedStats["addedEvents"]:
            #Check if message is not too long for telegram, else split it
            if (msgCounter > 25):
                bot.sendMessage(chat_id=telegram_chatid, text=message,parse_mode=telegram.ParseMode.HTML)
                message = ''
                msgCounter = 1
                message += "➕<b>Added</b>\n{}\n{} à {}\n{}\n<i>{}</i>\n\n".format(addedEvent.name,parse(str(addedEvent.begin)).strftime("%d/%m/%Y de %H:%M"),parse(str(addedEvent.end)).strftime("%H:%M"),addedEvent.location,addedEvent.description)
            else:
                message += "➕<b>Added</b>\n{}\n{} à {}\n{}\n<i>{}</i>\n\n".format(addedEvent.name,parse(str(addedEvent.begin)).strftime("%d/%m/%Y de %H:%M"),parse(str(addedEvent.end)).strftime("%H:%M"),addedEvent.location,addedEvent.description)
                msgCounter += 1

        #send message
        bot.sendMessage(chat_id=telegram_chatid, text=message,parse_mode=telegram.ParseMode.HTML)

        #Log informations
        if(now.hour ==23):
            print("        Daily Notification. Sent")
        else:
            print("        Changes Detected. Notification Sent")

    #0 changes. Don't send a notification
    else:
        #Log informations
        print("        Nothing Changed. No Notification Sent.")
