import pygame
import math
import time

pygame.init()

width = 2000
height = 1000

win = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption('Portal.py')

add_platform = pygame.image.load('add_platform.png')
play_button = pygame.image.load('play_button_new.png')

add_dict = {
    'x' : width - 140,
    'y' : 40,
    'width' : 100,
    'height' : 100
}

play_dict = {
    'x' : 40,
    'y' : 40,
    'width' : 100,
    'height' : 100
}

add_platform = pygame.transform.scale(add_platform, (add_dict['width'], add_dict['height']))
play_button = pygame.transform.scale(play_button, (play_dict['width'], play_dict['height']))

x = width // 2
y = height // 2
gun_x = x
gun_y = y
vel = 20 # Terminal velocity of the player
friction = 0.3
gravity = 0.1
power = 5
vertical_momentum = 0
lateral_momentum = 0
pX = 200
pY = 200
pW = 500
pH = 20
data = "object positional mmode"
barriers = True
shot_orange = False
shot_blue = False
portal_there = False
ready = False
portal_height = 0
portal_width = 0
bW = 0
bH = 0
bX = 0
bY = 0
bD = 0
oW = 0
oH = 0
oX = 0
oY = 0
oD = 0
a = 0
b = 0
override = False
touching_portal = False
offset2 = 0
frame_speed = 1
touching_portal = False
portal_color = (255, 255, 255)
print(height/width)
frame_num = 0
y = 0
force = 0
platform_queue = []
ready = True
run = True
orange_circle = pygame.image.load('orange-circle.png').convert()
orange_circle = pygame.transform.smoothscale(orange_circle, (10, 10))
blue_circle = pygame.image.load('blue-circle.png').convert()
blue_circle = pygame.transform.smoothscale(blue_circle, (10, 10))
white_circle = pygame.image.load('white-circle.png').convert()
white_circle = pygame.transform.smoothscale(white_circle, (10, 10))
orange_gun = pygame.image.load('orange-portal-gun.png')
orange_gun = pygame.transform.scale(orange_gun, (80, 70))
blue_gun = pygame.image.load('blue-portal-gun.png')
blue_gun = pygame.transform.scale(blue_gun, (80, 70))
white_gun = pygame.image.load('white-portal-gun.png')
white_gun = pygame.transform.scale(white_gun, (80, 70))
logo_width = int(width / 1.5)
logo_height = int(logo_width * (1200/2000))
print(logo_width, logo_height)
logo = pygame.image.load('portal-logo-white.png')
logo = pygame.transform.scale(logo, (logo_width, logo_height))
mini_logo = pygame.image.load('portal-logo-white-small2.png')
mini_logo = pygame.transform.scale(mini_logo, (150, 75))
logo_x = (width - logo_width) / 2
logo_y = (height - logo_height) / 2
plane2D = []
portal_x = None
portal_y = None
axised_x = False
axised_y = False

class Platform:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.x2 = x + w
        self.y2 = y + h
        self.width = w
        self.height = h
        self.name = "Platform#" + str(len(plane2D))
        plane2D.append(self)

    @classmethod
    def spawn(cls, x, y, w, h):
        myPlatform = cls(x, y, w, h)

    def touching(self, x, y):
        touch_matrix = [(x, y), (x + 20, y), (x, y + 20), (x + 20, y + 20)]
        for j in touch_matrix:
            x_fit = j[0] >= self.x and j[0] <= self.x2
            y_fit = j[1] >= self.y and j[1] <= self.y2
            if x_fit and y_fit:
                return True
                break
        return False

    def touch(self, x, y):
        return x >= self.x and y >= self.y and x <= self.x + self.width and y <= self.y + self.height + 20

    def touch2(self, x, y):
        return x > self.x and y > self.y and x < self.x + self.width and y < self.y + self.height + 20

def grounded():
    return y >= height - vertical_momentum and not override

