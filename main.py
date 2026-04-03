# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox, filedialog
import customtkinter as ctk
import os
import sys
import re
import threading
import time
import shutil
import glob
import subprocess
import requests
import platform
import csv
from PIL import Image, ImageTk
import core
from modern_ui import GameGrid

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

APP_VERSION = "1.0.0"

# ==================== PREMIUM COLOR PALETTE ====================

COLORS = {
    'bg_dark':        '#0f0f14',
    'bg_mid':         '#151520',
    'bg_card':        '#1e1e2e',
    'bg_card_hover':  '#252538',
    'sidebar':        '#0d0d18',
    'sidebar_active': '#1a1a2e',
    'border':         '#2a2a3e',
    'accent':         '#7c6cfc',
    'accent_hover':   '#9d8fff',
    'tab_store':      '#00d4aa',
    'tab_installed':  '#ff5566',
    'tab_updates':    '#7c6cfc',
    'tab_dlcs':       '#ffaa44',
    'tab_themes':     '#e67e22',
    'text':           '#e0e0ef',
    'text_muted':     '#7a7a9a',
    'text_dim':       '#3a3a5a',
    'success':        '#00d4aa',
    'error':          '#ff5566',
    'warning':        '#ffaa44',
}

def get_resource_path(filename):
    """Resolve caminho de arquivo tanto em dev quanto no exe empacotado"""
    if getattr(sys, 'frozen', False):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, filename)

TSV_FILE = get_resource_path("PSP_GAMES.tsv")
TEMP_DIR = "temp_dl"

# ==================== TRANSLATIONS ====================

TRANSLATIONS = {
    "pt": {
        # Janela principal
        "app_title": "PSP Freeshop Enhanced",

        # Abas
        "tab_store":     "🎮 Jogos da Loja",
        "tab_installed": "💾 Jogos Instalados",
        "tab_updates":   "🔄 Atualizações",
        "tab_dlcs":      "📦 DLCs",
        "tab_themes":    "🎨 Temas",

        # Diálogo de idioma
        "lang_dialog_title": "Selecionar Idioma",
        "lang_dialog_label": "Escolha o idioma da interface:",
        "lang_btn_pt": "🇧🇷 Português (Brasil)",
        "lang_btn_en": "🇺🇸 English",

        # Busca e filtros
        "search_label":       "🔍 Busca",
        "search_placeholder": "Buscar por nome...",
        "filter_type_label":  "📋 Tipo",
        "filter_region_label":"🌍 Região",
        "filter_sort_label":  "📊 Ordenar",
        "btn_clear_filters":  "🧹 Limpar Filtro",
        "all_types":          "Todas",
        "all_regions":        "Todas",
        "sort_name":          "Nome",
        "sort_size":          "Tamanho",
        "sort_region":        "Região",
        "sort_date":          "Data",

        # Botões de ação
        "btn_download_game":   "⬇️ BAIXAR JOGO",
        "btn_delete_game":     "🗑️ EXCLUIR JOGO",
        "btn_download_update": "⬇️ BAIXAR ATUALIZAÇÃO",
        "btn_download_dlc":    "⬇️ BAIXAR DLC",
        "btn_install_theme":   "⬇️ INSTALAR TEMA",

        # Paginação
        "btn_prev":  "◀ Anterior",
        "btn_next":  "Próxima ▶",
        "page_label": "Página {page}",
        "page_of":    "Página {page} / {total}",

        # Status
        "status_ready":           "PSP Freeshop pronto!",
        "status_loading_games":   "Carregando jogos...",
        "status_loading_updates": "Carregando atualizações...",
        "status_loading_dlcs":    "Carregando DLCs...",
        "status_loading_themes":  "Carregando temas...",
        "status_drive_selected":  "Drive PSP selecionado: {drive}",
        "status_no_drive":        "Nenhum drive USB encontrado",
        "status_drives_found":    "Drives encontrados: {count}",
        "status_scanning":        "🔍 Escaneando jogos instalados...",
        "status_installed_found": "✅ {count} jogos instalados encontrados",
        "status_select_drive":    "❌ Selecione um drive PSP primeiro!",
        "status_selected_count":  "📦 {count} jogo(s) selecionado(s)",
        "status_renamed":         "✏️ Renomeado: {name}",
        "status_opened_folder":   "📁 Aberto: {path}",
        "status_deleted":         "🗑️ '{name}' excluído",
        "status_deleted_count":   "🗑️ {count} jogo(s) excluído(s)",
        "status_ok_failures":     "⚠️ {ok} OK, {fail} falhas",
        "status_drive_sel":       "Drive selecionado: {drive}",
        "status_no_drive_sel":    "Nenhum drive selecionado",
        "status_filtered":        "Filtrados: {count} jogos",
        "status_games_page":      "{count} jogos — página {page}/{total}",
        "status_updates_region":  "Updates: {count} resultado(s) — Região: {region}",
        "status_dlcs_region":     "DLCs: {count} resultado(s) — Região: {region}",
        "status_loaded_updates":  "Carregados {count} updates",
        "status_loaded_dlcs":     "Carregados {count} DLCs",
        "status_loaded_themes":   "Carregados {count} temas",
        "status_downloading":     "📦 [{idx}/{total}] Baixando: {name}...",
        "status_dl_start":        "Iniciando download: {name}",
        "status_dl_start_batch":  "Iniciando download de {count} jogos...",
        "status_dl_items_ok":     "✅ {count} item(ns) baixado(s) com sucesso!",
        "status_dl_ok_fail":      "⚠️ {ok} OK, {fail} falhas",
        "status_dl_game_pct":     "⬇️ Baixando '{name}'... {pct}%",
        "status_extract_game":    "📦 Extraindo '{name}'...",
        "status_pkg2zip":         "📦 pkg2zip: {line}",
        "status_copy_game":       "💾 Copiando '{name}' para o console...",
        "status_copy_pct":        "💾 Copiando '{name}'... {pct}%",
        "status_dl_update_pct":   "⬇️ Baixando update '{name}'... {pct}%",
        "status_extract_update":  "📦 Extraindo update '{name}'...",
        "status_install_update":  "💾 Instalando update '{name}' em PSP/GAME/{tid}/...",
        "status_install_update_pct": "💾 Instalando update '{name}'... {pct}%",
        "status_update_done":     "✅ Update '{name}' instalado em PSP/GAME/{tid}/",
        "status_dl_dlc_pct":      "⬇️ Baixando DLC '{name}'... {pct}%",
        "status_extract_dlc":     "📦 Extraindo DLC '{name}'...",
        "status_install_dlc":     "💾 Instalando DLC '{name}' em PSP/GAME/{tid}/...",
        "status_install_dlc_pct": "💾 Instalando DLC '{name}'... {pct}%",
        "status_dlc_done":        "✅ DLC '{name}' instalado em PSP/GAME/{tid}/",
        "status_dl_theme_pct":    "⬇️ Baixando tema '{name}'... {pct}%",
        "status_extract_theme":   "📦 Extraindo tema '{name}'...",
        "status_install_theme_s": "💾 Instalando tema '{name}'...",
        "status_theme_done":      "✅ Tema '{name}' instalado em PSP/THEME/",
        "status_dl_game_legacy":  "Baixando {name}...",
        "status_extract_legacy":  "Extraindo {name}...",
        "status_copy_legacy":     "💾 Copiando para o console...",
        "status_dl_done_legacy":  "✅ Download e instalação concluídos: {name}",
        "status_dl_no_extract":   "⚠️ Download concluído (sem extração): {name}",
        "status_error":           "❌ {msg}",

        # Rodapé
        "drive_label":       "Drive:",
        "drive_not_sel":     "🎮 Drive: Não selecionado",
        "drive_sel":         "🎮 Drive: {drive}",
        "no_drives_found":   "Nenhum drive encontrado",
        "select_drive_btn":  "Selecionar drive",

        # Aba loja
        "installed_header":  "💾 Jogos Instalados no PSP",
        "btn_refresh":       "🔄 Atualizar",

        # Aba updates
        "updates_header":    "🔄 Atualizações Disponíveis",
        "region_label":      "Região:",
        "all_regions_combo": "Todas",

        # Aba DLCs
        "dlcs_header":       "📦 DLCs Disponíveis",
        "group_by_label":    "Agrupar por:",
        "group_all":         "Todos",
        "group_game":        "Jogo",
        "group_type":        "Tipo",

        # Aba Temas
        "themes_header":     "🎨 Temas Personalizados",
        "author_label":      "Autor:",
        "author_all":        "Todos",

        # Diálogo de drive
        "drive_method_title":  "Selecionar Drive PSP",
        "drive_method_label":  "Como deseja selecionar o drive?",
        "drive_method_search": "🔍 Procurar drive automaticamente",
        "drive_method_manual": "✏️ Informar unidade",
        "drive_dialog_title":  "Selecionar Drive PSP",
        "drive_dialog_label":  "🎮 Selecione o drive PSP:",
        "drive_btn":           "Drive {letter}",
        "no_usb_title":        "Drive PSP",
        "no_usb_msg":          "Nenhum drive USB encontrado.\nConecte seu PSP e selecione o manualmente.",
        "drive_manual_title":  "Informar Drive",
        "drive_manual_label":  "Digite a letra da unidade (ex: E):",
        "drive_manual_confirm":"Confirmar",
        "drive_manual_invalid":"Letra de unidade inválida ou drive não encontrado.",

        # Menu contexto
        "ctx_check_updates":     "🔄 Verificar Updates",
        "ctx_see_updates":       "🔄 Ver Updates Disponíveis",
        "ctx_check_dlcs":        "🎮 Verificar DLCs",
        "ctx_see_dlcs":          "🎮 Ver DLCs Disponíveis",
        "ctx_delete":            "🗑️ Excluir '{name}'",
        "ctx_rename":            "✏️ Renomear Jogo",
        "ctx_open_location":     "📁 Abrir Local do Arquivo",
        "ctx_game_info":         "📋 Ver Informações",

        # Diálogo Renomear
        "rename_title":     "Renomear Jogo",
        "rename_new_name":  "Novo nome:",
        "btn_rename_ok":    "✅ Renomear",
        "btn_cancel":       "❌ Cancelar",

        # Informações do jogo
        "game_info_title":   "Informações do Jogo",
        "info_name":         "Nome: {value}",
        "info_title_id":     "Title ID: {value}",
        "info_region":       "Região: {value}",
        "info_type":         "Tipo: {value}",
        "info_size":         "Tamanho: {value} bytes",
        "info_path":         "Caminho: {value}",
        "info_has_updates":  "\n🔄 Updates disponíveis para este jogo!",
        "info_has_dlcs":     "\n🎮 DLCs disponíveis para este jogo!",

        # Modal DLCs para jogo
        "dlc_modal_title":   "🎮 DLCs — {name}",
        "dlc_modal_header":  "🎮 {count} DLC(s) disponível(is) para {name}",
        "date_unknown":      "Data desconhecida",
        "btn_dl_selected":   "⬇️ Baixar Selecionados",
        "btn_close":         "❌ Fechar",

        # Modal Updates para jogo
        "upd_modal_title":   "🔄 Updates — {name}",
        "upd_modal_header":  "🔄 {count} update(s) disponível(is) para {name}",

        # Avisos
        "warn_select_game":      "Selecione um jogo primeiro!",
        "warn_select_dlc":       "Selecione pelo menos um DLC!",
        "warn_select_update":    "Selecione pelo menos um update!",
        "warn_name_empty":       "Nome não pode estar vazio!",
        "warn_no_drive":         "Selecione um drive PSP primeiro!",

        # Erros
        "err_no_path":           "Caminho do jogo não encontrado!",
        "err_rename":            "Falha ao renomear: {msg}",
        "err_open_folder":       "Falha ao abrir pasta: {msg}",
        "err_delete":            "Falha ao excluir: {msg}",
        "err_no_dl_link":        "Link de download não disponível!",
        "err_load_games":        "Falha ao carregar jogos: {msg}",
        "err_tsv_not_found":     "Arquivo {file} não encontrado!",
        "err_dl_error":          "Erro no download: {msg}",
        "err_no_link_game":      "Link de download não disponível",
        "err_no_link_update":    "Update '{name}': link de download não disponível",
        "err_no_link_dlc":       "DLC '{name}': link de download não disponível",
        "err_no_link_theme":     "Tema '{name}': link de download não disponível",

        # Confirmações
        "confirm_download_title":  "Confirmar Download",
        "confirm_download_msg":    "Baixar '{name}'?",
        "confirm_dl_batch_title":  "Confirmar Download em Lote",
        "confirm_dl_batch_msg":    "Baixar {count} jogos?\n\n{names}",
        "confirm_delete_title":    "Confirmar Exclusão",
        "confirm_delete_msg":      "Tem certeza que deseja excluir '{name}'?\n\nEsta ação não pode ser desfeita!",
        "confirm_del_batch_title": "Confirmar Exclusão em Lote",
        "confirm_del_batch_msg":   "Tem certeza que deseja excluir {count} jogos?\n\n{names}\n\nEsta ação não pode ser desfeita!",
        "more_items":              "... e mais {count} jogos",
        "more_errors":             "... e mais {count} erros",

        # Sucesso
        "success_title":         "Sucesso",
        "success_renamed":       "Jogo renomeado com sucesso!\n'{old}' → '{new}'",
        "success_deleted":       "'{name}' foi excluído com sucesso!",
        "success_deleted_count": "{count} jogos excluídos com sucesso!",
        "success_dl_all":        "Todos os {count} itens foram baixados e instalados!",
        "success_dl_game":       "Jogo baixado e instalado com sucesso!\n{name}",

        # Aviso de falhas
        "warn_done_failures":    "Concluído com Falhas",
        "warn_failures_msg":     "{ok} jogos OK, {fail} falhas:\n\n{errors}",
        "warn_dl_failures":      "{ok} item(ns) OK, {fail} falha(s)",
        "warn_pkg_no_extract":   "Jogo baixado mas não foi possível extrair.\nArquivo PKG salvo em ISO/",

        # Modal de Update (antigo NotificationManager)
        "update_modal_title":    "🔄 Atualizações Disponíveis",
        "update_modal_header":   "🔄 Atualizações para {name}",
        "btn_dl_selected_ok":    "✅ Baixar Selecionados",
        "dlc_toast_title":       "📦 DLCs Disponíveis",
        "dlc_toast_msg":         "📦 Este jogo possui {count} DLC(s) disponíveis!",
        "dlc_toast_sub":         "Confira a aba de DLCs para mais detalhes.",

        # Busca legacy DLC/Update sem resultado
        "no_dlc_title":          "DLCs",
        "no_dlc_msg":            "Nenhum DLC encontrado para '{name}'\n(Title ID: {tid})",
        "no_update_title":       "Updates",
        "no_update_msg":         "Nenhum update encontrado para '{name}'\n(Title ID: {tid})",
    },

    "en": {
        # Main window
        "app_title": "PSP Freeshop Enhanced",

        # Tabs
        "tab_store":     "🎮 Store",
        "tab_installed": "💾 Installed",
        "tab_updates":   "🔄 Updates",
        "tab_dlcs":      "📦 DLCs",
        "tab_themes":    "🎨 Themes",

        # Language dialog
        "lang_dialog_title": "Select Language",
        "lang_dialog_label": "Choose interface language:",
        "lang_btn_pt": "🇧🇷 Português (Brasil)",
        "lang_btn_en": "🇺🇸 English",

        # Search and filters
        "search_label":       "🔍 Search",
        "search_placeholder": "Search by name...",
        "filter_type_label":  "📋 Type",
        "filter_region_label":"🌍 Region",
        "filter_sort_label":  "📊 Sort",
        "btn_clear_filters":  "🧹 Clear Filters",
        "all_types":          "All",
        "all_regions":        "All",
        "sort_name":          "Name",
        "sort_size":          "Size",
        "sort_region":        "Region",
        "sort_date":          "Date",

        # Action buttons
        "btn_download_game":   "⬇️ DOWNLOAD GAME",
        "btn_delete_game":     "🗑️ DELETE GAME",
        "btn_download_update": "⬇️ DOWNLOAD UPDATE",
        "btn_download_dlc":    "⬇️ DOWNLOAD DLC",
        "btn_install_theme":   "⬇️ INSTALL THEME",

        # Pagination
        "btn_prev":   "◀ Previous",
        "btn_next":   "Next ▶",
        "page_label": "Page {page}",
        "page_of":    "Page {page} / {total}",

        # Status
        "status_ready":           "PSP Freeshop ready!",
        "status_loading_games":   "Loading games...",
        "status_loading_updates": "Loading updates...",
        "status_loading_dlcs":    "Loading DLCs...",
        "status_loading_themes":  "Loading themes...",
        "status_drive_selected":  "PSP drive selected: {drive}",
        "status_no_drive":        "No USB drive found",
        "status_drives_found":    "Drives found: {count}",
        "status_scanning":        "🔍 Scanning installed games...",
        "status_installed_found": "✅ {count} installed game(s) found",
        "status_select_drive":    "❌ Please select a PSP drive first!",
        "status_selected_count":  "📦 {count} game(s) selected",
        "status_renamed":         "✏️ Renamed: {name}",
        "status_opened_folder":   "📁 Opened: {path}",
        "status_deleted":         "🗑️ '{name}' deleted",
        "status_deleted_count":   "🗑️ {count} game(s) deleted",
        "status_ok_failures":     "⚠️ {ok} OK, {fail} failures",
        "status_drive_sel":       "Drive selected: {drive}",
        "status_no_drive_sel":    "No drive selected",
        "status_filtered":        "Filtered: {count} games",
        "status_games_page":      "{count} games — page {page}/{total}",
        "status_updates_region":  "Updates: {count} result(s) — Region: {region}",
        "status_dlcs_region":     "DLCs: {count} result(s) — Region: {region}",
        "status_loaded_updates":  "Loaded {count} updates",
        "status_loaded_dlcs":     "Loaded {count} DLCs",
        "status_loaded_themes":   "Loaded {count} themes",
        "status_downloading":     "📦 [{idx}/{total}] Downloading: {name}...",
        "status_dl_start":        "Starting download: {name}",
        "status_dl_start_batch":  "Starting download of {count} games...",
        "status_dl_items_ok":     "✅ {count} item(s) downloaded successfully!",
        "status_dl_ok_fail":      "⚠️ {ok} OK, {fail} failures",
        "status_dl_game_pct":     "⬇️ Downloading '{name}'... {pct}%",
        "status_extract_game":    "📦 Extracting '{name}'...",
        "status_pkg2zip":         "📦 pkg2zip: {line}",
        "status_copy_game":       "💾 Copying '{name}' to console...",
        "status_copy_pct":        "💾 Copying '{name}'... {pct}%",
        "status_dl_update_pct":   "⬇️ Downloading update '{name}'... {pct}%",
        "status_extract_update":  "📦 Extracting update '{name}'...",
        "status_install_update":  "💾 Installing update '{name}' to PSP/GAME/{tid}/...",
        "status_install_update_pct": "💾 Installing update '{name}'... {pct}%",
        "status_update_done":     "✅ Update '{name}' installed to PSP/GAME/{tid}/",
        "status_dl_dlc_pct":      "⬇️ Downloading DLC '{name}'... {pct}%",
        "status_extract_dlc":     "📦 Extracting DLC '{name}'...",
        "status_install_dlc":     "💾 Installing DLC '{name}' to PSP/GAME/{tid}/...",
        "status_install_dlc_pct": "💾 Installing DLC '{name}'... {pct}%",
        "status_dlc_done":        "✅ DLC '{name}' installed to PSP/GAME/{tid}/",
        "status_dl_theme_pct":    "⬇️ Downloading theme '{name}'... {pct}%",
        "status_extract_theme":   "📦 Extracting theme '{name}'...",
        "status_install_theme_s": "💾 Installing theme '{name}'...",
        "status_theme_done":      "✅ Theme '{name}' installed to PSP/THEME/",
        "status_dl_game_legacy":  "Downloading {name}...",
        "status_extract_legacy":  "Extracting {name}...",
        "status_copy_legacy":     "💾 Copying to console...",
        "status_dl_done_legacy":  "✅ Download and install complete: {name}",
        "status_dl_no_extract":   "⚠️ Download complete (no extraction): {name}",
        "status_error":           "❌ {msg}",

        # Footer
        "drive_label":       "Drive:",
        "drive_not_sel":     "🎮 Drive: Not selected",
        "drive_sel":         "🎮 Drive: {drive}",
        "no_drives_found":   "No drive found",
        "select_drive_btn":  "Select drive",

        # Installed tab
        "installed_header":  "💾 Games Installed on PSP",
        "btn_refresh":       "🔄 Refresh",

        # Updates tab
        "updates_header":    "🔄 Available Updates",
        "region_label":      "Region:",
        "all_regions_combo": "All",

        # DLCs tab
        "dlcs_header":       "📦 Available DLCs",
        "group_by_label":    "Group by:",
        "group_all":         "All",
        "group_game":        "Game",
        "group_type":        "Type",

        # Themes tab
        "themes_header":     "🎨 Custom Themes",
        "author_label":      "Author:",
        "author_all":        "All",

        # Drive dialog
        "drive_method_title":  "Select PSP Drive",
        "drive_method_label":  "How do you want to select the drive?",
        "drive_method_search": "🔍 Search drive automatically",
        "drive_method_manual": "✏️ Specify drive",
        "drive_dialog_title":  "Select PSP Drive",
        "drive_dialog_label":  "🎮 Select the PSP drive:",
        "drive_btn":           "Drive {letter}",
        "no_usb_title":        "PSP Drive",
        "no_usb_msg":          "No USB drive found.\nConnect your PSP and select it manually.",
        "drive_manual_title":  "Specify Drive",
        "drive_manual_label":  "Enter drive letter (e.g.: E):",
        "drive_manual_confirm":"Confirm",
        "drive_manual_invalid":"Invalid drive letter or drive not found.",

        # Context menu
        "ctx_check_updates":     "🔄 Check for Updates",
        "ctx_see_updates":       "🔄 View Available Updates",
        "ctx_check_dlcs":        "🎮 Check for DLCs",
        "ctx_see_dlcs":          "🎮 View Available DLCs",
        "ctx_delete":            "🗑️ Delete '{name}'",
        "ctx_rename":            "✏️ Rename Game",
        "ctx_open_location":     "📁 Open File Location",
        "ctx_game_info":         "📋 View Info",

        # Rename dialog
        "rename_title":     "Rename Game",
        "rename_new_name":  "New name:",
        "btn_rename_ok":    "✅ Rename",
        "btn_cancel":       "❌ Cancel",

        # Game info
        "game_info_title":   "Game Info",
        "info_name":         "Name: {value}",
        "info_title_id":     "Title ID: {value}",
        "info_region":       "Region: {value}",
        "info_type":         "Type: {value}",
        "info_size":         "Size: {value} bytes",
        "info_path":         "Path: {value}",
        "info_has_updates":  "\n🔄 Updates available for this game!",
        "info_has_dlcs":     "\n🎮 DLCs available for this game!",

        # DLC modal for game
        "dlc_modal_title":   "🎮 DLCs — {name}",
        "dlc_modal_header":  "🎮 {count} DLC(s) available for {name}",
        "date_unknown":      "Unknown date",
        "btn_dl_selected":   "⬇️ Download Selected",
        "btn_close":         "❌ Close",

        # Updates modal for game
        "upd_modal_title":   "🔄 Updates — {name}",
        "upd_modal_header":  "🔄 {count} update(s) available for {name}",

        # Warnings
        "warn_select_game":      "Please select a game first!",
        "warn_select_dlc":       "Please select at least one DLC!",
        "warn_select_update":    "Please select at least one update!",
        "warn_name_empty":       "Name cannot be empty!",
        "warn_no_drive":         "Please select a PSP drive first!",

        # Errors
        "err_no_path":           "Game path not found!",
        "err_rename":            "Failed to rename: {msg}",
        "err_open_folder":       "Failed to open folder: {msg}",
        "err_delete":            "Failed to delete: {msg}",
        "err_no_dl_link":        "Download link not available!",
        "err_load_games":        "Failed to load games: {msg}",
        "err_tsv_not_found":     "File {file} not found!",
        "err_dl_error":          "Download error: {msg}",
        "err_no_link_game":      "Download link not available",
        "err_no_link_update":    "Update '{name}': download link not available",
        "err_no_link_dlc":       "DLC '{name}': download link not available",
        "err_no_link_theme":     "Theme '{name}': download link not available",

        # Confirmations
        "confirm_download_title":  "Confirm Download",
        "confirm_download_msg":    "Download '{name}'?",
        "confirm_dl_batch_title":  "Confirm Batch Download",
        "confirm_dl_batch_msg":    "Download {count} games?\n\n{names}",
        "confirm_delete_title":    "Confirm Delete",
        "confirm_delete_msg":      "Are you sure you want to delete '{name}'?\n\nThis action cannot be undone!",
        "confirm_del_batch_title": "Confirm Batch Delete",
        "confirm_del_batch_msg":   "Are you sure you want to delete {count} games?\n\n{names}\n\nThis action cannot be undone!",
        "more_items":              "... and {count} more games",
        "more_errors":             "... and {count} more errors",

        # Success
        "success_title":         "Success",
        "success_renamed":       "Game renamed successfully!\n'{old}' → '{new}'",
        "success_deleted":       "'{name}' was deleted successfully!",
        "success_deleted_count": "{count} games deleted successfully!",
        "success_dl_all":        "All {count} items were downloaded and installed!",
        "success_dl_game":       "Game downloaded and installed successfully!\n{name}",

        # Failure warnings
        "warn_done_failures":    "Completed with Failures",
        "warn_failures_msg":     "{ok} games OK, {fail} failures:\n\n{errors}",
        "warn_dl_failures":      "{ok} item(s) OK, {fail} failure(s)",
        "warn_pkg_no_extract":   "Game downloaded but extraction failed.\nPKG file saved to ISO/",

        # Update modal (NotificationManager)
        "update_modal_title":    "🔄 Available Updates",
        "update_modal_header":   "🔄 Updates for {name}",
        "btn_dl_selected_ok":    "✅ Download Selected",
        "dlc_toast_title":       "📦 DLCs Available",
        "dlc_toast_msg":         "📦 This game has {count} DLC(s) available!",
        "dlc_toast_sub":         "Check the DLCs tab for more details.",

        # No DLC/Update found
        "no_dlc_title":          "DLCs",
        "no_dlc_msg":            "No DLC found for '{name}'\n(Title ID: {tid})",
        "no_update_title":       "Updates",
        "no_update_msg":         "No update found for '{name}'\n(Title ID: {tid})",
    },
}

