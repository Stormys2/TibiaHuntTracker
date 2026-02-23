"""
Tibia Hunt Tracker  ·  v3.0
────────────────────────────
Requiere: pip install customtkinter
Datos:    tibia_users.json  (usuarios/contraseñas)
          tibia_hunts_<usuario>.json  (hunts por usuario)
"""

import json, os, hashlib, calendar
from datetime import date, timedelta
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageDraw     # pip install pillow

# ══════════════════════════════════════════════════════════════════════════════
# RUTAS
# ══════════════════════════════════════════════════════════════════════════════
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, "tibia_users.json")

def hunt_file(username: str) -> str:
    return os.path.join(BASE_DIR, f"tibia_hunts_{username}.json")

# ══════════════════════════════════════════════════════════════════════════════
# PERSISTENCIA
# ══════════════════════════════════════════════════════════════════════════════
def load_json(path: str) -> dict:
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_json(path: str, data: dict):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

# ══════════════════════════════════════════════════════════════════════════════
# INTERNACIONALIZACIÓN
# ══════════════════════════════════════════════════════════════════════════════
LANG = {
    "es": {
        "app_title":        "Tibia Hunt Tracker",
        "created_by":       "creado por Axels2",
        "login_title":      "Iniciar Sesión",
        "register_title":   "Crear Cuenta",
        "username":         "Usuario",
        "password":         "Contraseña",
        "confirm_pw":       "Confirmar Contraseña",
        "btn_login":        "Entrar",
        "btn_register":     "Registrarse",
        "btn_go_register":  "¿No tienes cuenta? Regístrate",
        "btn_go_login":     "¿Ya tienes cuenta? Inicia sesión",
        "err_fields":       "Completa todos los campos.",
        "err_user_exists":  "Ese usuario ya existe.",
        "err_pw_match":     "Las contraseñas no coinciden.",
        "err_invalid":      "Usuario o contraseña incorrectos.",
        "err_short_pw":     "La contraseña debe tener al menos 4 caracteres.",
        "err_short_user":   "El usuario debe tener al menos 3 caracteres.",
        "ok_registered":    "¡Cuenta creada! Ya puedes iniciar sesión.",
        "tab_hunts":        "⚡  Mis Hunts",
        "tab_calendar":     "📅  Calendario",
        "hunt_session":     "Hunt Session",
        "hunt_sub":         "Registra tu sesión y guárdala en el historial",
        "date_label":       "📅  Fecha de la hunt",
        "xp_label":         "🔮 Experiencia Ganada",
        "loot_label":       "💰 Loot Total (gp)",
        "sup_label":        "🧪 Supplies Gastadas (gp)",
        "tc_label":         "💎 Precio de TC (gp/TC)",
        "btn_calc":         "⚡  CALCULAR",
        "btn_save":         "💾  GUARDAR HUNT",
        "this_session":     "Esta sesión",
        "xp_col":           "🔮 XP",
        "profit_gp":        "💰 Profit (gp)",
        "profit_tc":        "💎 Profit (TC)",
        "stats_title":      "Estadísticas acumuladas",
        "period_week":      "Semana",
        "period_month":     "Mes",
        "period_year":      "Año",
        "period_label":     "  Período: ",
        "xp_total":         "🔮 XP Total",
        "balance_gp":       "💰 Balance (gp)",
        "balance_tc":       "💎 Balance (TC)",
        "cal_title":        "Resumen del mes",
        "cal_days":         "📅 Días",
        "day_detail":       "Detalle del día",
        "no_records":       "Sin registros para este día",
        "hunt_n":           "Hunt #",
        "loot_row":         "💰 Loot",
        "sup_row":          "🧪 Supplies",
        "bal_row":          "📊 Balance",
        "bal_tc_row":       "💎 Balance TC",
        "btn_delete":       "🗑 Eliminar",
        "del_confirm":      "¿Eliminar esta hunt?",
        "day_total":        "Total del día",
        "saved_ok":         "Hunt guardada correctamente.\nRegistros hoy: ",
        "logout":           "Cerrar Sesión",
        "months": ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
                   "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"],
        "weekdays": ["Lun","Mar","Mié","Jue","Vie","Sáb","Dom"],
    },
    "en": {
        "app_title":        "Tibia Hunt Tracker",
        "created_by":       "created by Axels2",
        "login_title":      "Sign In",
        "register_title":   "Create Account",
        "username":         "Username",
        "password":         "Password",
        "confirm_pw":       "Confirm Password",
        "btn_login":        "Sign In",
        "btn_register":     "Register",
        "btn_go_register":  "No account? Register here",
        "btn_go_login":     "Already have an account? Sign in",
        "err_fields":       "Please fill in all fields.",
        "err_user_exists":  "That username already exists.",
        "err_pw_match":     "Passwords do not match.",
        "err_invalid":      "Invalid username or password.",
        "err_short_pw":     "Password must be at least 4 characters.",
        "err_short_user":   "Username must be at least 3 characters.",
        "ok_registered":    "Account created! You can now sign in.",
        "tab_hunts":        "⚡  My Hunts",
        "tab_calendar":     "📅  Calendar",
        "hunt_session":     "Hunt Session",
        "hunt_sub":         "Log your session and save it to history",
        "date_label":       "📅  Hunt date",
        "xp_label":         "🔮 Experience Gained",
        "loot_label":       "💰 Total Loot (gp)",
        "sup_label":        "🧪 Supplies Spent (gp)",
        "tc_label":         "💎 TC Price (gp/TC)",
        "btn_calc":         "⚡  CALCULATE",
        "btn_save":         "💾  SAVE HUNT",
        "this_session":     "This session",
        "xp_col":           "🔮 XP",
        "profit_gp":        "💰 Profit (gp)",
        "profit_tc":        "💎 Profit (TC)",
        "stats_title":      "Accumulated Stats",
        "period_week":      "Week",
        "period_month":     "Month",
        "period_year":      "Year",
        "period_label":     "  Period: ",
        "xp_total":         "🔮 Total XP",
        "balance_gp":       "💰 Balance (gp)",
        "balance_tc":       "💎 Balance (TC)",
        "cal_title":        "Month Summary",
        "cal_days":         "📅 Days",
        "day_detail":       "Day Detail",
        "no_records":       "No records for this day",
        "hunt_n":           "Hunt #",
        "loot_row":         "💰 Loot",
        "sup_row":          "🧪 Supplies",
        "bal_row":          "📊 Balance",
        "bal_tc_row":       "💎 Balance TC",
        "btn_delete":       "🗑 Delete",
        "del_confirm":      "Delete this hunt?",
        "day_total":        "Day Total",
        "saved_ok":         "Hunt saved!\nRecords today: ",
        "logout":           "Sign Out",
        "months": ["January","February","March","April","May","June",
                   "July","August","September","October","November","December"],
        "weekdays": ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# PALETA
# ══════════════════════════════════════════════════════════════════════════════
BG_DARK      = "#0A0C14"
BG_MID       = "#10131F"
BG_CARD      = "#161929"
BG_CARD2     = "#1C2035"
BG_INPUT     = "#1E2236"
ACCENT       = "#7C6EF8"
ACCENT2      = "#5A4FD4"
ACCENT_HOV   = "#9B8EFF"
TEXT_PRI     = "#E4E6F0"
TEXT_MUT     = "#545878"
TEXT_MUT2    = "#7A7FA8"
PROFIT_G     = "#2EE87A"
WASTE_R      = "#FF3D5A"
GOLD         = "#F0C040"
DIVIDER      = "#1E2240"
CAL_TODAY    = "#2A2650"
CAL_HAS      = "#1E3A28"
CAL_SEL      = "#4A3FCC"
CAL_WKND     = "#1A1C2E"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ══════════════════════════════════════════════════════════════════════════════
# ÍCONO PIXEL ART  — cockapoo marrón dibujado con PIL
# ══════════════════════════════════════════════════════════════════════════════
def make_icon() -> ImageDraw:
    """Genera un ícono 64×64 pixel art de un cockapoo marrón."""
    SIZE = 64
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d   = ImageDraw.Draw(img)

    # Paleta cockapoo
    FUR     = (139, 90,  43)   # marrón base
    FUR_D   = (100, 60,  20)   # sombra
    FUR_L   = (180, 130, 70)   # luz / rizos
    EYE     = (30,  20,  10)   # ojos oscuros
    EYE_SH  = (255, 255, 255)  # brillo ojo
    NOSE    = (50,  30,  20)   # nariz
    TONGUE  = (220, 80,  100)  # lengua
    BG_C    = (18,  20,  38)   # fondo de la imagen

    # Fondo redondeado
    d.rounded_rectangle([0, 0, 63, 63], radius=14, fill=BG_C)

    # ── Orejas (caídas, peludas) ──────────────────────────────────────────
    # Oreja izquierda
    d.ellipse([6, 18, 24, 46], fill=FUR_D)
    d.ellipse([8, 20, 22, 44], fill=FUR)
    # Oreja derecha
    d.ellipse([40, 18, 58, 46], fill=FUR_D)
    d.ellipse([42, 20, 56, 44], fill=FUR)

    # ── Cabeza ────────────────────────────────────────────────────────────
    d.ellipse([12, 12, 52, 50], fill=FUR)

    # ── Pelaje rizado (puntos más claros encima) ───────────────────────────
    for x, y in [(16,14),(22,11),(30,10),(38,11),(44,14),
                 (14,22),(46,22),(15,32),(47,30)]:
        d.ellipse([x-3, y-3, x+3, y+3], fill=FUR_L)

    # ── Ojos ──────────────────────────────────────────────────────────────
    for ex in [23, 41]:
        d.ellipse([ex-5, 23, ex+5, 33], fill=EYE)
        d.ellipse([ex+1, 24, ex+4, 27], fill=EYE_SH)   # brillo

    # ── Nariz ─────────────────────────────────────────────────────────────
    d.ellipse([28, 35, 36, 41], fill=NOSE)
    d.ellipse([30, 36, 34, 40], fill=(80, 50, 30))

    # ── Boca / lengua ─────────────────────────────────────────────────────
    d.arc([27, 38, 37, 46], start=0, end=180, fill=FUR_D, width=2)
    d.ellipse([29, 41, 35, 48], fill=TONGUE)

    # ── Flequillo ─────────────────────────────────────────────────────────
    for x, y in [(24,15),(30,13),(36,14)]:
        d.ellipse([x-4, y-3, x+4, y+4], fill=FUR_L)

    return img


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS MATEMÁTICOS
# ══════════════════════════════════════════════════════════════════════════════
def parse_number(raw: str) -> float:
    s = raw.strip()
    if not s:
        return 0.0
    has_comma, has_dot = "," in s, "." in s
    if has_comma and has_dot:
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "").replace(",", ".")
        else:
            s = s.replace(",", "")
    elif has_comma:
        parts = s.split(",")
        if len(parts) > 2 or (len(parts) == 2 and len(parts[-1]) == 3):
            s = s.replace(",", "")
        else:
            s = s.replace(",", ".")
    elif has_dot:
        parts = s.split(".")
        if len(parts) > 2 or (len(parts) == 2 and len(parts[-1]) == 3):
            s = s.replace(".", "")
    return float(s)

