import random
from decimal import Decimal

class RouletteGame:
    def __init__(self):
        self.black_numbers = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
        self.red_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
        self.green_number = 0
        
    def get_bet_types(self):
        """Zwraca dostępne typy zakładów"""
        return {
            'red': {'name': 'Red', 'payout': 2, 'description': 'Red numbers'},
            'black': {'name': 'Black', 'payout': 2, 'description': 'Black numbers'},
            'first_half': {'name': '1-18', 'payout': 2, 'description': 'Numbers 1-18'},
            'second_half': {'name': '19-36', 'payout': 2, 'description': 'Numbers 19-36'},
            'even': {'name': 'Even', 'payout': 2, 'description': 'Even numbers'},
            'odd': {'name': 'Odd', 'payout': 2, 'description': 'Odd numbers'},
            'number': {'name': 'Single Number', 'payout': 36, 'description': 'Specific number (0-36)'}
        }
    
    def spin(self):
        """Wykonuje obrót ruletki"""
        return random.randint(0, 36)
    
    def get_number_color(self, number):
        """Zwraca kolor numeru"""
        if number == 0:
            return 'green'
        elif number in self.red_numbers:
            return 'red'
        else:
            return 'black'
    
    def check_bet(self, bet_type, bet_number, winning_number):
        """Sprawdza czy zakład wygrał"""
        if bet_type == 'red':
            return winning_number in self.red_numbers
        elif bet_type == 'black':
            return winning_number in self.black_numbers
        elif bet_type == 'first_half':
            return 1 <= winning_number <= 18
        elif bet_type == 'second_half':
            return 19 <= winning_number <= 36
        elif bet_type == 'even':
            return winning_number != 0 and winning_number % 2 == 0
        elif bet_type == 'odd':
            return winning_number != 0 and winning_number % 2 == 1
        elif bet_type == 'number':
            return winning_number == int(bet_number)
        
        return False
    
    def calculate_payout(self, bet_amount, bet_type, won):
        """Oblicza wypłatę"""
        if not won:
            return Decimal('0')
        
        bet_types = self.get_bet_types()
        multiplier = bet_types.get(bet_type, {}).get('payout', 1)
        return Decimal(str(bet_amount)) * multiplier
    
    def play_round(self, bets_data):
        """
        Gra rundę ruletki z wieloma zakładami
        bets_data: lista słowników [{'type': 'red', 'amount': 100, 'number': None}, ...]
        """
        winning_number = self.spin()
        winning_color = self.get_number_color(winning_number)
        
        results = []
        total_payout = Decimal('0')
        
        for bet in bets_data:
            bet_type = bet['type']
            bet_amount = Decimal(str(bet['amount']))
            bet_number = bet.get('number')
            
            won = self.check_bet(bet_type, bet_number, winning_number)
            payout = self.calculate_payout(bet_amount, bet_type, won)
            
            results.append({
                'type': bet_type,
                'amount': bet_amount,
                'number': bet_number,
                'won': won,
                'payout': payout
            })
            
            total_payout += payout
        
        return {
            'winning_number': winning_number,
            'winning_color': winning_color,
            'bet_results': results,
            'total_payout': total_payout,
            'total_bet': sum(Decimal(str(bet['amount'])) for bet in bets_data)
        }