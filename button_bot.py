from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu():
    menu = InlineKeyboardMarkup(row_width=1)
    menu1 = InlineKeyboardButton(text='Добавить заметку', callback_data='id_new_note')
    menu2 = InlineKeyboardButton(text='Добавить напоминалку', callback_data='id_new_reminder')
    menu3 = InlineKeyboardButton(text='Все заметки', callback_data='id_all_note')
    menu4 = InlineKeyboardButton(text='Все напоминалки', callback_data='id_all_reminder')
    return menu.add(menu1, menu2, menu3, menu4)


def menu_back():
    menu = InlineKeyboardMarkup(row_width=1)
    menu1 = InlineKeyboardButton(text='Удалить напоминалку', callback_data='id_del_rem')
    menu2 = InlineKeyboardButton(text='<<', callback_data='id_back')
    return menu.add(menu1, menu2)


def menu_back1():
    menu = InlineKeyboardMarkup(row_width=1)
    menu1 = InlineKeyboardButton(text='Удалить заметку', callback_data='id_del_note')
    menu2 = InlineKeyboardButton(text='<<', callback_data='id_back')
    return menu.add(menu1, menu2)


def menu_cancell():
    menu = InlineKeyboardMarkup(row_width=1)
    menu1 = InlineKeyboardButton(text='Отменить ввод', callback_data='id_cancell')
    return menu.add(menu1)