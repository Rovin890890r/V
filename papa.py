from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
import time, json, os

ADMIN_ID = 8000733829
USERS_FILE = "users.json"
APPROVED_FILE = "approved.json"
user_states = {}

# Save user to full list
def save_user(user_id):
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump([], f)
    with open(USERS_FILE, "r") as f:
        users = json.load(f)
    if user_id not in users:
        users.append(user_id)
        with open(USERS_FILE, "w") as f:
            json.dump(users, f)

# Load approved users
def load_approved_users():
    if not os.path.exists(APPROVED_FILE):
        with open(APPROVED_FILE, "w") as f:
            json.dump([], f)
    with open(APPROVED_FILE, "r") as f:
        return json.load(f)

# Save approved user
def save_approved_user(user_id):
    approved = load_approved_users()
    if user_id not in approved:
        approved.append(user_id)
        with open(APPROVED_FILE, "w") as f:
            json.dump(approved, f)

# Start command
def start(update: Update, context: CallbackContext):
    if update.effective_chat.type != "private":
        update.message.reply_text("❗ This bot works only in private chat.")
        return

    user_id = update.effective_user.id
    save_user(user_id)

    if user_id not in load_approved_users():
        keyboard = [[InlineKeyboardButton("🛡 Contact Admin", url="https://t.me/+Tn8USVhdIhphY2Nl")]]
        update.message.reply_text(
            "🚫 You are *not approved* to use this bot.\n\nPlease contact the admin.",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
        return

    # Approved users get the full menu
    keyboard = [
        [InlineKeyboardButton("🔥 Start Attack", callback_data='start_attack')],
        [InlineKeyboardButton("💬 Contact Admin", url="https://t.me/rovin_vip")],
        [InlineKeyboardButton("💰 View Plans", callback_data='plans')],
        [InlineKeyboardButton("❌ Cancel", callback_data='cancel')],
    ]
    update.message.reply_text(
        "⚡ *Welcome to DRAGON STRIKE VIP* ⚡\n\nUnleash 3D fire on your enemies!",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

# Inline buttons
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    query.answer()

    if user_id not in load_approved_users():
        query.edit_message_text("❌ You are not approved. Contact admin.")
        return

    if query.data == "start_attack":
        if user_id != ADMIN_ID:
            query.edit_message_text("❌ Only admin can launch attacks.")
            return
        user_states[user_id] = "awaiting_ip"
        query.edit_message_text("🧨 Enter the *IP address* to attack:", parse_mode='Markdown')

    elif query.data == "plans":
        query.edit_message_text(
            "💸 *VIP PLANS LIST:*\n\n"
            "⚔️ 1 Day Access: ₹100\n"
            "⚔️ 7 Days Access: ₹500\n"
            "⚔️ 1 Month Access: ₹1200\n"
            "⚔️ Full Season: ₹2000\n\n"
            "👉 Contact: [@rovin_vip](https://t.me/+Tn8USVhdIhphY2Nl)",
            parse_mode='Markdown'
        )

    elif query.data == "cancel":
        query.edit_message_text("❌ Operation cancelled.")

    elif query.data == "menu":
        start(query, context)

# Message handler for IP/Port input
def message_handler(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in load_approved_users():
        update.message.reply_text("❌ You are not approved to use this bot.")
        return

    state = user_states.get(user_id)
    if state == "awaiting_ip":
        context.user_data['ip'] = update.message.text
        user_states[user_id] = "awaiting_port"
        update.message.reply_text("📡 Now enter the *PORT* to target:", parse_mode='Markdown')

    elif state == "awaiting_port":
        ip = context.user_data.get('ip')
        port = update.message.text
        user_states[user_id] = None
        launch_attack(update, context, ip, port)

# Stylish 3D launch system
def launch_attack(update, context, ip, port):
    msg = update.message.reply_text("🐉 Initializing 3D Dragon System...")
    time.sleep(1)
    msg.edit_text("🧠 AI Locking on target...")
    time.sleep(1)
    msg.edit_text(f"🎯 Target Locked: `{ip}:{port}`", parse_mode='Markdown')
    time.sleep(1)
    msg.edit_text("🚀 Engaging 3D Strike System...")
    time.sleep(1)

    context.bot.send_animation(
        chat_id=update.effective_chat.id,
        animation="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExN3g2NjloZ29hOGJ4aTdkOXY2aWZrdG54YW5va3hram0zNW52eWkxdyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/f9k1tV7HyORcikIHRB/giphy.gif",
        caption=(
            "⚠️ *DRAGON FIRE UNLEASHED!*\n\n"
            f"🔥 Target: `{ip}:{port}`\n"
            "⚔️ Power: *MAXIMUM OVERDRIVE*\n"
            "🧨 Status: `ENGAGED`\n\n"
            "*HUN... HUN... HUN...* 🔥🔥🔥\n"
            "No mercy. No escape."
        ),
        parse_mode='Markdown'
    )

    time.sleep(1)
    context.bot.send_message(update.effective_chat.id, "🔥 *HUN...*", parse_mode='Markdown')
    time.sleep(0.8)
    context.bot.send_message(update.effective_chat.id, "🔥🔥 *HUN... HUN...*", parse_mode='Markdown')
    time.sleep(0.8)
    context.bot.send_message(update.effective_chat.id, "🔥🔥🔥 *HUN... HUN... HUN...*", parse_mode='Markdown')

    back_btn = [[InlineKeyboardButton("🔙 Back to Menu", callback_data='menu')]]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="✅ Attack complete. What do you want next?",
        reply_markup=InlineKeyboardMarkup(back_btn)
    )

# /users command to count total registered users
def users_command(update: Update, context: CallbackContext):
    if update.effective_user.id != ADMIN_ID:
        update.message.reply_text("❌ You are not authorized.")
        return

    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            users = json.load(f)
        total = len(users)
    else:
        total = 0
    update.message.reply_text(f"👥 Total Registered Members: *{total}*", parse_mode='Markdown')

# /approve command
def approve(update: Update, context: CallbackContext):
    if update.effective_user.id != ADMIN_ID:
        update.message.reply_text("❌ You are not authorized.")
        return
    if context.args:
        try:
            user_id = int(context.args[0])
            save_approved_user(user_id)
            update.message.reply_text(f"✅ Approved user `{user_id}`.", parse_mode='Markdown')
        except:
            update.message.reply_text("❌ Invalid ID.")
    else:
        update.message.reply_text("Usage: /approve USER_ID")

# Run the bot
def main():
    updater = Updater("YOUR_BOT_TOKEN", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("approve", approve, pass_args=True))
    dp.add_handler(CommandHandler("users", users_command))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text & Filters.private, message_handler))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()