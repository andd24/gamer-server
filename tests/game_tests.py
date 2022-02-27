import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from raterprojectapi.models import Game, Category, Player
from raterprojectapi.models.game_category import GameCategory


class GameTests(APITestCase):
    def setUp(self):
        url = '/register'

        player = {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@stevebrownlee.com",
            "address": "100 Infinity Way",
            "phone_number": "555-1212",
            "first_name": "Steve",
            "last_name": "Brownlee",
            "name": "Stevie"
        }

        response = self.client.post(url, player, format='json')

        self.token = Token.objects.get(pk=response.data['token'])

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.game = Game()
        self.game.player_id = 1
        self.game.title = "Sorry"
        self.game.description = "sorrys a board game"
        self.game.year_released = 2005
        self.game.number_of_players = 4
        self.game.estimated_time_to_play = 1
        self.game.age_recommendation = 7
        self.game.designer = "Milt Brad"

        # Save the Game to the testing database
        self.game.save()
        
    def test_create_game(self):
        """Create game test"""
        url = "/games"

        # Define the Game properties
        game = {
            "title": "Clue",
            "description": "whodunnit",
            "year_released": 2000,
            "number_of_players": 6,
            "estimated_time_to_play": 2,
            "age_recommendation": 9,
            "designer": "Mike Scott",
            "categories": 1
        }

        response = self.client.post(url, game, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # self.assertEqual(response.data["gamer"]["user"], self.token.user_id)
        self.assertEqual(response.data["title"], game['title'])
        self.assertEqual(response.data["description"], game['description'])
        self.assertEqual(response.data["year_released"], game['year_released'])
        self.assertEqual(
            response.data["number_of_players"], game['number_of_players'])
        self.assertEqual(response.data['estimated_time_to_play'], game['estimated_time_to_play'])
        self.assertEqual(response.data['age_recommendation'], game['age_recommendation'])
        self.assertEqual(response.data['designer'], game['designer'])
    
    def test_get_game(self):
        """Get Game Test
        """
        game = Game()
        game.player_id = 1
        game.title = "Sorry"
        game.description = "sorrys a board game"
        game.year_released = 2005
        game.number_of_players = 4
        game.estimated_time_to_play = 1
        game.age_recommendation = 7
        game.designer = "Milt Brad"
        game.save()

        url = f'/games/{game.id}'

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(response.data["title"], game.title)
        self.assertEqual(response.data["description"], game.description)
        self.assertEqual(response.data["year_released"], game.year_released)
        self.assertEqual(
            response.data["number_of_players"], game.number_of_players)
        self.assertEqual(response.data["estimated_time_to_play"], game.estimated_time_to_play)
        self.assertEqual(response.data["age_recommendation"], game.age_recommendation)
        self.assertEqual(response.data["designer"], game.designer)
    
    def test_change_game(self):
        """test update game"""
        game = Game()
        game.player_id = 1
        game.title = "Sorry"
        game.description = "sorrys a board game"
        game.year_released = 2005
        game.number_of_players = 4
        game.estimated_time_to_play = 1
        game.age_recommendation = 7
        game.designer = "Milt Brad"

        # Save the Game to the testing database
        game.save()

        url = f'/games/{game.id}'

        new_game = {
            "title": "Sorry",
            "description": "sorrys a board game",
            "year_released": 1980,
            "number_of_players": 4,
            "estimated_time_to_play": 1,
            "age_recommendation": 7,
            "designer": "Milt Brad"
        }

        response = self.client.put(url, new_game, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(response.data['player']['id'], self.token.user_id)
        self.assertEqual(response.data["title"], new_game['title'])
        self.assertEqual(response.data["description"], new_game['description'])
        self.assertEqual(
            response.data["year_released"], new_game['year_released'])
        self.assertEqual(
            response.data["number_of_players"], new_game['number_of_players'])
        self.assertEqual(response.data["estimated_time_to_play"], new_game['estimated_time_to_play'])
        self.assertEqual(response.data["age_recommendation"], new_game['age_recommendation'])
        self.assertEqual(response.data['designer'], new_game['designer'])        
        
    def test_delete_game(self):
        """Test delete game"""

        url = f'/games/{self.game.id}'
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)