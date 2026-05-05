import logging
import os
from threading import Thread
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

# 1. Flask Server for Render (Keep-alive)
# Render ሰርቨሩ ቦቱ መኖሩን በየጊዜው የሚያረጋግጥበት የዌብ ገጽ
server = Flask('')

@server.route('/')
def home():
    return "Gato Bot is running and healthy!"

def run_flask():
    # Render የሚሰጠውን PORT ይጠቀማል
    port = int(os.environ.get('PORT', 8080))
    server.run(host='0.0.0.0', port=port)

# 2. የቦት መረጃዎች (Configuration)
TOKEN = "8713409379:AAHXJ2s_qxpwR_tVGRVPOPDvjgnGOKc-5l4"
ADMIN_CHAT_ID = "8723642768" 

# ዝርዝር የውል ይዘቶች
CONTRACTS = {
    "consultancy": {
        "name": "የንግድ አገልግሎት ውል ስምምነት",
        "content": (
            "📄 *የንግድ አገልግሎት ውል ስምምነት*\n\n"
            "ቁጥር፦ _____________\n"
            "ቀን፦ ________________\n\n"
            "ይህ የንግድ አገልግሎት ውል ስምምነት በሁለቱ ተዋዋይ ወገኖች መካከል ተደርጓል።\n\n"
            "*ተዋዋይ ወገኖች፦*\n"
            "1. ጋቶ ኮንሰልታንሲ እና ትሬዲንግ ኃ/የተ/የግ/ማህበር (አማካሪው)\n"
            "2. ደንበኛው (አቶ/ወ/ሮ/ድርጅት ______________)\n\n"
            "*አንቀጽ 1፦ የውሉ መነሻ*\n"
            "ደንበኛው በኢትዮጵያ የንግድ አዋጅ ቁጥር 1243/2013 መሰረት አዲስ የኮንስትራክሽን ኃላፊነቱ የተወሰነ የግል ማህበር (PLC) ለማቋቋም ለሚፈልገው ስራ አማካሪው ሙያዊ ድጋፍና ጉዳይ አስፈጻሚ እንዲሆን በመፈለጉ ይህ ውል ተመስርቷል።\n\n"
            "*አንቀጽ 2፦ የአማካሪው ግዴታዎች*\n"
            "አማካሪው በንግድ አዋጁ ድንጋጌዎች መሰረት የሚከተሉትን ስራዎች ያከናውናል፦\n"
            "2.1. በንግድ አዋጅ አንቀጽ 22 መሰረት የድርጅቱን ስም ማስፈቀድ።\n"
            "2.2. በአዋጁ አንቀጽ 256 እና ተከታዮቹ መሰረት የማህበሩን የመመስረቻ ጽሁፍ ማዘጋጀትና በውልና ማስረጃ ማጽደቅ።\n"
            "2.3. ለኮንስትራክሽን ስራ የሚያስፈልገውን የብቃት ማረጋገጫ ከሚመለከተው የመንግስት መስሪያ ቤት ማስፈጸም።\n"
            "2.4. የንግድ ምዝገባና የንግድ ፈቃድ ማውጣት፣ የታክስ መለያ ቁጥር (TIN) እና የቫት (VAT) ምዝገባ ማጠናቀቅ።\n\n"
            "*አንቀጽ 3፦ የአገልግሎት ክፍያ*\n"
            "3.1. ደንበኛው ለአማካሪው ለሚሰጠው አገልግሎት በጠቅላላው ብር 180,000.00 (አንድ መቶ ሰማኒያ ሺ ብር) ለመክፈል ተስማምቷል።\n"
            "3.2. አከፋፈሉም በሚከተለው መልኩ ይሆናል፦\n"
            "• ቅድመ ክፍያ (30%): ውሉ ሲፈረም ብር 54,000.00።\n"
            "• ሁለተኛ ክፍያ (40%): የመመስረቻ ጽሁፉ በሰነዶች ማረጋገጫ ጸድቆ የንግድ ፈቃዱ ሲወጣ ብር 72,000.00።\n"
            "• የመጨረሻ ክፍያ (30%): የኮንስትራክሽን ብቃት ማረጋገጫው ተጠናቆ ለደንበኛው ሲረከብ ብር 54,000.00።\n\n"
            "3.3. ለማንኛውም የመንግስት ክፍያዎች ደንበኛው እንደ አስፈላጊነቱ በደረሰኝ ይከፍላል፤ እነዚህ ወጪዎች ከአማካሪው የአገልግሎት ክፍያ ጋር አይገናኙም።\n\n"
            "*አንቀጽ 4፦ ምስጢር የመጠበቅ ግዴታ*\n"
            "አማካሪው ከደንበኛው የሚቀበላቸውን ማናቸውንም የንግድ ምስጢሮችና መረጃዎች ለሶስተኛ ወገን አሳልፎ ላለመስጠት በንግድ ህጉ መሰረት ተገቢውን ጥንቃቄ ያደርጋል።\n\n"
            "*አንቀጽ 5፦ ውሉ የሚጸናበት ጊዜ*\n"
            "ይህ ውል በሁለቱ ወገኖች ተፈርሞ ታክስና የንግድ ፈቃድ ስራዎች ተጠናቀው ለደንበኛው እስከሚረከቡ ድረስ የጸና ይሆናል።"
        )
    },
    "accounting": {
        "name": "የሂሳብ እና የግብር አገልግሎት ውል",
        "content": (
            "📦 *የሂሳብ አያያዝ እና የግብር አማካሪነት ውል*\n\n"
            "*አንቀጽ 1፦ የአገልግሎት ዝርዝር*\n"
            "ወርሃዊ የቫት (VAT)፣ የቲኦቲ (TOT) እና የፔይሮል (Payroll) ሪፖርቶችን ማዘጋጀትና ማሳወቅ።\n\n"
            "*አንቀጽ 2፦ የአገልግሎት ክፍያ*\n"
            "• ወርሃዊ ክፍያ፦ ብር 20,000.00 (Net)\n\n"
            "*አንቀጽ 3፦ ምስጢር የመጠበቅ ግዴታ*\n"
            "አማካሪው ማንኛውንም የድርጅቱን የፋይናንስ መረጃ ሚስጥራዊነቱን የመጠበቅ ግዴታ አለበት።"
        )
    },
    "investment": {
        "name": "የኢንቨስትመንት ውል",
        "content": "💰 *የኢንቨስትመንት ውል*\n\nይህ ውል ለጋራ ኢንቨስትመንት ስራዎች የተዘጋጀ የህግ ስምምነት ሰነድ ነው።"
    }
}

