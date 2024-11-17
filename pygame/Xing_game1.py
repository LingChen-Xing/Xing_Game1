import pygame
import random
import sys

pygame.init()

# 设置窗口大小
WIDTH, HEIGHT = 1100, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("星的第一个游戏")

# 加载背景图片
background = pygame.image.load("haha1.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# 定义颜色
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# 定义长条（板）属性
paddle_width, paddle_height = 100, 20
paddle_x = (WIDTH - paddle_width) // 2
paddle_y = HEIGHT - 50
paddle_speed = 15

# 定义小球属性
ball_radius = 10
ball_x = WIDTH // 2  # 初始位置居中
ball_y = HEIGHT // 2
ball_speed_x = 0  # 初速度为0
ball_speed_y = 0
gravity = 0.5  # 模拟重力

# 定义星星属性
star_radius = 10
stars = [(random.randint(0, WIDTH), random.randint(0, 200)) for _ in range(5)]
stars_number = 5

# 定义游戏变量
score = 0
missed_balls = 0
lives = 1  # 初始生命值
game_over = False

# 设置字体
font = pygame.font.Font(None, 36)

# 游戏主循环
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 如果游戏结束，显示分数并询问是否重新开始
    if game_over:
        screen.fill(WHITE)
        text = font.render(f"Game Over! Final Score: {score}", True, RED)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        screen.blit(text, text_rect)
        restart_text = font.render("Press Y to Restart or N to Quit", True, RED)
        restart_text_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        screen.blit(restart_text, restart_text_rect)
        pygame.display.flip()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_y]:
            # 重置游戏
            lives = 1
            score = 0
            missed_balls = 0
            game_over = False
            ball_x, ball_y = WIDTH // 2, HEIGHT // 2
            ball_speed_x, ball_speed_y = 0, 0
            paddle_width, paddle_height = 100, 20
            paddle_x = (WIDTH - paddle_width) // 2
            paddle_y = HEIGHT - 50
            stars = [(random.randint(0, WIDTH), random.randint(0, 200)) for _ in range(5)]
        elif keys[pygame.K_n]:
            pygame.quit()
            sys.exit()
        continue

    # 检查键盘输入
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:  # 左方向键
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < WIDTH - paddle_width:  # 右方向键
        paddle_x += paddle_speed
    if keys[pygame.K_w] and paddle_y > 200:  # 上方向键
        paddle_y -= paddle_speed
    if keys[pygame.K_s] and paddle_y < HEIGHT - paddle_height:  # 下方向键
        paddle_y += paddle_speed

    # 检测按键状态，用于控制小球反弹时的水平加速度
    add_speed_left = keys[pygame.K_a]  # 按下A键时
    add_speed_right = keys[pygame.K_d]  # 按下D键时

    # 更新小球位置
    if ball_speed_y <= 7:  # 如果小球向下的速度小于等于 7
        ball_speed_y += gravity  # 重力加速度
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # 碰到左右边界反弹
    if ball_x - ball_radius < 0 or ball_x + ball_radius > WIDTH:
        ball_speed_x = -ball_speed_x

    # 碰到顶部反弹
    if ball_y - ball_radius < 0:
        ball_speed_y = -ball_speed_y

    # 碰到板时反弹
    if (
        paddle_y < ball_y + ball_radius < paddle_y + paddle_height
        and paddle_x < ball_x < paddle_x + paddle_width
    ):
        ball_speed_y = -15  # 反弹向上
        # 根据按键增加水平速度
        if add_speed_left:
            ball_speed_x = -5
        elif add_speed_right:
            ball_speed_x = 5
        else:
            ball_speed_x = 0

    # 检查小球是否碰到星星
    new_stars = []
    for star_x, star_y in stars:
        if (
            (ball_x - star_x) ** 2 + (ball_y - star_y) ** 2
            <= (ball_radius + star_radius) ** 2
        ):
            score += 1  # 小球碰到星星，得分
            stars_number -= 1
        else:
            new_stars.append((star_x, star_y))  # 保留未碰到的星星
    stars = new_stars
    if stars_number == 0:
        stars = [(random.randint(0, WIDTH), random.randint(0, 200)) for _ in range(5)]
        stars_number = 5

    # 小球掉到屏幕底部时
    if ball_y > HEIGHT:
        missed_balls += 1
        lives -= 1
        if lives <= 0:  # 生命值耗尽，游戏结束
            game_over = True
        else:
            # 重置小球位置
            ball_x = WIDTH // 2
            ball_y = HEIGHT // 2
            ball_speed_x = 0
            ball_speed_y = 0

            # 重置板
            paddle_width, paddle_height = 100, 20
            paddle_x = (WIDTH - paddle_width) // 2
            paddle_y = HEIGHT - 50
            # 重置星星
            stars = [(random.randint(0, WIDTH), random.randint(0, 200)) for _ in range(5)]
            stars_number = 5

    # 绘制背景
    screen.blit(background, (0, 0))

    # 绘制长条
    pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, paddle_width, paddle_height))

    # 绘制小球
    pygame.draw.circle(screen, WHITE, (int(ball_x), int(ball_y)), ball_radius)

    # 绘制星星
    for star_x, star_y in stars:
        pygame.draw.circle(screen, YELLOW, (star_x, star_y), star_radius)

    # 绘制分数
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # 绘制剩余生命值
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(lives_text, (10, 50))

    # 更新屏幕
    pygame.display.flip()

    # 控制帧率
    clock.tick(45)