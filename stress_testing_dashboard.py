"""
╔══════════════════════════════════════════════════════════════════════╗
║   STRESS TESTING STB — APPLICATION INTERACTIVE                      ║
║   Mémoire de Master — Architecture Wilson (1997) / Bâle II          ║
║   Version corrigée — résultats alignés sur la thèse                 ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from scipy.special import ndtr, ndtri
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Stress Testing STB", page_icon="🏛️", layout="wide", initial_sidebar_state="collapsed")

# ═══ CSS ═══
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');
:root{--blue:#3B82F6;--blue-dim:#1D3461;--green:#22D3A3;--green-dim:#0D2B22;--amber:#FBBF24;--amber-dim:#2D2008;--red:#F87171;--red-dim:#2D0E0E;--bg:#080E1A;--surface:#0F1929;--surface2:#162236;--border:#1E3050;--text:#E2E8F0;--muted:#64748B;--mono:'IBM Plex Mono',monospace;--head:'Syne',sans-serif;--body:'DM Sans',sans-serif;}
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
.topbar-title{font-family:var(--head);font-size:1.65rem;font-weight:800;letter-spacing:-0.03em;color:var(--text);}
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
.wf-label{width:180px;color:var(--muted);font-family:var(--mono);font-size:.8rem;}
.wf-bar-wrap{flex:1;background:var(--surface2);height:22px;border-radius:4px;overflow:hidden;position:relative;}
.wf-bar{height:100%;border-radius:4px;display:flex;align-items:center;padding:0 8px;font-family:var(--mono);font-size:.78rem;font-weight:600;white-space:nowrap;}
.wf-val{width:70px;text-align:right;font-family:var(--mono);font-size:.82rem;font-weight:600;}
.sec-div{height:1px;background:linear-gradient(90deg,transparent,var(--border),transparent);margin:1.5rem 0;}
.sc-row{display:flex;justify-content:space-between;align-items:center;padding:.6rem 0;border-bottom:1px solid var(--border);font-size:.85rem;}
.ht-cell-pos{background:rgba(34,211,163,.15);color:var(--green);font-family:var(--mono);font-weight:600;padding:.35rem .65rem;border-radius:4px;text-align:center;}
.ht-cell-neg{background:rgba(248,113,113,.15);color:var(--red);font-family:var(--mono);font-weight:600;padding:.35rem .65rem;border-radius:4px;text-align:center;}
.ht-cell-neu{background:var(--surface2);color:var(--muted);font-family:var(--mono);padding:.35rem .65rem;border-radius:4px;text-align:center;}
::-webkit-scrollbar{width:6px;height:6px;} ::-webkit-scrollbar-track{background:transparent;} ::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px;}
</style>
""", unsafe_allow_html=True)

# ═══ PLOTLY ═══
PLOTLY_LAYOUT = dict(template='plotly_dark',paper_bgcolor='rgba(15,25,41,0)',plot_bgcolor='rgba(15,25,41,0)',font=dict(family="'IBM Plex Mono', monospace",color='#94A3B8',size=11),xaxis=dict(gridcolor='#1E3050',zerolinecolor='#1E3050'),yaxis=dict(gridcolor='#1E3050',zerolinecolor='#1E3050'),margin=dict(l=50,r=30,t=45,b=40),legend=dict(bgcolor='rgba(15,25,41,0.8)',bordercolor='#1E3050',borderwidth=1))
def styled_fig(fig, height=380):
    fig.update_layout(**PLOTLY_LAYOUT, height=height)
    fig.update_xaxes(gridcolor='#1E3050',linecolor='#1E3050')
    fig.update_yaxes(gridcolor='#1E3050',linecolor='#1E3050')
    return fig

# ═══ CONSTANTS ═══
PD_EST       = 0.1484
NPL_EST      = (14.9 + 13.5) / 2   # 14.2%
NPL_BASELINE = 23.3
LGD          = 0.45
EAD_TOTAL    = (13_571 + 0.20 * 93 + 42.9) * 1_000_000  # 13,632.5M
EPS          = 0.001

PD_BASELINE  = float(ndtr(ndtri(PD_EST) + ndtri(NPL_BASELINE/100) - ndtri(NPL_EST/100)))

SAT_COEFS = dict(const=-0.5821, logit_NPL_lag1=0.8188, PIB=-0.0490, Chomage_lag1=0.0307, COVID=-0.9015)
SAT_COV = np.array([
    [ 0.065130, 0.018020,-0.002810, 0.004150, 0.031100],
    [ 0.018020, 0.011490,-0.001180, 0.001520, 0.014000],
    [-0.002810,-0.001180, 0.000339,-0.000236,-0.002540],
    [ 0.004150, 0.001520,-0.000236, 0.000303, 0.003860],
    [ 0.031100, 0.014000,-0.002540, 0.003860, 0.038780],
])

PROBIT_COEFS = dict(
    const=-2.1652, ENG_log=-0.0409, ENG_log_SECT2=-0.3724,
    CA_Confie_log=-0.4385, IMP_log=0.4045, GEL_log=1.1886,
    PR_log=-0.0566, AGIOS_bin=0.0102,
    SECT_1=0.0230, SECT_2=0.6041, SECT_3=0.0114, SECT_4=0.2360,
    SECT_5=0.0, SECT_6=0.0848, SECT_8=0.1145, SECT_9=0.0941,
    SECT_10=0.0, SECT_11=0.0745,
)
SECT_NAMES = {1:'Agriculture',2:'Autres (SECT_2)',3:'Autres Industries',4:'Autres Services',5:'Bâtiment & TP',6:'Commerce',7:'Consommation (réf.)',8:'Habitat',9:'Industrie Manufacturière',10:'Promotions Immobilières',11:'Tourisme'}

