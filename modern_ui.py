# -*- coding: utf-8 -*-
import os
import customtkinter as ctk

# Paleta de cores premium (espelha COLORS em main.py)
CARD_BG           = "#1e1e2e"
CARD_BG_HOVER     = "#252538"
CARD_BORDER       = "#2a2a3e"
CARD_BORDER_HOVER = "#7c6cfc"
COVER_BG          = "#13131f"


class GameCard(ctk.CTkFrame):
    """Card premium para exibir informações do jogo"""

    def __init__(self, parent, game_data, on_select_callback,
                 on_right_click_callback=None,
                 on_ctrl_click_callback=None,
                 on_shift_click_callback=None,
                 selection_color="#7c6cfc",
                 selection_bg="#1e1a35",
                 covers_dir=None,
                 **kwargs):
        super().__init__(parent, **kwargs)

        self.game_data = game_data
        self.on_select_callback = on_select_callback
        self.on_right_click_callback = on_right_click_callback
        self.on_ctrl_click_callback = on_ctrl_click_callback
        self.on_shift_click_callback = on_shift_click_callback
        self.selection_color = selection_color
        self.selection_bg = selection_bg
        self.is_selected = False
        self._hovering = False
        self._covers_dir = covers_dir
        self._cover_image_ref = None

        self.configure(
            width=170,
            height=240,
            corner_radius=12,
            fg_color=CARD_BG,
            border_color=CARD_BORDER,
            border_width=1,
        )
        self.pack_propagate(False)
        self.grid_propagate(False)

        self._create_content()
        self._bind_events()

    def _create_content(self):
        name      = self.game_data.get('name', 'Sem nome')
        region    = self.game_data.get('region', 'N/A')
        game_type = self.game_data.get('type', 'N/A')[:14]
        title_id  = self.game_data.get('title_id', 'N/A')
        file_size = self.game_data.get('file_size', '')

        # ── ÁREA DE CAPA ─────────────────────────────────────────
        self.cover_frame = ctk.CTkFrame(
            self,
            width=170,
            height=108,
            corner_radius=10,
            fg_color=COVER_BG,
        )
        self.cover_frame.pack(fill="x")
        self.cover_frame.pack_propagate(False)

        # Inicial do jogo como placeholder de capa
        initial = name[0].upper() if name else "?"
        self.cover_label = ctk.CTkLabel(
            self.cover_frame,
            text=initial,
            font=ctk.CTkFont(size=44, weight="bold"),
            text_color="#252540",
        )
        self.cover_label.place(relx=0.5, rely=0.5, anchor="center")
        self._load_cover_image(title_id)

        # Pill de região no canto superior direito
        self.region_pill = ctk.CTkLabel(
            self.cover_frame,
            text=region[:3],
            font=ctk.CTkFont(size=9, weight="bold"),
            text_color="#7a7a9a",
            fg_color="#1e1e30",
            corner_radius=4,
            width=30,
            height=16,
        )
        self.region_pill.place(relx=1.0, rely=0.0, anchor="ne", x=-6, y=6)

        # Checkbox no canto superior esquerdo
        self.checkbox = ctk.CTkCheckBox(
            self.cover_frame,
            text="",
            width=20,
            height=20,
            checkbox_width=16,
            checkbox_height=16,
            fg_color="#7c6cfc",
            hover_color="#9d8fff",
            command=self._on_checkbox_toggle,
        )
        self.checkbox.place(x=7, y=7)

        # ── ÁREA DE INFO ──────────────────────────────────────────
        info_frame = ctk.CTkFrame(self, fg_color="transparent")
        info_frame.pack(fill="both", expand=True, padx=10, pady=(8, 8))

        # Nome do jogo
        display_name = (name[:22] + "…") if len(name) > 22 else name
        self.name_label = ctk.CTkLabel(
            info_frame,
            text=display_name,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#e0e0ef",
            anchor="w",
            wraplength=148,
            justify="left",
        )
        self.name_label.pack(anchor="w")

        # Tipo + Tamanho
        size_str  = self._format_size(file_size)
        info_text = game_type
        if size_str:
            info_text += f"  ·  {size_str}"

        self.info_label = ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=ctk.CTkFont(size=9),
            text_color="#7a7a9a",
            anchor="w",
        )
        self.info_label.pack(anchor="w", pady=(2, 0))

        # Title ID
        self.id_label = ctk.CTkLabel(
            info_frame,
            text=title_id,
            font=ctk.CTkFont(size=8),
            text_color="#3a3a5a",
            anchor="w",
        )
        self.id_label.pack(anchor="w", pady=(2, 0))

    def _format_size(self, file_size):
        if not file_size:
            return ""
        try:
            size_bytes = int(file_size)
            if size_bytes >= 1024 ** 3:
                return f"{size_bytes / 1024 ** 3:.1f} GB"
            elif size_bytes >= 1024 ** 2:
                return f"{size_bytes / 1024 ** 2:.0f} MB"
            elif size_bytes >= 1024:
                return f"{size_bytes / 1024:.0f} KB"
            return f"{size_bytes} B"
        except Exception:
            return ""

    def _load_cover_image(self, title_id):
        """Carrega capa de CoversCompressed/[title_id]-01.png; mantém placeholder se não encontrar."""
        if not self._covers_dir or not title_id or title_id == 'N/A':
            return
        try:
            from PIL import Image
            for seq in ('01', '02'):
                img_path = os.path.join(self._covers_dir, f"{title_id}-{seq}.png")
                if os.path.exists(img_path):
                    pil_img = Image.open(img_path).convert("RGB")
                    # object-fit: cover — preenche 170×108 sem distorcer, corta o excesso
                    tw, th = 170, 108
                    iw, ih = pil_img.size
                    scale = max(tw / iw, th / ih)
                    nw, nh = int(iw * scale), int(ih * scale)
                    pil_img = pil_img.resize((nw, nh), Image.LANCZOS)
                    left = (nw - tw) // 2
                    top  = (nh - th) // 2
                    pil_img = pil_img.crop((left, top, left + tw, top + th))
                    ctk_img = ctk.CTkImage(pil_img, size=(tw, th))
                    self._cover_image_ref = ctk_img
                    self.cover_label.configure(image=ctk_img, text="")
                    return
        except Exception:
            pass  # mantém placeholder com inicial do jogo

    def _bind_events(self):
        widgets = [
            self, self.cover_frame, self.cover_label,
            self.name_label, self.info_label, self.id_label, self.region_pill,
        ]
        for w in widgets:
            w.bind("<Button-1>",         self._on_click)
            w.bind("<Button-3>",         self._on_right_click)
            w.bind("<Control-Button-1>", self._on_ctrl_click)
            w.bind("<Shift-Button-1>",   self._on_shift_click)
            w.bind("<Enter>",            self._on_enter)
            w.bind("<Leave>",            self._on_leave)

    def _on_checkbox_toggle(self):
        self.is_selected = bool(self.checkbox.get())
        if self.on_ctrl_click_callback:
            self.on_ctrl_click_callback(self.game_data, self.is_selected)
        self._refresh_style()

    def _on_click(self, event=None):
        new_state = not bool(self.checkbox.get())
        if new_state:
            self.checkbox.select()
        else:
            self.checkbox.deselect()
        self.is_selected = new_state
        self._refresh_style()
        self.on_select_callback(self)

    def _on_ctrl_click(self, event=None):
        new_state = not bool(self.checkbox.get())
        if new_state:
            self.checkbox.select()
        else:
            self.checkbox.deselect()
        self.is_selected = new_state
        self._refresh_style()
        if self.on_ctrl_click_callback:
            self.on_ctrl_click_callback(self.game_data, self.is_selected)
        return "break"

    def _on_shift_click(self, event=None):
        if self.on_shift_click_callback:
            self.on_shift_click_callback(self.game_data)
        return "break"

    def _on_right_click(self, event=None):
        if self.on_right_click_callback:
            self.on_right_click_callback(self.game_data, event)

    def _on_enter(self, event=None):
        self._hovering = True
        if not self.is_selected:
            self.configure(fg_color=CARD_BG_HOVER, border_color=CARD_BORDER_HOVER)

    def _on_leave(self, event=None):
        self._hovering = False
        if not self.is_selected:
            self.configure(fg_color=CARD_BG, border_color=CARD_BORDER)

    def _refresh_style(self):
        if self.is_selected:
            self.configure(
                fg_color=self.selection_bg,
                border_color=self.selection_color,
                border_width=2,
            )
        else:
            self.configure(
                fg_color=CARD_BG_HOVER if self._hovering else CARD_BG,
                border_color=CARD_BORDER_HOVER if self._hovering else CARD_BORDER,
                border_width=1,
            )

    def set_selected(self, selected, update_checkbox=True):
        """Define estado de seleção visual"""
        self.is_selected = selected
        if update_checkbox:
            if selected:
                self.checkbox.select()
            else:
                self.checkbox.deselect()
        self._refresh_style()