def move(angle, step):
    global gun_x, gun_y
    rad = math.radians(angle)
    gun_x += math.cos(rad) * step
    gun_y += math.sin(rad) * step

def teleport(from_info, to_info):
    global b
    global a
    global offset2
    global x, y
    global vertical_momentum, lateral_momentum
    fromName = from_info[0]
    fromX = from_info[1]
    fromY = from_info[2]
    toName = to_info[0]
    toX = to_info[1]
    toY = to_info[2]

    if fromName == "floor" and vertical_momentum < 0:
        if toName == "floor":
            a = toX + (x - fromX)
            x = a
            y = toY - 30
            vertical_momentum = -vertical_momentum
        elif toName == "ceiling":
            a = toX + (x - fromX)
            x = a
            y = toY + 50
            vertical_momentum = vertical_momentum
        elif toName == "right":
            b = toY + (x - fromX)
            y = b
            x = toX - 30
            lateral_momentum = vertical_momentum
            vertical_momentum = 0
        elif toName == "left":
            b = toY + (x - fromX)
            y = b
            x = toX + 50
            lateral_momentum = -vertical_momentum
            vertical_momentum = 0

    if fromName == "ceiling" and vertical_momentum > 0:
        if toName == "ceiling":
            a = toX + (x - fromX)
            x = a
            y = toY + 50
            vertical_momentum = -vertical_momentum
        elif toName == "floor":
            a = toX + (x - fromX)
            x = a
            y = toY - 30
            vertical_momentum = vertical_momentum
        elif toName == "right":
            b = toY + (x - fromX)
            y = b
            x = toX - 30
            lateral_momentum = -vertical_momentum
            vertical_momentum = 0
        elif toName == "left":
            b = toY + (x - fromX)
            y = b
            x = toX + 50
            lateral_momentum = vertical_momentum
            vertical_momentum = 0

    if fromName == "right" and lateral_momentum > 0:
        if toName == "right":
            b = toY + (y - fromY)
            y = b
            x = toX - 30
            lateral_momentum = -lateral_momentum
            vertical_momentum = 0
        elif toName == "left":
            b = toY + (y - fromY)
            y = b
            x = toX + 50
            lateral_momentum = lateral_momentum
            vertical_momentum = 0
        elif toName == "floor":
            a = toX + (y - fromY)
            x = a
            y = toY - 30
            vertical_momentum = lateral_momentum
        elif toName == "ceiling":
            a = toX + (y - fromY)
            x = a
            y = toY + 50
            vertical_momentum = -lateral_momentum

    if fromName == "left" and lateral_momentum < 0:
        if toName == "left":
            b = toY + (y - fromY)
            y = b
            x = toX + 50
            lateral_momentum = -lateral_momentum
            vertical_momentum = 0
        elif toName == "right":
            b = toY + (y - fromY)
            y = b
            x = toX - 30
            lateral_momentum = lateral_momentum
            vertical_momentum = 0
        elif toName == "floor":
            a = toX + (y - fromY)
            x = a
            y = toY - 30
            vertical_momentum = -lateral_momentum
        elif toName == "ceiling":
            a = toX + (y - fromY)
            x = a
            y = toY + 50
            vertical_momentum = lateral_momentum


'''Platform.spawn(500, 500, 500, 500)
Platform.spawn(250, 750, 250, 250)
Platform.spawn(750, 250, 250, 250)
Platform.spawn(0, 100, 250, 250)'''

block_x = 0
block_y = 0
block_width = 100
block_height = 100
offset = 0
offset3 = 10
notflipped = True
selected = False