# ==================== NOTIFICATION SYSTEM ====================

class NotificationManager:
    """Sistema de notificações expandido"""

    def __init__(self, parent):
        self.parent = parent
        self.active_toasts = []
        self.active_modals = []

    def show_update_modal(self, game, updates):
        """Modal interativo para updates"""
        modal = ctk.CTkToplevel(self.parent)
        modal.title(self.parent.t('update_modal_title'))
        modal.geometry("500x400")
        modal.transient(self.parent)
        modal.grab_set()

        # Centralizar
        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - (500 // 2)
        y = (modal.winfo_screenheight() // 2) - (400 // 2)
        modal.geometry(f"500x400+{x}+{y}")

        # Header
        ctk.CTkLabel(
            modal,
            text=self.parent.t('update_modal_header', name=game.get('name', 'Game')),
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#7c6cfc"
        ).pack(pady=15)

        # Lista de updates
        scroll_frame = ctk.CTkScrollableFrame(modal, height=200)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

        selected_updates = []

        for i, update in enumerate(updates):
            update_frame = ctk.CTkFrame(scroll_frame)
            update_frame.pack(fill="x", pady=5)

            # Checkbox para seleção
            var = ctk.BooleanVar(value=True)
            checkbox = ctk.CTkCheckBox(
                update_frame,
                text="",
                variable=var
            )
            checkbox.pack(side="left", padx=10)

            # Info do update
            info_text = f"📦 {update.get('Name', 'Unknown')}\n"
            info_text += f"📅 {update.get('Last Modification Date', 'Unknown')}\n"
            info_text += f"💾 {self._format_size(update.get('File Size', '0'))}"

            ctk.CTkLabel(
                update_frame,
                text=info_text,
                font=ctk.CTkFont(size=11),
                justify="left"
            ).pack(side="left", padx=10)

            selected_updates.append({'update': update, 'var': var})

        # Botões
        btn_frame = ctk.CTkFrame(modal, fg_color="transparent")
        btn_frame.pack(pady=15)

        result = {'download': False, 'updates': []}

        def confirm():
            result['download'] = True
            result['updates'] = [item['update'] for item in selected_updates if item['var'].get()]
            modal.destroy()

        def cancel():
            modal.destroy()

        ctk.CTkButton(
            btn_frame,
            text=self.parent.t('btn_dl_selected_ok'),
            fg_color="#00d4aa",
            hover_color="#00b894",
            corner_radius=8,
            command=confirm,
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            btn_frame,
            text=self.parent.t('btn_cancel'),
            fg_color="#ff5566",
            hover_color="#dd4455",
            corner_radius=8,
            command=cancel,
        ).pack(side="left", padx=10)

        modal.wait_window()
        return result

    def show_dlc_toast(self, dlc_count):
        """Toast informativo para DLCs"""
        toast = ctk.CTkToplevel(self.parent)
        toast.title(self.parent.t('dlc_toast_title'))
        toast.geometry("400x120")
        toast.overrideredirect(True)

        # Centralizar na parte superior
        toast.update_idletasks()
        x = (toast.winfo_screenwidth() // 2) - (400 // 2)
        y = 100  # 100px do topo
        toast.geometry(f"400x120+{x}+{y}")

        # Estilo do toast
        toast_frame = ctk.CTkFrame(toast, fg_color="#2c3e50", corner_radius=10)
        toast_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(
            toast_frame,
            text=self.parent.t('dlc_toast_msg', count=dlc_count),
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ecf0f1"
        ).pack(pady=10)

        ctk.CTkLabel(
            toast_frame,
            text=self.parent.t('dlc_toast_sub'),
            font=ctk.CTkFont(size=12),
            text_color="#bdc3c7"
        ).pack(pady=5)

        # Auto-fechar após 4 segundos
        self.parent.after(4000, toast.destroy)

        self.active_toasts.append(toast)

    def _format_size(self, size_str):
        """Formata tamanho do arquivo"""
        try:
            size_bytes = int(size_str)
            if size_bytes >= 1024*1024*1024:
                return f"{size_bytes/(1024*1024*1024):.1f} GB"
            elif size_bytes >= 1024*1024:
                return f"{size_bytes/(1024*1024):.1f} MB"
            elif size_bytes >= 1024:
                return f"{size_bytes/1024:.1f} KB"
            else:
                return f"{size_bytes} bytes"
        except:
            return size_str


class PSPFreeshopApp(ctk.CTk):
    """Aplicação PSP Freeshop com 5 abas independentes"""

    def __init__(self):
        super().__init__()

        # Idioma padrão (será perguntado ao inicializar)
        self.lang = "pt"

        # Configuração da janela
        self.title("PSP Freeshop Enhanced")
        self.geometry("1200x900")
        self.configure(fg_color=COLORS['bg_dark'])

        # Dados
        self.all_games = []
        self.filtered_games = []
        self.selected_game = None
        self.selected_games_list = []  # Lista de jogos selecionados para download em lote
        self.current_page = 1
        self.games_per_page = 50
        self.view_mode = "store"
        self.selected_drive_path = None
        self._update_title_ids = set()  # title_ids com update disponível
        self._dlc_title_ids    = set()  # title_ids com DLC disponível
        self.all_dlcs_data = []         # todos os DLCs carregados
        self.dlc_page = 1               # página atual da aba DLC
        self.all_installed_games = []   # lista completa (não filtrada) dos jogos instalados

        # UI
        self._create_ui()

        # Carregar dados
        self.after(100, self._initialize_app)

    def t(self, key, **kwargs):
        """Retorna texto traduzido para o idioma atual."""
        lang = getattr(self, 'lang', 'pt')
        text = TRANSLATIONS.get(lang, TRANSLATIONS['pt']).get(
            key, TRANSLATIONS['pt'].get(key, key)
        )
        return text.format(**kwargs) if kwargs else text

    def _initialize_app(self):
        """Inicializa aplicação com pop-up de idioma, caminho e carregamento"""
        # Mostrar diálogo de seleção de idioma
        self._show_language_dialog()

        # Atualizar textos da UI após escolha do idioma
        self._apply_language_to_ui()

        # Mostrar pop-up para encontrar caminho de instalação
        self._show_path_dialog()

        # Carregar jogos após definir o caminho
        self._load_games()

    def _show_language_dialog(self):
        """Mostra diálogo de seleção de idioma — bloqueante até o usuário escolher."""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Language / Idioma")
        dialog.geometry("400x200")
        dialog.transient(self)
        dialog.grab_set()
        dialog.resizable(False, False)

        # Impede fechar sem escolher
        dialog.protocol("WM_DELETE_WINDOW", lambda: None)

        # Centralizar
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - 200
        y = (dialog.winfo_screenheight() // 2) - 100
        dialog.geometry(f"400x200+{x}+{y}")

        ctk.CTkLabel(
            dialog,
            text="Language / Idioma",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).pack(pady=(25, 10))

        ctk.CTkLabel(
            dialog,
            text="Choose interface language / Escolha o idioma da interface:",
            font=ctk.CTkFont(size=12),
            text_color="#aaaaaa",
        ).pack(pady=(0, 15))

        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack()

        def choose(lang):
            self.lang = lang
            dialog.destroy()

        ctk.CTkButton(
            btn_frame,
            text="🇧🇷 Português (Brasil)",
            width=160,
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=lambda: choose("pt"),
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            btn_frame,
            text="🇺🇸 English",
            width=160,
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=lambda: choose("en"),
        ).pack(side="left", padx=10)

        dialog.wait_window()

    def _setup_tabs(self):
        """Cria frames de aba e botões da sidebar com os nomes no idioma atual."""
        self.TAB_STORE     = self.t('tab_store')
        self.TAB_INSTALLED = self.t('tab_installed')
        self.TAB_UPDATES   = self.t('tab_updates')
        self.TAB_DLCS      = self.t('tab_dlcs')
        self.TAB_THEMES    = self.t('tab_themes')

        # Limpar frames e botões existentes
        for frame in list(self.tab_frames.values()):
            frame.destroy()
        self.tab_frames.clear()

        for btn in list(self.sidebar_btns.values()):
            btn.destroy()
        self.sidebar_btns.clear()

        # Configuração: (nome, cor_acento)
        tab_configs = [
            (self.TAB_STORE,     COLORS['tab_store']),
            (self.TAB_INSTALLED, COLORS['tab_installed']),
            (self.TAB_UPDATES,   COLORS['tab_updates']),
            (self.TAB_DLCS,      COLORS['tab_dlcs']),
            (self.TAB_THEMES,    COLORS['tab_themes']),
        ]

        for tab_name, color in tab_configs:
            frame = ctk.CTkFrame(self.tab_container, fg_color="transparent")
            self.tab_frames[tab_name] = frame

            btn = ctk.CTkButton(
                self.sidebar_nav,
                text=f"  {tab_name}",
                anchor="w",
                height=42,
                fg_color="transparent",
                hover_color=COLORS['sidebar_active'],
                text_color=COLORS['text_muted'],
                font=ctk.CTkFont(size=13),
                corner_radius=8,
                command=lambda name=tab_name: self._switch_tab(name),
            )
            btn.pack(fill="x", padx=10, pady=2)
            self.sidebar_btns[tab_name] = btn

        self._setup_store_tab()
        self._setup_installed_tab()

        self.notification_manager = NotificationManager(self)
        self.content_matcher = core.ContentMatcher()

        self._setup_updates_tab()
        self._setup_dlcs_tab()
        self._setup_themes_tab()

        self._switch_tab(self.TAB_STORE)

    def _switch_tab(self, tab_name):
        """Mostra o frame da aba selecionada e atualiza o estilo da sidebar."""
        for frame in self.tab_frames.values():
            frame.pack_forget()

        if tab_name in self.tab_frames:
            self.tab_frames[tab_name].pack(fill="both", expand=True)

        self._current_tab = tab_name

        tab_accent = {
            self.TAB_STORE:     COLORS['tab_store'],
            self.TAB_INSTALLED: COLORS['tab_installed'],
            self.TAB_UPDATES:   COLORS['tab_updates'],
            self.TAB_DLCS:      COLORS['tab_dlcs'],
            self.TAB_THEMES:    COLORS['tab_themes'],
        }

        for name, btn in self.sidebar_btns.items():
            if name == tab_name:
                color = tab_accent.get(name, COLORS['accent'])
                btn.configure(fg_color=COLORS['sidebar_active'], text_color=color)
            else:
                btn.configure(fg_color="transparent", text_color=COLORS['text_muted'])

        self._on_tab_change()

    def _apply_language_to_ui(self):
        """Atualiza os textos da UI principal após definição do idioma."""
        self._setup_tabs()
        self.title(self.t('app_title'))

        # Status inicial
        self.status_label.configure(text=self.t('status_ready'))

        # Drive path label
        self.drive_path_label.configure(text=self.t('drive_not_sel'))

        # Drive combo placeholder
        self.drive_combo.set(self.t('select_drive_btn'))

        # Botão de ação inicial
        self.action_btn.configure(text=self.t('btn_download_game'))

        # Labels de filtro
        # (os labels já foram criados; reconfigurar texto)
        self.search_label_widget.configure(text=self.t('search_label'))
        self.search_entry.configure(placeholder_text=self.t('search_placeholder'))
        self.filter_type_label_widget.configure(text=self.t('filter_type_label'))
        self.filter_region_label_widget.configure(text=self.t('filter_region_label'))
        self.filter_sort_label_widget.configure(text=self.t('filter_sort_label'))
        
        if hasattr(self, 'clear_filters_btn'):
            self.clear_filters_btn.configure(text=self.t('btn_clear_filters'))

        # Valores dos filtros
        all_types   = self.t('all_types')
        all_regions = self.t('all_regions')
        self.type_filter.configure(values=[all_types])
        self.type_filter.set(all_types)
        self.region_filter.configure(values=[all_regions])
        self.region_filter.set(all_regions)
        self.sort_filter.configure(values=[
            self.t('sort_name'), self.t('sort_size'),
            self.t('sort_region'), self.t('sort_date')
        ])
        self.sort_filter.set(self.t('sort_name'))

        # Botões de paginação da loja
        self.store_prev_btn.configure(text=self.t('btn_prev'))
        self.store_next_btn.configure(text=self.t('btn_next'))
        self.store_page_label.configure(text=self.t('page_label', page=1))

        # Botões de paginação DLC
        self.dlc_prev_btn.configure(text=self.t('btn_prev'))
        self.dlc_next_btn.configure(text=self.t('btn_next'))
        self.dlc_page_label.configure(text=self.t('page_label', page=1))

        # Drive label rodapé
        self.drive_label.configure(text=self.t('drive_label'))

    def _show_path_dialog(self):
        """Mostra diálogo para selecionar caminho de instalação"""
        # Primeiro perguntar ao usuário como deseja selecionar o drive
        method_dialog = ctk.CTkToplevel(self)
        method_dialog.title(self.t('drive_method_title'))
        method_dialog.geometry("400x180")
        method_dialog.transient(self)
        method_dialog.grab_set()
        method_dialog.resizable(False, False)

        method_dialog.update_idletasks()
        x = (method_dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (method_dialog.winfo_screenheight() // 2) - (180 // 2)
        method_dialog.geometry(f"400x180+{x}+{y}")

        ctk.CTkLabel(
            method_dialog,
            text=self.t('drive_method_label'),
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(20, 15))

        choice = {'value': None}

        def pick_search():
            choice['value'] = 'search'
            method_dialog.destroy()

        def pick_manual():
            choice['value'] = 'manual'
            method_dialog.destroy()

        btn_frame = ctk.CTkFrame(method_dialog, fg_color="transparent")
        btn_frame.pack(pady=5)

        ctk.CTkButton(
            btn_frame,
            text=self.t('drive_method_search'),
            width=180,
            command=pick_search
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            btn_frame,
            text=self.t('drive_method_manual'),
            width=180,
            command=pick_manual
        ).pack(side="left", padx=10)

        method_dialog.wait_window()

        if choice['value'] == 'search':
            self._show_drive_search_dialog()
        elif choice['value'] == 'manual':
            self._show_drive_manual_dialog()

    def _show_drive_search_dialog(self):
        """Procura drives automaticamente e apresenta opções"""
        usb_drives = self._find_usb_drives()

        if usb_drives:
            dialog = ctk.CTkToplevel(self)
            dialog.title(self.t('drive_dialog_title'))
            dialog.geometry("400x200")
            dialog.transient(self)
            dialog.grab_set()

            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
            y = (dialog.winfo_screenheight() // 2) - (200 // 2)
            dialog.geometry(f"400x200+{x}+{y}")

            ctk.CTkLabel(
                dialog,
                text=self.t('drive_dialog_label'),
                font=ctk.CTkFont(size=16, weight="bold")
            ).pack(pady=20)

            for drive in usb_drives:
                ctk.CTkButton(
                    dialog,
                    text=self.t('drive_btn', letter=drive),
                    width=300,
                    command=lambda d=drive: self._select_drive(d, dialog)
                ).pack(pady=5)

            dialog.wait_window()
        else:
            messagebox.showinfo(
                self.t('no_usb_title'),
                self.t('no_usb_msg')
            )

    def _show_drive_manual_dialog(self):
        """Permite ao usuário informar a letra da unidade manualmente"""
        dialog = ctk.CTkToplevel(self)
        dialog.title(self.t('drive_manual_title'))
        dialog.geometry("360x200")
        dialog.transient(self)
        dialog.grab_set()
        dialog.resizable(False, False)

        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (360 // 2)
        y = (dialog.winfo_screenheight() // 2) - (200 // 2)
        dialog.geometry(f"360x200+{x}+{y}")

        ctk.CTkLabel(
            dialog,
            text=self.t('drive_manual_label'),
            font=ctk.CTkFont(size=13)
        ).pack(pady=(25, 8))

        # Montar lista de drives existentes para o combo
        all_drives = [f"{l}" for l in "CDEFGHIJKLMNOPQRSTUVWXYZ"
                      if os.path.exists(f"{l}:\\")]
        drive_var = ctk.StringVar(value=all_drives[0] if all_drives else "E")

        combo = ctk.CTkComboBox(
            dialog,
            values=all_drives,
            variable=drive_var,
            width=200
        )
        combo.pack(pady=5)

        def confirm():
            letter = drive_var.get().strip().upper().rstrip(':\\')
            drive_path = f"{letter}:\\"
            if len(letter) == 1 and letter.isalpha() and os.path.exists(drive_path):
                self._select_drive(letter, dialog)
            else:
                messagebox.showwarning(
                    self.t('drive_manual_title'),
                    self.t('drive_manual_invalid')
                )

        ctk.CTkButton(
            dialog,
            text=self.t('drive_manual_confirm'),
            width=160,
            command=confirm
        ).pack(pady=15)

        dialog.wait_window()

    def _find_usb_drives(self):
        """Procura por drives USB que possam ser PSP"""
        possible_drives = []
        for letter in ['D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']:
            drive_path = f"{letter}:\\"
            if os.path.exists(drive_path):
                # Verificar se parece ser um PSP (tem pasta ISO ou PSP)
                iso_path = os.path.join(drive_path, "ISO")
                psp_path = os.path.join(drive_path, "PSP")
                if os.path.exists(iso_path) or os.path.exists(psp_path):
                    possible_drives.append(letter)
        return possible_drives

    def _select_drive(self, drive_letter, dialog):
        """Seleciona o drive e fecha o diálogo"""
        self.selected_drive_path = f"{drive_letter}:\\"

        # Atualizar status
        self.status_label.configure(text=self.t('status_drive_selected', drive=drive_letter + ':'))

        # Atualizar caminho no rodapé
        self.drive_path_label.configure(text=self.t('drive_sel', drive=self.selected_drive_path))

        # Sincronizar combo box do rodapé
        self.drive_combo.set(self.selected_drive_path)

        # Atualizar card de drive na sidebar
        if hasattr(self, 'sidebar_drive_label'):
            self.sidebar_drive_label.configure(text=self.selected_drive_path)

        dialog.destroy()

    def _update_drives(self):
        """Atualiza lista de drives USB"""
        drives = []
        for letter in ['C', 'D', 'E', 'F', 'G', 'H']:
            drive_path = f"{letter}:\\"
            if os.path.exists(drive_path):
                drives.append(drive_path)

        if drives:
            self.drive_combo.configure(values=drives)
            self.status_label.configure(text=self.t('status_drives_found', count=len(drives)))
        else:
            self.drive_combo.configure(values=[self.t('no_drives_found')])
            self.status_label.configure(text=self.t('status_no_drive'))

    def _create_ui(self):
        """Cria interface do usuário com layout sidebar + conteúdo premium"""
        self.configure(fg_color=COLORS['bg_dark'])

        # ── LAYOUT PRINCIPAL ────────────────────────────────────────────────
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True)

        # ── SIDEBAR (esquerda, 210px fixo) ──────────────────────────────────
        self.sidebar = ctk.CTkFrame(
            main_container,
            width=210,
            fg_color=COLORS['sidebar'],
            corner_radius=0,
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent", height=72)
        logo_frame.pack(fill="x")
        logo_frame.pack_propagate(False)
        ctk.CTkLabel(
            logo_frame,
            text="PSP",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=COLORS['accent'],
        ).pack(side="left", padx=(20, 0), pady=10)
        ctk.CTkLabel(
            logo_frame,
            text="freeshop",
            font=ctk.CTkFont(size=13),
            text_color=COLORS['text_muted'],
        ).pack(side="left", padx=(4, 0), pady=(18, 0))

        ctk.CTkFrame(self.sidebar, height=1, fg_color=COLORS['border']).pack(
            fill="x", padx=16, pady=(0, 8)
        )

        # Botões de navegação (populados em _setup_tabs)
        self.sidebar_nav = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.sidebar_nav.pack(fill="x", pady=4)
        self.sidebar_btns = {}

        # Card de drive no rodapé da sidebar
        ctk.CTkFrame(self.sidebar, height=1, fg_color=COLORS['border']).pack(
            side="bottom", fill="x", padx=16, pady=(0, 4)
        )
        ctk.CTkLabel(
            self.sidebar,
            text=f"v{APP_VERSION}",
            font=ctk.CTkFont(size=9),
            text_color=COLORS['text_dim'],
        ).pack(side="bottom", pady=(4, 0))

        sidebar_drive_card = ctk.CTkFrame(
            self.sidebar,
            fg_color=COLORS['bg_card'],
            corner_radius=10,
        )
        sidebar_drive_card.pack(side="bottom", fill="x", padx=12, pady=(0, 8))

        ctk.CTkLabel(
            sidebar_drive_card,
            text="DRIVE PSP",
            font=ctk.CTkFont(size=9, weight="bold"),
            text_color=COLORS['text_dim'],
        ).pack(anchor="w", padx=12, pady=(10, 2))

        self.sidebar_drive_label = ctk.CTkLabel(
            sidebar_drive_card,
            text="Não selecionado",
            font=ctk.CTkFont(size=11),
            text_color=COLORS['text_muted'],
        )
        self.sidebar_drive_label.pack(anchor="w", padx=12, pady=(0, 10))

        # ── ÁREA DE CONTEÚDO (direita) ───────────────────────────────────────
        self.content_area = ctk.CTkFrame(
            main_container,
            fg_color=COLORS['bg_mid'],
            corner_radius=0,
        )
        self.content_area.pack(side="left", fill="both", expand=True)

        # ── HEADER DE BUSCA ──────────────────────────────────────────────────
        search_header = ctk.CTkFrame(
            self.content_area,
            height=64,
            fg_color=COLORS['bg_dark'],
            corner_radius=0,
        )
        search_header.pack(fill="x")
        search_header.pack_propagate(False)

        search_inner = ctk.CTkFrame(search_header, fg_color="transparent")
        search_inner.pack(fill="both", expand=True, padx=16, pady=12)

        # Labels invisíveis mantidos para compatibilidade de tradução
        self.search_label_widget = ctk.CTkLabel(
            search_inner, text="", font=ctk.CTkFont(size=1), width=0
        )
        self.filter_type_label_widget = ctk.CTkLabel(
            search_inner, text="", font=ctk.CTkFont(size=1), width=0
        )
        self.filter_region_label_widget = ctk.CTkLabel(
            search_inner, text="", font=ctk.CTkFont(size=1), width=0
        )
        self.filter_sort_label_widget = ctk.CTkLabel(
            search_inner, text="", font=ctk.CTkFont(size=1), width=0
        )

        search_row = ctk.CTkFrame(search_inner, fg_color="transparent")
        search_row.pack(fill="x")

        self.search_entry = ctk.CTkEntry(
            search_row,
            placeholder_text="Buscar por nome...",
            width=300,
            height=38,
            fg_color=COLORS['bg_card'],
            border_color=COLORS['border'],
            text_color=COLORS['text'],
            placeholder_text_color=COLORS['text_dim'],
            corner_radius=10,
        )
        self.search_entry.pack(side="left")
        self.search_entry.bind("<Return>", lambda e: self._search())

        self.search_btn = ctk.CTkButton(
            search_row,
            text="🔍",
            width=38,
            height=38,
            fg_color=COLORS['accent'],
            hover_color=COLORS['accent_hover'],
            corner_radius=10,
            command=self._search,
        )
        self.search_btn.pack(side="left", padx=(6, 20))

        self.type_filter = ctk.CTkComboBox(
            search_row,
            values=["Todas"],
            width=120,
            height=38,
            fg_color=COLORS['bg_card'],
            border_color=COLORS['border'],
            text_color=COLORS['text'],
            button_color=COLORS['border'],
            button_hover_color=COLORS['accent'],
            dropdown_fg_color=COLORS['bg_card'],
            dropdown_text_color=COLORS['text'],
            corner_radius=10,
            command=lambda e: self._apply_filters(),
        )
        self.type_filter.pack(side="left", padx=(0, 6))
        self.type_filter.set("Todas")

        self.region_filter = ctk.CTkComboBox(
            search_row,
            values=["Todas"],
            width=110,
            height=38,
            fg_color=COLORS['bg_card'],
            border_color=COLORS['border'],
            text_color=COLORS['text'],
            button_color=COLORS['border'],
            button_hover_color=COLORS['accent'],
            dropdown_fg_color=COLORS['bg_card'],
            dropdown_text_color=COLORS['text'],
            corner_radius=10,
            command=lambda e: self._apply_filters(),
        )
        self.region_filter.pack(side="left", padx=(0, 6))
        self.region_filter.set("Todas")

        self.sort_filter = ctk.CTkComboBox(
            search_row,
            values=["Nome", "Tamanho", "Região", "Data"],
            width=110,
            height=38,
            fg_color=COLORS['bg_card'],
            border_color=COLORS['border'],
            text_color=COLORS['text'],
            button_color=COLORS['border'],
            button_hover_color=COLORS['accent'],
            dropdown_fg_color=COLORS['bg_card'],
            dropdown_text_color=COLORS['text'],
            corner_radius=10,
            command=self._apply_sort,
        )
        self.sort_filter.pack(side="left")
        self.sort_filter.set("Nome")
        
        self.clear_filters_btn = ctk.CTkButton(
            search_row,
            text="🧹 Limpar Filtro",
            width=130,
            height=38,
            fg_color=COLORS['bg_card'],
            hover_color=COLORS['sidebar_active'],
            border_color=COLORS['border'],
            border_width=1,
            text_color=COLORS['text'],
            corner_radius=10,
            command=self._clear_filters,
        )
        self.clear_filters_btn.pack(side="left", padx=(12, 0))

        # ── CONTAINER DE ABAS ────────────────────────────────────────────────
        self.tab_container = ctk.CTkFrame(self.content_area, fg_color="transparent")
        self.tab_container.pack(fill="both", expand=True)

        self.tab_frames   = {}
        self._current_tab = None

        # ── BARRA DE STATUS ──────────────────────────────────────────────────
        status_bar = ctk.CTkFrame(
            self.content_area,
            height=58,
            fg_color=COLORS['bg_dark'],
            corner_radius=0,
        )
        status_bar.pack(fill="x", side="bottom")
        status_bar.pack_propagate(False)

        status_inner = ctk.CTkFrame(status_bar, fg_color="transparent")
        status_inner.pack(fill="both", expand=True, padx=16, pady=8)

        # Esquerda: status + drive
        self.left_bottom_frame = ctk.CTkFrame(status_inner, fg_color="transparent")
        self.left_bottom_frame.pack(side="left", fill="y")

        self.status_label = ctk.CTkLabel(
            self.left_bottom_frame,
            text="PSP Freeshop pronto!",
            font=ctk.CTkFont(size=12),
            text_color=COLORS['text'],
            anchor="w",
        )
        self.status_label.pack(anchor="w")

        self.drive_path_label = ctk.CTkLabel(
            self.left_bottom_frame,
            text="🎮 Drive: Não selecionado",
            font=ctk.CTkFont(size=10),
            text_color=COLORS['text_muted'],
            anchor="w",
        )
        self.drive_path_label.pack(anchor="w")

        # Direita: barra de progresso + drive combo + botão de ação
        self.progress_frame = ctk.CTkFrame(status_inner, fg_color="transparent")
        self.progress_frame.pack(side="right", fill="y")

        self.action_btn = ctk.CTkButton(
            self.progress_frame,
            text="⬇️ BAIXAR JOGO",
            width=165,
            height=38,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=COLORS['success'],
            hover_color="#00b894",
            corner_radius=10,
            command=self._on_action_button_click,
        )
        self.action_btn.pack(side="right", padx=(8, 0))

        self.drive_frame = ctk.CTkFrame(self.progress_frame, fg_color="transparent")
        self.drive_frame.pack(side="right", padx=(8, 0))

        self.drive_label = ctk.CTkLabel(
            self.drive_frame,
            text="Drive:",
            font=ctk.CTkFont(size=11),
            text_color=COLORS['text_muted'],
        )
        self.drive_label.pack(side="left", padx=(0, 4))

        self.drive_combo = ctk.CTkComboBox(
            self.drive_frame,
            values=["Nenhum drive encontrado"],
            width=140,
            height=34,
            fg_color=COLORS['bg_card'],
            border_color=COLORS['border'],
            text_color=COLORS['text'],
            button_color=COLORS['border'],
            button_hover_color=COLORS['accent'],
            dropdown_fg_color=COLORS['bg_card'],
            dropdown_text_color=COLORS['text'],
            corner_radius=8,
            command=self._on_drive_selected,
        )
        self.drive_combo.pack(side="left")
        self.drive_combo.set("Selecionar drive")

        self.progress_bar = ctk.CTkProgressBar(
            self.progress_frame,
            width=220,
            height=6,
            progress_color=COLORS['accent'],
            fg_color=COLORS['border'],
            corner_radius=3,
        )
        self.progress_bar.pack(side="right", padx=(8, 0))
        self.progress_bar.set(0)

        # Atualizar lista de drives
        self.after(500, self._update_drives)

        # Flags de controle
        self.updates_loaded = False
        self.dlcs_loaded    = False
        self.themes_loaded  = False

    def _setup_store_tab(self):
        """Configura aba de Jogos da Loja"""
        tab = self.tab_frames[self.TAB_STORE]

        # Frame principal da aba
        store_frame = ctk.CTkFrame(tab, fg_color="transparent")
        store_frame.pack(fill="both", expand=True, padx=8, pady=8)

        # Grid de jogos da loja
        self.store_games_frame = GameGrid(store_frame, self._on_game_select, self._on_game_right_click, self._on_multi_select,
                                          selection_color=COLORS['tab_store'], selection_bg="#0a2e26",
                                          covers_dir=get_resource_path("CoversCompressed"))
        self.store_games_frame.pack(fill="both", expand=True)

        # Barra de paginação
        store_nav = ctk.CTkFrame(store_frame, fg_color="transparent")
        store_nav.pack(fill="x", pady=(5, 0))

        self.store_prev_btn = ctk.CTkButton(
            store_nav,
            text="◀ Anterior",
            width=110,
            height=30,
            fg_color=COLORS['bg_card'],
            hover_color=COLORS['sidebar_active'],
            border_color=COLORS['border'],
            border_width=1,
            text_color=COLORS['text_muted'],
            corner_radius=8,
            command=self._prev_page_store,
        )
        self.store_prev_btn.pack(side="left", padx=10)

        self.store_page_label = ctk.CTkLabel(
            store_nav,
            text="Página 1",
            font=ctk.CTkFont(size=12),
            text_color=COLORS['text_muted'],
        )
        self.store_page_label.pack(side="left", expand=True)

        self.store_next_btn = ctk.CTkButton(
            store_nav,
            text="Próxima ▶",
            width=110,
            height=30,
            fg_color=COLORS['bg_card'],
            hover_color=COLORS['sidebar_active'],
            border_color=COLORS['border'],
            border_width=1,
            text_color=COLORS['text_muted'],
            corner_radius=8,
            command=self._next_page_store,
        )
        self.store_next_btn.pack(side="right", padx=10)

        # Referência para uso global
        self.current_games_frame = self.store_games_frame

    def _setup_installed_tab(self):
        """Configura aba de Jogos Instalados"""
        tab = self.tab_frames[self.TAB_INSTALLED]

        # Frame principal da aba
        installed_frame = ctk.CTkFrame(tab, fg_color="transparent")
        installed_frame.pack(fill="both", expand=True, padx=8, pady=8)

        # Header com botão de atualizar
        header_frame = ctk.CTkFrame(installed_frame, fg_color=COLORS['bg_card'], corner_radius=10)
        header_frame.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(
            header_frame,
            text="💾 Jogos Instalados no PSP",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COLORS['tab_installed'],
        ).pack(side="left", pady=10, padx=16)

        refresh_btn = ctk.CTkButton(
            header_frame,
            text="🔄 Atualizar",
            width=100,
            height=32,
            fg_color=COLORS['bg_card'],
            hover_color=COLORS['sidebar_active'],
            border_color=COLORS['border'],
            border_width=1,
            text_color=COLORS['text_muted'],
            corner_radius=8,
            command=self._load_installed_games,
        )
        refresh_btn.pack(side="right", pady=10, padx=12)

        self.installed_type_filter = ctk.CTkComboBox(
            header_frame,
            values=["Todos", "Jogos", "Temas"],
            width=120,
            height=32,
            fg_color=COLORS['bg_card'],
            border_color=COLORS['border'],
            text_color=COLORS['text'],
            button_color=COLORS['border'],
            button_hover_color=COLORS['accent'],
            dropdown_fg_color=COLORS['bg_card'],
            dropdown_text_color=COLORS['text'],
            corner_radius=8,
            command=lambda e: self._apply_filters_installed(),
        )
        self.installed_type_filter.pack(side="right", pady=10, padx=12)
        self.installed_type_filter.set("Todos")

        # Grid de jogos instalados
        self.installed_games_frame = GameGrid(installed_frame, self._on_game_select, self._on_game_right_click, self._on_multi_select,
                                              selection_color=COLORS['tab_installed'], selection_bg="#2e0a12",
                                              covers_dir=get_resource_path("CoversCompressed"))
        self.installed_games_frame.pack(fill="both", expand=True)

    def _load_installed_games(self):
        """Carrega jogos instalados do drive PSP"""
        try:
            if not self.selected_drive_path:
                self.status_label.configure(text=self.t('status_select_drive'))
                # Mostrar mensagem vazia no grid
                if hasattr(self, 'installed_games_frame'):
                    self.installed_games_frame.display_games([])
                return

            self.status_label.configure(text=self.t('status_scanning'))

            # Procurar na pasta ISO
            iso_path = os.path.join(self.selected_drive_path, "ISO")
            installed_games = []

            if os.path.exists(iso_path):
                # Listar arquivos .iso, .cso, .pkg
                for ext in ['*.iso', '*.cso', '*.pkg']:
                    files = glob.glob(os.path.join(iso_path, ext))
                    for file_path in files:
                        file_name = os.path.basename(file_path)
                        file_size = os.path.getsize(file_path)

                        # Tentar encontrar informações do jogo pelo nome do arquivo
                        title_id = self._extract_title_id(file_name)
                        game_info = self._find_game_info(title_id, file_name)

                        installed_games.append({
                            'name': game_info.get('name', file_name),
                            'title_id': title_id or 'Unknown',
                            'region': game_info.get('region', 'Unknown'),
                            'type': game_info.get('type', 'PSP'),
                            'file_size': str(file_size),
                            'installed_path': file_path,
                            'pkg_link': '',  # Já instalado, não precisa de link
                            'content_id': game_info.get('content_id', ''),
                            'last_modified': ''
                        })

            # Procurar na pasta PSP/GAME
            psp_game_path = os.path.join(self.selected_drive_path, "PSP", "GAME")
            if os.path.exists(psp_game_path):
                # Listar pastas (cada pasta é um jogo)
                for game_dir in os.listdir(psp_game_path):
                    full_path = os.path.join(psp_game_path, game_dir)
                    if os.path.isdir(full_path):
                        # Calcular tamanho total da pasta
                        total_size = 0
                        for dirpath, dirnames, filenames in os.walk(full_path):
                            for f in filenames:
                                fp = os.path.join(dirpath, f)
                                total_size += os.path.getsize(fp)

                        title_id = game_dir
                        game_info = self._find_game_info(title_id, game_dir)

                        installed_games.append({
                            'name': game_info.get('name', game_dir),
                            'title_id': title_id,
                            'region': game_info.get('region', 'Unknown'),
                            'type': 'PSP Game',
                            'file_size': str(total_size),
                            'installed_path': full_path,
                            'pkg_link': '',
                            'content_id': game_info.get('content_id', ''),
                            'last_modified': ''
                        })

            # Procurar na pasta PSP/THEME
            psp_theme_path = os.path.join(self.selected_drive_path, "PSP", "THEME")
            if os.path.exists(psp_theme_path):
                # Listar arquivos .ptf
                for file_path in glob.glob(os.path.join(psp_theme_path, "*.ptf")):
                    file_name = os.path.basename(file_path)
                    file_size = os.path.getsize(file_path)
                    
                    theme_name = file_name[:-4] if file_name.endswith('.ptf') else file_name
                    
                    installed_games.append({
                        'name': theme_name,
                        'title_id': 'THEME',
                        'region': 'Unknown',
                        'type': 'Tema',
                        'file_size': str(file_size),
                        'installed_path': file_path,
                        'pkg_link': '',
                        'content_id': '',
                        'last_modified': ''
                    })


            # Guardar lista completa para filtros dinâmicos
            self.all_installed_games = installed_games

            # Exibir no grid (aplica filtro atual se houver)
            self._apply_filters_installed()

            self.status_label.configure(text=self.t('status_installed_found', count=len(installed_games)))

        except Exception as e:
            print(f"[DEBUG] Erro ao carregar jogos instalados: {e}")
            self.status_label.configure(text=self.t('status_error', msg=str(e)))

    def _extract_title_id(self, file_name):
        """Extrai Title ID do nome do arquivo.

        Formatos suportados:
          SOCOM - U.S. Navy SEALs [UCUS98716] [PSP].iso  -> UCUS98716
          SOCOM - Fireteam Bravo 3 [UCUS98716].iso        -> UCUS98716
          UCUS98716.pkg                                   -> UCUS98716
          UCUS-98716 (com hífen)                          -> UCUS98716 (normalizado)
        """
        name = os.path.splitext(file_name)[0]

        # 1. Padrão entre colchetes: [UCUS98716] ou [ULUS10001]
        match = re.search(r'\[([A-Z]{4}[A-Z0-9]{5})\]', name)
        if match:
            return match.group(1)

        # 2. Sem colchetes, sem hífen: UCUS98716 ULUS10001 NPEH00101 NPJH50300
        match = re.search(r'\b([A-Z]{4}[A-Z0-9]{5})\b', name)
        if match:
            return match.group(1)

        # 3. Com hífen: ULUS-10001 -> ULUS10001
        match = re.search(r'\b([A-Z]{4})-([0-9]{5})\b', name)
        if match:
            return match.group(1) + match.group(2)

        return None

    def _find_game_info(self, title_id, file_name):
        """Busca informações do jogo pelo Title ID na base de dados"""
        if not title_id or not hasattr(self, 'all_games'):
            return {}

        # Procurar na lista de jogos carregados
        for game in self.all_games:
            if game.get('title_id', '').upper() == title_id.upper():
                return game

        return {}

    def _on_tab_change(self):
        """Callback quando o usuário troca de aba"""
        current_tab = self._current_tab
        if not current_tab:
            return

        tab_btn_config = {
            self.TAB_STORE:     (self.t('btn_download_game'),   COLORS['success'],       "#00b894"),
            self.TAB_INSTALLED: (self.t('btn_delete_game'),     COLORS['error'],         "#dd4455"),
            self.TAB_UPDATES:   (self.t('btn_download_update'), COLORS['tab_updates'],   "#6d5deb"),
            self.TAB_DLCS:      (self.t('btn_download_dlc'),    COLORS['tab_dlcs'],      "#dd9933"),
            self.TAB_THEMES:    (self.t('btn_install_theme'),   COLORS['tab_themes'],    "#d35400"),
        }
        text, fg, hover = tab_btn_config.get(
            current_tab, (self.t('btn_download_game'), COLORS['success'], "#00b894")
        )
        self.action_btn.configure(text=text, fg_color=fg, hover_color=hover)

        if current_tab == self.TAB_INSTALLED:
            self._load_installed_games()
        elif current_tab == self.TAB_UPDATES:
            self._load_updates_on_demand()
            if self.updates_loaded:
                self._apply_filters_updates()
        elif current_tab == self.TAB_DLCS:
            self._load_dlcs_on_demand()
            if self.dlcs_loaded:
                self._apply_filters_dlcs()
        elif current_tab == self.TAB_THEMES:
            self._load_themes_on_demand()
            if self.themes_loaded:
                self._apply_filters_themes()
        else:  # Store
            if hasattr(self, 'all_games') and self.all_games:
                self._apply_filters_store()

    def _setup_updates_tab(self):
        """Configura aba de Atualizações"""
        tab = self.tab_frames[self.TAB_UPDATES]

        # Frame principal da aba
        updates_frame = ctk.CTkFrame(tab, fg_color="transparent")
        updates_frame.pack(fill="both", expand=True, padx=8, pady=8)

        # Header
        header_frame = ctk.CTkFrame(updates_frame, fg_color=COLORS['bg_card'], corner_radius=10)
        header_frame.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(
            header_frame,
            text="🔄 Atualizações Disponíveis",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COLORS['tab_updates'],
        ).pack(pady=12, padx=16, anchor="w")

        # Grid de atualizações
        self.updates_frame = GameGrid(updates_frame, self._on_game_select, self._on_game_right_click, self._on_multi_select,
                                      selection_color=COLORS['tab_updates'], selection_bg="#16153a",
                                      covers_dir=get_resource_path("CoversCompressed"))
        self.updates_frame.pack(fill="both", expand=True)

    def _setup_dlcs_tab(self):
        """Configura aba de DLCs"""
        tab = self.tab_frames[self.TAB_DLCS]

        # Frame principal da aba
        dlcs_frame = ctk.CTkFrame(tab, fg_color="transparent")
        dlcs_frame.pack(fill="both", expand=True, padx=8, pady=8)

        # Header
        header_frame = ctk.CTkFrame(dlcs_frame, fg_color=COLORS['bg_card'], corner_radius=10)
        header_frame.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(
            header_frame,
            text="📦 DLCs Disponíveis",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COLORS['tab_dlcs'],
        ).pack(side="left", pady=12, padx=16)

        # Filtros de DLCs
        filters_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        filters_frame.pack(side="right", padx=12)

        ctk.CTkLabel(
            filters_frame,
            text="Agrupar por:",
            font=ctk.CTkFont(size=11),
            text_color=COLORS['text_muted'],
        ).pack(side="left", padx=(0, 5))

        self.dlc_group_filter = ctk.CTkComboBox(
            filters_frame,
            values=["Todos", "Jogo", "Tipo"],
            width=100,
            height=32,
            fg_color=COLORS['bg_card'],
            border_color=COLORS['border'],
            text_color=COLORS['text'],
            button_color=COLORS['border'],
            button_hover_color=COLORS['accent'],
            dropdown_fg_color=COLORS['bg_card'],
            dropdown_text_color=COLORS['text'],
            corner_radius=8,
            command=self._filter_dlcs,
        )
        self.dlc_group_filter.pack(side="left")
        self.dlc_group_filter.set("Todos")

        # Grid de DLCs
        self.dlcs_frame = GameGrid(dlcs_frame, self._on_game_select, self._on_game_right_click, self._on_multi_select,
                                   selection_color=COLORS['tab_dlcs'], selection_bg="#2e1e00",
                                   covers_dir=get_resource_path("CoversCompressed"))
        self.dlcs_frame.pack(fill="both", expand=True)

        # Barra de paginação
        dlc_nav = ctk.CTkFrame(dlcs_frame, fg_color="transparent")
        dlc_nav.pack(fill="x", pady=(5, 0))

        self.dlc_prev_btn = ctk.CTkButton(
            dlc_nav,
            text="◀ Anterior",
            width=110,
            height=30,
            fg_color=COLORS['bg_card'],
            hover_color=COLORS['sidebar_active'],
            border_color=COLORS['border'],
            border_width=1,
            text_color=COLORS['text_muted'],
            corner_radius=8,
            command=self._prev_page_dlcs,
        )
        self.dlc_prev_btn.pack(side="left", padx=10)

        self.dlc_page_label = ctk.CTkLabel(
            dlc_nav,
            text="Página 1",
            font=ctk.CTkFont(size=12),
            text_color=COLORS['text_muted'],
        )
        self.dlc_page_label.pack(side="left", expand=True)

        self.dlc_next_btn = ctk.CTkButton(
            dlc_nav,
            text="Próxima ▶",
            width=110,
            height=30,
            fg_color=COLORS['bg_card'],
            hover_color=COLORS['sidebar_active'],
            border_color=COLORS['border'],
            border_width=1,
            text_color=COLORS['text_muted'],
            corner_radius=8,
            command=self._next_page_dlcs,
        )
        self.dlc_next_btn.pack(side="right", padx=10)

    def _setup_themes_tab(self):
        """Configura aba de Temas."""
        tab = self.tab_frames[self.TAB_THEMES]

        themes_frame = ctk.CTkFrame(tab, fg_color="transparent")
        themes_frame.pack(fill="both", expand=True, padx=8, pady=8)

        header_frame = ctk.CTkFrame(themes_frame, fg_color=COLORS['bg_card'], corner_radius=10)
        header_frame.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(
            header_frame,
            text=self.t('themes_header'),
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COLORS['tab_themes'],
        ).pack(side="left", pady=12, padx=16)

        self.themes_frame = GameGrid(themes_frame, self._on_game_select, self._on_game_right_click, self._on_multi_select,
                                     selection_color=COLORS['tab_themes'], selection_bg="#3d2510",
                                     covers_dir=get_resource_path("CoversCompressed"))
        self.themes_frame.pack(fill="both", expand=True)

        theme_nav = ctk.CTkFrame(themes_frame, fg_color="transparent")
        theme_nav.pack(fill="x", pady=(5, 0))

        self.theme_prev_btn = ctk.CTkButton(
            theme_nav, text="◀ Anterior", width=110, height=30,
            fg_color=COLORS['bg_card'], hover_color=COLORS['sidebar_active'],
            border_color=COLORS['border'], border_width=1, text_color=COLORS['text_muted'],
            corner_radius=8, command=self._prev_page_themes
        )
        self.theme_prev_btn.pack(side="left", padx=10)

        self.theme_page_label = ctk.CTkLabel(
            theme_nav, text="Página 1", font=ctk.CTkFont(size=12), text_color=COLORS['text_muted']
        )
        self.theme_page_label.pack(side="left", expand=True)

        self.theme_next_btn = ctk.CTkButton(
            theme_nav, text="Próxima ▶", width=110, height=30,
            fg_color=COLORS['bg_card'], hover_color=COLORS['sidebar_active'],
            border_color=COLORS['border'], border_width=1, text_color=COLORS['text_muted'],
            corner_radius=8, command=self._next_page_themes
        )
        self.theme_next_btn.pack(side="right", padx=10)

    # Métodos de callback
    def _on_game_select(self, game_data):
        """Callback para seleção de jogo"""
        self.selected_game = game_data
        print(f"[DEBUG] Jogo selecionado: {game_data.get('name', 'Unknown') if game_data else 'None'}")

    def _on_multi_select(self, selected_games):
        """Callback para seleção múltipla de jogos"""
        self.selected_games_list = selected_games
        count = len(selected_games)
        if count > 0:
            self.status_label.configure(text=self.t('status_selected_count', count=count))
            print(f"[DEBUG] {count} jogos selecionados para download em lote")

    def _on_game_right_click(self, game_data, event):
        """Callback para clique direito no jogo - mostra menu de contexto"""
        if not game_data:
            return

        # Criar menu de contexto
        menu = tk.Menu(self, tearoff=0)
        menu.configure(bg=COLORS['bg_card'], fg=COLORS['text'], activebackground=COLORS['accent'], activeforeground="white")

        # --- Opção Ver Updates (jogos sem installed_path = aba da loja) ---
        title_id = game_data.get('title_id', '')
        game_type = game_data.get('type', '')
        if game_type not in ('Update', 'DLC', 'Theme') and title_id:
            has_update = title_id.upper() in self._update_title_ids
            has_dlc    = title_id.upper() in self._dlc_title_ids

            update_label = self.t('ctx_see_updates') if has_update else self.t('ctx_check_updates')
            menu.add_command(
                label=update_label,
                command=lambda: self._show_updates_for_game(game_data)
            )

            dlc_label = self.t('ctx_see_dlcs') if has_dlc else self.t('ctx_check_dlcs')
            menu.add_command(
                label=dlc_label,
                command=lambda: self._show_dlcs_for_game(game_data)
            )
            menu.add_separator()

        # Opção de excluir (apenas para jogos instalados)
        if game_data.get('installed_path'):
            menu.add_command(
                label=self.t('ctx_delete', name=game_data.get('name', 'Game')),
                command=lambda: self._delete_game(game_data)
            )

        # Opção de renomear (apenas para jogos instalados)
        if game_data.get('installed_path'):
            menu.add_command(
                label=self.t('ctx_rename'),
                command=lambda: self._rename_game(game_data)
            )

        # Opção de abrir local do arquivo (apenas para jogos instalados)
        if game_data.get('installed_path'):
            menu.add_command(
                label=self.t('ctx_open_location'),
                command=lambda: self._open_file_location(game_data)
            )

        # Separador
        menu.add_separator()

        # Opção de ver informações
        menu.add_command(
            label=self.t('ctx_game_info'),
            command=lambda: self._show_game_info(game_data)
        )

        # Mostrar menu na posição do mouse
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def _rename_game(self, game_data):
        """Renomeia o jogo instalado"""
        old_path = game_data.get('installed_path', '')
        if not old_path:
            messagebox.showerror("Erro", self.t('err_no_path'))
            return

        old_name = os.path.basename(old_path)

        # Criar diálogo de renomear
        dialog = ctk.CTkToplevel(self)
        dialog.title(self.t('rename_title'))
        dialog.geometry("400x150")
        dialog.transient(self)
        dialog.grab_set()

        # Centralizar
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (150 // 2)
        dialog.geometry(f"400x150+{x}+{y}")

        ctk.CTkLabel(
            dialog,
            text=self.t('rename_new_name'),
            font=ctk.CTkFont(size=12)
        ).pack(pady=(20, 5))

        name_entry = ctk.CTkEntry(dialog, width=350)
        name_entry.pack(pady=5)
        name_entry.insert(0, old_name)
        name_entry.select_range(0, len(old_name))
        name_entry.focus()

        def do_rename():
            new_name = name_entry.get().strip()
            if not new_name:
                messagebox.showwarning("Aviso", self.t('warn_name_empty'))
                return

            if new_name == old_name:
                dialog.destroy()
                return

            try:
                new_path = os.path.join(os.path.dirname(old_path), new_name)
                os.rename(old_path, new_path)

                messagebox.showinfo(self.t('success_title'), self.t('success_renamed', old=old_name, new=new_name))
                self.status_label.configure(text=self.t('status_renamed', name=new_name))

                # Recarregar lista
                self._load_installed_games()
                dialog.destroy()

            except Exception as e:
                messagebox.showerror("Erro", self.t('err_rename', msg=str(e)))

        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=20)

        ctk.CTkButton(
            btn_frame,
            text=self.t('btn_rename_ok'),
            fg_color="#27ae60",
            hover_color="#229954",
            command=do_rename
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text=self.t('btn_cancel'),
            fg_color="#e74c3c",
            hover_color="#c0392b",
            command=dialog.destroy
        ).pack(side="left", padx=5)

    def _open_file_location(self, game_data):
        """Abre a pasta onde o jogo está localizado"""
        path = game_data.get('installed_path', '')
        if not path:
            messagebox.showerror("Erro", self.t('err_no_path'))
            return

        try:
            folder_path = os.path.dirname(path) if os.path.isfile(path) else path

            # Abrir no explorador de arquivos
            if platform.system() == "Windows":
                # No Windows, tentar selecionar o arquivo específico
                if os.path.isfile(path):
                    subprocess.run(["explorer", "/select,", os.path.normpath(path)])
                else:
                    subprocess.run(["explorer", os.path.normpath(folder_path)])
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", folder_path])
            else:  # Linux
                subprocess.run(["xdg-open", folder_path])

            self.status_label.configure(text=self.t('status_opened_folder', path=folder_path))

        except Exception as e:
            messagebox.showerror("Erro", self.t('err_open_folder', msg=str(e)))

    def _delete_game(self, game_data):
        """Exclui o jogo selecionado"""
        game_name = game_data.get('name', 'Game')
        installed_path = game_data.get('installed_path', '')

        if not installed_path:
            messagebox.showerror("Erro", self.t('err_no_path'))
            return

        # Confirmar exclusão
        if not messagebox.askyesno(
            self.t('confirm_delete_title'),
            self.t('confirm_delete_msg', name=game_name)
        ):
            return

        try:
            if os.path.isfile(installed_path):
                os.remove(installed_path)
            elif os.path.isdir(installed_path):
                shutil.rmtree(installed_path)

            messagebox.showinfo(self.t('success_title'), self.t('success_deleted', name=game_name))
            self.status_label.configure(text=self.t('status_deleted', name=game_name))

            # Recarregar a lista de jogos instalados
            self._load_installed_games()

        except Exception as e:
            messagebox.showerror("Erro", self.t('err_delete', msg=str(e)))

    def _show_game_info(self, game_data):
        """Mostra informações detalhadas do jogo"""
        info = self.t('info_name',    value=game_data.get('name',    'N/A')) + "\n"
        info += self.t('info_title_id', value=game_data.get('title_id', 'N/A')) + "\n"
        info += self.t('info_region',   value=game_data.get('region',   'N/A')) + "\n"
        info += self.t('info_type',     value=game_data.get('type',     'N/A')) + "\n"
        info += self.t('info_size',     value=game_data.get('file_size', 'N/A')) + "\n"
        info += self.t('info_path',     value=game_data.get('installed_path', 'N/A')) + "\n"

        title_id = game_data.get('title_id', '')
        if title_id and title_id.upper() in self._update_title_ids:
            info += self.t('info_has_updates')
        if title_id and title_id.upper() in self._dlc_title_ids:
            info += self.t('info_has_dlcs')

        messagebox.showinfo(self.t('game_info_title'), info)

    def _show_dlcs_for_game(self, game_data):
        """Mostra modal com os DLCs disponíveis para o jogo selecionado"""
        title_id  = game_data.get('title_id', '')
        game_name = game_data.get('name', 'Game')

        dlcs = self.content_matcher.dlc_manager.find_dlcs_for_game(title_id, game_name)

        if not dlcs:
            messagebox.showinfo(
                self.t('no_dlc_title'),
                self.t('no_dlc_msg', name=game_name, tid=title_id)
            )
            return

        modal = ctk.CTkToplevel(self)
        modal.title(self.t('dlc_modal_title', name=game_name))
        modal.geometry("580x460")
        modal.transient(self)
        modal.grab_set()

        modal.update_idletasks()
        x = (modal.winfo_screenwidth()  // 2) - 290
        y = (modal.winfo_screenheight() // 2) - 230
        modal.geometry(f"580x460+{x}+{y}")

        # Header
        header = ctk.CTkFrame(modal, fg_color="#1a2f47", corner_radius=8)
        header.pack(fill="x", padx=15, pady=(15, 5))
        ctk.CTkLabel(
            header,
            text=self.t('dlc_modal_header', count=len(dlcs), name=game_name),
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#52be80",
        ).pack(pady=10, padx=10)

        # Lista de DLCs com checkboxes
        scroll = ctk.CTkScrollableFrame(modal, height=250)
        scroll.pack(fill="both", expand=True, padx=15, pady=5)

        selected_vars = []
        for dlc in dlcs:
            row_frame = ctk.CTkFrame(scroll, fg_color="#1e3a2e", corner_radius=6)
            row_frame.pack(fill="x", pady=3, padx=2)

            var = ctk.BooleanVar(value=True)
            ctk.CTkCheckBox(row_frame, text="", variable=var, width=30).pack(
                side="left", padx=8, pady=8
            )

            info_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="x", expand=True, pady=6)

            ctk.CTkLabel(
                info_frame,
                text=dlc.get('name', 'DLC'),
                font=ctk.CTkFont(size=12, weight="bold"),
                anchor="w",
            ).pack(anchor="w")

            size_str = self.notification_manager._format_size(dlc.get('file_size', '0'))
            date_str = dlc.get('last_modified', '') or self.t('date_unknown')
            region   = dlc.get('region', '?')
            ctk.CTkLabel(
                info_frame,
                text=f"💾 {size_str}  •  📅 {date_str}  •  🌍 {region}",
                font=ctk.CTkFont(size=10),
                text_color="#95a5a6",
                anchor="w",
            ).pack(anchor="w")

            selected_vars.append({'dlc': dlc, 'var': var})

        # Botões
        btn_frame = ctk.CTkFrame(modal, fg_color="transparent")
        btn_frame.pack(pady=10)

        def download_selected():
            chosen = [item['dlc'] for item in selected_vars if item['var'].get()]
            if not chosen:
                messagebox.showwarning("Aviso", self.t('warn_select_dlc'), parent=modal)
                return
            modal.destroy()
            self.selected_games_list = chosen
            self._start_download()

        ctk.CTkButton(
            btn_frame,
            text=self.t('btn_dl_selected'),
            fg_color="#27ae60", hover_color="#229954",
            command=download_selected,
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            btn_frame,
            text=self.t('btn_close'),
            fg_color="#7f8c8d", hover_color="#636e72",
            command=modal.destroy,
        ).pack(side="left", padx=8)

        modal.wait_window()

    def _show_updates_for_game(self, game_data):
        """Mostra modal com os updates disponíveis para o jogo selecionado"""
        title_id  = game_data.get('title_id', '')
        game_name = game_data.get('name', 'Game')

        updates = self.content_matcher.update_manager.find_updates_for_game(title_id, game_name)

        if not updates:
            messagebox.showinfo(
                self.t('no_update_title'),
                self.t('no_update_msg', name=game_name, tid=title_id)
            )
            return

        # Criar modal de updates
        modal = ctk.CTkToplevel(self)
        modal.title(self.t('upd_modal_title', name=game_name))
        modal.geometry("560x420")
        modal.transient(self)
        modal.grab_set()

        modal.update_idletasks()
        x = (modal.winfo_screenwidth()  // 2) - 280
        y = (modal.winfo_screenheight() // 2) - 210
        modal.geometry(f"560x420+{x}+{y}")

        # Header
        header = ctk.CTkFrame(modal, fg_color="#1e3a5f", corner_radius=8)
        header.pack(fill="x", padx=15, pady=(15, 5))
        ctk.CTkLabel(
            header,
            text=self.t('upd_modal_header', count=len(updates), name=game_name),
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#5dade2",
        ).pack(pady=10, padx=10)

        # Lista de updates com checkboxes
        scroll = ctk.CTkScrollableFrame(modal, height=220)
        scroll.pack(fill="both", expand=True, padx=15, pady=5)

        selected_vars = []
        for update in updates:
            row_frame = ctk.CTkFrame(scroll, fg_color="#2c3e50", corner_radius=6)
            row_frame.pack(fill="x", pady=3, padx=2)

            var = ctk.BooleanVar(value=True)
            ctk.CTkCheckBox(
                row_frame, text="", variable=var, width=30
            ).pack(side="left", padx=8, pady=8)

            info_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="x", expand=True, pady=6)

            ctk.CTkLabel(
                info_frame,
                text=update.get('name', 'Update'),
                font=ctk.CTkFont(size=12, weight="bold"),
                anchor="w",
            ).pack(anchor="w")

            size_str  = self.notification_manager._format_size(update.get('file_size', '0'))
            date_str  = update.get('last_modified', '') or self.t('date_unknown')
            region    = update.get('region', '?')
            ctk.CTkLabel(
                info_frame,
                text=f"💾 {size_str}  •  📅 {date_str}  •  🌍 {region}",
                font=ctk.CTkFont(size=10),
                text_color="#95a5a6",
                anchor="w",
            ).pack(anchor="w")

            selected_vars.append({'update': update, 'var': var})

        # Botões
        btn_frame = ctk.CTkFrame(modal, fg_color="transparent")
        btn_frame.pack(pady=10)

        def download_selected():
            chosen = [item['update'] for item in selected_vars if item['var'].get()]
            if not chosen:
                messagebox.showwarning("Aviso", self.t('warn_select_update'), parent=modal)
                return
            modal.destroy()
            # Enfileirar downloads de updates
            self.selected_games_list = chosen
            self._start_download()

        ctk.CTkButton(
            btn_frame,
            text=self.t('btn_dl_selected'),
            fg_color="#27ae60", hover_color="#229954",
            command=download_selected,
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            btn_frame,
            text=self.t('btn_close'),
            fg_color="#7f8c8d", hover_color="#636e72",
            command=modal.destroy,
        ).pack(side="left", padx=8)

        modal.wait_window()

    def _filter_updates(self, choice):
        """Filtra atualizações por região"""
        try:
            all_val = self.t('all_regions_combo')
            region = choice if choice != all_val else ''
            updates = self.content_matcher.update_manager.filter_by_region(region)

            if hasattr(self, 'updates_frame'):
                self.updates_frame.display_games(updates)

            self.status_label.configure(
                text=self.t('status_updates_region', count=len(updates), region=choice)
            )
        except Exception as e:
            print(f"[DEBUG] Erro ao filtrar updates: {e}")

    def _filter_dlcs(self, _choice):
        """Callback do combobox de agrupamento — debounce para evitar travamento."""
        if not self.dlcs_loaded:
            return
        if hasattr(self, '_dlc_filter_after'):
            try:
                self.after_cancel(self._dlc_filter_after)
            except Exception:
                pass
        self._dlc_filter_after = self.after(150, self._apply_filters_dlcs)

    def _filter_themes(self, choice=None):
        """Filtra temas por busca"""
        if not hasattr(self, '_apply_filters_themes'):
            return
        if hasattr(self, '_theme_filter_after'):
            try:
                self.after_cancel(self._theme_filter_after)
            except Exception:
                pass
        self._theme_filter_after = self.after(150, self._apply_filters_themes)

    def _load_updates_on_demand(self):
        """Carrega atualizações apenas quando solicitado"""
        if not self.updates_loaded:
            self.status_label.configure(text=self.t('status_loading_updates'))
            self._load_updates()
            self.updates_loaded = True

    def _load_dlcs_on_demand(self):
        """Carrega DLCs apenas quando solicitado (em thread separada para não travar a UI)"""
        if self.dlcs_loaded:
            return
        self.dlcs_loaded = True  # marcar antes de iniciar para evitar carregamento duplo
        self.status_label.configure(text=self.t('status_loading_dlcs'))

        def _do_load():
            try:
                dlcs = self.content_matcher.dlc_manager.get_all_dlcs()
                dlc_title_ids = self.content_matcher.dlc_manager.build_title_id_index()
                total = len(dlcs)
                # Passar a lista original diretamente — sem criar cópia intermediária
                self.after(0, lambda: self._update_dlcs_ui(dlcs, dlc_title_ids, total))
            except Exception as e:
                print(f"[DEBUG] Erro ao carregar DLCs: {e}")
                self.after(0, lambda: self.status_label.configure(text=self.t('status_loading_dlcs')))

        threading.Thread(target=_do_load, daemon=True).start()

    def _update_dlcs_ui(self, dlcs, dlc_title_ids, total):
        """Atualiza a UI com os DLCs carregados (deve ser chamado na thread principal)"""
        self._dlc_title_ids = dlc_title_ids
        # Aponta para a lista original — sem cópia
        self.all_dlcs_data = dlcs
        self.dlc_page = 1
        self.status_label.configure(text=self.t('status_loaded_dlcs', count=total))
        self._display_dlc_page()

    def _load_themes_on_demand(self):
        """Carrega temas apenas quando solicitado"""
        if not self.themes_loaded:
            self.status_label.configure(text=self.t('status_loading_themes'))
            self._load_themes()
            self.themes_loaded = True

    def _load_updates(self):
        """Carrega atualizações na aba correspondente"""
        try:
            updates = self.content_matcher.update_manager.get_all_updates()
            self.status_label.configure(text=self.t('status_loaded_updates', count=len(updates)))
            print(f"[DEBUG] Carregados {len(updates)} updates")

            # Construir índice de title_ids com update p/ badge nos cards
            self._update_title_ids = self.content_matcher.update_manager.build_title_id_index()

            # Passar lista original diretamente — sem criar cópia intermediária
            if hasattr(self, 'updates_frame') and updates:
                self.updates_frame.display_games(updates)

        except Exception as e:
            print(f"[DEBUG] Erro ao carregar updates: {e}")

    def _load_dlcs(self):
        """Carrega DLCs na aba correspondente"""
        try:
            dlcs = self.content_matcher.dlc_manager.get_all_dlcs()
            self.status_label.configure(text=self.t('status_loaded_dlcs', count=len(dlcs)))
            print(f"[DEBUG] Carregados {len(dlcs)} DLCs")

            # Construir índice para badge nos cards
            self._dlc_title_ids = self.content_matcher.dlc_manager.build_title_id_index()

            # Passar lista original diretamente — sem criar cópia intermediária
            if hasattr(self, 'dlcs_frame') and dlcs:
                self.dlcs_frame.display_games(dlcs)

        except Exception as e:
            print(f"[DEBUG] Erro ao carregar DLCs: {e}")

    def _load_themes(self):
        """Carrega temas da pasta local 'themes'."""
        try:
            self.status_label.configure(text=self.t('status_loading_themes'))
            themes_dir = get_resource_path("themes")
            theme_games = []
            
            if os.path.exists(themes_dir):
                for file_name in os.listdir(themes_dir):
                    if file_name.lower().endswith(('.ptf', '.ctf')):
                        file_path = os.path.join(themes_dir, file_name)
                        file_size = os.path.getsize(file_path)
                        modified_time = os.path.getmtime(file_path)
                        date_str = time.strftime('%Y-%m-%d', time.localtime(modified_time))
                        
                        theme_games.append({
                            'name': file_name,
                            'region': 'Unknown',
                            'type': 'Theme',
                            'file_size': str(file_size),
                            'last_modified': date_str,
                            'title_id': file_name,
                            'installed_path': file_path,
                            'content_id': '',
                            'pkg_link': ''
                        })
            
            self.all_themes_data = theme_games
            self.theme_page = 1
            self.status_label.configure(text=self.t('status_loaded_themes', count=len(theme_games)))
            print(f"[DEBUG] Carregados {len(theme_games)} temas da pasta local")

            if hasattr(self, 'themes_frame') and theme_games:
                self._display_theme_page()

        except Exception as e:
            print(f"[DEBUG] Erro ao carregar temas: {e}")

    # Métodos placeholder (serão implementados depois)
    def _load_games(self):
        """Carrega jogos do arquivo TSV com paginação"""
        try:
            self.status_label.configure(text=self.t('status_loading_games'))

            if not os.path.exists(TSV_FILE):
                messagebox.showerror("Erro", self.t('err_tsv_not_found', file=TSV_FILE))
                return

            # Carregar apenas primeira página inicialmente
            self.all_games = core.parse_tsv(TSV_FILE)
            self.all_games.sort(key=lambda x: x['name'].lower())

            # Pré-carregar índice de updates E dlcs para badge nos cards
            try:
                self._update_title_ids = self.content_matcher.update_manager.build_title_id_index()
                print(f"[DEBUG] Índice de updates: {len(self._update_title_ids)} title_ids com update")
            except Exception as e:
                print(f"[DEBUG] Erro ao construir índice de updates: {e}")
                self._update_title_ids = set()

            try:
                self._dlc_title_ids = self.content_matcher.dlc_manager.build_title_id_index()
                print(f"[DEBUG] Índice de DLCs: {len(self._dlc_title_ids)} title_ids com DLC")
            except Exception as e:
                print(f"[DEBUG] Erro ao construir índice de DLCs: {e}")
                self._dlc_title_ids = set()

            # filtered_games guarda a lista completa filtrada; paginação é feita na exibição
            self.filtered_games = self.all_games[:]
            self.current_page = 1

            # Exibir primeira página
            self._display_store_page()

            # Atualizar opções dos filtros
            self._update_filter_options()

        except Exception as e:
            messagebox.showerror("Erro", self.t('err_load_games', msg=str(e)))

    def _load_more_games(self):
        """Mantido por compatibilidade — use _next_page_store."""
        self._next_page_store()

    # ── Paginação da loja ──────────────────────────────────────────────────────

    def _display_store_page(self):
        """Exibe a página atual de jogos filtrados e atualiza os controles."""
        if not hasattr(self, 'store_games_frame'):
            return
        start = (self.current_page - 1) * self.games_per_page
        end   = start + self.games_per_page
        page_items = self.filtered_games[start:end]
        self.store_games_frame.display_games(page_items)
        total_pages = max(1, -(-len(self.filtered_games) // self.games_per_page))  # ceil division
        self.store_page_label.configure(text=self.t('page_of', page=self.current_page, total=total_pages))
        self.store_prev_btn.configure(state="normal" if self.current_page > 1 else "disabled")
        self.store_next_btn.configure(state="normal" if self.current_page < total_pages else "disabled")
        self.status_label.configure(
            text=self.t('status_games_page', count=len(self.filtered_games), page=self.current_page, total=total_pages)
        )

    def _prev_page_store(self):
        if self.current_page > 1:
            self.current_page -= 1
            self._display_store_page()

    def _next_page_store(self):
        total_pages = max(1, -(-len(self.filtered_games) // self.games_per_page))
        if self.current_page < total_pages:
            self.current_page += 1
            self._display_store_page()

    # ── Paginação de DLCs ──────────────────────────────────────────────────────

    def _display_dlc_page(self):
        """Exibe a página atual de DLCs e atualiza os controles."""
        if not hasattr(self, 'dlcs_frame'):
            return
        per_page = 50
        start = (self.dlc_page - 1) * per_page
        end   = start + per_page
        page_items = self.all_dlcs_data[start:end]
        self.dlcs_frame.display_games(page_items)
        total_pages = max(1, -(-len(self.all_dlcs_data) // per_page))
        self.dlc_page_label.configure(text=self.t('page_of', page=self.dlc_page, total=total_pages))
        self.dlc_prev_btn.configure(state="normal" if self.dlc_page > 1 else "disabled")
        self.dlc_next_btn.configure(state="normal" if self.dlc_page < total_pages else "disabled")

    def _prev_page_dlcs(self):
        if self.dlc_page > 1:
            self.dlc_page -= 1
            self._display_dlc_page()

    def _next_page_dlcs(self):
        per_page = 50
        total_pages = max(1, -(-len(self.all_dlcs_data) // per_page))
        if self.dlc_page < total_pages:
            self.dlc_page += 1
            self._display_dlc_page()

    # ── Paginação de Temas ──────────────────────────────────────────────────────

    def _display_theme_page(self):
        if not hasattr(self, 'themes_frame'):
            return
        per_page = 50
        start = (self.theme_page - 1) * per_page
        end   = start + per_page
        page_items = self.all_themes_data[start:end]
        self.themes_frame.display_games(page_items)
        total_pages = max(1, -(-len(self.all_themes_data) // per_page))
        self.theme_page_label.configure(text=self.t('page_of', page=self.theme_page, total=total_pages))
        self.theme_prev_btn.configure(state="normal" if self.theme_page > 1 else "disabled")
        self.theme_next_btn.configure(state="normal" if self.theme_page < total_pages else "disabled")

    def _prev_page_themes(self):
        if self.theme_page > 1:
            self.theme_page -= 1
            self._display_theme_page()

    def _next_page_themes(self):
        per_page = 50
        total_pages = max(1, -(-len(self.all_themes_data) // per_page))
        if self.theme_page < total_pages:
            self.theme_page += 1
            self._display_theme_page()

    def _search(self):
        """Busca conteúdo na aba ativa usando os filtros atuais"""
        self._apply_filters()

    def _clear_filters(self):
        """Reseta todos os filtros e barra de busca para o padrão"""
        self.search_entry.delete(0, 'end')
        self.type_filter.set(self.t('all_types'))
        self.region_filter.set(self.t('all_regions'))
        self.sort_filter.set(self.t('sort_name'))
        
        if hasattr(self, 'installed_type_filter'):
            self.installed_type_filter.set("Todos")
            
        self._apply_filters()

    def _apply_filters(self):
        """Despacha para o método de filtro da aba ativa."""
        if not hasattr(self, '_current_tab') or not self._current_tab:
            return
        current_tab = self._current_tab
        if current_tab == self.TAB_INSTALLED:
            self._apply_filters_installed()
        elif current_tab == self.TAB_UPDATES:
            self._apply_filters_updates()
        elif current_tab == self.TAB_DLCS:
            self._apply_filters_dlcs()
        else:  # TAB_STORE (padrão)
            self._apply_filters_store()

    # ---- Filtros por aba -------------------------------------------------------

    def _apply_filters_store(self):
        """Filtra a lista de jogos da loja (tipo, região, nome)."""
        if not hasattr(self, 'all_games') or not self.all_games:
            return

        type_filter   = self.type_filter.get()
        region_filter = self.region_filter.get()
        all_types_val   = self.t('all_types')
        all_regions_val = self.t('all_regions')

        filtered = self.all_games.copy()

        if type_filter != all_types_val:
            filtered = [g for g in filtered if g.get('type', '') == type_filter]

        if region_filter != all_regions_val:
            filtered = [g for g in filtered if g.get('region', '') == region_filter]

        query = self.search_entry.get().strip().lower()
        if query:
            filtered = [g for g in filtered if query in g.get('name', '').lower()]

        self.filtered_games = filtered
        self.current_page = 1
        self._display_store_page()
        self.status_label.configure(text=self.t('status_filtered', count=len(self.filtered_games)))

    def _apply_filters_installed(self):
        """Filtra jogos instalados por nome e região."""
        if not hasattr(self, 'installed_games_frame'):
            return

        query         = self.search_entry.get().strip().lower() if hasattr(self, 'search_entry') else ''
        region_filter = self.region_filter.get() if hasattr(self, 'region_filter') else ''
        all_regions_val = self.t('all_regions')

        # Filtro exclusivo dessa aba
        local_type_filter = self.installed_type_filter.get() if hasattr(self, 'installed_type_filter') else 'Todos'

        filtered = self.all_installed_games[:]

        if local_type_filter == "Jogos":
            filtered = [g for g in filtered if not str(g.get('installed_path', '')).lower().endswith('.ptf')]
        elif local_type_filter == "Temas":
            filtered = [g for g in filtered if str(g.get('installed_path', '')).lower().endswith('.ptf')]

        if region_filter and region_filter != all_regions_val:
            filtered = [g for g in filtered if g.get('region', '') == region_filter]

        if query:
            filtered = [g for g in filtered if query in g.get('name', '').lower()]

        self.installed_games_frame.display_games(filtered)
        count_all = len(self.all_installed_games)
        count_filt = len(filtered)
        if query or (region_filter and region_filter != all_regions_val):
            self.status_label.configure(text=self.t('status_filtered', count=count_filt))
        else:
            self.status_label.configure(text=self.t('status_installed_found', count=count_all))

    def _apply_filters_updates(self):
        """Filtra updates por nome e região."""
        if not hasattr(self, 'updates_frame') or not self.updates_loaded:
            return

        query         = self.search_entry.get().strip().lower()
        region_filter = self.region_filter.get()
        all_regions_val = self.t('all_regions')

        all_updates = self.content_matcher.update_manager.get_all_updates()

        if region_filter and region_filter != all_regions_val:
            all_updates = [u for u in all_updates if u.get('region', '') == region_filter]

        if query:
            all_updates = [u for u in all_updates if query in u.get('name', '').lower()]

        self.updates_frame.display_games(all_updates)
        self.status_label.configure(
            text=self.t('status_updates_region', count=len(all_updates),
                        region=region_filter if region_filter != all_regions_val else self.t('all_regions_combo'))
        )

    def _apply_filters_dlcs(self):
        """Filtra/agrupa DLCs por busca, região e agrupamento, com paginação."""
        if not hasattr(self, 'dlcs_frame') or not self.dlcs_loaded:
            return

        query           = self.search_entry.get().strip().lower()
        region_filter   = self.region_filter.get()
        all_regions_val = self.t('all_regions')
        group_choice    = self.dlc_group_filter.get() if hasattr(self, 'dlc_group_filter') else ''
        group_game      = self.t('group_game')
        group_type      = self.t('group_type')

        all_dlcs = self.content_matcher.dlc_manager.get_all_dlcs()

        if region_filter and region_filter != all_regions_val:
            all_dlcs = [d for d in all_dlcs if d.get('region', '') == region_filter]

        if query:
            all_dlcs = [d for d in all_dlcs if query in d.get('name', '').lower()]

        # Aplicar agrupamento como ordenação
        if group_choice == group_game:
            all_dlcs = sorted(all_dlcs, key=lambda d: d.get('title_id', '').lower())
        elif group_choice == group_type:
            all_dlcs = sorted(all_dlcs, key=lambda d: d.get('type', '').lower())

        self.all_dlcs_data = all_dlcs
        self.dlc_page = 1
        self._display_dlc_page()
        self.status_label.configure(
            text=self.t('status_dlcs_region', count=len(all_dlcs),
                        region=region_filter if region_filter != all_regions_val else self.t('all_regions_combo'))
        )

    def _apply_filters_themes(self):
        """Filtra temas pela busca e pagina."""
        if not hasattr(self, 'themes_frame') or not getattr(self, 'themes_loaded', False):
            return

        query = self.search_entry.get().strip().lower()
        
        if not hasattr(self, '_original_themes_data'):
            self._original_themes_data = getattr(self, 'all_themes_data', [])[:]

        all_themes = self._original_themes_data

        if query:
            filtered = [t for t in all_themes if query in t.get('name', '').lower()]
        else:
            filtered = all_themes[:]

        self.all_themes_data = filtered
        self.theme_page = 1
        self._display_theme_page()

    # ---- Ordenação ------------------------------------------------------------

    def _apply_sort(self, choice=None):
        """Aplica ordenação na aba ativa."""
        if choice is None:
            choice = self.sort_filter.get()

        sort_name   = self.t('sort_name')
        sort_size   = self.t('sort_size')
        sort_region = self.t('sort_region')
        sort_date   = self.t('sort_date')

        def sort_key_size(x):
            try:
                return int(x.get('file_size', '0') or '0')
            except ValueError:
                return 0

        current_tab = self._current_tab if hasattr(self, '_current_tab') else None

        if current_tab == self.TAB_UPDATES and self.updates_loaded:
            lst = self.content_matcher.update_manager.updates
            if choice == sort_name:   lst.sort(key=lambda x: x.get('name', '').lower())
            elif choice == sort_size: lst.sort(key=sort_key_size, reverse=True)
            elif choice == sort_region: lst.sort(key=lambda x: x.get('region', ''))
            elif choice == sort_date:  lst.sort(key=lambda x: x.get('last_modified', ''), reverse=True)
            self._apply_filters_updates()

        elif current_tab == self.TAB_DLCS and self.dlcs_loaded:
            lst = self.content_matcher.dlc_manager.dlcs
            if choice == sort_name:   lst.sort(key=lambda x: x.get('name', '').lower())
            elif choice == sort_size: lst.sort(key=sort_key_size, reverse=True)
            elif choice == sort_region: lst.sort(key=lambda x: x.get('region', ''))
            elif choice == sort_date:  lst.sort(key=lambda x: x.get('last_modified', ''), reverse=True)
            self._apply_filters_dlcs()

        elif current_tab == self.TAB_INSTALLED:
            if choice == sort_name:   self.all_installed_games.sort(key=lambda x: x.get('name', '').lower())
            elif choice == sort_size: self.all_installed_games.sort(key=sort_key_size, reverse=True)
            elif choice == sort_region: self.all_installed_games.sort(key=lambda x: x.get('region', ''))
            self._apply_filters_installed()

        else:  # Store
            if not hasattr(self, 'all_games') or not self.all_games:
                return
            if choice == sort_name:   self.all_games.sort(key=lambda x: x.get('name', '').lower())
            elif choice == sort_size: self.all_games.sort(key=sort_key_size, reverse=True)
            elif choice == sort_region: self.all_games.sort(key=lambda x: x.get('region', ''))
            elif choice == sort_date:  self.all_games.sort(key=lambda x: x.get('last_modified', ''), reverse=True)
            self._apply_filters_store()

    def _update_filter_options(self):
        """Atualiza opções dos filtros baseado nos jogos carregados"""
        if not hasattr(self, 'all_games') or not self.all_games:
            return

        # Extrair tipos únicos
        types = list(set(game.get('type', '') for game in self.all_games if game.get('type', '')))
        types.sort()
        all_types_val = self.t('all_types')
        type_options = [all_types_val] + types
        self.type_filter.configure(values=type_options)

        # Extrair regiões únicas
        regions = list(set(game.get('region', '') for game in self.all_games if game.get('region', '')))
        regions.sort()
        all_regions_val = self.t('all_regions')
        region_options = [all_regions_val] + regions
        self.region_filter.configure(values=region_options)

    def _cleanup_temp_dir(self, temp_path=None):
        """Remove o arquivo .pkg temporário e quaisquer subpastas residuais em TEMP_DIR."""
        if temp_path:
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            except Exception as e:
                print(f"[DEBUG] Erro ao remover arquivo temporário {temp_path}: {e}")
        if os.path.exists(TEMP_DIR):
            for item in os.listdir(TEMP_DIR):
                item_path = os.path.join(TEMP_DIR, item)
                try:
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                    elif os.path.isfile(item_path) and item_path != temp_path:
                        os.remove(item_path)
                except Exception as e:
                    print(f"[DEBUG] Erro ao limpar temp_dir item {item_path}: {e}")

    def _on_action_button_click(self):
        """Gerencia o clique no botão de ação dinâmico"""
        current_tab = self._current_tab

        if current_tab == self.TAB_INSTALLED:
            # Na aba de jogos instalados, o botão exclui
            self._delete_selected_game()
        else:
            # Em outras abas, o botão baixa
            self._start_download()

    def _delete_selected_game(self):
        """Exclui o(s) jogo(s) selecionado(s) na aba de jogos instalados"""
        # Verificar se há múltiplos jogos selecionados
        games_to_delete = []
        if hasattr(self, 'selected_games_list') and len(self.selected_games_list) > 0:
            # Filtrar apenas jogos instalados (têm installed_path)
            games_to_delete = [g for g in self.selected_games_list if g.get('installed_path')]
        elif self.selected_game and self.selected_game.get('installed_path'):
            games_to_delete = [self.selected_game]

        if not games_to_delete:
            messagebox.showwarning("Aviso", self.t('warn_select_game'))
            return

        # Confirmar exclusão
        if len(games_to_delete) == 1:
            game_name = games_to_delete[0].get('name', 'Game')
            if not messagebox.askyesno(
                self.t('confirm_delete_title'),
                self.t('confirm_delete_msg', name=game_name)
            ):
                return
        else:
            game_names = "\n".join([f"- {g.get('name', 'Game')}" for g in games_to_delete[:5]])
            if len(games_to_delete) > 5:
                game_names += "\n" + self.t('more_items', count=len(games_to_delete) - 5)
            if not messagebox.askyesno(
                self.t('confirm_del_batch_title'),
                self.t('confirm_del_batch_msg', count=len(games_to_delete), names=game_names)
            ):
                return

        # Excluir jogos
        success_count = 0
        error_count = 0
        error_messages = []

        for game in games_to_delete:
            try:
                installed_path = game.get('installed_path', '')
                game_name = game.get('name', 'Game')

                if os.path.isfile(installed_path):
                    os.remove(installed_path)
                elif os.path.isdir(installed_path):
                    shutil.rmtree(installed_path)

                success_count += 1
                print(f"[DEBUG] Excluído: {game_name}")

            except Exception as e:
                error_count += 1
                error_messages.append(f"{game.get('name', 'Game')}: {str(e)}")
                print(f"[DEBUG] Erro ao excluir {game.get('name', 'Game')}: {e}")

        # Mostrar resultado
        if error_count == 0:
            if success_count == 1:
                messagebox.showinfo(self.t('success_title'), self.t('success_deleted', name=games_to_delete[0].get('name', 'Game')))
            else:
                messagebox.showinfo(self.t('success_title'), self.t('success_deleted_count', count=success_count))
            self.status_label.configure(text=self.t('status_deleted_count', count=success_count))
        else:
            error_text = "\n".join(error_messages[:3])
            if len(error_messages) > 3:
                error_text += "\n" + self.t('more_errors', count=len(error_messages) - 3)
            messagebox.showwarning(
                self.t('warn_done_failures'),
                self.t('warn_failures_msg', ok=success_count, fail=error_count, errors=error_text)
            )
            self.status_label.configure(text=self.t('status_ok_failures', ok=success_count, fail=error_count))

        # Limpar seleção e recarregar
        self.selected_games_list = []
        self._load_installed_games()

    def _start_download(self):
        """Inicia download do(s) jogo(s) selecionado(s)"""
        print(f"[DEBUG] Botão download clicado!")

        # Verificar se há múltiplos jogos selecionados
        games_to_download = []
        if hasattr(self, 'selected_games_list') and len(self.selected_games_list) > 1:
            games_to_download = self.selected_games_list
            print(f"[DEBUG] Download em lote: {len(games_to_download)} jogos")
        elif self.selected_game:
            games_to_download = [self.selected_game]
            print(f"[DEBUG] Download único: {self.selected_game.get('name', 'Unknown')}")
        else:
            messagebox.showwarning("Aviso", self.t('warn_select_game'))
            return

        print(f"[DEBUG] Drive selecionado: {self.selected_drive_path}")

        if not self.selected_drive_path:
            messagebox.showwarning("Aviso", self.t('warn_no_drive'))
            return

        # Confirmação antes de baixar
        if len(games_to_download) == 1:
            game_name = games_to_download[0].get('name', 'Game')
            if not messagebox.askyesno(
                self.t('confirm_download_title'),
                self.t('confirm_download_msg', name=game_name)
            ):
                return
        else:
            game_names = "\n".join([f"- {g.get('name', 'Game')}" for g in games_to_download[:5]])
            if len(games_to_download) > 5:
                game_names += "\n" + self.t('more_items', count=len(games_to_download) - 5)
            if not messagebox.askyesno(
                self.t('confirm_dl_batch_title'),
                self.t('confirm_dl_batch_msg', count=len(games_to_download), names=game_names)
            ):
                return

        # Iniciar download em thread separada
        if len(games_to_download) == 1:
            self.status_label.configure(text=self.t('status_dl_start', name=games_to_download[0].get('name', 'Game')))
        else:
            self.status_label.configure(text=self.t('status_dl_start_batch', count=len(games_to_download)))
        self.progress_bar.set(0)

        # Verificar se são todos updates ou dlcs (para rotear corretamente)
        all_updates = all(g.get('type', '') == 'Update' for g in games_to_download)
        all_dlcs    = all(g.get('type', '') == 'DLC'    for g in games_to_download)

        download_thread = threading.Thread(
            target=self._download_games_batch,
            args=(games_to_download, all_updates, all_dlcs),
            daemon=True
        )
        download_thread.start()

    def _download_games_batch(self, games, is_updates=False, is_dlcs=False):
        """Faz download em lote de múltiplos jogos, updates ou DLCs"""
        total_games = len(games)
        success_count = 0
        error_count = 0

        for i, game in enumerate(games):
            try:
                game_name = game.get('name', f'Game {i+1}')
                self.after(0, lambda gn=game_name, idx=i, total=total_games: self.status_label.configure(
                    text=self.t('status_downloading', idx=idx+1, total=total, name=gn)
                ))
                self.after(0, lambda p=(i/total_games): self.progress_bar.set(p))

                game_type = game.get('type', '')
                if is_updates or game_type == 'Update':
                    self._download_update_internal(game)
                elif is_dlcs or game_type == 'DLC':
                    self._download_dlc_internal(game)
                elif game_type == 'Theme':
                    self._download_theme_internal(game)
                else:
                    self._download_game_internal(game)
                success_count += 1

            except Exception as e:
                error_count += 1
                print(f"[DEBUG] Erro no download do item {i+1}: {e}")
                continue

        # Finalização
        self.after(0, lambda: self.progress_bar.set(1))
        if error_count == 0:
            self.after(0, lambda: self.status_label.configure(text=self.t('status_dl_items_ok', count=success_count)))
            self.after(0, lambda: messagebox.showinfo(self.t('success_title'), self.t('success_dl_all', count=success_count)))
        else:
            self.after(0, lambda: self.status_label.configure(text=self.t('status_dl_ok_fail', ok=success_count, fail=error_count)))
            self.after(0, lambda: messagebox.showwarning(self.t('warn_done_failures'), self.t('warn_dl_failures', ok=success_count, fail=error_count)))

    def _download_game_internal(self, game):
        """Faz download de um jogo PSP com feedback completo de progresso."""
        pkg_link = game.get('pkg_link', '')
        if not pkg_link:
            raise Exception(self.t('err_no_link_game'))

        game_name = game.get('name', 'Game')

        if not os.path.exists(TEMP_DIR):
            os.makedirs(TEMP_DIR)

        file_name = f"{game.get('title_id', 'game')}.pkg"
        temp_path = os.path.join(TEMP_DIR, file_name)

        try:
            # === FASE 1: Download (0% → 50%) ===
            self.after(0, lambda: self.status_label.configure(
                text=self.t('status_dl_game_pct', name=game_name, pct=0)
            ))
            response = requests.get(pkg_link, stream=True, timeout=60)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            with open(temp_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192 * 4):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            pct = int(downloaded * 100 / total_size)
                            self.after(0, lambda p=downloaded / total_size, pc=pct:
                                (
                                    self.progress_bar.set(p * 0.50),
                                    self.status_label.configure(text=self.t('status_dl_game_pct', name=game_name, pct=pc))
                                )
                            )

            # === FASE 2: Extração (50% → 75%) ===
            self.after(0, lambda: (
                self.progress_bar.set(0.50),
                self.status_label.configure(text=self.t('status_extract_game', name=game_name))
            ))

            def _log(line):
                if line.strip():
                    self.after(0, lambda ln=line: self.status_label.configure(
                        text=self.t('status_pkg2zip', line=ln[:80])
                    ))

            zrif = game.get('rap', '')
            core.extract_pkg(temp_path, zrif, TEMP_DIR, extract_as_eboot=False, log_callback=_log)

            # === FASE 3: Cópia para o PSP (75% → 100%) ===
            self.after(0, lambda: (
                self.progress_bar.set(0.75),
                self.status_label.configure(text=self.t('status_copy_game', name=game_name))
            ))

            def _copy_progress(copied, total):
                if total > 0:
                    p = 0.75 + 0.25 * (copied / total)
                    pct = int((copied / total) * 100)
                    self.after(0, lambda pv=p, pc=pct: (
                        self.progress_bar.set(pv),
                        self.status_label.configure(text=self.t('status_copy_pct', name=game_name, pct=pc))
                    ))

            core.transfer_to_psp(TEMP_DIR, self.selected_drive_path, progress_callback=_copy_progress)
        finally:
            self._cleanup_temp_dir(temp_path)

    def _download_update_internal(self, game):
        """Faz download de um update de título PSP com feedback completo.

        O update vai para PSP/GAME/<TITLE_ID>/ no drive PSP.
        """
        pkg_link = game.get('pkg_link', '')
        if not pkg_link:
            raise Exception(self.t('err_no_link_update', name=game.get('name', '?')))

        title_id  = game.get('title_id', 'UPDATE')
        game_name = game.get('name', '?')

        if not os.path.exists(TEMP_DIR):
            os.makedirs(TEMP_DIR)

        file_name = f"{title_id}_update.pkg"
        temp_path = os.path.join(TEMP_DIR, file_name)

        try:
            # === FASE 1: Download (0% → 50%) ===
            self.after(0, lambda: self.status_label.configure(
                text=self.t('status_dl_update_pct', name=game_name, pct=0)
            ))
            response = requests.get(pkg_link, stream=True, timeout=60)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            with open(temp_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192 * 4):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            pct = int(downloaded * 100 / total_size)
                            self.after(0, lambda p=downloaded / total_size, pc=pct: (
                                self.progress_bar.set(p * 0.50),
                                self.status_label.configure(text=self.t('status_dl_update_pct', name=game_name, pct=pc))
                            ))

            # === FASE 2: Extração (50% → 75%) ===
            self.after(0, lambda: (
                self.progress_bar.set(0.50),
                self.status_label.configure(text=self.t('status_extract_update', name=game_name))
            ))

            def _log(line):
                if line.strip():
                    self.after(0, lambda ln=line: self.status_label.configure(
                        text=self.t('status_pkg2zip', line=ln[:80])
                    ))

            zrif = game.get('rap', '')
            core.extract_pkg(temp_path, zrif, TEMP_DIR, extract_as_eboot=True, log_callback=_log)

            # === FASE 3: Cópia (75% → 100%) ===
            self.after(0, lambda: (
                self.progress_bar.set(0.75),
                self.status_label.configure(text=self.t('status_install_update', name=game_name, tid=title_id))
            ))

            def _copy_progress(copied, total):
                if total > 0:
                    p = 0.75 + 0.25 * (copied / total)
                    pct = int((copied / total) * 100)
                    self.after(0, lambda pv=p, pc=pct: (
                        self.progress_bar.set(pv),
                        self.status_label.configure(text=self.t('status_install_update_pct', name=game_name, pct=pc))
                    ))

            core.transfer_update_to_psp(
                TEMP_DIR, self.selected_drive_path, title_id,
                progress_callback=_copy_progress
            )

            self.after(0, lambda: self.status_label.configure(
                text=self.t('status_update_done', name=game_name, tid=title_id)
            ))
        finally:
            self._cleanup_temp_dir(temp_path)


    def _download_dlc_internal(self, game):
        """Faz download de um DLC de jogo PSP com feedback completo.

        DLCs vão para PSP/GAME/<TITLE_ID>/ no drive PSP.
        """
        pkg_link = game.get('pkg_link', '')
        if not pkg_link:
            raise Exception(self.t('err_no_link_dlc', name=game.get('name', '?')))

        title_id  = game.get('title_id', 'DLC')
        game_name = game.get('name', '?')

        if not os.path.exists(TEMP_DIR):
            os.makedirs(TEMP_DIR)

        file_name = f"{title_id}_{game.get('content_id', 'dlc')[-8:]}.pkg"
        temp_path = os.path.join(TEMP_DIR, file_name)

        try:
            # === FASE 1: Download (0% → 50%) ===
            self.after(0, lambda: self.status_label.configure(
                text=self.t('status_dl_dlc_pct', name=game_name, pct=0)
            ))
            response = requests.get(pkg_link, stream=True, timeout=60)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            with open(temp_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192 * 4):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            pct = int(downloaded * 100 / total_size)
                            self.after(0, lambda p=downloaded / total_size, pc=pct: (
                                self.progress_bar.set(p * 0.50),
                                self.status_label.configure(text=self.t('status_dl_dlc_pct', name=game_name, pct=pc))
                            ))

            # === FASE 2: Extração (50% → 75%) ===
            self.after(0, lambda: (
                self.progress_bar.set(0.50),
                self.status_label.configure(text=self.t('status_extract_dlc', name=game_name))
            ))

            def _log(line):
                if line.strip():
                    self.after(0, lambda ln=line: self.status_label.configure(
                        text=self.t('status_pkg2zip', line=ln[:80])
                    ))

            zrif = game.get('rap', '')
            core.extract_pkg(temp_path, zrif, TEMP_DIR, extract_as_eboot=True, log_callback=_log)

            # === FASE 3: Cópia (75% → 100%) ===
            self.after(0, lambda: (
                self.progress_bar.set(0.75),
                self.status_label.configure(text=self.t('status_install_dlc', name=game_name, tid=title_id))
            ))

            def _copy_progress(copied, total):
                if total > 0:
                    p = 0.75 + 0.25 * (copied / total)
                    pct = int((copied / total) * 100)
                    self.after(0, lambda pv=p, pc=pct: (
                        self.progress_bar.set(pv),
                        self.status_label.configure(text=self.t('status_install_dlc_pct', name=game_name, pct=pc))
                    ))

            core.transfer_update_to_psp(
                TEMP_DIR, self.selected_drive_path, title_id,
                progress_callback=_copy_progress
            )

            self.after(0, lambda: self.status_label.configure(
                text=self.t('status_dlc_done', name=game_name, tid=title_id)
            ))
        finally:
            self._cleanup_temp_dir(temp_path)

    def _download_theme_internal(self, game):
        """Instala um tema local em PSP/THEME/ no drive."""
        source_path = game.get('installed_path', '')
        if not source_path or not os.path.exists(source_path):
            raise Exception("Arquivo de tema local não encontrado")

        game_name = game.get('name', '?')

        try:
            self.after(0, lambda: self.status_label.configure(
                text=self.t('status_install_theme_s', name=game_name)
            ))

            target_dir = os.path.join(self.selected_drive_path, "PSP", "THEME")
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

            target_path = os.path.join(target_dir, os.path.basename(source_path))
            
            # Copiar arquivo
            shutil.copy2(source_path, target_path)

            self.after(0, lambda: self.status_label.configure(
                text=self.t('status_theme_done', name=game_name)
            ))
        except Exception as e:
            raise e

    def _download_game(self, game):
        """Faz o download do jogo selecionado"""
        try:
            pkg_link = game.get('pkg_link', '')
            if not pkg_link:
                self.after(0, lambda: messagebox.showerror("Erro", self.t('err_no_dl_link')))
                return

            # Criar pasta temp se não existir
            if not os.path.exists(TEMP_DIR):
                os.makedirs(TEMP_DIR)

            # Nome do arquivo
            file_name = f"{game.get('title_id', 'game')}.pkg"
            temp_path = os.path.join(TEMP_DIR, file_name)

            # Download
            game_name = game.get('name', 'game')
            self.after(0, lambda: self.status_label.configure(text=self.t('status_dl_game_legacy', name=game_name)))

            response = requests.get(pkg_link, stream=True, timeout=30)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0

            with open(temp_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            progress = downloaded / total_size
                            self.after(0, lambda p=progress: self.progress_bar.set(p))

            # Download concluído - agora extrair com pkg2zip
            self.after(0, lambda: self.status_label.configure(text=self.t('status_extract_legacy', name=game_name)))

            try:
                # Usar pkg2zip para extrair
                import core
                zrif = game.get('rap', '')  # Ou zrif se disponível

                # Extrair o PKG
                core.extract_pkg(temp_path, zrif, TEMP_DIR, extract_as_eboot=True)

                # Feedback de copiando para o console
                self.after(0, lambda: self.status_label.configure(text=self.t('status_copy_legacy')))

                # Transferir arquivos extraídos para o drive PSP
                core.transfer_to_psp(TEMP_DIR, self.selected_drive_path)

                # Limpar arquivos temporários
                if os.path.exists(temp_path):
                    os.remove(temp_path)

                self.after(0, lambda: self.status_label.configure(
                    text=self.t('status_dl_done_legacy', name=game_name)
                ))
                self.after(0, lambda: self.progress_bar.set(1))

                messagebox.showinfo(self.t('success_title'), self.t('success_dl_game', name=game_name))

            except Exception as extract_error:
                # Se falhar a extração, apenas mover o PKG como antes
                print(f"[DEBUG] Erro na extração, movendo PKG: {extract_error}")
                iso_path = os.path.join(self.selected_drive_path, "ISO")
                if not os.path.exists(iso_path):
                    os.makedirs(iso_path)

                final_path = os.path.join(iso_path, file_name)
                shutil.move(temp_path, final_path)

                self.after(0, lambda: self.status_label.configure(
                    text=self.t('status_dl_no_extract', name=game_name)
                ))
                self.after(0, lambda: self.progress_bar.set(1))
                messagebox.showwarning("Aviso", self.t('warn_pkg_no_extract'))

        except Exception as e:
            error_msg = self.t('err_dl_error', msg=str(e))
            print(f"[DEBUG] {error_msg}")
            # Garantir limpeza em caso de erro
            try:
                if 'temp_path' in locals() and os.path.exists(temp_path):
                    os.remove(temp_path)
            except Exception:
                pass
            self.after(0, lambda: self.status_label.configure(text=self.t('status_error', msg=error_msg)))
            self.after(0, lambda: messagebox.showerror("Erro", error_msg))

    def _update_drives(self):
        """Atualiza lista de drives USB"""
        drives = []
        for letter in ['C', 'D', 'E', 'F', 'G', 'H']:
            drive_path = f"{letter}:\\"
            if os.path.exists(drive_path):
                drives.append(drive_path)

        if drives:
            self.drive_combo.configure(values=drives)
            self.status_label.configure(text=self.t('status_drives_found', count=len(drives)))
        else:
            self.drive_combo.configure(values=[self.t('no_drives_found')])
            self.status_label.configure(text=self.t('status_no_drive'))

    def _on_drive_selected(self, choice):
        """Callback quando drive é selecionado"""
        self.selected_drive_path = choice
        if choice and self.t('no_drives_found') not in choice and "Nenhum" not in choice:
            self.status_label.configure(text=self.t('status_drive_sel', drive=choice))
            self.drive_path_label.configure(text=self.t('drive_sel', drive=choice))
            if hasattr(self, 'sidebar_drive_label'):
                self.sidebar_drive_label.configure(text=choice)
        else:
            self.status_label.configure(text=self.t('status_no_drive_sel'))
            self.drive_path_label.configure(text=self.t('drive_not_sel'))
            if hasattr(self, 'sidebar_drive_label'):
                self.sidebar_drive_label.configure(text="Não selecionado")


if __name__ == "__main__":
    app = PSPFreeshopApp()
    app.mainloop()
