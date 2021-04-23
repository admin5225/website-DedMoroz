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
import pprint
from mongodb import mdb, search_or_save_user, save_user_info

tb = telebot.TeleBot(TOKEN)
due = 0
flag = 0
total = 0
reply_keyboard = [['/info'],
                  ['/website'],
                  ['/game_quiz'], ['/add_functions']]
communication = [['/contacts'], ['/download_game'], ['/back']]
main_answer = [['/yes'], ['/no']]
addFunction = [['/christmas_image'], ['/christmas_music'], ['/advice'], ['/back']]
reply_close_timer = [['/close']]
choicer = [['/1'], ['/2'], ['/3'], ['/4'], ['/main_window']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
markupFUNC = ReplyKeyboardMarkup(addFunction, one_time_keyboard=False)
markup_choice = ReplyKeyboardMarkup(choicer, one_time_keyboard=False)
markup2 = ReplyKeyboardMarkup(communication, one_time_keyboard=False)
markup3 = ReplyKeyboardMarkup(main_answer, one_time_keyboard=False)
markup4 = ReplyKeyboardMarkup(reply_close_timer, one_time_keyboard=False)


def remove_job_if_exists(name, context):
    """Удаляем задачу по имени.
    Возвращаем True если задача была успешно удалена."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


# Обычный обработчик, как и те, которыми мы пользовались раньше.
def set_timer(update, context):
    chat_id = update.message.chat_id
    try:
        # args[0] должен содержать значение аргумента
        # (секунды таймера)
        global due
        due = int(context.args[0])
        if due < 0:
            update.message.reply_text(
                'Извините, не умеем возвращаться в прошлое')
            return

        # Добавляем задачу в очередь
        # и останавливаем предыдущую (если она была)
        job_removed = remove_job_if_exists(
            str(chat_id),
            context
        )
        context.job_queue.run_once(
            task,
            due,
            context=chat_id,
            name=str(chat_id)
        )
        text = f'Засек {due} секунд!'
        if job_removed:
            text += ' Старая задача удалена.'
        # Присылаем сообщение о том, что всё получилось.
        update.message.reply_text(text, reply_markup=markup4)

    except (IndexError, ValueError):
        update.message.reply_text('Использование: /set_time <секунд>')


def task(context):
    global due
    job = context.job
    context.bot.send_message(job.context, text=f'Истекло {due} секунд!', reply_markup=markup3)


def unset_timer(update, context):
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Хорошо, таймер сброшен!' if job_removed else 'Нет активного таймера.'
    update.message.reply_text(text, reply_markup=markup3)


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
    update.message.reply_text('1)Рандомная фотография с Рождеством!\n2)Рандомный совет на день!',
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
    flag = 1
    update.message.reply_text(
        f"Тогда мы НАЧНАЕМ!\nГде живет дед мороз?\n1) На северном полюсе.\n2) На южном полюсе.\n3) В Крыму!\n4) В "
        f"Солотче!", reply_markup=markup_choice)


def help(update, context):
    update.message.reply_text(
        "Я пока не умею помогать... Я только ваше эхо.")


def no(update, context):
    update.message.reply_text("Телефон: +7(495)776-3030")


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
        update.message.reply_text(
            f"ТЫ не угадал! {total}")


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
            "Верно!\nВ Сколько шуб у Деда Мороза?\n1) 1.\n2) 2"
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
        update.message.reply_text(
            f"ТЫ не угадал! {total}")


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
    else:
        update.message.reply_text(
            f"ТЫ не угадал! {total}")


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
    else:
        update.message.reply_text(
            f"ТЫ не угадал! {total}")


def time(update, context):
    today = datetime.datetime.today()
    update.message.reply_text(
        today.strftime("%H:%M:%S"))


def date(update, context):
    today = datetime.datetime.today()
    update.message.reply_text(
        today.strftime("%m/%d/%Y"))


def start(update, context):
    user = search_or_save_user(mdb, update.effective_user, total)
    print(user)
    print(update.effective_user)
    all_info = list(mdb.users.find({"total": 0}))
    print(list(all_info))
    for i in all_info:
        print(i["name"])
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

    # Получаем из него диспетчер сообщений.
    dp = updater.dispatcher

    updater.start_polling()
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("back", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("website", website))
    dp.add_handler(CommandHandler("date", date))
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
    dp.add_handler(CommandHandler("set_time", set_timer,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("unset", unset_timer,
                                  pass_chat_data=True))

    # Ждём завершения приложения.
    # (например, получения сигнала SIG_TERM при нажатии клавиш Ctrl+C)
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
