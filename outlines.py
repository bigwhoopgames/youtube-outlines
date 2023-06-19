import pygame

images = {}

class Outliner:
    
    def __init__(self):
        self.convolution_mask = pygame.mask.Mask((3, 3), fill = True)
        self.convolution_mask.set_at((0, 0), value = 0)
        self.convolution_mask.set_at((2, 0), value = 0)
        self.convolution_mask.set_at((0, 2), value = 0)
        self.convolution_mask.set_at((2, 2), value = 0)
    
    def outline_surface(self, surface, color = 'black', outline_only = False):
        
        mask = pygame.mask.from_surface(surface)
        
        surface_outline = mask.convolve(self.convolution_mask).to_surface(setcolor = color, unsetcolor = surface.get_colorkey())
        
        if outline_only:
            mask_surface = mask.to_surface()
            mask_surface.set_colorkey('black')
            
            surface_outline.blit(mask_surface, (1, 1))
            
        else:
            surface_outline.blit(surface, (1, 1))
        
        return surface_outline

class Game:
    def __init__(self):
        pygame.init()
        
        self.clock = pygame.time.Clock()
        self.running = False
        
        self.screen = pygame.display.set_mode((192, 108), flags = pygame.SCALED)

        self.outliner = Outliner()

        self.load_image('wabbit', colorkey = 'white')
        
        self.draw_pos = pygame.mouse.get_pos()
        
    def load_image(self, image_name, colorkey = None):
        
        image = pygame.image.load(f'{image_name}.png').convert()
        
        if colorkey is not None:
            image.set_colorkey(colorkey)
            
        images[image_name] = image
        images[f'{image_name}_outlined'] = self.outliner.outline_surface(image, color = 'black', outline_only = False)
        
    def update(self, dt):
        self.draw_pos = pygame.mouse.get_pos()
    
    def draw(self, surface):
        
        surface.fill('white')
        
        surface.blit(images['wabbit_outlined'], self.draw_pos)
        
        pygame.display.flip()
        
    def run(self):
        
        self.running = True
        
        while self.running:
            
            dt = self.clock.tick() * .001
            self.fps = self.clock.get_fps()
            pygame.display.set_caption(f'FPS: {self.fps}')
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
            
            self.update(dt)
            self.draw(self.screen)
        
        
if __name__ == '__main__':
    Game().run()