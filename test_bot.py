#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ملف اختبار للتأكد من عمل البوت بشكل صحيح
"""

import sys
import os

def test_imports():
    """اختبار استيراد المكتبات المطلوبة"""
    print("🔍 اختبار استيراد المكتبات...")
    
    try:
        import telegram
        print("✅ مكتبة telegram تم استيرادها بنجاح")
    except ImportError as e:
        print(f"❌ خطأ في استيراد مكتبة telegram: {e}")
        return False
    
    try:
        from telegram.ext import Application
        print("✅ مكتبة telegram.ext تم استيرادها بنجاح")
    except ImportError as e:
        print(f"❌ خطأ في استيراد telegram.ext: {e}")
        return False
    
    try:
        import asyncio
        print("✅ مكتبة asyncio تم استيرادها بنجاح")
    except ImportError as e:
        print(f"❌ خطأ في استيراد asyncio: {e}")
        return False
    
    return True

def test_config():
    """اختبار ملف الإعدادات"""
    print("\n🔍 اختبار ملف الإعدادات...")
    
    try:
        from config import BOT_TOKEN, CUSTOM_RESPONSES, SYSTEM_MESSAGES
        print("✅ ملف config.py تم استيراده بنجاح")
        
        if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
            print("⚠️  تحذير: لم يتم تعديل BOT_TOKEN في ملف config.py")
            print("   يجب الحصول على التوكن من @BotFather وتعديله في الملف")
        else:
            print("✅ تم تعديل BOT_TOKEN")
        
        print(f"✅ تم تحميل {len(CUSTOM_RESPONSES)} رد خاص")
        print(f"✅ تم تحميل {len(SYSTEM_MESSAGES)} رسالة نظام")
        
        return True
    except ImportError as e:
        print(f"❌ خطأ في استيراد ملف config.py: {e}")
        return False

def test_bot_class():
    """اختبار فئة البوت"""
    print("\n🔍 اختبار فئة البوت...")
    
    try:
        from bot import TelegramBot
        print("✅ فئة TelegramBot تم استيرادها بنجاح")
        
        # اختبار إنشاء كائن البوت (بدون تشغيل)
        test_token = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
        bot = TelegramBot(test_token)
        print("✅ تم إنشاء كائن البوت بنجاح")
        
        return True
    except Exception as e:
        print(f"❌ خطأ في اختبار فئة البوت: {e}")
        return False

def test_file_structure():
    """اختبار هيكل الملفات"""
    print("\n🔍 اختبار هيكل الملفات...")
    
    required_files = [
        "bot.py",
        "config.py", 
        "requirements.txt",
        "README.md"
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} موجود")
        else:
            print(f"❌ {file} غير موجود")
            all_exist = False
    
    return all_exist

def main():
    """الدالة الرئيسية للاختبار"""
    print("🚀 بدء اختبار بوت تليجرام")
    print("=" * 50)
    
    tests = [
        ("استيراد المكتبات", test_imports),
        ("ملف الإعدادات", test_config),
        ("فئة البوت", test_bot_class),
        ("هيكل الملفات", test_file_structure)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ فشل اختبار: {test_name}")
        except Exception as e:
            print(f"❌ خطأ في اختبار {test_name}: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 نتائج الاختبار: {passed}/{total} اختبار نجح")
    
    if passed == total:
        print("🎉 جميع الاختبارات نجحت! البوت جاهز للاستخدام")
        print("\n📝 الخطوات التالية:")
        print("1. احصل على توكن من @BotFather")
        print("2. عدّل BOT_TOKEN في ملف config.py")
        print("3. شغّل البوت بالأمر: python3 bot.py")
    else:
        print("⚠️  بعض الاختبارات فشلت. راجع الأخطاء أعلاه")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

