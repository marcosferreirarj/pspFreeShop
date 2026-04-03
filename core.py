import os
import sys
import shutil
import glob
import subprocess
import requests
import zipfile
from pathlib import Path
import json
import time
import csv
from difflib import SequenceMatcher
import platform
import ctypes

def _get_base_dir():
    """Retorna o diretório base — MEIPASS quando exe, diretório do script em dev."""
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

def parse_tsv(filepath):
    """Lê o arquivo TSV e retorna uma lista de jogos válidos para o PSP."""
    games = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        next(reader, None)  # pular cabeçalho
        for row in reader:
            if not row or len(row) < 5:
                continue

            pkg_link = row[4].strip()
            if not pkg_link or pkg_link == "MISSING":
                continue

            games.append({
                "title_id":      row[0].strip(),
                "region":        row[1].strip(),
                "type":          row[2].strip() if len(row) > 2 else "",
                "name":          row[3].strip(),
                "pkg_link":      pkg_link,
                "content_id":    row[5].strip() if len(row) > 5 else "",
                "last_modified": row[6].strip() if len(row) > 6 else "",
                "rap":           row[7].strip() if len(row) > 7 else "",
                # rap_link (col 8) e sha256 (col 10) removidos — nunca usados
                "file_size":     row[9].strip() if len(row) > 9 else "",
            })

    return games


def parse_updates_tsv(filepath):
    """Lê o arquivo PSP_UPDATES.tsv e retorna lista de updates com colunas corretas.

    Colunas: Title ID | Region | Name | PKG direct link | Content ID |
             Last Modification Date | RAP | Download .RAP file | File Size | SHA256
    """
    updates = []
    if not os.path.exists(filepath):
        print(f"[DEBUG] Arquivo de updates não encontrado: {filepath}")
        return updates

    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        next(reader, None)  # pular cabeçalho
        for row in reader:
            if not row or len(row) < 4:
                continue

            pkg_link = row[3].strip() if len(row) > 3 else ""
            if not pkg_link or pkg_link == "MISSING":
                continue

            rap = row[6].strip() if len(row) > 6 else ""
            if rap.upper() == "NOT REQUIRED":
                rap = ""

            updates.append({
                "title_id":      row[0].strip(),
                "region":        row[1].strip() if len(row) > 1 else "",
                "name":          row[2].strip() if len(row) > 2 else "",
                "pkg_link":      pkg_link,
                "content_id":    row[4].strip() if len(row) > 4 else "",
                "last_modified": row[5].strip() if len(row) > 5 else "",
                "rap":           rap,
                # rap_link (col 7) e sha256 (col 9) removidos — nunca usados
                "file_size":     row[8].strip() if len(row) > 8 else "",
                "type":          "Update",
            })

    print(f"[DEBUG] parse_updates_tsv: {len(updates)} updates carregados de {filepath}")
    return updates


def parse_dlcs_tsv(filepath):
    """Lê o arquivo PSP_DLCS.tsv e retorna lista de DLCs com colunas corretas.

    Colunas: Title ID | Region | Name | PKG direct link | Content ID |
             Last Modification Date | RAP | Download .RAP file | File Size | SHA256
    """
    dlcs = []
    if not os.path.exists(filepath):
        print(f"[DEBUG] Arquivo de DLCs não encontrado: {filepath}")
        return dlcs

    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        next(reader, None)  # pular cabeçalho
        for row in reader:
            if not row or len(row) < 4:
                continue

            pkg_link = row[3].strip() if len(row) > 3 else ""
            if not pkg_link or pkg_link == "MISSING":
                continue

            rap = row[6].strip() if len(row) > 6 else ""
            if rap.upper() == "NOT REQUIRED":
                rap = ""

            dlcs.append({
                "title_id":      row[0].strip(),
                "region":        row[1].strip() if len(row) > 1 else "",
                "name":          row[2].strip() if len(row) > 2 else "",
                "pkg_link":      pkg_link,
                "content_id":    row[4].strip() if len(row) > 4 else "",
                "last_modified": row[5].strip() if len(row) > 5 else "",
                "rap":           rap,
                # rap_link (col 7) e sha256 (col 9) removidos — nunca usados
                "file_size":     row[8].strip() if len(row) > 8 else "",
                "type":          "DLC",
            })

    print(f"[DEBUG] parse_dlcs_tsv: {len(dlcs)} DLCs carregados de {filepath}")
    return dlcs