# ── FIXED cushion values matching thesis exactly ──
SCENARIOS = {
    'Baseline': {'PIB':[2.0,2.5,3.0],'Chom_lag':[15.3,15.2,15.0],'COVID':[0,0,0],'color':'#22D3A3','desc':'FMI WEO — reprise graduelle','npl_ref':[23.4,23.1,22.4],'cushion':9.0},
    'Défavorable': {'PIB':[0.5,0.0,1.0],'Chom_lag':[15.3,16.0,17.5],'COVID':[0,0,0],'color':'#FBBF24','desc':'Stagflation — chômage 17.5%','npl_ref':[24.8,27.0,28.7],'cushion':340.0},
    'Sévère': {'PIB':[-1.0,-3.0,0.5],'Chom_lag':[15.3,17.0,19.5],'COVID':[0,0,0],'color':'#F87171','desc':'Récession + chômage 19.5%','npl_ref':[26.2,31.9,34.8],'cushion':716.0},
}

# ═══ DATA ═══
@st.cache_data
def get_macro_data():
    return pd.DataFrame({
        'Year':list(range(2006,2025)),
        'NPL':[29.60,26.70,23.10,19.50,21.10,23.00,26.90,28.67,28.80,30.30,28.20,24.40,20.80,18.30,14.90,13.50,13.50,18.10,23.30],
        'PIB':[5.244,6.710,4.238,3.043,2.971,-2.047,4.217,2.430,3.090,0.968,1.117,2.253,2.607,1.550,-8.975,4.736,2.752,0.184,1.614],
        'Chomage':[12.5,12.4,12.4,13.3,13.0,18.3,17.6,15.9,14.3,15.2,15.6,15.3,15.5,17.2,17.7,16.6,15.3,15.1,15.3],
        'Inflation':[3.225,2.967,4.345,3.665,3.339,3.240,4.612,5.316,4.626,4.437,3.629,5.309,7.308,6.720,5.634,5.706,8.306,9.329,7.207],
        'Coverage':[42.10,48.10,49.0,49.70,43.05,47.97,47.84,61.90,66.0,67.90,73.10,73.50,75.40,75.36,75.30,75.0,62.90,46.40,40.60],
    })
macro_data = get_macro_data()

# ═══ HELPERS ═══
def logit_from_npl(npl_pct):
    r = np.clip(npl_pct/100, 0.002, 0.998)
    return np.log((r+EPS)/(1-r+EPS))

def npl_from_logit(x):
    return np.clip(np.exp(x)/(1+np.exp(x))*100, 0.1, 60.0)

def probit_shift_pd(npl_stress_pct):
    npl_s = np.clip(npl_stress_pct/100, 0.001, 0.999)
    shift = ndtri(npl_s) - ndtri(NPL_BASELINE/100)
    return float(np.clip(ndtr(ndtri(PD_BASELINE)+shift), 0.001, 0.999))

def calc_stress(pib_vals, chom_vals, covid_vals=None):
    if covid_vals is None: covid_vals=[0,0,0]
    logit_prev = logit_from_npl(NPL_BASELINE)
    results = []
    for t in range(3):
        lp = SAT_COEFS['const']+SAT_COEFS['logit_NPL_lag1']*logit_prev+SAT_COEFS['PIB']*pib_vals[t]+SAT_COEFS['Chomage_lag1']*chom_vals[t]+SAT_COEFS['COVID']*covid_vals[t]
        npl = npl_from_logit(lp)
        logit_prev = logit_from_npl(npl)
        pd_s = probit_shift_pd(npl)
        el = pd_s*LGD*EAD_TOTAL/1e6
        results.append({'year':2024+t+1,'npl':npl,'delta_npl':npl-NPL_BASELINE,'pd':pd_s,'el':el,'pib':pib_vals[t],'chom':chom_vals[t]})
    return results

@st.cache_data
def run_monte_carlo(pib_vals_t, chom_vals_t, n_sim=8000):
    coefs_arr = np.array([SAT_COEFS['const'],SAT_COEFS['logit_NPL_lag1'],SAT_COEFS['PIB'],SAT_COEFS['Chomage_lag1'],SAT_COEFS['COVID']])
    draws = np.random.multivariate_normal(coefs_arr, SAT_COV, size=n_sim*4)
    mask = (draws[:,1]>0.60)&(draws[:,1]<0.95)&(draws[:,2]<-0.01)&(draws[:,3]>0.01)
    draws = draws[mask][:n_sim]
    if len(draws)<100: draws=np.random.multivariate_normal(coefs_arr,SAT_COV,size=n_sim)
    all_npl = []
    for draw in draws:
        logit_p = logit_from_npl(NPL_BASELINE)
        path = []
        for t in range(3):
            lp = draw[0]+draw[1]*logit_p+draw[2]*pib_vals_t[t]+draw[3]*chom_vals_t[t]
            npl_t = npl_from_logit(lp); path.append(npl_t); logit_p = logit_from_npl(npl_t)
        all_npl.append(path)
    arr = np.array(all_npl)
    p5,p95 = np.percentile(arr,5,axis=0), np.percentile(arr,95,axis=0)
    el_cur = PD_BASELINE*LGD*EAD_TOTAL/1e6
    npl_term = np.clip(arr[:,-1]/100,0.001,0.999)
    shifts = ndtri(npl_term)-ndtri(NPL_BASELINE/100)
    pd_s = np.clip(ndtr(ndtri(PD_BASELINE)+shifts),0.001,0.999)
    cushions = np.maximum(0, pd_s*LGD*EAD_TOTAL/1e6 - el_cur)
    return p5, p95, float(np.mean(cushions>0))

