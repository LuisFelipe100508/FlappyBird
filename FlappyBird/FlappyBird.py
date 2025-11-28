import pygame
import random
import sys

pygame.init()

LARGURA_TELA = 600 
ALTURA_TELA = 550
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption('Flappy Bird Clone')

relogio = pygame.time.Clock()
FPS = 120 

pontuacao = 0
maior_pontuacao = 0
fonte = pygame.font.Font('freesansbold.ttf', 25)

Y_CHAO = ALTURA_TELA - 70 

superficie_fundo = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
superficie_fundo.fill((78, 192, 202)) 
superficie_chao = pygame.Surface((LARGURA_TELA * 2, 70))
superficie_chao.fill((218, 165, 32)) 
superficie_cano = pygame.Surface((52, 320))
superficie_cano.fill((0, 128, 0))

try:
    superficie_fundo = pygame.image.load('assets/background-day.png').convert()
    superficie_fundo = pygame.transform.scale(superficie_fundo, (LARGURA_TELA, ALTURA_TELA))
    
    superficie_cano = pygame.image.load('assets/pipe-green.png').convert_alpha()
    
except pygame.error as e:
    pass

posicao_x_chao = 0
lista_canos = []
alturas_cano = [200, 300, 400] 

GERAR_CANO = pygame.USEREVENT
pygame.time.set_timer(GERAR_CANO, 1200)

pode_pontuar = True

class Passaro(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        try:
            self.image = pygame.image.load('assets/bird.png').convert_alpha()
        except pygame.error:
            self.image = pygame.Surface((20, 20)) 
            self.image.fill((255, 255, 0)) 
        
        self.rect = self.image.get_rect(center=(50, ALTURA_TELA / 2))
        self.gravidade = 0.25
        self.movimento = 0
    
    def aplicar_gravidade(self):
        self.movimento += self.gravidade
        self.rect.centery += self.movimento

    def pular(self):
        self.movimento = -6

    def update(self):
        self.aplicar_gravidade()

def criar_cano():
    posicao_cano_aleatoria = random.choice(alturas_cano)
    cano_baixo = superficie_cano.get_rect(midtop=(LARGURA_TELA + 50, posicao_cano_aleatoria))
    cano_cima = superficie_cano.get_rect(midbottom=(LARGURA_TELA + 50, posicao_cano_aleatoria - 150))
    return cano_baixo, cano_cima

def mover_canos(canos):
    for cano in canos:
        cano.centerx -= 2
    return [cano for cano in canos if cano.right > -50]

def desenhar_canos(canos):
    for cano in canos:
        if cano.bottom >= ALTURA_TELA:
            tela.blit(superficie_cano, cano)
        else:
            cano_invertido = pygame.transform.flip(superficie_cano, False, True)
            tela.blit(cano_invertido, cano)

def verificar_colisao(canos):
    for cano in canos:
        if grupo_passaro.sprite.rect.colliderect(cano):
            return False
    
    if grupo_passaro.sprite.rect.top <= 0 or grupo_passaro.sprite.rect.bottom >= Y_CHAO:
        return False

    return True

def desenhar_chao():
    chao_largura = superficie_chao.get_width()
    tela.blit(superficie_chao, (posicao_x_chao, Y_CHAO))
    tela.blit(superficie_chao, (posicao_x_chao + chao_largura, Y_CHAO))

def checar_pontuacao():
    global pontuacao, pode_pontuar
    
    if lista_canos:
        cano_rect = lista_canos[0]
        
        if cano_rect.right < grupo_passaro.sprite.rect.left and pode_pontuar:
            pontuacao += 1
            pode_pontuar = False
        
        if cano_rect.right < 0:
             pode_pontuar = True

def desenhar_placar(estado_jogo):
    global maior_pontuacao
    
    if estado_jogo == 'ativo':
        texto_placar = fonte.render(str(pontuacao), True, (255, 255, 255))
        placar_rect = texto_placar.get_rect(center=(LARGURA_TELA / 2, 50))
        tela.blit(texto_placar, placar_rect)
        
    if estado_jogo == 'game_over':
        if pontuacao > maior_pontuacao:
            maior_pontuacao = pontuacao
            
        placar_final_texto = fonte.render(f'Score: {pontuacao}', True, (255, 255, 255))
        placar_final_rect = placar_final_texto.get_rect(center=(LARGURA_TELA / 2, ALTURA_TELA / 2 - 40))
        tela.blit(placar_final_texto, placar_final_rect)
        
        recorde_texto = fonte.render(f'Record: {maior_pontuacao}', True, (255, 255, 255))
        recorde_rect = recorde_texto.get_rect(center=(LARGURA_TELA / 2, ALTURA_TELA / 2 + 20))
        tela.blit(recorde_texto, recorde_rect)

passaro = Passaro()
grupo_passaro = pygame.sprite.GroupSingle(passaro)

jogo_ativo = True

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and jogo_ativo:
                passaro.pular()
            
            if evento.key == pygame.K_SPACE and jogo_ativo == False:
                jogo_ativo = True
                lista_canos.clear()
                grupo_passaro.sprite.rect.center = (50, ALTURA_TELA / 2)
                grupo_passaro.sprite.movimento = 0 
                pontuacao = 0 
                pode_pontuar = True 

        if evento.type == GERAR_CANO:
            if jogo_ativo:
                lista_canos.extend(criar_cano())

    tela.blit(superficie_fundo, (0, 0))

    if jogo_ativo:
        grupo_passaro.update()
        grupo_passaro.draw(tela)

        lista_canos = mover_canos(lista_canos)
        desenhar_canos(lista_canos)
        
        jogo_ativo = verificar_colisao(lista_canos)
        
        checar_pontuacao()
        desenhar_placar('ativo')

    else:
        desenhar_placar('game_over')

    chao_largura = superficie_chao.get_width()
    posicao_x_chao -= 1
    desenhar_chao()
    
    if posicao_x_chao <= -chao_largura:
        posicao_x_chao = 0

    pygame.display.update()
    relogio.tick(FPS)