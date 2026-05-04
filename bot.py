import sqlite3
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Logging on rakhein taake GitHub logs mein sab nazar aaye
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)

# Aapka Token jo aapne bheja tha
TOKEN = '8686082838:AAH81ZiJpv1JIezHb4mZZDBpGyqujct0EWE'

def search_db(mobile_val):
    try:
        # Database se connect karna
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        # 'Mobile' column mein search karna (M capital)
        cursor.execute("SELECT * FROM details WHERE Mobile = ?", (mobile_val,))
        result = cursor.fetchone()
        
        # Columns ke naam nikalna
        cols = [d[0] for d in cursor.description]
        conn.close()
        return result, cols
    except Exception as e:
        print(f"⚠️ Database Error: {e}")
        return None, None

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check karein ke user ne text bheja hai
    if not update.message or not update.message.text:
        return

    user_input = update.message.text.strip()
    print(f"📩 User ne search kiya: {user_input}")
    
    data, cols = search_db(user_input)
    
    if data:
        msg = "✅ **Record Mil Gaya!**\n\n"
        for i in range(len(cols)):
            msg += f"**{cols[i]}**: {data[i]}\n"
        await update.message.reply_text(msg, parse_mode="Markdown")
    else:
        await update.message.reply_text(f"❌ Record nahi mila: {user_input}")

if __name__ == '__main__':
    print("--- BOT START HO RAHA HAI ---")
    
    # Application setup
    app = Application.builder().token(TOKEN).build()
    
    # Message handler lagana (Sirf text messages ke liye)
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_msg))
    
    print("🚀 Polling Shuru... Ab Telegram par number bhejein.")
    
    # Purane pending messages ko saaf karke bot chalu karna
    app.run_polling(drop_pending_updates=True)
    
