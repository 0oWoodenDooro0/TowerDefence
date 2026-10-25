import pygame as pg


class Scene:
    """Base interface for all game scenes."""

    def __init__(self, scene_manager):
        self.manager = scene_manager
        self.assets = scene_manager.assets
        self.save_manager = scene_manager.save_manager

    def on_enter(self, **kwargs):
        """Called when transitioning into this scene."""
        pass

    def on_exit(self):
        """Called when transitioning out of this scene."""
        pass

    def handle_event(self, event: pg.event.Event):
        """Processes individual pygame events."""
        pass

    def update(self, dt: float = 0.0):
        """Updates scene logic."""
        pass

    def draw(self, surface: pg.Surface):
        """Renders scene visuals to the target surface."""
        pass
