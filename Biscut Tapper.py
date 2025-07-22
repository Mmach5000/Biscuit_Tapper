import pygame
import os
import sys
import asyncio

pygame.font.init()

WIDTH,HEIGHT = 1100,650
WIN = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption("Biscuit Tapper!")

# colours
WHITE = (255, 255, 255)
BLACK = (8,8,8)
GREY = (165,165,165)

FPS = 60
CIRCLE_WIDTH, CIRCLE_HEIGHT = 300*1.65, 200*1.65

# fonts
TITLE_FONT = pygame.font.Font(None, 85)
UPGRADE_FONT = pygame.font.Font(None, 55)
SCORE_FONT = pygame.font.Font(None, 100)
SEVENTY_FONT = pygame.font.Font(None, 70)
SEVENTY_ONE_FONT = pygame.font.Font(None, 78)
GAME_OVER_FONT = pygame.font.Font(None, 200)

PLAYER_BISCUITS = 0
HEIGHT_BASE = HEIGHT//8

clicking_power = 1
biscuits_per_second = 0
upgrade1_cost = 15
upgrade2_cost = 25
boss = False
score_leak = 1 # Amount of score lost per second when boss is active
player_points = 0

# images
biscuit_image_object = pygame.image.load(
    os.path.join('Assets', 'biscuit_image.png'))

# image scaling
biscuit_image = pygame.transform.rotate(pygame.transform.scale(
    biscuit_image_object,(CIRCLE_WIDTH, CIRCLE_HEIGHT)),0)
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'background.jpg')), (WIDTH, HEIGHT))

#time stuff
TIMER_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TIMER_EVENT, 1000) # 1 second

BOSS_TIMER_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(BOSS_TIMER_EVENT, 40000) # 40 seconds
WORSEN_TIMER_EVENT = pygame.USEREVENT + 3
pygame.time.set_timer(WORSEN_TIMER_EVENT, 7500) # 7.5 seconds