while run:
    win.fill((0, 0, 0))
    pygame.time.delay(0)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    keys = pygame.key.get_pressed()
    mouse_x = pygame.mouse.get_pos()[0]
    mouse_y = pygame.mouse.get_pos()[1]
    mouse_c = pygame.mouse.get_pressed()[0]

    for platform in platform_queue:
        block_x = platform[0]
        block_y = platform[1]
        block_width = platform[2]
        block_height = platform[3]
        segment_a_bottom = [block_x, block_y + block_height - 10, block_width, 10]
        segment_b_right = [block_x + block_width - 10, block_y, 10, block_height]
        SABx = segment_a_bottom[0]
        SABy = segment_a_bottom[1]
        SABw = segment_a_bottom[2]
        SABh = segment_a_bottom[3]
        SBRx = segment_b_right[0]
        SBRy = segment_b_right[1]
        SBRw = segment_b_right[2]
        SBRh = segment_b_right[3]

        if mouse_x >= SABx and mouse_x <= SABx + SABw and mouse_y >= SABy and mouse_y <= SABy + SABh and mouse_c:
            selected = platform_queue.index(platform)
        elif selected == platform_queue.index(platform) and not axised_x:
            block_width = mouse_x - block_x
            axised_y = True

        if mouse_x >= SBRx and mouse_x <= SBRx + SBRw and mouse_y >= SBRy and mouse_y <= SBRy + SBRh and mouse_c:
            selected = platform_queue.index(platform)
        elif selected == platform_queue.index(platform) and not axised_y:
            block_height = mouse_y - block_y
            axised_x = True

        if not mouse_c:
            selected = -1
            axised_x = False
            axised_y = False

        if mouse_x >= block_x and mouse_y >= block_y and mouse_x <= block_x + block_width - SBRw and mouse_y <= block_y + block_height - SABh and mouse_c:
            block_x = mouse_x - block_width / 2
            block_y = mouse_y - block_height / 2

        if block_x + block_width > width:
            block_x = width - block_width

        if block_y + block_height > height:
            block_y = height - block_height

        if block_x < 0:
            block_x = 0

        if block_y < 0:
            block_y = 0


        platform_num = platform_queue.index(platform)
        platform_queue[platform_num][0] = block_x
        platform_queue[platform_num][1] = block_y
        platform_queue[platform_num][2] = block_width
        platform_queue[platform_num][3] = block_height

    # Add Platform Button Logic and Graphics
    if mouse_x >= add_dict['x'] and mouse_x <= add_dict['x'] + add_dict['width'] and mouse_y >= add_dict['y'] and mouse_y <= add_dict['y'] + add_dict["height"]:
        add_platform = pygame.image.load('add_platform.png').convert()
        add_platform = pygame.transform.smoothscale(add_platform, (add_dict['width'], add_dict['height']))
        if offset <= 3:
            offset += 1

        if mouse_c:
            if ready:
                offset = 0
                platform_queue.append([200, 200, 150, 150])
                print(platform_queue)
                ready = False
                if open == False:
                    open = True
                else:
                    open = False
        else:
            ready = True

        add_platform = pygame.transform.smoothscale(add_platform, (add_dict['width'] + offset * 2, add_dict['height'] + offset * 2))

    else:
        add_platform = pygame.image.load('add_platform.png').convert()
        add_platform = pygame.transform.smoothscale(add_platform, (add_dict['width'], add_dict['height']))
        if offset >= 0:
            offset -= 1

        add_platform = pygame.transform.smoothscale(add_platform, (add_dict['width'] + offset * 2, add_dict['height'] + offset * 2))


    # Play Button Logic and Graphics
    if mouse_x >= play_dict['x'] and mouse_x <= play_dict['x'] + play_dict['width'] and mouse_y >= play_dict['y'] and mouse_y <= play_dict['y'] + play_dict["height"]:
        play_button = pygame.image.load('play_button_new.png').convert()
        play_button = pygame.transform.smoothscale(play_button, (play_dict['width'], play_dict['height']))
        if offset2 <= 3:
            offset2 += 1

        if mouse_c:
            run = False

        play_button = pygame.transform.smoothscale(play_button, (play_dict['width'] + offset2 * 2, play_dict['height'] + offset2 * 2))

    else:
        play_button = pygame.image.load('play_button_new.png').convert()
        play_button = pygame.transform.smoothscale(play_button, (play_dict['width'], play_dict['height']))
        if offset2 >= 0:
            offset2 -= 1

        play_button = pygame.transform.smoothscale(play_button, (play_dict['width'] + offset2 * 2, play_dict['height'] + offset2 * 2))


    win.blit(logo, (logo_x, logo_y))
    if len(platform_queue) > 0:
        for platform in platform_queue:
            block_x = platform[0]
            block_y = platform[1]
            block_width = platform[2]
            block_height = platform[3]
            segment_a_bottom = [block_x, block_y + block_height - 10, block_width, 10]
            segment_b_right = [block_x + block_width - 10, block_y, 10, block_height]
            pygame.draw.rect(win, (0, 0, 255), platform)
            pygame.draw.rect(win, (255, 0, 0), segment_a_bottom)
            pygame.draw.rect(win, (0, 255, 0), segment_b_right)

    pygame.draw.rect(win, (255, 255, 255), (add_dict["x"] - offset * 1.5, add_dict["y"] - offset * 1.5, add_dict["width"] + offset * 3, add_dict["height"] + offset * 3), 2)
    pygame.draw.rect(win, (255, 255, 255), (play_dict["x"] - offset2 * 1.5, play_dict["y"] - offset2 * 1.5, play_dict["width"] + offset2 * 3, play_dict["height"] + offset2 * 3), 2)
    win.blit(add_platform, (add_dict['x'] - offset, add_dict['y'] - offset))
    win.blit(play_button, (play_dict['x'] - offset2, play_dict['y'] - offset2))

    pygame.display.update()

