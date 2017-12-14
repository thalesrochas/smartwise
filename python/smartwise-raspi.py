import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from datetime import datetime
import time
import sys
from gpiozero import LED, Button

# Para possibilitar a impressao de emoji
nbm = dict.fromkeys(range(0x10000, sys.maxunicode+1), 0xfffd)

LUA_CLARA = '\U0001F315'
LUA_ESCURA = '\U0001F311'

luz = [False, False, False, False, False, False]
eletro = [
    {'ligado': False, 'hora': None, 'min': None, 'seg': None},
    {'ligado': False, 'hora': None, 'min': None, 'seg': None},
    {'ligado': False, 'hora': None, 'min': None, 'seg': None},
    {'ligado': False, 'hora': None, 'min': None, 'seg': None}]

luzes = [LED(5), LED(6), LED(13), LED(19), LED(26), LED(21)]
eletros = LED(20)
janp = [Button(23), Button(24)]

numEletro = None

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
            '/eletrodomesticos - Posso ajudá-lo a ligar e desligar alguns eletrodomésticos!\n'
            '/janelas - As janelas estão abertas ou fechadas?\n'
            '/portas - E as portas da casa?\n'
            '/cancelar - Cancela a ação atual.')

    if command == '/cancelar':
        markup = ReplyKeyboardRemove()
        smartwiseBot.sendMessage(chatId, 'Ação cancelada!', reply_markup=markup)

    if command == 'Concluir':
        markup = ReplyKeyboardRemove()
        smartwiseBot.sendMessage(chatId, 'Ação concluída!', reply_markup=markup)

    if command == '/luzes':
        markup = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='\U0001F311 Luz 1' if luz[0] else '\U0001F315 Luz 1'),
           KeyboardButton(text='\U0001F311 Luz 2' if luz[1] else '\U0001F315 Luz 2')],
            [KeyboardButton(text='\U0001F311 Luz 3' if luz[2] else '\U0001F315 Luz 3'),
            KeyboardButton(text='\U0001F311 Luz 4' if luz[3] else '\U0001F315 Luz 4')],
            [KeyboardButton(text='\U0001F311 Luz 5' if luz[4] else '\U0001F315 Luz 5'),
            KeyboardButton(text='\U0001F311 Luz 6' if luz[5] else '\U0001F315 Luz 6')],
            [KeyboardButton(text='Concluir')]])
        smartwiseBot.sendMessage(chatId, 'Escolha no teclado qual luz você deseja ligar \U0001F315 ou desligar \U0001F311!', reply_markup=markup)

    if '\U0001F315 Luz' in command:
        try:
            numLuz = int(command[6])
            luz[numLuz-1] = True

            mensagem = '\U0001F315 Luz ' + str(numLuz) + ' ligada!'
            markup = ReplyKeyboardMarkup(keyboard=[
                [KeyboardButton(text='\U0001F311 Luz 1' if luz[0] else '\U0001F315 Luz 1'),
                KeyboardButton(text='\U0001F311 Luz 2' if luz[1] else '\U0001F315 Luz 2')],
                [KeyboardButton(text='\U0001F311 Luz 3' if luz[2] else '\U0001F315 Luz 3'),
                KeyboardButton(text='\U0001F311 Luz 4' if luz[3] else '\U0001F315 Luz 4')],
                [KeyboardButton(text='\U0001F311 Luz 5' if luz[4] else '\U0001F315 Luz 5'),
                KeyboardButton(text='\U0001F311 Luz 6' if luz[5] else '\U0001F315 Luz 6')],
                [KeyboardButton(text='Concluir')]])
            smartwiseBot.sendMessage(chatId, mensagem, reply_markup=markup)

        except IndexError:
            mensagem = 'Não entendi o que você quis dizer \U0001F625'
            markup = ReplyKeyboardRemove()
            smartwiseBot.sendMessage(chatId, mensagem, reply_markup=markup)
            

    elif '\U0001F311 Luz' in command:
        try:
            numLuz = int(command[6])
            luz[numLuz-1] = False
            
            mensagem = '\U0001F311 Luz ' + str(numLuz) + ' desligada!'
            markup = ReplyKeyboardMarkup(keyboard=[
                [KeyboardButton(text='\U0001F311 Luz 1' if luz[0] else '\U0001F315 Luz 1'),
                KeyboardButton(text='\U0001F311 Luz 2' if luz[1] else '\U0001F315 Luz 2')],
                [KeyboardButton(text='\U0001F311 Luz 3' if luz[2] else '\U0001F315 Luz 3'),
                KeyboardButton(text='\U0001F311 Luz 4' if luz[3] else '\U0001F315 Luz 4')],
                [KeyboardButton(text='\U0001F311 Luz 5' if luz[4] else '\U0001F315 Luz 5'),
                KeyboardButton(text='\U0001F311 Luz 6' if luz[5] else '\U0001F315 Luz 6')],
                [KeyboardButton(text='Concluir')]])
            smartwiseBot.sendMessage(chatId, mensagem, reply_markup=markup)

        except IndexError:
            mensagem = 'Não entendi o que você quis dizer \U0001F625'
            markup = ReplyKeyboardRemove()
            smartwiseBot.sendMessage(chatId, mensagem, reply_markup=markup)

    if command == '/eletrodomesticos':
        markup = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='\U0000274C Ventilador 1' if eletro[0]['ligado'] else '\U00002714 Ventilador 1'),
            KeyboardButton(text='\U0000274C Ventilador 2' if eletro[1]['ligado'] else '\U00002714 Ventilador 2')],
            [KeyboardButton(text='\U0000274C Ventilador 3' if eletro[2]['ligado'] else '\U00002714 Ventilador 3'),
            KeyboardButton(text='\U0000274C Ventilador 4' if eletro[3]['ligado'] else '\U00002714 Ventilador 4')],
            [KeyboardButton(text='Concluir')]])
        smartwiseBot.sendMessage(chatId, 'Escolha qual eletrodoméstico você deseja ligar \U00002714 ou desligar \U0000274C!', reply_markup=markup)

    if '\U00002714 Ventilador' in command:
        try:
            global numEletro
            numEletro = int(command[13])-1
            mensagem = 'Por quanto tempo deseja que o Ventilador ' + str(numEletro+1) + ' fique ligado?'
            markup = ReplyKeyboardMarkup(keyboard=[
                [KeyboardButton(text='1 Minuto \U0001F55B'), KeyboardButton(text='5 Minutos \U0001F550')],
                [KeyboardButton(text='10 Minutos \U0001F551'), KeyboardButton(text='50 Minutos \U0001F552')],
                [KeyboardButton(text='30 Minutos \U0001F555'), KeyboardButton(text='60 Minutos \U0001F55B')],
                [KeyboardButton(text='Eu desligo!'), KeyboardButton(text='/cancelar')]])
            smartwiseBot.sendMessage(chatId, mensagem, reply_markup=markup)

        except IndexError:
            mensagem = 'Não entendi o que você quis dizer \U0001F625'
            markup = ReplyKeyboardRemove()
            smartwiseBot.sendMessage(chatId, mensagem, reply_markup=markup)

    if '\U0000274C Ventilador' in command:
        try:
            eletro[int(command[13])-1]['ligado'] = False
            eletro[int(command[13])-1]['hora'] = None
            eletro[int(command[13])-1]['min'] = None
            eletro[int(command[13])-1]['seg'] = None

            mensagem = 'Ventilador ' + str(numEletro+1) + ' desligado!'
            markup = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='\U0000274C Ventilador 1' if eletro[0]['ligado'] else '\U00002714 Ventilador 1'),
            KeyboardButton(text='\U0000274C Ventilador 2' if eletro[1]['ligado'] else '\U00002714 Ventilador 2')],
            [KeyboardButton(text='\U0000274C Ventilador 3' if eletro[2]['ligado'] else '\U00002714 Ventilador 3'),
            KeyboardButton(text='\U0000274C Ventilador 4' if eletro[3]['ligado'] else '\U00002714 Ventilador 4')],
            [KeyboardButton(text='Concluir')]])
            smartwiseBot.sendMessage(chatId, mensagem, reply_markup=markup)

        except IndexError:
            mensagem = 'Não entendi o que você quis dizer \U0001F625'
            markup = ReplyKeyboardRemove()
            smartwiseBot.sendMessage(chatId, mensagem, reply_markup=markup)

    if 'Minuto' in command:
        try:
            minutos = int(command[:2])
            eletro[numEletro]['ligado'] = True

            data = datetime.now()
            hora = data.hour
            minuto = data.minute
            
            minn = int(minuto) + int(minutos)

            if minn > 60:
                eletro[numEletro]['hora'] = int(hora) + 1
            else:
                eletro[numEletro]['hora'] = int(hora)

            eletro[numEletro]['min'] = minn % 60
            eletro[numEletro]['seg'] = int(data.second)

            markup = ReplyKeyboardMarkup(keyboard=[
                [KeyboardButton(text='\U0000274C Ventilador 1' if eletro[0]['ligado'] else '\U00002714 Ventilador 1'),
                KeyboardButton(text='\U0000274C Ventilador 2' if eletro[1]['ligado'] else '\U00002714 Ventilador 2')],
                [KeyboardButton(text='\U0000274C Ventilador 3' if eletro[2]['ligado'] else '\U00002714 Ventilador 3'),
                KeyboardButton(text='\U0000274C Ventilador 4' if eletro[3]['ligado'] else '\U00002714 Ventilador 4')],
                [KeyboardButton(text='Concluir')]])
            smartwiseBot.sendMessage(chatId, 'O Ventilador ' + str(numEletro+1) + ' irá desligar em '
                + str(minutos) + (' minuto!' if minutos == 1 else ' minutos!'), reply_markup=markup)

        except (TypeError, ValueError):
            mensagem = 'Não entendi o que você quis dizer \U0001F625'
            markup = ReplyKeyboardRemove()
            smartwiseBot.sendMessage(chatId, mensagem, reply_markup=markup)

    if command == 'Eu desligo!':
        try:
            eletro[numEletro]['ligado'] = True
            eletro[numEletro]['hora'] = None
            eletro[numEletro]['min'] = None
            eletro[numEletro]['seg'] = None
            markup = ReplyKeyboardMarkup(keyboard=[
                [KeyboardButton(text='\U0000274C Ventilador 1' if eletro[0]['ligado'] else '\U00002714 Ventilador 1'),
                KeyboardButton(text='\U0000274C Ventilador 2' if eletro[1]['ligado'] else '\U00002714 Ventilador 2')],
                [KeyboardButton(text='\U0000274C Ventilador 3' if eletro[2]['ligado'] else '\U00002714 Ventilador 3'),
                KeyboardButton(text='\U0000274C Ventilador 4' if eletro[3]['ligado'] else '\U00002714 Ventilador 4')],
                [KeyboardButton(text='Concluir')]])
            smartwiseBot.sendMessage(chatId, 'Ventilador ' + str(numEletro+1) + ' foi ligado! Deverá ser desligado manualmente.', reply_markup=markup)

        except TypeError:
            mensagem = 'Não entendi o que você quis dizer \U0001F625'
            markup = ReplyKeyboardRemove()
            smartwiseBot.sendMessage(chatId, mensagem, reply_markup=markup)

    if command == '/portas':
        markup = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='\U0001F6AA Porta Principal'), KeyboardButton(text='\U0001F6AA Porta 1')],
            [KeyboardButton(text='\U0001F6AA Porta 2'), KeyboardButton(text='\U0001F6AA Porta 3')],
            [KeyboardButton(text='\U0001F6AA Porta 4'), KeyboardButton(text='\U0001F6AA Porta 5')],
            [KeyboardButton(text='Concluir')]])
        smartwiseBot.sendMessage(chatId, 'Qual porta você gostaria de verificar?', reply_markup=markup)

    if '\U0001F6AA Porta Principal' in command:
        # Fazer a leitura da entrada do raspi
        smartwiseBot.sendMessage(chatId, 'Não sei ainda')

    elif '\U0001F6AA Porta ' in command:
        smartwiseBot.sendMessage(chatId, 'Porta indisponível.')

    if command == '/janelas':
        markup = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='Janela 1'), KeyboardButton(text='Janela 2')],
            [KeyboardButton(text='Janela 3'), KeyboardButton(text='Janela 4')],
            [KeyboardButton(text='Concluir')]])
        smartwiseBot.sendMessage(chatId, 'Qual janela você gostaria de verificar?', reply_markup=markup)

    if 'Janela 1' in command:
        # Fazer a leitura da entrada do raspi
        smartwiseBot.sendMessage(chatId, 'Não sei ainda')

    elif 'Janela ' in command:
        smartwiseBot.sendMessage(chatId, 'Janela indisponível.')

def timer(bot):
    tempo = datetime.now()
    cont = 0
    for i in eletro:
        cont = cont+1
        if i['hora'] == tempo.hour and i['min'] == tempo.minute and i['seg'] == tempo.second:
            i['ligado'] = False
            i['hora'] = None
            i['min'] = None
            i['seg'] = None
            bot.sendMessage(25245002, 'O Ventilador ' + str(cont) + ' foi desligado!')


def atualizar():
    cont = 0
    for i in luz:
        if i:
            luzes[cont].on()
        else:
            luzes[cont].off()
        cont = cont+1

    if eletro[0]['ligado']:
        eletros.on()
    else:
        eletros.off()


# Token
smartwiseBot = telepot.Bot('421896367:AAHczYKBgmiAcWsuAsU1gsRIu6hAXnPEjEg')

MessageLoop(smartwiseBot, handle).run_as_thread()

while True:
    timer(smartwiseBot)
    atualizar()
    time.sleep(1)

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
