import logging
import os
from threading import Thread
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

# 1. Flask Server for Render (Keep-alive)
server = Flask('')

@server.route('/')
def home():
    return "Gato Bot is running!"

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    server.run(host='0.0.0.0', port=port)
# የቦት ቶከንዎን እዚህ ያስገቡ
TOKEN = "8713409379:AAHXJ2s_qxpwR_tVGRVPOPDvjgnGOKc-5l4"
# የአድሚን የቴሌግራም ID
ADMIN_CHAT_ID = "8723642768" 

# የውል ዓይነቶች ዝርዝር
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
            "ቁጥር፦ ________________\n"
            "ቀን፦ ________________\n\n"
            "*አንቀጽ 1፦ መግቢያ*\n"
            "ደንበኛው የፋይናንስ ስርአት እንዲዘረጋለት እና የግብር ግዴታዎቹ እንዲወጡለት አማካሪውን ቀጥሯል።\n\n"
            "*አንቀጽ 2፦ የአገልግሎቱ ዝርዝር*\n"
            "2.1. ወርሃዊ የቫት (VAT)፣ የቲኦቲ (TOT) እና የዊዝሆልዲንግ ማሳወቅ።\n"
            "2.2. የሰራተኞችን ደመወዝ ፔይሮል (Payroll) ማዘጋጀት።\n"
            "2.3. ዓመታዊ የሂሳብ ሪፖርት ማዘጋጀትና ለኦዲት ማቅረብ።\n\n"
            "*አንቀጽ 3፦ የደንበኛው ግዴታዎች*\n"
            "3.1. አማካሪው ለስራው የሚያስፈልጉ ሰነዶችን በወቅቱ ማቅረብ።\n"
            "3.2. ለስራው አስፈላጊ የሆኑ መረጃዎችን ትክክለኛነት ማረጋገጥ።\n\n"
            "*አንቀጽ 4፦ የውሉ ጸናታ ጊዜ*\n"
            "ይህ ውል በሁለቱ ወገኖች ስምምነት እስከ ተቋረጠ ድረስ ለ 1 (አንድ) አመት የጸና ይሆናል።\n\n"
            "*አንቀጽ 5፦ ስለ ክፍያ*\n"
            "5.1. ወርሃዊ ክፍያ፦ ብር 20,000 (ሃያ ሺህ ብር) የተጣራ (Net)።\n"
            "5.2. ትራንስፖርት እና አስተዳደራዊ ወጪዎች በደንበኛው ይሸፈናሉ።\n\n"
            "*አንቀጽ 6፦ የኃላፊነት ወሰን*\n"
            "አማካሪው ተጠያቂ የሚሆነው በራሱ የሙያ ግድፈት ለሚመጡ ስህተቶች ብቻ ነው።"
        )
    },
    "investment": {
        "name": "የኢንቨስትመንት ውል",
        "content": "💰 *የኢንቨስትመንት ውል*\n\nይህ ውል ለጋራ ኢንቨስትመንት ስራዎች የተዘጋጀ የህግ ስምምነት ነው። ዝርዝር ይዘቱ በቅርቡ ይካተታል።"
    }
}

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ቦቱ ሲጀመር የሚመጣ ሰላምታ"""
    user = update.effective_user
    welcome_message = (
        f"ሰላም {user.first_name}!\n\n"
        "ወደ ጋቶ ኮንሰልታንሲ እና ትሬዲንግ የቴሌግራም ቦት እንኳን ደህና መጡ።\n"
        "እባክዎ የትኛውን የውል ሰነድ ማግኘት እንደሚፈልጉ ይምረጡ።"
    )
    
    keyboard = []
    for key, value in CONTRACTS.items():
        keyboard.append([InlineKeyboardButton(value["name"], callback_data=f"select_{key}")])
    
    keyboard.append([InlineKeyboardButton("ስለ እኛ", callback_data='about_us')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(text=welcome_message, reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.reply_text(text=welcome_message, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    
    try:
        await query.answer()
    except Exception as e:
        logging.error(f"Error answering query: {e}")

    if query.data.startswith('select_'):
        contract_key = query.data.split('_')[1]
        contract = CONTRACTS.get(contract_key)
        
        if not contract:
            return

        text = f"{contract['content']}\n\nእባክዎ ውሉን ካነበቡ በኋላ ምርጫዎን ያሳውቁ።"
        keyboard = [
            [
                InlineKeyboardButton("✅ እስማማለሁ", callback_data=f'accept_{contract_key}'),
                InlineKeyboardButton("❌ አልስማማም", callback_data=f'decline_{contract_key}')
            ],
            [InlineKeyboardButton("⬅️ ወደ ኋላ ተመለስ", callback_data='back_to_start')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        try:
            await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode='Markdown')
        except Exception as e:
            logging.error(f"Error editing message: {e}")
            await query.edit_message_text(text=text, reply_markup=reply_markup)

    elif query.data.startswith('accept_'):
        contract_key = query.data.split('_')[1]
        contract_name = CONTRACTS[contract_key]['name']
        
        await query.edit_message_text(text=f"አመሰግናለን! የ'{contract_name}' ስምምነትን ተቀብለዋል። በቅርቡ እናገኝዎታለን።")
        
        notification = (
            "🔔 *አዲስ የውል ስምምነት!*\n\n"
            f"👤 ደንበኛ፦ {user.full_name}\n"
            f"🔗 Username: @{user.username}\n"
            f"📑 የውል ዓይነት፦ {contract_name}\n"
            "✅ ሁኔታ፦ ተስማምተዋል።"
        )
        try:
            await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=notification, parse_mode='Markdown')
        except Exception as e:
            logging.error(f"Admin notification error: {e}")

    elif query.data.startswith('decline_'):
        contract_key = query.data.split('_')[1]
        contract_name = CONTRACTS[contract_key]['name']
        await query.edit_message_text(text=f"የ'{contract_name}' ስምምነትን አልተቀበሉም።")

    elif query.data == 'about_us':
        about_text = "🏢 *ጋቶ ኮንሰልታንሲ እና ትሬዲንግ*\n\nእኛ በተለያዩ የንግድ ዘርፎች ላይ ማማከር እና የንግድ ስራዎችን እንሰራለን።"
        keyboard = [[InlineKeyboardButton("⬅️ ወደ ኋላ ተመለስ", callback_data='back_to_start')]]
        await query.edit_message_text(text=about_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    elif query.data == 'back_to_start':
        keyboard = []
        for key, value in CONTRACTS.items():
            keyboard.append([InlineKeyboardButton(value["name"], callback_data=f"select_{key}")])
        keyboard.append([InlineKeyboardButton("ስለ እኛ", callback_data='about_us')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text="እባክዎ የትኛውን የውል ሰነድ ማግኘት እንደሚፈልጉ ይምረጡ።",
            reply_markup=reply_markup
        )

if __name__ == '__main__':
    # ኢንተርኔት ቢቆራረጥ ቦቱ ስራ እንዳያቆም ጥንቃቄ ተደርጓል
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    print("ጋቶ ቦት ስራ ጀምሯል...")
    application.run_polling()