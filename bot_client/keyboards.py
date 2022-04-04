from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from bot_client import utils
from bot_admin.management.bot_creator import bot


# REGISTRATION PLACE OF CLIENT
from bot_client.json_func import Data

reg_place = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
tashkent = KeyboardButton("Город Ташкент")
andijan = KeyboardButton("Андижанская область")
buxara = KeyboardButton("Бухарская область")
fergana = KeyboardButton("Ферганская область")
djizak = KeyboardButton("Джизакская область")
khorezm = KeyboardButton("Хорезмская область")
namangan = KeyboardButton("Наманганская область")
navoiy = KeyboardButton("Навоийская область")
kashkadarya = KeyboardButton("Кашкадарьинская область")
samarkand = KeyboardButton("Самаркандская область")
sirdarya = KeyboardButton("Сырдарьинская область")
surxandarya = KeyboardButton("Сурхандарьинская область")
tashkent_region = KeyboardButton("Ташкентскаяская область")
karakalpakstan = KeyboardButton("Республика Каракалпакстан")
reg_place.row(tashkent)
reg_place.add(andijan, buxara, fergana, djizak, khorezm, namangan, navoiy, kashkadarya, samarkand, sirdarya, surxandarya, tashkent_region)
reg_place.row(karakalpakstan)


# START (MAIN) MENU
async def main_menu(message):
    text = f"Здравствуйте, <strong>{message.chat.first_name}</strong> 👋.\nДобро пожаловать в наш бот."
    keyboards = InlineKeyboardMarkup(row_width=2)
    catalog = InlineKeyboardButton("Продукция  📔🔎", callback_data="catalog")
    about_us = InlineKeyboardButton("О нас  👤", callback_data="about_us")
    contacts = InlineKeyboardButton("Контакты  ☎️📍", callback_data="contacts")
    keyboards.row(catalog)
    keyboards.add(about_us, contacts)
    await message.answer(text, reply_markup=keyboards)


# SHOWING CATEGORIES
async def categories(callback):
    chat_id = callback.message.chat.id
    if callback.data != "prev":
        product_path = "catalog/"
        print("Showed catalog")
        data = await Data(user_id=chat_id, path=product_path)
        data.create_path()
    text = "Выберите :"
    category_buttons = InlineKeyboardMarkup(row_width=2)
    categories_list = await utils.get_all_categories()
    for category in categories_list:
        button = InlineKeyboardButton(category, callback_data=category)  # /category/
        category_buttons.insert(button)
    prev = InlineKeyboardButton("Назад  ↩️", callback_data="home")
    home = InlineKeyboardButton("Главное меню  🏠", callback_data="home")
    category_buttons.row(prev)
    category_buttons.insert(home)
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=category_buttons)


# # SHOWING SUB-CATEGORIES AND PRODUCTS
# async def category_products(callback, category_name):
#     chat_id = callback.message.chat.id
#     if callback.data != "prev":
#         product_path = f"category={category_name}/"
#         data = await Data(user_id=chat_id, path=product_path)
#         data.create_path()
#     text = "Выберите :"
#     product_buttons = InlineKeyboardMarkup(row_width=2)
#     product_list = await utils.get_category_products_names(category_name=category_name)
#     for product in product_list:
#         button = InlineKeyboardButton(product, callback_data=product)
#         product_buttons.insert(button)
#     prev = InlineKeyboardButton("Назад  ↩️", callback_data=f"prev")
#     home = InlineKeyboardButton("Главное меню  🏠", callback_data="home")
#     product_buttons.row(prev)
#     product_buttons.insert(home)
#     await bot.send_message(chat_id=chat_id, text=text, reply_markup=product_buttons)


# SHOWING SUB-CATEGORIES AND PRODUCTS
async def subcategories_or_category_products(callback, category_name):
    chat_id = callback.message.chat.id
    if callback.data != "prev":
        # product_path = "subcategories/"
        product_path = f"categories={category_name}/"
        print("Showed catalog")
        data = await Data(user_id=chat_id, path=product_path)
        data.create_path()
    text = "Выберите :"
    subcategory_and_product_buttons = InlineKeyboardMarkup(row_width=3)
    subcategories_list = await utils.get_need_subcategories(callback=category_name)
    product_list = await utils.get_category_products(callback=category_name)
    for subcategory in subcategories_list:
        button = InlineKeyboardButton(subcategory, callback_data=subcategory)
        subcategory_and_product_buttons.insert(button)
    for product in product_list:
        button = InlineKeyboardButton(product, callback_data=product)
        subcategory_and_product_buttons.insert(button)
    prev = InlineKeyboardButton("Назад  ↩️", callback_data=f"prev")
    home = InlineKeyboardButton("Главное меню  🏠", callback_data="home")
    subcategory_and_product_buttons.row(prev)
    subcategory_and_product_buttons.insert(home)
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=subcategory_and_product_buttons)


async def subcategory_products(callback, subcategory_name):
    chat_id = callback.message.chat.id
    if callback.data != "prev":
        product_path = f"subcategories={subcategory_name}/"
        data = await Data(user_id=chat_id, path=product_path)
        data.create_path()
    text = "Выберите :"
    product_buttons = InlineKeyboardMarkup(row_width=3)
    product_list = await utils.get_subcategory_products(callback=subcategory_name)
    for product in product_list:
        button = InlineKeyboardButton(product, callback_data=product)
        product_buttons.insert(button)
    prev = InlineKeyboardButton("Назад  ↩️", callback_data=f"prev")
    home = InlineKeyboardButton("Главное меню  🏠", callback_data="home")
    product_buttons.row(prev)
    product_buttons.insert(home)
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=product_buttons)
