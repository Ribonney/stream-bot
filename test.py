import os
import time
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler
from telegram import ChatPermissions
from typing import Dict
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TOKEN')


user_commands_timestamps: Dict[str, float] = {}


def poslat(update, context):
    update.message.reply_text('Пошел нахуй')


def error(update, context):
    print(f'Update "{update}" caused error "{context.error}"')


def message_handler(update, context):
    entity_types = [e['type'] for e in update.message.entities]

    if 'bot_command' in entity_types:
        key = f'{update.message.from_user.id}/{update.message.chat_id}'

        # Ban user if last command from him was less than 10 sec ago
        try:
            if time.time() - user_commands_timestamps[key] < 10:
                # TODO mute user for 2 minutes
                context.bot.restrict_chat_member(
                    update.message.chat.id,
                    update.message.from_user.id,
                    ChatPermissions(can_send_messages=False),
                    until_date=time.time()+120,
                )

                # TODO send notification
                update.message.reply_text(f'Пользователь {update.message.from_user.full_name} вызывал команды ' +
                                          f'слишком часто и получил мьют на две минуты.')

        except KeyError:
            pass

        # Update map
        user_commands_timestamps[key] = update.message.date.timestamp()

    if update.message.text.lower() == 'похуй':
        update.message.reply_sticker('CAACAgIAAxkBAAEElGxeuYjT2-0WIJeyoG9N6RbEDm0bogACCAUAAlwohgh3VEpLUKZeRBkE')


def fallback_handler(update, context):
    print(update)


def main():
    updater = Updater(TOKEN, use_context=True)

    updater.bot.set_my_commands([('poslat', 'послать нахуй')])

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('poslat', poslat))
    dp.add_handler(MessageHandler(Filters.text, message_handler))
    # dp.add_handler()

    dp.add_error_handler(error)

    print('Starting polling')
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
