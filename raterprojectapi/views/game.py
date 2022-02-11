from django.forms import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from raterprojectapi.models import Game, Player, Rating

class GameView(ViewSet):
    def retrieve(self, request, pk):
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
    def list(self, request):
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        player = Player.objects.get(user=request.auth.user)
        try:
            serializer = CreateGameSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            game = serializer.save(player=player)
            game.categories.add(request.data['category'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, pk):
        try:
            game = Game.objects.get(pk=pk)
            serializer = CreateGameSerializer(game, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk):
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'title', 'description', 'year_released', 'number_of_players', 'estimated_time_to_play', 'age_recommendation', 'designer', 'player', 'categories', 'average_rating')
        depth = 2

class CreateGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['title', 'description', 'year_released', 'number_of_players', 'estimated_time_to_play', 'age_recommendation', 'designer']