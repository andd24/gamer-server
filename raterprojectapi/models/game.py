from django.db import models
from .rating import Rating

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
    
    @property
    def average_rating(self):
        """Average rating calculated attribute for each game"""
        ratings = Rating.objects.filter(game=self)

        # Sum all of the ratings for the game
        total_rating = 0
        for rating in ratings:
            total_rating += rating.rating
            
        avg = total_rating / len(ratings)
        return avg
        # Calculate the average and return it.
        # If you don't know how to calculate average, Google it.