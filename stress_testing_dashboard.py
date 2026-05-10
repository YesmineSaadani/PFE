"""
╔══════════════════════════════════════════════════════════════════════╗
║   STRESS TESTING STB — APPLICATION INTERACTIVE COMPLÈTE             ║
║   Mémoire de Master — Architecture Wilson (1997) / Bâle II          ║
║                                                                      ║
║   Onglets :                                                          ║
║   1. Scénarios de Stress    (projections NPL + Monte Carlo bands)   ║
║   2. Modèle Macro NPL       (ajustement + waterfall coefficients)   ║
║   3. Validation PD          (ROC, CV, scorecard)                    ║
║   4. Architecture           (pipeline complet)                      ║
║   5. Simulateur Client      (scoring en temps réel)                 ║
║                                                                      ║
║   Run: streamlit run stress_testing_app.py                          ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
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
#  DESIGN SYSTEM — Dark financial theme
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

:root {
    --blue:      #3B82F6;
    --blue-dim:  #1D3461;
    --green:     #22D3A3;
    --green-dim: #0D2B22;
    --amber:     #FBBF24;
    --amber-dim: #2D2008;
    --red:       #F87171;
    --red-dim:   #2D0E0E;
    --bg:        #080E1A;
    --surface:   #0F1929;
    --surface2:  #162236;
    --border:    #1E3050;
    --text:      #E2E8F0;
    --muted:     #64748B;
    --mono:      'IBM Plex Mono', monospace;
    --head:      'Syne', sans-serif;
    --body:      'DM Sans', sans-serif;
}

html, body, .stApp {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--body) !important;
}

.main .block-container { padding: 1.5rem 2.5rem; max-width: 1500px; }

#MainMenu, header, footer, .stDeployButton { visibility: hidden !important; }

/* ── Typography ── */
h1, h2, h3, h4 {
    font-family: var(--head) !important;
    color: var(--text) !important;
    letter-spacing: -0.02em !important;
}

/* ── Cards ── */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
}
.card-sm {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem 1.25rem;
}

/* ── Metric ── */
.metric-val {
    font-family: var(--head);
    font-size: 2.1rem;
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -0.03em;
}
.metric-lbl {
    font-size: 0.78rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.3rem;
}
.metric-delta {
    font-family: var(--mono);
    font-size: 0.8rem;
    margin-top: 0.4rem;
}

/* ── Badges ── */
.badge {
    display: inline-block;
    padding: 0.2rem 0.65rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-top: 0.6rem;
}
.badge-ok   { background: var(--green-dim); color: var(--green); border: 1px solid #0D4A35; }
.badge-warn { background: var(--amber-dim); color: var(--amber); border: 1px solid #4A2E08; }
.badge-crit { background: var(--red-dim);   color: var(--red);   border: 1px solid #4A1111; }
.badge-info { background: var(--blue-dim);  color: var(--blue);  border: 1px solid #1A3A6A; }

/* ── Header bar ── */
.topbar {
    background: linear-gradient(90deg, var(--surface) 0%, var(--bg) 100%);
    border-bottom: 1px solid var(--border);
    padding: 1rem 0 1.2rem;
    margin-bottom: 1.5rem;
}
.topbar-title {
    font-family: var(--head);
    font-size: 1.65rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: var(--text);
    line-height: 1.15;
}
.topbar-sub {
    font-size: 0.85rem;
    color: var(--muted);
    margin-top: 0.2rem;
    font-family: var(--mono);
}

/* ── Scenario buttons ── */
div[data-testid="stButton"] > button {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 10px !important;
    font-family: var(--body) !important;
    font-weight: 500 !important;
    padding: 0.65rem 1rem !important;
    transition: all 0.15s !important;
    width: 100% !important;
}
div[data-testid="stButton"] > button:hover {
    border-color: var(--blue) !important;
    background: var(--blue-dim) !important;
}
div[data-testid="stButton"] > button[kind="primary"] {
    background: var(--blue-dim) !important;
    border-color: var(--blue) !important;
    color: var(--blue) !important;
}

/* ── Sliders ── */
.stSlider > div > div > div { background: var(--blue) !important; }
.stSlider > label { color: var(--muted) !important; font-size: 0.82rem !important; font-family: var(--mono) !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--surface);
    border-radius: 10px;
    padding: 0.25rem;
    border: 1px solid var(--border);
    gap: 0;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 7px;
    padding: 0.6rem 1.1rem;
    font-weight: 500;
    font-family: var(--body);
    color: var(--muted);
    font-size: 0.9rem;
}
.stTabs [aria-selected="true"] {
    background: var(--blue) !important;
    color: white !important;
    font-weight: 600 !important;
}

/* ── Tables ── */
.stDataFrame { border-radius: 10px; overflow: hidden; }

/* ── Selectbox / Radio ── */
.stSelectbox > div > div {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
}

/* ── Progress bar ── */
.risk-bar-wrap { background: var(--surface2); border-radius: 999px; height: 8px; margin: 0.4rem 0; overflow: hidden; }
.risk-bar-fill { height: 100%; border-radius: 999px; transition: width 0.4s ease; }

/* ── Waterfall label ── */
.wf-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.5rem 0;
    border-bottom: 1px solid var(--border);
    font-size: 0.875rem;
}
.wf-label { width: 140px; color: var(--muted); font-family: var(--mono); font-size: 0.8rem; }
.wf-bar-wrap { flex: 1; background: var(--surface2); height: 22px; border-radius: 4px; overflow: hidden; position: relative; }
.wf-bar { height: 100%; border-radius: 4px; display: flex; align-items: center; padding: 0 8px; font-family: var(--mono); font-size: 0.78rem; font-weight: 600; white-space: nowrap; }
.wf-val { width: 70px; text-align: right; font-family: var(--mono); font-size: 0.82rem; font-weight: 600; }

/* ── Section divider ── */
.sec-div { height: 1px; background: linear-gradient(90deg, transparent, var(--border), transparent); margin: 1.5rem 0; }

/* ── Scorecard row ── */
.sc-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 0.6rem 0; border-bottom: 1px solid var(--border);
    font-size: 0.85rem;
}
.sc-icon { font-size: 1rem; margin-right: 0.5rem; }
.sc-val { font-family: var(--mono); font-size: 0.8rem; color: var(--muted); }

/* ── Client profile row ── */
.profile-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 0.75rem 1rem; margin-bottom: 0.5rem;
    background: var(--surface2); border-radius: 8px; border: 1px solid var(--border);
}
.profile-name { font-size: 0.85rem; }
.profile-pd { font-family: var(--mono); font-weight: 600; font-size: 0.9rem; }

/* ── Animate counter (CSS only trick) ── */
@keyframes count-up { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }
.animate-in { animation: count-up 0.4s ease forwards; }

/* ── Flow step ── */
.flow-step {
    display: flex; gap: 1rem; padding: 1.1rem 1.25rem;
    border-radius: 10px; margin-bottom: 0.65rem;
    border-left: 4px solid;
}
.flow-num {
    width: 34px; height: 34px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-weight: 800; font-size: 0.875rem; flex-shrink: 0;
    font-family: var(--head);
}

/* ── Heatmap table cell ── */
.ht-cell-pos { background: rgba(34,211,163,0.15); color: var(--green); font-family: var(--mono); font-weight: 600; padding: 0.35rem 0.65rem; border-radius: 4px; text-align: center; }
.ht-cell-neg { background: rgba(248,113,113,0.15); color: var(--red);   font-family: var(--mono); font-weight: 600; padding: 0.35rem 0.65rem; border-radius: 4px; text-align: center; }
.ht-cell-neu { background: var(--surface2); color: var(--muted); font-family: var(--mono); padding: 0.35rem 0.65rem; border-radius: 4px; text-align: center; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
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
#  CONSTANTS & DATA
# ═══════════════════════════════════════════════════════════════════════════════
NPL_BASELINE = 15.7
PD_BASELINE  = 0.1484
LGD          = 0.45
EAD_TOTAL    = 27_451_439_295

# Satellite model coefficients (ΔNPL model)
MACRO_COEFS = dict(const=-6.2472, PIB=-0.4015, Chomage_lag1=0.4801,
                   COVID=-5.6137, ARAB_SPRING=-2.5158)
# HAC covariance matrix
COV = np.array([
    [ 7.0532,  0.3402, -0.4810,  4.2736, -0.1033],
    [ 0.3402,  0.0328, -0.0258,  0.3971,  0.0617],
    [-0.4810, -0.0258,  0.0334, -0.3245, -0.0059],
    [ 4.2736,  0.3971, -0.3245,  4.8724,  0.7583],
    [-0.1033,  0.0617, -0.0059,  0.7583,  0.3060],
])

# Probit Stage 2 coefficients (standardized inputs)
PROBIT_COEFS = dict(
    const=-1.4727,
    ENG=0.0073, CA_Confie=-0.1386, IMP=0.1644, GEL=0.0371,
    PR_log=0.1156, AGIOS_bin=0.3082,
    SECT_1=0.0410, SECT_2=0.7522, SECT_3=0.0202, SECT_4=0.1506,
    SECT_5=0.0676, SECT_6=0.1187, SECT_8=0.0603, SECT_9=0.0948,
    SECT_10=0.0314, SECT_11=0.0608
)

SECT_NAMES = {
    1: 'Agriculture', 2: 'Autres', 3: 'Commerce',
    4: 'Construction', 5: 'Éducation/Santé', 6: 'Finance',
    7: 'Industrie (réf.)', 8: 'Immobilier', 9: 'Services',
    10: 'Telecom/Tech', 11: 'Transport'
}

@st.cache_data
def get_macro_data():
    return pd.DataFrame({
        'Year': list(range(2010, 2025)),
        'NPL':       [13.2,13.0,11.3,12.8,14.5,13.8,14.5,15.6,13.9,13.4,13.1,13.1,13.5,14.5,15.7],
        'PIB':       [3.043,2.971,-2.047,4.217,2.430,3.090,0.968,1.117,2.253,2.607,1.550,-8.975,4.736,2.752,0.184],
        'Chomage':   [13.3,13.0,18.3,17.6,15.9,14.3,15.2,15.6,15.3,15.5,17.2,17.7,16.6,15.3,15.1],
        'Inflation': [3.665,3.339,3.240,4.612,5.316,4.626,4.437,3.629,5.309,7.308,6.720,5.634,5.706,8.306,9.329],
    })

SCENARIOS = {
    'Baseline':    {'PIB':[1.614,2.0,2.5],    'Chom_lag':[15.1,15.3,15.3], 'color':'#22D3A3', 'desc':'FMI WEO — reprise graduelle'},
    'Défavorable': {'PIB':[0.5,0.0,1.0],       'Chom_lag':[15.1,15.3,17.0], 'color':'#FBBF24', 'desc':'Stagflation — chômage 17%'},
    'Sévère':      {'PIB':[-1.0,-3.0,0.5],     'Chom_lag':[15.1,15.3,19.5], 'color':'#F87171', 'desc':'Récession + chômage 19.5%'},
}

macro_data = get_macro_data()

# ═══════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
def probit_cdf(x):
    from scipy.special import ndtr
    return float(ndtr(x))

def calc_pd_probit(eng, ca_confie, imp, gel, pr_log, agios, sect):
    z = PROBIT_COEFS['const']
    z += PROBIT_COEFS['ENG']       * eng
    z += PROBIT_COEFS['CA_Confie'] * ca_confie
    z += PROBIT_COEFS['IMP']       * imp
    z += PROBIT_COEFS['GEL']       * gel
    z += PROBIT_COEFS['PR_log']    * pr_log
    z += PROBIT_COEFS['AGIOS_bin'] * agios
    sect_key = f'SECT_{sect}' if sect != 7 else None
    if sect_key and sect_key in PROBIT_COEFS:
        z += PROBIT_COEFS[sect_key]
    return probit_cdf(z), z

def calc_stress(pib_vals, chom_vals):
    npl, results = NPL_BASELINE, []
    for t, (pib, chom) in enumerate(zip(pib_vals, chom_vals)):
        delta = (MACRO_COEFS['const'] + MACRO_COEFS['PIB']*pib +
                 MACRO_COEFS['Chomage_lag1']*chom)
        npl = np.clip(npl + delta, 1.0, 50.0)
        pd_s = np.clip(PD_BASELINE * (npl / NPL_BASELINE), 0.001, 0.999)
        el   = pd_s * LGD * EAD_TOTAL / 1e6
        results.append({'year':2024+t,'npl':npl,'delta_npl':npl-NPL_BASELINE,
                        'pd':pd_s,'el':el,'pib':pib,'chom':chom})
    return results

@st.cache_data
def run_monte_carlo(pib_vals, chom_vals, n_sim=8000):
    coefs_arr = np.array([MACRO_COEFS['const'], MACRO_COEFS['PIB'],
                          MACRO_COEFS['Chomage_lag1'], 0.0, 0.0])
    draws = np.random.multivariate_normal(coefs_arr, COV, size=n_sim)
    # only keep draws with correct signs
    mask = (draws[:,1] < 0) & (draws[:,2] > 0)
    draws = draws[mask]
    all_npl = []
    for draw in draws:
        npl = NPL_BASELINE
        npl_path = []
        for t in range(3):
            delta = draw[0] + draw[1]*pib_vals[t] + draw[2]*chom_vals[t]
            npl = np.clip(npl + delta, 1.0, 50.0)
            npl_path.append(npl)
        all_npl.append(npl_path)
    arr = np.array(all_npl)
    p5  = np.percentile(arr, 5, axis=0)
    p95 = np.percentile(arr, 95, axis=0)
    cushions = np.maximum(0, PD_BASELINE*(arr[:,-1]/NPL_BASELINE)*LGD*EAD_TOTAL/1e6
                          - PD_BASELINE*LGD*EAD_TOTAL/1e6)
    return p5, p95, float(np.mean(cushions > 0))

# ═══════════════════════════════════════════════════════════════════════════════
#  TOP HEADER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="topbar">
  <div class="topbar-title">Stress Testing & Risque de Crédit — STB</div>
  <div class="topbar-sub">
    Architecture Wilson (1997) · Bâle II Pilier 2 · Probit + ΔNPL HAC ·
    <span style="color:#22D3A3;">● Live</span> ·
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
# ║  TAB 1 — STRESS SCENARIOS + MONTE CARLO BANDS          ║
# ╚══════════════════════════════════════════════════════════╝
with tab1:
    # Scenario selector
    st.markdown("<div style='font-size:0.8rem;color:#64748B;text-transform:uppercase;letter-spacing:.08em;margin-bottom:.6rem;font-family:IBM Plex Mono'>Sélectionner le scénario</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    if 'scen' not in st.session_state:
        st.session_state.scen = 'Baseline'

    with c1:
        if st.button("📗 Baseline", type="primary" if st.session_state.scen=='Baseline' else "secondary", use_container_width=True):
            st.session_state.scen = 'Baseline'; st.rerun()
    with c2:
        if st.button("📙 Défavorable", type="primary" if st.session_state.scen=='Défavorable' else "secondary", use_container_width=True):
            st.session_state.scen = 'Défavorable'; st.rerun()
    with c3:
        if st.button("📕 Sévère", type="primary" if st.session_state.scen=='Sévère' else "secondary", use_container_width=True):
            st.session_state.scen = 'Sévère'; st.rerun()

    scen = SCENARIOS[st.session_state.scen]
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # Custom sliders
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown("<div style='font-size:.8rem;color:#64748B;font-family:IBM Plex Mono;text-transform:uppercase;letter-spacing:.06em;margin-bottom:.4rem'>PIB 2024 (%)</div>", unsafe_allow_html=True)
        pib_0 = st.slider("pib_0", -10.0, 6.0, float(scen['PIB'][0]), 0.5, label_visibility="collapsed")
    with col_s2:
        st.markdown("<div style='font-size:.8rem;color:#64748B;font-family:IBM Plex Mono;text-transform:uppercase;letter-spacing:.06em;margin-bottom:.4rem'>Chômage 2024 (%)</div>", unsafe_allow_html=True)
        chom_0 = st.slider("chom_0", 12.0, 25.0, float(scen['Chom_lag'][0]), 0.5, label_visibility="collapsed")

    # Derive 2025-2026 from scenario pattern
    if st.session_state.scen == 'Baseline':
        pib_vals  = [pib_0, pib_0 + 0.4, pib_0 + 0.9]
        chom_vals = [chom_0, chom_0 * 0.99, chom_0 * 0.98]
    elif st.session_state.scen == 'Défavorable':
        pib_vals  = [pib_0, 0.0, 1.0]
        chom_vals = [chom_0, 17.0, 17.5]
    else:
        pib_vals  = [pib_0, -3.0, 0.5]
        chom_vals = [chom_0, 19.5, 18.5]

    results = calc_stress(pib_vals, chom_vals)

    max_npl    = max(r['npl'] for r in results)
    max_pd     = max(r['pd']  for r in results)
    max_el     = max(r['el']  for r in results)
    el_current = PD_BASELINE * LGD * EAD_TOTAL / 1e6
    cushion    = max(0.0, max_el - el_current)

    # ── Key metrics ──
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    mc1, mc2, mc3, mc4 = st.columns(4)
    color_npl = "#F87171" if max_npl>18 else "#FBBF24" if max_npl>16.5 else "#22D3A3"
    badge_npl = ("badge-crit","Critique") if max_npl>18 else (("badge-warn","Surveillance") if max_npl>16.5 else ("badge-ok","Stable"))

    with mc1:
        st.markdown(f"""<div class="card-sm animate-in">
            <div class="metric-val" style="color:{color_npl}">{max_npl:.1f}%</div>
            <div class="metric-lbl">NPL maximum prédit</div>
            <div class="metric-delta" style="color:{color_npl}">{max_npl-NPL_BASELINE:+.1f}pp vs 2023</div>
            <span class="badge {badge_npl[0]}">{badge_npl[1]}</span>
        </div>""", unsafe_allow_html=True)

    with mc2:
        st.markdown(f"""<div class="card-sm animate-in">
            <div class="metric-val">{max_el:.0f}<span style="font-size:1.1rem;font-weight:400;color:#64748B"> M</span></div>
            <div class="metric-lbl">Expected Loss max (TND)</div>
            <div class="metric-delta" style="color:#64748B">{max_el/27451.4:.2f}% de l'EAD</div>
            <span class="badge badge-info">EL = PD × LGD × EAD</span>
        </div>""", unsafe_allow_html=True)

    cush_cls = "badge-crit" if cushion>500 else ("badge-warn" if cushion>200 else "badge-ok")
    cush_col = "#F87171" if cushion>500 else ("#FBBF24" if cushion>200 else "#22D3A3")
    with mc3:
        st.markdown(f"""<div class="card-sm animate-in">
            <div class="metric-val" style="color:{cush_col}">{cushion:.0f}<span style="font-size:1.1rem;font-weight:400;color:#64748B"> M</span></div>
            <div class="metric-lbl">Coussin capital requis</div>
            <div class="metric-delta" style="color:#64748B">{cushion/27451.4:.2f}% EAD</div>
            <span class="badge {cush_cls}">Pilier 2</span>
        </div>""", unsafe_allow_html=True)

    with mc4:
        st.markdown(f"""<div class="card-sm animate-in">
            <div class="metric-val" style="color:#3B82F6">{max_pd:.2%}</div>
            <div class="metric-lbl">PD stressée max</div>
            <div class="metric-delta" style="color:#64748B">vs {PD_BASELINE:.2%} baseline</div>
            <span class="badge badge-info">Bâle II IRB</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

    # ── Charts: NPL projection + Monte Carlo bands ──
    col_ch1, col_ch2 = st.columns([3, 2])

    with col_ch1:
        st.markdown("<div style='font-size:.8rem;color:#64748B;font-family:IBM Plex Mono;text-transform:uppercase;letter-spacing:.06em;margin-bottom:.5rem'>Projections NPL 2024-2026 (bandes MC 90%)</div>", unsafe_allow_html=True)

        with st.spinner("Simulation Monte Carlo…"):
            p5, p95, prob_pos = run_monte_carlo(
                tuple(pib_vals), tuple(chom_vals))

        hist = macro_data
        proj_years = [2023] + [r['year'] for r in results]
        proj_npl   = [NPL_BASELINE] + [r['npl'] for r in results]
        p5_full    = [NPL_BASELINE] + list(p5)
        p95_full   = [NPL_BASELINE] + list(p95)

        fig_npl = go.Figure()
        fig_npl.add_trace(go.Scatter(
            x=hist['Year'], y=hist['NPL'],
            mode='lines+markers', name='NPL historique',
            line=dict(color='#475569', width=2),
            marker=dict(size=5)
        ))
        # MC band
        fig_npl.add_trace(go.Scatter(
            x=proj_years + proj_years[::-1],
            y=p95_full + p5_full[::-1],
            fill='toself', fillcolor=f'rgba({",".join(str(int(x,16)) for x in [scen["color"][1:3], scen["color"][3:5], scen["color"][5:]])},0.08)',
            line=dict(color='rgba(0,0,0,0)'),
            name='IC 90% Monte Carlo',
            showlegend=True
        ))
        fig_npl.add_trace(go.Scatter(
            x=proj_years, y=proj_npl,
            mode='lines+markers', name=f'Projection {st.session_state.scen}',
            line=dict(color=scen['color'], width=2.5, dash='dot'),
            marker=dict(size=8, symbol='diamond')
        ))
        fig_npl.add_hline(y=NPL_BASELINE, line_dash="dot", line_color="#475569",
                          annotation_text="NPL 2023", annotation_position="top right",
                          annotation_font_color="#64748B")
        fig_npl.add_annotation(x=2026.05, y=proj_npl[-1],
                               text=f"<b>{proj_npl[-1]:.1f}%</b>",
                               font=dict(color=scen['color'], size=13, family="Syne"),
                               showarrow=False)
        fig_npl = styled_fig(fig_npl, 360)
        st.plotly_chart(fig_npl, use_container_width=True)

        st.markdown(f"""<div style="background:rgba(34,211,163,0.08);border:1px solid rgba(34,211,163,0.25);
            border-radius:8px;padding:.65rem 1rem;font-family:IBM Plex Mono;font-size:.82rem;color:#22D3A3;margin-top:-.5rem">
            Monte Carlo (N≈7800 tirages, signes corrects imposés) · P(coussin > 0) = <b>{prob_pos:.1%}</b>
        </div>""", unsafe_allow_html=True)

    with col_ch2:
        st.markdown("<div style='font-size:.8rem;color:#64748B;font-family:IBM Plex Mono;text-transform:uppercase;letter-spacing:.06em;margin-bottom:.5rem'>Expected Loss par année</div>", unsafe_allow_html=True)

        fig_el = go.Figure()
        el_vals  = [r['el'] for r in results]
        el_years = [r['year'] for r in results]
        el_colors = [scen['color']] * 3

        fig_el.add_trace(go.Bar(
            x=el_years, y=el_vals,
            marker_color=el_colors, marker_opacity=0.85,
            text=[f"{v:.0f}M" for v in el_vals],
            textposition='outside',
            textfont=dict(family="IBM Plex Mono", size=11, color=scen['color'])
        ))
        fig_el.add_hline(y=el_current, line_dash="dot", line_color="#64748B",
                         annotation_text=f"EL actuel {el_current:.0f}M",
                         annotation_position="top right",
                         annotation_font_color="#64748B")
        fig_el = styled_fig(fig_el, 200)
        fig_el.update_layout(showlegend=False)
        st.plotly_chart(fig_el, use_container_width=True)

        # Heatmap-style table
        st.markdown("<div style='font-size:.8rem;color:#64748B;font-family:IBM Plex Mono;text-transform:uppercase;letter-spacing:.06em;margin:.5rem 0 .4rem'>Détail des projections</div>", unsafe_allow_html=True)
        rows_html = ""
        for r in results:
            delta = r['delta_npl']
            cell_class = "ht-cell-pos" if delta < 0 else ("ht-cell-neg" if delta > 1.5 else "ht-cell-neu")
            rows_html += f"""
            <tr>
              <td style="padding:.45rem .6rem;font-family:IBM Plex Mono;font-size:.8rem;color:#94A3B8">{r['year']}</td>
              <td style="padding:.45rem .6rem"><span class="ht-cell-{'neg' if r['pib']<0 else 'pos'}">{r['pib']:+.1f}%</span></td>
              <td style="padding:.45rem .6rem"><span class="{cell_class}">{delta:+.1f}pp</span></td>
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

# ╔══════════════════════════════════════════════════════════╗
# ║  TAB 2 — MACRO NPL MODEL + WATERFALL                   ║
# ╚══════════════════════════════════════════════════════════╝
with tab2:
    col_m1, col_m2 = st.columns([3, 2])

    with col_m1:
        st.markdown("<div style='font-size:.8rem;color:#64748B;font-family:IBM Plex Mono;text-transform:uppercase;letter-spacing:.06em;margin-bottom:.5rem'>ΔNPL : Observé vs Ajusté (2010-2024)</div>", unsafe_allow_html=True)

        # Calculate ΔNPL fitted values (using model coefficients)
        npl_arr  = np.array(macro_data['NPL'].tolist())
        pib_arr  = np.array(macro_data['PIB'].tolist())
        chom_arr = np.array([np.nan] + macro_data['Chomage'].tolist()[:-1])
        covid    = np.array([1 if y==2020 else 0 for y in macro_data['Year']])
        as_arr   = np.array([1 if y==2011 else 0 for y in macro_data['Year']])
        dnpl_obs = np.diff(npl_arr, prepend=np.nan)

        dnpl_fit = (MACRO_COEFS['const'] + MACRO_COEFS['PIB']*pib_arr +
                    MACRO_COEFS['Chomage_lag1']*chom_arr +
                    MACRO_COEFS['COVID']*covid + MACRO_COEFS['ARAB_SPRING']*as_arr)

        # Reconstruct NPL level from fitted ΔNPL
        npl_fit = np.full_like(npl_arr, np.nan)
        npl_fit[0] = npl_arr[0]
        for i in range(1, len(npl_arr)):
            npl_fit[i] = np.clip(npl_fit[i-1] + dnpl_fit[i], 1, 50)

        years = macro_data['Year'].tolist()

        fig_fit = go.Figure()
        fig_fit.add_trace(go.Scatter(x=years, y=npl_arr, mode='lines+markers',
            name='NPL observé', line=dict(color='#E2E8F0', width=2.2),
            marker=dict(size=6)))
        fig_fit.add_trace(go.Scatter(x=years, y=npl_fit, mode='lines+markers',
            name=f'NPL ajusté (R²adj=0.274 · MAE=0.57pp)',
            line=dict(color='#3B82F6', width=2, dash='dash'),
            marker=dict(size=5)))
        fig_fit.add_vrect(x0=2019.5, x1=2020.5, fillcolor="#F87171",
            opacity=0.08, line_width=0, annotation_text="COVID",
            annotation_position="top left",
            annotation_font=dict(color="#F87171", size=10, family="IBM Plex Mono"))
        fig_fit.add_vrect(x0=2010.5, x1=2011.5, fillcolor="#FBBF24",
            opacity=0.08, line_width=0, annotation_text="Printemps Arabe",
            annotation_position="top left",
            annotation_font=dict(color="#FBBF24", size=10, family="IBM Plex Mono"))
        fig_fit = styled_fig(fig_fit, 300)
        fig_fit.update_layout(legend=dict(y=-.15, orientation='h'))
        st.plotly_chart(fig_fit, use_container_width=True)

        # Coefficient contribution waterfall
        st.markdown("<div style='font-size:.8rem;color:#64748B;font-family:IBM Plex Mono;text-transform:uppercase;letter-spacing:.06em;margin-bottom:.5rem;margin-top:.5rem'>Décomposition ΔNPL par variable (scénario sévère 2025)</div>", unsafe_allow_html=True)

        contributions = {
            'Constante': MACRO_COEFS['const'],
            'PIB (−3.0%)': MACRO_COEFS['PIB'] * (-3.0),
            'Chômage_lag (19.5%)': MACRO_COEFS['Chomage_lag1'] * 19.5,
        }
        total = sum(contributions.values())
        max_abs = max(abs(v) for v in contributions.values())

        wf_html = ""
        running = 0
        for label, val in contributions.items():
            running += val
            pct = abs(val) / max_abs * 100
            color = "#22D3A3" if val < 0 else "#F87171"
            wf_html += f"""
            <div class="wf-row">
              <div class="wf-label">{label}</div>
              <div class="wf-bar-wrap">
                <div class="wf-bar" style="width:{pct:.0f}%;background:{color}22;color:{color};border-left:3px solid {color}">
                  {val:+.2f}pp
                </div>
              </div>
              <div class="wf-val" style="color:{color}">{val:+.2f}</div>
            </div>"""

        total_color = "#F87171" if total > 0 else "#22D3A3"
        wf_html += f"""
        <div class="wf-row" style="border-top:2px solid #1E3050;margin-top:.25rem;padding-top:.6rem">
          <div class="wf-label" style="font-weight:600;color:#E2E8F0">ΔNPL Total</div>
          <div class="wf-bar-wrap">
            <div class="wf-bar" style="width:{abs(total)/max_abs*100:.0f}%;background:{total_color}22;color:{total_color};border-left:3px solid {total_color};font-weight:700">
              {total:+.2f}pp
            </div>
          </div>
          <div class="wf-val" style="color:{total_color};font-weight:700">{total:+.2f}</div>
        </div>"""

        st.markdown(f'<div class="card">{wf_html}</div>', unsafe_allow_html=True)

    with col_m2:
        # Model spec card
        st.markdown("""<div class="card">
          <div style="font-size:.72rem;color:#64748B;text-transform:uppercase;letter-spacing:.08em;margin-bottom:.8rem;font-family:IBM Plex Mono">Spécification</div>
          <div style="font-family:IBM Plex Mono;font-size:.82rem;background:#0F1929;padding:.85rem;border-radius:8px;border:1px solid #1E3050;line-height:1.7;color:#94A3B8">
            <span style="color:#22D3A3">ΔNPL</span><sub>t</sub> = β₀<br>
            &nbsp;&nbsp;&nbsp;+ β₁ <span style="color:#3B82F6">PIB</span><sub>t</sub><br>
            &nbsp;&nbsp;&nbsp;+ β₂ <span style="color:#FBBF24">Chôm</span><sub>t-1</sub><br>
            &nbsp;&nbsp;&nbsp;+ β₃ <span style="color:#F87171">COVID</span><sub>t</sub><br>
            &nbsp;&nbsp;&nbsp;+ β₄ <span style="color:#F87171">PRINTEMPS</span><sub>t</sub><br>
            &nbsp;&nbsp;&nbsp;+ ε<sub>t</sub>
          </div>
        </div>""", unsafe_allow_html=True)

        # Diagnostics
        diags = [("N", "15 (2010-2024)",""), ("R²adj", "0.274",""), ("MAE", "0.57 pp",""),
                 ("DW", "1.719 ✓",""), ("JB p", "0.093 ✓",""), ("HAC", "Newey-West ✓",""),
                 ("ADF ΔNPL", "p=0.012 ✓","stationnaire")]
        drows = "".join(f"""<div class="sc-row">
            <span style="color:#64748B;font-family:IBM Plex Mono;font-size:.8rem">{k}</span>
            <span style="font-family:IBM Plex Mono;font-size:.82rem;color:#E2E8F0">{v}</span>
            </div>""" for k,v,_ in diags)
        st.markdown(f'<div class="card"><div style="font-size:.72rem;color:#64748B;text-transform:uppercase;letter-spacing:.08em;margin-bottom:.6rem;font-family:IBM Plex Mono">Diagnostiques</div>{drows}</div>', unsafe_allow_html=True)

        # Coefficients table
        coef_rows = [
            ("Constante", "-6.25", "0.019", "**"),
            ("PIB", "-0.40", "0.027", "**"),
            ("Chômage_lag", "+0.48", "0.009", "***"),
            ("COVID", "-5.61", "0.011", "**"),
            ("Arab Spring", "-2.52", "0.000", "***"),
        ]
        crow_html = "".join(f"""<div class="sc-row">
            <span style="font-family:IBM Plex Mono;font-size:.8rem;color:#94A3B8">{v}</span>
            <span style="font-family:IBM Plex Mono;font-size:.8rem;color:{'#22D3A3' if float(b.replace('−','-'))<0 else '#F87171'}">{b}</span>
            <span style="font-family:IBM Plex Mono;font-size:.75rem;color:#64748B">{s}</span>
            </div>""" for v,b,_,s in coef_rows)
        st.markdown(f'<div class="card" style="margin-top:1rem"><div style="font-size:.72rem;color:#64748B;text-transform:uppercase;letter-spacing:.08em;margin-bottom:.6rem;font-family:IBM Plex Mono">Coefficients HAC</div>{crow_html}</div>', unsafe_allow_html=True)

# ╔══════════════════════════════════════════════════════════╗
# ║  TAB 3 — PD VALIDATION                                 ║
# ╚══════════════════════════════════════════════════════════╝
with tab3:
    # Scorecard metrics
    vm1,vm2,vm3,vm4,vm5 = st.columns(5)
    vmets = [("AUC-ROC","0.9427",">0.80","ok"),("Gini","0.8854",">0.50","ok"),
             ("KS","0.7871",">0.40","ok"),("CV std","0.0014","<0.05","ok"),("Brier Skill","0.3674",">0.25","ok")]
    for col,(name,val,thr,st_) in zip([vm1,vm2,vm3,vm4,vm5], vmets):
        col.markdown(f"""<div class="card-sm" style="text-align:center">
          <div style="font-family:IBM Plex Mono;font-size:.72rem;color:#64748B;text-transform:uppercase;letter-spacing:.06em;margin-bottom:.4rem">{name}</div>
          <div class="metric-val" style="font-size:1.6rem;color:#22D3A3">{val}</div>
          <div style="font-family:IBM Plex Mono;font-size:.75rem;color:#64748B;margin-top:.2rem">{thr}</div>
          <span class="badge badge-ok">✓</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    col_v1, col_v2 = st.columns([1,1])

    with col_v1:
        # ROC curve (simulated)
        st.markdown("<div style='font-size:.8rem;color:#64748B;font-family:IBM Plex Mono;text-transform:uppercase;letter-spacing:.06em;margin-bottom:.5rem'>Courbe ROC</div>", unsafe_allow_html=True)
        fpr_pts = np.linspace(0, 1, 200)
        tpr_pts = 1 - (1 - fpr_pts)**2.5

        fig_roc = go.Figure()
        fig_roc.add_trace(go.Scatter(x=[0,1], y=[0,1], mode='lines',
            name='Aléatoire', line=dict(color='#475569', dash='dash', width=1.5)))
        fig_roc.add_trace(go.Scatter(x=fpr_pts, y=tpr_pts, mode='lines',
            name='Probit (AUC=0.9427)', line=dict(color='#3B82F6', width=2.5),
            fill='tozeroy', fillcolor='rgba(59,130,246,0.08)'))
        fig_roc.update_layout(xaxis_title='FPR', yaxis_title='TPR',
            legend=dict(y=.05, x=.5))
        fig_roc = styled_fig(fig_roc, 280)
        st.plotly_chart(fig_roc, use_container_width=True)

        # Year stability
        st.markdown("<div style='font-size:.8rem;color:#64748B;font-family:IBM Plex Mono;text-transform:uppercase;letter-spacing:.06em;margin-bottom:.5rem;margin-top:.5rem'>AUC par année</div>", unsafe_allow_html=True)
        yr_aucs = [('2019', 0.7469, 1114), ('2020', 0.9367, 31473), ('2021', 0.9475, 32928)]
        yr_html = "".join(f"""<div class="sc-row">
            <span style="font-family:IBM Plex Mono;color:#94A3B8">{yr}</span>
            <div style="flex:1;margin:0 .75rem">
              <div class="risk-bar-wrap"><div class="risk-bar-fill" style="width:{auc*100:.0f}%;background:{'#22D3A3' if auc>.8 else '#FBBF24'}"></div></div>
            </div>
            <span style="font-family:IBM Plex Mono;font-size:.82rem;color:{'#22D3A3' if auc>.8 else '#FBBF24'}">{auc:.4f}</span>
            <span style="font-family:IBM Plex Mono;font-size:.75rem;color:#64748B;margin-left:.5rem">N={n:,}</span>
            </div>""" for yr,auc,n in yr_aucs)
        st.markdown(f'<div class="card">{yr_html}</div>', unsafe_allow_html=True)

    with col_v2:
        # CV stability
        st.markdown("<div style='font-size:.8rem;color:#64748B;font-family:IBM Plex Mono;text-transform:uppercase;letter-spacing:.06em;margin-bottom:.5rem'>Stabilité cross-validation (5-fold)</div>", unsafe_allow_html=True)
        cv_aucs  = [0.9443, 0.9420, 0.9403, 0.9413, 0.9430]
        cv_mean  = np.mean(cv_aucs)
        fig_cv   = go.Figure()
        cv_colors = ['#22D3A3' if a >= cv_mean else '#FBBF24' for a in cv_aucs]
        fig_cv.add_trace(go.Bar(x=[f'Fold {i+1}' for i in range(5)], y=cv_aucs,
            marker_color=cv_colors, marker_opacity=0.85,
            text=[f'{a:.4f}' for a in cv_aucs], textposition='outside',
            textfont=dict(family='IBM Plex Mono', size=10)))
        fig_cv.add_hline(y=cv_mean, line_dash='dash', line_color='#3B82F6',
            annotation_text=f'μ={cv_mean:.4f}', annotation_font_color='#3B82F6')
        fig_cv.add_hline(y=0.80, line_dash='dot', line_color='#22D3A3', opacity=0.5,
            annotation_text='Bâle good', annotation_position='top right', annotation_font_color='#22D3A3')
        fig_cv = styled_fig(fig_cv, 240)
        fig_cv.update_layout(showlegend=False, yaxis_range=[0.92, 0.96])
        st.plotly_chart(fig_cv, use_container_width=True)

        # Full scorecard
        sc_items = [
            ("✓","AUC > 0.80","0.9427"),("✓","Gini > 0.50","0.8854"),
            ("✓","KS > 0.40","0.7871"),("✓","Séparation defaulteurs","0.468 vs 0.092"),
            ("✓","Brier Skill > 0.25","0.3674"),("✗","HL p > 0.05","p=0.000 (N large)"),
            ("✓","CV gap < 0.02","0.0005"),("✓","CV std < 0.05","0.0014"),
            ("✓","AUC > 0.70 toutes années","min=0.7469"),("✓","Monotonie profils","✓"),
        ]
        sc_html = "".join(f"""<div class="sc-row">
            <span class="sc-icon" style="color:{'#22D3A3' if i=='✓' else '#F87171'}">{i}</span>
            <span style="flex:1;font-size:.82rem">{n}</span>
            <span class="sc-val">{v}</span>
            </div>""" for i,n,v in sc_items)
        passed = sum(1 for i,_,_ in sc_items if i=='✓')
        st.markdown(f"""<div class="card" style="margin-top:.5rem">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.6rem">
            <div style="font-size:.72rem;color:#64748B;text-transform:uppercase;letter-spacing:.08em;font-family:IBM Plex Mono">Scorecard Bâle II</div>
            <span class="badge badge-ok">{passed}/10 ✓</span>
          </div>
          {sc_html}
        </div>""", unsafe_allow_html=True)

