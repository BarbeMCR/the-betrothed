import pygame

"""A simple text wrapper derived from the one at https://www.pygame.org/wiki/TextWrap"""

def render(text, font, display_surface, rect, color, line_spacing=2, aa=False, bkg=None):
    """Render some text.

    Arguments:
    text -- the text to render
    font -- the font object
    display_surface -- the screen
    rect -- the bounding text rectangle
    color -- the text color
    line_spacing -- the pixels of spacing between lines
    aa -- antialiasing flag
    bkg -- the background color
    """
    rect = pygame.Rect(rect)
    y = rect.top
    font_height = font.size("Tg")[1]
    while text:
        i = 1
        # determine if the row of text will be outside our area
        if y + font_height > rect.bottom:
            break
        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1
        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1
        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)
        display_surface.blit(image, (rect.left, y))
        y += font_height + line_spacing
        # remove the text we just blitted
        text = text[i:]
    return text
