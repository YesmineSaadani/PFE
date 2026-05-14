"""
╔══════════════════════════════════════════════════════════════════════╗
║   STRESS TESTING STB — APPLICATION INTERACTIVE COMPLÈTE             ║
║   Mémoire de Master — Architecture Wilson (1997) / Bâle II          ║
║                                                                      ║
║   Version finale — données STB 2006-2024 corrigées                  ║
║   Modèle satellite : logit_NPL AR(1) + PIB + Chôm_lag + COVID       ║
║   Probit Stage 2   : AUC=0.9427 · Gini=0.8855 · N=327,571          ║
║                                                                      ║
║   Run: streamlit run stress_testing_app.py                          ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from scipy.special import ndtr
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ═══════════════════════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ═══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Stress Testing STB",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ═══════════════════════════════════════════════════════════════════════════════
#  CSS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');
:root {
    --blue:#3B82F6;--blue-dim:#1D3461;--green:#22D3A3;--green-dim:#0D2B22;
    --amber:#FBBF24;--amber-dim:#2D2008;--red:#F87171;--red-dim:#2D0E0E;
    --bg:#080E1A;--surface:#0F1929;--surface2:#162236;--border:#1E3050;
    --text:#E2E8F0;--muted:#64748B;
    --mono:'IBM Plex Mono',monospace;--head:'Syne',sans-serif;--body:'DM Sans',sans-serif;
}
html,body,.stApp{background:var(--bg)!important;color:var(--text)!important;font-family:var(--body)!important;}
.main .block-container{padding:1.5rem 2.5rem;max-width:1500px;}
#MainMenu,header,footer,.stDeployButton{visibility:hidden!important;}
h1,h2,h3,h4{font-family:var(--head)!important;color:var(--text)!important;letter-spacing:-0.02em!important;}
.card{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:1.25rem 1.5rem;margin-bottom:1rem;}
.card-sm{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:1rem 1.25rem;}
.metric-val{font-family:var(--head);font-size:2.1rem;font-weight:800;line-height:1.1;letter-spacing:-0.03em;}
.metric-lbl{font-size:0.78rem;color:var(--muted);text-transform:uppercase;letter-spacing:0.08em;margin-top:0.3rem;}
.metric-delta{font-family:var(--mono);font-size:0.8rem;margin-top:0.4rem;}
.badge{display:inline-block;padding:.2rem .65rem;border-radius:999px;font-size:.72rem;font-weight:600;letter-spacing:.05em;text-transform:uppercase;margin-top:.6rem;}
.badge-ok{background:var(--green-dim);color:var(--green);border:1px solid #0D4A35;}
.badge-warn{background:var(--amber-dim);color:var(--amber);border:1px solid #4A2E08;}
.badge-crit{background:var(--red-dim);color:var(--red);border:1px solid #4A1111;}
.badge-info{background:var(--blue-dim);color:var(--blue);border:1px solid #1A3A6A;}
.topbar{background:linear-gradient(90deg,var(--surface) 0%,var(--bg) 100%);border-bottom:1px solid var(--border);padding:1rem 0 1.2rem;margin-bottom:1.5rem;}
.topbar-title{font-family:var(--head);font-size:1.65rem;font-weight:800;letter-spacing:-0.03em;color:var(--text);line-height:1.15;}
.topbar-sub{font-size:.85rem;color:var(--muted);margin-top:.2rem;font-family:var(--mono);}
div[data-testid="stButton"]>button{background:var(--surface2)!important;border:1px solid var(--border)!important;color:var(--text)!important;border-radius:10px!important;font-family:var(--body)!important;font-weight:500!important;padding:.65rem 1rem!important;transition:all .15s!important;width:100%!important;}
div[data-testid="stButton"]>button:hover{border-color:var(--blue)!important;background:var(--blue-dim)!important;}
div[data-testid="stButton"]>button[kind="primary"]{background:var(--blue-dim)!important;border-color:var(--blue)!important;color:var(--blue)!important;}
.stSlider>div>div>div{background:var(--blue)!important;}
.stSlider>label{color:var(--muted)!important;font-size:.82rem!important;font-family:var(--mono)!important;}
.stTabs [data-baseweb="tab-list"]{background:var(--surface);border-radius:10px;padding:.25rem;border:1px solid var(--border);gap:0;}
.stTabs [data-baseweb="tab"]{border-radius:7px;padding:.6rem 1.1rem;font-weight:500;font-family:var(--body);color:var(--muted);font-size:.9rem;}
.stTabs [aria-selected="true"]{background:var(--blue)!important;color:white!important;font-weight:600!important;}
.risk-bar-wrap{background:var(--surface2);border-radius:999px;height:8px;margin:.4rem 0;overflow:hidden;}
.risk-bar-fill{height:100%;border-radius:999px;transition:width .4s ease;}
.wf-row{display:flex;align-items:center;gap:.75rem;padding:.5rem 0;border-bottom:1px solid var(--border);font-size:.875rem;}
.wf-label{width:160px;color:var(--muted);font-family:var(--mono);font-size:.8rem;}
.wf-bar-wrap{flex:1;background:var(--surface2);height:22px;border-radius:4px;overflow:hidden;position:relative;}
.wf-bar{height:100%;border-radius:4px;display:flex;align-items:center;padding:0 8px;font-family:var(--mono);font-size:.78rem;font-weight:600;white-space:nowrap;}
.wf-val{width:70px;text-align:right;font-family:var(--mono);font-size:.82rem;font-weight:600;}
.sec-div{height:1px;background:linear-gradient(90deg,transparent,var(--border),transparent);margin:1.5rem 0;}
.sc-row{display:flex;justify-content:space-between;align-items:center;padding:.6rem 0;border-bottom:1px solid var(--border);font-size:.85rem;}
.sc-icon{font-size:1rem;margin-right:.5rem;}
.sc-val{font-family:var(--mono);font-size:.8rem;color:var(--muted);}
.flow-step{display:flex;gap:1rem;padding:1.1rem 1.25rem;border-radius:10px;margin-bottom:.65rem;border-left:4px solid;}
.flow-num{width:34px;height:34px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:.875rem;flex-shrink:0;font-family:var(--head);}
.ht-cell-pos{background:rgba(34,211,163,.15);color:var(--green);font-family:var(--mono);font-weight:600;padding:.35rem .65rem;border-radius:4px;text-align:center;}
.ht-cell-neg{background:rgba(248,113,113,.15);color:var(--red);font-family:var(--mono);font-weight:600;padding:.35rem .65rem;border-radius:4px;text-align:center;}
.ht-cell-neu{background:var(--surface2);color:var(--muted);font-family:var(--mono);padding:.35rem .65rem;border-radius:4px;text-align:center;}
::-webkit-scrollbar{width:6px;height:6px;}
::-webkit-scrollbar-track{background:transparent;}
::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px;}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  PLOTLY THEME
# ═══════════════════════════════════════════════════════════════════════════════
PLOTLY_LAYOUT = dict(
    template='plotly_dark',
    paper_bgcolor='rgba(15,25,41,0)',
    plot_bgcolor='rgba(15,25,41,0)',
    font=dict(family="'IBM Plex Mono', monospace", color='#94A3B8', size=11),
    xaxis=dict(gridcolor='#1E3050', zerolinecolor='#1E3050', showgrid=True),
    yaxis=dict(gridcolor='#1E3050', zerolinecolor='#1E3050', showgrid=True),
    margin=dict(l=50, r=30, t=45, b=40),
    legend=dict(bgcolor='rgba(15,25,41,0.8)', bordercolor='#1E3050', borderwidth=1),
)

def styled_fig(fig, height=380):
    fig.update_layout(**PLOTLY_LAYOUT, height=height)
    fig.update_xaxes(gridcolor='#1E3050', linecolor='#1E3050')
    fig.update_yaxes(gridcolor='#1E3050', linecolor='#1E3050')
    return fig

# ═══════════════════════════════════════════════════════════════════════════════
#  CONSTANTS — FINAL PIPELINE VALUES
# ═══════════════════════════════════════════════════════════════════════════════

# ── Portfolio ──────────────────────────────────────────────────────────────────
NPL_BASELINE = 23.3          # STB 2024 observé
PD_BASELINE  = 0.1484        # Stage 2 Probit baseline PD
LGD          = 0.45          # Basel II corporate floor
EAD_TOTAL    = (13_571 + 0.20 * 93 + 42.9) * 1_000_000  # 13,632.5M TND
EPS          = 0.001

# ── Satellite model: logit_NPL ~ AR(1) + PIB + Chomage_lag1 + COVID ───────────
# HAC Newey-West coefficients (final pipeline output)
SAT_COEFS = dict(
    const          = -0.5821,
    logit_NPL_lag1 =  0.8188,
    PIB            = -0.0490,
    Chomage_lag1   =  0.0307,
    COVID          = -0.9015,
)

# Exact HAC covariance matrix from statsmodels (calculated from your Python script)
# Order: const, logit_NPL_lag1, PIB, Chomage_lag1, COVID
SAT_COV = np.array([
    [ 0.065130,  0.018020, -0.002810,  0.004150,  0.031100],
    [ 0.018020,  0.011490, -0.001180,  0.001520,  0.014000],
    [-0.002810, -0.001180,  0.000339, -0.000236, -0.002540],
    [ 0.004150,  0.001520, -0.000236,  0.000303,  0.003860],
    [ 0.031100,  0.014000, -0.002540,  0.003860,  0.038780],
])

# ── Probit Stage 2 coefficients (standardized inputs, final output) ───────────
PROBIT_COEFS = dict(
    const          = -1.4644,
    ENG            =  0.0071,
    CA_Confie      = -0.1214,
    IMP            =  0.1720,
    GEL            =  0.0354,
    PR_log         =  0.1373,
    AGIOS_bin      =  0.3055,
    SECT_1         =  0.0394,
    SECT_3         =  0.0197,
    SECT_4         =  0.1466,
    SECT_5         =  0.0656,
    SECT_6         =  0.1145,
    SECT_8         =  0.0537,
    SECT_9         =  0.0917,
    SECT_10        =  0.0304,
    SECT_11        =  0.0594,
    SECT2_post2019 =  0.7451,   # interaction COVID — SECT 2 post-2019
)

SECT_NAMES = {
    1:  'Agriculture',
    2:  'Autres (SECT2_post2019)',
    3:  'Commerce',
    4:  'Construction',
    5:  'Éducation / Santé',
    6:  'Finance',
    7:  'Consommation (réf.)',
    8:  'Immobilier',
    9:  'Services',
    10: 'Telecom / Tech',
    11: 'Transport',
}

# ── Scenarios (from final stress testing output) ───────────────────────────────
SCENARIOS = {
    'Baseline': {
        'PIB':       [ 2.0,  2.5,  3.0],
        'Chom_lag':  [15.3, 15.2, 15.0],
        'COVID':     [0, 0, 0],
        'color':     '#22D3A3',
        'desc':      'FMI WEO — reprise graduelle',
        'npl_ref':   [23.4, 23.1, 22.4],   # reference from pipeline
        'cushion':   5.8,
    },
    'Défavorable': {
        'PIB':       [ 0.5,  0.0,  1.0],
        'Chom_lag':  [15.3, 16.0, 17.5],
        'COVID':     [0, 0, 0],
        'color':     '#FBBF24',
        'desc':      'Stagflation — chômage 17.5%',
        'npl_ref':   [24.8, 27.0, 28.7],
        'cushion':   212.9,
    },
    'Sévère': {
        'PIB':       [-1.0, -3.0,  0.5],
        'Chom_lag':  [15.3, 17.0, 19.5],
        'COVID':     [0, 0, 0],
        'color':     '#F87171',
        'desc':      'Récession + chômage 19.5%',
        'npl_ref':   [26.2, 31.9, 34.8],
        'cushion':   449.5,
    },
}

# ═══════════════════════════════════════════════════════════════════════════════
#  DATA
# ═══════════════════════════════════════════════════════════════════════════════
@st.cache_data
def get_macro_data():
    """STB NPL 2006-2024 + Tunisia macro (final pipeline data)."""
    return pd.DataFrame({
        'Year':      list(range(2006, 2025)),
        'NPL':       [29.60, 26.70, 23.10, 19.50, 21.10, 23.00, 26.90, 28.67,
                      28.80, 30.30, 28.20, 24.40, 20.80, 18.30, 14.90, 13.50,
                      13.50, 18.10, 23.30],
        'PIB':       [ 5.244,  6.710,  4.238,  3.043,  2.971, -2.047,  4.217,
                       2.430,  3.090,  0.968,  1.117,  2.253,  2.607,  1.550,
                      -8.975,  4.736,  2.752,  0.184,  1.614],
        'Chomage':   [12.5, 12.4, 12.4, 13.3, 13.0, 18.3, 17.6, 15.9,
                      14.3, 15.2, 15.6, 15.3, 15.5, 17.2, 17.7, 16.6,
                      15.3, 15.1, 15.3],
        'Inflation': [ 3.225,  2.967,  4.345,  3.665,  3.339,  3.240,  4.612,
                       5.316,  4.626,  4.437,  3.629,  5.309,  7.308,  6.720,
                       5.634,  5.706,  8.306,  9.329,  7.207],
    })

macro_data = get_macro_data()

# ═══════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
def logit_from_npl(npl_pct):
    r = np.clip(npl_pct / 100, 0.002, 0.998)
    return np.log((r + EPS) / (1 - r + EPS))

def npl_from_logit(x):
    return np.clip(np.exp(x) / (1 + np.exp(x)) * 100, 0.1, 60.0)

def calc_stress(pib_vals, chom_vals, covid_vals=None):
    """Project NPL using AR(1) logit_NPL satellite model."""
    if covid_vals is None:
        covid_vals = [0, 0, 0]
    logit_prev = logit_from_npl(NPL_BASELINE)
    results    = []
    for t in range(3):
        logit_pred = (SAT_COEFS['const']
                      + SAT_COEFS['logit_NPL_lag1'] * logit_prev
                      + SAT_COEFS['PIB']            * pib_vals[t]
                      + SAT_COEFS['Chomage_lag1']   * chom_vals[t]
                      + SAT_COEFS['COVID']          * covid_vals[t])
        npl       = npl_from_logit(logit_pred)
        logit_prev = logit_from_npl(npl)
        pd_s      = float(np.clip(PD_BASELINE * (npl / NPL_BASELINE), 0.001, 0.999))
        el        = pd_s * LGD * EAD_TOTAL / 1e6
        results.append({'year': 2024 + t + 1, 'npl': npl,
                        'delta_npl': npl - NPL_BASELINE,
                        'pd': pd_s, 'el': el,
                        'pib': pib_vals[t], 'chom': chom_vals[t]})
    return results

@st.cache_data
def run_monte_carlo(pib_vals_t, chom_vals_t, n_sim=8000):
    """Multivariate Monte Carlo on HAC covariance matrix (5 params)."""
    coefs_arr = np.array([SAT_COEFS['const'], SAT_COEFS['logit_NPL_lag1'],
                          SAT_COEFS['PIB'], SAT_COEFS['Chomage_lag1'],
                          SAT_COEFS['COVID']])
    draws = np.random.multivariate_normal(coefs_arr, SAT_COV, size=n_sim * 2)
    # constrain to economically valid signs
    mask  = (draws[:, 1] > 0.5) & (draws[:, 1] < 1.0) & \
            (draws[:, 2] < 0)   & (draws[:, 3] > 0)
    draws = draws[mask][:n_sim]
    if len(draws) < 100:
        draws = np.random.multivariate_normal(coefs_arr, SAT_COV, size=n_sim)

    all_npl = []
    for draw in draws:
        logit_p = logit_from_npl(NPL_BASELINE)
        path    = []
        for t in range(3):
            lp = (draw[0] + draw[1] * logit_p
                  + draw[2] * pib_vals_t[t]
                  + draw[3] * chom_vals_t[t])
            npl_t  = npl_from_logit(lp)
            path.append(npl_t)
            logit_p = logit_from_npl(npl_t)
        all_npl.append(path)

    arr     = np.array(all_npl)
    p5      = np.percentile(arr, 5,  axis=0)
    p95     = np.percentile(arr, 95, axis=0)
    el_cur  = PD_BASELINE * LGD * EAD_TOTAL / 1e6
    cushions = np.maximum(0,
        PD_BASELINE * (arr[:, -1] / NPL_BASELINE) * LGD * EAD_TOTAL / 1e6 - el_cur)
    return p5, p95, float(np.mean(cushions > 0))

def calc_pd_probit(eng, ca_confie, imp, gel, pr_log, agios, sect,
                   is_post2019=True):
    """Compute PD from Stage 2 Probit (standardized inputs)."""
    z = PROBIT_COEFS['const']
    z += PROBIT_COEFS['ENG']       * eng
    z += PROBIT_COEFS['CA_Confie'] * ca_confie
    z += PROBIT_COEFS['IMP']       * imp
    z += PROBIT_COEFS['GEL']       * gel
    z += PROBIT_COEFS['PR_log']    * pr_log
    z += PROBIT_COEFS['AGIOS_bin'] * agios
    if sect == 2:
        # SECT_2.0 replaced by SECT2_post2019 interaction
        if is_post2019:
            z += PROBIT_COEFS['SECT2_post2019']
        # else: no sector premium (2019 behavior = reference)
    elif sect != 7:
        key = f'SECT_{sect}'
        z  += PROBIT_COEFS.get(key, 0.0)
    return float(ndtr(z)), float(z)

# ═══════════════════════════════════════════════════════════════════════════════
#  HEADER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="topbar">
  <div class="topbar-title">Stress Testing & Risque de Crédit — STB</div>
  <div class="topbar-sub">
    Architecture Wilson (1997) · Bâle II Pilier 2 · logit_NPL AR(1)+PIB+Chôm+COVID · HAC NW ·
    <span style="color:#22D3A3">● Version finale</span> ·
    {datetime.now().strftime("%d %b %Y")}
  </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  TABS
# ═══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Scénarios de Stress",
    "📈 Modèle Macro NPL",
    "🎯 Validation PD",
    "🏗️ Architecture",
    "🎮 Simulateur Client",
])

# ╔══════════════════════════════════════════════════════════╗
# ║  TAB 1 — STRESS SCENARIOS + MONTE CARLO                ║
# ╚══════════════════════════════════════════════════════════╝
with tab1:
    st.markdown("<div style='font-size:.8rem;color:#64748B;text-transform:uppercase;letter-spacing:.08em;margin-bottom:.6rem;font-family:IBM Plex Mono'>Sélectionner le scénario</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    if 'scen' not in st.session_state:
        st.session_state.scen = 'Baseline'

    with c1:
        if st.button("📗 Baseline", type="primary" if st.session_state.scen == 'Baseline' else "secondary", use_container_width=True):
            st.session_state.scen = 'Baseline'; st.rerun()
    with c2:
        if st.button("📙 Défavorable", type="primary" if st.session_state.scen == 'Défavorable' else "secondary", use_container_width=True):
            st.session_state.scen = 'Défavorable'; st.rerun()
    with c3:
        if st.button("📕 Sévère", type="primary" if st.session_state.scen == 'Sévère' else "secondary", use_container_width=True):
            st.session_state.scen = 'Sévère'; st.rerun()

    scen = SCENARIOS[st.session_state.scen]
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown("<div style='font-size:.8rem;color:#64748B;font-family:IBM Plex Mono;text-transform:uppercase;letter-spacing:.06em;margin-bottom:.4rem'>PIB 2025 (%)</div>", unsafe_allow_html=True)
        pib_0 = st.slider("pib_0", -10.0, 6.0, float(scen['PIB'][0]), 0.5, label_visibility="collapsed")
    with col_s2:
        st.markdown("<div style='font-size:.8rem;color:#64748B;font-family:IBM Plex Mono;text-transform:uppercase;letter-spacing:.06em;margin-bottom:.4rem'>Chômage_lag 2025 (%, valeur 2024)</div>", unsafe_allow_html=True)
        chom_0 = st.slider("chom_0", 12.0, 25.0, float(scen['Chom_lag'][0]), 0.5, label_visibility="collapsed")

    # Build 3-year paths using same logic as pipeline (reversion to scenario path)
    # User modifies 2025 values → 2026-2027 gradually revert to scenario baseline
    delta_pib  = pib_0 - scen['PIB'][0]
    pib_vals   = [pib_0,
                  max(scen['PIB'][1], pib_0 + delta_pib * 0.3),
                  max(scen['PIB'][2], pib_0 + delta_pib * 0.1)]
    
    delta_chom = chom_0 - scen['Chom_lag'][0]
    chom_vals  = [chom_0,
                  min(scen['Chom_lag'][1] + delta_chom, 22.0),
                  min(scen['Chom_lag'][2] + delta_chom * 0.3, 22.0)]
    results = calc_stress(pib_vals, chom_vals)

    max_npl  = max(r['npl'] for r in results)
    max_pd   = max(r['pd']  for r in results)
    max_el   = max(r['el']  for r in results)
    el_cur   = PD_BASELINE * LGD * EAD_TOTAL / 1e6
    cushion  = max(0.0, max_el - el_cur)

    # ── Metrics ──
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    mc1, mc2, mc3, mc4 = st.columns(4)

    color_npl = "#F87171" if max_npl > 30 else ("#FBBF24" if max_npl > 25 else "#22D3A3")
    badge_npl = ("badge-crit", "Critique") if max_npl > 30 else (("badge-warn", "Surveillance") if max_npl > 25 else ("badge-ok", "Stable"))

    with mc1:
        st.markdown(f"""<div class="card-sm">
            <div class="metric-val" style="color:{color_npl}">{max_npl:.1f}%</div>
            <div class="metric-lbl">NPL maximum prédit</div>
            <div class="metric-delta" style="color:{color_npl}">{max_npl - NPL_BASELINE:+.1f}pp vs 2024</div>
            <span class="badge {badge_npl[0]}">{badge_npl[1]}</span>
        </div>""", unsafe_allow_html=True)

    with mc2:
        st.markdown(f"""<div class="card-sm">
            <div class="metric-val">{max_el:.0f}<span style="font-size:1.1rem;font-weight:400;color:#64748B"> M</span></div>
            <div class="metric-lbl">Expected Loss max (TND)</div>
            <div class="metric-delta" style="color:#64748B">{max_el / (EAD_TOTAL/1e6) * 100:.2f}% de l'EAD</div>
            <span class="badge badge-info">EL = PD × LGD × EAD</span>
        </div>""", unsafe_allow_html=True)

    cush_col = "#F87171" if cushion > 400 else ("#FBBF24" if cushion > 150 else "#22D3A3")
    cush_cls = "badge-crit"  if cushion > 400 else ("badge-warn"  if cushion > 150 else "badge-ok")
    with mc3:
        st.markdown(f"""<div class="card-sm">
            <div class="metric-val" style="color:{cush_col}">{cushion:.0f}<span style="font-size:1.1rem;font-weight:400;color:#64748B"> M</span></div>
            <div class="metric-lbl">Coussin Pilier 2</div>
            <div class="metric-delta" style="color:#64748B">{cushion / (EAD_TOTAL/1e6) * 100:.2f}% EAD</div>
            <span class="badge {cush_cls}">Bâle II Pilier 2</span>
        </div>""", unsafe_allow_html=True)

    with mc4:
        st.markdown(f"""<div class="card-sm">
            <div class="metric-val" style="color:#3B82F6">{max_pd:.2%}</div>
            <div class="metric-lbl">PD stressée max</div>
            <div class="metric-delta" style="color:#64748B">baseline {PD_BASELINE:.2%}</div>
            <span class="badge badge-info">IRB Bâle II</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="card-sm" style="margin-top:0.5rem;">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <div>
          <div style="font-size:0.7rem;color:#64748B;">EAD total (Bâle II)</div>
          <div style="font-family:Syne;font-size:1.4rem;font-weight:700;color:#3B82F6">{EAD_TOTAL/1e9:.2f} Mds TND</div>
        </div>
        <div style="text-align:right;">
          <div style="font-size:0.7rem;color:#64748B;">Gross receivables 2024</div>
          <div style="font-family:IBM Plex Mono;font-size:0.9rem;color:#94A3B8">13 571 M</div>
          <div style="font-family:IBM Plex Mono;font-size:0.75rem;color:#475569">+ CCF×93M + intérêts 42.9M</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_ch1, col_ch2 = st.columns([3, 2])

    with col_ch1:
        st.markdown("<div style='font-size:.8rem;color:#64748B;font-family:IBM Plex Mono;text-transform:uppercase;letter-spacing:.06em;margin-bottom:.5rem'>Projections NPL 2025-2027 — IC 90% Monte Carlo</div>", unsafe_allow_html=True)

        with st.spinner("Simulation Monte Carlo…"):
            p5, p95, prob_pos = run_monte_carlo(tuple(pib_vals), tuple(chom_vals))

        hist_years = macro_data['Year'].tolist()
        hist_npl   = macro_data['NPL'].tolist()
        proj_years = [2024] + [r['year'] for r in results]
        proj_npl   = [NPL_BASELINE] + [r['npl'] for r in results]
        p5_full    = [NPL_BASELINE] + list(p5)
        p95_full   = [NPL_BASELINE] + list(p95)

        fig_npl = go.Figure()
        # Historical
        fig_npl.add_trace(go.Scatter(
            x=hist_years, y=hist_npl, mode='lines+markers',
            name='NPL STB observé (2006-2024)',
            line=dict(color='#475569', width=2), marker=dict(size=5)
        ))
        # MC band
        rgb = tuple(int(scen['color'][i:i+2], 16) for i in (1, 3, 5))
        fig_npl.add_trace(go.Scatter(
            x=proj_years + proj_years[::-1],
            y=p95_full + p5_full[::-1],
            fill='toself',
            fillcolor=f'rgba({rgb[0]},{rgb[1]},{rgb[2]},0.10)',
            line=dict(color='rgba(0,0,0,0)'),
            name='IC 90% Monte Carlo', showlegend=True
        ))
        # Projection line
        fig_npl.add_trace(go.Scatter(
            x=proj_years, y=proj_npl, mode='lines+markers',
            name=f'Projection {st.session_state.scen}',
            line=dict(color=scen['color'], width=2.5, dash='dot'),
            marker=dict(size=8, symbol='diamond')
        ))
        # Historical max reference
        fig_npl.add_hline(y=30.3, line_dash="dot", line_color="#475569",
                          annotation_text="Max historique 2015 (30.3%)",
                          annotation_position="top right",
                          annotation_font_color="#64748B")
        fig_npl.add_hline(y=NPL_BASELINE, line_dash="dot", line_color="#3B82F6",
                          annotation_text=f"NPL 2024 = {NPL_BASELINE}%",
                          annotation_position="bottom right",
                          annotation_font_color="#3B82F6")
        # Annotations for 2020 and 2011
        fig_npl.add_vrect(x0=2019.5, x1=2020.5, fillcolor="#F87171",
                          opacity=0.07, line_width=0,
                          annotation_text="COVID+BCT", annotation_position="top left",
                          annotation_font=dict(color="#F87171", size=9))
        fig_npl.add_annotation(x=proj_years[-1] + 0.1, y=proj_npl[-1],
                                text=f"<b>{proj_npl[-1]:.1f}%</b>",
                                font=dict(color=scen['color'], size=13, family="Syne"),
                                showarrow=False)
        fig_npl = styled_fig(fig_npl, 380)
        st.plotly_chart(fig_npl, use_container_width=True)

        st.markdown(f"""<div style="background:rgba(34,211,163,.08);border:1px solid rgba(34,211,163,.25);
            border-radius:8px;padding:.65rem 1rem;font-family:IBM Plex Mono;font-size:.82rem;color:#22D3A3;margin-top:-.5rem">
            Monte Carlo multivarié N≈{int(prob_pos*8000):,} tirages valides · Signes économiques imposés ·
            P(coussin > 0) = <b>{prob_pos:.1%}</b>
        </div>""", unsafe_allow_html=True)

    with col_ch2:
        st.markdown("<div style='font-size:.8rem;color:#64748B;font-family:IBM Plex Mono;text-transform:uppercase;letter-spacing:.06em;margin-bottom:.5rem'>Expected Loss par année</div>", unsafe_allow_html=True)

        fig_el = go.Figure()
        fig_el.add_trace(go.Bar(
            x=[r['year'] for r in results],
            y=[r['el'] for r in results],
            marker_color=[scen['color']] * 3, marker_opacity=0.85,
            text=[f"{v['el']:.0f}M" for v in results],
            textposition='outside',
            textfont=dict(family="IBM Plex Mono", size=11, color=scen['color'])
        ))
        fig_el.add_hline(y=el_cur, line_dash="dot", line_color="#64748B",
                         annotation_text=f"EL actuel {el_cur:.0f}M",
                         annotation_position="top right",
                         annotation_font_color="#64748B")
        fig_el = styled_fig(fig_el, 200)
        fig_el.update_layout(showlegend=False)
        st.plotly_chart(fig_el, use_container_width=True)

        # Detail table
        rows_html = ""
        for r in results:
            delta = r['delta_npl']
            cell  = "ht-cell-pos" if delta < 0 else ("ht-cell-neg" if delta > 3 else "ht-cell-neu")
            rows_html += f"""<tr>
              <td style="padding:.45rem .6rem;font-family:IBM Plex Mono;font-size:.8rem;color:#94A3B8">{r['year']}</td>
              <td style="padding:.45rem .6rem"><span class="{'ht-cell-neg' if r['pib']<0 else 'ht-cell-pos'}">{r['pib']:+.1f}%</span></td>
              <td style="padding:.45rem .6rem"><span class="{cell}">{delta:+.1f}pp</span></td>
              <td style="padding:.45rem .6rem;font-family:IBM Plex Mono;font-size:.82rem;color:#E2E8F0">{r['npl']:.1f}%</td>
              <td style="padding:.45rem .6rem;font-family:IBM Plex Mono;font-size:.82rem;color:#3B82F6">{r['pd']:.2%}</td>
            </tr>"""

        st.markdown(f"""<div class="card" style="padding:.8rem">
        <table style="width:100%;border-collapse:collapse">
          <thead><tr style="border-bottom:1px solid #1E3050">
            <th style="padding:.4rem .6rem;text-align:left;font-size:.72rem;color:#64748B;text-transform:uppercase;letter-spacing:.06em">Année</th>
            <th style="padding:.4rem .6rem;text-align:left;font-size:.72rem;color:#64748B;text-transform:uppercase;letter-spacing:.06em">PIB</th>
            <th style="padding:.4rem .6rem;text-align:left;font-size:.72rem;color:#64748B;text-transform:uppercase;letter-spacing:.06em">ΔNPL</th>
            <th style="padding:.4rem .6rem;text-align:left;font-size:.72rem;color:#64748B;text-transform:uppercase;letter-spacing:.06em">NPL</th>
            <th style="padding:.4rem .6rem;text-align:left;font-size:.72rem;color:#64748B;text-transform:uppercase;letter-spacing:.06em">PD</th>
          </tr></thead>
          <tbody>{rows_html}</tbody>
        </table></div>""", unsafe_allow_html=True)

        # Coussin table for all 3 scenarios (pipeline reference)
        st.markdown("<div style='font-size:.8rem;color:#64748B;font-family:IBM Plex Mono;text-transform:uppercase;letter-spacing:.06em;margin:.8rem 0 .4rem'>Coussins Pilier 2 — pipeline final</div>", unsafe_allow_html=True)
        for sname, sdata in SCENARIOS.items():
            c = sdata['color']
            st.markdown(f"""<div style="display:flex;justify-content:space-between;align-items:center;
                padding:.5rem .75rem;margin-bottom:.3rem;background:#162236;border-radius:7px;border:1px solid #1E3050">
                <span style="font-size:.82rem;color:#94A3B8">{sname}</span>
                <span style="font-family:IBM Plex Mono;font-size:.85rem;color:{c};font-weight:600">{sdata['cushion']:.0f} M TND</span>
                <span style="font-family:IBM Plex Mono;font-size:.75rem;color:#64748B">{sdata['cushion']/(EAD_TOTAL/1e6)*100:.2f}% EAD</span>
            </div>""", unsafe_allow_html=True)

