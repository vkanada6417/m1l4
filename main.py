import telebot 
from config import token
from logic import Pokemon

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['go'])
def go(message):
    if message.from_user.username not in Pokemon.pokemons.keys():
        pokemon = Pokemon(message.from_user.username)
        bot.send_message(message.chat.id, pokemon.info())
        bot.send_photo(message.chat.id, pokemon.show_img())
        
        if pokemon.is_rare:
            bot.send_message(message.chat.id, pokemon.add_achievement())
    else:
        bot.reply_to(message, "Ты уже создал себе покемона")

@bot.message_handler(commands=['rename'])
def rename(message):
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "Укажите новое имя для покемона: /rename <новое_имя>")
        return

    if message.from_user.username in Pokemon.pokemons:
        new_name = args[1]
        Pokemon.pokemons[message.from_user.username].set_name(new_name)
        bot.send_message(message.chat.id, f"Имя покемона изменено на {new_name}")
    else:
        bot.reply_to(message, "Сначала создайте покемона с помощью команды /go")

@bot.message_handler(commands=['info'])
def info(message):
    if message.from_user.username in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[message.from_user.username]
        bot.send_message(message.chat.id, pokemon.info())
    else:
        bot.reply_to(message, "Сначала создайте покемона с помощью команды /go")

@bot.message_handler(commands=['feed'])
def feed(message):
    if message.from_user.username in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[message.from_user.username]
        result = pokemon.feed()
        bot.send_message(message.chat.id, result)
    else:
        bot.reply_to(message, "Сначала создайте покемона с помощью команды /go")

@bot.message_handler(commands=['help'])
def help(message):
    help_text = (
        "Доступные команды:\n"
        "/go - Создать нового покемона.\n"
        "/info - Показать информацию о вашем покемоне.\n"
        "/rename <новое_имя> - Изменить имя вашего покемона.\n"
        "/feed - Покормить покемона.\n"
        "/help - Показать список команд и их описание."
    )
    bot.send_message(message.chat.id, help_text)

bot.infinity_polling(none_stop=True)
