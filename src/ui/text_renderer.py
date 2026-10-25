import pygame as pg


def draw_text(surface: pg.Surface, text: str, font: pg.font.Font, text_color, x: int, y: int, center: bool = False):
    """Renders and blits text to the specified surface."""
    img = font.render(text, True, text_color)
    if center:
        img_rect = img.get_rect(center=(x, y))
        surface.blit(img, img_rect)
    else:
        surface.blit(img, (x, y))