def fmt_num(n: float, dec=0) -> str:
    sign = "+" if n > 0 else ""
    return f"{sign}{n:,.{dec}f}"

def week_range(d: date):
    s = d - timedelta(days=d.weekday())
    return s, s + timedelta(days=6)

def month_range(d: date):
    s = d.replace(day=1)
    return s, d.replace(day=calendar.monthrange(d.year, d.month)[1])

def sum_range(data: dict, start: date, end: date):
    exp = loot = sup = 0.0
    cur = start
    while cur <= end:
        for h in data.get(cur.strftime("%Y-%m-%d"), []):
            exp  += h.get("experience", 0)
            loot += h.get("loot", 0)
            sup  += h.get("supplies", 0)
        cur += timedelta(days=1)
    return exp, loot, sup, loot - sup


# ══════════════════════════════════════════════════════════════════════════════
# PANTALLA DE LOGIN / REGISTRO
# ══════════════════════════════════════════════════════════════════════════════
class AuthScreen(ctk.CTkFrame):
    def __init__(self, master, lang: str, on_lang_change, on_login):
        super().__init__(master, fg_color=BG_DARK)
        self.lang           = lang
        self.on_lang_change = on_lang_change
        self.on_login       = on_login
        self.mode           = "login"   # "login" | "register"
        self._build()

    def t(self, key): return LANG[self.lang][key]

    def _build(self):
        self.pack(fill="both", expand=True)

        # ── Barra de idioma (top-right) ───────────────────────────────────
        top_bar = ctk.CTkFrame(self, fg_color=BG_MID, height=36, corner_radius=0)
        top_bar.pack(fill="x")
        top_bar.pack_propagate(False)

        ctk.CTkLabel(top_bar, text=f"  ⚔  {self.t('app_title')}",
                     font=ctk.CTkFont("Consolas", 12, "bold"),
                     text_color=ACCENT).pack(side="left", padx=10)

        lang_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        lang_frame.pack(side="right", padx=10)

        for code, label in [("es", "🇪🇸 ES"), ("en", "🇬🇧 EN")]:
            color = ACCENT if self.lang == code else BG_CARD
            ctk.CTkButton(lang_frame, text=label, width=54, height=24,
                          fg_color=color, hover_color=ACCENT2,
                          font=ctk.CTkFont("Consolas", 10),
                          corner_radius=6,
                          command=lambda c=code: self.on_lang_change(c)
                          ).pack(side="left", padx=2)

        # ── Centro ────────────────────────────────────────────────────────
        center = ctk.CTkFrame(self, fg_color=BG_DARK)
        center.pack(expand=True)

        # Ícono pixel art
        try:
            pil_img = make_icon()
            big = pil_img.resize((96, 96), Image.NEAREST)
            self._icon_img = ctk.CTkImage(light_image=big, dark_image=big, size=(96, 96))
            ctk.CTkLabel(center, image=self._icon_img, text="").pack(pady=(0, 6))
        except Exception:
            ctk.CTkLabel(center, text="🐶", font=ctk.CTkFont(size=64)).pack(pady=(0, 6))

        ctk.CTkLabel(center, text=self.t("app_title"),
                     font=ctk.CTkFont("Consolas", 22, "bold"),
                     text_color=ACCENT).pack()
        ctk.CTkLabel(center, text=self.t("created_by"),
                     font=ctk.CTkFont("Consolas", 9),
                     text_color=TEXT_MUT).pack(pady=(2, 20))

        # ── Card de formulario ────────────────────────────────────────────
        self.card = ctk.CTkFrame(center, fg_color=BG_CARD, corner_radius=16,
                                  width=340)
        self.card.pack(ipadx=20, ipady=10)
        # NO pack_propagate(False) — dejar que crezca con el contenido

        self.lbl_title = ctk.CTkLabel(self.card, text=self.t("login_title"),
                                       font=ctk.CTkFont("Consolas", 15, "bold"),
                                       text_color=GOLD)
        self.lbl_title.pack(pady=(20, 14))

        # Usuario
        ctk.CTkLabel(self.card, text=self.t("username"),
                     font=ctk.CTkFont("Consolas", 10), text_color=TEXT_MUT,
                     anchor="w").pack(fill="x", padx=24)
        self.ent_user = ctk.CTkEntry(self.card, placeholder_text="axels2",
                                      fg_color=BG_INPUT, border_color=DIVIDER,
                                      text_color=TEXT_PRI,
                                      font=ctk.CTkFont("Consolas", 12),
                                      height=38, corner_radius=8)
        self.ent_user.pack(fill="x", padx=24, pady=(2, 10))

        # Contraseña
        ctk.CTkLabel(self.card, text=self.t("password"),
                     font=ctk.CTkFont("Consolas", 10), text_color=TEXT_MUT,
                     anchor="w").pack(fill="x", padx=24)
        self.ent_pw = ctk.CTkEntry(self.card, placeholder_text="••••••••",
                                    show="•",
                                    fg_color=BG_INPUT, border_color=DIVIDER,
                                    text_color=TEXT_PRI,
                                    font=ctk.CTkFont("Consolas", 12),
                                    height=38, corner_radius=8)
        self.ent_pw.pack(fill="x", padx=24, pady=(2, 10))

        # Confirmar contraseña (solo en registro)
        self.frm_confirm = ctk.CTkFrame(self.card, fg_color="transparent")
        ctk.CTkLabel(self.frm_confirm, text=self.t("confirm_pw"),
                     font=ctk.CTkFont("Consolas", 10), text_color=TEXT_MUT,
                     anchor="w").pack(fill="x")
        self.ent_pw2 = ctk.CTkEntry(self.frm_confirm, placeholder_text="••••••••",
                                     show="•",
                                     fg_color=BG_INPUT, border_color=DIVIDER,
                                     text_color=TEXT_PRI,
                                     font=ctk.CTkFont("Consolas", 12),
                                     height=38, corner_radius=8)
        self.ent_pw2.pack(fill="x", pady=(2, 0))

        # Error label
        self.lbl_err = ctk.CTkLabel(self.card, text="",
                                     font=ctk.CTkFont("Consolas", 9),
                                     text_color=WASTE_R)
        self.lbl_err.pack(pady=(4, 0))

        # Botón principal
        self.btn_main = ctk.CTkButton(self.card, text=self.t("btn_login"),
                                       font=ctk.CTkFont("Consolas", 13, "bold"),
                                       fg_color=ACCENT, hover_color=ACCENT_HOV,
                                       height=42, corner_radius=10,
                                       command=self._submit)
        self.btn_main.pack(fill="x", padx=24, pady=(10, 6))

        # Toggle login/register
        self.btn_toggle = ctk.CTkButton(self.card, text=self.t("btn_go_register"),
                                         font=ctk.CTkFont("Consolas", 9),
                                         fg_color="transparent",
                                         hover_color=BG_CARD2,
                                         text_color=TEXT_MUT2,
                                         height=28,
                                         command=self._toggle_mode)
        self.btn_toggle.pack(pady=(0, 16))

        # Bind Enter
        self.ent_user.bind("<Return>", lambda e: self._submit())
        self.ent_pw.bind("<Return>",   lambda e: self._submit())
        self.ent_pw2.bind("<Return>",  lambda e: self._submit())

    def _toggle_mode(self):
        self.mode = "register" if self.mode == "login" else "login"
        self.lbl_err.configure(text="")
        if self.mode == "register":
            self.lbl_title.configure(text=self.t("register_title"))
            self.btn_main.configure(text=self.t("btn_register"))
            self.btn_toggle.configure(text=self.t("btn_go_login"))
            self.frm_confirm.pack(fill="x", padx=24, pady=(0, 4))
        else:
            self.lbl_title.configure(text=self.t("login_title"))
            self.btn_main.configure(text=self.t("btn_login"))
            self.btn_toggle.configure(text=self.t("btn_go_register"))
            self.frm_confirm.pack_forget()

    def _submit(self):
        self.lbl_err.configure(text="")
        users = load_json(USERS_FILE)
        u = self.ent_user.get().strip().lower()
        p = self.ent_pw.get()

        if not u or not p:
            self.lbl_err.configure(text=self.t("err_fields")); return

        if self.mode == "login":
            if u not in users or users[u] != hash_pw(p):
                self.lbl_err.configure(text=self.t("err_invalid")); return
            self.on_login(u)

        else:  # register
            p2 = self.ent_pw2.get()
            if len(u) < 3:
                self.lbl_err.configure(text=self.t("err_short_user")); return
            if len(p) < 4:
                self.lbl_err.configure(text=self.t("err_short_pw")); return
            if p != p2:
                self.lbl_err.configure(text=self.t("err_pw_match")); return
            if u in users:
                self.lbl_err.configure(text=self.t("err_user_exists")); return
            users[u] = hash_pw(p)
            save_json(USERS_FILE, users)
            messagebox.showinfo("✅", self.t("ok_registered"))
            self._toggle_mode()