run = True

# Generating blocks
for platform in platform_queue:
    block_x = platform[0]
    block_y = platform[1]
    block_width = platform[2]
    block_height = platform[3]
    Platform.spawn(block_x, block_y, block_width, block_height)

for i in range(255):
    win.fill((i, i, i))
    pygame.display.update()

while run:
    pygame.time.delay(frame_speed)
    time.sleep(0.001)
    offset_x = x
    offset_y = y
    mX = pygame.mouse.get_pos()[0]
    mY = pygame.mouse.get_pos()[1]
    my_delta_x = x - mX + 20
    my_delta_y = y - mY - 20
    unit = ((-my_delta_x) / 5, (-my_delta_y) / 5)
    dot1 = (unit[0] * 1 + x + 5, unit[1] * 1 + y - 15)
    dot2 = (unit[0] * 2 + x + 5, unit[1] * 2 + y - 15)
    dot3 = (unit[0] * 3 + x + 5, unit[1] * 3 + y - 15)
    dot4 = (unit[0] * 4 + x + 5, unit[1] * 4 + y - 15)
    dot5 = (unit[0] * 5 + x + 5, unit[1] * 5 + y - 15)
    gun_x = x
    gun_y = y
    win.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if pygame.mouse.get_pressed()[0]: # Blue Portal Select
        portal_color = (0, 72, 132) # RGB - Blue
        if keys[pygame.K_q]:
            shot_orange = False
            shot_blue = True
            bW = portal_width
            bH = portal_height
            bX = portal_x
            bY = portal_y
            bD = portal_direction
        else:
            shot_blue = False
    elif pygame.mouse.get_pressed()[2]: # Orange Portal Select
        portal_color = (135, 78, 0) # RGB - Orange
        if keys[pygame.K_q]:
            shot_blue = False
            shot_orange = True
            oW = portal_width
            oH = portal_height
            oX = portal_x
            oY = portal_y
            oD = portal_direction
        else:
            shot_orange = False
    else:
        for platform in plane2D:
            if platform.touch(mX, mY):
                portal_color = (239, 38, 38) # RGB - Red
        shot_orange = False
        shot_blue = False
        portal_color = (0, 0, 0)

    if keys[pygame.K_e]:
        frame_speed = 10
    else:
        frame_speed = 1

    if keys[pygame.K_a] or keys[pygame.K_LEFT] and lateral_momentum > -vel:
        lateral_momentum -= 0.1 * friction
    elif keys[pygame.K_d] or keys[pygame.K_RIGHT] and lateral_momentum < vel:
        lateral_momentum += 0.1 * friction
    else:
        if lateral_momentum < -0.1:
            lateral_momentum += 0.1 * friction
        elif lateral_momentum > 0.1:
            lateral_momentum -= 0.1 * friction
        else:
            lateral_momentum = 0



    if grounded() and not keys[pygame.K_SPACE] and not touching_portal:
        if data == "object positional mode":
            print('Player: touching the ground')
        vertical_momentum = 0
        y = height
    elif grounded() and keys[pygame.K_SPACE]:
        if data == "object positional mode":
            print("Player: jumped from the ground")
        vertical_momentum = power
    else:
        if data == "object positional mode":
            print("Player: touching the air")
        vertical_momentum -= gravity

    touch_matrix = [(x, y), (x + 20, y), (x, y + 20), (x + 20, y + 20)]
    for j in touch_matrix:
        touching_portal = False
        bX_fit = j[0] >= bX and j[0] <= bX + bW
        bY_fit = j[1] >= bY and j[1] <= bY + bH + 30
        oX_fit = j[0] >= oX and j[0] <= oX + oW
        oY_fit = j[1] >= oY and j[1] <= oY + oH + 30
        if oX_fit and oY_fit:
            if data == "object positional mode":
                print('Player: touching the orange portal')
            teleport((oD, oX, oY), (bD, bX, bY))
            touching_portal = True
            break
        elif bX_fit and bY_fit:
            if data == "object positional mode":
                print('Player: touching the blue portal')
            teleport((bD, bX, bY), (oD, oX, oY))
            touching_portal = True
            break

    if data == "advanced object positional mode":
        print("Player: velocity({}), angle({})".format(lateral_momentum, angle))

    if barriers:
        if x > width - 20:
            x = width - 20
            lateral_momentum = 0
        elif x < 0:
            x = 0
            lateral_momentum = 0
    else:
        if x > width - 20:
            x = 0
        elif x < 0:
            x = width - 20


    if mX >= width - 40:
        if data == "portal positional mode":
            print("Mouse: touching right wall, mX:({}), mY:({}), shot:[blue:({}), orange:({})]".format(mX, mY, shot_blue, shot_orange))
        portal_there = True
        portal_width = 10
        portal_height = 100
        portal_direction = "right"
        if mY < height - portal_height:
            portal_y = mY
        portal_x = width - portal_width
    elif mX <= 40:
        if data == "portal positional mode":
            print("Mouse: touching left wall, mX:({}), mY:({}), shot:[blue:({}), orange:({})]".format(mX, mY, shot_blue, shot_orange))
        portal_there = True
        portal_width = 10
        portal_height = 100
        portal_direction = "left"
        if mY < height - portal_height:
            portal_y = mY
        portal_x = 0
    elif mY >= height - 40:
        if data == "portal positional mode":
            print("Mouse: touching floor, mX:({}), mY:({}), shot:[blue:({}), orange:({})]".format(mX, mY, shot_blue, shot_orange))
        portal_there = True
        portal_width = 100
        portal_height = 10
        portal_direction = "floor"
        portal_y = height - portal_height
        portal_x = mX
    elif mY <= 40:
        if data == "portal positional mode":
            print("Mouse: touching ceiling, mX:({}), mY:({}), shot:[blue:({}), orange:({})]".format(mX, mY, shot_blue, shot_orange))
        portal_there = True
        portal_width = 100
        portal_height = 10
        portal_direction = "ceiling"
        portal_y = 0
        portal_x = mX - portal_width / 2
    else:
        portal_there = False

    for platform in plane2D:
        if mY <= platform.y and mY >= platform.y - portal_height and mX >= platform.x + portal_width / 2 and mX <= platform.x + platform.width - portal_width / 2 and platform.width > 100:
            portal_there = True
            portal_width = 100
            portal_height = 10
            portal_direction = "floor"
            portal_x = mX - portal_width / 2
            portal_y = platform.y - portal_height
        elif mY <= platform.y + (platform.height + portal_height) and mY >= platform.y + 20 and mX >= platform.x + portal_width / 2 and mX <= platform.x + platform.width - portal_width / 2 and platform.width > 100:
            portal_there = True
            portal_width = 100
            portal_height = 10
            portal_direction = "ceiling"
            portal_x = mX - portal_width / 2
            portal_y = platform.y + portal_height + platform.height - 10
        elif mX <= platform.x and mX >= platform.x - portal_width - 20 and mY >= platform.y and mY <= platform.y + platform.height - portal_height / 2:
            portal_there = True
            portal_width = 10
            portal_height = 100
            portal_direction = "right"
            if mY < height - portal_height:
                portal_y = mY
            portal_x = platform.x - portal_width
        elif mX >= platform.x + platform.width and mX <= platform.x + platform.width + portal_width * 2 and mY >= platform.y + portal_width / 2 and mY <= platform.y + platform.height - portal_width / 2:
            portal_there = True
            portal_width = 10
            portal_height = 100
            portal_direction = "left"
            if mY < height - portal_height:
                portal_y = mY
            portal_x = platform.x + platform.width

    if data == "advanced portal positional mode":
        print("Player:(blue:({}, {}); orange:({}, {}))".format(bX, bY, oX, oY))

    for platform in plane2D:
        touch_matrix = [(x, y), (x + 20, y), (x, y + 20), (x + 20, y + 20)]
        first = platform.touch(touch_matrix[0][0], touch_matrix[0][1])
        second = platform.touch(touch_matrix[1][0], touch_matrix[1][1])
        third = platform.touch(touch_matrix[2][0], touch_matrix[2][1])
        fourth = platform.touch(touch_matrix[3][0], touch_matrix[3][1])
        if third and fourth and keys[pygame.K_SPACE]:
            vertical_momentum = power
            jumped = True
        else:
            jumped = False

        if not jumped:
            if second and fourth: # Touching left side
                x -= 1
                lateral_momentum = 0
            elif third and fourth: # Touching top side
                y = platform.y - 1
                vertical_momentum = 0
            elif first and second: # Touching bottom side
                y += 1
                vertical_momentum = 0
            elif first and third: # Touching right side
                x += 1
                lateral_momentum = 0
            elif fourth:
                x -= 1
                y -= 1


    y -= vertical_momentum
    x += lateral_momentum

    try:
        myAngle = math.degrees(math.atan(my_delta_y/my_delta_x))
    except:
        pass

    if myAngle < 0: # pointing towards top-left quadrant
        if my_delta_y < 0:
            print("left")
            if notflipped:
                final_blue_gun = pygame.transform.flip(blue_gun, True, False)
                final_orange_gun = pygame.transform.flip(orange_gun, True, False)
                final_white_gun = pygame.transform.flip(white_gun, True, False)
                gun_x -= 40
                notflipped = False
            move(myAngle, -300)
        else:
            print("right")
            notflipped = True
            move(myAngle, 180)
            final_blue_gun = blue_gun
            final_orange_gun = orange_gun
            final_white_gun = white_gun
    elif myAngle > 0: # pointing towards top-right quadrant
        if my_delta_y < 0:
            print("right")
            move(myAngle, 180)
            notflipped = True
            final_blue_gun = blue_gun
            final_orange_gun = orange_gun
            final_white_gun = white_gun
        else:
            print("left")
            if notflipped:
                final_blue_gun = pygame.transform.flip(blue_gun, True, False)
                final_orange_gun = pygame.transform.flip(orange_gun, True, False)
                final_white_gun = pygame.transform.flip(white_gun, True, False)
                gun_x -= 40
                notflipped = False
            move(myAngle, -300)

    try:
        pygame.draw.rect(win, (255, 148, 0), (oX, oY, oW, oH))
        pygame.draw.rect(win, (0, 140, 255), (bX, bY, bW, bH))
    except:
        pass
    pygame.draw.rect(win, (255, 0, 0), (x, y - 1, 20, -20))
    for platform in plane2D:
        pygame.draw.rect(win, (0, 0, 255), (platform.x, platform.y, platform.width, platform.height))

    temp_angle = 0
    final_blue_gun2 = pygame.transform.rotate(final_blue_gun, round(-myAngle))
    final_orange_gun2 = pygame.transform.rotate(final_orange_gun, round(-myAngle))
    final_white_gun2 = pygame.transform.rotate(final_white_gun, round(-myAngle))

    if portal_color == (0, 72, 132): # If color is blue
        win.blit(final_blue_gun2, (dot1[0] - 40, dot1[1] - 35))
        for platform in plane2D:
            if not platform.touch(mX, mY):
                win.blit(blue_circle, dot2)
                win.blit(blue_circle, dot3)
                win.blit(blue_circle, dot4)
                win.blit(blue_circle, dot5)

        if len(plane2D) == 0:
            win.blit(blue_circle, dot2)
            win.blit(blue_circle, dot3)
            win.blit(blue_circle, dot4)
            win.blit(blue_circle, dot5)
        '''blue_gun = pygame.transform.scale(blue_gun, (80, 70))
        win.blit(final_blue_gun2, (int(gun_x), int(gun_y)))'''
    elif portal_color == (135, 78, 0): # If color is orange
        win.blit(final_orange_gun2, (dot1[0] - 40, dot1[1] - 35))
        for platform in plane2D:
            if not platform.touch(mX, mY):
                win.blit(orange_circle, dot2)
                win.blit(orange_circle, dot3)
                win.blit(orange_circle, dot4)
                win.blit(orange_circle, dot5)

        if len(plane2D) == 0:
            win.blit(orange_circle, dot2)
            win.blit(orange_circle, dot3)
            win.blit(orange_circle, dot4)
            win.blit(orange_circle, dot5)

        '''orange_gun = pygame.transform.scale(orange_gun, (120, 105))
        win.blit(final_orange_gun2, (int(gun_x), int(gun_y)))'''
    elif portal_color == (0, 0, 0): # If color is white (no color)
        win.blit(final_white_gun2, (dot1[0] - 40, dot1[1] - 35))
        for platform in plane2D:
            if not platform.touch(mX, mY):
                win.blit(white_circle, dot2)
                win.blit(white_circle, dot3)
                win.blit(white_circle, dot4)
                win.blit(white_circle, dot5)

        if len(plane2D) == 0:
            win.blit(white_circle, dot2)
            win.blit(white_circle, dot3)
            win.blit(white_circle, dot4)
            win.blit(white_circle, dot5)
        '''white_gun = pygame.transform.scale(white_gun, (120, 105))
        win.blit(final_white_gun2, (int(gun_x), int(gun_y)))'''


    '''pygame.draw.rect(win, (80, 244, 66), (dot1[0], dot1[1], 5, -5))
    pygame.draw.rect(win, portal_color, (dot2[0], dot2[1], 5, -5))
    pygame.draw.rect(win, portal_color, (dot3[0], dot3[1], 5, -5))
    pygame.draw.rect(win, portal_color, (dot4[0], dot4[1], 5, -5))
    pygame.draw.rect(win, portal_color, (dot5[0], dot5[1], 5, -5))'''

    try:
        if portal_there:
            pygame.draw.rect(win, portal_color, (portal_x, portal_y, portal_width, portal_height))
    except:
        pass

    win.blit(mini_logo, (width - 100, -10))

    pygame.display.update()
