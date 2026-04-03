import os
import pathlib
import sys

def main():
    """
    Script para higienização do diretório de capas.
    Ele compara as capas presentes no diretório 'novas capas' com os IDs do arquivo 'PSP_GAMES.tsv'.
    Capas com IDs que não constam no arquivo TSV são permanentemente excluídas.
    """
    # Nomes padrão baseados na estrutura do projeto
    tsv_filename = "PSP_GAMES.tsv"
    covers_dirname = "novas capas"

    # Resolução dos caminhos
    base_dir = pathlib.Path(__file__).parent.resolve()
    tsv_path = base_dir / tsv_filename
    covers_path = base_dir / covers_dirname

    # Validação da existência do arquivo e diretório
    if not tsv_path.exists():
        print(f"Erro: O arquivo '{tsv_filename}' não foi encontrado em '{base_dir}'.")
        sys.exit(1)

    if not covers_path.exists() or not covers_path.is_dir():
        print(f"Erro: O subdiretório '{covers_dirname}' não foi encontrado em '{base_dir}'.")
        sys.exit(1)

    # 1. Extração de Dados: Armazena IDs num set nativo
    valid_ids: set[str] = set()
    try:
        # Lê o TSV assumindo encoding utf-8
        with open(tsv_path, 'r', encoding='utf-8') as f:
            for line_idx, line in enumerate(f):
                # Pula a primeira linha (cabeçalho)
                if line_idx == 0:
                    continue
                
                # O ID é a primeira coluna do TSV, separada por tabulação
                parts = line.split('\t')
                if len(parts) > 0:
                    # Remove eventuais espaços e normaliza para maiúsculo
                    title_id = parts[0].strip().upper()
                    if title_id:
                        valid_ids.add(title_id)
    except Exception as e:
        print(f"Erro inesperado ao ler o arquivo TSV: {e}")
        sys.exit(1)

    # 2. Varredura de Diretório
    total_checked = 0
    total_removed = 0

    try:
        # Itera sobre todos os arquivos dentro do diretório de capas
        for filepath in covers_path.iterdir():
            if filepath.is_file():
                total_checked += 1
                
                # 3. Validação: Apenas o nome do arquivo, ignorando a extensão
                # Exemplo: 'ULUS10041.jpg' -> stem = 'ULUS10041'
                image_id = filepath.stem.upper().strip()
                
                # 4. Exclusão (Orphans)
                if image_id not in valid_ids:
                    try:
                        filepath.unlink() # Exclusão definitiva (equivalente ao os.remove)
                        total_removed += 1
                    except PermissionError:
                        print(f"Aviso: Sem permissão para remover '{filepath.name}'. O arquivo pode estar em uso.")
                    except OSError as e:
                        # Trata outros erros relacionados a operação com arquivos
                        print(f"Erro ao tentar remover '{filepath.name}': {e}")
                        
    except Exception as e:
        print(f"Erro inesperado ao acessar o diretório de capas: {e}")
        sys.exit(1)

    # Finalização / Saída Esperada
    print("-" * 50)
    print(f"Total de capas verificadas: {total_checked} | Total de capas removidas: {total_removed}")
    print("-" * 50)

if __name__ == "__main__":
    main()
