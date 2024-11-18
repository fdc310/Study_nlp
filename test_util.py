import pygame
import sys
import math
import cv2
import dlib
import numpy as np

# 初始化 Pygame
pygame.init()

# 设置屏幕尺寸
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Eye Animation")

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 加载左右眼图像
left_eye_image = pygame.image.load('eye.jpg')
right_eye_image = pygame.image.load('eye.jpg')

# 加载左右眼珠图像
left_pupil_image = pygame.image.load('pilu.jpg')
right_pupil_image = pygame.image.load('pilu.jpg')

# 缩小眼珠图像
left_pupil_image = pygame.transform.smoothscale(left_pupil_image, (left_pupil_image.get_width() // 2, left_pupil_image.get_height() // 2))
right_pupil_image = pygame.transform.smoothscale(right_pupil_image, (right_pupil_image.get_width() // 2, right_pupil_image.get_height() // 2))

# 获取图像尺寸
left_eye_rect = left_eye_image.get_rect()
right_eye_rect = right_eye_image.get_rect()
left_pupil_rect = left_pupil_image.get_rect()
right_pupil_rect = right_pupil_image.get_rect()

# 设置眼睛位置
left_eye_position = (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
right_eye_position = (SCREEN_WIDTH * 3 // 4, SCREEN_HEIGHT // 2)
left_eye_rect.center = left_eye_position
right_eye_rect.center = right_eye_position

# 设置眼珠初始位置
left_pupil_position = left_eye_position
right_pupil_position = right_eye_position
left_pupil_rect.center = left_pupil_position
right_pupil_rect.center = right_pupil_position

# 设置眼球移动放大的比例因子
movement_scale_factor = 2.0

# 初始化摄像头
cap = cv2.VideoCapture(0)

# 初始化dlib的人脸检测器和68点特征预测器
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

def get_eye_landmarks(shape, eye_indices):
    """从shape对象中提取眼睛标记点的坐标"""
    points = np.array([(shape.part(i).x, shape.part(i).y) for i in eye_indices], dtype=np.int32)
    return points

def eye_center(eye):
    """计算眼睛的中心点"""
    x = (eye[0][0] + eye[3][0]) // 2
    y = (eye[1][1] + eye[4][1]) // 2
    return (x, y)

# 眼睛索引
LEFT_EYE_INDICES = [36, 37, 38, 39, 40, 41]
RIGHT_EYE_INDICES = [42, 43, 44, 45, 46, 47]

def get_eye_positions():
    ret, frame = cap.read()
    if not ret:
        return None, None

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    if len(faces) == 0:
        return None, None

    face = faces[0]
    shape = predictor(gray, face)
    left_eye = get_eye_landmarks(shape, LEFT_EYE_INDICES)
    right_eye = get_eye_landmarks(shape, RIGHT_EYE_INDICES)

    left_eye_center = eye_center(left_eye)
    right_eye_center = eye_center(right_eye)

    return left_eye_center, right_eye_center

# 游戏主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 获取眼球中心位置
    left_eye_center, right_eye_center = get_eye_positions()
    if left_eye_center is not None and right_eye_center is not None:
        # 计算左眼珠新位置
        dx_left = left_eye_center[0] - left_eye_position[0]
        dy_left = left_eye_center[1] - left_eye_position[1]
        left_pupil_position = (left_eye_position[0] + int(dx_left * movement_scale_factor), left_eye_position[1] + int(dy_left * movement_scale_factor))
        left_pupil_rect.center = left_pupil_position

        # 计算右眼珠新位置
        dx_right = right_eye_center[0] - right_eye_position[0]
        dy_right = right_eye_center[1] - right_eye_position[1]
        right_pupil_position = (right_eye_position[0] + int(dx_right * movement_scale_factor), right_eye_position[1] + int(dy_right * movement_scale_factor))
        right_pupil_rect.center = right_pupil_position

    # 绘制背景
    screen.fill(WHITE)

    # 绘制左右眼
    screen.blit(left_eye_image, left_eye_rect)
    screen.blit(right_eye_image, right_eye_rect)

    # 绘制左右眼珠
    screen.blit(left_pupil_image, left_pupil_rect)
    screen.blit(right_pupil_image, right_pupil_rect)

    # 更新屏幕
    pygame.display.flip()

# 退出 Pygame
pygame.quit()
cap.release()
cv2.destroyAllWindows()
sys.exit()
