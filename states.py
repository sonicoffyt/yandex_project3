from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminPanel(StatesGroup):
    count_changing_days_after_changing_type = State()
    input_type_subscription = State()
    change_type_subscription = State()
    count_changing_days = State()
    change_days_subscription = State()
    summa_manual_replenishment = State()
    user_id_manual_replenishment = State()
    mailing_wait = State()
    ban = State()


class Deposit(StatesGroup):
    amount_CrystalPay = State()
    amount_Freekassa = State()


class UserPanel(StatesGroup):
    ask_question = State()
    generate_img = State()
    activation_promo = State()


class PromoCodes(StatesGroup):
    name = State()
    amount = State()
    count = State()
