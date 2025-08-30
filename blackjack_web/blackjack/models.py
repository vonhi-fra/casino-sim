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
    player_cards = models.JSONField()  # Lista kart gracza
    dealer_cards = models.JSONField()  # Lista kart dealera
    result = models.CharField(max_length=10)  # 'win', 'lose', 'draw'
    payout = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.player.nickname} - ${self.bet_amount} - {self.result}"