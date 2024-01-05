from poker import Combo
from poker import Card

def calculate_equity(players_hands, community_cards):
    player_equities = []

    for i, player_hand in enumerate(players_hands):
        print(player_hand)
        player_hand = Combo(player_hand)
        community_cards_list = [Card(card) for card in community_cards]
        opponents_hands = [Combo(hand) for j, hand in enumerate(players_hands) if j != i]

        # Calculate hand equity for the player's hand against all opponents' hands
        equity = player_hand.equity(community_cards_list, opponents_hands)
        player_equities.append(equity)

    return player_equities

def main():
    players_hands = ["AhKs", "QhQd", "JcTc"]  # Replace with the known hands of each player
    community_cards = ["7s", "8s", "9d"]  # Replace with the known community cards

    player_equities = calculate_equity(players_hands, community_cards)

    for i, equity in enumerate(player_equities):
        print(f"Player {i+1} equity: {equity:.2%}")

if __name__ == "__main__":
    main()
