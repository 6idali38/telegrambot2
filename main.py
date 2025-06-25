import telebot
from flask import Flask, request
from datetime import datetime
import os

# 🔐 Token et ID du groupe
TOKEN = '7800030017:AAFSqyNM91DyyB0693OqwM3rat739iBuQrM'
GROUP_ID = -1002844644447

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

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
        try:
            media_group = []
            for i in range(1, 11):
                path = f"images/photo{i}.jpeg"
                caption = list(menu_items.keys())[i-1] if i-1 < len(menu_items) else ""
                media_group.append(telebot.types.InputMediaPhoto(open(path, "rb"), caption=caption))
            bot.send_media_group(call.message.chat.id, media_group)
        except Exception as e:
            bot.send_message(call.message.chat.id, "⚠️ Une erreur est survenue lors de l'envoi des photos.")
            print(f"❌ Erreur: {e}")

    elif item == "contact":
        bot.send_message(call.message.chat.id, "📞 Pour toute information, contactez-nous sur E-mail : elisavasile0603@gmail.com")
        bot.answer_callback_query(call.id)

@app.route('/')
def index():
    return "Bot is running", 200

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return '', 200

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"https://telegrambot2-vkgt.onrender.com/7800030017:AAFSqyNM91DyyB0693OqwM3rat739iBuQrM")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
