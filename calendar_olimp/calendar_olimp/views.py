from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from main.models import Olympiad
from .serializers import OlympiadSerializer

class OlympiadViewSet(ReadOnlyModelViewSet):
    """
    ViewSet для предоставления данных по олимпиадам.
    """
    queryset = Olympiad.objects.all()
    serializer_class = OlympiadSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """
        Переопределение метода list для предоставления данных в формате событий для календаря.
        """
        queryset = self.get_queryset()
        serialized_data = []

        for olympiad in queryset:
            if olympiad.date:
                serialized_data.append({
                    'title': olympiad.name,
                    'start': olympiad.date.strftime('%Y-%m-%dT%H:%M:%S'),
                    'description': olympiad.description,
                    'location':olympiad.location,
                })

        return Response(serialized_data)