class GameGrid(ctk.CTkScrollableFrame):
    """Grid de jogos com scroll e seleção múltipla"""

    def __init__(self, parent, on_game_select, on_right_click_callback=None,
                 on_multi_select=None,
                 selection_color="#7c6cfc",
                 selection_bg="#1e1a35",
                 covers_dir=None,
                 **kwargs):
        super().__init__(parent, **kwargs)

        self.on_game_select          = on_game_select
        self.on_right_click_callback = on_right_click_callback
        self.on_multi_select         = on_multi_select
        self.selection_color         = selection_color
        self.selection_bg            = selection_bg
        self._covers_dir             = covers_dir
        self.cards                   = []
        self.selected_card           = None
        self.selected_games          = []
        self.games                   = []
        self.last_selected_index     = -1

        self.configure(fg_color="transparent")
        self.columns = 5
        self.padding = 8

    def display_games(self, games):
        """Exibe lista de jogos"""
        self.games = games
        self._clear_grid()
        self.selected_games      = []
        self.last_selected_index = -1

        if not games:
            self._show_empty_message()
            return

        for index, game in enumerate(games):
            self._create_card(game, index)

    def _clear_grid(self):
        for card in self.cards:
            card.destroy()
        self.cards.clear()
        self.selected_card = None

    def _show_empty_message(self):
        label = ctk.CTkLabel(
            self,
            text="Nenhum jogo encontrado",
            font=ctk.CTkFont(size=14),
            text_color="#3a3a5a",
        )
        label.pack(pady=80)
        self.cards.append(label)

    def _create_card(self, game, index):
        try:
            row = index // self.columns
            col = index % self.columns

            card = GameCard(
                self,
                game,
                self._on_card_selected,
                self.on_right_click_callback,
                self._on_ctrl_click,
                self._on_shift_click,
                selection_color=self.selection_color,
                selection_bg=self.selection_bg,
                covers_dir=self._covers_dir,
            )
            card.index = index

            card.grid(
                row=row,
                column=col,
                padx=self.padding,
                pady=self.padding,
                sticky="n",
            )
            self.cards.append(card)
        except Exception as e:
            print(f"Erro ao criar card: {e}")

    def _on_card_selected(self, card):
        selected_set = {c for c in self.cards if hasattr(c, 'is_selected') and c.is_selected}
        if card not in selected_set:
            self._clear_selection()

        self.selected_card = card
        card.set_selected(True)
        self.last_selected_index = card.index
        self._update_selected_games()
        self.on_game_select(card.game_data)

    def _on_ctrl_click(self, game_data, is_selected):
        if is_selected:
            if game_data not in self.selected_games:
                self.selected_games.append(game_data)
        else:
            if game_data in self.selected_games:
                self.selected_games.remove(game_data)

        for card in self.cards:
            if hasattr(card, 'game_data') and card.game_data == game_data:
                self.last_selected_index = card.index
                break

        if self.on_multi_select:
            self.on_multi_select(self.selected_games)

    def _on_shift_click(self, game_data):
        clicked_index = -1
        for i, card in enumerate(self.cards):
            if hasattr(card, 'game_data') and card.game_data == game_data:
                clicked_index = i
                break

        if clicked_index == -1 or self.last_selected_index == -1:
            return

        start = min(self.last_selected_index, clicked_index)
        end   = max(self.last_selected_index, clicked_index)

        for i in range(start, end + 1):
            if i < len(self.cards):
                card = self.cards[i]
                card.set_selected(True)
                if hasattr(card, 'game_data') and card.game_data not in self.selected_games:
                    self.selected_games.append(card.game_data)

        if self.on_multi_select:
            self.on_multi_select(self.selected_games)

    def _clear_selection(self):
        for card in self.cards:
            if hasattr(card, 'set_selected'):
                card.set_selected(False)
        self.selected_games = []

    def _update_selected_games(self):
        self.selected_games = [
            card.game_data
            for card in self.cards
            if hasattr(card, 'is_selected') and card.is_selected
        ]
        if self.on_multi_select:
            self.on_multi_select(self.selected_games)

    def get_selected_games(self):
        return self.selected_games

    def get_selected_game(self):
        if self.selected_games:
            return self.selected_games[0]
        return None
