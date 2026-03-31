import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# --- زانیاریێن بۆتێ تە یێ نوی ---
TOKEN = "8529357054:AAG2P9yyJOr-ftykUfO8t87JjeQRi3CabG4"
GEMINI_KEY = "AIzaSyD3ijHsJOPRtHdSuiMQdPGqQcZRe06FgE4"

# --- ڕێکخستنا مێشکێ ڕاوێژکارێ دەروونی ---
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction="""تۆ ڕاوێژکارەکێ دەروونی یێ شارەزا و دلسۆزی ل دەڤەرا بەهدینان. 
    زاراڤێ تە بەهـدیـنـی یە. کارێ تە گوهداریکردن و پشتەڤانیکردنا خەلکییە. 
    ئەگەر کەسەک باسی ئازاردانا خۆ کر، بێژێ 'تکایە سەرەدانا دکتۆرەکێ پسپۆر بکە'."""
)

async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_text = update.message.text
        # وەرگرتنا بەرسڤێ ژ مێشکێ AI
        chat = model.start_chat(history=[])
        response = chat.send_message(user_text)
        # فرێکرنا بەرسڤێ ب بەهدینی
        await update.message.reply_text(response.text)
    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("ببوورە کێشەیەکا تەکنیکی هەبوو، جارەکا دی تاقی بکە.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = "بخێر بێی.. ئەز ڕاوێژکارێ تە یێ دەروونی مە ب زاراڤێ بەهدینی. دشێی هەر خەمەک یان ئاریشەکا تە هەبیت لێرە بنڤیسی. 🌿"
    await update.message.reply_text(welcome_msg)

if __name__ == "__main__":
    # دروستکرنا ئەپلیکەیشنا بۆتی
    application = Application.builder().token(TOKEN).build()
    
    # زێدەکرنا فرمانێن تێلیگرامێ
    application.add_handler(MessageHandler(filters.COMMAND & filters.Regex("/start"), start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))
    
    print("بۆتێ ڕاوێژکاری یێ ئامادەیە...")
    application.run_polling()
