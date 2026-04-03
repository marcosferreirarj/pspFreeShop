import os
import sys
from PIL import Image

def comprimir_capas(pasta_entrada, pasta_saida):
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)

    arquivos = [f for f in os.listdir(pasta_entrada) if f.endswith('.png')]
    total_arquivos = len(arquivos)
    tamanho_original_total = 0
    tamanho_comprimido_total = 0
    
    print(f"Encontradas {total_arquivos} imagens em '{pasta_entrada}'. Iniciando compressão extrema...")
    
    for i, arquivo in enumerate(arquivos, 1):
        caminho_entrada = os.path.join(pasta_entrada, arquivo)
        caminho_saida = os.path.join(pasta_saida, arquivo)
        
        try:
            tamanho_original_total += os.path.getsize(caminho_entrada)
            
            with Image.open(caminho_entrada) as img:
                novo_tamanho = (max(1, img.width // 2), max(1, img.height // 2))
                img_resized = img.resize(novo_tamanho, Image.Resampling.LANCZOS)
                img_compressed = img_resized.convert("P", palette=Image.ADAPTIVE, colors=64)
                img_compressed.save(caminho_saida, format="PNG", optimize=True)
            
            tamanho_comprimido_total += os.path.getsize(caminho_saida)
                
            if i % 200 == 0 or i == total_arquivos:
                print(f"Progresso: {i}/{total_arquivos} imagens processadas.")
        except Exception as e:
            print(f"Erro ao comprimir {arquivo}: {e}")

    mb_original = tamanho_original_total / (1024 * 1024)
    mb_comprimido = tamanho_comprimido_total / (1024 * 1024)
    reducao_percentual = 100 - ((tamanho_comprimido_total / tamanho_original_total) * 100) if tamanho_original_total > 0 else 0
    
    print("\nResumo Final da Compressão Extrema:")
    print(f"Tamanho Original: {mb_original:.2f} MB")
    print(f"Tamanho Final Comprimido: {mb_comprimido:.2f} MB")
    print(f"Redução de tamanho real: {reducao_percentual:.2f}%")

if __name__ == "__main__":
    pasta_entrada = sys.argv[1] if len(sys.argv) > 1 else 'novas_capas'
    pasta_saida = sys.argv[2] if len(sys.argv) > 2 else 'novas_capas_compressed'
    comprimir_capas(pasta_entrada, pasta_saida)
