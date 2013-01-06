#
#
#    Helper functions used by the modules.
#
#
import pygame

def load_image(path):
    return pygame.image.load(path).convert_alpha()

def tsub(tup1, tup2):
    """ Subtracts tup1 elements from tup2 elements. """
    return (tup1[0]-tup2[0], tup1[1]-tup2[1])

def tadd(tup1, tup2):
    """ Adds the elements of tup1 and tup2. """
    return (tup1[0]+tup2[0], tup1[1]+tup2[1])

def tflip(tup):
    """
    Flips tuple elements.
    This is useful for list to screen coordinates translation.
    In list of lists: x = rows = vertical
    whereas on screen: x = horizontal
    """
    return (tup[1], tup[0])  