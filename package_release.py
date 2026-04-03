# Script para empacotar PSP Freeshop completo
import os
import shutil
import zipfile

def create_release_package():
    """Cria pacote completo para distribuição"""
    
    print("📦 Empacotando PSP Freeshop...")
    
    # Criar pasta de release
    release_dir = "PSP_Freeshop_Portable"
    if os.path.exists(release_dir):
        shutil.rmtree(release_dir)
    os.makedirs(release_dir)
    
    # Arquivos para copiar
    files_to_copy = [
        ("dist/PSPFreeshop.exe", "PSPFreeshop.exe"),
        ("PSP_GAMES.tsv", "PSP_GAMES.tsv"),
        ("pkg2zip.exe", "pkg2zip.exe"),
        ("downloads", "downloads"),
        ("covers_cache.json", "covers_cache.json"),
        ("README.md", "README.md"),
        ("COMO_USAR.md", "COMO_USAR.md")
    ]
    
    # Copiar arquivos
    for src, dst in files_to_copy:
        if os.path.exists(src):
            dst_path = os.path.join(release_dir, dst)
            if os.path.isfile(src):
                shutil.copy2(src, dst_path)
                print(f"📄 Arquivo: {dst}")
            else:
                if os.path.exists(dst_path):
                    shutil.rmtree(dst_path)
                shutil.copytree(src, dst_path)
                print(f"📁 Pasta: {dst}")
        else:
            print(f"❌ Não encontrado: {src}")
    
    # Criar instruções
    instructions = f"""
🎮 PSP FREESHOP - VERSÃO PORTÁVEL 🎮

📋 INSTRUÇÕES RÁPIDAS:
1. Extraia este arquivo em qualquer pasta
2. Execute PSPFreeshop.exe
3. Selecione o drive onde quer instalar os jogos
4. Baixe e instale seus jogos PSP!

📁 ESTRUTURA DE PASTAS:
├── PSPFreeshop.exe     # Aplicativo principal
├── PSP_GAMES.tsv         # Base de dados dos jogos
├── pkg2zip.exe          # Ferramenta de extração
├── downloads/            # Pasta de downloads temporários
├── covers_cache.json     # Cache de capas (opcional)
└── COMO_USAR.md        # Instruções detalhadas

⚠️  REQUISITOS:
- Windows 7 ou superior
- Drive USB ou pasta para jogos PSP
- Conexão com internet para downloads

🔧 CRIADO POR:
Sistema desenvolvido com Python + CustomTkinter
Download automático de jogos da PlayStation Store
Extração e instalação automática
Interface moderna e intuitiva

🚀 DIVIRTA-SE!
"""
    
    with open(os.path.join(release_dir, "LEIA-ME.txt"), "w", encoding="utf-8") as f:
        f.write(instructions)
    
    # Criar ZIP para distribuição
    zip_name = f"{release_dir}.zip"
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(release_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, release_dir)
                zipf.write(file_path, arcname)
    
    print(f"\n✅ Pacote criado: {zip_name}")
    print(f"📁 Tamanho: {os.path.getsize(zip_name) / (1024*1024):.1f} MB")
    print(f"\n🎉 PSP Freeshop Portable pronto para distribuição!")
    
    # Limpar pasta temporária
    shutil.rmtree(release_dir)
    
    return zip_name

if __name__ == "__main__":
    create_release_package()
