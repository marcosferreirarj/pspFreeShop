# -*- mode: python ; coding: utf-8 -*-
import sys
import os

# Adicionar diretório atual ao path para encontrar os módulos
if getattr(sys, 'frozen', False):
    # Se estiver rodando como executável
    application_path = os.path.dirname(sys.executable)
    os.chdir(application_path)
else:
    # Se estiver rodando como script
    application_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(application_path)

# Adicionar o diretório ao path do Python
sys.path.insert(0, application_path)

# Importar e executar o aplicativo principal
try:
    import main
    app = main.PSPFreeshopApp()
    app.mainloop()
except ImportError as e:
    print(f"Erro ao importar módulos: {e}")
    print("Verifique se todos os arquivos estão na mesma pasta:")
    print("- main.py")
    print("- core.py") 
    print("- modern_ui.py")
    print("- cover_manager.py")
    print("- PSP_GAMES.tsv")
    print("- pkg2zip.exe")
    input("\nPressione Enter para sair...")
except Exception as e:
    print(f"Erro ao executar aplicação: {e}")
    input("\nPressione Enter para sair...")
