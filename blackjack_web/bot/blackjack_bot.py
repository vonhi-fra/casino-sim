# blackjack_web/bot/blackjack_bot.py

class BlackjackBot:
    """
    Bot grający matematycznie optymalną strategią w blackjacka (Basic Strategy).
    Strategia oparta na probabilistycznych kalkulacjach dla standardowej talii kart.
    """
    
    def __init__(self):
        # Hard totals strategy (bez asów liczonych jako 11)
        self.hard_strategy = {
            # Suma gracza: {karta dealera: akcja}
            5: {2: 'hit', 3: 'hit', 4: 'hit', 5: 'hit', 6: 'hit', 7: 'hit', 8: 'hit', 9: 'hit', 10: 'hit', 11: 'hit'},
            6: {2: 'hit', 3: 'hit', 4: 'hit', 5: 'hit', 6: 'hit', 7: 'hit', 8: 'hit', 9: 'hit', 10: 'hit', 11: 'hit'},
            7: {2: 'hit', 3: 'hit', 4: 'hit', 5: 'hit', 6: 'hit', 7: 'hit', 8: 'hit', 9: 'hit', 10: 'hit', 11: 'hit'},
            8: {2: 'hit', 3: 'hit', 4: 'hit', 5: 'hit', 6: 'hit', 7: 'hit', 8: 'hit', 9: 'hit', 10: 'hit', 11: 'hit'},
            9: {2: 'hit', 3: 'double', 4: 'double', 5: 'double', 6: 'double', 7: 'hit', 8: 'hit', 9: 'hit', 10: 'hit', 11: 'hit'},
            10: {2: 'double', 3: 'double', 4: 'double', 5: 'double', 6: 'double', 7: 'double', 8: 'double', 9: 'double', 10: 'hit', 11: 'hit'},
            11: {2: 'double', 3: 'double', 4: 'double', 5: 'double', 6: 'double', 7: 'double', 8: 'double', 9: 'double', 10: 'double', 11: 'double'},
            12: {2: 'hit', 3: 'hit', 4: 'stand', 5: 'stand', 6: 'stand', 7: 'hit', 8: 'hit', 9: 'hit', 10: 'hit', 11: 'hit'},
            13: {2: 'stand', 3: 'stand', 4: 'stand', 5: 'stand', 6: 'stand', 7: 'hit', 8: 'hit', 9: 'hit', 10: 'hit', 11: 'hit'},
            14: {2: 'stand', 3: 'stand', 4: 'stand', 5: 'stand', 6: 'stand', 7: 'hit', 8: 'hit', 9: 'hit', 10: 'hit', 11: 'hit'},
            15: {2: 'stand', 3: 'stand', 4: 'stand', 5: 'stand', 6: 'stand', 7: 'hit', 8: 'hit', 9: 'hit', 10: 'hit', 11: 'hit'},
            16: {2: 'stand', 3: 'stand', 4: 'stand', 5: 'stand', 6: 'stand', 7: 'hit', 8: 'hit', 9: 'hit', 10: 'hit', 11: 'hit'},
            17: {2: 'stand', 3: 'stand', 4: 'stand', 5: 'stand', 6: 'stand', 7: 'stand', 8: 'stand', 9: 'stand', 10: 'stand', 11: 'stand'},
            18: {2: 'stand', 3: 'stand', 4: 'stand', 5: 'stand', 6: 'stand', 7: 'stand', 8: 'stand', 9: 'stand', 10: 'stand', 11: 'stand'},
            19: {2: 'stand', 3: 'stand', 4: 'stand', 5: 'stand', 6: 'stand', 7: 'stand', 8: 'stand', 9: 'stand', 10: 'stand', 11: 'stand'},
            20: {2: 'stand', 3: 'stand', 4: 'stand', 5: 'stand', 6: 'stand', 7: 'stand', 8: 'stand', 9: 'stand', 10: 'stand', 11: 'stand'},
            21: {2: 'stand', 3: 'stand', 4: 'stand', 5: 'stand', 6: 'stand', 7: 'stand', 8: 'stand', 9: 'stand', 10: 'stand', 11: 'stand'},
        }
        
        # Soft totals strategy (z asem liczonym jako 11)
        self.soft_strategy = {
            # Suma gracza: {karta dealera: akcja}
            13: {2: 'hit', 3: 'hit', 4: 'hit', 5: 'double', 6: 'double', 7: 'hit', 8: 'hit', 9: 'hit', 10: 'hit', 11: 'hit'},  # A,2
            14: {2: 'hit', 3: 'hit', 4: 'hit', 5: 'double', 6: 'double', 7: 'hit', 8: 'hit', 9: 'hit', 10: 'hit', 11: 'hit'},  # A,3
            15: {2: 'hit', 3: 'hit', 4: 'double', 5: 'double', 6: 'double', 7: 'hit', 8: 'hit', 9: 'hit', 10: 'hit', 11: 'hit'},  # A,4
            16: {2: 'hit', 3: 'hit', 4: 'double', 5: 'double', 6: 'double', 7: 'hit', 8: 'hit', 9: 'hit', 10: 'hit', 11: 'hit'},  # A,5
            17: {2: 'hit', 3: 'double', 4: 'double', 5: 'double', 6: 'double', 7: 'hit', 8: 'hit', 9: 'hit', 10: 'hit', 11: 'hit'},  # A,6
            18: {2: 'stand', 3: 'double', 4: 'double', 5: 'double', 6: 'double', 7: 'stand', 8: 'stand', 9: 'hit', 10: 'hit', 11: 'hit'},  # A,7
            19: {2: 'stand', 3: 'stand', 4: 'stand', 5: 'stand', 6: 'stand', 7: 'stand', 8: 'stand', 9: 'stand', 10: 'stand', 11: 'stand'},  # A,8
            20: {2: 'stand', 3: 'stand', 4: 'stand', 5: 'stand', 6: 'stand', 7: 'stand', 8: 'stand', 9: 'stand', 10: 'stand', 11: 'stand'},  # A,9
            21: {2: 'stand', 3: 'stand', 4: 'stand', 5: 'stand', 6: 'stand', 7: 'stand', 8: 'stand', 9: 'stand', 10: 'stand', 11: 'stand'},  # A,10
        }
        
        # Pairs strategy
        self.pairs_strategy = {
            # Para: {karta dealera: akcja}
            'A,A': {2: 'split', 3: 'split', 4: 'split', 5: 'split', 6: 'split', 7: 'split', 8: 'split', 9: 'split', 10: 'split', 11: 'split'},
            '2,2': {2: 'split', 3: 'split', 4: 'split', 5: 'split', 6: 'split', 7: 'split', 8: 'hit', 9: 'hit', 10: 'hit', 11: 'hit'},
            '3,3': {2: 'split', 3: 'split', 4: 'split', 5: 'split', 6: 'split', 7: 'split', 8: 'hit', 9: 'hit', 10: 'hit', 11: 'hit'},
            '4,4': {2: 'hit', 3: 'hit', 4: 'hit', 5: 'split', 6: 'split', 7: 'hit', 8: 'hit', 9: 'hit', 10: 'hit', 11: 'hit'},
            '5,5': {2: 'double', 3: 'double', 4: 'double', 5: 'double', 6: 'double', 7: 'double', 8: 'double', 9: 'double', 10: 'hit', 11: 'hit'},
            '6,6': {2: 'split', 3: 'split', 4: 'split', 5: 'split', 6: 'split', 7: 'hit', 8: 'hit', 9: 'hit', 10: 'hit', 11: 'hit'},
            '7,7': {2: 'split', 3: 'split', 4: 'split', 5: 'split', 6: 'split', 7: 'split', 8: 'hit', 9: 'hit', 10: 'hit', 11: 'hit'},
            '8,8': {2: 'split', 3: 'split', 4: 'split', 5: 'split', 6: 'split', 7: 'split', 8: 'split', 9: 'split', 10: 'split', 11: 'split'},
            '9,9': {2: 'split', 3: 'split', 4: 'split', 5: 'split', 6: 'split', 7: 'stand', 8: 'split', 9: 'split', 10: 'stand', 11: 'stand'},
            '10,10': {2: 'stand', 3: 'stand', 4: 'stand', 5: 'stand', 6: 'stand', 7: 'stand', 8: 'stand', 9: 'stand', 10: 'stand', 11: 'stand'},
        }

    def normalize_card_value(self, card_str):
        """Konwertuje reprezentację karty na wartość numeryczną"""
        # Wyciąga symbol karty (usuwa kolor)
        symbol = card_str[0] if len(card_str) > 1 else card_str
        
        if symbol == 'A':
            return 11  # As
        elif symbol in ['J', 'Q', 'K']:
            return 10  # Figury
        else:
            try:
                return int(symbol) if len(symbol) == 1 else int(card_str[:-1])
            except:
                return 10  # Domyślnie 10 w przypadku błędu

    def calculate_hand_value(self, cards):
        """Oblicza wartość ręki z prawidłowym traktowaniem asów"""
        total = 0
        aces = 0
        
        for card in cards:
            value = self.normalize_card_value(card)
            if value == 11:  # As
                aces += 1
                total += 11
            else:
                total += value
        
        # Konwertuj asy z 11 na 1 jeśli potrzeba
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
            
        return total, aces > 0  # (wartość, czy ma soft ace)

    def is_pair(self, cards):
        """Sprawdza czy ręka to para"""
        if len(cards) != 2:
            return False
        
        card1_symbol = cards[0][0] if len(cards[0]) > 1 else cards[0]
        card2_symbol = cards[1][0] if len(cards[1]) > 1 else cards[1]
        
        # Normalizuj figury do 10
        if card1_symbol in ['J', 'Q', 'K']:
            card1_symbol = '10'
        if card2_symbol in ['J', 'Q', 'K']:
            card2_symbol = '10'
            
        return card1_symbol == card2_symbol

    def get_pair_key(self, cards):
        """Zwraca klucz dla pary"""
        card1_symbol = cards[0][0] if len(cards[0]) > 1 else cards[0]
        card2_symbol = cards[1][0] if len(cards[1]) > 1 else cards[1]
        
        # Normalizuj figury
        if card1_symbol in ['J', 'Q', 'K']:
            card1_symbol = '10'
        if card2_symbol in ['J', 'Q', 'K']:
            card2_symbol = '10'
        
        return f"{card1_symbol},{card2_symbol}"

    def get_optimal_action(self, player_cards, dealer_up_card, can_double=True, can_split=True, player_balance=0, current_bet=0):
        """
        Zwraca optymalną akcję według Basic Strategy
        
        Args:
            player_cards: lista kart gracza (np. ['A♠', '5♥'])
            dealer_up_card: widoczna karta dealera (np. '6♣')
            can_double: czy można dublować
            can_split: czy można splitować
            player_balance: saldo gracza (do sprawdzenia czy stać na split/double)
            current_bet: obecny zakład
        
        Returns:
            str: 'hit', 'stand', 'double', 'split'
        """
        
        # Normalizuj kartę dealera
        dealer_value = self.normalize_card_value(dealer_up_card)
        if dealer_value == 11:  # As dealera
            dealer_value = 11
        elif dealer_value > 10:
            dealer_value = 10
        
        player_total, has_soft_ace = self.calculate_hand_value(player_cards)
        
        # 1. Sprawdź czy to para i czy można splitować
        if can_split and len(player_cards) == 2 and self.is_pair(player_cards):
            # Sprawdź czy gracza stać na split
            if player_balance >= current_bet:
                pair_key = self.get_pair_key(player_cards)
                if pair_key in self.pairs_strategy:
                    action = self.pairs_strategy[pair_key].get(dealer_value, 'hit')
                    if action == 'split':
                        return 'split'
        
        # 2. Sprawdź soft totals (z asem jako 11)
        if has_soft_ace and player_total <= 21:
            if player_total in self.soft_strategy:
                action = self.soft_strategy[player_total].get(dealer_value, 'hit')
                # Sprawdź czy można wykonać akcję
                if action == 'double' and can_double and player_balance >= current_bet:
                    return 'double'
                elif action == 'double':
                    return 'hit'  # Jeśli nie można dublować, to hit
                else:
                    return action
        
        # 3. Hard totals
        if player_total in self.hard_strategy:
            action = self.hard_strategy[player_total].get(dealer_value, 'hit')
            # Sprawdź czy można wykonać akcję
            if action == 'double' and can_double and player_balance >= current_bet:
                return 'double'
            elif action == 'double':
                return 'hit'  # Jeśli nie można dublować, to hit
            else:
                return action
        
        # 4. Domyślne akcje dla wartości spoza tabeli
        if player_total >= 17:
            return 'stand'
        else:
            return 'hit'

    def get_betting_strategy(self, balance, min_bet=100, max_bet=1000):
        """
        Prosta strategia zakładów - stały procent balansu
        
        Args:
            balance: aktualny balans
            min_bet: minimalny zakład
            max_bet: maksymalny zakład
            
        Returns:
            int: kwota zakładu
        """
        # Stawiaj 2% balansu, ale nie mniej niż min_bet i nie więcej niż max_bet
        bet = max(min_bet, min(max_bet, int(balance * 0.02)))
        return min(bet, balance)  # Nie stawiaj więcej niż masz

    def explain_decision(self, player_cards, dealer_up_card, action, player_balance=0, current_bet=0):
        """
        Wyjaśnia dlaczego bot wybrał daną akcję
        
        Returns:
            str: wyjaśnienie decyzji
        """
        dealer_value = self.normalize_card_value(dealer_up_card)
        player_total, has_soft_ace = self.calculate_hand_value(player_cards)
        
        explanations = {
            'hit': f"Dobrać kartę - suma {player_total} przeciwko {dealer_value} dealera",
            'stand': f"Pas - suma {player_total} jest wystarczająca przeciwko {dealer_value} dealera",
            'double': f"Dublować - suma {player_total} ma dobrą szansę na wygraną po jednej karcie",
            'split': f"Split - para daje lepsze szanse niż granie razem"
        }
        
        base_explanation = explanations.get(action, f"Akcja: {action}")
        
        if has_soft_ace and player_total <= 21:
            base_explanation += f" (soft {player_total})"
        
        # Dodaj informację o balansie jeśli to istotne
        if action in ['double', 'split'] and current_bet > 0:
            if player_balance < current_bet:
                base_explanation += f" - UWAGA: Niewystarczający balans (${player_balance} < ${current_bet})"
        
        return base_explanation


