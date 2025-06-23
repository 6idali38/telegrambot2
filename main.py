import telebot
from datetime import datetime
from keep_alive import keep_alive  # لإبقاء البوت شغال 24/24

# 🔐 Token et ID du groupe
TOKEN = '7800030017:AAFQW30A4zzO-Awj5W388Rink5gx4zQQDm4'
GROUP_ID = -1002844644447

bot = telebot.TeleBot(TOKEN)

# 📋 Menu
menu_items = {
    "🍔 Burger sushi – 200g – 10 €": "commande: Burger sushi – 10 €",
    "🍣 Sandwich sushi – 120g – 8 €": "commande: Sandwich sushi – 8 €",
    "🌭 Hot dog sushi – 250g – 10 €": "commande: Hot dog sushi – 10 €",
    "🍗 Ailes de poulet épicées (6 pièces) – 7 €": "commande: Ailes de poulet épicées – 7 €",
    "🍟🥘 Nuggets (10 pièces) – 8 €": "commande: Nuggets – 8 €",
    "🌭 Saucisses en pâte – 8 €": "commande: Saucisses en pâte – 8 €",
    "🥙 Kebab de poitrine de poulet – 200g – 8 €": "commande: Kebab de poulet – 8 €",
    "🍟 Frites – 3,5 €": "commande: Frites – 3,5 €",
    "🧃 Jus de fruits naturel – 8 €": "commande: Jus de fruits – 8 €",
    "🍔 Krabs Burgher": "commande: Krabs Burgher"
}

# 🚀 Commande /start → Affiche le menu
@bot.message_handler(commands=['start'])
def send_menu(message):
    markup = telebot.types.InlineKeyboardMarkup()
    for item in menu_items:
        markup.add(telebot.types.InlineKeyboardButton(text=item, callback_data=item))
    markup.add(
        telebot.types.InlineKeyboardButton("📷 Voir les photos", callback_data="photos"),
        telebot.types.InlineKeyboardButton("📞 Nous contacter", callback_data="contact")
    )
    bot.send_message(message.chat.id, "📋 Bienvenue dans notre menu ! Veuillez choisir un plat ci-dessous :", reply_markup=markup)

# 🖱️ Gérer les clics sur les boutons
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    item = call.data
    if item in menu_items:
        order_text = menu_items[item]
        user = f"👤 {call.from_user.first_name} (@{call.from_user.username})"
        time_now = f"🕒 {datetime.now().strftime('%d/%m/%Y - %H:%M')}"
        full_msg = f"🍽️ Nouvelle commande :\n{user}\n{order_text}\n{time_now}"
        bot.send_message(GROUP_ID, full_msg)
        bot.answer_callback_query(call.id, text="✅ Votre commande a été envoyée !")

    elif item == "photos":
        bot.send_photo(call.message.chat.id, "AgACAgQAAxkBAAIC8mhZI8WEEDEOdok1TVkmU7zbOEf8AALmxjEbusXIUiyMZk9g-CySAQADAgADeAADNgQ", caption="🍔 Burger sushi – 10 €")
        # 🔁 أضف باقي الصور بنفس الشكل

    elif item == "contact":
        bot.send_message(call.message.chat.id, "📞 Pour toute information, contactez-nous sur E-mail : elisavasile0603@gmail.com")
        bot.answer_callback_query(call.id)

# ✅ Logs
print("✅ Le bot est en ligne...")

# 🧠 Garder البوت شغال 24/24
keep_alive()

# ▶️ Démarrage du bot
bot.infinity_polling()
