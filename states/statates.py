from aiogram.dispatcher.filters.state import StatesGroup, State


class StateMachine(StatesGroup):
    # Ввод Снилс
    Snls = State()

    # Ввод 1-5 данных
    VuzInfo = State()
    InstInfo = State()
    NapInfo = State()
    FormInfo = State()
    CatInfo = State()

    # Еще одно направление
    YesOrNo = State()

    # Главные кнопки
    Main = State()

    # Подписка
    Podpis = State()

    # Настройки Main Кнопки
    OptionsMainButtons = State()
    # Снилс
    SnlsOption = State()
    # Ожидание Команды Настроек Направления
    WaitNapCommand = State()
    # Ожидание Delete Номера Направления
    DeleteNapNum = State()