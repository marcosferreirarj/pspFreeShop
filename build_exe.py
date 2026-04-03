# Script para criar executável do PSP Freeshop
# Requerimentos: pip install pyinstaller

import os
import subprocess
import shutil

def create_exe():
    """Cria executável standalone do PSP Freeshop"""
    
    print("🔧 Criando executável do PSP Freeshop...")
    
    # Arquivos necessários
    required_files = [
        "main.py",
        "core.py", 
        "modern_ui.py",
        "cover_manager.py",
        "PSP_GAMES.tsv",
        "pkg2zip.exe",
        "run_psp_freeshop.py"
    ]
    
    # Verificar se todos os arquivos existem
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Arquivos faltando: {missing_files}")
        return False
    
    # Criar pasta dist se não existir
    if not os.path.exists("dist"):
        os.makedirs("dist")
    
    # Comando PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",           # Criar único executável
        "--windowed",          # Sem console
        "--name=PSPFreeshop", # Nome do executável
        "--icon=icon.ico",      # Ícone (se existir)
        "--add-data=PSP_GAMES.tsv;PSP_GAMES.tsv",  # Incluir TSV
        "--add-data=pkg2zip.exe;pkg2zip.exe",      # Incluir pkg2zip
        "--add-data=downloads;downloads",              # Incluir pasta downloads
        "--add-data=covers_cache.json;covers_cache.json", # Incluir cache
        "run_psp_freeshop.py"
    ]
    
    # Se não tiver ícone, remover opção
    if not os.path.exists("icon.ico"):
        cmd = [c for c in cmd if not c.startswith("--icon=")]
    
    try:
        print("📦 Executando PyInstaller...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Executável criado com sucesso!")
            print(f"📁 Local: dist/PSPFreeshop.exe")
            
            # Copiar arquivos necessários para pasta dist
            dist_files = [
                ("PSP_GAMES.tsv", "PSP_GAMES.tsv"),
                ("pkg2zip.exe", "pkg2zip.exe"),
                ("downloads", "downloads"),
                ("covers_cache.json", "covers_cache.json")
            ]
            
            for src, dst in dist_files:
                if os.path.exists(src):
                    dst_path = os.path.join("dist", dst)
                    if os.path.exists(dst_path):
                        if os.path.isfile(dst_path):
                            os.remove(dst_path)
                        else:
                            shutil.rmtree(dst_path)
                    
                    if os.path.isfile(src):
                        shutil.copy2(src, dst_path)
                    else:
                        shutil.copytree(src, dst_path)
                    print(f"📄 Copiado: {src} → dist/{dst}")
            
            print("\n🎮 PSP Freeshop.exe pronto para uso!")
            print("📁 Pasta completa: dist/")
            return True
        else:
            print(f"❌ Erro no PyInstaller: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ PyInstaller não encontrado. Instale com:")
        print("pip install pyinstaller")
        return False
    except Exception as e:
        print(f"❌ Erro ao criar executável: {e}")
        return False

if __name__ == "__main__":
    create_exe()
