import os
import json
import time

class CoverManager:
    def __init__(self):
        self.cache_dir = "covers_cache"
        self.covers_data_file = "covers_cache.json"
        self.covers_data = {}  # mantido vazio — funcionalidade desativada

        # Criar diretório de cache
        os.makedirs(self.cache_dir, exist_ok=True)

        # NÃO carrega covers_cache.json: o download de capas está desativado,
        # portanto não há motivo para alocar ~3-5 MB na RAM com esse JSON.
    
    def load_covers_data(self):
        """Carrega os dados de capas do arquivo JSON"""
        try:
            if os.path.exists(self.covers_data_file):
                with open(self.covers_data_file, 'r', encoding='utf-8') as f:
                    self.covers_data = json.load(f)
        except Exception as e:
            print(f"Erro ao carregar dados de capas: {e}")
            self.covers_data = {}
    
    def save_covers_data(self):
        """Salva os dados de capas no arquivo JSON"""
        try:
            with open(self.covers_data_file, 'w', encoding='utf-8') as f:
                json.dump(self.covers_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar dados de capas: {e}")
    
    def get_cover_path(self, title_id):
        """Retorna o caminho da capa em cache se existir"""
        cache_path = os.path.join(self.cache_dir, f"{title_id}.jpg")
        if os.path.exists(cache_path):
            return cache_path
        return None
    
    def download_cover(self, title_id, game_name, callback=None):
        """Cria placeholder simples sem processamento complexo"""
        # Simplesmente marca como processado e chama callback
        if callback:
            callback(title_id, None)  # None indica para usar placeholder
    
    def create_placeholder(self, title_id, game_name, callback=None):
        """Não cria mais placeholders complexos"""
        if callback:
            callback(title_id, None)
    
    def download_covers_batch(self, games, progress_callback=None):
        """Processa em batch sem criar arquivos"""
        total = len(games)
        for i, game in enumerate(games):
            if progress_callback:
                progress_callback(i + 1, total)
            # Simplesmente marca como processado
            time.sleep(0.001)  # Pequeno delay para não travar
    
    def preload_covers(self, games):
        """Não pré-carrega mais nada"""
        pass
