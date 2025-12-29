from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import League, Medal, Rating, PersonalMedal
from .serializers import LeagueSerializer, MedalSerializer, RatingSerializer, PersonalMedalSerializer
from users.models import User


class LeagueViewSet(ModelViewSet):
    """
    ViewSet для управления лигами.
    """
    queryset = League.objects.all()
    serializer_class = LeagueSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='by-points/(?P<points>\d+)')
    def get_league_by_points(self, request, points=None):
        """
        Пользовательский метод для получения лиги по количеству очков.
        """
        try:
            points = int(points)
            league_type = League.get_league_for_points(points)
            league = League.objects.get(type=league_type)
            serializer = self.get_serializer(league)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except League.DoesNotExist:
            return Response({'detail': 'Лига не найдена.'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({'detail': 'Неверный формат очков.'}, status=status.HTTP_400_BAD_REQUEST)


class MedalViewSet(ModelViewSet):
    """
    ViewSet для управления медалями.
    """
    queryset = Medal.objects.select_related('user', 'olympiad').all()
    serializer_class = MedalSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>\d+)')
    def get_medals_by_user(self, request, user_id=None):
        """
        Пользовательский метод для получения медалей конкретного пользователя.
        """
        try:
            user = User.objects.get(id=user_id)
            medals = self.queryset.filter(user=user)
            serializer = self.get_serializer(medals, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'detail': 'Пользователь не найден.'}, status=status.HTTP_404_NOT_FOUND)


class RatingViewSet(ModelViewSet):
    """
    ViewSet для управления рейтингами.
    """
    queryset = Rating.objects.select_related('user').all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>\d+)')
    def get_rating_by_user(self, request, user_id=None):
        """
        Пользовательский метод для получения рейтинга пользователя.
        """
        try:
            user = User.objects.get(id=user_id)
            rating = self.queryset.get(user=user)
            serializer = self.get_serializer(rating)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'detail': 'Пользователь не найден.'}, status=status.HTTP_404_NOT_FOUND)
        except Rating.DoesNotExist:
            return Response({'detail': 'Рейтинг для пользователя не найден.'}, status=status.HTTP_404_NOT_FOUND)


class PersonalMedalViewSet(ModelViewSet):
    """
    ViewSet для управления именными медалями.
    """
    queryset = PersonalMedal.objects.select_related('user').all()
    serializer_class = PersonalMedalSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>\d+)')
    def get_personal_medals_by_user(self, request, user_id=None):
        """
        Пользовательский метод для получения именных медалей конкретного пользователя.
        """
        try:
            user = User.objects.get(id=user_id)
            personal_medals = self.queryset.filter(user=user)
            serializer = self.get_serializer(personal_medals, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'detail': 'Пользователь не найден.'}, status=status.HTTP_404_NOT_FOUND)
