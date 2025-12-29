from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from raiting_system.models import Rating, Medal


class Result(models.Model):
    """
    Модель для хранения результатов олимпиад.
    """
    PARTICIPANT = 'У'
    PRIZE = 'ПР'
    WINNER = 'ПОБД'

    STATUSRES = [
        (PARTICIPANT, 'Участник'),
        (PRIZE, 'Призер'),
        (WINNER, 'Победитель')
    ]

    info_children = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        verbose_name='Информация об ученике',
        related_name='results'
    )
    info_olympiad = models.ForeignKey(
        'main.Olympiad',
        on_delete=models.CASCADE,
        verbose_name='Информация об олимпиаде'
    )
    points = models.PositiveIntegerField(
        verbose_name='Количество набранных очков',
        blank=True,
        null=True
    )
    status_result = models.CharField(
        verbose_name='Статус результата',
        max_length=256,
        choices=STATUSRES,
        default=PARTICIPANT
    )
    advanced = models.BooleanField(default=False, verbose_name='Прошел на следующий этап')
    date_added = models.DateTimeField(auto_now_add=True)
    school = models.ForeignKey(
        'school.School',
        on_delete=models.CASCADE,
        verbose_name='Школа'
    )
    notified = models.BooleanField(default=False, verbose_name='Уведомление отправлено')

    def __str__(self):
        """
        Строковое представление результата.
        """
        return f'{self.info_children.get_full_name()} - {self.info_olympiad.name} - {self.points} очков'

    def save(self, *args, **kwargs):
        """
        Переопределение метода save для обновления рейтинга пользователя после сохранения результата.
        """
        super().save(*args, **kwargs)
        self.update_user_rating()

    def update_user_rating(self):
        """
        Обновление рейтинга пользователя и добавление медалей в зависимости от результата и этапа олимпиады.
        """
        if not self.info_olympiad or not self.info_olympiad.stage:
            return

        stage_points = {
            'Школьный': {self.WINNER: (100, Medal.SILVER), self.PRIZE: (50, Medal.BRONZE)},
            'Городской': {self.WINNER: (450, Medal.PLATINUM), self.PRIZE: (300, Medal.GOLD)},
            'Региональный': {self.WINNER: (1000, Medal.RUBY), self.PRIZE: (450, Medal.PLATINUM)},
            'Заключительный': {self.WINNER: (6000, Medal.PERSONAL), self.PRIZE: (3000, Medal.DIAMOND)},
        }

        stage_name = self.info_olympiad.stage.name
        points, medal_type = stage_points.get(stage_name, {}).get(self.status_result, (0, None))

        # Обновляем рейтинг
        rating, _ = Rating.objects.get_or_create(user=self.info_children)
        rating.update_points(points)

        # Добавляем медаль, если требуется
        if medal_type:
            Medal.objects.create(
                type=medal_type,
                olympiad=self.info_olympiad,
                user=self.info_children
            )
