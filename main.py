import constants as c
import pygame as pg
from enemy import Enemy

pg.init()

clock = pg.time.Clock()

screen = pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
pg.display.set_caption(c.TITLE)

waypoints = [
    (100, 100),
    (400, 200),
    (400, 100),
    (200, 300)
]

enemy_image = pg.image.load('assets/enemy/enemy1.png').convert_alpha()

enemy_group = pg.sprite.Group()

enemy = Enemy(waypoints, enemy_image)
enemy_group.add(enemy)


run = True
while run:

    clock.tick(c.FPS)

    screen.fill("grey100")

    pg.draw.lines(screen, "grey0", False, waypoints)

    enemy_group.update()

    enemy_group.draw(screen)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    pg.display.flip()

pg.quit()
