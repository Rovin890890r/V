import asyncio
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# === CONFIGURATION ===
BOT_TOKEN = "7806976016:AAFNRC_r_quK6qJkri6J_LOMe1ZvxygaboU"
ADMIN_IDS = [8000733829]  # Replace with actual admin ID(s)
ADMIN_USERNAME = "@rovin_vip"

approved_users = set()

def is_admin(user_id):
    return user_id in ADMIN_IDS

def is_approved(user_id):
    return user_id in approved_users

# === /start COMMAND ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    plans = (
        "✨ *Welcome to VIP Attack System* ✨\n\n"
        "💸 *Plans Available:*\n"
        "• ₹100 = 🔥 *1 Day* Access\n"
        "• ₹500 = ⚡ *7 Days* Access\n"
        "• ₹1200 = ⚔️ *30 Days* Access\n"
        "• ₹2000 = 🛡️ *Full Season* Access\n\n"
        f"📩 *Contact Admin:* {ADMIN_USERNAME} for approval."
    )
    await update.message.reply_text(plans, parse_mode="Markdown")

    keyboard = [
        [InlineKeyboardButton("📞 Contact Admin", url=f"https://t.me/{ADMIN_USERNAME.lstrip('@')}")],
        [
            InlineKeyboardButton("💸 View Plans", callback_data="view_plans"),
            InlineKeyboardButton("✅ Start", callback_data="start_attack" if is_admin(user_id) or is_approved(user_id) else "not_approved")
        ],
        [InlineKeyboardButton("❌ Cancel", callback_data="cancel")]
    ]

    await update.message.reply_text("👇 *Select an option below:*", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

# === CALLBACK HANDLER ===
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "view_plans":
        await query.edit_message_text(
            "💸 *VIP Plans:*\n\n• ₹100 = 1 Day\n• ₹500 = 7 Days\n• ₹1200 = 30 Days\n• ₹2000 = Full Season\n\nContact admin for approval.",
            parse_mode="Markdown"
        )
    elif query.data == "start_attack":
        await query.edit_message_text("✅ *Use command:* `/attack <ip> <port> <time>`", parse_mode="Markdown")
    elif query.data == "not_approved":
        await query.edit_message_text("⛔ *Access Denied!*\nPlease contact admin for approval.", parse_mode="Markdown")
    elif query.data == "cancel":
        await query.edit_message_text("❌ *Menu closed.*", parse_mode="Markdown")

# === /approve COMMAND ===
async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return await update.message.reply_text("❌ Unauthorized.")

    if len(context.args) != 1:
        return await update.message.reply_text("Usage: /approve <chat_id>")

    try:
        chat_id = int(context.args[0])
        approved_users.add(chat_id)
        await update.message.reply_text(f"✅ User `{chat_id}` approved successfully.", parse_mode="Markdown")
    except:
        await update.message.reply_text("❌ Invalid chat_id.")

# === /attack COMMAND ===
async def attack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    username = user.username or user.first_name or "N/A"

    if not (is_admin(user_id) or is_approved(user_id)):
        return await update.message.reply_text("❌ Permission denied. पहले admin से अनुमति लें।")

    if len(context.args) != 3:
        return await update.message.reply_text("⚠️ Usage: /attack <ip> <port> <time>")

    ip, port, duration = context.args
    try:
        duration = int(duration)
        if duration > 240:
            duration = 240
    except:
        return await update.message.reply_text("❌ Invalid time. Max allowed: 240 seconds.")

    now = datetime.now().strftime("%d-%m-%Y at %H:%M")

    # === CONFIRM TO USER ===
    await update.message.reply_text(
        f"🚀 *Attack Launched!*\n\n"
        f"🎯 Target: `{ip}:{port}`\n"
        f"⏱ Duration: `{duration} sec`\n"
        f"🕒 Time: *{now}*\n"
        f"👤 By: @{username} (`{user_id}`)",
        parse_mode="Markdown"
    )

    # === ADMIN BROADCAST WITH DRAGON IMAGE ===
    dragon_img = "https://i.imgur.com/KYVY1TP.jpeg"  # Replace if needed

    caption = (
        f"🔥 *DRAGON STRIKE INITIATED!* 🔥\n\n"
        f"👤 User: @{username}\n"
        f"🆔 ID: `{user_id}`\n\n"
        f"🎯 Target: `{ip}:{port}`\n"
        f"⏱️ Duration: `{duration} sec`\n"
        f"🕒 Launched: *{now}*\n\n"
        f"⚠️ Status: `ATTACK LIVE`\n"
        f"🐉 *This is not a drill!*"
    )

    for admin_id in ADMIN_IDS:
        try:
            await context.bot.send_photo(
                chat_id=admin_id,
                photo=dragon_img,
                caption=caption,
                parse_mode="Markdown"
            )
        except Exception as e:
            print("Error sending broadcast:", e)

    # USER BROADCAST WITH STYLE
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=dragon_img,
        caption="☣️ *DRAGON UNLEASHED!*\n\n🔥 Attack officially started!",
        parse_mode="Markdown"
    )

    await asyncio.sleep(duration)

    # FINISH NOTICE
    finish = (
        f"✅ *Attack Finished!*\n\n"
        f"👤 @{username} (`{user_id}`)\n"
        f"🎯 Target: `{ip}:{port}`"
    )
    for admin_id in ADMIN_IDS:
        try:
            await context.bot.send_message(chat_id=admin_id, text=finish, parse_mode="Markdown")
        except:
            pass

    await update.message.reply_text("✅ *Attack Completed!*", parse_mode="Markdown")

# === /admin PANEL ===
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return await update.message.reply_text("❌ Unauthorized.")

    msg = "👑 *Admin Panel*\n\n✅ *Approved Users:*\n"
    if approved_users:
        msg += "\n".join([f"• `{uid}`" for uid in approved_users])
    else:
        msg += "❌ कोई भी user approved नहीं है।"

    await update.message.reply_text(msg, parse_mode="Markdown")

# === MAIN FUNCTION ===
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(CommandHandler("approve", approve))
    app.add_handler(CommandHandler("attack", attack))
    app.add_handler(CommandHandler("admin", admin))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()