from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Result
from django.conf import settings
from asgiref.sync import async_to_sync
import requests
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Result)
def send_result_notification(sender, instance, created, **kwargs):
    """
    Сигнал для отправки уведомления о результате после его создания.
    """
    if created and not instance.notified:
        student = instance.info_children
        olympiad = instance.info_olympiad
        points = instance.points
        status = instance.get_status_result_display()

        # Создание сообщения
        message = (
            f"👋 *Здравствуйте, {student.get_full_name()}!*\n\n"
            f"🎓 *Ваш результат по олимпиаде «{olympiad.name}»*:\n"
            f"✨ *Этап*: {olympiad.stage.name}\n"
            f"📝 *Статус*: {status}\n"
            f"🏆 *Набранные очки*: {points}\n\n"
            f"Спасибо за участие и желаем успехов в следующих соревнованиях! 😊"
        )

        # Отправка сообщения через Telegram
        if student.telegram_id:
            try:
                async_to_sync(send_message_via_telegram)(student.telegram_id, message)
            except Exception as e:
                logger.error(f"Ошибка при отправке уведомления в Telegram: {e}")
        else:
            logger.warning(f"Ученик {student.get_full_name()} не имеет Telegram ID.")

        # Обновление статуса уведомления
        instance.notified = True
        instance.save(update_fields=['notified'])


async def send_message_via_telegram(chat_id, message):
    """
    Асинхронная отправка сообщения через Telegram.
    """
    token = settings.TELEGRAM_BOT_TOKEN
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Ошибка отправки сообщения в Telegram: {e}")
