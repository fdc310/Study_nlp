import pygame
import sys

# 初始化pygame
pygame.init()

# 设置屏幕大小
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 设置标题
pygame.display.set_caption("推箱子小游戏")

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 设置游戏时钟
clock = pygame.time.Clock()

# 定义玩家、箱子和目标的位置
player_pos = [50, 50]
box_pos = [200, 200]
target_pos = [400, 400]
player_size = 50
box_size = 50
target_size = 50

# 按键间隔时间（毫秒）
key_interval = 200
last_key_time = 0

# 游戏主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 获取当前时间
    current_time = pygame.time.get_ticks()

    # 获取按键状态
    keys = pygame.key.get_pressed()
    move_distance = player_size  # 移动距离为玩家的大小

    # 初始化移动标志
    moved = False

    # 计算移动后的位置
    new_player_pos = player_pos.copy()
    if keys[pygame.K_LEFT] and current_time - last_key_time > key_interval:
        new_player_pos[0] -= move_distance
        moved = True
    if keys[pygame.K_RIGHT] and current_time - last_key_time > key_interval:
        new_player_pos[0] += move_distance
        moved = True
    if keys[pygame.K_UP] and current_time - last_key_time > key_interval:
        new_player_pos[1] -= move_distance
        moved = True
    if keys[pygame.K_DOWN] and current_time - last_key_time > key_interval:
        new_player_pos[1] += move_distance
        moved = True

    # 检查玩家是否推到箱子
    if new_player_pos == box_pos and moved:
        new_box_pos = box_pos.copy()
        if keys[pygame.K_LEFT]:
            new_box_pos[0] -= move_distance
        if keys[pygame.K_RIGHT]:
            new_box_pos[0] += move_distance
        if keys[pygame.K_UP]:
            new_box_pos[1] -= move_distance
        if keys[pygame.K_DOWN]:
            new_box_pos[1] += move_distance

        # 检查箱子移动后是否超出屏幕
        if 0 <= new_box_pos[0] <= SCREEN_WIDTH - box_size and 0 <= new_box_pos[1] <= SCREEN_HEIGHT - box_size:
            box_pos = new_box_pos
            player_pos = new_player_pos
            last_key_time = current_time  # 更新按键时间
    elif moved:
        # 检查玩家移动后是否超出屏幕
        if 0 <= new_player_pos[0] <= SCREEN_WIDTH - player_size and 0 <= new_player_pos[1] <= SCREEN_HEIGHT - player_size:
            player_pos = new_player_pos
            last_key_time = current_time  # 更新按键时间

    # 检查箱子是否到达目标位置
    if box_pos == target_pos:
        print("恭喜你，成功推到箱子！")
        running = False

    # 填充背景色
    screen.fill(WHITE)

    # 绘制玩家、箱子和目标
    pygame.draw.rect(screen, BLACK, (player_pos[0], player_pos[1], player_size, player_size))
    pygame.draw.rect(screen, RED, (box_pos[0], box_pos[1], box_size, box_size))
    pygame.draw.rect(screen, GREEN, (target_pos[0], target_pos[1], target_size, target_size))

    # 更新屏幕
    pygame.display.flip()

    # 设置帧率
    clock.tick(60)

# 退出pygame
pygame.quit()
sys.exit()
