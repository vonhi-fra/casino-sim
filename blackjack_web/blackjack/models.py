from django.db import models

class Player(models.Model):
    nickname = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=10000)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nickname} (${self.balance})"

class Game(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    bet_amount = models.DecimalField(max_digits=8, decimal_places=2)
    player_cards = models.JSONField()
    dealer_cards = models.JSONField()
    result = models.CharField(max_length=10)
    payout = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.player.nickname} - ${self.bet_amount} - {self.result}"
    
class RouletteGameModel(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    total_bet = models.DecimalField(max_digits=8, decimal_places=2)
    winning_number = models.IntegerField()
    winning_color = models.CharField(max_length=10)
    total_payout = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    bets_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.player.nickname} - Roulette - ${self.total_bet} - Number: {self.winning_number}"

class RouletteBet(models.Model):
    game = models.ForeignKey(RouletteGameModel, on_delete=models.CASCADE)
    bet_type = models.CharField(max_length=20)
    bet_amount = models.DecimalField(max_digits=8, decimal_places=2)
    bet_number = models.IntegerField(null=True, blank=True)
    won = models.BooleanField(default=False)
    payout = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    
    def __str__(self):
        return f"{self.bet_type} - ${self.bet_amount} - Won: {self.won}"