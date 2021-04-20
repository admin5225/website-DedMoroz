import datetime
import random

from tok import TOKEN
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove

due = 0
reply_keyboard = [['/info'],
                  ['/website'],
                  ['/game_quiz']]
communication = [['/contacts'], ['/back']]
main_answer = [['/yes'], ['/no']]
reply_close_timer = [['/close']]
choicer = [['/1'], ['/2'], ['/3'], ['/4'], ['/main_window']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
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
    """Выводит сообщение"""
    job = context.job
    context.bot.send_message(job.context, text=f'Истекло {due} секунд!', reply_markup=markup3)


def unset_timer(update, context):
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Хорошо, таймер сброшен!' if job_removed else 'Нет активного таймера.'
    update.message.reply_text(text, reply_markup=markup3)


def info(update, context):
    update.message.reply_text('ИГРА ГОДА 2021!', reply_markup=markup2)


def website(update, context):
    update.message.reply_text('https://slavina-flask-proga.herokuapp.com/', reply_markup=markup)


def contacts(update, context):
    update.message.reply_text(
        f"@slaav1k")


def game_quiz(update, context):
    update.message.reply_text(
        f"Хочешь сыграть в викторину?", reply_markup=markup3)


def yes(update, context):
    update.message.reply_text(
        f"Тогда мы НАЧНАЕМ!\nГде живет дед мороз?\n1) На северном полюсе.\n2) На южном полюсе.\n 3) В Крыму!\n4) В "
        f"Солотче!", reply_markup=markup_choice)


def help(update, context):
    update.message.reply_text(
        "Я пока не умею помогать... Я только ваше эхо.")


def no(update, context):
    update.message.reply_text("Телефон: +7(495)776-3030")


def site(update, context):
    update.message.reply_text(
        "Сайт: http://www.yandex.ru/company")


def time(update, context):
    today = datetime.datetime.today()
    update.message.reply_text(
        today.strftime("%H:%M:%S"))


def date(update, context):
    today = datetime.datetime.today()
    update.message.reply_text(
        today.strftime("%m/%d/%Y"))


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
    dp.add_handler(CommandHandler("yes", yes))
    dp.add_handler(CommandHandler("no", start))
    dp.add_handler(CommandHandler("site", site))
    dp.add_handler(CommandHandler("close", unset_timer))
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
