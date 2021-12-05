from aiogram import types

def main_menu():
    buttons = ['❤️ Мои места', '🧑‍💻 Поддержка']
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🌚 Выбрать место')
    markup.add('⭐️ Добавить место')
    markup.add(*buttons)
    return markup

def show_categories(categories):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(len(categories)):
            btn = "🌚 {}. {}".format(categories[i][0], categories[i][1])
            markup.add(btn)
    markup.add("⬅️ Назад")
    return markup

def show_places_list_keyboard(places):
    # places => [post_id, post_name]
    buttons = []
    for i in range(len(places)):
        buttons.append(types.InlineKeyboardButton(text="{}".format((i + 1)), callback_data="post_id_{}".format(places[i][0])))
    buttons.append(types.InlineKeyboardButton(text="❌", callback_data="post_id_cancel"))
    markup = types.InlineKeyboardMarkup(row_width=5)
    markup.add(*buttons)
    return markup

def generate_link_markup(link):
    button = types.InlineKeyboardMarkup(text="🗺 Открыть карту", url=link)
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(button)
    return markup

def generate_our_website(link):
    button = types.InlineKeyboardMarkup(text="Перейти на сайт", url=link)
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(button)
    return markup
