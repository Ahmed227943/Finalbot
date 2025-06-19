#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
بوت تليجرام بردود خاصة مع إمكانية عمل تاك لجميع الأعضاء
"""

import logging
import asyncio
from telegram import Update, ChatMember
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import TelegramError
from config import BOT_TOKEN, CUSTOM_RESPONSES, SYSTEM_MESSAGES

# إعداد نظام السجلات
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.application = Application.builder().token(token).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """إعداد معالجات الأوامر والرسائل"""
        # معالجات الأوامر
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        
        # معالج الرسائل النصية
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # معالج أمر @all للتاك الجماعي
        self.application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"@all"), self.mention_all_command))
        
        # معالج الأعضاء الجدد
        self.application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, self.welcome_new_members))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالج أمر /start"""
        user = update.effective_user
        welcome_text = f"مرحباً {user.first_name}! 👋\n\n"
        welcome_text += "أنا بوت مساعد يمكنني:\n"
        welcome_text += "• الرد على رسائلك بردود خاصة\n"
        welcome_text += "• عمل تاك لجميع أعضاء المجموعة باستخدام @all\n"
        welcome_text += "• الدردشة معك\n\n"
        welcome_text += "استخدم /help لمعرفة المزيد من الأوامر"
        
        await update.message.reply_text(welcome_text)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالج أمر /help"""
        help_text = "📋 قائمة الأوامر المتاحة:\n\n"
        help_text += "/start - بدء المحادثة مع البوت\n"
        help_text += "/help - عرض هذه القائمة\n"
        help_text += "@all - عمل تاك لجميع الأعضاء\n\n"
        help_text += "💬 يمكنك أيضاً إرسال أي رسالة وسأرد عليك بردود خاصة!"
        
        await update.message.reply_text(help_text)
    
    async def mention_all_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالج أمر عمل تاك لجميع الأعضاء"""
        chat = update.effective_chat
        
        # التحقق من أن الأمر في مجموعة
        if chat.type == 'private':
            await update.message.reply_text(SYSTEM_MESSAGES["private_chat_only"])
            return
        
        try:
            # جلب قائمة الأعضاء
            members = []
            async for member in chat.get_members():
                if not member.user.is_bot and member.status != 'left':
                    if member.user.username:
                        members.append(f"@{member.user.username}")
                    else:
                        members.append(f"[{member.user.first_name}](tg://user?id={member.user.id})")
            
            if members:
                # تقسيم القائمة إلى مجموعات صغيرة لتجنب تجاوز حد الرسالة
                chunk_size = 50
                for i in range(0, len(members), chunk_size):
                    chunk = members[i:i + chunk_size]
                    mention_text = "📢 " + " ".join(chunk)
                    await update.message.reply_text(mention_text, parse_mode='Markdown')
                
                await update.message.reply_text(SYSTEM_MESSAGES["mention_all_success"])
            else:
                await update.message.reply_text("لم أجد أعضاء لعمل تاك لهم.")
                
        except TelegramError as e:
            logger.error(f"خطأ في عمل تاك للأعضاء: {e}")
            await update.message.reply_text(SYSTEM_MESSAGES["mention_all_error"])
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالج الرسائل النصية العادية"""
        message_text = update.message.text.lower().strip()
        
        # البحث عن رد مناسب في الردود الخاصة
        response = None
        for keyword, reply in CUSTOM_RESPONSES.items():
            if keyword in message_text:
                response = reply
                break
        
        # إذا لم يوجد رد مناسب، استخدم الرد الافتراضي
        if not response:
            response = SYSTEM_MESSAGES["default_response"]
        
        await update.message.reply_text(response)
    
    async def welcome_new_members(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """ترحيب بالأعضاء الجدد"""
        for member in update.message.new_chat_members:
            if not member.is_bot:
                welcome_text = f"مرحباً {member.first_name}! 🎉\n"
                welcome_text += SYSTEM_MESSAGES["welcome_group"]
                await update.message.reply_text(welcome_text)
    
    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE):
        """معالج الأخطاء"""
        logger.error(f"حدث خطأ: {context.error}")
    
    def run(self):
        """تشغيل البوت"""
        # إضافة معالج الأخطاء
        self.application.add_error_handler(self.error_handler)
        
        logger.info("بدء تشغيل البوت...")
        print("🤖 البوت يعمل الآن...")
        print("اضغط Ctrl+C لإيقاف البوت")
        
        # تشغيل البوت
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

def main():
    """الدالة الرئيسية"""
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ خطأ: يجب تعديل BOT_TOKEN في ملف config.py")
        print("احصل على التوكن من @BotFather في تليجرام")
        return
    
    bot = TelegramBot(BOT_TOKEN)
    try:
        bot.run()
    except KeyboardInterrupt:
        print("\n🛑 تم إيقاف البوت بواسطة المستخدم")
    except Exception as e:
        print(f"❌ خطأ في تشغيل البوت: {e}")

if __name__ == "__main__":
    main()

