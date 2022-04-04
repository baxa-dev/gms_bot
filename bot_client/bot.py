from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.markdown import hlink
from asgiref.sync import sync_to_async

from bot_client import keyboards, utils
from bot_admin.models import *

from bot_client.json_func import Data
from bot_admin.management.bot_creator import bot
from config.settings import CHANNEL_ID


# ------------------------------------- REGISTRATION OF USERS -------------------------------------------
# class Reg_User(StatesGroup):
#     name = State()
#     phone_number = State()
#     address = State()


# # Catching 1 response from client to reg: name
# # @dp.message_handler(content_types=['text'], state=Reg_User.name)
# async def reg_name(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         defaults = {'name': message.text}
#         await utils.create_or_update_user(user_id=message.chat.id, defaults=defaults)
#         await Reg_User.next()
#         query_number = await message.answer("Пожалуйста введите или отправьте свой номер телефона ☎️",
#                                             reply_markup=ReplyKeyboardMarkup
#                                             (row_width=1, resize_keyboard=True, one_time_keyboard=True).
#                                             add(KeyboardButton("Поделиться контактом 📞", request_contact=True)))
#         data['query_number'] = query_number.message_id
#
#
# # Catching 2 response from client to reg: phone_number
# # @dp.message_handler(content_types=['contact', 'text'], state=Reg_User.phone_number)
# async def reg_number(message: types.Message, state: FSMContext):
#     if "contact" in message:
#         defaults = {'number': message.contact.phone_number}
#         await utils.create_or_update_user(user_id=message.chat.id, defaults=defaults)
#     else:
#         defaults = {'number': message.text}
#         await utils.create_or_update_user(user_id=message.chat.id, defaults=defaults)
#     async with state.proxy() as data:
#         await bot.delete_message(chat_id=message.chat.id, message_id=data['query_number'])
#         del data['query_number']
#         query_location = await message.answer("Введите адрес или выберите регион  ⤵️ :",
#                                               reply_markup=keyboards.reg_place)
#         data['query_location'] = query_location.message_id
#     await Reg_User.next()
#
#
# # Catching 3 response from client to reg: location
# # @dp.message_handler(content_types=['text'], state=Reg_User.address)
# async def reg_location(message: types.Message, state: FSMContext):
#     # if "location" in message:
#     #     location = f"latitude: {message.location.latitude}\nlongitude: {message.location.longitude}"
#     #     defaults = {'location': location}
#     #     await functions.create_or_update_user(tg_id=message.chat.id, defaults=defaults)
#     #     async with state.proxy() as data:
#     #         await bot_client.delete_message(chat_id=message.chat.id, message_id=data['query_location'])
#     #         del data['query_location']
#     # else:
#     defaults = {'address': message.text}
#     await utils.create_or_update_user(user_id=message.chat.id, defaults=defaults)
#     async with state.proxy() as data:
#         await bot.delete_message(chat_id=message.chat.id, message_id=data['query_location'])
#         del data['query_location']
#     await state.finish()
#     await message.answer("Регистрация прошла успешно ! 🥳😃\nСпасибо, что уделили ваше время!")
#     await start_menu(message=message, state=state)


# ------------------------------------- REGISTRATION OF APPLICANTS -------------------------------------------
class Reg_Applicant(StatesGroup):
    name = State()
    phone = State()


# Catching 1 response from applicant to reg: name
# @dp.message_handler(content_types=['text'], state=Reg_Applicant.name)
async def applicant_name(message: types.Message, state: FSMContext):
    customer_name = message.text
    async with state.proxy() as data:
        apply_id = data['apply_id']
    await utils.change_apply_customer_name(apply_id=apply_id, customer_name=customer_name)
    await Reg_Applicant.next()

    query_number = await message.answer("Введите Ваш номер телефона ☎️ или отправьте  ⬇️",
                                        reply_markup=ReplyKeyboardMarkup
                                        (row_width=1, resize_keyboard=True, one_time_keyboard=True).
                                        add(KeyboardButton("Поделиться контактом 📞", request_contact=True)))
    async with state.proxy() as data:
        data['query_number'] = query_number.message_id


