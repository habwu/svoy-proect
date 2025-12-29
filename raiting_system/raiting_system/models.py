from django.db import models
from users.models import User
from main.models import Olympiad


class League(models.Model):
    """Модель лиги с диапазоном очков и типами лиг"""
    BRONZE = 'bronze'
    SILVER = 'silver'
    GOLD = 'gold'
    PLATINUM = 'platinum'
    RUBY = 'ruby'
    DIAMOND = 'diamond'
    TOP_250 = 'top_250'

    LEAGUE_TYPES = [
        (BRONZE, 'Бронзовая лига (0-150 очков)'),
        (SILVER, 'Серебряная лига (151-500 очков)'),
        (GOLD, 'Золотая лига (501-1000 очков)'),
        (PLATINUM, 'Платиновая лига (1001-2000 очков)'),
        (RUBY, 'Рубиновая лига (2001-3500 очков)'),
        (DIAMOND, 'Алмазная лига (3501+ очков)'),
        (TOP_250, 'ТОП-250'),
    ]

    type = models.CharField('Тип лиги', max_length=20, choices=LEAGUE_TYPES, unique=True)
    min_points = models.IntegerField('Минимальные очки')
    max_points = models.IntegerField('Максимальные очки', blank=True, null=True)

    def __str__(self):
        return self.get_type_display()

    @staticmethod
    def get_league_for_points(points):
        """Возвращает тип лиги в зависимости от количества очков"""
        for league in League.objects.all():
            if league.min_points <= points and (league.max_points is None or points <= league.max_points):
                return league.type
        return None


class Medal(models.Model):
    """Модель медали, связанная с пользователем и олимпиадой"""
    BRONZE = 'bronze'
    SILVER = 'silver'
    GOLD = 'gold'
    PLATINUM = 'platinum'
    DIAMOND = 'diamond'
    RUBY = 'ruby'
    PERSONAL = 'personal'

    MEDAL_TYPES = [
        (BRONZE, 'Бронзовая'),
        (SILVER, 'Серебряная'),
        (GOLD, 'Золотая'),
        (PLATINUM, 'Платиновая'),
        (DIAMOND, 'Алмазная'),
        (RUBY, 'Рубиновая'),
        (PERSONAL, 'Именная'),
    ]

    type = models.CharField('Тип медали', max_length=20, choices=MEDAL_TYPES)
    olympiad = models.ForeignKey(Olympiad, on_delete=models.SET_NULL, null=True, verbose_name='Олимпиада')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return f'{self.get_type_display()} - {self.user} - {self.olympiad}'


class Rating(models.Model):
    """Модель рейтинга пользователя с очками и лигой"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='rating', verbose_name='Пользователь')
    points = models.IntegerField('Очки', default=0)
    league = models.CharField('Лига', max_length=20, choices=League.LEAGUE_TYPES, blank=True, null=True)

    def __str__(self):
        return f'{self.user.get_full_name()} - {self.points} очков - {self.get_league_display()}'

    def update_points(self, additional_points):
        """Обновляет очки пользователя и пересчитывает его лигу"""
        self.points += additional_points
        self.league = League.get_league_for_points(self.points)
        self.save()


class PersonalMedal(models.Model):
    """Модель именной медали, связанная с пользователем"""
    name = models.CharField('Название медали', max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    date_awarded = models.DateField('Дата вручения', auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.user.get_full_name()}'
