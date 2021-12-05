# -*- coding: utf-8 -*-

from os import replace
import config
import interface

import logging
import re


from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text

logging.basicConfig(level=logging.INFO)

bot = Bot(token = config.API_TOKEN)
dp = Dispatcher(bot)

# for redirecting user to add self place
CHECKPLACE_LINK = "https://checkplace.net/"

# Place to read images
IMAGE_DIRECTORY = "/var/www/www-root/data/www/checkplace.net/gallery/"

# auth process of user
@dp.message_handler(commands=['start'])
async def registration_process(message: types.Message):
    is_register = config.UserDatabaseConfig(message.from_user.id, '', 0).is_registered()
    if not is_register:
        markup = types.ReplyKeyboardRemove(selective=False)
        await message.answer("Привет, {}! Для того, чтобы пройти регистрацию, пожалуйста введите свою дату рождения в формате дд.мм.гггг:".format(message.from_user.first_name), reply_markup=markup)
    else:
        await message.answer("Привет, {}!".format(message.from_user.first_name), reply_markup=interface.main_menu())



# check for auth user
@dp.message_handler(regexp=r"(\d\d.\d\d.\d\d\d\d)")
async def check_date_of_birth(message: types.Message):
    date = str(re.search(r'(\d\d.\d\d.\d\d\d\d)', str(message.text)).group(0))
    is_register = config.UserDatabaseConfig(message.from_user.id, message.from_user.first_name, 0).is_registered()
    if not is_register:
        reg_user = config.UserDatabaseConfig(message.from_user.id, message.from_user.first_name, date).user_register()
        if reg_user:
            await message.answer("Поздравляем! Вы успешно зарегистрировались 😁", reply_markup=interface.main_menu())
        else:
            await message.answer("У нас возникли кое-какие проблемы, пожалуйста обратитесь в поддержку!")
    else:
        await message.answer("Куда отправляемся? 😊", reply_markup=interface.main_menu())



@dp.message_handler(regexp=r"(⭐️\sДобавить\sместо)")
async def show_info_by_adding_place(message: types.Message):
    is_register = config.UserDatabaseConfig(message.from_user.id, '', 0).is_registered()
    if not is_register:
        markup = types.ReplyKeyboardRemove(selective=False)
        await message.answer("Привет, {}! Вы еще не зарегистрированы 😔 Для того, чтобы пройти регистрацию, пожалуйста введите свою дату рождения в формате дд-мм-гггг:".format(message.from_user.first_name), reply_markup=markup)
    else:
        hours_passed = config.UserDatabaseConfig(int(message.from_user.id), '', 0).check_hours()
        message_info = """Учавствуйте в нашем развитие, открывайте новые места с CheckPlace!\n\nПривет, путешественник 😊 Если ты знаешь интересное место, о котором хочешь поделится с нами, то мы будем очень рады узнать об этом.\n\nПравила такие:\n1. Ты можешь присылать нам свое место только один раз за сутки.\n2. Для того, чтобы послать нам описание твоего места, ты должен перейти к нам на страницу и заполнить форму.\n3. После того, как твое место будет одобрено администрацией, ты сможешь увидеть это в разделе \"❤️ Мои места\" и также найти это место в основном списке.\n\nСпасибо, что учавствуете в развитии CheckPlace! 🤩"""
        if hours_passed >= 24:
            await message.answer(message_info, reply_markup=interface.generate_our_website(CHECKPLACE_LINK + f"?id={message.from_user.id}"))
        else:
            await message.answer(message_info)
            await message.answer(f"Для отправки заявки осталось {24 - hours_passed} час/а. Пожалуйста, ожидайте.")