# Catching 2 response from applicant to reg: phone_number
# @dp.message_handler(content_types=['contact', 'text'], state=Reg_Applicant.phone)
async def applicant_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        apply_id = data['apply_id']
    if "contact" in message:
        customer_phone = message.contact.phone_number
    else:
        customer_phone = message.text

    async with state.proxy() as data:
        await bot.delete_message(chat_id=message.chat.id, message_id=data['query_number'])
        del data['query_number']

    await state.finish()
    await message.answer(text="Ваша заявка на данный товар принят ✅.\nВ скором времени 🕐 наши менеждеры с вами "
                              "свяжутся 📞 ! ")

    apply_details = await utils.change_apply_customer_phone(apply_id=apply_id, customer_phone=customer_phone)
    text = f"Поступил заказ от клиента :\n\nusername - {hlink('{}', 'https://t.me/{}').format(message.chat.username, message.chat.username)}" \
           f"\nИмя :  {apply_details[0]} \nНомер телефона :  {apply_details[1]}.\n\n" \
           f"Заявка на товар :\n{apply_details[2]}"

    await bot.send_message(chat_id=CHANNEL_ID, text=text)


# -------------------------------------- MAIN MENU --------------------------------------------------

# @dp.message_handler(commands=['start'])
async def start_menu(message: types.Message, state: FSMContext):
    await state.finish()
    chat_id = message.chat.id
    username = message.chat.username
    print(type(chat_id), chat_id)
    user = await utils.check_user(user_id=chat_id)
    if user:
        await keyboards.main_menu(message=message)
    else:
        print("Created new object in Client model")
        await sync_to_async(Customer.objects.create, thread_sensitive=True)(user_id=chat_id, username=username)
        await keyboards.main_menu(message=message)
        # await message.answer("Мы рады вас видеть вас в нашем боте ! 😊\n"
        #                      "Уделите немного времени для регистрации вашего аккаунта в боте!")
        # await Reg_User.name.set()
        # await message.answer("Введите своё имя  👤 :")


# --------------------------------- PRODUCT INFO FUNCTION -----------------------------------------------

async def product_info(callback):
    chat_id = callback.message.chat.id
    caption = ''
    product_name = callback.data
    product_path = f"product={product_name}/"
    data = await Data(user_id=chat_id, path=product_path)
    data.create_path()

    detail_list = await utils.get_category_products_detail(product_name=product_name)
    product_name = detail_list[1]
    photo = InputFile(detail_list[0])
    caption += f"<strong>{product_name}</strong>\n\n{detail_list[2]}\n\n{str(detail_list[3])} сум"
    about_product = InlineKeyboardMarkup(row_width=2)
    apply = InlineKeyboardButton("Оставить заявку  📤✅", callback_data=f"apply|{product_name}")
    prev = InlineKeyboardButton("Назад  ↩️", callback_data=f"prev")
    home = InlineKeyboardButton("Главное меню  🏠", callback_data="home")
    about_product.add(apply)
    about_product.row(prev)
    about_product.insert(home)
    await bot.send_photo(chat_id=chat_id, photo=photo, caption=caption, reply_markup=about_product)


# ------------------------------------ CALLBACK QUERY HANDLER ---------------------------------------------

