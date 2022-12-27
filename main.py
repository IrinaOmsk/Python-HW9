import telebot
import reader
from random import choice, randint

token = reader.get_token("token")

bot = telebot.TeleBot(token)

is_game_start = False

game_params = {
    "table_candy" : 117,
    "player_candy" : 0,
    "bot_candy" : 0
}

def reset_game():
    global is_game_start
    game_params["table_candy"] = 117
    game_params["player_candy"] = 0
    game_params["bot_candy"] = 0
    is_game_start = False

limit_candy_in_hand = 28

bot_phrases = [
    "Ах так, тогда я возьму ",
    "Хммм... я возьму ",
    "На этом ходу я возьму ",
    "Хотелось бы забрать все, но я возму "
]

def print_current_status(dct):
    text = "***********************************\n" + \
        f"На столе конфет: {dct['table_candy']}\n" + \
        f"У тебя конфет: {dct['player_candy']}\n" + \
        f"У меня конфет: {dct['bot_candy']}\n" + \
        "***********************************"
    return text

gamers = ["human", "bot"]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f"Привет {message.chat.first_name}, пока я умею только играть в конфетки.")
    bot.send_message(message.chat.id, "Напиши /candy что бы начать игру")

@bot.message_handler(commands=['candy'])
def send_welcome(message):
    global is_game_start
    is_game_start = True
    bot.reply_to(message, "Давай я расскажу правила:")   
    text = "На столе лежит 117 конфет. Мы по очереди берём конфеты,\n" + \
        f"но не больше чем {limit_candy_in_hand} за раз.\n" + \
        "Первый ход определяем случайным образом.\n" +\
        "Тот, кто возьмёт последние конфеты, забирает весь мешок!"
    bot.send_message(message.chat.id, text)

    who_next = gamers[randint(0, 1)]
    if who_next == "human":
        bot.send_message(message.chat.id, "В этот раз первым ходишь ты!")
        bot.send_message(message.chat.id, print_current_status(game_params))
        bot.send_message(message.chat.id, "Сколько конфет возьмёшь?")
    else:
        bot.send_message(message.chat.id, "В этот раз первым хохожу я!")
        candies_in_hand = randint(1, limit_candy_in_hand)
        bot.send_message(message.chat.id, choice(bot_phrases[1:]) + f"{candies_in_hand}.")
        game_params["table_candy"] -= candies_in_hand
        game_params["bot_candy"] += candies_in_hand
        bot.send_message(message.chat.id, print_current_status(game_params))
        bot.send_message(message.chat.id, "Твой ход. Сколько конфет возьмёшь?")
        

@bot.message_handler(content_types='text')
def game_round(message):
    if not is_game_start:
         bot.send_message(message.chat.id, "Я не понимаю, возможно ты хочешь поиграть? Тогда введи /candy")
    else:
        candies_in_hand = message.text
        if not candies_in_hand.isdigit():
            bot.send_message(message.chat.id, f"Нужно вводить число, а ты ввел {candies_in_hand}")
        else:
            candies_in_hand = int(candies_in_hand)
            if candies_in_hand > limit_candy_in_hand:
                bot.send_message(message.chat.id, f"Нельзя брать больше {limit_candy_in_hand}")
            elif candies_in_hand <= 0:
                bot.send_message(message.chat.id, f"Ай ай, не мухлюй")
            else:
                game_params["table_candy"] -= candies_in_hand
                game_params["player_candy"] += candies_in_hand
        
                if game_params["table_candy"] <= 0:
                    bot.send_message(message.chat.id, "Поздравляю, ты победил. Все конфеты твои!")
                    reset_game()
                else:
                    if game_params["table_candy"] <= limit_candy_in_hand:
                        bot.send_message(message.chat.id, f"Конечно я беру {game_params['table_candy']}!")
                        bot.send_message(message.chat.id, "На этот раз победа за мной. Все конфеты мои!")
                        reset_game()
                    else:
                        candies_in_hand = randint(1, limit_candy_in_hand)
                        bot.send_message(message.chat.id, choice(bot_phrases) + f"{candies_in_hand}.")
                        game_params["table_candy"] -= candies_in_hand
                        game_params["bot_candy"] += candies_in_hand
                        bot.send_message(message.chat.id, print_current_status(game_params))
                        bot.send_message(message.chat.id, "Твой ход. Сколько конфет возьмёшь?")

bot.infinity_polling()