# Logging ቅንብር
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ቦቱ ሲጀመር የሚመጣ ሰላምታ"""
    user = update.effective_user
    keyboard = []
    for key, value in CONTRACTS.items():
        keyboard.append([InlineKeyboardButton(value["name"], callback_data=f"select_{key}")])
    
    keyboard.append([InlineKeyboardButton("🏢 ስለ እኛ", callback_data='about_us')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"ሰላም {user.first_name}!\nወደ ጋቶ ኮንሰልታንሲ ቦት እንኳን ደህና መጡ።\nእባክዎ ማየት የሚፈልጉትን የውል ሰነድ ይምረጡ፦",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """የአዝራር ምርጫዎችን የሚያስተናግድ ክፍል"""
    query = update.callback_query
    user = query.from_user
    
    try:
        await query.answer()
    except Exception as e:
        logging.error(f"Error answering query: {e}")

    if query.data.startswith('select_'):
        key = query.data.split('_')[1]
        contract = CONTRACTS.get(key)
        
        text = f"{contract['content']}\n\nእባክዎ ውሉን በጥንቃቄ ካነበቡ በኋላ ምርጫዎን ያሳውቁ፦"
        keyboard = [
            [
                InlineKeyboardButton("✅ እስማማለሁ", callback_data=f"acc_{key}"),
                InlineKeyboardButton("❌ አልስማማም", callback_data=f"dec_{key}")
            ],
            [InlineKeyboardButton("⬅️ ወደ ኋላ ተመለስ", callback_data="back")]
        ]
        await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    
    elif query.data.startswith('acc_'):
        key = query.data.split('_')[1]
        contract_name = CONTRACTS[key]['name']
        
        await query.edit_message_text(f"አመሰግናለን! በ'{contract_name}' ስምምነት ላይ ያለዎት ተገቢነት ተመዝግቧል። በቅርቡ እናገኝዎታለን።")
        
        # ለአድሚን መልዕክት መላክ
        admin_msg = (
            "🔔 *አዲስ የውል ስምምነት ተፈርሟል!*\n\n"
            f"👤 ደንበኛ፦ {user.full_name}\n"
            f"🔗 ዩዘር ኔም፦ @{user.username if user.username else 'የለውም'}\n"
            f"📑 የውል አይነት፦ {contract_name}"
        )
        try:
            await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_msg, parse_mode='Markdown')
        except Exception as e:
            logging.error(f"Admin notification failed: {e}")

    elif query.data.startswith('dec_'):
        await query.edit_message_text("ስምምነቱን ባለመቀበልዎ እናዝናለን። ለተጨማሪ መረጃ በስልክ ቁጥራችን ይደውሉልን።")

    elif query.data == 'about_us':
        about_text = "🏢 *ጋቶ ኮንሰልታንሲ እና ትሬዲንግ*\n\nእኛ በንግድ አማካሪነት እና በተለያዩ ዘርፎች ላይ የምንሰራ ድርጅት ነን።"
        keyboard = [[InlineKeyboardButton("⬅️ ተመለስ", callback_data="back")]]
        await query.edit_message_text(text=about_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    elif query.data == "back":
        keyboard = []
        for key, value in CONTRACTS.items():
            keyboard.append([InlineKeyboardButton(value["name"], callback_data=f"select_{key}")])
        keyboard.append([InlineKeyboardButton("🏢 ስለ እኛ", callback_data='about_us')])
        await query.edit_message_text("እባክዎ የውል አይነት ይምረጡ፦", reply_markup=InlineKeyboardMarkup(keyboard))

if __name__ == '__main__':
    # Flask ሰርቨሩን በሌላ Thread ያስነሳል (Render keep-alive)
    Thread(target=run_flask).start()
    
    # ቦቱን ያስነሳል
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("ጋቶ ቦት እና ሰርቨሩ ስራ ጀምረዋል...")
    
    # በ Render ላይ ለረጅም ጊዜ እንዲቆይ poll_interval ጨምረናል
    app.run_polling(poll_interval=1.0)