# @dp.callback_query_handler(lambda callback: callback.data)
async def command_response(callback: types.CallbackQuery, state: FSMContext):
    categories_list = await utils.get_all_categories()
    subcategories_list = await utils.get_all_subcategories()
    products_list = await utils.get_all_products()
    chat_id = callback.message.chat.id

    if callback.data == "catalog":
        await callback.message.delete()
        await keyboards.categories(callback=callback)
        await callback.answer()

    elif callback.data in categories_list:
        await callback.message.delete()
        category_name = callback.data
        await keyboards.subcategories_or_category_products(callback=callback, category_name=category_name)
        await callback.answer()

    elif callback.data in subcategories_list:
        await callback.message.delete()
        subcategory_name = callback.data
        await keyboards.subcategory_products(callback=callback, subcategory_name=subcategory_name)
        await callback.answer()

    elif callback.data in products_list:
        await callback.message.delete()
        await product_info(callback=callback)
        await callback.answer()

    elif callback.data == "home":
        await callback.message.delete()
        await start_menu(message=callback.message, state=state)

    elif callback.data == "prev":
        await callback.message.delete()
        product_path = ""
        json_path = await Data(user_id=chat_id, path=product_path)
        path = json_path.get_path()
        print(type(path), "Current path : ", path)
        last_room = path.split(sep='/')[-2]
        prev_room = path.split(sep='/')[-3]
        print("Last room in path : ", last_room)
        print("Prev room in path : ", prev_room)

        if "product" in last_room:
            subcategory_name = prev_room.split(sep='=')[-1]
            print("subcategory name : ", subcategory_name)
            # await keyboards.category_products(callback=callback, category_name=category_name)
            await keyboards.subcategory_products(callback=callback, subcategory_name=subcategory_name)
            json_path.delete()
            await callback.answer()

        elif "subcategories" in last_room:
            category_name = prev_room.split(sep='=')[-1]
            print("category name : ", category_name)
            await keyboards.subcategories_or_category_products(callback=callback, category_name=category_name)
            json_path.delete()
            await callback.answer()

        elif "categories" in last_room:
            await keyboards.categories(callback=callback)
            json_path.delete()
            await callback.answer()

    elif callback.data.split(sep='|')[0] == "apply":
        customer_name = ""
        customer_phone = ""
        product_name = callback.data.split(sep='|')[1]
        async with state.proxy() as data:
            data['product_name'] = callback.data.split(sep='|')[1]
            data['apply_id'] = await utils.create_apply(user_id=chat_id, customer_name=customer_name,
                                                        customer_phone=customer_phone, product_name=product_name)

        await bot.send_message(chat_id=chat_id, text="Пожалуйста, оставьте свои контакты !")
        await Reg_Applicant.name.set()
        await bot.send_message(chat_id=chat_id, text="Ваше имя  👤 :")
        await callback.answer()

    elif callback.data == "about_us":
        await callback.message.delete()
        text_about = await utils.get_about_us()
        text = ""
        for about in text_about:
            text += about
        await bot.send_message(chat_id=chat_id, text=text, reply_markup=InlineKeyboardMarkup(row_width=1).
                               insert(InlineKeyboardButton("Главное меню  🏠", callback_data="home")))
        await callback.answer()

    elif callback.data == "contacts":
        await callback.message.delete()
        text_contacts = await utils.get_contacts()
        text_address = "<strong>Адреса :</strong>"
        text_number = "\n\n<strong>Номера телефонов :</strong>"
        text_location = "\n\n<strong>Локации адресов :</strong>"
        for i in range(len(text_contacts)):
            if i == 0 or i % 3 == 0:
                text_address += f"\n{text_contacts[i]}"
            elif i == 1 or i % 4 == 0:
                text_number += f"\n{text_contacts[i]}"
            elif i == 2 or i % 5 == 0:
                text_location += f"\n{text_contacts[i]}"

        # text = f"<strong>Адреса :</strong>\n" \
        #        f"{text_contacts[0]}\n\n" \
        #        f"<strong>Номера телефонов :</strong>\n" \
        #        f"{text_contacts[1]}\n\n" \
        #        f"<strong>Локации адресов :</strong>\n" \
        #        f"{text_contacts[2]}"
        text = text_address + text_number + text_location

        await bot.send_message(chat_id=chat_id, text=text, reply_markup=InlineKeyboardMarkup(row_width=1).
                               insert(InlineKeyboardButton("Главное меню  🏠", callback_data="home")))
        await callback.answer()


# ------------------------------------------ REGISTRATION ALL HANDLERS ---------------------------------------------

def register_client_message_handlers(dp: Dispatcher):
    dp.register_message_handler(start_menu, commands=['start'], state=None)
    # dp.register_message_handler(reg_name, content_types=['text'], state=Reg_User.name)
    # dp.register_message_handler(reg_number, content_types=['contact', 'text'], state=Reg_User.phone_number)
    # dp.register_message_handler(reg_location, content_types=['text'], state=Reg_User.address)
    dp.register_message_handler(applicant_name, content_types=['text'], state=Reg_Applicant.name)
    dp.register_message_handler(applicant_number, content_types=['contact', 'text'], state=Reg_Applicant.phone)


def register_client_callback_query_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(command_response, lambda callback: callback.data)
