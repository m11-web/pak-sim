import sqlite3
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = '8686082838:AAH81ZiJpv1JIezHb4mZZDBpGyqujct0EWE'

def search_db(num):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        # Hum assume kar rahe hain column ka naam 'number' hai
        cursor.execute("SELECT * FROM details WHERE number = ?", (num,))
        result = cursor.fetchone()
        cols = [d[0] for d in cursor.description]
        conn.close()
        return result, cols
    except:
        return None, None

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    num = update.message.text.strip()
    data, cols = search_db(num)
    if data:
        msg = "✅ **Detail:**\n"
        for i in range(len(cols)):
            msg += f"**{cols[i]}**: {data[i]}\n"
        await update.message.reply_text(msg, parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ Record nahi mila.")

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
    app.run_polling()
    
