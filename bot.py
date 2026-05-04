import sqlite3
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = '8686082838:AAH81ZiJpv1JIezHb4mZZDBpGyqujct0EWE'

def search_db(user_input):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        # User ke input se saari dashes (-) aur spaces saaf karna
        clean_input = user_input.replace("-", "").replace(" ", "").strip()
        
        # SQL Query jo DB mein se bhi dashes hata kar match karegi
        # Is se database wala dash (0312-0000000) user ke clean input (03120000000) se match ho jayega
        query = """
        SELECT * FROM details 
        WHERE REPLACE(REPLACE(Mobile, '-', ''), ' ', '') = ? 
        OR REPLACE(REPLACE(mobile, '-', ''), ' ', '') = ?
        """
        cursor.execute(query, (clean_input, clean_input))
        
        result = cursor.fetchone()
        column_names = [description[0] for description in cursor.description]
        
        conn.close()
        return result, column_names
    except Exception as e:
        print(f"⚠️ Error: {e}")
        return None, None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Assalam-o-Alaikum!\nMobile number bhejen, chahay dash (-) ke sath ya baghair, main detail nikaal doon ga.")

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    raw_input = update.message.text.strip()
    print(f"🔍 Searching for: {raw_input}")
    
    row_data, column_headers = search_db(raw_input)
    
    if row_data:
        response_msg = "✅ **Record Mil Gaya!**\n\n"
        for i in range(len(column_headers)):
            val = row_data[i] if row_data[i] else "N/A"
            response_msg += f"📌 **{column_headers[i]}**: `{val}`\n"
        
        await update.message.reply_text(response_msg, parse_mode="Markdown")
    else:
        await update.message.reply_text(f"❌ Record nahi mila: {raw_input}\nFormat sahi se check karein.")

if __name__ == '__main__':
    print("🚀 Bot starting with Dash-Proof logic...")
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_msg))
    
    print("✅ Bot Online! Ab test karein.")
    app.run_polling(drop_pending_updates=True)
    
