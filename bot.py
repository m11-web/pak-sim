import sqlite3
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TOKEN = '8686082838:AAH81ZiJpv1JIezHb4mZZDBpGyqujct0EWE'

def search_db(mobile_val):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        # Query mein column ka naam 'Mobile' rakha hai
        cursor.execute("SELECT * FROM details WHERE Mobile = ?", (mobile_val,))
        result = cursor.fetchone()
        cols = [d[0] for d in cursor.description]
        conn.close()
        return result, cols
    except Exception as e:
        return None, None

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()
    data, cols = search_db(user_input)
    
    if data:
        msg = "✅ **Detail Mil Gayi:**\n\n"
        for i in range(len(cols)):
            msg += f"**{cols[i]}**: {data[i]}\n"
        await update.message.reply_text(msg, parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ Record maujood nahi hai.")

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
    print("Bot is running...")
    app.run_polling()