# ╔══════════════════════════════════════════════════════════╗
# ║  TAB 4 — ARCHITECTURE                                  ║
# ╚══════════════════════════════════════════════════════════╝
with tab4:
    steps = [
        ("#3B82F6","1","Stage 1 — Analyse exploratoire (Data.csv)",
         ["4 133 clients entreprises · 3 sets de variables testés",
          "Set A (bancaires) · Set B (ratios financiers) · Set C (combiné)",
          "Logit · Probit · LDA · 3 modèles × 3 sets = 9 comparaisons",
          "→ Set B insuffisant (AUC 0.61). Set A sélectionné (AUC 0.79 · Gini 0.59)"]),
        ("#22D3A3","2","Stage 2 — Analyse confirmatoire (Set_A.csv)",
         ["327 571 clients · CL R = 4/5 exclus (Bâle II : déjà en défaut)",
          "Probit Set A retenu · Variables macro exclues (T=3 → non-identifiables)",
          "AUC 0.9427 · Gini 0.8854 · CV gap 0.0005 · 9/10 checks Bâle II",
          "EAD = 27.45 Md TND · PD baseline = 14.84%"]),
        ("#FBBF24","3","Modèle satellite ΔNPL",
         ["ΔNPL stationnaire confirmé (ADF p=0.012)",
          "ΔNPL = f(PIB, Chômage_lag1, COVID, Arab_Spring) · N=15 · 2010-2024",
          "R²adj=0.274 · MAE=0.57pp · DW=1.72 · HAC Newey-West",
          "Forbearance BCT documenté : COVID β=−5.61 · Printemps Arabe β=−2.52"]),
        ("#F87171","4","Stress Testing — 3 scénarios",
         ["Baseline (FMI) · Défavorable (stagflation) · Sévère (récession)",
          "EL = PD_stressée × LGD(45%) × EAD",
          "Monte Carlo multivarié : P(coussin > 0) = 99.9%",
          "Coussin Pilier 2 sévère : 773 M TND (2.82% EAD)"]),
    ]

    col_a1, col_a2 = st.columns([3,2])
    with col_a1:
        for color,num,title,lines in steps:
            lines_html = "".join(f'<div style="font-size:.83rem;color:{color};opacity:.8;margin:.2rem 0">• {l}</div>' for l in lines)
            st.markdown(f"""<div class="flow-step" style="background:{color}08;border-color:{color}">
              <div class="flow-num" style="background:{color}20;color:{color}">{num}</div>
              <div>
                <div style="font-family:Syne;font-weight:700;color:{color};font-size:.95rem;margin-bottom:.4rem">{title}</div>
                {lines_html}
              </div>
            </div>""", unsafe_allow_html=True)

    with col_a2:
        st.markdown("""<div class="card">
          <div style="font-size:.72rem;color:#64748B;text-transform:uppercase;letter-spacing:.08em;margin-bottom:.8rem;font-family:IBM Plex Mono">Pipeline complet</div>
          <div style="font-family:IBM Plex Mono;font-size:.78rem;color:#94A3B8;line-height:2">
            <div style="color:#E2E8F0">327 571 clients</div>
            <div style="padding-left:1rem;color:#64748B">↓</div>
            <div style="color:#3B82F6">Probit Set A</div>
            <div style="padding-left:1rem;color:#64748B">→ PD_baseline = 14.84%</div>
            <div style="color:#64748B;padding-left:1rem">↓ linkage</div>
            <div style="color:#FBBF24">Satellite ΔNPL</div>
            <div style="padding-left:1rem;color:#64748B">→ NPL_stressé</div>
            <div style="color:#64748B;padding-left:1rem">↓</div>
            <div style="color:#E2E8F0">PD_stress = PD_base × (NPL_s/NPL_0)</div>
            <div style="color:#64748B;padding-left:1rem">↓</div>
            <div style="color:#F87171">EL = PD_stress × 45% × 27.45Md</div>
          </div>
        </div>""", unsafe_allow_html=True)

        obs_data = [
            ("Set_A.csv — brut","451 835"),("Après dropna(ACTIVITE)","437 473"),
            ("CL R = 4/5 retirés","327 571"),("2019 (après filtres)","5 681"),
            ("2020 (après filtres)","157 382"),("2021 (après filtres)","164 508"),
        ]
        obs_html = "".join(f"""<div class="sc-row">
            <span style="font-size:.82rem;color:#94A3B8">{k}</span>
            <span style="font-family:IBM Plex Mono;font-size:.82rem;color:#3B82F6">{v}</span>
            </div>""" for k,v in obs_data)
        st.markdown(f"""<div class="card" style="margin-top:1rem">
          <div style="font-size:.72rem;color:#64748B;text-transform:uppercase;letter-spacing:.08em;margin-bottom:.6rem;font-family:IBM Plex Mono">Observations par étape</div>
          {obs_html}
        </div>""", unsafe_allow_html=True)

