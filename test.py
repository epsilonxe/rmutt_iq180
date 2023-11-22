import pygame
pygame.init()
window = pygame.display.set_mode((500, 100))
clock = pygame.time.Clock()
font_fade = pygame.USEREVENT + 1
pygame.time.set_timer(font_fade, 300)
font = pygame.font.SysFont(None, 40)
text_surf = font.render('press  any  button  to  start', True, (255, 255, 0), (0,0,0,20))    
show_text = True
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False     
        if event.type == font_fade:
            show_text = not show_text     
    window.fill(0)
    if show_text:
        window.blit(text_surf, text_surf.get_rect(center = window.get_rect().center))
    pygame.display.update()
    clock.tick(60)
pygame.quit()
exit()