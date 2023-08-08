from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from button_bot import *
from note_sqlite import *
from datetime import *
import asyncio

TOKEN = '6567856903:AAFRoHGcFth19gDMixoWCnPybEefjG2WQvE'

bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def on_startup(_):
    await db_connect()


class NoteAnswer(StatesGroup):
    waiting_for_answer = State()
    waiting_del_answer = State()


class RemiderAnswer(StatesGroup):
    waiting_for_answer = State()
    waiting_for_time = State()
    waiting_for_date = State()
    waiting_del_answer = State()


@dp.message_handler(commands=['start'])
async def cmd_start(message):
    await message.delete()
    await message.answer('Бот запущен',
                         reply_markup=main_menu())


@dp.callback_query_handler(text='id_all_reminder')
async def cmd_all_reminder(call):
    res = await get_reminder()
    await call.message.delete()
    await call.message.answer(text=res,
                              reply_markup=menu_back())


@dp.callback_query_handler(text='id_all_note')
async def cmd_all_note(call):
    res = await get_note()
    await call.message.delete()
    await call.message.answer(text=res,
                              reply_markup=menu_back1())


@dp.callback_query_handler(text='id_back')
async def cmd_back(call):
    await call.message.delete()
    await call.message.answer(text="Главное меню",
                              reply_markup=main_menu())
    while True:
        await asyncio.sleep(1)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_date = now.strftime('%m-%d')
        list_time = await get_remider_time()

        if current_time == '00:00:00' and current_date in list_time:
            for i in list_time:
                if current_date == i[4]:
                    await cmd_changes_bool(1, i[0])

        for item in list_time:
            if current_time in item and item[4] == 1:
                await call.message.delete()
                await call.message.answer(text=f'Напоминаю - {item[1]}',
                                          reply_markup=main_menu())
                await cmd_changes_bool(0, item[0])


@dp.callback_query_handler(text='id_new_note')
async def cmd_new_note(call):
    await call.message.delete()
    await call.message.answer('Введите текст заметки',
                              reply_markup=menu_cancell())
    await NoteAnswer.waiting_for_answer.set()


@dp.message_handler(content_types=['text'], state=NoteAnswer.waiting_for_answer)
async def finish_state(message, state):
    await add_note(message.text)
    await message.delete()
    await message.answer(text='Заметка добавлена',
                         reply_markup=menu_back1())
    await state.finish()


@dp.callback_query_handler(text='id_del_note')
async def cmd_del_note(call):
    await call.message.delete()
    await call.message.answer(text='введите номер заметки, которую хотите удалить')
    res = await get_note()
    await call.message.answer(text=res,
                              reply_markup=menu_cancell())

    await NoteAnswer.waiting_del_answer.set()


@dp.message_handler(content_types=['text'], state=NoteAnswer.waiting_del_answer)
async def handler_del_note(message, state):
    await del_note(message.text)
    await state.finish()
    await message.delete()
    await message.answer(text='Ваша заметка удалена', 
                         reply_markup=menu_back1())


@dp.callback_query_handler(text='id_new_reminder')
async def cmd_new_reminder(call):
    global reminder

    reminder = []

    await call.message.delete()
    await call.message.answer(text='Введите текст напоминалки',
                              reply_markup=menu_cancell())
    await RemiderAnswer.waiting_for_answer.set()


@dp.message_handler(content_types=['text'], state=RemiderAnswer.waiting_for_answer)
async def cmd_new_reminder1(message):
    reminder.append(message.text)
    await message.delete()
    await message.answer(text='Теперь укажите время в фомате HH:MM:SS',
                         reply_markup=menu_cancell())

    await RemiderAnswer.next()


@dp.message_handler(content_types=['text'], state=RemiderAnswer.waiting_for_time)
async def cmd_reminder_add_date(message):
    reminder.append(message.text)
    message.delete()
    await message.answer(text='Теперь укажите дату в формате MM-DD',
                         reply_markup=menu_cancell())
    
    await RemiderAnswer.next()


@dp.message_handler(content_types=['text'], state=RemiderAnswer.waiting_for_date)
async def cmd_new_reminder_finish(message, state):
    reminder.append(message.text)
    await add_reminder(reminder[0], reminder[1], reminder[2])
    await state.finish()
    reminder.clear()
    await message.delete()
    await message.answer(text='Напоминлка добавлена',
                         reply_markup=menu_back())


@dp.callback_query_handler(text='id_del_rem')
async def cmd_del_rem(call):
    await call.message.delete()
    await call.message.answer(text='Введите номер напоминалки')
    reminder = await get_reminder()
    await call.message.answer(text=reminder,
                              reply_markup=menu_cancell())

    await RemiderAnswer.waiting_del_answer.set()


@dp.message_handler(content_types=['text'], state=RemiderAnswer.waiting_del_answer)
async def cmd_del_rem1(message, state):
    await cmd_del_reminder(message.text)
    await state.finish()
    await message.delete()
    await message.answer(text='Ваша напоминалка удалена',
                         reply_markup=menu_back())


#@dp.callback_query_handler(text='id_cancell')
#async def cmd_cancell(call, state):
#    await state.finish()
#    await call.message.answer(text='ВВод прерван',
#                              reply_markup=main_menu())


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp,
                           skip_updates=True,
                           on_startup=on_startup)