# Przykład użycia bota
def demo_bot():
    """Demonstracja działania bota"""
    bot = BlackjackBot()
    
    # Przykładowe scenariusze
    scenarios = [
        (['A♠', '5♥'], '6♣', "Soft 16 vs 6"),
        (['K♦', '6♠'], '10♥', "Hard 16 vs 10"), 
        (['8♣', '8♠'], '7♦', "Pair of 8s vs 7"),
        (['A♥', 'A♦'], '10♠', "Pair of Aces vs 10"),
        (['5♣', '5♥'], '9♦', "Pair of 5s vs 9"),
        (['10♠', '9♥'], '6♣', "Hard 19 vs 6"),
        (['A♦', '7♠'], '3♥', "Soft 18 vs 3"),
    ]
    
    print("=== DEMONSTRACJA BLACKJACK BOTA ===\n")
    
    for player_cards, dealer_card, description in scenarios:
        action = bot.get_optimal_action(
            player_cards=player_cards,
            dealer_up_card=dealer_card,
            can_double=True,
            can_split=True,
            player_balance=1000,
            current_bet=100
        )
        
        explanation = bot.explain_decision(
            player_cards=player_cards,
            dealer_up_card=dealer_card,
            action=action,
            player_balance=1000,
            current_bet=100
        )
        
        print(f"Scenariusz: {description}")
        print(f"Karty gracza: {player_cards}")
        print(f"Karta dealera: {dealer_card}")
        print(f"Akcja bota: {action.upper()}")
        print(f"Wyjaśnienie: {explanation}")
        print("-" * 50)

if __name__ == "__main__":
    demo_bot()