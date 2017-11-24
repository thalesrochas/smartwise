import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import serial
import time
import sys

# Para possibilitar a impressao de emoji
nbm = dict.fromkeys(range(0x10000, sys.maxunicode+1), 0xfffd)

ser = serial.Serial('COM3', 9600)

LUA_CLARA = '\U0001F315'
LUA_ESCURA = '\U0001F311'

luz = [False, False, False, False, False, False]

def handle(msg):
    contentType, chatType, chatId = telepot.glance(msg)

    command = msg['text']

    print('User: %s \tId: %s \tComando: %s'.translate(nbm) % (msg['from']['first_name'], chatId, command))

    if contentType != 'text':
        return

    if command == '/start':
        smartwiseBot.sendMessage(chatId, 'Olá, eu sou o Smartwise e vou ajudá-lo a controlar sua casa!\n'
            'Para saber o que eu posso fazer use o comando /ajuda.')

    if command == '/ajuda':
        smartwiseBot.sendMessage(chatId, 'Esses são os comandos que você pode usar para que eu possa ajudá-lo:\n'
            '/luzes - Posso ajudá-lo a verificar as luzes da casa, ligando ou desligando-as!\n'
            '/janelas - As janelas estão abertas ou fechadas?\n'
            '/portas - \U0001F6AA E as portas da casa?\n'
            '/cancelar - Cancela a ação atual.')

    if command == '/cancelar':
        markup = ReplyKeyboardRemove()
        smartwiseBot.sendMessage(chatId, 'Ação cancelada!', reply_markup=markup)

    if command == 'Concluir':
        markup = ReplyKeyboardRemove()
        smartwiseBot.sendMessage(chatId, 'Ação concluída!', reply_markup=markup)

    if command == '/luzes':
        markup = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='\U0001F315 Luz 1' if luz[0] else '\U0001F311 Luz 1'),
            KeyboardButton(text='\U0001F315 Luz 2' if luz[1] else '\U0001F311 Luz 2')],
            [KeyboardButton(text='\U0001F315 Luz 3' if luz[2] else '\U0001F311 Luz 3'),
            KeyboardButton(text='\U0001F315 Luz 4' if luz[3] else '\U0001F311 Luz 4')],
            [KeyboardButton(text='\U0001F315 Luz 5' if luz[4] else '\U0001F311 Luz 5'),
            KeyboardButton(text='\U0001F315 Luz 6' if luz[5] else '\U0001F311 Luz 6')],
            [KeyboardButton(text='Concluir')]])
        smartwiseBot.sendMessage(chatId, 'Escolha no teclado qual luz você deseja ligar/desligar!', reply_markup=markup)

    if '\U0001F311 Luz' in command:
        try:
            numLuz = int(command[6])
            luz[numLuz-1] = True
            
            ser.write(b'H')
            ser.write(bytes([numLuz]))

            mensagem = '\U0001F315 Luz ' + str(numLuz) + ' ligada!'
            markup = ReplyKeyboardMarkup(keyboard=[
                [KeyboardButton(text='\U0001F315 Luz 1' if luz[0] else '\U0001F311 Luz 1'),
                KeyboardButton(text='\U0001F315 Luz 2' if luz[1] else '\U0001F311 Luz 2')],
                [KeyboardButton(text='\U0001F315 Luz 3' if luz[2] else '\U0001F311 Luz 3'),
                KeyboardButton(text='\U0001F315 Luz 4' if luz[3] else '\U0001F311 Luz 4')],
                [KeyboardButton(text='\U0001F315 Luz 5' if luz[4] else '\U0001F311 Luz 5'),
                KeyboardButton(text='\U0001F315 Luz 6' if luz[5] else '\U0001F311 Luz 6')],
                [KeyboardButton(text='Concluir')]])
            smartwiseBot.sendMessage(chatId, mensagem, reply_markup=markup)

        except IndexError:
            mensagem = 'Não entendi o que você quis dizer \U0001F625'
            markup = ReplyKeyboardRemove()
            smartwiseBot.sendMessage(chatId, mensagem, reply_markup=markup)
            

    elif '\U0001F315 Luz' in command:
        try:
            numLuz = int(command[6])
            luz[numLuz-1] = False
            
            ser.write(b'L')
            ser.write(bytes([numLuz]))
            
            mensagem = '\U0001F311 Luz ' + str(numLuz) + ' desligada!'
            markup = ReplyKeyboardMarkup(keyboard=[
                [KeyboardButton(text='\U0001F315 Luz 1' if luz[0] else '\U0001F311 Luz 1'),
                KeyboardButton(text='\U0001F315 Luz 2' if luz[1] else '\U0001F311 Luz 2')],
                [KeyboardButton(text='\U0001F315 Luz 3' if luz[2] else '\U0001F311 Luz 3'),
                KeyboardButton(text='\U0001F315 Luz 4' if luz[3] else '\U0001F311 Luz 4')],
                [KeyboardButton(text='\U0001F315 Luz 5' if luz[4] else '\U0001F311 Luz 5'),
                KeyboardButton(text='\U0001F315 Luz 6' if luz[5] else '\U0001F311 Luz 6')],
                [KeyboardButton(text='Concluir')]])
            smartwiseBot.sendMessage(chatId, mensagem, reply_markup=markup)

        except IndexError:
            mensagem = 'Não entendi o que você quis dizer \U0001F625'
            markup = ReplyKeyboardRemove()
            smartwiseBot.sendMessage(chatId, mensagem, reply_markup=markup)

    if command == '/janelas' or command == '/portas':
        smartwiseBot.sendMessage(chatId, 'Ainda não fui programado para fazer isso \U0001F62C')

#Token
smartwiseBot = telepot.Bot('421896367:AAHczYKBgmiAcWsuAsU1gsRIu6hAXnPEjEg')

# 
MessageLoop(smartwiseBot, handle).run_as_thread()

while True:
    time.sleep(10)

'''
Mensagem Recebida do Usuario
{'message_id': 55,
 'from': {'id': 25245002,
          'is_bot': False,
          'first_name': 'Thales',
          'last_name': 'Rocha',
          'username': 'thalesrochas',
          'language_code': 'pt-BR'},
 'chat': {'id': 25245002,
          'first_name': 'Thales',
          'last_name': 'Rocha',
          'username': 'thalesrochas',
          'type': 'private'},
 'date': 1504834814,
 'text': 'a msg tá aqui'}

Mensagem Enviada pelo BOT
{'text': 'showzi',
 'chat': {'username': 'thalesrochas',
          'last_name': 'Rocha',
          'id': 25245002,
          'type': 'private',
          'first_name': 'Thales'},
 'message_id': 657,
 'date': 1504982033,
 'from': {'username': 'SmartwiseBot',
          'first_name': 'Smartwise',
          'id': 421896367,
          'is_bot': True}}

'''
