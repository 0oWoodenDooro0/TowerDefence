import constants as c


class World:
    def __init__(self, map_image):
        self.tile_map = c.TILE_MAP
        self.waypoints = c.WAYPOINTS
        self.image = map_image

    def draw(self, surface):
        surface.blit(self.image, (0, 0))