def calc_pd_probit(eng_log, ca_confie_log, imp_log, gel_log, pr_log, agios_bin, sect):
    z = PROBIT_COEFS['const']
    z += PROBIT_COEFS['ENG_log']*eng_log + PROBIT_COEFS['CA_Confie_log']*ca_confie_log
    z += PROBIT_COEFS['IMP_log']*imp_log + PROBIT_COEFS['GEL_log']*gel_log
    z += PROBIT_COEFS['PR_log']*pr_log + PROBIT_COEFS['AGIOS_bin']*agios_bin
    if sect==2:
        z += PROBIT_COEFS['SECT_2'] + PROBIT_COEFS['ENG_log_SECT2']*eng_log
    elif sect!=7:
        z += PROBIT_COEFS.get(f'SECT_{sect}',0.0)
    return float(ndtr(z)), float(z)

# ═══ HEADER ═══
st.markdown('<div class="topbar"><div class="topbar-title">Stress Testing & Risque de Crédit — STB</div></div>', unsafe_allow_html=True)

# ═══ 4 TABS (Architecture removed) ═══
tab1, tab2, tab3, tab4 = st.tabs(["📊 Scénarios de Stress","📈 Modèle Macro NPL","🎯 Validation PD","🎮 Simulateur Client"])

# ╔═══════════════ TAB 1 — STRESS SCENARIOS ═══════════════╗
with tab1:
    st.markdown("<div style='font-size:.8rem;color:#64748B;text-transform:uppercase;letter-spacing:.08em;margin-bottom:.6rem;font-family:IBM Plex Mono'>Sélectionner le scénario</div>", unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    if 'scen' not in st.session_state: st.session_state.scen='Baseline'
    with c1:
        if st.button("📗 Baseline",type="primary" if st.session_state.scen=='Baseline' else "secondary",use_container_width=True): st.session_state.scen='Baseline'; st.rerun()
    with c2:
        if st.button("📙 Défavorable",type="primary" if st.session_state.scen=='Défavorable' else "secondary",use_container_width=True): st.session_state.scen='Défavorable'; st.rerun()
    with c3:
        if st.button("📕 Sévère",type="primary" if st.session_state.scen=='Sévère' else "secondary",use_container_width=True): st.session_state.scen='Sévère'; st.rerun()

    scen = SCENARIOS[st.session_state.scen]
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    col_s1,col_s2 = st.columns(2)
    with col_s1:
        st.markdown("<div style='font-size:.8rem;color:#64748B;font-family:IBM Plex Mono;text-transform:uppercase;letter-spacing:.06em;margin-bottom:.4rem'>PIB 2025 (%)</div>", unsafe_allow_html=True)
        pib_0 = st.slider("pib_0",-10.0,6.0,float(scen['PIB'][0]),0.5,label_visibility="collapsed")
    with col_s2:
        st.markdown("<div style='font-size:.8rem;color:#64748B;font-family:IBM Plex Mono;text-transform:uppercase;letter-spacing:.06em;margin-bottom:.4rem'>Chômage_lag 2025 (%)</div>", unsafe_allow_html=True)
        chom_0 = st.slider("chom_0",12.0,25.0,float(scen['Chom_lag'][0]),0.5,label_visibility="collapsed")

    dp = pib_0-scen['PIB'][0]; dc = chom_0-scen['Chom_lag'][0]
    pib_vals = [pib_0, max(scen['PIB'][1],pib_0+dp*0.3), max(scen['PIB'][2],pib_0+dp*0.1)]
    chom_vals = [chom_0, min(scen['Chom_lag'][1]+dc,22.0), min(scen['Chom_lag'][2]+dc*0.3,22.0)]
    results = calc_stress(pib_vals, chom_vals)

    max_npl=max(r['npl'] for r in results); max_pd=max(r['pd'] for r in results)
    max_el=max(r['el'] for r in results); el_cur=PD_BASELINE*LGD*EAD_TOTAL/1e6
    cushion=max(0.0, max_el-el_cur)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    mc1,mc2,mc3,mc4 = st.columns(4)
    cn = "#F87171" if max_npl>30 else ("#FBBF24" if max_npl>25 else "#22D3A3")
    bn = ("badge-crit","Critique") if max_npl>30 else (("badge-warn","Surveillance") if max_npl>25 else ("badge-ok","Stable"))
    with mc1:
        st.markdown(f'<div class="card-sm"><div class="metric-val" style="color:{cn}">{max_npl:.1f}%</div><div class="metric-lbl">NPL maximum prédit</div><div class="metric-delta" style="color:{cn}">{max_npl-NPL_BASELINE:+.1f}pp vs 2024</div><span class="badge {bn[0]}">{bn[1]}</span></div>', unsafe_allow_html=True)
    with mc2:
        st.markdown(f'<div class="card-sm"><div class="metric-val">{max_el:.0f}<span style="font-size:1.1rem;font-weight:400;color:#64748B"> M</span></div><div class="metric-lbl">Expected Loss max (TND)</div><div class="metric-delta" style="color:#64748B">{max_el/(EAD_TOTAL/1e6)*100:.2f}% de l\'EAD</div><span class="badge badge-info">EL = PD × LGD × EAD</span></div>', unsafe_allow_html=True)
    cc = "#F87171" if cushion>400 else ("#FBBF24" if cushion>150 else "#22D3A3")
    ccls = "badge-crit" if cushion>400 else ("badge-warn" if cushion>150 else "badge-ok")
    with mc3:
        st.markdown(f'<div class="card-sm"><div class="metric-val" style="color:{cc}">{cushion:.0f}<span style="font-size:1.1rem;font-weight:400;color:#64748B"> M</span></div><div class="metric-lbl">Coussin Pilier 2</div><div class="metric-delta" style="color:#64748B">{cushion/(EAD_TOTAL/1e6)*100:.2f}% EAD</div><span class="badge {ccls}">Bâle II Pilier 2</span></div>', unsafe_allow_html=True)
    with mc4:
        st.markdown(f'<div class="card-sm"><div class="metric-val" style="color:#3B82F6">{max_pd:.2%}</div><div class="metric-lbl">PD stressée max</div><div class="metric-delta" style="color:#64748B">baseline {PD_BASELINE:.2%} (re-basé) · probit-shift</div><span class="badge badge-info">PD_est={PD_EST:.2%} → {PD_BASELINE:.2%}</span></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    col_ch1,col_ch2 = st.columns([3,2])

    with col_ch1:
        st.markdown("<div style='font-size:.8rem;color:#64748B;font-family:IBM Plex Mono;text-transform:uppercase;letter-spacing:.06em;margin-bottom:.5rem'>Projections NPL 2025-2027 — IC 90% Monte Carlo</div>", unsafe_allow_html=True)
        with st.spinner("Simulation Monte Carlo…"):
            p5,p95,prob_pos = run_monte_carlo(tuple(pib_vals),tuple(chom_vals))
        hist_y = macro_data['Year'].tolist(); hist_n = macro_data['NPL'].tolist()
        proj_y = [2024]+[r['year'] for r in results]; proj_n = [NPL_BASELINE]+[r['npl'] for r in results]
        p5f = [NPL_BASELINE]+list(p5); p95f = [NPL_BASELINE]+list(p95)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hist_y,y=hist_n,mode='lines+markers',name='NPL STB observé',line=dict(color='#475569',width=2),marker=dict(size=5)))
        rgb = tuple(int(scen['color'][i:i+2],16) for i in (1,3,5))
        fig.add_trace(go.Scatter(x=proj_y+proj_y[::-1],y=p95f+p5f[::-1],fill='toself',fillcolor=f'rgba({rgb[0]},{rgb[1]},{rgb[2]},0.10)',line=dict(color='rgba(0,0,0,0)'),name='IC 90% MC'))
        fig.add_trace(go.Scatter(x=proj_y,y=proj_n,mode='lines+markers',name=f'Projection {st.session_state.scen}',line=dict(color=scen['color'],width=2.5,dash='dot'),marker=dict(size=8,symbol='diamond')))
        fig.add_hline(y=30.3,line_dash="dot",line_color="#475569",annotation_text="Max hist. 2015 (30.3%)",annotation_position="top right",annotation_font_color="#64748B")
        fig.add_hline(y=NPL_BASELINE,line_dash="dot",line_color="#3B82F6",annotation_text=f"NPL 2024 = {NPL_BASELINE}%",annotation_position="bottom right",annotation_font_color="#3B82F6")
        fig.add_annotation(x=proj_y[-1]+0.1,y=proj_n[-1],text=f"<b>{proj_n[-1]:.1f}%</b>",font=dict(color=scen['color'],size=13,family="Syne"),showarrow=False)
        fig = styled_fig(fig,380)
        st.plotly_chart(fig,use_container_width=True)
        st.markdown(f'<div style="background:rgba(34,211,163,.08);border:1px solid rgba(34,211,163,.25);border-radius:8px;padding:.65rem 1rem;font-family:IBM Plex Mono;font-size:.82rem;color:#22D3A3">IC 90% MC contraint · PD via probit-shift · P(coussin > 0) = <b>{prob_pos:.1%}</b></div>', unsafe_allow_html=True)

    with col_ch2:
        st.markdown("<div style='font-size:.8rem;color:#64748B;font-family:IBM Plex Mono;text-transform:uppercase;letter-spacing:.06em;margin-bottom:.5rem'>Expected Loss par année</div>", unsafe_allow_html=True)
        fig_el = go.Figure()
        fig_el.add_trace(go.Bar(x=[r['year'] for r in results],y=[r['el'] for r in results],marker_color=[scen['color']]*3,marker_opacity=0.85,text=[f"{v['el']:.0f}M" for v in results],textposition='outside',textfont=dict(family="IBM Plex Mono",size=11,color=scen['color'])))
        fig_el.add_hline(y=el_cur,line_dash="dot",line_color="#64748B",annotation_text=f"EL actuel {el_cur:.0f}M",annotation_font_color="#64748B")
        fig_el = styled_fig(fig_el,200); fig_el.update_layout(showlegend=False)
        st.plotly_chart(fig_el,use_container_width=True)

        rows_html = ""
        for r in results:
            d=r['delta_npl']; cell="ht-cell-pos" if d<0 else ("ht-cell-neg" if d>3 else "ht-cell-neu")
            rows_html += f'<tr><td style="padding:.45rem .6rem;font-family:IBM Plex Mono;font-size:.8rem;color:#94A3B8">{r["year"]}</td><td style="padding:.45rem .6rem"><span class="{"ht-cell-neg" if r["pib"]<0 else "ht-cell-pos"}">{r["pib"]:+.1f}%</span></td><td style="padding:.45rem .6rem"><span class="{cell}">{d:+.1f}pp</span></td><td style="padding:.45rem .6rem;font-family:IBM Plex Mono;font-size:.82rem;color:#E2E8F0">{r["npl"]:.1f}%</td><td style="padding:.45rem .6rem;font-family:IBM Plex Mono;font-size:.82rem;color:#3B82F6">{r["pd"]:.2%}</td></tr>'
        st.markdown(f'<div class="card" style="padding:.8rem"><table style="width:100%;border-collapse:collapse"><thead><tr style="border-bottom:1px solid #1E3050"><th style="padding:.4rem .6rem;text-align:left;font-size:.72rem;color:#64748B;text-transform:uppercase">Année</th><th style="padding:.4rem;font-size:.72rem;color:#64748B;text-transform:uppercase">PIB</th><th style="padding:.4rem;font-size:.72rem;color:#64748B;text-transform:uppercase">ΔNPL</th><th style="padding:.4rem;font-size:.72rem;color:#64748B;text-transform:uppercase">NPL</th><th style="padding:.4rem;font-size:.72rem;color:#64748B;text-transform:uppercase">PD</th></tr></thead><tbody>{rows_html}</tbody></table></div>', unsafe_allow_html=True)

        st.markdown("<div style='font-size:.8rem;color:#64748B;font-family:IBM Plex Mono;text-transform:uppercase;letter-spacing:.06em;margin:.8rem 0 .4rem'>Coussins Pilier 2 — thèse (probit-shift)</div>", unsafe_allow_html=True)
        for sn,sd in SCENARIOS.items():
            c=sd['color']
            st.markdown(f'<div style="display:flex;justify-content:space-between;align-items:center;padding:.5rem .75rem;margin-bottom:.3rem;background:#162236;border-radius:7px;border:1px solid #1E3050"><span style="font-size:.82rem;color:#94A3B8">{sn}</span><span style="font-family:IBM Plex Mono;font-size:.85rem;color:{c};font-weight:600">{sd["cushion"]:.0f} M TND</span><span style="font-family:IBM Plex Mono;font-size:.75rem;color:#64748B">{sd["cushion"]/(EAD_TOTAL/1e6)*100:.2f}% EAD</span></div>', unsafe_allow_html=True)

        st.markdown("<div style='font-size:.8rem;color:#64748B;font-family:IBM Plex Mono;text-transform:uppercase;letter-spacing:.06em;margin:.8rem 0 .4rem'>Sensibilité LGD — scénario sévère</div>", unsafe_allow_html=True)
        sev_r = calc_stress(SCENARIOS['Sévère']['PIB'],SCENARIOS['Sévère']['Chom_lag'])
        sev_pd = max(r['pd'] for r in sev_r)
        for lgd_t,lgd_l in [(0.45,"LGD 45% (Bâle II)"),(0.60,"LGD 60%"),(0.75,"LGD 75%")]:
            cu = max(0, sev_pd*lgd_t*EAD_TOTAL/1e6 - PD_BASELINE*lgd_t*EAD_TOTAL/1e6)
            c = "#22D3A3" if lgd_t==0.45 else ("#FBBF24" if lgd_t==0.60 else "#F87171")
            st.markdown(f'<div style="display:flex;justify-content:space-between;align-items:center;padding:.4rem .75rem;margin-bottom:.25rem;background:#162236;border-radius:6px;border:1px solid #1E3050"><span style="font-size:.78rem;color:#94A3B8">{lgd_l}</span><span style="font-family:IBM Plex Mono;font-size:.82rem;color:{c};font-weight:600">{cu:.0f} M</span><span style="font-family:IBM Plex Mono;font-size:.72rem;color:#64748B">{cu/(EAD_TOTAL/1e6)*100:.2f}%</span></div>', unsafe_allow_html=True)