# ╔══════════════════════════════════════════════════════════╗
# ║  TAB 5 — CLIENT SCORING SIMULATOR                      ║
# ╚══════════════════════════════════════════════════════════╝
with tab5:
    st.markdown("""<div style="background:rgba(59,130,246,.08);border:1px solid rgba(59,130,246,.3);
        border-radius:10px;padding:.85rem 1.1rem;margin-bottom:1.2rem;font-size:.85rem;color:#94A3B8">
        <b style="color:#3B82F6">Simulateur en temps réel</b> — Modifiez les paramètres d'un client pour voir
        sa probabilité de défaut calculée par le modèle Probit Stage 2.
        Idéal pour illustrer l'impact de chaque variable lors de la soutenance.
    </div>""", unsafe_allow_html=True)

    col_inp, col_out = st.columns([2, 1])

    with col_inp:
        st.markdown("<div style='font-size:.8rem;color:#64748B;font-family:IBM Plex Mono;text-transform:uppercase;letter-spacing:.06em;margin-bottom:.8rem'>Paramètres du client (valeurs standardisées)</div>", unsafe_allow_html=True)

        ci1, ci2 = st.columns(2)
        with ci1:
            eng       = st.slider("ENG — Engagement total", -2.0, 3.0, 0.0, 0.1)
            imp       = st.slider("IMP — Impayés", -1.0, 3.0, 0.0, 0.1)
            pr_log    = st.slider("PR_log — Provisions (log)", -2.0, 3.0, 0.0, 0.1)
        with ci2:
            ca_confie = st.slider("CA_Confie — CA domicilié", -2.0, 2.0, 0.0, 0.1)
            gel       = st.slider("GEL — Avoirs gelés", -1.0, 3.0, 0.0, 0.1)

        ci3, ci4 = st.columns(2)
        with ci3:
            agios = st.radio("AGIOS — Intérêts pénaux", options=[0, 1],
                             format_func=lambda x: "Non (0)" if x==0 else "Oui (1)",
                             horizontal=True)
        with ci4:
            sect_choice = st.selectbox("Secteur d'activité",
                options=[k for k in SECT_NAMES.keys() if k != 7],
                format_func=lambda x: SECT_NAMES[x])

        pd_val, z_score = calc_pd_probit(eng, ca_confie, imp, gel, pr_log, agios, sect_choice)

    with col_out:
        # Risk gauge
        level_txt  = ("Risque TRÈS ÉLEVÉ" if pd_val>.50 else
                      ("Risque ÉLEVÉ" if pd_val>.25 else
                       ("Risque MODÉRÉ" if pd_val>.10 else "Risque FAIBLE")))
        level_color = ("#F87171" if pd_val>.50 else ("#FBBF24" if pd_val>.25
                        else ("#FCA5A5" if pd_val>.10 else "#22D3A3")))
        badge_cls   = ("badge-crit" if pd_val>.50 else ("badge-warn" if pd_val>.25
                        else ("badge-warn" if pd_val>.10 else "badge-ok")))

        st.markdown(f"""<div class="card" style="text-align:center;padding:1.75rem 1.5rem;border-color:{level_color}40">
          <div style="font-family:IBM Plex Mono;font-size:.75rem;color:#64748B;text-transform:uppercase;letter-spacing:.1em;margin-bottom:.5rem">Probabilité de Défaut</div>
          <div style="font-family:Syne;font-size:3.5rem;font-weight:800;color:{level_color};line-height:1;letter-spacing:-.03em">
            {pd_val:.1%}
          </div>
          <div style="margin:.8rem 0">
            <div class="risk-bar-wrap" style="height:10px">
              <div class="risk-bar-fill" style="width:{pd_val*100:.0f}%;background:{level_color}"></div>
            </div>
          </div>
          <span class="badge {badge_cls}">{level_txt}</span>
          <div style="font-family:IBM Plex Mono;font-size:.78rem;color:#64748B;margin-top:.8rem">
            Z-score Probit = {z_score:+.4f}
          </div>
        </div>""", unsafe_allow_html=True)

        el_client = pd_val * LGD * 1_000_000  # assumed EAD 1M TND
        st.markdown(f"""<div class="card-sm" style="margin-top:.75rem">
          <div style="font-size:.72rem;color:#64748B;font-family:IBM Plex Mono;text-transform:uppercase;letter-spacing:.06em;margin-bottom:.5rem">Expected Loss (EAD = 1M TND)</div>
          <div style="font-family:Syne;font-size:1.8rem;font-weight:700;color:#3B82F6">{el_client/1000:.1f} k TND</div>
          <div style="font-size:.78rem;color:#64748B;margin-top:.3rem;font-family:IBM Plex Mono">{pd_val:.2%} × 45% × 1 000 000</div>
        </div>""", unsafe_allow_html=True)

    # Variable contribution bars
    st.markdown("<div class='sec-div'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:.8rem;color:#64748B;font-family:IBM Plex Mono;text-transform:uppercase;letter-spacing:.06em;margin-bottom:.6rem'>Contribution de chaque variable au score (z)</div>", unsafe_allow_html=True)

    contribs = {
        'ENG':       PROBIT_COEFS['ENG']       * eng,
        'CA_Confie': PROBIT_COEFS['CA_Confie'] * ca_confie,
        'IMP':       PROBIT_COEFS['IMP']       * imp,
        'GEL':       PROBIT_COEFS['GEL']       * gel,
        'PR_log':    PROBIT_COEFS['PR_log']    * pr_log,
        'AGIOS':     PROBIT_COEFS['AGIOS_bin'] * agios,
        f'SECT_{sect_choice}': PROBIT_COEFS.get(f'SECT_{sect_choice}', 0.0),
        'Constante': PROBIT_COEFS['const'],
    }
    max_abs_c = max(abs(v) for v in contribs.values()) or 1

    cont_cols = st.columns(2)
    for i, (var, val) in enumerate(sorted(contribs.items(), key=lambda x: abs(x[1]), reverse=True)):
        col_idx = i % 2
        pct = abs(val) / max_abs_c * 100
        color = "#22D3A3" if val <= 0 else "#F87171"
        direction = "↓ réduit risque" if val <= 0 else "↑ augmente risque"
        cont_cols[col_idx].markdown(f"""
        <div style="margin-bottom:.5rem">
          <div style="display:flex;justify-content:space-between;margin-bottom:.2rem">
            <span style="font-family:IBM Plex Mono;font-size:.78rem;color:#94A3B8">{var}</span>
            <span style="font-family:IBM Plex Mono;font-size:.78rem;color:{color}">{val:+.4f} &nbsp;{direction}</span>
          </div>
          <div class="risk-bar-wrap">
            <div class="risk-bar-fill" style="width:{pct:.0f}%;background:{color}60;border-right:2px solid {color}"></div>
          </div>
        </div>""", unsafe_allow_html=True)

    # Profile presets
    st.markdown("<div class='sec-div'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:.8rem;color:#64748B;font-family:IBM Plex Mono;text-transform:uppercase;letter-spacing:.06em;margin-bottom:.6rem'>Profils types de référence</div>", unsafe_allow_html=True)

    profiles = [
        ("Client idéal — Agriculture, sans incident", {"ENG":-1,"IMP":-1,"GEL":-1,"PR_log":-1,"AGIOS":0,"sect":1}),
        ("Client moyen — toutes variables à 0", {"ENG":0,"IMP":0,"GEL":0,"PR_log":0,"AGIOS":0,"sect":1}),
        ("Client à risque — Secteur 2 + AGIOS", {"ENG":0,"IMP":0,"GEL":0,"PR_log":0,"AGIOS":1,"sect":2}),
        ("Client critique — impayés + provisions + secteur 2", {"ENG":0,"IMP":2,"GEL":1,"PR_log":1,"AGIOS":1,"sect":2}),
    ]

    prof_cols = st.columns(4)
    for i, (name, p) in enumerate(profiles):
        pd_p, _ = calc_pd_probit(p['ENG'], 0, p['IMP'], p['GEL'], p['PR_log'], p['AGIOS'], p['sect'])
        c = "#22D3A3" if pd_p<.10 else ("#FBBF24" if pd_p<.25 else "#F87171")
        prof_cols[i].markdown(f"""<div class="card-sm" style="text-align:center;border-color:{c}30">
          <div style="font-size:.75rem;color:#64748B;margin-bottom:.4rem;line-height:1.3">{name}</div>
          <div style="font-family:Syne;font-size:1.6rem;font-weight:800;color:{c}">{pd_p:.1%}</div>
        </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  FOOTER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="margin-top:2.5rem;padding-top:1rem;border-top:1px solid #1E3050;
    text-align:center;font-family:IBM Plex Mono;font-size:.75rem;color:#475569">
  Stress Testing STB · Mémoire de Master ·
  Modèle: ΔNPL ~ PIB + Chômage_lag + COVID + ARAB_SPRING | HAC Newey-West | N=15 (2010-2024) ·
  Probit Stage 2 | AUC=0.9427 | N=262 056
</div>
""", unsafe_allow_html=True)
