from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    year_released = models.IntegerField()
    number_of_players = models.IntegerField()
    estimated_time_to_play = models.IntegerField()
    age_recommendation = models.IntegerField()
    designer = models.CharField(max_length=50)
    player = models.ForeignKey("Player", on_delete=models.CASCADE)
    categories =  models.ManyToManyField("Category", through="GameCategory", related_name="categories")