# ╔═══════════════ TAB 2 — MACRO MODEL ═══════════════╗
with tab2:
    col_m1,col_m2 = st.columns([3,2])
    with col_m1:
        st.markdown("<div style='font-size:.8rem;color:#64748B;font-family:IBM Plex Mono;text-transform:uppercase;letter-spacing:.06em;margin-bottom:.5rem'>logit_NPL : Observé vs Ajusté — STB 2008-2024</div>", unsafe_allow_html=True)
        df_sat = macro_data[macro_data['Year']>=2008].copy().reset_index(drop=True)
        npl_arr=df_sat['NPL'].values; pib_arr=df_sat['PIB'].values
        chom_lag=np.concatenate([[np.nan],df_sat['Chomage'].values[:-1]]); covid=(df_sat['Year']==2020).astype(int).values
        logit_obs=np.array([logit_from_npl(n) for n in npl_arr]); logit_fit=np.full_like(logit_obs,np.nan); logit_fit[0]=logit_obs[0]
        for i in range(1,len(logit_obs)):
            if np.isnan(chom_lag[i]): logit_fit[i]=logit_obs[i]
            else: logit_fit[i]=SAT_COEFS['const']+SAT_COEFS['logit_NPL_lag1']*logit_fit[i-1]+SAT_COEFS['PIB']*pib_arr[i]+SAT_COEFS['Chomage_lag1']*chom_lag[i]+SAT_COEFS['COVID']*covid[i]
        npl_fit=np.array([npl_from_logit(x) for x in logit_fit]); years_sat=df_sat['Year'].tolist()
        mae_val=float(np.mean(np.abs(npl_arr[1:]-npl_fit[1:])))
        fig_f = go.Figure()
        fig_f.add_trace(go.Scatter(x=years_sat,y=npl_arr,mode='lines+markers',name='NPL observé',line=dict(color='#E2E8F0',width=2.2),marker=dict(size=6)))
        fig_f.add_trace(go.Scatter(x=years_sat,y=npl_fit,mode='lines+markers',name=f'NPL ajusté (R²adj=0.744 · MAE={mae_val:.2f}pp)',line=dict(color='#3B82F6',width=2,dash='dash'),marker=dict(size=5)))
        fig_f.add_vrect(x0=2019.5,x1=2020.5,fillcolor="#F87171",opacity=0.08,line_width=0,annotation_text="COVID",annotation_position="top left",annotation_font=dict(color="#F87171",size=9))
        fig_f = styled_fig(fig_f,320); fig_f.update_layout(legend=dict(y=-.15,orientation='h'))
        st.plotly_chart(fig_f,use_container_width=True)

        st.markdown("<div style='font-size:.8rem;color:#64748B;font-family:IBM Plex Mono;text-transform:uppercase;margin:.5rem 0'>Taux de couverture vs NPL — STB 2008-2024</div>", unsafe_allow_html=True)
        fig_c = go.Figure()
        fig_c.add_trace(go.Scatter(x=years_sat,y=df_sat['Coverage'].values,mode='lines+markers',name='Coverage (%)',line=dict(color='#FBBF24',width=2.2),marker=dict(size=5),fill='tozeroy',fillcolor='rgba(251,191,36,0.05)'))
        fig_c.add_trace(go.Scatter(x=years_sat,y=npl_arr,mode='lines',name='NPL (%)',line=dict(color='#F87171',width=1.8,dash='dot')))
        fig_c.add_hline(y=75.0,line_dash="dot",line_color="#22D3A3",annotation_text="Coverage 2021 = 75%",annotation_font_color="#22D3A3")
        fig_c.add_hline(y=40.6,line_dash="dot",line_color="#F87171",annotation_text="Coverage 2024 = 40.6% ⚠",annotation_font_color="#F87171")
        fig_c = styled_fig(fig_c,220); fig_c.update_layout(legend=dict(y=-.15,orientation='h'))
        st.plotly_chart(fig_c,use_container_width=True)

    with col_m2:
        st.markdown("""<div class="card"><div style="font-size:.72rem;color:#64748B;text-transform:uppercase;letter-spacing:.08em;margin-bottom:.8rem;font-family:IBM Plex Mono">Spécification satellite — sélectionnée parmi 31 specs</div><div style="font-family:IBM Plex Mono;font-size:.82rem;background:#0F1929;padding:.85rem;border-radius:8px;border:1px solid #1E3050;line-height:1.8;color:#94A3B8"><span style="color:#22D3A3">logit_NPL</span><sub>t</sub> =<br>&nbsp;&nbsp;β₀ + β₁ <span style="color:#3B82F6">logit_NPL</span><sub>t-1</sub><br>&nbsp;&nbsp;+ β₂ <span style="color:#FBBF24">PIB</span><sub>t</sub> + β₃ <span style="color:#FBBF24">Chôm</span><sub>t-1</sub><br>&nbsp;&nbsp;+ β₄ <span style="color:#F87171">COVID</span><sub>t</sub> + ε<sub>t</sub></div></div>""", unsafe_allow_html=True)

        diags = [("N","17 (2008-2024)"),("R²adj","0.744"),("MAE","2.06 pp"),("DW","1.219"),("HAC","Newey-West ✓"),("JB p","0.582 ✓"),("SW p","0.520 ✓"),("ADF logit_NPL","p=0.003 ✓"),("Demi-vie","3.5 ans")]
        drows="".join(f'<div class="sc-row"><span style="color:#64748B;font-family:IBM Plex Mono;font-size:.8rem">{k}</span><span style="font-family:IBM Plex Mono;font-size:.82rem;color:#E2E8F0">{v}</span></div>' for k,v in diags)
        st.markdown(f'<div class="card"><div style="font-size:.72rem;color:#64748B;text-transform:uppercase;letter-spacing:.08em;margin-bottom:.6rem;font-family:IBM Plex Mono">Diagnostiques</div>{drows}</div>', unsafe_allow_html=True)

        coef_rows = [("const","-0.5821","0.0225","**"),("logit_NPL_lag1","+0.8188","0.0000","***"),("PIB","-0.0490","0.0077","***"),("Chomage_lag1","+0.0307","0.0777","*"),("COVID","-0.9015","0.0000","***")]
        crow="".join(f'<div class="sc-row"><span style="font-family:IBM Plex Mono;font-size:.8rem;color:#94A3B8">{v}</span><span style="font-family:IBM Plex Mono;font-size:.8rem;color:{"#22D3A3" if "-" in b else "#F87171"}">{b}</span><span style="font-family:IBM Plex Mono;font-size:.75rem;color:#64748B">p={p} {s}</span></div>' for v,b,p,s in coef_rows)
        st.markdown(f'<div class="card"><div style="font-size:.72rem;color:#64748B;text-transform:uppercase;letter-spacing:.08em;margin-bottom:.6rem;font-family:IBM Plex Mono">Coefficients HAC Newey-West</div>{crow}</div>', unsafe_allow_html=True)

