# استخدام Python 3.11 كصورة أساسية
FROM python:3.11-slim

# تعيين متغيرات البيئة
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# إنشاء مجلد العمل
WORKDIR /app

# نسخ ملف المتطلبات وتثبيتها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ ملفات البوت
COPY bot.py .
COPY config.py .

# إنشاء مستخدم غير جذر
RUN adduser --disabled-password --gecos '' botuser
RUN chown -R botuser:botuser /app
USER botuser

# تشغيل البوت
CMD ["python", "bot.py"]

