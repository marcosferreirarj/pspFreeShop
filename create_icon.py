# Criar ícone simples para o PSP Freeshop
from PIL import Image, ImageDraw
import os

def create_icon():
    """Cria um ícone simples para o PSP Freeshop"""
    
    # Criar imagem 64x64 com fundo transparente
    size = 64
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Desenhar fundo (círculo arredondado)
    draw.ellipse([8, 8, 56, 56], fill=(52, 152, 219))  # Azul PSP
    
    # Desenhar "PSP" em branco
    draw.text((32, 20), "PSP", fill=(255, 255, 255), anchor="mm")
    
    # Desenhar ícone de controle simples
    # Contorno do controle
    draw.rectangle([20, 32, 44, 44], fill=(255, 255, 255))
    draw.rectangle([22, 34, 42, 42], fill=(52, 152, 219))
    
    # Botões
    draw.ellipse([24, 36, 26, 38], fill=(200, 200, 200))  # Esquerdo
    draw.ellipse([38, 36, 40, 38], fill=(200, 200, 200))  # Direito
    draw.ellipse([30, 40, 34, 42], fill=(200, 200, 200))  # Cima
    draw.ellipse([34, 40, 38, 42], fill=(200, 200, 200))  # Baixo
    
    # Salvar como ICO
    img.save('icon.ico', format='ICO', sizes=[(32, 32), (64, 64)])
    print("✅ Ícone criado: icon.ico")

if __name__ == "__main__":
    try:
        from PIL import Image, ImageDraw
        create_icon()
    except ImportError:
        print("❌ PIL não instalado. Instale com:")
        print("pip install Pillow")
        # Criar ícone simples com ASCII arte
        with open('icon.txt', 'w') as f:
            f.write("""
    ____  ____ _    _    ____   ___    _  _     
   / __ \/ __ \| |  |  |  _ \ / __ \  / \| | |    
  |  |  |  | | |  | |_) | |__) |  | | |    
  |  |  |  | | |  |  _ < | _  | |  | | |    
   \____/\_____|_|_|  |____/ \___/  |_|_|_|    
            """)
        print("✅ Icon ASCII criado: icon.txt")