def draw_window(PLAYER_BISCUITS, upgrade1_cost, clicking_power, biscuits_per_second, upgrade2_cost,
                 BACKGROUND, score_leak, boss):
    WIN.blit(BACKGROUND, (0, 0))

    #Biscuit image
    WIN.blit(biscuit_image, (WIDTH//3 - (CIRCLE_WIDTH//2), HEIGHT//2 - (CIRCLE_HEIGHT//2)))

    title_label = TITLE_FONT.render("Upgrades:", 1, BLACK)
    WIN.blit(title_label, (WIDTH//1.6, HEIGHT_BASE))

    clicking_power_label = SEVENTY_FONT.render("Clicking Power: " + str(clicking_power), 1, BLACK)
    WIN.blit(clicking_power_label, (WIDTH - 1025, HEIGHT - 75))

    biscuits_per_second_label = SEVENTY_FONT.render("Biscuits per Second: " + str(biscuits_per_second), 1, BLACK)
    WIN.blit(biscuits_per_second_label, (WIDTH - 1025, HEIGHT - 145))

    if boss == True:
        score_leak_label = SEVENTY_ONE_FONT.render("Biscuit Loss: " + str(score_leak), 1, BLACK)
        WIN.blit(score_leak_label, (WIDTH - 450, HEIGHT - 145))

    #UPGRADES
    if PLAYER_BISCUITS >= upgrade1_cost:
        upgrade1_colour = BLACK
    else:
        upgrade1_colour = GREY
    upgrade1_label = UPGRADE_FONT.render("Upgrade Clicking:", 1, upgrade1_colour)
    upgrade1_label2 = UPGRADE_FONT.render(str(upgrade1_cost) + " Biscuits", 1, upgrade1_colour)
    WIN.blit(upgrade1_label, (WIDTH//1.6, HEIGHT_BASE + 100))
    WIN.blit(upgrade1_label2, (WIDTH//1.6, HEIGHT_BASE + 150))

    if PLAYER_BISCUITS >= upgrade2_cost:
        upgrade2_colour = BLACK
    else:
        upgrade2_colour = GREY
    upgrade2_label = UPGRADE_FONT.render("Upgrade Biscuits per", 1, upgrade2_colour)
    upgrade2_label2 = UPGRADE_FONT.render("Second: " + str(upgrade2_cost) + " Biscuits", 1, upgrade2_colour)
    WIN.blit(upgrade2_label, (WIDTH//1.6, HEIGHT_BASE + 215))
    WIN.blit(upgrade2_label2, (WIDTH//1.6, HEIGHT_BASE + 265))


    # SCORE
    score_label = SCORE_FONT.render("Biscuits: " + str(PLAYER_BISCUITS), 1, BLACK)
    WIN.blit(score_label, (WIDTH//3 - (score_label.get_width()//2), HEIGHT//2.65 - (CIRCLE_HEIGHT//2)))

    pygame.display.update()

def game_over(player_points):
    WIN.fill(BLACK)
    game_over_label = GAME_OVER_FONT.render("Game Over!", 1, WHITE)
    WIN.blit(game_over_label, (WIDTH//2 - (game_over_label.get_width()//2), HEIGHT//2 - (game_over_label.get_height()//2)))
    pygame.display.update()
    pygame.time.delay(3000)

    WIN.fill(BLACK)
    game_over_label1 = GAME_OVER_FONT.render("Total Score:", 1, WHITE)
    game_over_label2 = GAME_OVER_FONT.render(str(player_points), 1, WHITE)
    WIN.blit(game_over_label1, (WIDTH//2 - (game_over_label1.get_width()//2), HEIGHT//2.75 - (game_over_label1.get_height()//2)))
    WIN.blit(game_over_label2, (WIDTH//2 - (game_over_label2.get_width()//2), HEIGHT//1.5 - (game_over_label2.get_height()//2)))
    pygame.display.update()
    pygame.time.delay(4500)
    pygame.quit()
    sys.exit()


async def main(PLAYER_BISCUITS, clicking_power, upgrade1_cost, upgrade2_cost,
          biscuits_per_second, BACKGROUND, boss, score_leak, player_points):
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == TIMER_EVENT:
                PLAYER_BISCUITS += biscuits_per_second
                player_points += biscuits_per_second
                if boss == True:
                    PLAYER_BISCUITS -= score_leak #random.randint(1,3)

            if event.type == BOSS_TIMER_EVENT:
                BACKGROUND = pygame.transform.scale(pygame.image.load(
                    os.path.join('Assets', 'evil_background.jpg')), (WIDTH, HEIGHT))
                boss = True

            if event.type == WORSEN_TIMER_EVENT and boss == True:
                score_leak *= 2
                score_leak = round(score_leak)
                upgrade1_cost *= 2
                upgrade2_cost *= 2
                clicking_power /= 1.5
                biscuits_per_second /= 2
                clicking_power = round(clicking_power)
                biscuits_per_second = round(biscuits_per_second)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    biscuit_button = pygame.Rect(WIDTH//3.25 - (CIRCLE_WIDTH//2), HEIGHT//1.85 - (CIRCLE_HEIGHT//2.25),
                                                 CIRCLE_WIDTH, CIRCLE_HEIGHT)
                    if biscuit_button.collidepoint(mouse_pos):
                        PLAYER_BISCUITS += clicking_power
                        player_points += clicking_power

                    upgrade1_button = pygame.Rect(WIDTH//1.625, HEIGHT_BASE + 90,
                                        WIDTH//3, HEIGHT_BASE + 25)
                    if upgrade1_button.collidepoint(mouse_pos) and PLAYER_BISCUITS >= upgrade1_cost:
                        PLAYER_BISCUITS -= upgrade1_cost
                        clicking_power += 1
                        upgrade1_cost *= 1.4
                        upgrade1_cost = round(upgrade1_cost)

                    upgrade2_button = pygame.Rect(WIDTH//1.625, HEIGHT_BASE + 120,
                                        WIDTH//3, HEIGHT_BASE + 210)
                    if upgrade2_button.collidepoint(mouse_pos) and PLAYER_BISCUITS >= upgrade2_cost:
                        PLAYER_BISCUITS -= upgrade2_cost
                        biscuits_per_second += 2
                        upgrade2_cost *= 1.5
                        upgrade2_cost = round(upgrade2_cost)


            if PLAYER_BISCUITS <= 0 and boss == True:
                game_over(player_points)

        draw_window(PLAYER_BISCUITS, upgrade1_cost, clicking_power, biscuits_per_second,
                     upgrade2_cost, BACKGROUND, score_leak, boss)
        await asyncio.sleep(0)



if __name__ == "__main__":
    asyncio.run(main(PLAYER_BISCUITS, clicking_power, upgrade1_cost, upgrade2_cost,
          biscuits_per_second, BACKGROUND, boss, score_leak, player_points))
