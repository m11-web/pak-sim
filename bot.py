import sqlite3
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Aapka Token
TOKEN = '8686082838:AAH81ZiJpv1JIezHb4mZZDBpGyqujct0EWE'

def search_db(user_input):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        # User input se space khatam karna
        search_term = user_input.strip()
        
        # Smart Search: Ye 'details' table mein search karega
        # Hum 'LIKE' use kar rahe hain taake agar number ke aage-piche thora farq ho tab bhi mil jaye
        query = "SELECT * FROM details WHERE Mobile LIKE ? OR mobile LIKE ?"
        cursor.execute(query, (f'%{search_term}%', f'%{search_term}%'))
        
        result = cursor.fetchone()
        
        # Automatic Column Names: Aapko naam dene ki zaroorat nahi, ye khud nikalega
        column_names = [description[0] for description in cursor.description]
        
        conn.close()
        return result, column_names
    except Exception as e:
        print(f"⚠️ Error: {e}")
        return None, None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Assalam-o-Alaikum!\nBas mobile number likh kar bhejen, main poori detail nikaal doon ga.")

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user_input = update.message.text.strip()
    print(f"🔍 Searching for: {user_input}")
    
    row_data, column_headers = search_db(user_input)
    
    if row_data:
        response_msg = "✅ **Record Mil Gaya!**\n\n"
        # Ye loop khud hi saare columns (Name, Address, CNIC etc) ko print karega
        for i in range(len(column_headers)):
            val = row_data[i] if row_data[i] else "N/A"
            response_msg += f"📌 **{column_headers[i]}**: `{val}`\n"
        
        await update.message.reply_text(response_msg, parse_mode="Markdown")
    else:
        await update.message.reply_text(f"❌ Record nahi mila: {user_input}\nFormat check karein ya confirm karein ke number list mein hai.")

if __name__ == '__main__':
    print("🚀 Bot starting...")
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_msg))
    
    print("✅ Bot Online hai! Ab check karein.")
    app.run_polling(drop_pending_updates=True)
    