@dp.message_handler(regexp=r"(❤️\sМои\sместа)")
async def show_global_places(message: types.Message):
    is_register = config.UserDatabaseConfig(message.from_user.id, '', 0).is_registered()
    if not is_register:
        markup = types.ReplyKeyboardRemove(selective=False)
        await message.answer("Привет, {}! Вы еще не зарегистрированы 😔 Для того, чтобы пройти регистрацию, пожалуйста введите свою дату рождения в формате дд-мм-гггг:".format(message.from_user.first_name), reply_markup=markup)
    else:
        data = config.UserPlaces(int(message.from_user.id)).show_user_places()
        if not data:
            await message.answer("Список ваших мест пуст.")
        else:
            await message.answer("Ваши места:")
            output_text = ""
            status = ['🕓 Проверяется', '✅ Опубликовано']
            for i in range(len(data)):
                if int(data[i][1]) != 0:
                    output_text += f"{i + 1}. {status[1]} | {data[i][0]}\n\n"
                else:
                    output_text += f"{i + 1}. {status[0]} | {data[i][0]}\n\n"
            await message.answer(output_text)




@dp.message_handler(regexp=r"(🌚\sВыбрать\sместо)")
async def show_global_places(message: types.Message):
    categories = config.Checkplace().show_categories()
    if not categories:
        await message.answer('Категории не были найдены, пожалуйста обратитесь в поддержку.')
    else:
        await message.answer('Выберите категорию:', reply_markup=interface.show_categories(categories))
    


@dp.message_handler(regexp=r"(🌚\s\d+.\s\w+)")
async def open_places_list(message: types.Message):
    
    category_id = int(re.search(r'\d+', str(message.text)).group(0))
    preview_list = config.Checkplace().show_posts_preview_list(category_id)
    output = ""
    if not preview_list:
        await message.answer('Места под данную категорию не найдены.', reply_markup=interface.main_menu())
    else:
        await message.answer("Выберите место:", reply_markup=interface.main_menu())
        for i in range(len(preview_list)):
            output += "{}. {}\n".format((i + 1), preview_list[i][1])
        
        await message.answer(output, reply_markup=interface.show_places_list_keyboard(preview_list))



@dp.callback_query_handler(Text(startswith="post_id_"))
async def callbacks_post_list(call: types.CallbackQuery):
    action = call.data.split("_")[2]
    if action == 'cancel':
        await call.message.delete_reply_markup()
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    else:
        output_text = ""
        post_data = config.Checkplace().show_post(int(action))
        if post_data:
            output_text = f"*Название:* {post_data[0][1]}\n*Описание:* {post_data[0][2]}\n*Время работы:* {post_data[0][3]}\n*Особенности:* {post_data[0][4]}\n*Ориентиры:* {post_data[0][5]}\n"
        else:
            output_text = "Что-то пошло не так, попробуйте позже."

        try:
            img = open(f"{IMAGE_DIRECTORY}{post_data[0][6]}", "rb")
            print(img)
        except:
            await call.message.answer(output_text, parse_mode='Markdown', reply_markup=interface.generate_link_markup(post_data[0][7]))
        else:
            await bot.send_photo(chat_id=call.from_user.id, photo=img, caption=output_text, parse_mode='Markdown', reply_markup=interface.generate_link_markup(post_data[0][7]))
            img.close()
    
    await call.answer()



@dp.message_handler(regexp=r"(🧑‍💻\sПоддержка)")
async def support(message: types.Message):
    await message.answer("Пишите по всем вопросам нам:\n@Neputat_sosnovoy или @Misterioy.", reply_markup=interface.main_menu())



@dp.message_handler(regexp=r"(⬅️\sНазад)")
async def cancellation(message: types.Message):
    await message.answer('Куда отправляемся? 😊', reply_markup=interface.main_menu())



@dp.message_handler()
async def getinfo(message: types.Message):
    is_register = config.UserDatabaseConfig(message.from_user.id, '', 0).is_registered()
    if not is_register:
        markup = types.ReplyKeyboardRemove(selective=False)
        await message.answer("Привет, {}! Вы еще не зарегистрированы 😔 Для того, чтобы пройти регистрацию, пожалуйста введите свою дату рождения в формате дд-мм-гггг:".format(message.from_user.first_name), reply_markup=markup)
    else:
        await message.answer("Куда отправляемся? 😊", reply_markup=interface.main_menu())


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)