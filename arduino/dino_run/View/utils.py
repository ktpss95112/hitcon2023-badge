import pygame as pg

__image_cache = dict()


def load_image(path):
    global __image_cache
    if path in __image_cache:
        return __image_cache[path].copy()
    __image_cache[path] = pg.image.load(path)
    return __image_cache[path]


def scale_surface(surface, scale):
    try:
        return pg.transform.smoothscale(
            surface,
            (int(scale * surface.get_width()), int(scale * surface.get_height())),
        )
    except:
        return pg.transform.scale(
            surface,
            (int(scale * surface.get_width()), int(scale * surface.get_height())),
        )


def resize_surface(surface, width: int, height: int):
    try:
        return pg.transform.smoothscale(surface, (width, height))
    except:
        return pg.transform.scale(surface, (width, height))
