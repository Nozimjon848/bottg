import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8175639769:AAFhaRviSi__0FnkAjlNnff8o0xSAiV4U98"  # Bu yerga tokeningizni qo‘ying
bot = telebot.TeleBot(TOKEN)

ADMIN_IDS = [7591362695]  # O‘z Telegram ID'ingizni qo‘shing

# Ovoz narxlari (admin o‘zgartirishi mumkin)
prices = {
    "1ta ovoz": 12000,
    "2ta ovoz": 24000,
    "3ta ovoz": 38000
}

# Asosiy menyu
def get_menu(user_id):
    menu = ReplyKeyboardMarkup(resize_keyboard=True)
    menu.add(KeyboardButton("⚡ Budjet ma’lumotlari"))
    menu.add(KeyboardButton("🔄 Ovoz berish"), KeyboardButton("✍ Administor"))
    
    if user_id in ADMIN_IDS:
        menu.add(KeyboardButton("⚙ Admin Panel"))

    return menu

# Ovoz berish inline tugmalari
vote_inline = InlineKeyboardMarkup()
vote_inline.add(InlineKeyboardButton("🛠 Admin", url="https://t.me/Nematov_Nozimjon"))

@bot.message_handler(commands=['start'])
def start(message):
    first_name = message.from_user.first_name if message.from_user.first_name else "Foydalanuvchi"
    bot.send_message(message.chat.id, f"Salom, {first_name}! Open Budget botiga xush kelibsiz!", reply_markup=get_menu(message.from_user.id))

@bot.message_handler(func=lambda message: message.text == "🔄 Ovoz berish")
def vote(message):
    with open("a.png", "rb") as photo:
        bot.send_photo(message.chat.id, photo, caption="Assalomu alekum\nOpen Budget ga ovoz berishni istasangiz marhamat\nBiz ishonchli va tezkormiz\n\n1-ta ovoz = 12,000 so'm\nOvoz berishni istasangiz Admin tugmasini bosing\n\nBizni tanlaganingiz uchun xursandmiz", reply_markup=vote_inline)

@bot.message_handler(func=lambda message: message.text == "⚡ Budjet ma’lumotlari")
def budget_info(message):
    text = "📊 Budjet bo‘yicha umumiy ma’lumotlar:\n\n"
    for key, value in prices.items():
        text += f" {key} = {value} so‘m\n"
    
    text += "\nOvoz berish uchun 🔄 Ovoz berish tugmasini bosing\nFiribgarlarga aldanib qolmang.\n📌 Batafsil: @Person8778"
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda message: message.text == "✍ Administor")
def contact_admin(message):
    bot.send_message(message.chat.id, "📊 Admin bilan bog‘laning:\n📌 Admin: @Person8778")

# *** ADMIN PANEL ***
@bot.message_handler(func=lambda message: message.text == "⚙ Admin Panel")
def admin_panel(message):
    if message.from_user.id not in ADMIN_IDS:
        bot.send_message(message.chat.id, "🚫 Siz admin emassiz!")
        return

    admin_menu = ReplyKeyboardMarkup(resize_keyboard=True)
    admin_menu.add(KeyboardButton("📝 Reklama qo‘shish"), KeyboardButton("💰 Narxni o‘zgartirish"))
    admin_menu.add(KeyboardButton("🔙 Ortga"))

    bot.send_message(message.chat.id, "⚙ Admin paneliga xush kelibsiz!", reply_markup=admin_menu)

# *** Admin Panel - Statistika ***
@bot.message_handler(func=lambda message: message.text == "📊 Statistika")
def show_statistics(message):
    if message.from_user.id not in ADMIN_IDS:
        bot.send_message(message.chat.id, "🚫 Siz admin emassiz!")
        return

    bot.send_message(message.chat.id, "📈 Bot statistikasi:\n\n👥 Foydalanuvchilar: 1500\n📌 Ovozlar sotildi: 240 ta\n💰 Jami daromad: 2 880 000 so‘m")

# *** Admin Panel - Reklama qo‘shish ***
@bot.message_handler(func=lambda message: message.text == "📝 Reklama qo‘shish")
def add_advertisement(message):
    if message.from_user.id not in ADMIN_IDS:
        bot.send_message(message.chat.id, "🚫 Siz admin emassiz!")
        return

    bot.send_message(message.chat.id, "📝 Yangi reklamani kiriting:")
    bot.register_next_step_handler(message, save_advertisement)

def save_advertisement(message):
    if message.from_user.id not in ADMIN_IDS:
        bot.send_message(message.chat.id, "🚫 Siz admin emassiz!")
        return

    bot.send_message(message.chat.id, f"📢 Yangi reklama saqlandi:\n\n{message.text}")

# *** Admin Panel - Narxlarni o‘zgartirish ***
@bot.message_handler(func=lambda message: message.text == "💰 Narxni o‘zgartirish")
def change_price(message):
    if message.from_user.id not in ADMIN_IDS:
        bot.send_message(message.chat.id, "🚫 Siz admin emassiz!")
        return

    bot.send_message(message.chat.id, "💰 Yangi narxni kiriting (masalan: 1ta ovoz = 15 000 so‘m):")
    bot.register_next_step_handler(message, save_new_price)

def save_new_price(message):
    if message.from_user.id not in ADMIN_IDS:
        bot.send_message(message.chat.id, "🚫 Siz admin emassiz!")
        return

    try:
        key, value = message.text.split("=")
        key = key.strip()
        value = int(value.strip().replace("so‘m", "").replace(",", ""))
        prices[key] = value
        bot.send_message(message.chat.id, f"✅ Yangi narx saqlandi:\n\n{key} = {value} so‘m")
    except:
        bot.send_message(message.chat.id, "❌ Xato! Formatni to‘g‘ri kiriting: 1ta ovoz = 15000 so‘m")

# *** Ortga qaytish tugmasi ***
@bot.message_handler(func=lambda message: message.text == "🔙 Ortga")
def go_back(message):
    bot.send_message(message.chat.id, "🏠 Asosiy menyu", reply_markup=get_menu(message.from_user.id))

bot.polling(none_stop=True)