# ══════════════════════════════════════════════════════════════════════════════
# PESTAÑA HUNTS
# ══════════════════════════════════════════════════════════════════════════════
class TabHunts(ctk.CTkFrame):
    def __init__(self, master, data: dict, lang: str, on_save):
        super().__init__(master, fg_color=BG_DARK)
        self.data    = data
        self.lang    = lang
        self.on_save = on_save
        self.entries = {}
        self._build()

    def t(self, k): return LANG[self.lang][k]

    def _build(self):
        scroll = ctk.CTkScrollableFrame(self, fg_color=BG_DARK,
                                         scrollbar_button_color=ACCENT2)
        scroll.pack(fill="both", expand=True)
        inner = ctk.CTkFrame(scroll, fg_color=BG_DARK)
        inner.pack(fill="both", expand=True, padx=20, pady=16)

        # Header
        ctk.CTkLabel(inner, text=self.t("hunt_session"),
                     font=ctk.CTkFont("Consolas", 14, "bold"),
                     text_color=GOLD).pack(anchor="w")
        ctk.CTkLabel(inner, text=self.t("hunt_sub"),
                     font=ctk.CTkFont("Consolas", 9),
                     text_color=TEXT_MUT).pack(anchor="w", pady=(2, 12))

        # Fecha
        date_card = ctk.CTkFrame(inner, fg_color=BG_CARD, corner_radius=10)
        date_card.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(date_card, text=self.t("date_label"),
                     font=ctk.CTkFont("Consolas", 9), text_color=TEXT_MUT
                     ).pack(anchor="w", padx=14, pady=(10, 4))

        di = ctk.CTkFrame(date_card, fg_color="transparent")
        di.pack(fill="x", padx=14, pady=(0, 12))

        today = date.today()
        self.var_day   = ctk.StringVar(value=str(today.day))
        self.var_month = ctk.StringVar(value=self.t("months")[today.month - 1])
        self.var_year  = ctk.StringVar(value=str(today.year))

        for var, vals, w in [
            (self.var_day,   [str(d) for d in range(1, 32)], 70),
            (self.var_month, self.t("months"),                160),
            (self.var_year,  [str(y) for y in range(2023, 2031)], 90),
        ]:
            ctk.CTkComboBox(di, values=vals, variable=var, width=w, height=32,
                             fg_color=BG_INPUT, border_color=DIVIDER,
                             button_color=ACCENT2, dropdown_fg_color=BG_CARD2,
                             font=ctk.CTkFont("Consolas", 11),
                             text_color=TEXT_PRI).pack(side="left", padx=(0, 6))

        # Inputs 2×2
        card = ctk.CTkFrame(inner, fg_color=BG_CARD, corner_radius=10)
        card.pack(fill="x", pady=(0, 10))
        g = ctk.CTkFrame(card, fg_color="transparent")
        g.pack(fill="x", padx=14, pady=12)
        g.columnconfigure(0, weight=1); g.columnconfigure(1, weight=1)

        fields = [
            ("experience", self.t("xp_label"),   "ej: 1000000", 0, 0),
            ("loot",       self.t("loot_label"),  "ej: 300000",  0, 1),
            ("supplies",   self.t("sup_label"),   "ej: 180000",  1, 0),
            ("tc_price",   self.t("tc_label"),    "ej: 9500",    1, 1),
        ]
        for key, lbl, ph, r, c in fields:
            self._add_field(g, key, lbl, ph, r, c)

        # Botones
        br = ctk.CTkFrame(inner, fg_color="transparent")
        br.pack(fill="x", pady=(0, 10))
        ctk.CTkButton(br, text=self.t("btn_calc"),
                      font=ctk.CTkFont("Consolas", 12, "bold"),
                      fg_color=ACCENT, hover_color=ACCENT_HOV,
                      corner_radius=8, height=38,
                      command=self._calculate).pack(side="left", expand=True, fill="x", padx=(0, 6))
        ctk.CTkButton(br, text=self.t("btn_save"),
                      font=ctk.CTkFont("Consolas", 12, "bold"),
                      fg_color="#2A6640", hover_color="#3A8A55",
                      corner_radius=8, height=38,
                      command=self._save_hunt).pack(side="left", expand=True, fill="x")

        # Resultados sesión
        rc = ctk.CTkFrame(inner, fg_color=BG_CARD, corner_radius=10)
        rc.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(rc, text=self.t("this_session"),
                     font=ctk.CTkFont("Consolas", 11, "bold"),
                     text_color=TEXT_PRI).pack(anchor="w", padx=14, pady=(12, 6))
        rr = ctk.CTkFrame(rc, fg_color="transparent")
        rr.pack(fill="x", padx=14, pady=(0, 12))
        rr.columnconfigure(0, weight=1); rr.columnconfigure(1, weight=1); rr.columnconfigure(2, weight=1)
        self.lbl_exp  = self._res_col(rr, self.t("xp_col"),     "—", 0)
        self.lbl_gold = self._res_col(rr, self.t("profit_gp"),  "—", 1)
        self.lbl_tc   = self._res_col(rr, self.t("profit_tc"),  "—", 2)
        self.lbl_err  = ctk.CTkLabel(rc, text="",
                                      font=ctk.CTkFont("Consolas", 9), text_color=WASTE_R)
        self.lbl_err.pack(anchor="w", padx=14, pady=(0, 6))

        # Stats acumuladas
        sc = ctk.CTkFrame(inner, fg_color=BG_CARD, corner_radius=10)
        sc.pack(fill="x", pady=(0, 4))
        sh = ctk.CTkFrame(sc, fg_color="transparent")
        sh.pack(fill="x", padx=14, pady=(12, 6))
        ctk.CTkLabel(sh, text=self.t("stats_title"),
                     font=ctk.CTkFont("Consolas", 11, "bold"),
                     text_color=TEXT_PRI).pack(side="left")

        self.var_period = ctk.StringVar(value=self.t("period_week"))
        seg = ctk.CTkSegmentedButton(sh,
                                      values=[self.t("period_week"),
                                              self.t("period_month"),
                                              self.t("period_year")],
                                      variable=self.var_period,
                                      font=ctk.CTkFont("Consolas", 10),
                                      fg_color=BG_CARD2,
                                      selected_color=ACCENT2,
                                      selected_hover_color=ACCENT,
                                      unselected_color=BG_CARD2,
                                      unselected_hover_color=BG_INPUT,
                                      command=self._refresh_stats)
        seg.pack(side="right")

        sf = ctk.CTkFrame(sc, fg_color="transparent")
        sf.pack(fill="x", padx=14, pady=(0, 6))
        sf.columnconfigure(0, weight=1); sf.columnconfigure(1, weight=1); sf.columnconfigure(2, weight=1)
        self.stat_exp = self._res_col(sf, self.t("xp_total"),   "—", 0)
        self.stat_bal = self._res_col(sf, self.t("balance_gp"), "—", 1)
        self.stat_tc  = self._res_col(sf, self.t("balance_tc"), "—", 2)
        self.lbl_period_sub = ctk.CTkLabel(sc, text="",
                                            font=ctk.CTkFont("Consolas", 8),
                                            text_color=TEXT_MUT)
        self.lbl_period_sub.pack(anchor="w", padx=14, pady=(0, 10))

        self._refresh_stats()

    def _add_field(self, parent, key, label, ph, row, col):
        w = ctk.CTkFrame(parent, fg_color="transparent")
        w.grid(row=row, column=col,
               padx=(0, 6) if col == 0 else (6, 0), pady=4, sticky="ew")
        ctk.CTkLabel(w, text=label, font=ctk.CTkFont("Consolas", 9),
                     text_color=TEXT_MUT, anchor="w").pack(fill="x", pady=(0, 2))
        e = ctk.CTkEntry(w, placeholder_text=ph,
                          font=ctk.CTkFont("Consolas", 12),
                          fg_color=BG_INPUT, border_color=DIVIDER,
                          border_width=1, text_color=TEXT_PRI,
                          placeholder_text_color=TEXT_MUT,
                          corner_radius=8, height=36)
        e.pack(fill="x")
        self.entries[key] = e

    def _res_col(self, parent, label, value, col):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.grid(row=0, column=col, sticky="ew", padx=2, pady=4)
        ctk.CTkLabel(f, text=label, font=ctk.CTkFont("Consolas", 8),
                     text_color=TEXT_MUT).pack(anchor="center")
        lbl = ctk.CTkLabel(f, text=value,
                            font=ctk.CTkFont("Consolas", 12, "bold"),
                            text_color=TEXT_PRI)
        lbl.pack(anchor="center", pady=(2, 0))
        return lbl

    def _get_date_key(self) -> str:
        months = self.t("months")
        try:
            m_str = self.var_month.get()
            month = months.index(m_str) + 1 if m_str in months else int(m_str)
            return f"{int(self.var_year.get()):04d}-{month:02d}-{int(self.var_day.get()):02d}"
        except Exception:
            return date.today().strftime("%Y-%m-%d")

    def _calculate(self):
        self.lbl_err.configure(text="")
        try:
            exp      = parse_number(self.entries["experience"].get())
            loot     = parse_number(self.entries["loot"].get())
            supplies = parse_number(self.entries["supplies"].get())
            tc_price = parse_number(self.entries["tc_price"].get()) or 1
            balance  = loot - supplies
            color    = PROFIT_G if balance >= 0 else WASTE_R
            self.lbl_exp.configure(text=f"{exp:,.0f} XP", text_color=GOLD)
            self.lbl_gold.configure(text=f"{fmt_num(balance)} gp", text_color=color)
            self.lbl_tc.configure(text=f"{fmt_num(balance/tc_price, 2)} TC", text_color=color)
            self._last = dict(experience=exp, loot=loot, supplies=supplies, tc_price=tc_price)
        except Exception as e:
            self.lbl_err.configure(text=f"Error: {e}")

    def _save_hunt(self):
        if not hasattr(self, "_last"):
            self._calculate()
            if not hasattr(self, "_last"):
                return
        key = self._get_date_key()
        if key not in self.data:
            self.data[key] = []
        self.data[key].append(self._last)
        save_json(hunt_file(self._username), self.data)
        del self._last
        messagebox.showinfo("✅", self.t("saved_ok") + str(len(self.data[key])))
        self._refresh_stats()
        self.on_save()

    def set_username(self, u: str):
        self._username = u

    def _refresh_stats(self, *_):
        today  = date.today()
        period = self.var_period.get()
        wk, mo, yr = self.t("period_week"), self.t("period_month"), self.t("period_year")
        if period == wk:
            start, end = week_range(today)
            label = f"{start.strftime('%d/%m')} – {end.strftime('%d/%m/%Y')}"
        elif period == mo:
            start, end = month_range(today)
            label = f"{self.t('months')[today.month-1]} {today.year}"
        else:
            start = today.replace(month=1, day=1)
            end   = today.replace(month=12, day=31)
            label = str(today.year)
        exp, loot, sup, balance = sum_range(self.data, start, end)
        tc = max(parse_number(self.entries["tc_price"].get()), 1) if self.entries else 1
        color = PROFIT_G if balance >= 0 else WASTE_R
        self.stat_exp.configure(text=f"{exp:,.0f}", text_color=GOLD)
        self.stat_bal.configure(text=f"{fmt_num(balance)} gp", text_color=color)
        self.stat_tc.configure(text=f"{fmt_num(balance/tc, 2)} TC", text_color=color)
        self.lbl_period_sub.configure(text=self.t("period_label") + label)


