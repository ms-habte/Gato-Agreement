import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton
import os
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# ይህንን ቦትህ ከሚጀምርበት ኮድ በፊት አስቀምጠው
Thread(target=run).start()
import threading
import os
# ቦቶቹን እዚህ ጋር Import ያድርጉ

def start_gato():
    # Gato ቦት የሚነሳበት ኮድ
    pass

def start_member_status():
    # Gato Member Status ቦት የሚነሳበት ኮድ
    pass

if __name__ == "__main__":
    t1 = threading.Thread(target=start_gato)
    t2 = threading.Thread(target=start_member_status)
    
    t1.start()
    t2.start()
# --- Configuration ---
API_TOKEN = '8634460031:AAGOqHZZlN4iWPwV_AqReCWjjn7LyKfuHgM'
ADMIN_CHAT_ID = '8723642768' 

# ጊዜያዊ ዳታ ቤዝ
all_reports = []

# Logging setup
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- States for FSM ---
class SurveyStates(StatesGroup):
    waiting_for_full_name = State()
    waiting_for_position = State() 
    waiting_for_job_type = State()
    waiting_for_work_hours = State() 
    waiting_for_decision = State()
    waiting_for_decision_reason = State()
    waiting_for_past_issues = State()
    waiting_for_solution = State()

# --- Keyboards ---
def get_job_type_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="🕒 የትርፍ ሰዓት (Part-time)"), KeyboardButton(text="📅 ሙሉ ሰዓት (Full-time)"))
    return builder.as_markup(resize_keyboard=True)

def get_decision_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="✅ መቀጠል እፈልጋለሁ"), KeyboardButton(text="❌ ማቋረጥ እፈልጋለሁ"))
    return builder.as_markup(resize_keyboard=True)

# --- Handlers ---

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    welcome_text = (
        "እንኳን ወደ ጋቶ ኮንሰልታንሲ እና ትሬዲንግ የአቋም መግለጫ ቦት በሰላም መጡ።\n\n"
        "እባክዎን መጀመሪያ ሙሉ ስምዎን ያስገቡ፦"
    )
    await message.answer(welcome_text)
    await state.set_state(SurveyStates.waiting_for_full_name)

# --- Admin Reply Logic (አስተዳዳሪው ለሰራተኛው መልስ እንዲሰጥ) ---
@dp.message(F.chat.id == int(ADMIN_CHAT_ID), F.reply_to_message)
async def admin_reply_handler(message: types.Message):
    """
    አስተዳዳሪው በቦቱ ሪፖርት ላይ 'Reply' ሲያደርግ ለሰራተኛው መልዕክቱን ያስተላልፋል
    """
    try:
        # ሪፖርቱ ሲላክ ከስር የተቀመጠውን User ID ፈልጎ ያወጣል
        reply_text = message.reply_to_message.text
        if "🆔 UserID:" in reply_text:
            # የሰራተኛውን Chat ID ከጽሁፉ ውስጥ ይለያል
            target_user_id = reply_text.split("🆔 UserID:")[1].strip().split("\n")[0]
            
            # መልዕክቱን ለሰራተኛው መላክ
            await bot.send_message(
                chat_id=target_user_id,
                text=f"🔔 ከአስተዳዳሪው የተላከ መልስ፦\n\n{message.text}"
            )
            await message.answer("✅ መልዕክትዎ ለሰራተኛው ተልኳል።")
        else:
            await message.answer("⚠️ ይቅርታ፣ መልዕክቱን ለማን መላክ እንዳለብኝ ማወቅ አልቻልኩም። (የUserID መረጃው በሪፖርቱ ላይ መኖሩን ያረጋግጡ)")
    except Exception as e:
        logging.error(f"Error in admin reply: {e}")
        await message.answer("❌ መልዕክቱን መላክ አልተቻለም።")

@dp.message(Command("report"))
async def cmd_report(message: types.Message):
    if str(message.chat.id) != str(ADMIN_CHAT_ID):
        await message.answer("ይቅርታ፣ ይህ ትዕዛዝ ለአስተዳዳሪ ብቻ የተፈቀደ ነው።")
        return
    
    if not all_reports:
        await message.answer("እስካሁን ምንም የተመዘገበ ሪፖርት የለም።")
        return
    
    final_report = "📋 የሰራተኞች አጠቃላይ ሪፖርት፦\n\n"
    for r in all_reports:
        final_report += f"👤 ስም: {r['full_name']}\n🛠 ኃላፊነት: {r['position']}\n🚩 ውሳኔ: {r['decision']}\n\n"
    
    await message.answer(final_report)