# ╔══════════════════════════════════════════════════════════╗
# ║  TAB 2 — MACRO NPL MODEL                               ║
# ╚══════════════════════════════════════════════════════════╝
with tab2:
    col_m1, col_m2 = st.columns([3, 2])

    with col_m1:
        st.markdown("<div style='font-size:.8rem;color:#64748B;font-family:IBM Plex Mono;text-transform:uppercase;letter-spacing:.06em;margin-bottom:.5rem'>logit_NPL : Observé vs Ajusté — STB 2008-2024</div>", unsafe_allow_html=True)

        df_sat  = macro_data[macro_data['Year'] >= 2008].copy().reset_index(drop=True)
        npl_arr = df_sat['NPL'].values
        pib_arr = df_sat['PIB'].values
        chom_lag = np.concatenate([[np.nan], df_sat['Chomage'].values[:-1]])
        covid    = (df_sat['Year'] == 2020).astype(int).values

        logit_obs = np.array([logit_from_npl(n) for n in npl_arr])
        logit_fit = np.full_like(logit_obs, np.nan)
        logit_fit[0] = logit_obs[0]
        for i in range(1, len(logit_obs)):
            if np.isnan(chom_lag[i]):
                logit_fit[i] = logit_obs[i]
            else:
                logit_fit[i] = (SAT_COEFS['const']
                                + SAT_COEFS['logit_NPL_lag1'] * logit_fit[i-1]
                                + SAT_COEFS['PIB']            * pib_arr[i]
                                + SAT_COEFS['Chomage_lag1']   * chom_lag[i]
                                + SAT_COEFS['COVID']          * covid[i])

        npl_fit_level = np.array([npl_from_logit(x) for x in logit_fit])
        years_sat     = df_sat['Year'].tolist()

        mae_val = float(np.mean(np.abs(npl_arr[1:] - npl_fit_level[1:])))

        fig_fit = go.Figure()
        fig_fit.add_trace(go.Scatter(x=years_sat, y=npl_arr, mode='lines+markers',
            name='NPL STB observé',
            line=dict(color='#E2E8F0', width=2.2), marker=dict(size=6)))
        fig_fit.add_trace(go.Scatter(x=years_sat, y=npl_fit_level, mode='lines+markers',
            name=f'NPL ajusté (R²adj=0.744 · MAE={mae_val:.2f}pp)',
            line=dict(color='#3B82F6', width=2, dash='dash'), marker=dict(size=5)))
        fig_fit.add_vrect(x0=2019.5, x1=2020.5, fillcolor="#F87171",
            opacity=0.08, line_width=0,
            annotation_text="COVID\n(forbearance BCT)",
            annotation_position="top left",
            annotation_font=dict(color="#F87171", size=9, family="IBM Plex Mono"))
        fig_fit.add_vrect(x0=2010.5, x1=2011.5, fillcolor="#FBBF24",
            opacity=0.08, line_width=0,
            annotation_text="Printemps Arabe",
            annotation_position="top left",
            annotation_font=dict(color="#FBBF24", size=9, family="IBM Plex Mono"))
        fig_fit = styled_fig(fig_fit, 300)
        fig_fit.update_layout(legend=dict(y=-.15, orientation='h'))
        st.plotly_chart(fig_fit, use_container_width=True)

        # Waterfall — coefficient contributions for severe 2026
        st.markdown("<div style='font-size:.8rem;color:#64748B;font-family:IBM Plex Mono;text-transform:uppercase;letter-spacing:.06em;margin-bottom:.5rem;margin-top:.5rem'>Décomposition logit_NPL — scénario sévère 2026 (PIB=−3%, Chôm=17%)</div>", unsafe_allow_html=True)

        logit_2025 = logit_from_npl(26.2)   # sévère 2025 result
        contributions = {
            'AR(1) term':         SAT_COEFS['logit_NPL_lag1'] * logit_2025,
            'Constante':          SAT_COEFS['const'],
            'PIB (−3.0%)':        SAT_COEFS['PIB']          * (-3.0),
            'Chômage_lag (17.0%)':SAT_COEFS['Chomage_lag1'] * 17.0,
            'COVID (=0)':         0.0,
        }
        total_logit = sum(contributions.values())
        total_npl   = npl_from_logit(total_logit)
        max_abs     = max(abs(v) for v in contributions.values() if v != 0) or 1

        wf_html = ""
        for label, val in contributions.items():
            if val == 0:
                continue
            pct   = abs(val) / max_abs * 100
            color = "#22D3A3" if val < 0 else "#F87171"
            wf_html += f"""<div class="wf-row">
              <div class="wf-label">{label}</div>
              <div class="wf-bar-wrap">
                <div class="wf-bar" style="width:{pct:.0f}%;background:{color}22;color:{color};border-left:3px solid {color}">
                  {val:+.4f}
                </div>
              </div>
              <div class="wf-val" style="color:{color}">{val:+.4f}</div>
            </div>"""

        wf_html += f"""<div class="wf-row" style="border-top:2px solid #1E3050;margin-top:.25rem;padding-top:.6rem">
          <div class="wf-label" style="font-weight:600;color:#E2E8F0">logit_NPL prédit</div>
          <div class="wf-bar-wrap">
            <div class="wf-bar" style="width:80%;background:#F87171;color:#F87171;border-left:3px solid #F87171;font-weight:700">
              → NPL = {total_npl:.1f}%
            </div>
          </div>
          <div class="wf-val" style="color:#F87171;font-weight:700">{total_logit:+.4f}</div>
        </div>"""

        st.markdown(f'<div class="card">{wf_html}</div>', unsafe_allow_html=True)

    with col_m2:
        # Model specification
        st.markdown("""<div class="card">
          <div style="font-size:.72rem;color:#64748B;text-transform:uppercase;letter-spacing:.08em;margin-bottom:.8rem;font-family:IBM Plex Mono">Spécification satellite</div>
          <div style="font-family:IBM Plex Mono;font-size:.82rem;background:#0F1929;padding:.85rem;border-radius:8px;border:1px solid #1E3050;line-height:1.8;color:#94A3B8">
            <span style="color:#22D3A3">logit_NPL</span><sub>t</sub> =<br>
            &nbsp;&nbsp;&nbsp;β₀ (const)<br>
            &nbsp;&nbsp;&nbsp;+ β₁ <span style="color:#3B82F6">logit_NPL</span><sub>t-1</sub><br>
            &nbsp;&nbsp;&nbsp;+ β₂ <span style="color:#FBBF24">PIB</span><sub>t</sub><br>
            &nbsp;&nbsp;&nbsp;+ β₃ <span style="color:#FBBF24">Chôm</span><sub>t-1</sub><br>
            &nbsp;&nbsp;&nbsp;+ β₄ <span style="color:#F87171">COVID</span><sub>t</sub><br>
            &nbsp;&nbsp;&nbsp;+ ε<sub>t</sub>
          </div>
          <div style="font-family:IBM Plex Mono;font-size:.75rem;color:#64748B;margin-top:.7rem">
            logit_NPL = log(NPL/(1-NPL)) · stationnaire (ADF p=0.003)<br>
            HAC Newey-West · 2 lags · N=17 (2008-2024)
          </div>
        </div>""", unsafe_allow_html=True)

        # Diagnostics
        diags = [
            ("N", "17  (2008-2024)"),
            ("R²adj", "0.744"),
            ("MAE", "2.06 pp"),
            ("RMSE", "2.34 pp"),
            ("DW", "1.219  (zone inconcl.)"),
            ("HAC", "Newey-West 2 lags ✓"),
            ("JB p", "0.582 ✓"),
            ("SW p", "0.520 ✓"),
            ("ADF logit_NPL", "p=0.003 ✓"),
            ("GLS stab. macro", "Δ<0.05 ✓"),
        ]
        drows = "".join(f"""<div class="sc-row">
            <span style="color:#64748B;font-family:IBM Plex Mono;font-size:.8rem">{k}</span>
            <span style="font-family:IBM Plex Mono;font-size:.82rem;color:#E2E8F0">{v}</span>
        </div>""" for k, v in diags)
        st.markdown(f'<div class="card"><div style="font-size:.72rem;color:#64748B;text-transform:uppercase;letter-spacing:.08em;margin-bottom:.6rem;font-family:IBM Plex Mono">Diagnostiques</div>{drows}</div>', unsafe_allow_html=True)

        # Coefficients HAC
        coef_rows = [
            ("const",           "-0.5821", "0.0225", "**"),
            ("logit_NPL_lag1",  "+0.8188", "0.0000", "***"),
            ("PIB",             "-0.0490", "0.0077", "***"),
            ("Chomage_lag1",    "+0.0307", "0.0777", "*"),
            ("COVID",           "-0.9015", "0.0000", "***"),
        ]
        crow_html = "".join(f"""<div class="sc-row">
            <span style="font-family:IBM Plex Mono;font-size:.8rem;color:#94A3B8">{v}</span>
            <span style="font-family:IBM Plex Mono;font-size:.8rem;color:{'#22D3A3' if '-' in b else '#F87171'}">{b}</span>
            <span style="font-family:IBM Plex Mono;font-size:.75rem;color:#64748B">p={p} {s}</span>
        </div>""" for v, b, p, s in coef_rows)
        st.markdown(f'<div class="card" style="margin-top:1rem"><div style="font-size:.72rem;color:#64748B;text-transform:uppercase;letter-spacing:.08em;margin-bottom:.6rem;font-family:IBM Plex Mono">Coefficients HAC Newey-West</div>{crow_html}</div>', unsafe_allow_html=True)

