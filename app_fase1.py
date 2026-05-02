# ============================================================
#  FLOWVENT — Versión 5.2
#  + Mensajes en vivo (INFO / ALERTA / GANADOR)
# ============================================================

import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Flowvent | Live", page_icon="⚡", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<meta name="google" content="notranslate">
<meta http-equiv="Content-Language" content="es">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;900&family=Inter:wght@400;500;600&display=swap');
  html, body, [data-testid="stAppViewContainer"] { background:#07070F; font-family:'Inter',sans-serif; color:#fff; }
  [data-testid="stHeader"] { display:none; }
  [data-testid="block-container"] { padding:0 1.2rem 4rem; max-width:1600px; margin:0 auto; }
  section[data-testid="stSidebar"] { display:none; }
  [data-testid="stMetric"] { background:#11111C; border:0.5px solid #1E1E35; border-radius:10px; padding:14px 18px; }
  [data-testid="stMetricLabel"] { font-size:0.7rem !important; letter-spacing:.1em; text-transform:uppercase; color:#555 !important; }
  [data-testid="stMetricValue"] { font-family:'Barlow Condensed',sans-serif !important; font-size:2.2rem !important; font-weight:700 !important; color:#fff !important; }
  div.stButton > button { background:#00E676 !important; color:#000 !important; font-weight:700 !important; border:none !important; border-radius:8px !important; padding:8px 20px !important; font-size:.8rem !important; letter-spacing:.06em !important; text-transform:uppercase !important; }
  div.stButton > button:hover { background:#00c95e !important; }
  .fv-header { display:flex; align-items:center; justify-content:space-between; padding:1.4rem 0 1.2rem; border-bottom:1px solid #1a1a2e; margin-bottom:1.4rem; }
  .fv-logo-flow { font-family:'Barlow Condensed',sans-serif; font-size:2.6rem; font-weight:900; color:#FFF; text-transform:uppercase; line-height:1; }
  .fv-logo-vent { font-family:'Barlow Condensed',sans-serif; font-size:2.6rem; font-weight:900; color:#00E676; text-transform:uppercase; line-height:1; }
  .fv-logo-dot  { width:8px; height:8px; background:#00E676; border-radius:50%; margin-left:5px; margin-bottom:5px; display:inline-block; animation:pulse 1.4s ease-in-out infinite; }
  .fv-tagline   { font-size:0.68rem; font-weight:500; letter-spacing:.15em; text-transform:uppercase; color:#444; margin-top:2px; }
  .fv-live-badge { display:flex; align-items:center; gap:8px; background:rgba(0,230,118,.08); border:1px solid rgba(0,230,118,.2); border-radius:20px; padding:6px 16px; font-size:0.72rem; font-weight:700; letter-spacing:.12em; text-transform:uppercase; color:#00E676; }
  .fv-live-dot  { width:7px; height:7px; background:#00E676; border-radius:50%; animation:pulse 1.4s ease-in-out infinite; }
  @keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.35;transform:scale(1.4)} }
  @keyframes fadeInUp { from{opacity:0;transform:translateY(12px)} to{opacity:1;transform:translateY(0)} }
  .ev-card { background:#0E0E1A; border:1px solid #1E1E35; border-top:4px solid #00E676; border-radius:20px; padding:48px 40px; margin-bottom:4px; animation:fadeInUp .3s ease both; transition:transform .18s ease, box-shadow .18s ease; }
  .ev-card:hover { transform:translateY(-4px); box-shadow:0 16px 48px rgba(0,230,118,.15); }
  .ev-nombre { font-family:'Barlow Condensed',sans-serif; font-size:3.2rem; font-weight:900; color:#FFF; text-transform:uppercase; margin:0 0 14px; letter-spacing:.03em; line-height:1.1; }
  .ev-desc { font-size:1.1rem; color:#666; margin:0 0 20px; line-height:1.6; }
  .ev-meta { display:flex; gap:18px; flex-wrap:wrap; margin-bottom:6px; }
  .ev-meta-item { font-size:.95rem; color:#555; }
  .ev-badge { display:inline-block; font-size:.82rem; font-weight:700; letter-spacing:.1em; text-transform:uppercase; padding:7px 18px; border-radius:20px; background:rgba(0,230,118,.15); color:#00E676; border:1px solid rgba(0,230,118,.3); }
  .ev-event-name { font-family:'Barlow Condensed',sans-serif; font-size:1.1rem; font-weight:700; color:#00E676; text-transform:uppercase; letter-spacing:.06em; }
  .cat-chip { display:inline-block; font-size:.62rem; font-weight:700; letter-spacing:.1em; text-transform:uppercase; padding:3px 10px; border-radius:20px; }
  .cat-RX      { background:rgba(0,230,118,.15); color:#00E676; border:1px solid rgba(0,230,118,.3); }
  .cat-SCALED  { background:rgba(122,143,255,.15); color:#7a8fff; border:1px solid rgba(122,143,255,.3); }
  .cat-MASTERS { background:rgba(255,179,0,.15); color:#FFB300; border:1px solid rgba(255,179,0,.3); }
  .cat-DUPLAS-MASCULINAS { background:rgba(55,138,221,.15); color:#378ADD; border:1px solid rgba(55,138,221,.3); }
  .cat-DUPLAS-FEMENINAS  { background:rgba(212,83,126,.15); color:#D4537E; border:1px solid rgba(212,83,126,.3); }
  .cat-DUPLAS-MIXTAS     { background:rgba(127,119,221,.15); color:#7F77DD; border:1px solid rgba(127,119,221,.3); }
  .cat-DEFAULT { background:rgba(255,255,255,.08); color:#888; border:1px solid #333; }
  .fv-section { display:flex; align-items:center; gap:12px; margin:0 0 1rem; padding-bottom:.5rem; }
  .fv-section-line { flex:1; height:1px; }
  .fv-section-text { font-family:'Barlow Condensed',sans-serif; font-size:1rem; font-weight:700; letter-spacing:.2em; text-transform:uppercase; white-space:nowrap; }
  .sec-live .fv-section-text{color:#00E676} .sec-live .fv-section-line{background:linear-gradient(90deg,#00E676,transparent)}
  .sec-next .fv-section-text{color:#FFB300} .sec-next .fv-section-line{background:linear-gradient(90deg,#FFB300,transparent)}
  .sec-done .fv-section-text{color:#555}    .sec-done .fv-section-line{background:linear-gradient(90deg,#333,transparent)}
  .fv-card { background:#0E0E1A; border-radius:14px; overflow:hidden; border:1px solid #1E1E35; transition:transform .18s ease; animation:fadeInUp .35s ease both; margin-bottom:4px; }
  .fv-card:hover { transform:translateY(-3px); box-shadow:0 12px 40px rgba(0,0,0,.6); }
  .card-live { border-top:3px solid #00E676; box-shadow:0 0 28px rgba(0,230,118,.1); }
  .card-next { border-top:3px solid #FFB300; }
  .card-done { border-top:3px solid #2a2a3a; opacity:.6; }
  .fv-card-header { display:flex; justify-content:space-between; align-items:flex-start; padding:14px 16px 10px; border-bottom:1px solid #1E1E35; }
  .fv-card-header-left { display:flex; flex-direction:column; gap:5px; }
  .fv-equipo { font-family:'Barlow Condensed',sans-serif; font-size:1.5rem; font-weight:800; color:#FFF; text-transform:uppercase; letter-spacing:.04em; line-height:1; }
  .fv-badge { font-size:.62rem; font-weight:700; letter-spacing:.12em; text-transform:uppercase; padding:5px 11px; border-radius:20px; flex-shrink:0; margin-left:8px; }
  .badge-live{background:rgba(0,230,118,.15);color:#00E676;border:1px solid rgba(0,230,118,.3)}
  .badge-next{background:rgba(255,179,0,.15);color:#FFB300;border:1px solid rgba(255,179,0,.3)}
  .badge-done{background:rgba(80,80,100,.2);color:#666;border:1px solid #2a2a3a}
  .fv-card-body { padding:12px 16px 16px; }
  .fv-field { display:flex; justify-content:space-between; align-items:baseline; padding:5px 0; border-bottom:1px solid #13131F; }
  .fv-field:last-child { border-bottom:none; }
  .fv-label { font-size:.68rem; font-weight:600; letter-spacing:.1em; text-transform:uppercase; color:#444; }
  .fv-value { font-size:.88rem; font-weight:500; color:#BBB; text-align:right; }
  .fv-value.wod { font-family:'Barlow Condensed',sans-serif; font-size:1.1rem; font-weight:700; color:#FFF; }
  .fv-value.res-live { color:#00E676; font-weight:700; }
  .fv-value.res-done { color:#888; }
  .fv-value.arena-val { font-size:.75rem; padding:2px 9px; border-radius:5px; background:#1a1a2e; color:#7a8fff; font-weight:600; }
  .fv-empty { text-align:center; padding:2.5rem; color:#333; font-size:.82rem; border:1px dashed #1a1a2e; border-radius:12px; }
  .sb-wrap { overflow-x:auto; -webkit-overflow-scrolling:touch; }
  .sb-table { width:100%; border-collapse:separate; border-spacing:0; font-size:.82rem; }
  .sb-table th { background:#0E0E1A; color:#555; font-size:.65rem; font-weight:600; letter-spacing:.12em; text-transform:uppercase; padding:10px 14px; border-bottom:1px solid #1E1E35; text-align:center; }
  .sb-table th.hora-col { text-align:left; color:#444; min-width:100px; }
  .sb-table th.arena-col { min-width:160px; color:#7a8fff; }
  .sb-table td { padding:8px 10px; border-bottom:1px solid #0f0f1a; vertical-align:top; }
  .sb-table td.hora-td { color:#FFFFFF; font-size:1rem; font-weight:700; white-space:nowrap; padding-top:12px; }
  .sb-fecha { font-size:1.4rem; color:#FFFFFF; font-weight:800; display:block; letter-spacing:.03em; }
  .sb-hora  { display:none; }
  .sb-cell { background:#11111C; border-radius:8px; padding:8px 10px; border:1px solid #1E1E35; margin-bottom:6px; }
  .sb-cell.st-live { border-left:3px solid #00E676; background:rgba(0,230,118,.05); }
  .sb-cell.st-next { border-left:3px solid #FFB300; }
  .sb-cell.st-done { border-left:3px solid #2a2a3a; opacity:.6; }
  .sb-team { font-family:'Barlow Condensed',sans-serif; font-size:1rem; font-weight:700; color:#FFF; text-transform:uppercase; }
  .sb-wod  { font-size:.7rem; color:#666; margin-top:3px; }
  .sb-heat { font-size:.65rem; color:#444; margin-top:2px; }
  .sb-estado { display:inline-block; font-size:.58rem; font-weight:700; letter-spacing:.1em; text-transform:uppercase; padding:2px 7px; border-radius:10px; margin-top:4px; }
  .sb-estado.st-live{background:rgba(0,230,118,.15);color:#00E676}
  .sb-estado.st-next{background:rgba(255,179,0,.15);color:#FFB300}
  .sb-estado.st-done{background:rgba(80,80,100,.15);color:#555}
  .sb-empty-cell { color:#2a2a3a; font-size:.7rem; text-align:center; padding:10px 0; }
  .rk-table { width:100%; border-collapse:separate; border-spacing:0 6px; }
  .rk-table th { font-size:.65rem; font-weight:600; letter-spacing:.1em; text-transform:uppercase; color:#444; padding:6px 12px; text-align:left; }
  .rk-row { background:#0E0E1A; }
  .rk-row td { padding:12px 14px; border-top:1px solid #1E1E35; border-bottom:1px solid #1E1E35; }
  .rk-row td:first-child { border-left:1px solid #1E1E35; border-radius:10px 0 0 10px; }
  .rk-row td:last-child  { border-right:1px solid #1E1E35; border-radius:0 10px 10px 0; }
  .rk-pos { font-family:'Barlow Condensed',sans-serif; font-size:1.8rem; font-weight:900; color:#333; width:48px; }
  .rk-pos.p1{color:#FFD700} .rk-pos.p2{color:#C0C0C0} .rk-pos.p3{color:#CD7F32}
  .rk-team { font-family:'Barlow Condensed',sans-serif; font-size:1.2rem; font-weight:700; color:#FFF; text-transform:uppercase; }
  .rk-pts  { font-family:'Barlow Condensed',sans-serif; font-size:1.5rem; font-weight:900; color:#00E676; text-align:right; }
  .rk-pts-label { font-size:.65rem; color:#444; text-align:right; letter-spacing:.08em; text-transform:uppercase; }
  .grp-arena { margin-bottom:2rem; }
  .grp-arena-title { font-family:'Barlow Condensed',sans-serif; font-size:1.3rem; font-weight:800; color:#7a8fff; text-transform:uppercase; letter-spacing:.1em; padding:8px 0 6px; border-bottom:1px solid #1a1a2e; margin-bottom:1rem; }
  .grp-heat { background:#0E0E1A; border-radius:12px; border:1px solid #1E1E35; margin-bottom:12px; overflow:hidden; }
  .grp-heat-header { display:flex; align-items:center; gap:14px; padding:10px 16px; background:#111120; border-bottom:1px solid #1E1E35; }
  .grp-heat-num { font-family:'Barlow Condensed',sans-serif; font-size:1rem; font-weight:800; color:#FFF; text-transform:uppercase; letter-spacing:.06em; }
  .grp-wod-name { font-family:'Barlow Condensed',sans-serif; font-size:.95rem; font-weight:600; color:#00E676; }
  .grp-hora-tag { font-size:.7rem; color:#555; margin-left:auto; }
  .grp-estado-badge { font-size:.6rem; font-weight:700; letter-spacing:.1em; text-transform:uppercase; padding:3px 9px; border-radius:12px; }
  .grp-estado-badge.live { background:rgba(0,230,118,.15); color:#00E676; border:1px solid rgba(0,230,118,.3); }
  .grp-estado-badge.next { background:rgba(255,179,0,.15); color:#FFB300; border:1px solid rgba(255,179,0,.3); }
  .grp-estado-badge.done { background:rgba(80,80,100,.2); color:#666; border:1px solid #2a2a3a; }
  .grp-atleta-list { padding:8px 16px 12px; display:flex; flex-direction:column; gap:5px; }
  .grp-atleta-row { display:flex; align-items:center; justify-content:space-between; padding:6px 10px; border-radius:7px; background:#13131F; }
  .grp-atleta-name { font-size:.85rem; font-weight:500; color:#CCC; }
  .grp-atleta-cat { font-size:.6rem; }
  .grp-atleta-res { font-size:.82rem; font-weight:600; color:#00E676; }
  .fv-footer { text-align:center; padding:2rem 0 0; font-size:.65rem; color:#2a2a3a; letter-spacing:.08em; text-transform:uppercase; }
</style>
""", unsafe_allow_html=True)

st_autorefresh(interval=20_000, key="fv_refresh")

SCOPES = ["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"]

def get_client():
    s = st.secrets["connections"]["gsheets"]
    d = {
        "type":"service_account","project_id":s["project_id"],
        "private_key_id":s["private_key_id"],"private_key":s["private_key"].replace("\\n","\n"),
        "client_email":s["client_email"],"client_id":s["client_id"],
        "auth_uri":s["auth_uri"],"token_uri":s["token_uri"],
        "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url":f"https://www.googleapis.com/robot/v1/metadata/x509/{s['client_email'].replace('@','%40')}",
    }
    creds = Credentials.from_service_account_info(d, scopes=SCOPES)
    return gspread.authorize(creds), s["spreadsheet"]

@st.cache_data(ttl=20)
def load_eventos():
    client, url = get_client()
    sh = client.open_by_url(url)
    ws = sh.worksheet("eventos")
    data = ws.get_all_records()
    if not data: return pd.DataFrame()
    df = pd.DataFrame(data)
    for c in ["evento_id","nombre","descripcion","fecha","lugar","activo"]:
        if c not in df.columns: df[c] = ""
    df["activo"] = df["activo"].astype(str).str.strip().str.upper()
    return df[df["activo"]=="SI"].reset_index(drop=True)

@st.cache_data(ttl=20)
def load_data(evento_nombre: str):
    client, url = get_client()
    sh = client.open_by_url(url)
    ws = sh.worksheet("events")
    data = ws.get_all_records()
    if not data: return pd.DataFrame()
    df = pd.DataFrame(data)
    cols = ["event_id","event_name","equipo","categoria","heat","wod_nombre","arena","estado","fecha","hora_inicio","resultado","puntos","tipo_puntaje","orden_display","activo"]
    for c in cols:
        if c not in df.columns: df[c] = ""
    df = df.dropna(subset=["event_id","equipo","estado"])
    df["estado"]    = df["estado"].astype(str).str.strip().str.upper()
    df["categoria"] = df["categoria"].astype(str).str.strip().str.upper()
    df["activo"]    = df["activo"].astype(str).str.strip().str.upper()
    df = df[df["activo"]=="SI"]
    df = df[df["event_name"].astype(str).str.strip().str.upper() == evento_nombre.strip().upper()]
    df = df[df["estado"].isin({"EN_CURSO","FINALIZADO","PROXIMO"})]
    orden_estado = {"EN_CURSO":0,"PROXIMO":1,"FINALIZADO":2}
    df["_orden_estado"] = df["estado"].map(orden_estado)
    df["orden_display"] = pd.to_numeric(df["orden_display"], errors="coerce").fillna(999)
    df["puntos"] = pd.to_numeric(df["puntos"], errors="coerce").fillna(0)
    df = df.sort_values(["_orden_estado","orden_display","hora_inicio"]).reset_index(drop=True)
    return df

@st.cache_data(ttl=15)
def load_mensajes():
    try:
        client, url = get_client()
        sh = client.open_by_url(url)
        ws = sh.worksheet("mensajes")
        data = ws.get_all_records()
        if not data: return pd.DataFrame()
        df = pd.DataFrame(data)
        for c in ["mensaje_id","texto","tipo","activo","duracion_min"]:
            if c not in df.columns: df[c] = ""
        df["activo"] = df["activo"].astype(str).str.strip().str.upper()
        df["tipo"]   = df["tipo"].astype(str).str.strip().str.upper()
        return df[df["activo"]=="SI"].reset_index(drop=True)
    except:
        return pd.DataFrame()

def parse_hora(val):
    try:
        f = float(val); mins = round(f*24*60)
        return f"{mins//60:02d}:{mins%60:02d}"
    except:
        return str(val).strip()

def tiempo_a_segundos(t):
    try:
        t = str(t).strip()
        ms = 0
        if "." in t:
            t, ms_str = t.split(".", 1)
            ms = int(ms_str.ljust(3,"0")[:3])
        p = [int(x) for x in t.split(":")]
        if len(p)==2:  return (p[0]*60 + p[1]) * 1000 + ms
        if len(p)==3:  return (p[0]*3600 + p[1]*60 + p[2]) * 1000 + ms
    except:
        pass
    return 999999999

def segundos_a_str(ms):
    ms = int(ms)
    mins   = ms // 60000
    secs   = (ms % 60000) // 1000
    millis = ms % 1000
    return f"{mins}:{secs:02d}.{millis:03d}"

def cat_chip(cat):
    cat = str(cat).strip().upper()
    key = cat.replace(" ","-")
    cls = {"RX":"cat-RX","SCALED":"cat-SCALED","MASTERS":"cat-MASTERS",
           "DUPLAS-MASCULINAS":"cat-DUPLAS-MASCULINAS",
           "DUPLAS-FEMENINAS":"cat-DUPLAS-FEMENINAS",
           "DUPLAS-MIXTAS":"cat-DUPLAS-MIXTAS"}.get(key,"cat-DEFAULT")
    return f'<span class="cat-chip {cls}">{cat or "—"}</span>'

def render_mensajes():
    df_msg = load_mensajes()
    if df_msg.empty: return
    color_map = {
        "INFO":    ("rgba(0,230,118,.12)",  "#00E676", "rgba(0,230,118,.3)",  "ℹ️"),
        "ALERTA":  ("rgba(255,179,0,.12)",  "#FFB300", "rgba(255,179,0,.3)",  "⚠️"),
        "GANADOR": ("rgba(255,215,0,.12)",  "#FFD700", "rgba(255,215,0,.3)",  "🏆"),
    }
    for _, msg in df_msg.iterrows():
        tipo  = str(msg.get("tipo","INFO")).strip().upper()
        texto = str(msg.get("texto","")).strip()
        bg, color, border, icon = color_map.get(tipo, color_map["INFO"])
        st.markdown(
            f'<div style="background:{bg};border:1px solid {border};border-left:4px solid {color};'
            f'border-radius:10px;padding:14px 20px;margin-bottom:12px;'
            f'display:flex;align-items:center;gap:12px;animation:fadeInUp .3s ease both">'
            f'<span style="font-size:1.2rem">{icon}</span>'
            f'<span style="font-family:\'Barlow Condensed\',sans-serif;font-size:1.15rem;'
            f'font-weight:700;color:{color};text-transform:uppercase;letter-spacing:.04em">{texto}</span>'
            f'</div>',
            unsafe_allow_html=True
        )

def render_envivo(df):
    """Vista agrupada: Arena > Heat > WOD > lista de atletas"""
    if df.empty:
        st.markdown('<div class="fv-empty">Sin actividad en este momento</div>', unsafe_allow_html=True)
        return

    estado_badge = {
        "EN_CURSO": ('live','⚡ En Curso'),
        "PROXIMO":  ('next','◷ Próximo'),
        "FINALIZADO":('done','✓ Finalizado'),
    }

    arenas = sorted(df["arena"].dropna().unique().tolist())
    for arena in arenas:
        df_arena = df[df["arena"]==arena]
        html = f'<div class="grp-arena"><div class="grp-arena-title">🏟️ {arena}</div>'

        # Agrupar por heat + wod
        grupos = df_arena.groupby(["heat","wod_nombre","estado","hora_inicio"], sort=False)
        heats_vistos = {}
        for (heat, wod, estado, hora), grp in df_arena.groupby(["heat","wod_nombre","estado","hora_inicio"]):
            key = (heat, wod)
            if key in heats_vistos: continue
            heats_vistos[key] = True

            bc, bt = estado_badge.get(estado, ('next',estado))
            hora_str = parse_hora(hora)
            try: heat_n = int(float(str(heat)))
            except: heat_n = heat

            html += (f'<div class="grp-heat">'
                     f'<div class="grp-heat-header">'
                     f'<span class="grp-heat-num">Heat #{heat_n}</span>'
                     f'<span class="grp-wod-name">{wod}</span>'
                     f'<span class="grp-estado-badge {bc}">{bt}</span>'
                     f'<span class="grp-hora-tag">⏱ {hora_str}</span>'
                     f'</div><div class="grp-atleta-list">')

            for _,r in grp.iterrows():
                res = str(r.get("resultado","")).strip()
                res_html = f'<span class="grp-atleta-res">{res}</span>' if res else ""
                html += (f'<div class="grp-atleta-row">'
                         f'<span class="grp-atleta-name">{r["equipo"]}</span>'
                         f'<span class="grp-atleta-cat">{cat_chip(r.get("categoria",""))}</span>'
                         f'{res_html}</div>')
            html += '</div></div>'
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)

def render_schedule(df):
    arenas = sorted(df["arena"].dropna().unique().tolist())
    if "fecha" in df.columns:
        df = df.copy()
        df["_fh"] = df["fecha"].astype(str).str.strip() + "||" + df["hora_inicio"].astype(str).str.strip()
    else:
        df = df.copy()
        df["_fh"] = "||" + df["hora_inicio"].astype(str).str.strip()
    claves = sorted(df["_fh"].dropna().unique().tolist(),
                    key=lambda x: (x.split("||")[0], parse_hora(x.split("||")[1])))
    if not arenas or not claves:
        st.warning("Sin datos para el programa."); return
    th = "".join(f'<th class="arena-col">🏟️ {a}</th>' for a in arenas)
    html = f'<div class="sb-wrap"><table class="sb-table"><thead><tr><th class="hora-col">📅 Fecha / ⏱ Hora</th>{th}</tr></thead><tbody>'
    em = {"EN_CURSO":"st-live","FINALIZADO":"st-done","PROXIMO":"st-next"}
    et = {"EN_CURSO":"⚡ En Curso","FINALIZADO":"✓ Listo","PROXIMO":"◷ Próximo"}
    for clave in claves:
        fecha_disp, hora_raw = clave.split("||")
        hora_disp = parse_hora(hora_raw)
        html += (f'<tr><td class="hora-td">'
                 f'<span class="sb-fecha">{fecha_disp}</span>'
                 f'<span class="sb-hora">{hora_disp}</span>'
                 f'</td>')
        for a in arenas:
            rows = df[(df["_fh"]==clave)&(df["arena"]==a)]
            if rows.empty:
                html += '<td><div class="sb-empty-cell">—</div></td>'
            else:
                cells = ""
                for _,r in rows.iterrows():
                    sc = em.get(r["estado"],"st-next"); st2 = et.get(r["estado"],r["estado"])
                    try: hn = int(float(str(r.get("heat",""))))
                    except: hn = r.get("heat","")
                    cells += (f'<div class="sb-cell {sc}"><div class="sb-team">{r["equipo"]}</div>'
                              f'<div class="sb-wod">{r["wod_nombre"]}</div>'
                              f'<div class="sb-heat">Heat #{hn}</div>'
                              f'<div style="margin-top:4px">{cat_chip(r.get("categoria",""))}</div>'
                              f'<span class="sb-estado {sc}">{st2}</span></div>')
                html += f'<td>{cells}</td>'
        html += '</tr>'
    html += '</tbody></table></div>'
    st.markdown(html, unsafe_allow_html=True)

def render_ranking(df):
    df_fin = df[df["estado"]=="FINALIZADO"].copy()
    if df_fin.empty:
        st.markdown('<div class="fv-empty">El ranking aparece cuando finalicen los primeros heats.</div>', unsafe_allow_html=True)
        return
    tipo = df_fin["tipo_puntaje"].astype(str).str.strip().str.upper().mode()
    es_tiempo = len(tipo)>0 and tipo[0]=="TIEMPO"
    pc = {0:"p1",1:"p2",2:"p3"}; pi = {0:"🥇",1:"🥈",2:"🥉"}
    if es_tiempo:
        df_fin["_seg"] = df_fin["resultado"].apply(tiempo_a_segundos)
        rk = df_fin[df_fin["_seg"]<999999999].groupby(["equipo","categoria"])["_seg"].min().reset_index()
        rk = rk.sort_values("_seg").reset_index(drop=True)
        html = '<table class="rk-table"><thead><tr><th>Pos</th><th>Equipo</th><th>Categoría</th><th style="text-align:right">Tiempo</th></tr></thead><tbody>'
        for i,r in rk.iterrows():
            html += (f'<tr class="rk-row"><td><span class="rk-pos {pc.get(i,"")}">{pi.get(i,str(i+1))}</span></td>'
                     f'<td><span class="rk-team">{r["equipo"]}</span></td>'
                     f'<td>{cat_chip(r["categoria"])}</td>'
                     f'<td><div class="rk-pts">{segundos_a_str(r["_seg"])}</div><div class="rk-pts-label">tiempo</div></td></tr>')
    else:
        rk = df_fin.groupby(["equipo","categoria"])["puntos"].sum().reset_index()
        rk = rk.sort_values("puntos", ascending=False).reset_index(drop=True)
        html = '<table class="rk-table"><thead><tr><th>Pos</th><th>Equipo</th><th>Categoría</th><th style="text-align:right">Puntos</th></tr></thead><tbody>'
        for i,r in rk.iterrows():
            html += (f'<tr class="rk-row"><td><span class="rk-pos {pc.get(i,"")}">{pi.get(i,str(i+1))}</span></td>'
                     f'<td><span class="rk-team">{r["equipo"]}</span></td>'
                     f'<td>{cat_chip(r["categoria"])}</td>'
                     f'<td><div class="rk-pts">{int(r["puntos"])}</div><div class="rk-pts-label">pts</div></td></tr>')
    html += '</tbody></table>'
    st.markdown(html, unsafe_allow_html=True)

def render_header():
    st.markdown(
        '<div class="fv-header">'
        '<div><div style="display:flex;align-items:baseline;gap:2px">'
        '<span class="fv-logo-flow">Flow</span><span class="fv-logo-vent">vent</span><span class="fv-logo-dot"></span>'
        '</div><div class="fv-tagline">Plataforma de eventos en tiempo real</div></div>'
        '<div class="fv-live-badge"><div class="fv-live-dot"></div>EN VIVO</div>'
        '</div>', unsafe_allow_html=True)

def main():
    render_header()
    params = st.query_params
    evento_sel = params.get("evento", None)

    if not evento_sel:
        try: df_eventos = load_eventos()
        except Exception as e:
            st.error(f"Error cargando eventos: {e}"); return
        if df_eventos.empty:
            st.warning("No hay eventos activos en la hoja 'eventos'."); return
        if len(df_eventos)==1:
            st.query_params["evento"] = df_eventos.iloc[0]["nombre"]
            st.rerun()
        st.markdown('<div class="fv-section sec-live"><span class="fv-section-text" style="font-size:1.3rem">Eventos activos</span><div class="fv-section-line"></div></div>', unsafe_allow_html=True)
        cols = st.columns(min(len(df_eventos),2))
        for i,(_,ev) in enumerate(df_eventos.iterrows()):
            nombre = str(ev.get("nombre","")).strip()
            desc   = str(ev.get("descripcion","")).strip()
            fecha  = str(ev.get("fecha","")).strip()
            lugar  = str(ev.get("lugar","")).strip()
            with cols[i%3]:
                st.markdown(
                    f'<div class="ev-card">'
                    f'<p class="ev-nombre">{nombre}</p>'
                    f'<p class="ev-desc">{desc}</p>'
                    f'<div class="ev-meta"><span class="ev-meta-item">📅 {fecha}</span>&nbsp;&nbsp;<span class="ev-meta-item">📍 {lugar}</span></div>'
                    f'<div style="margin-top:12px"><span class="ev-badge">⚡ En vivo</span></div>'
                    f'</div>', unsafe_allow_html=True)
                if st.button("Ingresar →", key=f"ev_{i}", use_container_width=True):
                    st.query_params["evento"] = nombre
                    st.rerun()
        return

    if st.button("← Volver a eventos"):
        st.query_params.clear(); st.rerun()

    try: df = load_data(evento_sel)
    except Exception as e:
        st.error(f"Error cargando datos: {e}"); return

    if df.empty:
        st.warning(f"Sin datos activos para '{evento_sel}'."); return

    st.markdown(f'<div style="margin-bottom:1rem"><span class="ev-event-name">⚡ {evento_sel}</span></div>', unsafe_allow_html=True)

    render_mensajes()

    vista = st.radio("Vista", ["⚡  En Vivo","📋  Programa","🏆  Ranking"], horizontal=True, label_visibility="collapsed")
    st.markdown("<br>", unsafe_allow_html=True)

    categorias = sorted([c for c in df["categoria"].dropna().unique() if c and c not in ("NAN","")])
    cat_opts   = ["Todas las categorías"] + categorias
    arena_opts = ["Todas las arenas"] + sorted(df["arena"].dropna().unique().tolist())

    if vista=="⚡  En Vivo":
        fc,fa = st.columns(2)
        cat_sel   = fc.selectbox("Categoría", cat_opts,  label_visibility="collapsed")
        arena_sel = fa.selectbox("Arena",     arena_opts, label_visibility="collapsed")
        dv = df.copy()
        if cat_sel!="Todas las categorías": dv = dv[dv["categoria"]==cat_sel]
        if arena_sel!="Todas las arenas":   dv = dv[dv["arena"]==arena_sel]
        # En Curso primero
        dl = dv[dv["estado"]=="EN_CURSO"]
        dn = dv[dv["estado"]=="PROXIMO"]
        if not dl.empty:
            st.markdown('<div class="fv-section sec-live"><span class="fv-section-text">⚡ En Curso</span><div class="fv-section-line"></div></div>', unsafe_allow_html=True)
            render_envivo(dl)
        if not dn.empty:
            st.markdown('<div class="fv-section sec-next"><span class="fv-section-text">◷ Próximamente</span><div class="fv-section-line"></div></div>', unsafe_allow_html=True)
            render_envivo(dn)
        if dl.empty and dn.empty:
            st.markdown('<div class="fv-empty">Sin actividad activa en este momento</div>', unsafe_allow_html=True)
    elif vista=="📋  Programa":
        cat_sel = st.selectbox("Categoría", cat_opts, label_visibility="collapsed")
        dv = df if cat_sel=="Todas las categorías" else df[df["categoria"]==cat_sel]
        st.markdown('<div class="fv-section sec-live"><span class="fv-section-text">📋 Programa del Evento</span><div class="fv-section-line"></div></div>', unsafe_allow_html=True)
        render_schedule(dv)
    else:
        cat_sel = st.selectbox("Categoría", cat_opts, label_visibility="collapsed")
        dv = df if cat_sel=="Todas las categorías" else df[df["categoria"]==cat_sel]
        st.markdown('<div class="fv-section sec-live"><span class="fv-section-text">🏆 Ranking Acumulado</span><div class="fv-section-line"></div></div>', unsafe_allow_html=True)
        render_ranking(dv)

    st.markdown('<div class="fv-footer">Flowvent · Actualizando cada 20s · F11 para pantalla completa</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
