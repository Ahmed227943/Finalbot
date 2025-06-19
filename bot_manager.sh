#!/bin/bash
# سكريبت تشغيل البوت بشكل مستمر

# اسم البوت
BOT_NAME="telegram_bot"
BOT_DIR="/home/ubuntu/telegram_bot"
BOT_FILE="bot.py"
PID_FILE="/tmp/${BOT_NAME}.pid"
LOG_FILE="/tmp/${BOT_NAME}.log"

# دالة بدء البوت
start_bot() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            echo "البوت يعمل بالفعل (PID: $PID)"
            return 1
        else
            rm -f "$PID_FILE"
        fi
    fi
    
    echo "بدء تشغيل البوت..."
    cd "$BOT_DIR"
    nohup python3 "$BOT_FILE" > "$LOG_FILE" 2>&1 &
    echo $! > "$PID_FILE"
    echo "تم بدء البوت (PID: $(cat $PID_FILE))"
    echo "لمراقبة السجلات: tail -f $LOG_FILE"
}

# دالة إيقاف البوت
stop_bot() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            echo "إيقاف البوت (PID: $PID)..."
            kill $PID
            rm -f "$PID_FILE"
            echo "تم إيقاف البوت"
        else
            echo "البوت غير مُشغل"
            rm -f "$PID_FILE"
        fi
    else
        echo "البوت غير مُشغل"
    fi
}

# دالة إعادة تشغيل البوت
restart_bot() {
    stop_bot
    sleep 2
    start_bot
}

# دالة فحص حالة البوت
status_bot() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            echo "البوت يعمل (PID: $PID)"
            echo "وقت التشغيل: $(ps -o etime= -p $PID)"
        else
            echo "البوت متوقف (ملف PID موجود لكن العملية غير موجودة)"
            rm -f "$PID_FILE"
        fi
    else
        echo "البوت متوقف"
    fi
}

# دالة عرض السجلات
logs_bot() {
    if [ -f "$LOG_FILE" ]; then
        tail -f "$LOG_FILE"
    else
        echo "ملف السجلات غير موجود"
    fi
}

# معالجة الأوامر
case "$1" in
    start)
        start_bot
        ;;
    stop)
        stop_bot
        ;;
    restart)
        restart_bot
        ;;
    status)
        status_bot
        ;;
    logs)
        logs_bot
        ;;
    *)
        echo "الاستخدام: $0 {start|stop|restart|status|logs}"
        echo ""
        echo "الأوامر:"
        echo "  start   - بدء تشغيل البوت"
        echo "  stop    - إيقاف البوت"
        echo "  restart - إعادة تشغيل البوت"
        echo "  status  - فحص حالة البوت"
        echo "  logs    - عرض سجلات البوت"
        exit 1
        ;;
esac

