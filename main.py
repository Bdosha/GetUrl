from aiogram import Bot, Dispatcher
from aiogram.filters import Text, Command
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)
import codecs

BOT_TOKEN: str = 'BOT_TOKEN'
f = codecs.open("check_chanel\\text.txt", "r", "utf-8")
main_text = f.read() 
f.close()
print(main_text)

bot: Bot = Bot(token=BOT_TOKEN)
dp: Dispatcher = Dispatcher()
admins = ['', '']
chanels = ['', '']

chan_1 =  InlineKeyboardButton(
    text='Канал',
    url=f'https://t.me/{chanels[0]}')


chan_2 =  InlineKeyboardButton(
    text='Канал',
    url=f'https://t.me/{chanels[1]}')

get_url = InlineKeyboardButton(
    text='Получить доступ',
    callback_data='get')

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[chan_1], 
                     [chan_2],
                     [get_url]])


@dp.message(Command(commands=['start']))
async def start_command(message: Message):
    print(message.from_user.username)
    await message.answer(text=main_text, 
                         reply_markup=keyboard)

@dp.callback_query(Text(text='get'))
async def get_but(callback: CallbackQuery):
    print(callback.from_user.username)
    for chanel in chanels:
        print(chanel)
        try:
            temp = await bot.get_chat_member(chat_id=f'@{chanel}', user_id=callback.from_user.id)
            print(temp.status)
            if temp.status == 'left':
                await callback.answer(text='Вы еще не подписались на все каналы')
                return 

        except:
            await callback.answer(text='Вы еще не подписались на все каналы')
            return
    await callback.message.edit_text(text=f'Вот ссылка на трансляцию! https://url.com')

@dp.message()
async def message(message: Message):  #
    if message.from_user.username in admins:
        global main_text
        main_text = message.text
        await message.answer(text='Текст успешно изменен')
        with codecs.open("check_chanel\\text.txt", "w", "utf-8-sig") as temp:
            temp.write(message.text)

if __name__ == '__main__':
    dp.run_polling(bot)  # Запуск бота