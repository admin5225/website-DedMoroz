import datetime
import random
import telebot
from tok import TOKEN
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from images.randomIMAGE import img
from music import dt
from translate import Translator
import requests
from mongodb import mdb, search_or_save_user, save_user_info

tb = telebot.TeleBot(TOKEN)
due = 0
flag = 0
total = 0
user = ''
reply_keyboard = [['/info'],
                  ['/website'],
                  ['/game_quiz'], ['/add_functions']]
communication = [['/contacts'], ['/download_game'], ['/back']]
main_answer = [['/yes'], ['/no']]
addFunction = [['/christmas_image'], ['/christmas_music'], ['/advice'], ['/time_untilNY'], ['/back']]
reply_close_timer = [['/close']]
choicer = [['/1'], ['/2'], ['/3'], ['/4'], ['/main_window']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
markupFUNC = ReplyKeyboardMarkup(addFunction, one_time_keyboard=False)
markup_choice = ReplyKeyboardMarkup(choicer, one_time_keyboard=False)
markup2 = ReplyKeyboardMarkup(communication, one_time_keyboard=False)
markup3 = ReplyKeyboardMarkup(main_answer, one_time_keyboard=False)
markup4 = ReplyKeyboardMarkup(reply_close_timer, one_time_keyboard=False)


def get_advice(update, context):
    response = requests.get('https://api.adviceslip.com/advice')
    data = response.json()
    text = data['slip']['advice']

    translator = Translator(to_lang="RU")
    translation = translator.translate(text)
    if 'WARNING' in translation:
        update.message.reply_text(text,
                                  reply_markup=markupFUNC)
    else:
        update.message.reply_text(translation,
                                  reply_markup=markupFUNC)


def info(update, context):
    update.message.reply_text('ИГРА ГОДА 2021!', reply_markup=markup2)


def download_game(update, context):
    update.message.reply_text('https://clck.ru/UQido')


def website(update, context):
    update.message.reply_text('https://slavina-flask-proga.herokuapp.com/', reply_markup=markup)


def add_functions(update, context):
    update.message.reply_text('1) Рандомная фотография с Рождеством!\n2) Рандомный совет на день!\n3) Случайный '
                              'совет!\n 4) Сколько дней до нового года?',
                              reply_markup=markupFUNC)


def christmas_image(update, context):
    update.message.reply_text('Загружаю картинку...')
    photo = random.choice(img)
    if not photo:
        photo = random.choice(img)
    tb.send_photo(update.message.chat_id,
                  photo)


def christmas_music(update, context):
    try:
        ms = random.choice(dt)
        update.message.reply_text(f'Идет загрузка\n{ms[:-4]}...')
        print(f'music/{ms}')
        mus = open(f'music/{ms}', 'rb')
        tb.send_document(update.message.chat_id, mus)
    except Exception as r:
        update.message.reply_text('ОШИБКА! Попробуйте еще раз! Или чуть похже...')


def contacts(update, context):
    photo = 'https://i.pinimg.com/originals/d0/8f/0a/d08f0a9a93af07aa14a710fb3bc92f4d.jpg'
    tb.send_photo(update.message.chat_id,
                  photo)
    update.message.reply_text(
        f"@slaav1k")


def game_quiz(update, context):
    update.message.reply_text(
        f"Хочешь сыграть в викторину?", reply_markup=markup3)


def yes(update, context):
    global flag
    global user
    user = search_or_save_user(mdb, update.effective_user, total)
    flag = 1
    update.message.reply_text(
        f"Тогда мы НАЧНАЕМ!\nГде живет дед мороз?\n1) На северном полюсе.\n2) На южном полюсе.\n3) В Крыму!\n4) В "
        f"Солотче!", reply_markup=markup_choice)


def help(update, context):
    update.message.reply_text(
        "Я пока не умею помогать... Я только ваше эхо.")


def first(update, context):
    global flag, total
    if flag == 1:
        flag += 1
        total += 1
        update.message.reply_text(
            "Верно!\nКак называется праздник, на который приходит Дед Мороз?\n1) Пасха.\n2) День знаний."
            "\n3) Новый Год.\n4) Масленица.", reply_markup=markup_choice)
    elif flag == 5:
        flag += 1
        total += 1
        update.message.reply_text(
            "Верно!\nЧто на ногах у Деда Мороза?\n1) Унты.\n2) Валенки."
            "\n3) Сапоги.\n4) Черевички.", reply_markup=markup_choice)
    elif flag == 13:
        flag += 1
        total += 1
        update.message.reply_text(
            "Верно!\nУ представителей какого народа под Новый год принято вспоминать о совершенных грехах и давать "
            "обещание искупить их новыми делами в Новом году?\n1) Евреи.\n2) Aфганцы. "
            "\n3) Греки.\n4) Японцы.", reply_markup=markup_choice)
    elif flag == 14:
        flag += 1
        total += 1
        update.message.reply_text(
            "Верно!\nКитайцы считают, что первый день наступившего года окутан злыми духами, которых необходимо "
            "отпугнуть. Чем китайцы их отпугивают?\n1) Рисом.\n2) Чаем. "
            "\n3) Петардами.\n4) Волшебными словами.", reply_markup=markup_choice)
    else:
        global user
        user = search_or_save_user(mdb, update.effective_user, total)
        if int(user["total"]) < total:
            user = save_user_info(mdb, user, update.effective_user, total)
        all_info = list(mdb.users.find({}))
        out_info1 = []
        out_info = []
        for i in all_info:
            out_info1.append((i["name"], int(i["total"])))
        out_info1 = sorted(out_info1, key=lambda x: x[1], reverse=True)
        k = 0
        for i in out_info1:
            k += 1
            out_info.append(f'{k}) {i[0]} {i[1]}')
        out_info = "\n".join(out_info)
        print(list(all_info))
        update.message.reply_text(
            f'ТЫ не угадал!\n\n\nА теперь рекорды! \n{out_info}')
        update.message.reply_text(
            f'Игра окончена!', reply_markup=reply_keyboard)


def second(update, context):
    global flag, total
    if flag == 4:
        flag += 1
        total += 1
        update.message.reply_text(
            "Верно!\nВокруг чего Дед Мороз, Снегурочка и дети водят хоровод?\n1) Вокруг елки.\n2) Вокруг пальмы."
            "\n3) Вокруг березы.\n4) Вокруг дуба.", reply_markup=markup_choice)
    elif flag == 6:
        flag += 1
        total += 1
        update.message.reply_text(
            "Верно!\nВ какой стране дети и взрослые находят новогодние подарки на подоконнике?\n1) В Польше.\n2) В "
            "Германии. "
            "\n3) В Америке.\n4) В Китае.", reply_markup=markup_choice)
    elif flag == 7:
        flag += 1
        total += 1
        update.message.reply_text(
            "Верно!\nСколько шуб у Деда Мороза?\n1) 1.\n2) 2"
            ""
            "\n3) 3.\n4) 4.", reply_markup=markup_choice)
    elif flag == 9:
        flag += 1
        total += 1
        update.message.reply_text(
            "Верно!\nЧто символизирует тройка лошадей?\n1) Любовь к троице.\n2) Счастье, радость и любовь."
            "\n3) Количество зимних праздников.\n4) Зимние месяца.", reply_markup=markup_choice)
    elif flag == 11:
        flag += 1
        total += 1
        update.message.reply_text(
            "Верно!\nПо указу какого царя датой празднования Нового года на Руси стало 1 января?\n1) Ивана "
            "Грозного.\n2) "
            "Александра I. 0"
            "\n3) Петра I.\n4) Александра II.", reply_markup=markup_choice)
    elif flag == 15:
        flag += 1
        total += 1
        update.message.reply_text(
            "Верно!\nВ каком городе получил прописку российский Дед Мороз?\n1) Новгород. "
            "\n2) "
            "Тула. 0"
            "\n3) Великий Устюг.\n4) Оренбург.", reply_markup=markup_choice)
    else:
        global user
        user = search_or_save_user(mdb, update.effective_user, total)
        if int(user["total"]) < total:
            user = save_user_info(mdb, user, update.effective_user, total)
        all_info = list(mdb.users.find({}))
        out_info1 = []
        out_info = []
        for i in all_info:
            out_info1.append((i["name"], int(i["total"])))
        out_info1 = sorted(out_info1, key=lambda x: x[1], reverse=True)
        k = 0
        for i in out_info1:
            k += 1
            out_info.append(f'{k}) {i[0]} {i[1]}')
        out_info = "\n".join(out_info)
        print(list(all_info))
        update.message.reply_text(
            f'ТЫ не угадал!\n\n\nА теперь рекорды! \n{out_info}')
        update.message.reply_text(
            f'Игра окончена!', reply_markup=reply_keyboard)


def third(update, context):
    global flag, total
    if flag == 2:
        flag += 1
        total += 1
        update.message.reply_text(
            "Верно!\nЧто спрятано в мешке у Деда Мороза?\n1) Гранаты.\n2) Фрукты."
            "\n3) Спорт инвентарь.\n4) Подарки.", reply_markup=markup_choice)
    elif flag == 8:
        flag += 1
        total += 1
        update.message.reply_text(
            "Верно!\nСколько лошадей запрягает в сани Дед Мороз?\n1) Двух.\n2) Трех."
            "\n3) Четырех.\n4) Семерых.", reply_markup=markup_choice)
    elif flag == 12:
        flag += 1
        total += 1
        update.message.reply_text(
            "Верно!\nВ какой стране в XVI веке появилась первая елочная игрушка?\n1) Саксония.\n2) Австралия."
            "\n3) Богемия.\n4) Германия.", reply_markup=markup_choice)
    elif flag == 16:
        flag += 1
        total += 1
        update.message.reply_text(
            "Верно!\nЧему равна «сумма» декабря, января и февраля? \n1) Лету. "
            "\n2) "
            "Весне. 0"
            "\n3) Осени.\n4) Зиме.", reply_markup=markup_choice)
    else:
        global user
        user = search_or_save_user(mdb, update.effective_user, total)
        if int(user["total"]) < total:
            user = save_user_info(mdb, user, update.effective_user, total)
        all_info = list(mdb.users.find({}))
        out_info1 = []
        out_info = []
        for i in all_info:
            out_info1.append((i["name"], int(i["total"])))
        out_info1 = sorted(out_info1, key=lambda x: x[1], reverse=True)
        k = 0
        for i in out_info1:
            k += 1
            out_info.append(f'{k}) {i[0]} {i[1]}')
        out_info = "\n".join(out_info)
        print(list(all_info))
        update.message.reply_text(
            f'ТЫ не угадал!\n\n\nА теперь рекорды! \n{out_info}')
        update.message.reply_text(
            f'Игра окончена!', reply_markup=reply_keyboard)


def fourth(update, context):
    global flag, total
    if flag == 3:
        flag += 1
        total += 1
        update.message.reply_text(
            "Верно!\nКак зовут внучку Деда Мороза?\n1) Дюймовочка.\n2) Снегурочка."
            "\n3) Несмеяна.\n4) Мария Васильевна.")
    elif flag == 10:
        flag += 1
        total += 1
        update.message.reply_text(
            "Верно!\nКак величали сурового предшественника современного русского Деда Мороза?\n1) Дед Колотун.\n2) "
            "Дед Трескун. "
            "\n3) Дед Вьюговей.\n4) Дед Иван.", reply_markup=markup_choice)
    elif flag == 17:
        flag += 1
        total += 1
        update.message.reply_text(
            "Верно!\nНазовёте «зимний» синоним глагола «поколотить»? \n1) Побить. "
            "\n2) "
            "Отмутузить."
            "\n3) Исколотить.\n4) Отметелить.", reply_markup=markup_choice)
    elif flag == 18:
        flag += 1
        total += 1
        update.message.reply_text(
            "Верно!\nКОНЕЦ \n1) Побить. "
            "\n2) "
            "Отмутузить."
            "\n3) Исколотить.\n4) Отметелить.", reply_markup=markup_choice)
    else:
        global user
        user = search_or_save_user(mdb, update.effective_user, total)
        if int(user["total"]) < total:
            user = save_user_info(mdb, user, update.effective_user, total)
        all_info = list(mdb.users.find({}))
        out_info1 = []
        out_info = []
        for i in all_info:
            out_info1.append((i["name"], int(i["total"])))
        out_info1 = sorted(out_info1, key=lambda x: x[1], reverse=True)
        k = 0
        for i in out_info1:
            k += 1
            out_info.append(f'{k}) {i[0]} {i[1]}')
        out_info = "\n".join(out_info)
        print(list(all_info))
        update.message.reply_text(
            f'ТЫ не угадал!\n\n\nА теперь рекорды! \n{out_info}', reply_markup=markup)
        update.message.reply_text(
            f'Игра окончена!', reply_markup=markup)


def time_untilNY(update, context):
    now = datetime.datetime.today()
    NY = datetime.datetime(int(now.year) + 1, 1, 1)
    d = NY - now
    mm, ss = divmod(d.seconds, 60)
    hh, mm = divmod(mm, 60)
    update.message.reply_text('До нового года: {} дней {} часа {} мин {} сек.'.format(d.days, hh, mm, ss))


def start(update, context):
    update.message.reply_text(
        "Я помощник деда мороза. Какая помощь вам нужна?",
        reply_markup=markup
    )


def close_keyboard(update, context):
    update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    updater.start_polling()
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("back", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("website", website))
    dp.add_handler(CommandHandler("time_untilNY", time_untilNY))
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(CommandHandler("contacts", contacts))
    dp.add_handler(CommandHandler("game_quiz", game_quiz))
    dp.add_handler(CommandHandler("add_functions", add_functions))
    dp.add_handler(CommandHandler("advice", get_advice))
    dp.add_handler(CommandHandler("download_game", download_game))
    dp.add_handler(CommandHandler("christmas_image", christmas_image))
    dp.add_handler(CommandHandler("christmas_music", christmas_music))
    dp.add_handler(CommandHandler("yes", yes))
    dp.add_handler(CommandHandler("no", start))
    dp.add_handler(CommandHandler("1", first))
    dp.add_handler(CommandHandler("2", second))
    dp.add_handler(CommandHandler("3", third))
    dp.add_handler(CommandHandler("4", fourth))
    dp.add_handler(CommandHandler("main_window", start))
    dp.add_handler(CommandHandler("close_keyboard", close_keyboard))
    updater.idle()


if __name__ == '__main__':
    main()