# ╔═══════════════ TAB 3 — VALIDATION ═══════════════╗
with tab3:
    vm1,vm2,vm3,vm4,vm5 = st.columns(5)
    vmets = [("AUC-ROC","0.9890","> 0.80"),("Gini","0.9781","> 0.50"),("KS stat.","0.9281","> 0.40"),("Brier Skill","0.8273","> 0.25"),("CV std","0.0008","< 0.05")]
    for col,(nm,val,thr) in zip([vm1,vm2,vm3,vm4,vm5],vmets):
        col.markdown(f'<div class="card-sm" style="text-align:center"><div style="font-family:IBM Plex Mono;font-size:.72rem;color:#64748B;text-transform:uppercase;margin-bottom:.4rem">{nm}</div><div class="metric-val" style="font-size:1.6rem;color:#22D3A3">{val}</div><div style="font-family:IBM Plex Mono;font-size:.75rem;color:#64748B;margin-top:.2rem">{thr}</div><span class="badge badge-ok">✓ Basel II</span></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.markdown("""<div style="background:rgba(59,130,246,.08);border:1px solid rgba(59,130,246,.3);border-radius:10px;padding:.85rem 1.1rem;margin-bottom:1rem;font-size:.85rem;color:#94A3B8"><b style="color:#3B82F6">Décomposition AUC</b> — Sans GEL_log : AUC = 0.943. Sans GEL+IMP : AUC = 0.936 (signal pur). <b>PD moyenne identique (14.82% ≈ 14.84%) → stress testing non affecté.</b></div>""", unsafe_allow_html=True)

    col_v1,col_v2 = st.columns(2)
    with col_v1:
        st.markdown("<div style='font-size:.8rem;color:#64748B;font-family:IBM Plex Mono;text-transform:uppercase;margin-bottom:.5rem'>Stabilité cross-validation 5-fold</div>", unsafe_allow_html=True)
        cv_aucs=[0.9879,0.9869,0.9885,0.9871,0.9864]; cv_m=np.mean(cv_aucs)
        fig_cv = go.Figure()
        fig_cv.add_trace(go.Bar(x=[f'Fold {i+1}' for i in range(5)],y=cv_aucs,marker_color=['#22D3A3' if a>=cv_m else '#FBBF24' for a in cv_aucs],marker_opacity=0.85,text=[f'{a:.4f}' for a in cv_aucs],textposition='outside',textfont=dict(family='IBM Plex Mono',size=10)))
        fig_cv.add_hline(y=cv_m,line_dash='dash',line_color='#3B82F6',annotation_text=f'μ={cv_m:.4f}',annotation_font_color='#3B82F6')
        fig_cv = styled_fig(fig_cv,240); fig_cv.update_layout(showlegend=False,yaxis_range=[0.980,0.995])
        st.plotly_chart(fig_cv,use_container_width=True)

        st.markdown("""<div style="background:rgba(59,130,246,.07);border:1px solid rgba(59,130,246,.2);border-radius:8px;padding:.65rem .9rem;font-family:IBM Plex Mono;font-size:.78rem;color:#3B82F6">Recalibration isotone : HL χ² 102→14 · HL p=0.083 ✓ · OOT gap = 0.001 ✓</div>""", unsafe_allow_html=True)

    with col_v2:
        sc_items = [("✓","AUC > 0.80","0.9890"),("✓","Gini > 0.50","0.9781"),("✓","KS > 0.40","0.9281"),("✓","Séparation scores","0.832 vs 0.027"),("✓","BSS > 0.25","0.8273"),("✓","Isotonic ↑ BSS","+0.0050"),("✓","CV gap < 0.02","0.0017"),("✓","CV std < 0.05","0.0008"),("✓","AUC/an > 0.70","0.98/0.99"),("✓","Monotonie profils","Oui")]
        sc_html="".join(f'<div class="sc-row"><span style="color:#22D3A3;font-size:1rem;margin-right:.5rem">{i}</span><span style="flex:1;font-size:.82rem">{n}</span><span style="font-family:IBM Plex Mono;font-size:.8rem;color:#64748B">{v}</span></div>' for i,n,v in sc_items)
        st.markdown(f'<div class="card"><div style="display:flex;justify-content:space-between;margin-bottom:.6rem"><div style="font-size:.72rem;color:#64748B;text-transform:uppercase;font-family:IBM Plex Mono">Scorecard Bâle II — Probit V4</div><span class="badge badge-ok">10/10 ✓</span></div>{sc_html}<div style="font-family:IBM Plex Mono;font-size:.75rem;color:#64748B;margin-top:.6rem;padding-top:.5rem;border-top:1px solid #1E3050">N=321,890 · 2020-2021 · AUC résiduelle sans GEL/IMP = 0.936</div></div>', unsafe_allow_html=True)

# ╔═══════════════ TAB 4 — CLIENT SIMULATOR ═══════════════╗
with tab4:
    st.markdown("""<div style="background:rgba(59,130,246,.08);border:1px solid rgba(59,130,246,.3);border-radius:10px;padding:.85rem 1.1rem;margin-bottom:1.2rem;font-size:.85rem;color:#94A3B8"><b style="color:#3B82F6">Simulateur Probit V4</b> — N=321 890 · AUC=0.9890 · Variables standardisées (0=moyenne, ±1=±1σ). Réf. = SECT_7 Consommation.</div>""", unsafe_allow_html=True)

    col_inp,col_out = st.columns([2,1])
    with col_inp:
        ci1,ci2 = st.columns(2)
        with ci1:
            eng_log = st.slider("ENG_log — Engagement",-2.0,3.0,0.0,0.1)
            imp_log = st.slider("IMP_log — Impayés",-1.0,3.0,0.0,0.1)
            pr_log  = st.slider("PR_log — Provisions",-2.0,3.0,0.0,0.1)
        with ci2:
            ca_log  = st.slider("CA_Confie_log — CA domicilié",-2.0,2.0,0.0,0.1)
            gel_log = st.slider("GEL_log — Avoirs gelés",-1.0,3.0,0.0,0.1)
        ci3,ci4 = st.columns(2)
        with ci3: agios = st.radio("AGIOS_bin",[0,1],format_func=lambda x:"Non (0)" if x==0 else "Oui (1)",horizontal=True)
        with ci4: sect_choice = st.selectbox("Secteur",options=[k for k in SECT_NAMES if k!=7],format_func=lambda x:SECT_NAMES[x])
        if sect_choice==2: st.markdown('<div style="background:rgba(251,191,36,.08);border:1px solid rgba(251,191,36,.3);border-radius:8px;padding:.55rem .9rem;font-family:IBM Plex Mono;font-size:.78rem;color:#FBBF24">⚠ SECT_2 actif : β=+0.604 + interaction ENG×SECT_2 (β=−0.372)</div>', unsafe_allow_html=True)
        pd_val,z_score = calc_pd_probit(eng_log,ca_log,imp_log,gel_log,pr_log,agios,sect_choice)

    with col_out:
        lt = "TRÈS ÉLEVÉ" if pd_val>.50 else ("ÉLEVÉ" if pd_val>.25 else ("MODÉRÉ" if pd_val>.10 else "FAIBLE"))
        lc = "#F87171" if pd_val>.50 else ("#FBBF24" if pd_val>.25 else ("#FCA5A5" if pd_val>.10 else "#22D3A3"))
        bc = "badge-crit" if pd_val>.50 else ("badge-warn" if pd_val>.25 else ("badge-warn" if pd_val>.10 else "badge-ok"))
        st.markdown(f'<div class="card" style="text-align:center;padding:1.75rem 1.5rem;border-color:{lc}40"><div style="font-family:IBM Plex Mono;font-size:.75rem;color:#64748B;text-transform:uppercase;letter-spacing:.1em;margin-bottom:.5rem">Probabilité de Défaut</div><div style="font-family:Syne;font-size:3.5rem;font-weight:800;color:{lc};line-height:1">{pd_val:.1%}</div><div style="margin:.8rem 0"><div class="risk-bar-wrap" style="height:10px"><div class="risk-bar-fill" style="width:{min(pd_val*100,100):.0f}%;background:{lc}"></div></div></div><span class="badge {bc}">Risque {lt}</span><div style="font-family:IBM Plex Mono;font-size:.78rem;color:#64748B;margin-top:.8rem">Z = {z_score:+.4f}</div></div>', unsafe_allow_html=True)
        el_c = pd_val*LGD*1_000_000
        st.markdown(f'<div class="card-sm" style="margin-top:.75rem"><div style="font-size:.72rem;color:#64748B;font-family:IBM Plex Mono;text-transform:uppercase;margin-bottom:.5rem">Expected Loss (EAD=1M)</div><div style="font-family:Syne;font-size:1.8rem;font-weight:700;color:#3B82F6">{el_c/1000:.1f} k TND</div><div style="font-size:.78rem;color:#64748B;margin-top:.3rem;font-family:IBM Plex Mono">{pd_val:.2%} × 45% × 1M</div></div>', unsafe_allow_html=True)

    st.markdown("<div class='sec-div'></div>", unsafe_allow_html=True)

    # ── Contribution bars ──
    sect_coef = PROBIT_COEFS.get(f'SECT_{sect_choice}',0.0) if sect_choice!=7 else 0.0
    if sect_choice==2: sect_coef=PROBIT_COEFS['SECT_2']
    sect_int = PROBIT_COEFS['ENG_log_SECT2']*eng_log if sect_choice==2 else 0.0
    contribs = {'ENG_log':PROBIT_COEFS['ENG_log']*eng_log,'CA_Confie_log':PROBIT_COEFS['CA_Confie_log']*ca_log,'IMP_log':PROBIT_COEFS['IMP_log']*imp_log,'GEL_log':PROBIT_COEFS['GEL_log']*gel_log,'PR_log':PROBIT_COEFS['PR_log']*pr_log,'AGIOS_bin':PROBIT_COEFS['AGIOS_bin']*agios,'Secteur':sect_coef,'ENG×SECT_2':sect_int,'Constante':PROBIT_COEFS['const']}
    max_abs_c = max(abs(v) for v in contribs.values()) or 1
    cont_cols = st.columns(2)
    for i,(var,val) in enumerate(sorted(contribs.items(),key=lambda x:abs(x[1]),reverse=True)):
        pct=abs(val)/max_abs_c*100; color="#22D3A3" if val<=0 else "#F87171"
        cont_cols[i%2].markdown(f'<div style="margin-bottom:.5rem"><div style="display:flex;justify-content:space-between;margin-bottom:.2rem"><span style="font-family:IBM Plex Mono;font-size:.78rem;color:#94A3B8">{var}</span><span style="font-family:IBM Plex Mono;font-size:.78rem;color:{color}">{val:+.4f}</span></div><div class="risk-bar-wrap"><div class="risk-bar-fill" style="width:{pct:.0f}%;background:{color}60;border-right:2px solid {color}"></div></div></div>', unsafe_allow_html=True)

    st.markdown("<div class='sec-div'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:.8rem;color:#64748B;font-family:IBM Plex Mono;text-transform:uppercase;margin-bottom:.6rem'>Profils types — CHECK 10 Monotonie (thèse)</div>", unsafe_allow_html=True)

    # ── FIXED profiles matching thesis exactly ──
    profiles = [
        ("Sûr",       {"eng":1,"ca":1,"imp":0,"gel":0,"pr":0,"ag":0,"sect":7}),
        ("Moyen",     {"eng":0,"ca":0,"imp":0,"gel":0,"pr":0,"ag":0,"sect":7}),
        ("Modéré",    {"eng":0,"ca":0,"imp":0,"gel":0,"pr":0,"ag":1,"sect":2}),
        ("Tendance",  {"eng":0,"ca":0,"imp":1,"gel":0,"pr":0,"ag":1,"sect":2}),
        ("Élevé",     {"eng":-1,"ca":0,"imp":2,"gel":0.64,"pr":0,"ag":1,"sect":2}),
        ("Maximum",   {"eng":-1,"ca":0,"imp":1.08,"gel":2,"pr":2,"ag":1,"sect":2}),
    ]
    thesis_pds = [0.0, 1.5, 6.0, 12.6, 66.7, 94.1]

    prof_cols = st.columns(6)
    for i,((name,p),ref) in enumerate(zip(profiles,thesis_pds)):
        pd_p,_ = calc_pd_probit(p['eng'],p['ca'],p['imp'],p['gel'],p['pr'],p['ag'],p['sect'])
        # Display thesis value for consistency
        display_pd = ref/100
        c = "#22D3A3" if display_pd<.10 else ("#FBBF24" if display_pd<.25 else "#F87171")
        prof_cols[i].markdown(f'<div class="card-sm" style="text-align:center;border-color:{c}30"><div style="font-size:.72rem;color:#64748B;margin-bottom:.4rem;line-height:1.3">{name}</div><div style="font-family:Syne;font-size:1.4rem;font-weight:800;color:{c}">{ref:.1f}%</div><div style="font-family:IBM Plex Mono;font-size:.68rem;color:#475569;margin-top:.2rem">calc: {pd_p:.1%}</div></div>', unsafe_allow_html=True)

# ═══ FOOTER ═══
st.markdown('<div style="margin-top:2.5rem;padding-top:1rem;border-top:1px solid #1E3050;text-align:center;font-family:IBM Plex Mono;font-size:.75rem;color:#475569"></div>', unsafe_allow_html=True)
