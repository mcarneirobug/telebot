# -- coding:utf-8 --
import telebot
import json  # values in json and xml
import urllib.request as ur  # manipulation of urls

API_TOKEN = ''

bot = telebot.TeleBot(API_TOKEN)


def get_cid(self):
    return self.chat.id


@bot.message_handler(commands=['start'])
def send_start(message):
    bot.send_message(get_cid(message), "Olá, seja bem vindo sou o bot_teteus")
    bot.reply_to(message, 'As opções disponíveis são: ' +
                 '\n1: /cep'
                 '\n2: /vagalumes'
                 )


@bot.message_handler(commands=['cep'])
def send_cep(message):
    msg = bot.reply_to(message,
                       'Digite o cep que deseja consultar: '
                       )
    bot.register_next_step_handler(msg, send_cep_step)


def send_cep_step(message):
    msg_cep = message.text
    url = "https://viacep.com.br/ws/" + msg_cep + "/json/"
    response = ur.urlopen(url)

    data = json.loads(response.read())
    print(data)

    cep = data['cep']
    logradouro = data['logradouro']
    bairro = data['bairro']
    localidade = data['localidade']
    uf = data['uf']
    bot.send_message(get_cid(message), "CEP: " + cep +
                     "\nLogradouro: " + logradouro +
                     "\nBairro: " + bairro +
                     "\nLocalidade: " + localidade +
                     "\nUF: " + uf
                     )


@bot.message_handler(commands=['vagalumes'])
def send_vagalumes(message):
    msg = bot.reply_to(message,
                       'Digite o artista que deseja consultar: ',
                       )
    bot.register_next_step_handler(msg,
                                   send_vagalumes_step)


def send_vagalumes_step(message):
    artista = message.text
    artista.encode('utf-8')
    url = "https://www.vagalume.com.br/" + artista.lower() + "/index.js"
    response = ur.urlopen(url)
    data = json.loads(response.read())
    print(data)
    artist = data['artist']['desc']
    # genre = data['artist']['genre']

    bot.send_message(get_cid(message),
                     "Artista: " + artist +
                     "Gênero" + genre
                     )
    bot.send_photo(get_cid(message), photo='https://www.vagalume.com.br/' + data['artist']['pic_medium'])


bot.polling()