# ╔══════════════════════════════════════════════════════════╗
# ║  TAB 3 — VALIDATION PD                                 ║
# ╚══════════════════════════════════════════════════════════╝
with tab3:
    vm1, vm2, vm3, vm4, vm5 = st.columns(5)
    vmets = [
        ("AUC-ROC",    "0.9427", "> 0.80", "ok"),
        ("Gini",       "0.8855", "> 0.50", "ok"),
        ("KS stat.",   "0.7833", "> 0.40", "ok"),
        ("CV std",     "0.0016", "< 0.05", "ok"),
        ("Brier Skill","0.3746", "> 0.25", "ok"),
    ]
    for col, (name, val, thr, _) in zip([vm1, vm2, vm3, vm4, vm5], vmets):
        col.markdown(f"""<div class="card-sm" style="text-align:center">
          <div style="font-family:IBM Plex Mono;font-size:.72rem;color:#64748B;text-transform:uppercase;letter-spacing:.06em;margin-bottom:.4rem">{name}</div>
          <div class="metric-val" style="font-size:1.6rem;color:#22D3A3">{val}</div>
          <div style="font-family:IBM Plex Mono;font-size:.75rem;color:#64748B;margin-top:.2rem">{thr}</div>
          <span class="badge badge-ok">✓ Basel II</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    col_v1, col_v2 = st.columns([1, 1])

    with col_v1:
        st.markdown("<div style='font-size:.8rem;color:#64748B;font-family:IBM Plex Mono;text-transform:uppercase;letter-spacing:.06em;margin-bottom:.5rem'>Courbe ROC — Probit Stage 2</div>", unsafe_allow_html=True)
        fpr_pts = np.linspace(0, 1, 300)
        # Approximation plus précise pour AUC=0.9427
        # TPR = 1 - (1 - FPR)^(1/(1-AUC)) approx
        power = 1 / (1 - 0.9427)  # ≈ 17.45
        tpr_pts = np.clip(1 - (1 - fpr_pts) ** (1/power), 0, 1)

        fig_roc = go.Figure()
        fig_roc.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode='lines',
            name='Aléatoire (AUC=0.50)',
            line=dict(color='#475569', dash='dash', width=1.5)))
        fig_roc.add_trace(go.Scatter(x=fpr_pts, y=tpr_pts, mode='lines',
            name='Probit Stage 2 (AUC=0.9427)',
            line=dict(color='#3B82F6', width=2.5),
            fill='tozeroy', fillcolor='rgba(59,130,246,0.08)'))
        fig_roc.update_layout(xaxis_title='FPR', yaxis_title='TPR',
            legend=dict(y=.05, x=.4))
        fig_roc = styled_fig(fig_roc, 290)
        st.plotly_chart(fig_roc, use_container_width=True)
        st.markdown("""
        <div style="font-size:0.7rem; color:#64748B; margin-top:-0.5rem; margin-bottom:1rem;">
          *Courbe ROC simulée à partir de l'AUC=0.9427 — données réelles (65 515 obs) disponibles dans le rapport*
        </div>
        """, unsafe_allow_html=True)

        # AUC by year
        st.markdown("<div style='font-size:.8rem;color:#64748B;font-family:IBM Plex Mono;text-transform:uppercase;letter-spacing:.06em;margin-bottom:.5rem;margin-top:.5rem'>AUC par année (robustesse COVID)</div>", unsafe_allow_html=True)
        yr_aucs = [
            ('2019', 0.7295, 1114,  '#FBBF24', '⚠ Small N'),
            ('2020', 0.9366, 31473, '#22D3A3', '✓'),
            ('2021', 0.9476, 32928, '#22D3A3', '✓'),
        ]
        yr_html = "".join(f"""<div class="sc-row">
            <span style="font-family:IBM Plex Mono;color:#94A3B8;width:3rem">{yr}</span>
            <div style="flex:1;margin:0 .75rem">
              <div class="risk-bar-wrap">
                <div class="risk-bar-fill" style="width:{auc*100:.0f}%;background:{c}"></div>
              </div>
            </div>
            <span style="font-family:IBM Plex Mono;font-size:.82rem;color:{c};width:4rem">{auc:.4f}</span>
            <span style="font-family:IBM Plex Mono;font-size:.75rem;color:#64748B;margin-left:.3rem;width:3rem">{note}</span>
            <span style="font-family:IBM Plex Mono;font-size:.72rem;color:#475569;margin-left:.3rem">N={n:,}</span>
        </div>""" for yr, auc, n, c, note in yr_aucs)
        st.markdown(f'<div class="card">{yr_html}</div>', unsafe_allow_html=True)

        # Note on 2019
        st.markdown("""<div style="background:rgba(251,191,36,.07);border:1px solid rgba(251,191,36,.25);
            border-radius:8px;padding:.6rem .9rem;font-family:IBM Plex Mono;font-size:.78rem;color:#FBBF24;margin-top:.5rem">
            2019 : AUC=0.7295 (>seuil Bâle II 0.70 ✓) · N=1 114 limité · SECT2_post2019 inactif (2019)
        </div>""", unsafe_allow_html=True)

    with col_v2:
        # CV stability
        st.markdown("<div style='font-size:.8rem;color:#64748B;font-family:IBM Plex Mono;text-transform:uppercase;letter-spacing:.06em;margin-bottom:.5rem'>Stabilité cross-validation 5-fold</div>", unsafe_allow_html=True)
        cv_aucs = [0.9447, 0.9407, 0.9406, 0.9436, 0.9432]
        cv_mean = np.mean(cv_aucs)
        fig_cv  = go.Figure()
        cv_col  = ['#22D3A3' if a >= cv_mean else '#FBBF24' for a in cv_aucs]
        fig_cv.add_trace(go.Bar(
            x=[f'Fold {i+1}' for i in range(5)], y=cv_aucs,
            marker_color=cv_col, marker_opacity=0.85,
            text=[f'{a:.4f}' for a in cv_aucs], textposition='outside',
            textfont=dict(family='IBM Plex Mono', size=10)
        ))
        fig_cv.add_hline(y=cv_mean, line_dash='dash', line_color='#3B82F6',
            annotation_text=f'μ={cv_mean:.4f}', annotation_font_color='#3B82F6')
        fig_cv.add_hline(y=0.80, line_dash='dot', line_color='#22D3A3', opacity=0.5,
            annotation_text='Bâle good (0.80)', annotation_position='top right',
            annotation_font_color='#22D3A3')
        fig_cv = styled_fig(fig_cv, 240)
        fig_cv.update_layout(showlegend=False, yaxis_range=[0.925, 0.960])
        st.plotly_chart(fig_cv, use_container_width=True)

        # Full scorecard
        sc_items = [
            ("✓", "AUC > 0.80",                    "0.9427"),
            ("✓", "Gini > 0.50",                   "0.8855"),
            ("✓", "KS > 0.40",                     "0.7833"),
            ("✓", "Séparation defaulteurs",        "0.472 vs 0.091"),
            ("✓", "Brier Skill > 0.25",             "0.3746"),
            ("✗", "HL p > 0.05",                    "p=0.000  (N=65k)"),
            ("✓", "CV gap < 0.02",                  "0.0002"),
            ("✓", "CV std < 0.05",                  "0.0016"),
            ("✓", "AUC > 0.70 toutes années",       "min=0.7295"),
            ("✓", "Monotonie profils clients",      "✓"),
        ]
        sc_html = "".join(f"""<div class="sc-row">
            <span class="sc-icon" style="color:{'#22D3A3' if i=='✓' else '#F87171'}">{i}</span>
            <span style="flex:1;font-size:.82rem">{n}</span>
            <span class="sc-val">{v}</span>
        </div>""" for i, n, v in sc_items)
        passed = sum(1 for i, _, _ in sc_items if i == '✓')
        st.markdown(f"""<div class="card" style="margin-top:.5rem">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.6rem">
            <div style="font-size:.72rem;color:#64748B;text-transform:uppercase;letter-spacing:.08em;font-family:IBM Plex Mono">Scorecard Bâle II — Probit Stage 2</div>
            <span class="badge badge-{'ok' if passed>=9 else 'warn'}">{passed}/10</span>
          </div>
          {sc_html}
          <div style="font-family:IBM Plex Mono;font-size:.75rem;color:#64748B;margin-top:.6rem;padding-top:.5rem;border-top:1px solid #1E3050">
            HL [✗] attendu pour N>50 000 — Hosmer & Lemeshow (2000, p.147).<br>
            Brier Skill 0.375 confirme une bonne calibration globale.
          </div>
        </div>""", unsafe_allow_html=True)

# ╔══════════════════════════════════════════════════════════╗
# ║  TAB 4 — ARCHITECTURE PIPELINE                         ║
# ╚══════════════════════════════════════════════════════════╝
with tab4:
    steps = [
        ("#3B82F6", "1", "Stage 1 — Analyse exploratoire (Data.csv)",
         ["4 133 clients entreprises · CL R 0-3 · 2019-2021",
          "Set A (bancaires 16 vars) · Set B (5 ratios) · Set C (21 vars combinés)",
          "Logit · Probit · LDA · 9 comparaisons · backward elimination",
          "Résultat : Set A dominant (Gini=0.591 > C=0.585 > B=0.224)",
          "Conclusion : variables bancaires > ratios financiers"]),
        ("#22D3A3", "2", "Stage 2 — Analyse confirmatoire (Set_A.csv)",
         ["327 571 clients · CL R = 4/5 exclus (Bâle II : déjà en défaut)",
          "Fix SECT_2.0 → SECT2_post2019 (artefact moratoire BCT, CV AUC 0.9426)",
          "Probit Stage 2 retenu · AUC=0.9427 · Gini=0.8855 · 9/10 checks",
          "EAD = 13 632.5 M TND · PD baseline = 14.84% · N=262 056 (train)"]),
        ("#FBBF24", "3", "Modèle satellite — logit_NPL STB",
         ["Données NPL STB 2006-2024 (rapports annuels)",
          "logit_NPL stationnaire confirmé (ADF p=0.003)",
          "Sélection exhaustive : 31 specs testées → AR(1)+PIB+Chôm_lag+COVID",
          "R²adj=0.744 · MAE=2.06pp · HAC NW · GLS confirme stabilité coefs",
          "COVID β=−0.9015 (forbearance BCT 2020) — mis à 0 pour projections"]),
        ("#F87171", "4", "Stress Testing — 3 scénarios 2025-2027",
         ["Baseline (FMI) · Défavorable (stagflation) · Sévère (récession)",
          "Linkage : PD_stress = PD_base × (NPL_stressé / NPL_2024)",
          "EL = PD_stress × 45% × 13 632.5M TND",
          "Monte Carlo multivarié (N≈8000, signes imposés) · P(coussin>0)=99.7%",
          "Coussin Pilier 2 sévère : 449.5 M TND (3.30% EAD)"]),
    ]

    col_a1, col_a2 = st.columns([3, 2])
    with col_a1:
        for color, num, title, lines in steps:
            lines_html = "".join(f'<div style="font-size:.82rem;color:{color};opacity:.85;margin:.2rem 0">• {l}</div>' for l in lines)
            st.markdown(f"""<div class="flow-step" style="background:{color}08;border-color:{color}">
              <div class="flow-num" style="background:{color}20;color:{color}">{num}</div>
              <div>
                <div style="font-family:Syne;font-weight:700;color:{color};font-size:.95rem;margin-bottom:.4rem">{title}</div>
                {lines_html}
              </div>
            </div>""", unsafe_allow_html=True)

    with col_a2:
        st.markdown("""<div class="card">
          <div style="font-size:.72rem;color:#64748B;text-transform:uppercase;letter-spacing:.08em;margin-bottom:.8rem;font-family:IBM Plex Mono">Linkage macro ↔ micro</div>
          <div style="font-family:IBM Plex Mono;font-size:.78rem;color:#94A3B8;line-height:2.1">
            <div style="color:#E2E8F0">327 571 clients (Set_A)</div>
            <div style="padding-left:1rem;color:#64748B">↓ backward elim p&lt;0.05</div>
            <div style="color:#3B82F6">Probit Stage 2</div>
            <div style="padding-left:1rem;color:#64748B">→ PD_baseline = 14.84%</div>
            <div style="color:#64748B;padding-left:1rem">↕ linkage NPL</div>
            <div style="color:#FBBF24">Satellite logit_NPL AR(1)</div>
            <div style="padding-left:1rem;color:#64748B">→ NPL_stressé (2025-27)</div>
            <div style="color:#64748B;padding-left:1rem">↓</div>
            <div style="color:#E2E8F0;font-size:.75rem">PD_s = PD_b × (NPL_s/23.3%)</div>
            <div style="color:#64748B;padding-left:1rem">↓</div>
            <div style="color:#F87171">EL = PD_s × 45% × 13 632 M</div>
            <div style="color:#64748B;padding-left:1rem">↓</div>
            <div style="color:#22D3A3">Coussin = EL_stress − EL_base</div>
          </div>
        </div>""", unsafe_allow_html=True)

        obs_data = [
            ("Set_A.csv brut",         "451 835"),
            ("Après dropna(ACTIVITE)", "437 473"),
            ("CL R = 4/5 retirés",     "327 571"),
            ("Train (80%)",             "262 056"),
            ("Test (20%)",              "65 515"),
            ("Défauts test set",        "9 701  (14.8%)"),
            ("NPL STB 2024",            "23.3%"),
            ("EAD total",               "13 632.5 M TND"),
        ]
        obs_html = "".join(f"""<div class="sc-row">
            <span style="font-size:.82rem;color:#94A3B8">{k}</span>
            <span style="font-family:IBM Plex Mono;font-size:.82rem;color:#3B82F6">{v}</span>
        </div>""" for k, v in obs_data)
        st.markdown(f"""<div class="card" style="margin-top:1rem">
          <div style="font-size:.72rem;color:#64748B;text-transform:uppercase;letter-spacing:.08em;margin-bottom:.6rem;font-family:IBM Plex Mono">Chiffres clés du pipeline</div>
          {obs_html}
        </div>""", unsafe_allow_html=True)

# ╔══════════════════════════════════════════════════════════╗
# ║  TAB 5 — CLIENT SCORING SIMULATOR                      ║
# ╚══════════════════════════════════════════════════════════╝
with tab5:
    st.markdown("""<div style="background:rgba(59,130,246,.08);border:1px solid rgba(59,130,246,.3);
        border-radius:10px;padding:.85rem 1.1rem;margin-bottom:1.2rem;font-size:.85rem;color:#94A3B8">
        <b style="color:#3B82F6">Simulateur en temps réel</b> — Modèle Probit Stage 2 (N=327 571 · AUC=0.9427).
        Modifiez les paramètres (valeurs <i>standardisées</i> : 0 = moyenne portefeuille, ±1 = ±1 écart-type).
        <b style="color:#FBBF24">SECT 2 (Autres)</b> active SECT2_post2019 (artefact moratoire BCT).
    </div>""", unsafe_allow_html=True)

    col_inp, col_out = st.columns([2, 1])

    with col_inp:
        st.markdown("<div style='font-size:.8rem;color:#64748B;font-family:IBM Plex Mono;text-transform:uppercase;letter-spacing:.06em;margin-bottom:.8rem'>Variables bancaires (standardisées)</div>", unsafe_allow_html=True)

        ci1, ci2 = st.columns(2)
        with ci1:
            eng    = st.slider("ENG — Engagement total",         -2.0, 3.0,  0.0, 0.1)
            imp    = st.slider("IMP — Impayés",                  -1.0, 3.0,  0.0, 0.1)
            pr_log = st.slider("PR_log — Provisions (log)",      -2.0, 3.0,  0.0, 0.1)
        with ci2:
            ca_confie = st.slider("CA_Confie — CA domicilié",   -2.0, 2.0,  0.0, 0.1)
            gel       = st.slider("GEL — Avoirs gelés",          -1.0, 3.0,  0.0, 0.1)

        ci3, ci4 = st.columns(2)
        with ci3:
            agios = st.radio("AGIOS — Intérêts pénaux",
                             options=[0, 1],
                             format_func=lambda x: "Non (0)" if x == 0 else "Oui (1)",
                             horizontal=True)
        with ci4:
            sect_choice = st.selectbox(
                "Secteur d'activité",
                options=[k for k in SECT_NAMES.keys() if k != 7],
                format_func=lambda x: SECT_NAMES[x]
            )

        # SECT2_post2019 toggle
        post2019 = True
        if sect_choice == 2:
            post2019 = st.checkbox(
                "SECT2_post2019 actif (période post-2019 → moratoire BCT)",
                value=True
            )

        pd_val, z_score = calc_pd_probit(eng, ca_confie, imp, gel, pr_log,
                                          agios, sect_choice, post2019)

    with col_out:
        level_txt   = ("Risque TRÈS ÉLEVÉ" if pd_val > .50 else
                       ("Risque ÉLEVÉ"      if pd_val > .25 else
                        ("Risque MODÉRÉ"    if pd_val > .10 else "Risque FAIBLE")))
        level_color = ("#F87171" if pd_val > .50 else
                       ("#FBBF24" if pd_val > .25 else
                        ("#FCA5A5" if pd_val > .10 else "#22D3A3")))
        badge_cls   = ("badge-crit" if pd_val > .50 else
                       ("badge-warn" if pd_val > .25 else
                        ("badge-warn" if pd_val > .10 else "badge-ok")))

        st.markdown(f"""<div class="card" style="text-align:center;padding:1.75rem 1.5rem;border-color:{level_color}40">
          <div style="font-family:IBM Plex Mono;font-size:.75rem;color:#64748B;text-transform:uppercase;letter-spacing:.1em;margin-bottom:.5rem">
            Probabilité de Défaut — Probit
          </div>
          <div style="font-family:Syne;font-size:3.5rem;font-weight:800;color:{level_color};line-height:1;letter-spacing:-.03em">
            {pd_val:.1%}
          </div>
          <div style="margin:.8rem 0">
            <div class="risk-bar-wrap" style="height:10px">
              <div class="risk-bar-fill" style="width:{min(pd_val*100,100):.0f}%;background:{level_color}"></div>
            </div>
          </div>
          <span class="badge {badge_cls}">{level_txt}</span>
          <div style="font-family:IBM Plex Mono;font-size:.78rem;color:#64748B;margin-top:.8rem">
            Z-score Probit = {z_score:+.4f}<br>
            PD_baseline = {PD_BASELINE:.2%}
          </div>
        </div>""", unsafe_allow_html=True)

        el_client = pd_val * LGD * 1_000_000
        st.markdown(f"""<div class="card-sm" style="margin-top:.75rem">
          <div style="font-size:.72rem;color:#64748B;font-family:IBM Plex Mono;text-transform:uppercase;letter-spacing:.06em;margin-bottom:.5rem">
            Expected Loss (EAD = 1 M TND)
          </div>
          <div style="font-family:Syne;font-size:1.8rem;font-weight:700;color:#3B82F6">
            {el_client/1000:.1f} k TND
          </div>
          <div style="font-size:.78rem;color:#64748B;margin-top:.3rem;font-family:IBM Plex Mono">
            {pd_val:.2%} × 45% × 1 000 000
          </div>
        </div>""", unsafe_allow_html=True)

    # Variable contributions
    st.markdown("<div class='sec-div'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:.8rem;color:#64748B;font-family:IBM Plex Mono;text-transform:uppercase;letter-spacing:.06em;margin-bottom:.6rem'>Contribution de chaque variable au score Z (Probit)</div>", unsafe_allow_html=True)

    sect_coef = PROBIT_COEFS.get('SECT2_post2019' if (sect_choice == 2 and post2019)
                                   else f'SECT_{sect_choice}', 0.0)
    contribs = {
        'ENG':       PROBIT_COEFS['ENG']       * eng,
        'CA_Confie': PROBIT_COEFS['CA_Confie'] * ca_confie,
        'IMP':       PROBIT_COEFS['IMP']       * imp,
        'GEL':       PROBIT_COEFS['GEL']       * gel,
        'PR_log':    PROBIT_COEFS['PR_log']    * pr_log,
        'AGIOS':     PROBIT_COEFS['AGIOS_bin'] * agios,
        'Secteur':   sect_coef,
        'Constante': PROBIT_COEFS['const'],
    }
    max_abs_c = max(abs(v) for v in contribs.values()) or 1

    cont_cols = st.columns(2)
    for i, (var, val) in enumerate(sorted(contribs.items(), key=lambda x: abs(x[1]), reverse=True)):
        pct   = abs(val) / max_abs_c * 100
        color = "#22D3A3" if val <= 0 else "#F87171"
        txt   = "↓ réduit risque" if val <= 0 else "↑ augmente risque"
        cont_cols[i % 2].markdown(f"""<div style="margin-bottom:.5rem">
          <div style="display:flex;justify-content:space-between;margin-bottom:.2rem">
            <span style="font-family:IBM Plex Mono;font-size:.78rem;color:#94A3B8">{var}</span>
            <span style="font-family:IBM Plex Mono;font-size:.78rem;color:{color}">{val:+.4f} &nbsp;{txt}</span>
          </div>
          <div class="risk-bar-wrap">
            <div class="risk-bar-fill" style="width:{pct:.0f}%;background:{color}60;border-right:2px solid {color}"></div>
          </div>
        </div>""", unsafe_allow_html=True)

    # Reference profiles
    st.markdown("<div class='sec-div'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:.8rem;color:#64748B;font-family:IBM Plex Mono;text-transform:uppercase;letter-spacing:.06em;margin-bottom:.6rem'>Profils types de référence (pipeline final)</div>", unsafe_allow_html=True)

    profiles = [
        ("Sain — Agri., sans incident",          {"eng":-1,"ca":0,"imp":-1,"gel":-1,"pr":-1,"agios":0,"sect":1,"post":True}),
        ("Moyen — toutes vars à 0",              {"eng":0,"ca":0,"imp":0,"gel":0,"pr":0,"agios":0,"sect":9,"post":False}),
        ("Modéré — AGIOS + Sect 2 (post-2019)", {"eng":0,"ca":0,"imp":0,"gel":0,"pr":0,"agios":1,"sect":2,"post":True}),
        ("Élevé — impayés + prov. + Sect 2",    {"eng":0,"ca":0,"imp":2,"gel":1,"pr":1,"agios":1,"sect":2,"post":True}),
    ]
    ref_pds = [3.5, 7.2, 12.3, 26.0]   # from final pipeline output

    prof_cols = st.columns(4)
    for i, ((name, p), ref) in enumerate(zip(profiles, ref_pds)):
        pd_p, _ = calc_pd_probit(p['eng'], p['ca'], p['imp'], p['gel'],
                                   p['pr'], p['agios'], p['sect'], p['post'])
        c = "#22D3A3" if pd_p < .10 else ("#FBBF24" if pd_p < .25 else "#F87171")
        prof_cols[i].markdown(f"""<div class="card-sm" style="text-align:center;border-color:{c}30">
          <div style="font-size:.75rem;color:#64748B;margin-bottom:.4rem;line-height:1.3">{name}</div>
          <div style="font-family:Syne;font-size:1.6rem;font-weight:800;color:{c}">{pd_p:.1%}</div>
          <div style="font-family:IBM Plex Mono;font-size:.72rem;color:#475569;margin-top:.2rem">
            réf pipeline: {ref:.1f}%
          </div>
        </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  FOOTER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div style="margin-top:2.5rem;padding-top:1rem;border-top:1px solid #1E3050;
    text-align:center;font-family:IBM Plex Mono;font-size:.75rem;color:#475569;line-height:1.9">
  Stress Testing STB · Mémoire de Master ·
  Modèle satellite : logit_NPL ~ AR(1) + PIB + Chômage_lag + COVID | HAC NW | N=17 (2008-2024) | R²adj=0.744 ·
  Probit Stage 2 | AUC=0.9427 | Gini=0.8855 | N=327 571 | SECT2_post2019 ·
  EAD={EAD_TOTAL/1e6:.1f} M TND | PD_base={PD_BASELINE:.2%} | LGD=45%
</div>
""", unsafe_allow_html=True)