# ══════════════════════════════════════════════════════════════════════════════
# PESTAÑA CALENDARIO
# ══════════════════════════════════════════════════════════════════════════════
class TabCalendar(ctk.CTkFrame):
    def __init__(self, master, data: dict, lang: str):
        super().__init__(master, fg_color=BG_DARK)
        self.data          = data
        self.lang          = lang
        self.current_year  = date.today().year
        self.current_month = date.today().month
        self.selected_date = date.today()
        self._build()
        self._draw_calendar()
        self._show_day(self.selected_date)

    def t(self, k): return LANG[self.lang][k]

    def _build(self):
        left = ctk.CTkFrame(self, fg_color=BG_DARK)
        left.pack(side="left", fill="both", expand=True, padx=(16, 8), pady=16)

        # Nav
        nav = ctk.CTkFrame(left, fg_color=BG_CARD, corner_radius=10)
        nav.pack(fill="x", pady=(0, 10))
        ctk.CTkButton(nav, text="◀", width=36, height=32,
                      fg_color="transparent", hover_color=BG_CARD2,
                      font=ctk.CTkFont("Consolas", 14), text_color=TEXT_PRI,
                      command=self._prev_month).pack(side="left", padx=8, pady=6)
        self.lbl_month = ctk.CTkLabel(nav, text="",
                                       font=ctk.CTkFont("Consolas", 13, "bold"),
                                       text_color=GOLD)
        self.lbl_month.pack(side="left", expand=True)
        ctk.CTkButton(nav, text="▶", width=36, height=32,
                      fg_color="transparent", hover_color=BG_CARD2,
                      font=ctk.CTkFont("Consolas", 14), text_color=TEXT_PRI,
                      command=self._next_month).pack(side="right", padx=8, pady=6)

        # Días semana
        df = ctk.CTkFrame(left, fg_color="transparent")
        df.pack(fill="x", pady=(0, 4))
        for i, d in enumerate(self.t("weekdays")):
            ctk.CTkLabel(df, text=d,
                         font=ctk.CTkFont("Consolas", 9, "bold"),
                         text_color=ACCENT if i < 5 else TEXT_MUT,
                         width=52).pack(side="left", expand=True)

        self.cal_frame = ctk.CTkFrame(left, fg_color="transparent")
        self.cal_frame.pack(fill="both", expand=False)

        # Resumen mes
        ms = ctk.CTkFrame(left, fg_color=BG_CARD, corner_radius=10)
        ms.pack(fill="x", pady=(10, 0))
        ctk.CTkLabel(ms, text=self.t("cal_title"),
                     font=ctk.CTkFont("Consolas", 10, "bold"),
                     text_color=TEXT_PRI).pack(anchor="w", padx=14, pady=(10, 4))
        sr = ctk.CTkFrame(ms, fg_color="transparent")
        sr.pack(fill="x", padx=14, pady=(0, 10))
        sr.columnconfigure(0, weight=1); sr.columnconfigure(1, weight=1); sr.columnconfigure(2, weight=1)
        self.sm_exp  = self._stat_col(sr, "🔮 XP",             "—", 0)
        self.sm_bal  = self._stat_col(sr, "💰 Balance",         "—", 1)
        self.sm_days = self._stat_col(sr, self.t("cal_days"),   "—", 2)

        # Panel derecho
        right = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=14)
        right.pack(side="right", fill="both", padx=(0, 16), pady=16, ipadx=8)
        ctk.CTkLabel(right, text=self.t("day_detail"),
                     font=ctk.CTkFont("Consolas", 12, "bold"),
                     text_color=TEXT_PRI).pack(anchor="w", padx=16, pady=(14, 0))
        self.lbl_sel_date = ctk.CTkLabel(right, text="",
                                          font=ctk.CTkFont("Consolas", 9),
                                          text_color=ACCENT)
        self.lbl_sel_date.pack(anchor="w", padx=16, pady=(2, 10))
        self.day_scroll = ctk.CTkScrollableFrame(right, fg_color="transparent",
                                                  width=240, height=340,
                                                  scrollbar_button_color=ACCENT2)
        self.day_scroll.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        dt = ctk.CTkFrame(right, fg_color=BG_CARD2, corner_radius=8)
        dt.pack(fill="x", padx=12, pady=(0, 12))
        ctk.CTkLabel(dt, text=self.t("day_total"),
                     font=ctk.CTkFont("Consolas", 9, "bold"),
                     text_color=TEXT_MUT2).pack(anchor="w", padx=10, pady=(8, 4))
        tr = ctk.CTkFrame(dt, fg_color="transparent")
        tr.pack(fill="x", padx=10, pady=(0, 8))
        tr.columnconfigure(0, weight=1); tr.columnconfigure(1, weight=1)
        self.day_tot_xp = self._stat_col(tr, "XP",     "—", 0)
        self.day_tot_gp = self._stat_col(tr, "Balance", "—", 1)

    def _stat_col(self, parent, label, value, col):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.grid(row=0, column=col, sticky="ew", padx=2)
        ctk.CTkLabel(f, text=label, font=ctk.CTkFont("Consolas", 8),
                     text_color=TEXT_MUT).pack(anchor="center")
        lbl = ctk.CTkLabel(f, text=value,
                            font=ctk.CTkFont("Consolas", 11, "bold"),
                            text_color=TEXT_PRI)
        lbl.pack(anchor="center")
        return lbl

    def _draw_calendar(self):
        for w in self.cal_frame.winfo_children():
            w.destroy()
        self.lbl_month.configure(
            text=f"{self.t('months')[self.current_month-1]}  {self.current_year}")
        today = date.today()
        for wi, week in enumerate(calendar.monthcalendar(self.current_year, self.current_month)):
            for di, dn in enumerate(week):
                if dn == 0:
                    ctk.CTkFrame(self.cal_frame, width=52, height=44,
                                 fg_color="transparent").grid(row=wi, column=di, padx=2, pady=2)
                    continue
                d     = date(self.current_year, self.current_month, dn)
                key   = d.strftime("%Y-%m-%d")
                has   = key in self.data and self.data[key]
                is_t  = d == today
                is_s  = d == self.selected_date
                is_w  = di >= 5
                bg    = CAL_SEL if is_s else (CAL_TODAY if is_t else (CAL_HAS if has else (CAL_WKND if is_w else BG_CARD)))
                cell  = ctk.CTkFrame(self.cal_frame, width=52, height=44,
                                     fg_color=bg, corner_radius=8,
                                     border_width=2 if is_s else 0,
                                     border_color=ACCENT if is_s else bg)
                cell.grid(row=wi, column=di, padx=2, pady=2)
                cell.grid_propagate(False)
                nc  = ACCENT if is_t else (GOLD if has else TEXT_PRI)
                lbl = ctk.CTkLabel(cell, text=str(dn),
                                   font=ctk.CTkFont("Consolas", 12,
                                                     "bold" if (is_t or is_s) else "normal"),
                                   text_color=nc)
                lbl.place(relx=0.5, rely=0.38, anchor="center")
                if has:
                    ctk.CTkLabel(cell, text=f"{len(self.data[key])}h",
                                 font=ctk.CTkFont("Consolas", 7),
                                 text_color=PROFIT_G).place(relx=0.5, rely=0.78, anchor="center")
                for widget in [cell, lbl]:
                    widget.bind("<Button-1>", lambda e, dd=d: self._on_day_click(dd))
                    widget.configure(cursor="hand2")

        start, end = month_range(date(self.current_year, self.current_month, 1))
        exp, _, _, balance = sum_range(self.data, start, end)
        days_with = sum(1 for k, v in self.data.items()
                        if k.startswith(f"{self.current_year}-{self.current_month:02d}-") and v)
        self.sm_exp.configure(text=f"{exp/1e6:.1f}M" if exp >= 1e6 else f"{exp:,.0f}")
        color = PROFIT_G if balance >= 0 else WASTE_R
        self.sm_bal.configure(
            text=f"{fmt_num(balance/1e3)}k" if abs(balance) >= 1000 else fmt_num(balance),
            text_color=color)
        self.sm_days.configure(text=str(days_with))

    def _on_day_click(self, d):
        self.selected_date = d
        self._draw_calendar()
        self._show_day(d)

    def _show_day(self, d):
        for w in self.day_scroll.winfo_children():
            w.destroy()
        self.lbl_sel_date.configure(
            text=f"{d.day} {self.t('months')[d.month-1]} {d.year}")
        key   = d.strftime("%Y-%m-%d")
        hunts = self.data.get(key, [])
        if not hunts:
            ctk.CTkLabel(self.day_scroll, text=self.t("no_records"),
                         font=ctk.CTkFont("Consolas", 10),
                         text_color=TEXT_MUT).pack(pady=20)
            self.day_tot_xp.configure(text="—", text_color=TEXT_PRI)
            self.day_tot_gp.configure(text="—", text_color=TEXT_PRI)
            return
        total_exp = total_bal = 0.0
        for i, h in enumerate(hunts, 1):
            loot = h.get("loot", 0); sup = h.get("supplies", 0)
            exp  = h.get("experience", 0)
            tc   = h.get("tc_price", 1) or 1
            bal  = loot - sup
            total_exp += exp; total_bal += bal
            color = PROFIT_G if bal >= 0 else WASTE_R
            card  = ctk.CTkFrame(self.day_scroll, fg_color=BG_CARD2, corner_radius=8)
            card.pack(fill="x", pady=3, padx=2)
            ctk.CTkLabel(card, text=f"{self.t('hunt_n')}{i}",
                         font=ctk.CTkFont("Consolas", 10, "bold"),
                         text_color=ACCENT).pack(anchor="w", padx=10, pady=(8, 2))
            for lbl_text, val, col in [
                (self.t("xp_col"),     f"{exp:,.0f}",         GOLD),
                (self.t("loot_row"),   f"{loot:,.0f} gp",     TEXT_PRI),
                (self.t("sup_row"),    f"{sup:,.0f} gp",      TEXT_PRI),
                (self.t("bal_row"),    f"{fmt_num(bal)} gp",  color),
                (self.t("bal_tc_row"), f"{fmt_num(bal/tc, 2)} TC", color),
            ]:
                r = ctk.CTkFrame(card, fg_color="transparent")
                r.pack(fill="x", padx=10, pady=1)
                ctk.CTkLabel(r, text=lbl_text,
                             font=ctk.CTkFont("Consolas", 9),
                             text_color=TEXT_MUT, width=90, anchor="w").pack(side="left")
                ctk.CTkLabel(r, text=val,
                             font=ctk.CTkFont("Consolas", 9, "bold"),
                             text_color=col).pack(side="right")
            ctk.CTkButton(card, text=self.t("btn_delete"),
                          font=ctk.CTkFont("Consolas", 8),
                          fg_color="#3A1520", hover_color="#5A2030",
                          height=24, corner_radius=6,
                          command=lambda idx=i-1, k=key: self._delete_hunt(k, idx)
                          ).pack(anchor="e", padx=10, pady=(4, 8))
        color = PROFIT_G if total_bal >= 0 else WASTE_R
        self.day_tot_xp.configure(text=f"{total_exp:,.0f}", text_color=GOLD)
        self.day_tot_gp.configure(text=f"{fmt_num(total_bal)} gp", text_color=color)

    def _delete_hunt(self, key, idx):
        if messagebox.askyesno("", self.t("del_confirm")):
            self.data[key].pop(idx)
            if not self.data[key]:
                del self.data[key]
            save_json(hunt_file(self._username), self.data)
            self._draw_calendar()
            self._show_day(self.selected_date)

    def set_username(self, u):
        self._username = u

    def _prev_month(self):
        if self.current_month == 1: self.current_month, self.current_year = 12, self.current_year - 1
        else: self.current_month -= 1
        self._draw_calendar()

    def _next_month(self):
        if self.current_month == 12: self.current_month, self.current_year = 1, self.current_year + 1
        else: self.current_month += 1
        self._draw_calendar()

    def refresh(self):
        self._draw_calendar()
        self._show_day(self.selected_date)