@dp.message(SurveyStates.waiting_for_full_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("በድርጅቱ ውስጥ ያለዎት የሥራ ኃላፊነት (Position) ምንድነው?")
    await state.set_state(SurveyStates.waiting_for_position)

@dp.message(SurveyStates.waiting_for_position)
async def process_position(message: types.Message, state: FSMContext):
    await state.update_data(position=message.text)
    await message.answer("በጋቶ ውስጥ በምን ዓይነት የሥራ ሁኔታ ላይ ይገኛሉ?", reply_markup=get_job_type_keyboard())
    await state.set_state(SurveyStates.waiting_for_job_type)

@dp.message(SurveyStates.waiting_for_job_type)
async def process_job_type(message: types.Message, state: FSMContext):
    if message.text not in ["🕒 የትርፍ ሰዓት (Part-time)", "📅 ሙሉ ሰዓት (Full-time)"]:
        await message.answer("እባክዎን ከተሰጡት አማራጮች ይምረጡ።")
        return
    await state.update_data(job_type=message.text)
    await message.answer("የሥራ ሰዓትዎ ከስንት እስከ ስንት ነው? (ለምሳሌ፦ 2:00 - 11:00)", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(SurveyStates.waiting_for_work_hours)

@dp.message(SurveyStates.waiting_for_work_hours)
async def process_hours(message: types.Message, state: FSMContext):
    await state.update_data(work_hours=message.text)
    await message.answer("ወደፊት መቀጠል ይፈልጋሉ ወይስ ማቋረጥ?", reply_markup=get_decision_keyboard())
    await state.set_state(SurveyStates.waiting_for_decision)

@dp.message(SurveyStates.waiting_for_decision)
async def process_decision(message: types.Message, state: FSMContext):
    if message.text not in ["✅ መቀጠል እፈልጋለሁ", "❌ ማቋረጥ እፈልጋለሁ"]:
        await message.answer("እባክዎን ከተሰጡት አማራጮች ይምረጡ።")
        return
    await state.update_data(decision=message.text)
    await message.answer("ለዚህ ውሳኔዎ ዋናው ምክንያትዎ ምንድነው?", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(SurveyStates.waiting_for_decision_reason)

@dp.message(SurveyStates.waiting_for_decision_reason)
async def process_decision_reason(message: types.Message, state: FSMContext):
    await state.update_data(decision_reason=message.text)
    await message.answer("ባለፈው የአሰራር ሂደታችን ላይ የታዘቧቸውን ድክመቶችና ያጋጠሙዎትን ችግሮች ካሉ ይግለጹልን፦")
    await state.set_state(SurveyStates.waiting_for_past_issues)

@dp.message(SurveyStates.waiting_for_past_issues)
async def process_past_issues(message: types.Message, state: FSMContext):
    await state.update_data(past_issues=message.text)
    await message.answer("እነዚህን ችግሮች ለመፍታትና የጋቶን ስራ ለማሳለጥ እንደ መፍትሔ ምን ቢደረግ ይሻላል ይላሉ? (የመፍትሔ ሃሳብዎን ያጋሩን)፦")
    await state.set_state(SurveyStates.waiting_for_solution)

@dp.message(SurveyStates.waiting_for_solution)
async def process_solution(message: types.Message, state: FSMContext):
    data = await state.get_data()
    solution = message.text
    user_id = message.from_user.id
    
    report_text = (
        f"📊 አዲስ ሪፖርት (ሙሉ ዝርዝር)\n"
        f"--------------------------\n"
        f"👤 ስም: {data['full_name']}\n"
        f"🛠 ኃላፊነት: {data['position']}\n"
        f"💼 ሁኔታ: {data['job_type']}\n"
        f"⏰ ሰዓት: {data['work_hours']}\n"
        f"🚩 ውሳኔ: {data['decision']}\n"
        f"❓ የውሳኔው ምክንያት: {data['decision_reason']}\n"
        f"📝 የታዩ ችግሮች: {data['past_issues']}\n"
        f"💡 የመፍትሔ ሃሳብ: {solution}\n"
        f"--------------------------\n"
        f"🆔 UserID: {user_id}" # ይህ ለመልስ መስጫ ወሳኝ ነው
    )
    
    data['solution'] = solution
    all_reports.append(data)
    
    try:
        await bot.send_message(ADMIN_CHAT_ID, report_text)
        await message.answer("በጣም እናመሰግናለን! የሰጡን መረጃ እና የመፍትሔ ሃሳብ ለጋቶ እድገት ትልቅ ግብዓት ነው።")
    except Exception as e:
        logging.error(f"Error: {e}")
        await message.answer("እናመሰግናለን! መረጃው ተመዝግቧል።")
    
    await state.clear()

async def main():
    while True:
        try:
            print("ጋቶ ቦት (Admin Reply Enabled) ስራ ጀምሯል...")
            await dp.start_polling(bot)
        except Exception as e:
            logging.error(f"Network error: {e}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())