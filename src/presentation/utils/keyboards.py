from aiogram import Bot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import BotCommand


exit_filling_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отмена')]],
                                            resize_keyboard=True,
                                            one_time_keyboard=True)


menu_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Сыграть в игру'),
                                               KeyboardButton(text='Изменить профиль'),
                                               KeyboardButton(text='Рейтинг')]],
                                    resize_keyboard=True,
                                    one_time_keyboard=False)


async def set_command(bot: Bot) -> None:
    commands = [BotCommand(command='menu',  description='главное меню'),
                BotCommand(command='game',  description='сыграть в игру'),
                BotCommand(command='rating', description='показать общий рейтинг'),
                BotCommand(command='set_profile', description='обновить данные профиля'),
                BotCommand(command='info',  description='справочная информация')]
    await bot.set_my_commands(commands)


tap_button = InlineKeyboardBuilder()
tap_button.button(text='Жми!',
                  callback_data='tap')
