from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters import Text
from collect_data import *
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
import json
from time import sleep

# инициализация бота

TOKEN = '6311363880:AAEEPaz_rag9gHNMUJz-prSzUW-euccrKmk'
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

start_buttons = ['Получить новые задания', 'Интересные задания', 'Очистить интересные задания']
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(*start_buttons)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await bot.send_message(message.chat.id, 'Добро пожаловать. Этот бот отслеживает задания с сайта https://client.work-zilla.com/freelancer', reply_markup=keyboard)

@dp.message_handler(Text(equals='Получить новые задания'))
async def get_new_tasks(message:types.Message):
    check_tasks()

    with open('data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    results = []

    for i in data.get('data').get('other')[:10]:
        result = f'{i.get("description")}\n\n<b>Цена - {int(i.get("price"))}р.\nЦена с комиссией - {i.get("freelancerEarn")}р.</b>\n\nhttps://client.work-zilla.com/freelancer'
        results.append(result)

    for i in data.get('data').get('interesting'):
        result = f'{i.get("description")}\n\n<b>Цена - {int(i.get("price"))}р.\nЦена с комиссией - {i.get("freelancerEarn")}р.</b>\n\nhttps://client.work-zilla.com/freelancer'
        results.append(result)

    await bot.send_message(message.chat.id, 'Подождите, загрузка...', reply_markup=keyboard)

    for result in results:
        await bot.send_message(message.chat.id, result, reply_markup=keyboard)

@dp.message_handler(Text(equals='Интересные задания'))
async def get_intresting_tasks(message:types.Message):
    check_intresting()

    with open('intresting.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    for numeric, i in enumerate(data[::-1]):
        result = f'{i.get("name")}\n\n<b>Цена - {int(i.get("price"))}\nЦена с комиссией {i.get("freelancerEarn")}</b>\nhttps://client.work-zilla.com/freelancer'
        await bot.send_message(message.chat.id, result, reply_markup=keyboard)
        if numeric % 10 == 0:
            sleep(3)

    if len(data) == 0:
        await bot.send_message(message.chat.id, 'Интересных заданий пока что нет', reply_markup=keyboard)

@dp.message_handler(Text(equals='Очистить интересные задания'))
async def clear_intrestring(message:types.Message):
    with open('intresting.json', 'w', encoding='utf-8') as file:
        json.dump([], file, indent=4, ensure_ascii=False)

    await bot.send_message(message.chat.id, 'Очистка завершена.')

async def send_message_intresting(bot:Bot):
    if check_intresting():
        await bot.send_message(794764771, 'Появились новые инетерсные задания')

def main():
    executor.start_polling(dp)

update_intrestring = AsyncIOScheduler(timezone="Europe/Moscow")
update_intrestring.add_job(send_message_intresting, trigger='interval', seconds=30,
                  kwargs={'bot' : bot})
update_intrestring.start()

update_all_tasks = AsyncIOScheduler(timezone="Europe/Moscow")
update_all_tasks.add_job(check_tasks, trigger='interval', minutes=5)
update_all_tasks.start()

if __name__ == '__main__':
    main()