# ══════════════════════════════════════════════════════════════════════════════
# VENTANA PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.lang     = "es"
        self.username = None
        self.title("Tibia Hunt Tracker")
        self.configure(fg_color=BG_DARK)
        self.resizable(True, True)
        self.minsize(820, 580)

        # Ícono pixel art en la barra de título
        try:
            icon_img = make_icon()
            icon_img = icon_img.resize((32, 32), Image.NEAREST)
            self._tk_icon = ctk.CTkImage(light_image=icon_img, dark_image=icon_img, size=(32, 32))
            from PIL import ImageTk
            self._raw_icon = ImageTk.PhotoImage(icon_img)
            self.iconphoto(True, self._raw_icon)
        except Exception:
            pass

        self.update_idletasks()
        w, h = 920, 680
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

        self._show_auth()

    def t(self, k): return LANG[self.lang][k]

    def _show_auth(self):
        for widget in self.winfo_children():
            widget.destroy()
        self._auth = AuthScreen(self, self.lang,
                                 on_lang_change=self._change_lang,
                                 on_login=self._on_login)

    def _change_lang(self, code: str):
        self.lang = code
        self._show_auth()   # rebuild auth screen with new lang

    def _on_login(self, username: str):
        self.username = username
        data = load_json(hunt_file(username))
        for widget in self.winfo_children():
            widget.destroy()
        self._build_main(data)

    def _build_main(self, data: dict):
        # Barra superior
        ctk.CTkFrame(self, height=3, fg_color=ACCENT, corner_radius=0).pack(fill="x")

        header = ctk.CTkFrame(self, fg_color=BG_MID, corner_radius=0, height=48)
        header.pack(fill="x")
        header.pack_propagate(False)

        # Ícono pequeño en header
        try:
            small = make_icon().resize((28, 28), Image.NEAREST)
            self._header_icon = ctk.CTkImage(light_image=small, dark_image=small, size=(28, 28))
            ctk.CTkLabel(header, image=self._header_icon, text="").pack(side="left", padx=(10, 4), pady=10)
        except Exception:
            pass

        ctk.CTkLabel(header, text="TIBIA HUNT TRACKER",
                     font=ctk.CTkFont("Consolas", 15, "bold"),
                     text_color=ACCENT).pack(side="left", pady=12)

        ctk.CTkLabel(header, text=f"created by Axels2",
                     font=ctk.CTkFont("Consolas", 8),
                     text_color=TEXT_MUT).pack(side="left", padx=(8, 0), pady=14)

        # Lado derecho del header
        right_bar = ctk.CTkFrame(header, fg_color="transparent")
        right_bar.pack(side="right", padx=12)

        # Selector de idioma
        for code, label in [("es", "🇪🇸"), ("en", "🇬🇧")]:
            col = ACCENT2 if self.lang == code else "transparent"
            ctk.CTkButton(right_bar, text=label, width=32, height=26,
                          fg_color=col, hover_color=ACCENT2,
                          font=ctk.CTkFont(size=14), corner_radius=6,
                          command=lambda c=code: self._switch_lang(c)
                          ).pack(side="left", padx=2)

        # Usuario + logout
        ctk.CTkLabel(right_bar, text=f"  👤 {self.username}",
                     font=ctk.CTkFont("Consolas", 10),
                     text_color=TEXT_MUT2).pack(side="left", padx=(8, 4))
        ctk.CTkButton(right_bar, text=self.t("logout"),
                      font=ctk.CTkFont("Consolas", 9),
                      fg_color="#3A1520", hover_color="#5A2030",
                      height=26, width=90, corner_radius=6,
                      command=self._logout).pack(side="left", padx=4)

        # Tabs
        self._tabview = ctk.CTkTabview(self, fg_color=BG_DARK,
                                        segmented_button_fg_color=BG_MID,
                                        segmented_button_selected_color=ACCENT2,
                                        segmented_button_selected_hover_color=ACCENT,
                                        segmented_button_unselected_color=BG_MID,
                                        segmented_button_unselected_hover_color=BG_CARD,
                                        text_color=TEXT_PRI,
                                        text_color_disabled=TEXT_MUT)
        self._tabview.pack(fill="both", expand=True)

        tab_h = self.t("tab_hunts")
        tab_c = self.t("tab_calendar")
        self._tabview.add(tab_h)
        self._tabview.add(tab_c)

        self._tab_hunts = TabHunts(self._tabview.tab(tab_h), data, self.lang,
                                    on_save=self._on_save)
        self._tab_hunts.set_username(self.username)
        self._tab_hunts.pack(fill="both", expand=True)

        self._tab_cal = TabCalendar(self._tabview.tab(tab_c), data, self.lang)
        self._tab_cal.set_username(self.username)
        self._tab_cal.pack(fill="both", expand=True)

    def _on_save(self):
        self._tab_cal.refresh()

    def _switch_lang(self, code: str):
        if code == self.lang:
            return
        self.lang = code
        # Recargar la app principal con el nuevo idioma
        data = load_json(hunt_file(self.username))
        for w in self.winfo_children():
            w.destroy()
        self._build_main(data)

    def _logout(self):
        self.username = None
        self._show_auth()


# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = App()
    app.mainloop()
