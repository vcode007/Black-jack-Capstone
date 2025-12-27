import random
import itertools

# Define card ranks and suits
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

# Generate the deck using list comprehension
available_cards = [f"{rank} of {suit}" for rank, suit in itertools.product(ranks, suits)]

# Shuffle the deck before starting the game
random.shuffle(available_cards)


def get_a_card():
    """Draw one card from the deck"""
    return available_cards.pop(0)


def get_user_score(user_cards):
    """Calculate score for each player."""
    score = get_card_scores(user_cards)
    return score


def get_rank(card):
    """Extract the rank from a card string.

        Example:
            "10 of Hearts" -> "10"
            "A of Spades"  -> "A"
        """
    return card.split(" ")[0]


def get_dealer_score(dealer_cards):
    """Return the score of the dealer's visible (first) card."""
    rank = get_rank(dealer_cards[0])
    if rank in ['J', 'Q', 'K', '10']:
        return 10
    elif rank == "A":
        return 11
    else:
        return int(rank)


def get_card_scores(cards):
    """Calculate the total score for a list of cards."""

    score = sum(10 if get_rank(card) in ['J', 'Q', 'K', '10'] else
                11 if get_rank(card) == 'A' else int(get_rank(card)) for card in cards)

    aces = sum(1 for card in cards if get_rank(card) == 'A')

    # Adjust for Aces if score is over 21
    while score > 21 and aces > 0:
        score -= 10
        aces -= 1

    return score


def check_if_user_blackjack(cards):
    """Check if any of the players has got a blackjack"""
    ranks_in_hand = [get_rank(card) for card in cards]
    return ((ranks_in_hand[0] in ['J', 'Q', 'K', '10'] and ranks_in_hand[1] == "A") or
            (ranks_in_hand[0] == "A" and ranks_in_hand[1] in ['K', 'J', 'Q', '10']))


def format_cards(cards):
    """Return a formatted string of the card list."""
    return ", ".join(cards)


def main():
    user_cards = []
    dealer_cards = []
    user_hits = True

    # Deal initial 2 cards for user and dealer
    user_cards.append(get_a_card())
    dealer_cards.append(get_a_card())
    user_cards.append(get_a_card())
    dealer_cards.append(get_a_card())

    print(f"Your cards: {format_cards(user_cards)} | Score: {get_card_scores(user_cards)}")

    # Check if user or dealer have blackjack
    user_blackjack = check_if_user_blackjack(user_cards)
    dealer_blackjack = check_if_user_blackjack(dealer_cards)

    if user_blackjack and dealer_blackjack:
        print("Its a tie! Both you and Dealer have Blackjack!")
        print(f"Your cards: {user_cards}")
        print(f"Dealer's cards: {dealer_cards}")
        return
    elif user_blackjack:
        print("You got a Blackjack! You won!")
        print(f"Your cards: {user_cards}")
        print(f"Dealer's cards: {dealer_cards}")
        return
    elif dealer_blackjack:
        print("Dealer got Blackjack! You lose.")
        print(f"Your cards: {user_cards}")
        print(f"Dealer's cards: {dealer_cards}")
        return

    # Reveal dealer's visible card and its score
    print(f"Dealer's visible card: {dealer_cards[0]} | Score: {get_dealer_score(dealer_cards)}")

    # User's turn: Hit until the user stands or busts
    while user_hits:
        user_add_card = input("Do you want another card (y/n)? ").strip().casefold()
        if user_add_card == 'y':
            user_cards.append(get_a_card())
            current_score = get_card_scores(user_cards)
            print(f"Your current hand: {format_cards(user_cards)} | Score: {current_score}")
            if current_score > 21:
                print("You score exceeds 21. You Bust! Dealer wins.")
                return
        else:
            break

    # Dealer's turn: Dealer must hit until score is at least 17
    while get_card_scores(dealer_cards) < 17:
        dealer_cards.append(get_a_card())

    user_score, dealer_score = get_card_scores(user_cards), get_card_scores(dealer_cards)
    print(f"Dealer's final hand: {format_cards(dealer_cards)} | Score: {dealer_score}")
    print(f"Your final hand: {format_cards(user_cards)} | Score: {user_score}")

    if dealer_score > 21 or user_score > dealer_score:
        print("You win!")
    elif dealer_score > user_score:
        print("Dealer wins!")
    else:
        print("It's a tie!")


if __name__ == '__main__':
    main()
