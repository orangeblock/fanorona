import pygame
import game
import gfx

def main():
    pygame.init()
    gfx.init()
    game.init()
    
    while not game.finished:
        game.clock.tick(60)
        gfx.update()
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                # QUIT #
                game.finished = True
                break
            if game.current == game.player:
                # player's turn
                if event.type is pygame.MOUSEBUTTONDOWN and event.button == 1:
                    game.player_move(pygame.mouse.get_pos())
                if event.type is pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pass
                        
        if game.current == game.cpu:
            # computer's turn
            game.cpu_move()
        
        if game.game_over():
            game.finished = True
if __name__ == '__main__':
    main()