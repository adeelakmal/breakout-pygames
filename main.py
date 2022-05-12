import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 720, 540
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('BLOCK BREAKER')

WIN_FONT = pygame.font.SysFont('VCR OSD Mono', 80)
LOSE_FONT = pygame.font.SysFont('VCR OSD Mono', 80)

HIT_SOUND = pygame.mixer.Sound(
    os.path.join('Assets','pong hit.mp3'))
BLOCK_SOUND = pygame.mixer.Sound(
    os.path.join('Assets','block hit.mp3'))

PADDLE_WIDTH, PADDLE_HEIGHT = 98, 25
BALL_WIDTH, BALL_HEIGHT = 20,20
BLOCK_WIDTH, BLOCK_HEIGHT = 34,34

BLOCK_Y = 50

WHITE = (20,40,60)
WHITE2 = (255,255,255)

FPS = 60
VEL = 5
BALL_VEL_X = 5
BALL_VEL_Y = 5

BLOCK_COL_X = pygame.USEREVENT + 1
BLOCK_COL_Y = pygame.USEREVENT + 2

#ASSETS
SMALL_PADDLE = pygame.image.load(
    os.path.join('Assets','paddle.png'))
PADDLE = pygame.transform.scale(SMALL_PADDLE, (PADDLE_WIDTH, PADDLE_HEIGHT))

BALL_IMAGE = pygame.image.load(
    os.path.join('Assets','ball.png'))
BALL = pygame.transform.scale(BALL_IMAGE, (BALL_WIDTH, BALL_HEIGHT))

BLOCK_IMAGE = pygame.image.load(
    os.path.join('Assets','block.png'))
BLOCK = pygame.transform.scale(BLOCK_IMAGE,(BLOCK_WIDTH, BLOCK_HEIGHT))



# Draws/imports images to the window
def draw_win(paddle,ball,BLOCKS, win):
    WIN.fill(WHITE)
    WIN.blit(PADDLE,(paddle.x, paddle.y))
    WIN.blit(BALL,(ball.x, ball.y))

    for blk in BLOCKS :
        WIN.blit(BLOCK, (blk.x,blk.y))

    pygame.display.update()

# Keeps track of movement
def paddle_movement(keys_pressed, paddle, ball, start):
    if keys_pressed[pygame.K_RIGHT] and paddle.x < WIDTH - paddle.width:
        paddle.x += VEL
        if start is False:
            ball.x += VEL

    if keys_pressed[pygame.K_LEFT] and paddle.x  > 0:
        paddle.x -= VEL
        if start is False:
            ball.x -= VEL

# Moves the ball
def ball_movement(ball):
    global  BALL_VEL_X, BALL_VEL_Y
    ball.y -= BALL_VEL_Y
    ball.x -= BALL_VEL_X
    
def handle_collision(BLOCKS, ball):
    for blk in BLOCKS:
        if blk.collidepoint(ball.x,ball.y + BALL_HEIGHT //2) or blk.collidepoint(ball.x + BALL_WIDTH, ball.y + BALL_HEIGHT //2):
            BLOCKS.remove(blk)
            pygame.event.post(pygame.event.Event(BLOCK_COL_X))
        elif blk.collidepoint(ball.x + BALL_WIDTH // 2, ball.y) or blk.collidepoint(ball.x + BALL_WIDTH // 2, ball.y + BALL_HEIGHT):
            BLOCKS.remove(blk)
            pygame.event.post(pygame.event.Event(BLOCK_COL_Y))

def draw_winner(text):
    win_text = WIN_FONT.render(text, 1, WHITE2)
    WIN.blit(win_text, 
    (WIDTH // 2 - (win_text.get_width() // 2),
     HEIGHT // 2 - (win_text.get_height() // 2) ) )
    
    pygame.display.update()
    pygame.time.delay(2000)

def draw_looser(text):
    lose_text = LOSE_FONT.render(text, 1, WHITE2)
    WIN.blit(lose_text, 
    (WIDTH // 2 - (lose_text.get_width() // 2),
     HEIGHT // 2 - (lose_text.get_height() // 2) ) )
    
    pygame.display.update()
    pygame.time.delay(2000)

#Main Game loop
def main():
    global BALL_VEL_X, BALL_VEL_Y

    Run = True
    start = False
    clock = pygame.time.Clock()

    paddle = pygame.Rect(300, 500, PADDLE_WIDTH, PADDLE_HEIGHT )
    ball = pygame.Rect(
        paddle.x + (paddle.width // 2) - (BALL_WIDTH // 2) , paddle.y - BALL_HEIGHT , BALL_WIDTH, BALL_HEIGHT )

    BLOCKS = []
    for y_value in range (30, BLOCK_HEIGHT * 4, BLOCK_HEIGHT+5):
        for x_value in range(200,BLOCK_WIDTH*15,BLOCK_WIDTH):
            block = pygame.Rect(x_value,y_value,BLOCK_WIDTH, BLOCK_HEIGHT)
            BLOCKS.append(block)

    while Run:
        win = ''
        lose = 'YOU LOSE!'
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Run = False
                pygame.quit()
            # Detects if game has started
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start = True
            if event.type == BLOCK_COL_X:
                BALL_VEL_X = -BALL_VEL_X
                BLOCK_SOUND.play()
            if event.type == BLOCK_COL_Y:
                BALL_VEL_Y = -BALL_VEL_Y
                BLOCK_SOUND.play() 

        keys_pressed = pygame.key.get_pressed()
        paddle_movement(keys_pressed, paddle, ball, start)

        # Keeps ball in the screen
        if start:
        
            ball_movement(ball)
            if ball.x < 0 or ball.x + ball.width > WIDTH:
                BALL_VEL_X = -BALL_VEL_X
            if ball.y < 0:
                BALL_VEL_Y = -BALL_VEL_Y  
            if ball.y  > HEIGHT:
                draw_looser(lose)
                break
            if paddle.colliderect(ball):
                BALL_VEL_Y = -BALL_VEL_Y
                HIT_SOUND.play()

        if len(BLOCKS) == 0:
            win = 'YOU WON!'
        if win != '':
            draw_winner(win)
            break

        handle_collision(BLOCKS, ball) 
        draw_win(paddle, ball, BLOCKS, win)

    BALL_VEL_X = abs(BALL_VEL_X)
    BALL_VEL_Y = abs(BALL_VEL_Y)
    main()

if __name__ == '__main__':
    main()