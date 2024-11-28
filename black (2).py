import pygame
import random

# Ініціалізація Pygame
pygame.init()

# Розміри екрану
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Назва гри
pygame.display.set_caption("Blackjack")

# Кольори
green = (34, 139, 34)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Шрифти
font = pygame.font.SysFont(None, 55)
small_font = pygame.font.SysFont(None, 35)

# Створення колоди карт
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

# Витягнути карту з колоди
def draw_card(deck):
    return deck.pop(random.randint(0, len(deck) - 1))

# Підрахунок очок у руці
def calculate_score(hand):
    score = 0
    aces = 0
    for card in hand:
        score += values[card[0]]
        if card[0] == 'A':
            aces += 1
    while score > 21 and aces:
        score -= 10
        aces -= 1
    return score

# Виведення тексту на екран
def display_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Створення колоди
def create_deck():
    deck = []
    for suit in suits:
        for value in values:
            deck.append((value, suit))
    return deck

# Основний цикл гри
def game_loop():
    game_over = False

    while not game_over:
        deck = create_deck()

        player_hand = [draw_card(deck), draw_card(deck)]
        dealer_hand = [draw_card(deck), draw_card(deck)]

        player_stands = False
        player_busted = False
        dealer_busted = False
        game_finished = False

        while not game_finished:
            screen.fill(green)

            # Виводимо карти гравця і дилера
            display_text("Ваші карти:", small_font, white, 50, 100)
            for i, card in enumerate(player_hand):
                display_text(f"{card[0]} of {card[1]}", small_font, white, 50, 150 + i * 30)

            display_text("Карти дилера:", small_font, white, 400, 100)
            if player_stands:
                for i, card in enumerate(dealer_hand):
                    display_text(f"{card[0]} of {card[1]}", small_font, white, 400, 150 + i * 30)
            else:
                display_text(f"{dealer_hand[0][0]} of {dealer_hand[0][1]}", small_font, white, 400, 150)
                display_text("???", small_font, white, 400, 180)

            # Виводимо кнопки
            pygame.draw.rect(screen, white, [50, 400, 200, 50])
            display_text("Взяти карту", small_font, black, 70, 410)

            pygame.draw.rect(screen, white, [300, 400, 200, 50])
            display_text("Залишитися", small_font, black, 320, 410)

            # Отримуємо координати миші та перевіряємо кліки
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            if 50 <= mouse[0] <= 250 and 400 <= mouse[1] <= 450 and click[0] == 1 and not player_stands:
                # Гравець бере карту
                player_hand.append(draw_card(deck))
                if calculate_score(player_hand) > 21:
                    player_busted = True
                    game_finished = True
                pygame.time.delay(300)

            if 300 <= mouse[0] <= 500 and 400 <= mouse[1] <= 450 and click[0] == 1 and not player_stands:
                # Гравець вирішив залишитися
                player_stands = True

            # Якщо гравець залишився, дилер грає
            if player_stands and not game_finished:
                while calculate_score(dealer_hand) < 17:
                    dealer_hand.append(draw_card(deck))
                if calculate_score(dealer_hand) > 21:
                    dealer_busted = True
                game_finished = True

            # Визначаємо переможця
            if game_finished:
                player_score = calculate_score(player_hand)
                dealer_score = calculate_score(dealer_hand)

                if player_busted:
                    display_text("Ви програли!", font, red, 50, 300)
                elif dealer_busted or player_score > dealer_score:
                    display_text("Ви виграли!", font, red, 50, 300)
                elif player_score < dealer_score:
                    display_text("Ви програли!", font, red, 50, 300)
                else:
                    display_text("Нічия!", font, red, 50, 300)

                # Затримка перед питанням про продовження
                pygame.display.update()
                pygame.time.delay(2000)

                # Питання про продовження
                while True:
                    screen.fill(green)
                    display_text("Хочете продовжити?", font, white, 200, 200)

                    pygame.draw.rect(screen, white, [150, 400, 150, 50])
                    display_text("Так", small_font, black, 175, 410)

                    pygame.draw.rect(screen, white, [400, 400, 150, 50])
                    display_text("Ні", small_font, black, 425, 410)

                    mouse = pygame.mouse.get_pos()
                    click = pygame.mouse.get_pressed()

                    # Якщо гравець обирає "Так"
                    if 150 <= mouse[0] <= 300 and 400 <= mouse[1] <= 450 and click[0] == 1:
                        game_loop()

                    # Якщо гравець обирає "Ні"
                    if 400 <= mouse[0] <= 550 and 400 <= mouse[1] <= 450 and click[0] == 1:
                        game_over = True
                        pygame.quit()
                        return

                    pygame.display.update()

            # Оновлюємо екран
            pygame.display.update()

            # Обробка подій
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_finished = True

            clock = pygame.time.Clock()
            clock.tick(30)

    pygame.quit()

# Запускаємо гру
game_loop()