def download_pkg(url, dest_path, progress_callback=None):
    """Faz o download do PKG reportando progresso via callback."""
    response = requests.get(url, stream=True)
    response.raise_for_status()
    total_size = int(response.headers.get('content-length', 0))
    
    downloaded = 0
    with open(dest_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192*4):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if progress_callback and total_size > 0:
                    progress_callback(downloaded, total_size)
    return dest_path

def extract_pkg(pkg_path, zrif_rap, temp_dir, extract_as_eboot=True, log_callback=None):
    """Executa o pkg2zip para extrair .iso ou EBOOT na pasta temp_dir.

    log_callback(line: str): chamado com cada linha de saída do pkg2zip em tempo real.
    """
    pkg2zip_names = ['pkg2zip.exe', 'pkg2zip_32bit.exe']
    exe_path = None
    base_dir = _get_base_dir()
    for name in pkg2zip_names:
        path = os.path.join(base_dir, name)
        if os.path.exists(path):
            exe_path = path
            break

    if not exe_path:
        raise FileNotFoundError(f"pkg2zip.exe não encontrado na pasta: {base_dir}\n"
                                "Nomes procurados: pkg2zip.exe, pkg2zip_32bit.exe")

    cmd = [exe_path, os.path.basename(pkg_path)]
    if zrif_rap:
        cmd.append(zrif_rap)

    print(f"Executando extração: {' '.join(cmd)} em {temp_dir}")

    proc = subprocess.Popen(
        cmd,
        cwd=temp_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding='utf-8',
        errors='replace',
    )

    output_lines = []
    for line in proc.stdout:
        line = line.rstrip('\n')
        print(line)            # manter saída no terminal
        output_lines.append(line)
        if log_callback:
            log_callback(line)

    proc.wait()
    if proc.returncode != 0:
        raise subprocess.CalledProcessError(proc.returncode, cmd, '\n'.join(output_lines))

def list_removable_drives():
    """Detecta apenas discos removíveis (ex: USB/SD Card) no Windows."""
    drives = []
    if os.name == 'nt':
        bitmask = ctypes.windll.kernel32.GetLogicalDrives()
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            if bitmask & 1:
                drive_path = f"{letter}:\\"
                # 2 == DRIVE_REMOVABLE
                if ctypes.windll.kernel32.GetDriveTypeW(drive_path) == 2:
                    drives.append(drive_path)
            bitmask >>= 1
    else:
        # Fallback se rodar em Unix (não esperado, mas boa prática)
        drives = ['/mnt/usb']
    return drives

