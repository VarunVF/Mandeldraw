import sys
from collections.abc import Callable

import pygame

import formulas
from formulas import mandelbrot


pygame.init()

SCALE = 0.004
SCREEN_SIZE = (800, 600)
SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_SIZE
MAX_DEPTH = 15
UPDATE_AFTER_LINES = 50
# shift coordinate system downward and rightward, as top-left is (0, 0)
X_SHIFT = -int(SCREEN_WIDTH / 2)
Y_SHIFT = -int(SCREEN_HEIGHT / 2)


def transform(x_coord: int,
              y_coord: int,
              scale: int = SCALE,
              x_shift: int = X_SHIFT,
              y_shift: int = Y_SHIFT) -> tuple[float, float]:
    """
    Transform the point by the desired translation (shift) and scale.
    The shift is applied before the scaling.
    :param x_coord: x-coordinate
    :param y_coord: y-coordinate
    :param scale: multiplier to scale by
    :param x_shift: horizontal translation
    :param y_shift: vertical translation
    :return: transformed coordinate point
    """
    x_coord = (x_coord + x_shift) * scale
    y_coord = (y_coord + y_shift) * scale
    return x_coord, y_coord


def color(surface: pygame.Surface,
          formula: Callable[[float, float, int], complex],
          max_depth: int = MAX_DEPTH,
          do_update: bool = True,
          update_after_lines: int = UPDATE_AFTER_LINES):
    """
    Colors a Surface based on existence in the Mandelbrot or multibrot set.
    Points that diverge at different depths will be colored differently.
    :param surface: surface to be colored
    :param formula: recursive formula to be used, in function form
    :param max_depth: maximum number of iterations for which the formula will be applied
    :param do_update: progressively update the surface as colors are calculated
    :param update_after_lines: number of lines after which to update the surface
    :return:
    """
    surface.lock()
    for x in range(surface.width):
        for y in range(surface.height):
            x_param, y_param = transform(x, y)
            for n in range(max_depth):
                r = 255 * (max_depth - n - 1) / max_depth
                if formula(x_param, y_param, n):
                    surface.set_at((x, y), (r, 0, 0))
        if do_update and x % update_after_lines == 0:
            pygame.display.update()
    surface.unlock()


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Mandelbrot Set Visualisation")
    clock = pygame.Clock()

    func = formulas.get_multibrot_func(2.3)
    color(screen, func)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)
