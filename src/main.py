import pygame
import game
import gfx

def main():
    pygame.init()
    pygame.display.set_caption("Fanorona v0.9")
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
                    game.player_move(game.grid.collision(pygame.mouse.get_pos()))
                if event.type is pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    game.finished = True
        
        if game.current == game.cpu and not game.game_over():
            # computer's turn
            game.cpu_move()
            
        if not game.moving and game.game_over():
            game.finished = True
            if game.winner == game.player:
                gfx.text = "YOU WIN!"
            else:
                gfx.text = "YOU LOSE!"
            quitting = False
            while not quitting:
                game.clock.tick(60)
                gfx.update()
                for event in pygame.event.get():
                    if event.type is pygame.QUIT:
                        quitting = True
                                    
if __name__ == '__main__':
    main()