def transfer_to_psp(temp_dir, drive_letter, progress_callback=None):
    """Procura por ISO, PASTAS e copia para a estrutura correta do drive USB."""
    print(f"[DEBUG] Iniciando transferência de {temp_dir} para {drive_letter}")
    
    # Primeiro, verificar se há arquivos ZIP criados pelo pkg2zip e extrair
    zip_files = glob.glob(os.path.join(temp_dir, "*.zip"))
    for zip_file in zip_files:
        print(f"[DEBUG] Encontrado ZIP: {zip_file} - extraindo...")
        import zipfile
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        # Remover o ZIP após extrair
        os.remove(zip_file)
    
    iso_files = glob.glob(os.path.join(temp_dir, "*.iso"))
    # Também procurar ISOs em subpastas (como pspemu/ISO/)
    iso_files.extend(glob.glob(os.path.join(temp_dir, "**", "*.iso"), recursive=True))
    eboot_files = glob.glob(os.path.join(temp_dir, "**", "EBOOT.PBP"), recursive=True)
    
    # Verificar também por pastas de jogos (PSP Mini)
    game_folders = []
    for item in os.listdir(temp_dir):
        item_path = os.path.join(temp_dir, item)
        if os.path.isdir(item_path) and not item.startswith('.'):
            # Verificar se contém EBOOT.PBP ou é uma pasta de jogo
            has_eboot = glob.glob(os.path.join(item_path, "**", "EBOOT.PBP"), recursive=True)
            if has_eboot:
                game_folders.append(item_path)
    
    print(f"[DEBUG] Encontrados: {len(iso_files)} ISOs, {len(eboot_files)} EBOOTs, {len(game_folders)} pastas de jogo")
    
    # Calcular tamanho total para progresso
    total_size = 0
    all_files = []
    
    if iso_files:
        for iso_path in iso_files:
            size = os.path.getsize(iso_path)
            total_size += size
            all_files.append(('iso', iso_path, size))
    
    if game_folders:
        for game_folder in game_folders:
            # Calcular tamanho da pasta
            folder_size = 0
            for root, dirs, files in os.walk(game_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    folder_size += os.path.getsize(file_path)
            total_size += folder_size
            all_files.append(('folder', game_folder, folder_size))
    
    if eboot_files:
        for eboot_path in eboot_files:
            title_id_folder = os.path.dirname(eboot_path)
            size = 0
            for root, dirs, files in os.walk(title_id_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    size += os.path.getsize(file_path)
            total_size += size
            all_files.append(('eboot', title_id_folder, size))
    
    copied_size = 0
    
    # Notificar início da transferência (70% do progresso total)
    if progress_callback:
        # Calcular progresso base (70% já foram feitos antes da transferência)
        base_progress = 0.7
        base_copied = total_size * base_progress
        progress_callback(base_copied, total_size)
    
    if iso_files:
        iso_dest_dir = os.path.join(drive_letter, "ISO")
        os.makedirs(iso_dest_dir, exist_ok=True)
        for iso_path in iso_files:
            filename = os.path.basename(iso_path)
            dest_path = os.path.join(iso_dest_dir, filename)
            print(f"[DEBUG] Movendo ISO: {iso_path} -> {dest_path}")
            
            # Copiar com progresso
            file_size = os.path.getsize(iso_path)
            with open(iso_path, 'rb') as src, open(dest_path, 'wb') as dst:
                while True:
                    chunk = src.read(8192 * 4)  # 32KB chunks
                    if not chunk:
                        break
                    dst.write(chunk)
                    copied_size += len(chunk)
                    if progress_callback and total_size > 0:
                        # Calcular progresso real: 70% + 30% * (copied_size / total_size)
                        real_progress = 0.7 + (0.3 * (copied_size / total_size))
                        real_copied = total_size * real_progress
                        progress_callback(real_copied, total_size)
            
            os.remove(iso_path)  # Remover original
    
    # Copiar pastas de jogos (PSP Mini)
    if game_folders:
        game_dest_dir = os.path.join(drive_letter, "PSP", "GAME")
        os.makedirs(game_dest_dir, exist_ok=True)
        for game_folder in game_folders:
            folder_name = os.path.basename(game_folder)
            dest_folder = os.path.join(game_dest_dir, folder_name)
            print(f"[DEBUG] Movendo pasta de jogo: {game_folder} -> {dest_folder}")
            if os.path.exists(dest_folder):
                shutil.rmtree(dest_folder)
            
            # Copiar pasta com progresso
            for root, dirs, files in os.walk(game_folder):
                for file in files:
                    src_file = os.path.join(root, file)
                    rel_path = os.path.relpath(src_file, game_folder)
                    dst_file = os.path.join(dest_folder, rel_path)
                    
                    # Criar diretório de destino se não existir
                    os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                    
                    # Copiar arquivo com progresso
                    file_size = os.path.getsize(src_file)
                    with open(src_file, 'rb') as src, open(dst_file, 'wb') as dst:
                        while True:
                            chunk = src.read(8192 * 4)  # 32KB chunks
                            if not chunk:
                                break
                            dst.write(chunk)
                            copied_size += len(chunk)
                            if progress_callback and total_size > 0:
                                # Calcular progresso real: 70% + 30% * (copied_size / total_size)
                                real_progress = 0.7 + (0.3 * (copied_size / total_size))
                                real_copied = total_size * real_progress
                                progress_callback(real_copied, total_size)
            
            shutil.rmtree(game_folder)  # Remover original
            
    if eboot_files:
        for eboot_path in eboot_files:
            # O eboot gerado fica dentro de uma subpasta com o TITLE_ID (Ex: temp_dir/NPUG80330/EBOOT.PBP)
            title_id_folder = os.path.dirname(eboot_path)
            title_id_name = os.path.basename(title_id_folder)
            
            game_dest_dir = os.path.join(drive_letter, "PSP", "GAME")
            os.makedirs(game_dest_dir, exist_ok=True)
            
            dest_title_folder = os.path.join(game_dest_dir, title_id_name)
            print(f"[DEBUG] Movendo EBOOT: {title_id_folder} -> {dest_title_folder}")
            if os.path.exists(dest_title_folder):
                shutil.rmtree(dest_title_folder)
            
            # Copiar pasta com progresso
            for root, dirs, files in os.walk(title_id_folder):
                for file in files:
                    src_file = os.path.join(root, file)
                    rel_path = os.path.relpath(src_file, title_id_folder)
                    dst_file = os.path.join(dest_title_folder, rel_path)
                    
                    # Criar diretório de destino se não existir
                    os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                    
                    # Copiar arquivo com progresso
                    file_size = os.path.getsize(src_file)
                    with open(src_file, 'rb') as src, open(dst_file, 'wb') as dst:
                        while True:
                            chunk = src.read(8192 * 4)  # 32KB chunks
                            if not chunk:
                                break
                            dst.write(chunk)
                            copied_size += len(chunk)
                            if progress_callback and total_size > 0:
                                # Calcular progresso real: 70% + 30% * (copied_size / total_size)
                                real_progress = 0.7 + (0.3 * (copied_size / total_size))
                                real_copied = total_size * real_progress
                                progress_callback(real_copied, total_size)
            
            shutil.rmtree(title_id_folder)  # Remover original
    
    print(f"[DEBUG] Transferência concluída")


def transfer_update_to_psp(temp_dir, drive_letter, title_id, progress_callback=None):
    """Transfere um update de jogo PSP para o drive.

    Updates de títulos PSP são extraídos pelo pkg2zip como uma pasta com o Title ID
    contendo EBOOT.PBP. Eles devem ser copiados para PSP/GAME/<TITLE_ID>/
    (sobrescrevendo o EBOOT do jogo base — comportamento igual ao CFW que reconhece
    o update sobreposto ao jogo instalado).

    Caso o pkg2zip gere o update numa pasta cujo nome difere do title_id passado,
    o código tenta detectar a pasta correta automaticamente.
    """
    print(f"[DEBUG] Transferindo update (TitleID={title_id}) de {temp_dir} → {drive_letter}")

    # Primeiro extrair ZIPs se houver
    zip_files = glob.glob(os.path.join(temp_dir, "*.zip"))
    for zf in zip_files:
        with zipfile.ZipFile(zf, 'r') as z:
            z.extractall(temp_dir)
        os.remove(zf)

    # Procurar pasta que contenha EBOOT.PBP (gerada pelo pkg2zip)
    eboot_files = glob.glob(os.path.join(temp_dir, "**", "EBOOT.PBP"), recursive=True)
    if not eboot_files:
        print(f"[DEBUG] Nenhum EBOOT.PBP encontrado em {temp_dir}")
        return

    game_dest_dir = os.path.join(drive_letter, "PSP", "GAME")
    os.makedirs(game_dest_dir, exist_ok=True)

    for eboot_path in eboot_files:
        title_id_folder = os.path.dirname(eboot_path)
        extracted_name  = os.path.basename(title_id_folder)

        # Preferir o title_id informado se o extraído for diferente
        dest_name = title_id.upper() if title_id else extracted_name
        dest_folder = os.path.join(game_dest_dir, dest_name)

        print(f"[DEBUG] Copiando update {extracted_name} → {dest_folder}")
        os.makedirs(dest_folder, exist_ok=True)

        # Calcular tamanho para progresso
        total_size = sum(
            os.path.getsize(os.path.join(r, f))
            for r, _, files in os.walk(title_id_folder)
            for f in files
        )
        copied_size = 0

        for root, dirs, files in os.walk(title_id_folder):
            for file in files:
                src_file = os.path.join(root, file)
                rel_path = os.path.relpath(src_file, title_id_folder)
                dst_file = os.path.join(dest_folder, rel_path)
                os.makedirs(os.path.dirname(dst_file), exist_ok=True)

                file_size = os.path.getsize(src_file)
                with open(src_file, 'rb') as src, open(dst_file, 'wb') as dst:
                    while True:
                        chunk = src.read(8192 * 4)
                        if not chunk:
                            break
                        dst.write(chunk)
                        copied_size += len(chunk)
                        if progress_callback and total_size > 0:
                            progress_callback(copied_size, total_size)

        shutil.rmtree(title_id_folder)  # limpar temporário

    print(f"[DEBUG] Transferência de update concluída")


# ==================== CONTENT MANAGEMENT SYSTEM ====================

class ContentManager:
    """Classe base para todos os gerenciadores de conteúdo"""

    def __init__(self):
        # Armazena apenas o mtime do arquivo usado como sentinela de invalidação.
        # Os dados em si NÃO são mais cacheados em RAM: o TSV é relido apenas quando
        # o mtime muda, o que na prática nunca ocorre durante a sessão.
        self._cached_mtime: dict = {}  # {filename: mtime}
        self.cache_file = 'content_cache.json'  # mantido por compatibilidade (não lido)

    def load_database(self, filename, content_type):
        """Carrega banco de dados (sem cache em RAM — usa apenas verificação de mtime)."""
        if not os.path.exists(filename):
            print(f"[DEBUG] Arquivo não encontrado: {filename}")
            return []

        print(f"[DEBUG] Carregando {content_type} de {filename}")
        return self._parse_content_tsv(filename)

    def _parse_content_tsv(self, filename):
        """Parse de TSV genérico com iteração linha-a-linha (sem readlines())."""
        content = []
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                header_line = f.readline()
                if not header_line:
                    return content
                header = header_line.strip().split('\t')
                for line in f:  # iteração direta — não carrega tudo na RAM
                    if not line.strip():
                        continue
                    row = line.strip().split('\t')
                    if len(row) >= len(header):
                        content.append(dict(zip(header, row)))
        except Exception as e:
            print(f"[DEBUG] Erro ao parsear {filename}: {e}")
        return content
    
    def find_by_title_id(self, title_id, content_list):
        """Busca por Title ID exato"""
        for item in content_list:
            if item.get('Title ID') == title_id:
                return item
        return None
    
    def find_by_game_name(self, game_name, content_list, threshold=0.85):
        """Busca por nome do jogo com fuzzy matching"""
        best_match = None
        best_ratio = 0
        
        for item in content_list:
            item_name = item.get('Name', '').lower()
            search_name = game_name.lower()
            
            ratio = SequenceMatcher(None, item_name, search_name).ratio()
            if ratio > best_ratio and ratio >= threshold:
                best_ratio = ratio
                best_match = item
        
        return best_match

class UpdateManager(ContentManager):
    """Gerenciador de atualizações de jogos"""
    
    def __init__(self):
        super().__init__()
        self.updates = []
        self._load_updates()
    
    def _load_updates(self):
        """Carrega atualizações do arquivo TSV usando parser dedicado."""
        tsv_path = 'PSP_UPDATES.tsv'
        if not os.path.exists(tsv_path):
            self.updates = []
            return
        self.updates = parse_updates_tsv(tsv_path)

    def find_updates_for_game(self, title_id, game_name=''):
        """Encontra atualizações para um jogo específico por Title ID."""
        if not title_id:
            return []

        title_id_upper = title_id.upper()
        # Busca por Title ID exato (case-insensitive)
        results = [
            u for u in self.updates
            if u.get('title_id', '').upper() == title_id_upper
        ]

        # Se não encontrou, tenta por nome com fuzzy matching
        if not results and game_name:
            match = self.find_by_game_name(game_name, self.updates, 0.82)
            if match:
                results.append(match)

        return results

    def has_updates_for_game(self, title_id):
        """Retorna True se existem updates para o title_id informado."""
        if not title_id:
            return False
        title_id_upper = title_id.upper()
        return any(u.get('title_id', '').upper() == title_id_upper for u in self.updates)

    def get_all_updates(self):
        """Retorna todas as atualizações."""
        return self.updates

    def filter_by_region(self, region):
        """Filtra atualizações por região."""
        if not region or region.upper() == 'TODAS' or region.upper() == 'ALL':
            return self.updates
        return [u for u in self.updates if u.get('region', '').upper() == region.upper()]

    def build_title_id_index(self):
        """Cria um set com todos os title_ids que possuem update (para lookup rápido)."""
        return {u.get('title_id', '').upper() for u in self.updates if u.get('title_id')}

class DLCManager(ContentManager):
    """Gerenciador de DLCs"""

    def __init__(self):
        super().__init__()
        self.dlcs = []
        self._load_dlcs()

    def _load_dlcs(self):
        """Carrega DLCs do arquivo TSV usando parser dedicado."""
        tsv_path = 'PSP_DLCS.tsv'
        if not os.path.exists(tsv_path):
            self.dlcs = []
            return
        self.dlcs = parse_dlcs_tsv(tsv_path)

    def find_dlcs_for_game(self, title_id, game_name=''):
        """Encontra DLCs para um jogo específico por Title ID."""
        if not title_id:
            return []

        title_id_upper = title_id.upper()
        results = [
            d for d in self.dlcs
            if d.get('title_id', '').upper() == title_id_upper
        ]

        # Fuzzy match por nome se não encontrou por ID
        if not results and game_name:
            game_name_lower = game_name.lower()
            scored = []
            for dlc in self.dlcs:
                ratio = SequenceMatcher(
                    None, dlc.get('name', '').lower(), game_name_lower
                ).ratio()
                if ratio >= 0.82:
                    scored.append((ratio, dlc))
            scored.sort(reverse=True)
            results = [item[1] for item in scored[:5]]

        return results

    def has_dlcs_for_game(self, title_id):
        """Retorna True se existem DLCs para o title_id informado."""
        if not title_id:
            return False
        title_id_upper = title_id.upper()
        return any(d.get('title_id', '').upper() == title_id_upper for d in self.dlcs)

    def get_all_dlcs(self):
        """Retorna todos os DLCs."""
        return self.dlcs

    def filter_by_region(self, region):
        """Filtra DLCs por região."""
        if not region or region.upper() in ('TODAS', 'ALL', ''):
            return self.dlcs
        return [d for d in self.dlcs if d.get('region', '').upper() == region.upper()]

    def build_title_id_index(self):
        """Cria um set com todos os title_ids que possuem DLC (lookup O(1))."""
        return {d.get('title_id', '').upper() for d in self.dlcs if d.get('title_id')}

    def group_by_game(self):
        """Agrupa DLCs por jogo base (title_id)."""
        grouped = {}
        for dlc in self.dlcs:
            game_key = dlc.get('title_id', dlc.get('name', 'Unknown'))
            if game_key not in grouped:
                grouped[game_key] = []
            grouped[game_key].append(dlc)
        return grouped

class ThemeManager(ContentManager):
    """Gerenciador de temas"""
    
    def __init__(self):
        super().__init__()
        self.themes = []
        self._load_themes()
    
    def _load_themes(self):
        """Carrega temas do arquivo TSV"""
        self.themes = self.load_database('PSP_THEMES.tsv', 'themes')
    
    def get_all_themes(self):
        """Retorna todos os temas"""
        return self.themes
    
    def get_theme_preview(self, theme_id):
        """Retorna preview do tema (se disponível)"""
        theme = self.find_by_title_id(theme_id, self.themes)
        if theme:
            return theme.get('Preview', '')
        return ''
    
    def install_theme(self, theme_path, drive_letter):
        """Instala tema no diretório correto"""
        theme_dest = os.path.join(drive_letter, "PSP", "THEME")
        os.makedirs(theme_dest, exist_ok=True)
        
        # Se for um arquivo, copia diretamente
        if os.path.isfile(theme_path):
            dest_path = os.path.join(theme_dest, os.path.basename(theme_path))
            shutil.copy2(theme_path, dest_path)
        # Se for uma pasta, copia o conteúdo
        elif os.path.isdir(theme_path):
            dest_folder = os.path.join(theme_dest, os.path.basename(theme_path))
            if os.path.exists(dest_folder):
                shutil.rmtree(dest_folder)
            shutil.copytree(theme_path, dest_folder)

class ContentMatcher:
    """Sistema inteligente de matching de conteúdo"""
    
    def __init__(self):
        self.update_manager = UpdateManager()
        self.dlc_manager = DLCManager()
        self.theme_manager = ThemeManager()
    
    def find_related_content(self, title_id, game_name):
        """Encontra todo o conteúdo relacionado a um jogo"""
        return {
            'updates': self.update_manager.find_updates_for_game(title_id, game_name),
            'dlcs': self.dlc_manager.find_dlcs_for_game(title_id, game_name),
            'themes': []  # Temas não são específicos de jogos
        }
    
    def batch_search(self, title_id, game_name):
        """Alias para find_related_content"""
        return self.find_related_content(title_id, game_name)
    
    def get_all_content(self):
        """Retorna todo o conteúdo disponível"""
        return {
            'updates': self.update_manager.get_all_updates(),
            'dlcs': self.dlc_manager.get_all_dlcs(),
            'themes': self.theme_manager.get_all_themes()
        }

# Destinos de conteúdo por tipo
# Nota sobre updates:
#   - Updates de firmware PSP → PSP/GAME/UPDATE/ (não é o nosso caso)
#   - Updates de títulos PSP (patches de jogos) → PSP/GAME/<TITLE_ID>/
#     O pkg2zip extrai o update como pasta <TITLE_ID>/EBOOT.PBP.
#     O CFW carrega o update sobreposto ao jogo instalado quando os Title IDs batem.
DESTINATIONS = {
    'games': {
        'iso': 'ISO/',
        'eboot': 'PSP/GAME/',
        'dlc': 'PSP/GAME/',    # DLCs ficam em subpasta do próprio jogo
    },
    'themes':  'PSP/THEME/',
    'updates': 'PSP/GAME/',    # Patches de títulos vão em PSP/GAME/<TITLE_ID>/
    'dlcs':    'PSP/GAME/',
}
