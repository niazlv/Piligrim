from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

YesOrNoMenu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Да✅"),
            KeyboardButton(text="Нет❌"),
        ],
    ],
    resize_keyboard=True
)

MainMenu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Получить данные📘"),
        ],
        [
            KeyboardButton(text="Подписка📥"),
        ],
        [
            KeyboardButton(text="Настройки🌀"),
        ],
    ],
    resize_keyboard=True
)

OptionsMenu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="ID Абитуриента/СНИЛС🔹"),
        ],
        [
            KeyboardButton(text="Направления📘"),
        ],
        [
            KeyboardButton(text="Отменить◀️"),
        ],
    ],
    resize_keyboard=True
)

NapOptionsMenu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить✅"),
        ],
        [
            KeyboardButton(text="Удалить❌"),
        ],
        [
            KeyboardButton(text="Отменить◀️"),
        ],
    ],
    resize_keyboard=True
)
