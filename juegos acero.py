import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Simulador Metalúrgico Integral Fe-C / TTT", layout="wide")

st.markdown("""
    <style>
        .block-container { padding-top: 0.6rem; padding-bottom: 0.4rem; max-width: 98%; }
        header { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

html_simulador = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; font-family: 'Segoe UI', system-ui, sans-serif; }
  body { margin: 0; background: #0e1117; color: #f1f5f9; }
  
  /* BARRA DE NAVEGACIÓN DE PESTAÑAS */
  .top-nav {
    display: flex; justify-content: space-between; align-items: center;
    background: #131822; padding: 8px 14px; border-bottom: 1px solid #262f40; margin-bottom: 10px;
  }
  .nav-title { font-size: 1.08rem; font-weight: 700; color: #f8fafc; }
  .tab-bar { display: flex; gap: 8px; }
  .tab-btn {
    padding: 7px 14px; background: #0f172a; color: #94a3b8;
    border: 1px solid #334155; border-radius: 8px; cursor: pointer;
    font-size: 0.83rem; font-weight: 600; transition: all 0.15s;
  }
  .tab-btn:hover { border-color: #38bdf8; color: #f8fafc; }
  .tab-btn.active { background: #0284c7; color: #ffffff; border-color: #38bdf8; box-shadow: 0 0 12px rgba(2,132,199,0.35); }

  .tab-content { display: none; }
  .tab-content.active { display: block; }

  .grid-top { display: grid; grid-template-columns: 1.65fr 1.15fr; gap: 14px; }
  .card { background: #161b26; border: 1px solid #262f40; border-radius: 10px; padding: 11px; }
  .card-title { font-size: 0.91rem; font-weight: 700; color: #38bdf8; margin-bottom: 7px; display: flex; justify-content: space-between; align-items: center; }
  
  canvas { width: 100%; border-radius: 6px; display: block; background: #0b0f17; }
  
  .control-group { margin-bottom: 7px; }
  .control-label { display: flex; justify-content: space-between; font-size: 0.81rem; margin-bottom: 2px; color: #cbd5e1; }
  .control-val { font-weight: 700; color: #22c55e; font-variant-numeric: tabular-nums; }
  input[type=range] { width: 100%; accent-color: #22c55e; cursor: pointer; height: 6px; background: #334155; border-radius: 4px; }
  
  .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
  select { width: 100%; background: #0f172a; color: #f1f5f9; border: 1px solid #334155; border-radius: 6px; padding: 5px 8px; font-size: 0.8rem; }
  .radio-group { display: flex; gap: 6px; }
  .radio-btn { padding: 4px 8px; background: #0f172a; border: 1px solid #334155; border-radius: 6px; cursor: pointer; font-size: 0.74rem; }
  .radio-btn.active { background: #0284c7; border-color: #38bdf8; font-weight: 600; }

  .grid-bottom { display: grid; grid-template-columns: 1.12fr 1.06fr 1.17fr; gap: 14px; margin-top: 11px; }
  .metric-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 7px; margin-bottom: 9px; }
  .metric-box { background: #0f172a; padding: 6px 8px; border-radius: 7px; border-left: 3px solid #38bdf8; }
  .metric-lbl { font-size: 0.69rem; color: #94a3b8; }
  .metric-num { font-size: 0.98rem; font-weight: 700; color: #f8fafc; }
  .metric-sub { font-size: 0.69rem; color: #4ade80; }

  .phase-item { display: flex; justify-content: space-between; padding: 4px 0; border-bottom: 1px dashed #262f40; font-size: 0.8rem; }
  .story-box { background: #0f172a; padding: 8px 10px; border-radius: 7px; font-size: 0.8rem; margin-bottom: 7px; border-left: 3px solid #38bdf8; line-height: 1.42; color: #e2e8f0; }
  .aleante-box { background: #0f172a; padding: 6px 8px; border-radius: 6px; font-size: 0.77rem; margin-bottom: 5px; border-left: 3px solid #f59e0b; line-height: 1.32; }
  .micro-caption { font-size: 0.76rem; color: #94a3b8; margin-top: 5px; line-height: 1.32; }
  
  .legend-pill { display: inline-flex; align-items: center; gap: 5px; font-size: 0.75rem; margin-right: 10px; color: #cbd5e1; }
  .dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; }
</style>
</head>
<body>

<div class="top-nav">
  <div class="nav-title">Simulador Metalúrgico Interactivo · Ingeniería Metalúrgica</div>
  <div class="tab-bar">
    <div id="tabBtn1" class="tab-btn active" onclick="switchTab(1)">1. Diagrama Fe–Fe₃C y Fe–Grafito</div>
    <div id="tabBtn2" class="tab-btn" onclick="switchTab(2)">2. Diagrama TTT y Microestructuras</div>
    <div id="tabBtn3" class="tab-btn" onclick="switchTab(3)">3. Curvas de Enfriamiento y Subenfriamiento</div>
  </div>
</div>

<!-- ===================================================================== -->
<!-- PESTAÑA 1: DIAGRAMA DE EQUILIBRIO Fe-Fe3C Y Fe-GRAFITO                -->
<!-- ===================================================================== -->
<div id="tab1" class="tab-content active">
  <div class="grid-top">
    <div class="card">
      <div class="card-title">
        <span>Diagrama de Fases a Escala</span>
        <div class="radio-group">
          <div id="btnFull" class="radio-btn active" onclick="setZoom('full')">Completo (0–6.67%)</div>
          <div id="btnAceros" class="radio-btn" onclick="setZoom('aceros')">Aceros (0–2.3%)</div>
          <div id="btnPeri" class="radio-btn" onclick="setZoom('peri')">Zoom Peritéctico</div>
        </div>
      </div>
      <canvas id="phaseCanvas" width="760" height="430"></canvas>
    </div>

    <div class="card">
      <div class="card-title"><span>Composición Química y Ruta de Proceso</span></div>
      <div class="control-group">
        <div class="control-label"><span>Carbono (%C)</span><span id="valC" class="control-val">0.45 %</span></div>
        <input type="range" id="slC" min="0.01" max="6.67" step="0.01" value="0.45">
      </div>
      <div class="control-group">
        <div class="control-label"><span>Temperatura de Análisis (°C)</span><span id="valT" class="control-val">25 °C</span></div>
        <input type="range" id="slT" min="25" max="1600" step="5" value="25">
      </div>
      <div class="grid-2">
        <div class="control-group">
          <div class="control-label"><span>Silicio (%Si · Grafitizante)</span><span id="valSi" class="control-val">0.25 %</span></div>
          <input type="range" id="slSi" min="0.0" max="3.5" step="0.05" value="0.25">
        </div>
        <div class="control-group">
          <div class="control-label"><span>Cromo (%Cr · Carburígeno)</span><span id="valCr" class="control-val">0.00 %</span></div>
          <input type="range" id="slCr" min="0.0" max="5.0" step="0.1" value="0.0">
        </div>
        <div class="control-group">
          <div class="control-label"><span>Manganeso (%Mn · Gamágeno)</span><span id="valMn" class="control-val">0.70 %</span></div>
          <input type="range" id="slMn" min="0.0" max="3.0" step="0.05" value="0.70">
        </div>
        <div class="control-group">
          <div class="control-label"><span>Níquel (%Ni · Gamágeno)</span><span id="valNi" class="control-val">0.00 %</span></div>
          <input type="range" id="slNi" min="0.0" max="5.0" step="0.1" value="0.0">
        </div>
      </div>
      <div class="control-group" style="margin-top:3px;">
        <div class="control-label"><span>Velocidad de Enfriamiento / Espesor:</span></div>
        <select id="selVel">
          <option value="lento">Lento / Pieza gruesa (> 60 mm · Recocido / Grafitizante)</option>
          <option value="moderado">Moderado / Espesor medio (20–60 mm · Normalizado)</option>
          <option value="rapido">Rápido / Pieza delgada (< 20 mm · Temple v > v_crítica)</option>
        </select>
      </div>
      <div class="control-group">
        <div class="control-label"><span>Tratamiento Térmico / Metalurgia Secundaria:</span></div>
        <select id="selTrat">
          <option value="ninguno">Estándar (Enfriamiento continuo sin tratamiento posterior)</option>
          <option value="revenido">Revenido post-temple (400 °C · Martensita revenida)</option>
          <option value="globulizado">Recocido de Globulización (Subcrítico · Esferoidita)</option>
          <option value="bainita">Austemperado Isotérmico (Bainita / Ausferrita ADI)</option>
          <option value="nodular">Nodulizante en cuchara (Adición Mg / Ce · Fundición Dúctil)</option>
          <option value="vermicular">Compactante controlado (Fundición Vermicular CGI)</option>
          <option value="maleable">Recocido de Maleabilización (Desde fundición blanca)</option>
        </select>
      </div>
    </div>
  </div>

  <div class="grid-bottom">
    <div class="card">
      <div class="card-title">
        <span id="microTitle">Microscopía Óptica (500×)</span>
        <span id="microEtch" style="font-size:0.73rem; color:#94a3b8;">Ataque Nital 3%</span>
      </div>
      <canvas id="microCanvas" width="460" height="300"></canvas>
      <div id="microDesc" class="micro-caption"></div>
    </div>

    <div class="card">
      <div class="card-title"><span>Regla de la Palanca y Puntos Críticos</span></div>
      <div class="metric-row">
        <div class="metric-box">
          <div class="metric-lbl">Temp. A1 / Ms</div>
          <div id="mA1" class="metric-num">727 °C</div>
          <div id="mA1d" class="metric-sub">Ms: 325 °C</div>
        </div>
        <div class="metric-box">
          <div class="metric-lbl">%C Eutectoide</div>
          <div id="mCeut" class="metric-num">0.76 %</div>
          <div id="mCeutSub" class="metric-sub">Base: 0.76%</div>
        </div>
        <div class="metric-box">
          <div class="metric-lbl">Carbono Eq. (CE)</div>
          <div id="mCE" class="metric-num">0.53 %</div>
          <div id="mCEsub" class="metric-sub">Eutéctico: 4.30%</div>
        </div>
      </div>
      <div id="estadoTexto" style="font-size:0.83rem; font-weight:700; color:#fbbf24; margin-bottom:6px;"></div>
      <div id="palancaLista"></div>
    </div>

    <div class="card">
      <div class="card-title"><span>Historia Metalúrgica y Aleantes</span></div>
      <div id="historiaBox" class="story-box"></div>
      <div id="aleantesLista"></div>
    </div>
  </div>
</div>

<!-- ===================================================================== -->
<!-- PESTAÑA 2: DIAGRAMA TTT Y MICROESTRUCTURAS FUERA DEL EQUILIBRIO       -->
<!-- ===================================================================== -->
<div id="tab2" class="tab-content">
  <div class="grid-top">
    <div class="card">
      <div class="card-title">
        <span>Diagrama TTT (Transformación Isotérmica · Escala Logarítmica)</span>
        <div>
          <span class="legend-pill"><span class="dot" style="background:#38bdf8;"></span>Inicio (Ps)</span>
          <span class="legend-pill"><span class="dot" style="background:#f97316;"></span>Fin (Pf)</span>
          <span class="legend-pill"><span class="dot" style="background:#22c55e;"></span>Ruta Seleccionada</span>
        </div>
      </div>
      <canvas id="tttCanvas" width="760" height="430"></canvas>
    </div>

    <div class="card">
      <div class="card-title"><span>Parámetros de Templabilidad y Ruta TTT</span></div>
      
      <div class="control-group">
        <div class="control-label"><span>Ruta de Transformación en Diagrama TTT:</span></div>
        <select id="tttRuta">
          <option value="recocido">1. Recocido (Enfriamiento muy lento · 680 °C → Perlita Gruesa)</option>
          <option value="patentado">2. Normalizado / Patentado (Transformación ~530 °C · Perlita Fina)</option>
          <option value="bainita_sup">3. Austemperado Isotérmico Superior (420 °C · Bainita Superior)</option>
          <option value="bainita_inf">4. Austemperado Isotérmico Inferior (310 °C · Bainita Inferior)</option>
          <option value="temple">5. Temple Directo (v > v_crítica · Martensita 100%)</option>
          <option value="martemperado">6. Martemperado (Temple escalonado sobre Ms → Martensita sin grietas)</option>
          <option value="incompleto">7. Temple Interrumpido en Nariz (50% Perlita Fina + 50% Martensita)</option>
        </select>
      </div>

      <div class="control-group">
        <div class="control-label"><span>Carbono del Acero (%C)</span><span id="tttValC" class="control-val">0.76 %</span></div>
        <input type="range" id="tttSlC" min="0.20" max="1.20" step="0.02" value="0.76">
      </div>

      <div class="control-group">
        <div class="control-label"><span>Aleantes Templabilidad (%Cr + %Mn + %Ni)</span><span id="tttValAl" class="control-val">0.80 %</span></div>
        <input type="range" id="tttSlAl" min="0.0" max="4.5" step="0.1" value="0.80">
      </div>

      <div class="control-group">
        <div class="control-label"><span>Tiempo de Permanencia / Enfriamiento (s)</span><span id="tttValTime" class="control-val">1000 s</span></div>
        <input type="range" id="tttSlTime" min="0.2" max="10000" step="1" value="1000">
      </div>

      <div class="story-box" style="margin-top:8px; border-color:#f59e0b;">
        <b>Efecto de la Templabilidad en las Curvas "C":</b><br>
        • Al aumentar <b>%C</b> o <b>aleantes (Cr, Mn, Ni)</b>, se frena la difusión del carbono en la austenita γ.<br>
        • La <b>"nariz perlítica" (≈ 550 °C)</b> se desplaza hacia la <b>derecha</b> (más segundos disponibles para enfriar), reduciendo la velocidad crítica de temple ($v_{\text{crítica}}$) y bajando $M_s$.
      </div>
    </div>
  </div>

  <div class="grid-bottom">
    <div class="card">
      <div class="card-title">
        <span id="tttMicroTitle">Microestructura Resultante (500×)</span>
        <span style="font-size:0.73rem; color:#94a3b8;">Ataque Nital 3%</span>
      </div>
      <canvas id="tttMicroCanvas" width="460" height="300"></canvas>
      <div id="tttMicroDesc" class="micro-caption"></div>
    </div>

    <div class="card">
      <div class="card-title"><span>Cinética, Subenfriamiento y Propiedades</span></div>
      <div class="metric-row">
        <div class="metric-box">
          <div class="metric-lbl">Subenfriamiento ΔT</div>
          <div id="tttMetDT" class="metric-num">47 °C</div>
          <div id="tttMetDTsub" class="metric-sub">Bajo A1 (727°C)</div>
        </div>
        <div class="metric-box">
          <div class="metric-lbl">Espaciado / Morfología</div>
          <div id="tttMetS" class="metric-num">0.40 µm</div>
          <div id="tttMetSsub" class="metric-sub">Perlita gruesa</div>
        </div>
        <div class="metric-box">
          <div class="metric-lbl">Dureza Estimada</div>
          <div id="tttMetHRC" class="metric-num">20 HRC</div>
          <div id="tttMetHV" class="metric-sub">~230 HV</div>
        </div>
      </div>
      <div id="tttFasesLista"></div>
    </div>

    <div class="card">
      <div class="card-title"><span>Explicación Metalúrgica de la Ruta TTT</span></div>
      <div id="tttStoryBox" class="story-box"></div>
    </div>
  </div>
</div>

<!-- ===================================================================== -->
<!-- PESTAÑA 3: CURVAS DE ENFRIAMIENTO, CALENTAMIENTO Y SUBENFRIAMIENTO    -->
<!-- ===================================================================== -->
<div id="tab3" class="tab-content">
  <div class="grid-top">
    <div class="card">
      <div class="card-title">
        <span>Curvas Térmicas (Temperatura vs. Tiempo): Teórica vs. Real</span>
        <div>
          <span class="legend-pill"><span class="dot" style="background:#94a3b8;"></span>Equilibrio Teórico</span>
          <span class="legend-pill"><span class="dot" style="background:#2dd4bf;"></span>Enfriamiento Real (Ar)</span>
          <span class="legend-pill"><span class="dot" style="background:#fb923c;"></span>Calentamiento Real (Ac)</span>
        </div>
      </div>
      <canvas id="coolCanvas" width="760" height="430"></canvas>
    </div>

    <div class="card">
      <div class="card-title"><span>Configuración del Ensayo Térmico</span></div>
      
      <div class="control-group">
        <div class="control-label"><span>Material / Aleación Analizada:</span></div>
        <select id="coolMat">
          <option value="puro">1. Hierro Puro (0.00 %C · Mesetas alotrópicas A4, A3, A2 Curie)</option>
          <option value="hipo">2. Acero Hipoeutectoide (0.45 %C · Tramo intercrítico Ar3–Ar1)</option>
          <option value="eut">3. Acero Eutectoide (0.76 %C · Meseta isotérmica Ar1 + Recalescencia)</option>
          <option value="eutectica">4. Fundición Eutéctica (4.30 %C · Meseta de solidificación 1148 °C)</option>
        </select>
      </div>

      <div class="control-group">
        <div class="control-label"><span>Velocidad de Extracción / Aporte de Calor:</span><span id="coolValRate" class="control-val">Moderada (Normalizado)</span></div>
        <input type="range" id="coolSlRate" min="1" max="5" step="1" value="3">
      </div>

      <div class="control-group" style="margin-top:8px;">
        <label style="display:flex; align-items:center; gap:8px; font-size:0.82rem; cursor:pointer;">
          <input type="checkbox" id="chkHeat" checked style="accent-color:#fb923c;">
          <span>Mostrar Curva de Calentamiento Real (Puntos Ac · <i>Chauffage</i>)</span>
        </label>
      </div>
      <div class="control-group">
        <label style="display:flex; align-items:center; gap:8px; font-size:0.82rem; cursor:pointer;">
          <input type="checkbox" id="chkEq" checked style="accent-color:#94a3b8;">
          <span>Mostrar Curva Teórica de Equilibrio Ideal (v → 0, ΔT = 0)</span>
        </label>
      </div>

      <div class="story-box" style="margin-top:8px; border-color:#2dd4bf;">
        <b>¿Por qué existe el Subenfriamiento (ΔT) y la Recalescencia?</b><br>
        • <b>Teoría (Equilibrio):</b> Ocurre exactamente a $A_3 = 912\text{ }^\circ\text{C}$ o $A_1 = 727\text{ }^\circ\text{C}$ porque se asume tiempo infinito.<br>
        • <b>Realidad (Cinética):</b> Crear una nueva fase exige vencer la <b>energía superficial de nucleación</b>. Por ello el metal debe enfriarse por debajo de la temperatura de equilibrio ($Ar < A$) hasta acumular suficiente fuerza motriz $\Delta G_v \propto \Delta T$.<br>
        • <b>Recalescencia:</b> Al dispararse la nucleación masiva, la liberación súbita de calor latente eleva ligeramente la temperatura real antes de estabilizar la meseta.
      </div>
    </div>
  </div>

  <div class="grid-bottom">
    <div class="card">
      <div class="card-title"><span>Puntos Críticos Medidos (Histéresis Térmica)</span></div>
      <div class="metric-row">
        <div class="metric-box" style="border-color:#94a3b8;">
          <div class="metric-lbl">Equilibrio (A)</div>
          <div id="coolMetA" class="metric-num">727 °C</div>
          <div class="metric-sub">Ideal (v → 0)</div>
        </div>
        <div class="metric-box" style="border-color:#2dd4bf;">
          <div class="metric-lbl">Enfriamiento (Ar)</div>
          <div id="coolMetAr" class="metric-num">692 °C</div>
          <div id="coolMetDT" class="metric-sub">ΔT = -35 °C</div>
        </div>
        <div class="metric-box" style="border-color:#fb923c;">
          <div class="metric-lbl">Calentamiento (Ac)</div>
          <div id="coolMetAc" class="metric-num">748 °C</div>
          <div id="coolMetDTc" class="metric-sub">ΔT = +21 °C</div>
        </div>
      </div>
      <div id="coolPuntosLista"></div>
    </div>

    <div class="card">
      <div class="card-title"><span>¿Qué se obtiene bajo estas condiciones?</span></div>
      <div id="coolResultadoBox" class="story-box" style="border-color:#22c55e;"></div>
    </div>

    <div class="card">
      <div class="card-title"><span>Relación Subenfriamiento ↔ Microestructura</span></div>
      <div id="coolFisicaBox" class="story-box" style="border-color:#a78bfa;"></div>
    </div>
  </div>
</div>

<script>
// =========================================================================
// CONTROL DE PESTAÑAS
// =========================================================================
function switchTab(n) {
  [1, 2, 3].forEach(i => {
    document.getElementById('tab' + i).className = i === n ? 'tab-content active' : 'tab-content';
    document.getElementById('tabBtn' + i).className = i === n ? 'tab-btn active' : 'tab-btn';
  });
  if (n === 1) updateAll();
  if (n === 2) updateTTT();
  if (n === 3) updateCooling();
}

// =========================================================================
// MOTOR DE MICROESTRUCTURAS COMPARTIDO (VORONOI CALIBRADO)
// =========================================================================
const W = 460, H = 300;
let seed = 98765;
function rand() { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }

const COLS_G = 5, ROWS_G = 3;
const NUM_GAMMA = COLS_G * ROWS_G;
const gammaGrains = [];
for (let r = 0; r < ROWS_G; r++) {
  for (let c = 0; c < COLS_G; c++) {
    const cellW = W / COLS_G, cellH = H / ROWS_G;
    gammaGrains.push({
      x: (c + 0.25 + rand() * 0.5) * cellW,
      y: (r + 0.25 + rand() * 0.5) * cellH,
      angle: rand() * Math.PI,
      shade: (rand() - 0.5) * 18,
      twinWidth: 8 + rand() * 10
    });
  }
}

const NUM_ALPHA = 54;
const alphaGrains = [];
for (let i = 0; i < NUM_ALPHA; i++) {
  alphaGrains.push({ x: rand() * W, y: rand() * H, shade: (rand() - 0.5) * 20 });
}

const NUM_DELTA = 8;
const deltaGrains = [];
for (let i = 0; i < NUM_DELTA; i++) {
  deltaGrains.push({ x: 30 + rand() * (W - 60), y: 30 + rand() * (H - 60), shade: (rand() - 0.5) * 16 });
}

const gammaIdMap = new Int16Array(W * H);
const gammaEdgeDist = new Float32Array(W * H);
const gammaMaxR = new Float32Array(NUM_GAMMA);
const alphaIdMap = new Int16Array(W * H);
const alphaEdgeDist = new Float32Array(W * H);
const deltaIdMap = new Int16Array(W * H);
const deltaEdgeDist = new Float32Array(W * H);

for (let y = 0; y < H; y++) {
  for (let x = 0; x < W; x++) {
    const idx = y * W + x;
    let d1 = 1e9, d2 = 1e9, id1 = 0;
    for (let i = 0; i < NUM_GAMMA; i++) {
      const dx = x - gammaGrains[i].x + 3.0 * Math.sin(y * 0.045 + i);
      const dy = y - gammaGrains[i].y + 3.0 * Math.cos(x * 0.045 + i);
      const d = dx*dx + dy*dy;
      if (d < d1) { d2 = d1; d1 = d; id1 = i; } else if (d < d2) { d2 = d; }
    }
    gammaIdMap[idx] = id1;
    const distEdge = (Math.sqrt(d2) - Math.sqrt(d1)) * 0.5;
    gammaEdgeDist[idx] = distEdge;
    if (distEdge > gammaMaxR[id1]) gammaMaxR[id1] = distEdge;

    d1 = 1e9; d2 = 1e9; id1 = 0;
    for (let i = 0; i < NUM_ALPHA; i++) {
      const dx = x - alphaGrains[i].x + 2.0 * Math.sin(y * 0.07 + i);
      const dy = y - alphaGrains[i].y + 2.0 * Math.cos(x * 0.07 + i);
      const d = dx*dx + dy*dy;
      if (d < d1) { d2 = d1; d1 = d; id1 = i; } else if (d < d2) { d2 = d; }
    }
    alphaIdMap[idx] = id1;
    alphaEdgeDist[idx] = (Math.sqrt(d2) - Math.sqrt(d1)) * 0.5;

    d1 = 1e9; d2 = 1e9; id1 = 0;
    for (let i = 0; i < NUM_DELTA; i++) {
      const dx = x - deltaGrains[i].x + 4.5 * Math.sin(y * 0.03 + i);
      const dy = y - deltaGrains[i].y + 4.5 * Math.cos(x * 0.03 + i);
      const d = dx*dx + dy*dy;
      if (d < d1) { d2 = d1; d1 = d; id1 = i; } else if (d < d2) { d2 = d; }
    }
    deltaIdMap[idx] = id1;
    deltaEdgeDist[idx] = (Math.sqrt(d2) - Math.sqrt(d1)) * 0.5;
  }
}

const gammaNormDist = new Float32Array(W * H);
for (let i = 0; i < W * H; i++) {
  const gId = gammaIdMap[i];
  const maxR = Math.max(1.0, gammaMaxR[gId]);
  gammaNormDist[i] = Math.min(1.0, gammaEdgeDist[i] / maxR);
}

// =========================================================================
// PESTAÑA 1: LÓGICA Y RENDERIZADO Fe-Fe3C
// =========================================================================
let zoomMode = 'full';
const pCanvas = document.getElementById('phaseCanvas');
const pCtx = pCanvas.getContext('2d');
const mCanvas = document.getElementById('microCanvas');
const mCtx = mCanvas.getContext('2d');

function setZoom(mode) {
  zoomMode = mode;
  document.getElementById('btnFull').className = mode === 'full' ? 'radio-btn active' : 'radio-btn';
  document.getElementById('btnAceros').className = mode === 'aceros' ? 'radio-btn active' : 'radio-btn';
  document.getElementById('btnPeri').className = mode === 'peri' ? 'radio-btn active' : 'radio-btn';
  updateAll();
}

function getParams() {
  const C = parseFloat(document.getElementById('slC').value);
  const T = parseFloat(document.getElementById('slT').value);
  const Si = parseFloat(document.getElementById('slSi').value);
  const Cr = parseFloat(document.getElementById('slCr').value);
  const Mn = parseFloat(document.getElementById('slMn').value);
  const Ni = parseFloat(document.getElementById('slNi').value);
  const vel = document.getElementById('selVel').value;
  const trat = document.getElementById('selTrat').value;

  document.getElementById('valC').textContent = C.toFixed(2) + ' %';
  document.getElementById('valT').textContent = T.toFixed(0) + ' °C';
  document.getElementById('valSi').textContent = Si.toFixed(2) + ' %';
  document.getElementById('valCr').textContent = Cr.toFixed(2) + ' %';
  document.getElementById('valMn').textContent = Mn.toFixed(2) + ' %';
  document.getElementById('valNi').textContent = Ni.toFixed(2) + ' %';

  const tA1 = 727.0 - 10.7*Mn - 16.9*Ni + 29.1*Si + 16.9*Cr;
  const cEut = Math.max(0.30, 0.76 - 0.08*Cr - 0.06*Si - 0.03*Mn - 0.02*Ni);
  const cMaxG = Math.max(1.20, 2.11 - 0.15*Si - 0.10*Cr + 0.05*Ni);
  const CE = C + Si / 3.0;
  const Ms = Math.max(50, Math.min(520, 539 - 423*C - 30.4*Mn - 17.7*Ni - 12.1*Cr - 7.5*Si));
  const Mf = Ms - 215;

  return { C, T, Si, Cr, Mn, Ni, vel, trat, tA1, cEut, cMaxG, CE, Ms, Mf };
}

function drawPhaseDiagram(p) {
  const cw = pCanvas.width, ch = pCanvas.height;
  pCtx.clearRect(0, 0, cw, ch);
  
  const padL = 55, padR = 25, padT = 25, padB = 42;
  const plotW = cw - padL - padR;
  const plotH = ch - padT - padB;
  
  let xMin = 0, xMax = 6.85, yMin = 25, yMax = 1600;
  if (zoomMode === 'aceros') { xMax = 2.3; yMin = 25; }
  else if (zoomMode === 'peri') { xMax = 0.85; yMin = 1320; yMax = 1560; }

  const toX = c => padL + ((c - xMin) / (xMax - xMin)) * plotW;
  const toY = t => padT + plotH - ((t - yMin) / (yMax - yMin)) * plotH;

  pCtx.strokeStyle = '#1e293b'; pCtx.lineWidth = 1;
  pCtx.fillStyle = '#94a3b8'; pCtx.font = '11px sans-serif';
  const yStep = zoomMode === 'peri' ? 40 : 200;
  for (let t = Math.ceil(yMin/yStep)*yStep; t <= yMax; t += yStep) {
    const y = toY(t);
    pCtx.beginPath(); pCtx.moveTo(padL, y); pCtx.lineTo(cw - padR, y); pCtx.stroke();
    pCtx.fillText(t + '°', 10, y + 4);
  }
  const xStep = zoomMode === 'peri' ? 0.1 : (zoomMode === 'aceros' ? 0.5 : 1.0);
  for (let c = 0; c <= xMax; c += xStep) {
    const x = toX(c);
    pCtx.beginPath(); pCtx.moveTo(x, padT); pCtx.lineTo(x, ch - padB); pCtx.stroke();
    pCtx.fillText(c.toFixed(zoomMode === 'peri' ? 2 : 1) + '%', x - 14, ch - 20);
  }
  pCtx.fillStyle = '#cbd5e1'; pCtx.font = 'bold 12px sans-serif';
  pCtx.fillText('Carbono (% en peso)', cw/2 - 45, ch - 5);

  function drawLine(pts, color, width=2.5, dash=[]) {
    pCtx.save();
    pCtx.strokeStyle = color; pCtx.lineWidth = width; pCtx.setLineDash(dash);
    pCtx.beginPath();
    pts.forEach((pt, i) => {
      const px = toX(pt[0]), py = toY(pt[1]);
      if (i === 0) pCtx.moveTo(px, py); else pCtx.lineTo(px, py);
    });
    pCtx.stroke();
    pCtx.restore();
  }

  drawLine([[0, 1538], [0.09, 1495], [0, 1394]], '#38bdf8', 2.5);
  drawLine([[0.09, 1495], [0.17, 1495], [0.53, 1495]], '#a78bfa', 3.2);
  drawLine([[0, 1394], [0.17, 1495]], '#818cf8', 2.5);

  drawLine([[0, 1538], [0.53, 1495], [4.30, 1148], [6.67, 1227]], '#f8fafc', 2.5);
  drawLine([[0.17, 1495], [p.cMaxG, 1148]], '#cbd5e1', 2.5);
  drawLine([[p.cMaxG, 1148], [4.30, 1148], [6.67, 1148]], '#fb923c', 3);

  drawLine([[0, 912], [0.022, p.tA1], [0.008, 25]], '#2dd4bf', 2);
  drawLine([[0, 912], [p.cEut, p.tA1]], '#14b8a6', 3);
  drawLine([[p.cEut, p.tA1], [p.cMaxG, 1148]], '#f97316', 3);
  drawLine([[0.022, p.tA1], [6.67, p.tA1]], '#ef4444', 3);
  drawLine([[6.67, 25], [6.67, 1227]], '#64748b', 3);

  if (p.vel === 'rapido' && p.C <= p.cMaxG && zoomMode !== 'peri') {
    drawLine([[0.15, p.Ms], [p.cMaxG, p.Ms]], '#3b82f6', 2, [5, 4]);
    pCtx.fillStyle = '#60a5fa'; pCtx.font = 'bold 11px sans-serif';
    pCtx.fillText(`Ms = ${p.Ms.toFixed(0)}°C`, toX(0.22), toY(p.Ms) - 5);
  }

  if (p.Si >= 1.0 && zoomMode !== 'peri') {
    drawLine([[0.02, 738], [0.68, 738], [2.03, 1154], [4.26, 1154], [6.67, 1600]], '#4ade80', 2, [6, 5]);
    drawLine([[0.02, 738], [6.67, 738]], '#4ade80', 1.8, [6, 5]);
  }

  if (zoomMode === 'peri') {
    pCtx.fillStyle = '#38bdf8'; pCtx.font = 'bold 12px sans-serif';
    pCtx.fillText('δ (Ferrita Delta)', toX(0.01), toY(1475));
    pCtx.fillStyle = '#cbd5e1'; pCtx.font = '11px sans-serif';
    pCtx.fillText('δ + L', toX(0.22), toY(1512));
    pCtx.fillText('δ + γ', toX(0.04), toY(1430));
    pCtx.fillStyle = '#38bdf8'; pCtx.font = 'bold 13px sans-serif';
    pCtx.fillText('γ (Austenita)', toX(0.18), toY(1390));
    pCtx.fillStyle = '#94a3b8';
    pCtx.fillText('γ + L', toX(0.55), toY(1445));
    pCtx.fillText('L (Líquido)', toX(0.55), toY(1525));
  } else {
    pCtx.fillStyle = '#94a3b8'; pCtx.font = 'bold 13px sans-serif';
    pCtx.fillText('L (Líquido)', toX(zoomMode === 'aceros' ? 1.2 : 2.8), toY(1430));
    pCtx.fillStyle = '#38bdf8';
    pCtx.fillText('γ (Austenita)', toX(zoomMode === 'aceros' ? 0.65 : 1.05), toY(1220));
    if (zoomMode === 'full') {
      pCtx.fillStyle = '#cbd5e1'; pCtx.font = '12px sans-serif';
      pCtx.fillText('α + Fe₃C / α + Grafito', toX(3.2), toY(420));
      pCtx.fillText('γ + Fe₃C + Ledeburita', toX(3.6), toY(940));
    }
  }

  const invs = [
    { c: 0.17, t: 1495, col: '#a78bfa', lbl: 'Peritéctico (0.17%C, 1495°C)' },
    { c: 4.30, t: 1148, col: '#fb923c', lbl: 'Eutéctico (4.30%C, 1148°C)' },
    { c: p.cEut, t: p.tA1, col: '#ef4444', lbl: `Eutectoide (${p.cEut.toFixed(2)}%C, ${p.tA1.toFixed(0)}°C)` }
  ];
  invs.forEach(inv => {
    if (inv.c <= xMax && inv.t >= yMin && inv.t <= yMax) {
      pCtx.fillStyle = inv.col;
      pCtx.beginPath(); pCtx.arc(toX(inv.c), toY(inv.t), 5, 0, Math.PI*2); pCtx.fill();
      pCtx.strokeStyle = '#fff'; pCtx.lineWidth = 1; pCtx.stroke();
      pCtx.font = 'bold 11px sans-serif';
      pCtx.fillText(inv.lbl, toX(inv.c) + 7, toY(inv.t) - 6);
    }
  });

  if (p.C <= xMax && p.T >= yMin && p.T <= yMax) {
    const ux = toX(p.C), uy = toY(p.T);
    pCtx.strokeStyle = 'rgba(34, 197, 94, 0.45)'; pCtx.lineWidth = 1.5; pCtx.setLineDash([4,4]);
    pCtx.beginPath(); pCtx.moveTo(ux, padT); pCtx.lineTo(ux, ch - padB); pCtx.stroke();
    pCtx.beginPath(); pCtx.moveTo(padL, uy); pCtx.lineTo(cw - padR, uy); pCtx.stroke();
    pCtx.setLineDash([]);

    pCtx.fillStyle = '#22c55e';
    pCtx.beginPath();
    pCtx.moveTo(ux, uy - 8); pCtx.lineTo(ux + 8, uy); pCtx.lineTo(ux, uy + 8); pCtx.lineTo(ux - 8, uy);
    pCtx.closePath(); pCtx.fill();
    pCtx.strokeStyle = '#ffffff'; pCtx.lineWidth = 2; pCtx.stroke();
  }
}

function analyzeAlloy(p) {
  const { C, T, Si, Cr, Mn, Ni, vel, trat, tA1, cEut, cMaxG, CE, Ms } = p;
  const cAlpha = T >= 400 ? 0.022 : 0.008;
  const cFe3C = 6.67;
  const rhoA = 7.87, rhoC = 7.66, rhoG = 7.69, rhoL = 7.00, rhoGr = 1.50;

  let tLiq = 1538;
  if (C <= 0.53) tLiq = 1538 - (1538 - 1495)*(C / 0.53);
  else if (C <= 4.30) tLiq = 1495 - (1495 - 1148)*((C - 0.53)/(4.30 - 0.53));
  else tLiq = 1148 + (1227 - 1148)*((C - 4.30)/(6.67 - 4.30));

  if (T > tLiq) {
    return {
      mode: 'liquido', desc: 'Líquido Homogéneo (L)',
      fases: [['Líquido (L)', 100, 100]], solidFrac: 0, martFrac: 0, fPro: 0, perl: 0, cemPro: 0,
      story: `Por encima de la temperatura Liquidus (${tLiq.toFixed(0)} °C), toda la aleación con ${C.toFixed(2)}%C está en estado líquido homogéneo.`
    };
  }

  if (T >= 1394 && C <= 0.53) {
    if (T >= 1495) {
      const cDeltaMax = 0.09 * ((1538 - T) / (1538 - 1495));
      const cLiqT = 0.53 * ((1538 - T) / (1538 - 1495));
      if (C <= cDeltaMax) {
        return {
          mode: 'ferrita_delta', desc: 'Ferrita Delta (δ - BCC alta T)',
          fases: [['Ferrita δ (BCC)', 100, 100]], solidFrac: 1, martFrac: 0, fPro: 1, perl: 0, cemPro: 0,
          story: `Con muy bajo carbono (${C.toFixed(2)}%C) entre 1394 °C y 1538 °C, solidifica en red BCC de alta temperatura (Ferrita δ).`
        };
      } else {
        const wD = (cLiqT - C) / Math.max(0.001, (cLiqT - cDeltaMax));
        const wL = 1 - wD;
        const vD = (wD/rhoA)/((wD/rhoA) + (wL/rhoL));
        return {
          mode: 'delta_liq', desc: 'Solidificación: Dendritas δ + Líquido',
          fases: [['Ferrita δ (BCC)', wD*100, vD*100], ['Líquido (L)', wL*100, (1-vD)*100]], solidFrac: vD, martFrac: 0, fPro: wD, perl: 0, cemPro: 0,
          story: `Nuclean dendritas primarias de ferrita δ pobres en carbono, rechazando carbono hacia el líquido interdendrítico.`
        };
      }
    } else {
      const cDeltaT = 0.09 * ((T - 1394) / (1495 - 1394));
      const cGammaT = 0.17 * ((T - 1394) / (1495 - 1394));
      if (C <= cDeltaT) {
        return {
          mode: 'ferrita_delta', desc: 'Ferrita Delta (δ - BCC alta T)',
          fases: [['Ferrita δ (BCC)', 100, 100]], solidFrac: 1, martFrac: 0, fPro: 1, perl: 0, cemPro: 0,
          story: `Campo monofásico de Ferrita δ (BCC) antes de transformarse en austenita γ.`
        };
      } else if (C <= cGammaT) {
        const wD = (cGammaT - C) / Math.max(0.001, (cGammaT - cDeltaT));
        const wG = 1 - wD;
        const vD = (wD/rhoA)/((wD/rhoA) + (wG/rhoG));
        return {
          mode: 'delta_gamma', desc: 'Reacción Peritéctica: Ferrita δ + Austenita γ',
          fases: [['Ferrita δ (BCC)', wD*100, vD*100], ['Austenita γ (FCC)', wG*100, (1-vD)*100]], solidFrac: 1, martFrac: 0, fPro: wD, perl: 0, cemPro: 0,
          story: `Tras cruzar la horizontal peritéctica (1495 °C: δ + L → γ), la austenita γ nuclea sobre los bordes de la ferrita δ.`
        };
      }
    }
  }

  if (T >= 1148 && T <= tLiq) {
    if (C <= 4.30) {
      const cSol = 0.17 + (cMaxG - 0.17)*((1495 - Math.min(T, 1495))/(1495 - 1148));
      const cLiqT = 0.53 + (4.30 - 0.53)*((1495 - Math.min(T, 1495))/(1495 - 1148));
      const wG = Math.max(0.05, Math.min(0.95, (cLiqT - C)/Math.max(0.01, cLiqT - cSol)));
      const wL = 1 - wG;
      const vG = (wG/rhoG)/((wG/rhoG) + (wL/rhoL));
      return {
        mode: 'semisolido_g', desc: 'Solidificación: Dendritas γ + Líquido',
        fases: [['Austenita γ (Dendritas)', wG*100, vG*100], ['Líquido interdendrítico', wL*100, (1-vG)*100]], solidFrac: vG, martFrac: 0, fPro: 0, perl: 0, cemPro: 0,
        story: `Al enfriar bajo Liquidus (${tLiq.toFixed(0)} °C), crecen <b>dendritas arborescentes de austenita γ</b> expulsando carbono hacia el líquido interdendrítico.`
      };
    } else {
      const cLiqT = 4.30 + (6.67 - 4.30)*((T - 1148)/(1227 - 1148));
      const wL = Math.max(0.05, Math.min(0.95, (6.67 - C)/Math.max(0.01, 6.67 - cLiqT)));
      const wC = 1 - wL;
      const vL = (wL/rhoL)/((wL/rhoL) + (wC/rhoC));
      return {
        mode: 'semisolido_c', desc: 'Solidificación Hipereutéctica: Líquido + Fe₃C primaria',
        fases: [['Líquido (L)', wL*100, vL*100], ['Cementita Fe₃C primaria', wC*100, (1-vL)*100]], solidFrac: 1 - vL, martFrac: 0, fPro: 0, perl: 0, cemPro: wC,
        story: `Por ser hipereutéctica (${C.toFixed(2)}%C > 4.30%), nuclean directamente placas alargadas de <b>cementita primaria (Fe₃C)</b> en el líquido.`
      };
    }
  }

  if (C > cMaxG) {
    const ceCritBlanca = (vel === 'rapido' ? 4.35 : (vel === 'moderado' ? 3.85 : 3.25)) + 0.45*Cr + 0.15*Mn - 0.35*Si;
    const ceCritGris = ceCritBlanca + 0.42;

    let tipoF = '', modeF = '', storyF = '';
    if (trat === 'maleable') {
      tipoF = 'Fundición Maleable (Carbono de revenido)'; modeF = 'f_maleable';
      storyF = `Colada inicialmente como <b>fundición blanca</b> y recocida prolongadamente: la Fe₃C se descompuso en rosetas de <b>carbono de revenido</b>.`;
    } else if (trat === 'bainita') {
      tipoF = 'Fundición ADI (Ausferrita + Nódulos)'; modeF = 'f_adi';
      storyF = `Austemperado isotérmico sobre fundición nodular: matriz de <b>ausferrita</b> (ferrita acicular + austenita retenida) con nódulos de grafito.`;
    } else if (trat === 'nodular') {
      if (CE < ceCritBlanca || Cr > 0.8) {
        tipoF = 'Fundición Blanca (Bloqueo de grafitización)'; modeF = 'f_blanca_hipo';
        storyF = `⚠️ Bajo potencial grafitizante (CE=${CE.toFixed(2)}%) o exceso de Cr: el carbono quedó como <b>ledeburita blanca</b>.`;
      } else {
        const isFerritic = (Si >= 2.2 && vel === 'lento');
        tipoF = `Fundición Nodular / Dúctil (${isFerritic ? 'Ojo de buey ferrítico' : 'Matriz perlítica'})`;
        modeF = isFerritic ? 'f_nodular' : 'f_nodular_perl';
        storyF = `Adición de <b>Mg/Ce en cuchara</b>: grafito en <b>nódulos esféricos</b>. ${isFerritic ? 'Con halos blancos de ferrita ("ojo de buey").' : 'En matriz perlítica.'}`;
      }
    } else if (trat === 'vermicular') {
      if (CE < ceCritBlanca || Cr > 0.8) {
        tipoF = 'Fundición Blanca (Sub-grafitizada)'; modeF = 'f_blanca_hipo';
        storyF = `⚠️ Falta Silicio o CE (${CE.toFixed(2)}%) frente a la velocidad de enfriamiento.`;
      } else {
        tipoF = 'Fundición Vermicular (CGI · Grafito compacto)'; modeF = 'f_vermicular';
        storyF = `Grafito en <b>gusanos cortos y redondeados</b> interconectados en la celda eutéctica.`;
      }
    } else {
      if (CE < ceCritBlanca) {
        if (Cr >= 1.5 || CE >= 4.30) {
          tipoF = 'Fundición Blanca Alta en Carburos (ASTM A532)'; modeF = 'f_blanca_hiper';
          storyF = `Efecto carburígeno del Cr (${Cr.toFixed(1)}%): carburos eutécticos blancos alargados en matriz oscura.`;
        } else {
          tipoF = 'Fundición Blanca Hipoeutéctica (Ledeburita + Perlita)'; modeF = 'f_blanca_hipo';
          storyF = `Vía metaestable Fe–Fe₃C: dendritas oscuras de austenita transformada (perlita) en matriz blanca de <b>ledeburita</b>.`;
        }
      } else if (CE <= ceCritGris) {
        tipoF = 'Fundición Atruchada (Transición Blanca–Gris)'; modeF = 'f_atruchada';
        storyF = `Coexisten colonias blancas de <b>ledeburita</b> y <b>láminas oscuras de grafito</b>.`;
      } else {
        const isFerritic = (Si >= 2.35 && vel === 'lento');
        tipoF = `Fundición Gris (Grafito laminar tipo A · matriz ${isFerritic ? 'ferrítica' : 'perlítica'})`;
        modeF = isFerritic ? 'f_gris_ferr' : 'f_gris_perl';
        storyF = `Alto Silicio (${Si.toFixed(2)}%) y enfriamiento ${vel}: gobierna el diagrama estable <b>Fe–Grafito (1154 °C)</b> con láminas de grafito tipo A.`;
      }
    }

    if (modeF.startsWith('f_blanca') || modeF === 'f_atruchada') {
      const wA = (cFe3C - C)/(cFe3C - cAlpha), wC = 1 - wA;
      const vA = (wA/rhoA)/((wA/rhoA) + (wC/rhoC));
      return {
        mode: modeF, desc: tipoF,
        fases: [['Ferrita α (en perlita)', wA*100, vA*100], ['Cementita Fe₃C / Carburos', wC*100, (1-vA)*100]],
        solidFrac: 1, martFrac: 0, fPro: 0, perl: 0.5, cemPro: 0.5, story: storyF
      };
    } else {
      const wM = (100 - C)/(100 - 0.02), wGr = 1 - wM;
      const vM = (wM/rhoA)/((wM/rhoA) + (wGr/rhoGr));
      return {
        mode: modeF, desc: tipoF,
        fases: [['Matriz metálica', wM*100, vM*100], ['Grafito libre (ρ = 1.50 g/cm³)', wGr*100, (1-vM)*100]],
        solidFrac: 1, martFrac: 0, fPro: 0, perl: 0, cemPro: 0, story: storyF
      };
    }
  }

  const tA3 = C <= cEut ? 912 - (912 - tA1)*(C/cEut) : tA1 + (1148 - tA1)*((C - cEut)/(cMaxG - cEut));

  if (trat === 'globulizado' && T < tA1) {
    const wA = (cFe3C - C)/(cFe3C - cAlpha), wC = 1 - wA;
    const vA = (wA/rhoA)/((wA/rhoA) + (wC/rhoC));
    return {
      mode: 'globulizado', desc: 'Acero Globulizado / Esferoidita (α + Fe₃C esferoidal)',
      fases: [['Matriz Ferrita α', wA*100, vA*100], ['Cementita Fe₃C globular', wC*100, (1-vA)*100]],
      solidFrac: 1, martFrac: 0, fPro: 0, perl: 0, cemPro: 0,
      story: `Recocido prolongado bajo A1 (${tA1.toFixed(0)} °C): las láminas de perlita se esferoidizan en <b>glóbulos de cementita</b> en matriz ferrítica blanda.`
    };
  }

  if (trat === 'bainita' && T < 550) {
    return {
      mode: 'bainita', desc: 'Acero Austemperado: Bainita (α acicular + carburos finos)',
      fases: [['Ferrita bainítica sobresaturada', 88, 88], ['Carburos finos dispersos', 12, 12]],
      solidFrac: 1, martFrac: 0, fPro: 0, perl: 0, cemPro: 0,
      story: `Temple escalonado evitando la nariz perlítica hasta la zona intermedia (250–500 °C) antes de Ms (${Ms.toFixed(0)} °C): <b>ferrita bainítica acicular</b>.`
    };
  }

  if (vel === 'rapido' && C > 0.12) {
    if (T > Ms) {
      return {
        mode: 'austenita', desc: `Austenita Subenfriada Metaestable (Sobre Ms = ${Ms.toFixed(0)} °C)`,
        fases: [['Austenita γ subenfriada', 100, 100]],
        solidFrac: 1, martFrac: 0, fPro: 0, perl: 0, cemPro: 0,
        story: `Por encima de <b>Ms (${Ms.toFixed(0)} °C)</b>, la austenita subenfriada aún no inicia la transformación cizallante.`
      };
    } else {
      const fMart = Math.min(0.99, 1 - Math.exp(-0.011 * (Ms - T)));
      const fRet = 1 - fMart;
      const isPlate = C >= 0.60;
      const isRevenido = (trat === 'revenido');
      return {
        mode: isRevenido ? 'martensita_rev' : (isPlate ? 'martensita_placas' : 'martensita_listones'),
        desc: isRevenido
          ? `Martensita Revenida (${isPlate ? 'Placas' : 'Listones'} + carburos ε/Fe₃C)`
          : `Martensita en ${isPlate ? 'Placas Lenticulares (C ≥ 0.6%)' : 'Listones / Agujas (C < 0.6%)'}`,
        fases: [
          [isRevenido ? 'Martensita revenida (α + Fe₃C fino)' : 'Martensita (BCT sobresaturada)', fMart*100, fMart*100],
          ['Austenita retenida (γ_ret)', fRet*100, fRet*100]
        ],
        solidFrac: 1, martFrac: fMart, fPro: 0, perl: 0, cemPro: 0,
        story: isRevenido
          ? `El <b>revenido a 400 °C</b> precipitó carburos muy finos, aliviando tensiones y recuperando tenacidad.`
          : `Transformación sin difusión bajo Ms (${Ms.toFixed(0)} °C) hacia red tetragonal BCT (${(fMart*100).toFixed(1)}% martensita).`
      };
    }
  }

  if (T >= tA3) {
    return {
      mode: 'austenita', desc: 'Acero: Austenita γ (FCC homogénea)',
      fases: [['Austenita γ (FCC)', 100, 100]], solidFrac: 1, martFrac: 0, fPro: 0, perl: 0, cemPro: 0,
      story: `Por encima de ${C <= cEut ? 'A3' : 'Acm'} (${tA3.toFixed(0)} °C), el acero (${C.toFixed(2)}%C) está 100% austenitizado.`
    };
  }

  if (T >= tA1 && T < tA3) {
    if (C < cEut) {
      const cGint = cEut * ((912 - T)/(912 - tA1));
      const cAint = 0.022 * ((912 - T)/(912 - tA1));
      const wA = Math.max(0, Math.min(1, (cGint - C)/Math.max(0.01, cGint - cAint)));
      const wG = 1 - wA;
      const vA = (wA/rhoA)/((wA/rhoA) + (wG/rhoG));
      return {
        mode: 'intercritico_hipo', desc: 'Intercrítico: Ferrita α creciendo en borde γ',
        fases: [['Ferrita α proeutectoide', wA*100, vA*100], ['Austenita γ remanente', wG*100, (1-vA)*100]],
        solidFrac: 1, martFrac: 0, fPro: wA, perl: 0, cemPro: 0,
        story: `Entre A3 (${tA3.toFixed(0)} °C) y A1 (${tA1.toFixed(0)} °C), la <b>ferrita α proeutectoide</b> (${(wA*100).toFixed(1)}%) nuclea en los bordes de grano austenítico.`
      };
    } else {
      const cGint = cEut + (cMaxG - cEut)*((T - tA1)/(1148 - tA1));
      const wG = (cFe3C - C)/(cFe3C - cGint), wC = 1 - wG;
      const vG = (wG/rhoG)/((wG/rhoG) + (wC/rhoC));
      return {
        mode: 'intercritico_hiper', desc: 'Intercrítico: Red Fe₃C creciendo en borde γ',
        fases: [['Austenita γ remanente', wG*100, vG*100], ['Cementita Fe₃C proeutectoide', wC*100, (1-vG)*100]],
        solidFrac: 1, martFrac: 0, fPro: 0, perl: 0, cemPro: wC,
        story: `Entre Acm (${tA3.toFixed(0)} °C) y A1 (${tA1.toFixed(0)} °C), precipita una <b>red blanca continua de cementita proeutectoide</b> (${(wC*100).toFixed(1)}%).`
      };
    }
  }

  if (C <= cAlpha) {
    return {
      mode: 'ferrita_alfa', desc: 'Hierro / Acero Extra Bajo C: Ferrita α poligonal',
      fases: [['Ferrita α (BCC)', 100, 100]], solidFrac: 1, martFrac: 0, fPro: 1, perl: 0, cemPro: 0,
      story: `Con ≤0.022%C, toda la austenita transformó en granos poligonales equiaxiales limpios de <b>ferrita α (BCC)</b>.`
    };
  }

  const wAtot = (cFe3C - C)/(cFe3C - cAlpha), wCtot = 1 - wAtot;
  const vAtot = (wAtot/rhoA)/((wAtot/rhoA) + (wCtot/rhoC));

  if (Math.abs(C - cEut) <= 0.025) {
    return {
      mode: 'perlita_eutectoide', desc: 'Acero Eutectoide: 100% Perlita Laminar (α + Fe₃C)',
      fases: [['Ferrita α (en perlita)', wAtot*100, vAtot*100], ['Cementita Fe₃C (en perlita)', wCtot*100, (1-vAtot)*100]],
      solidFrac: 1, martFrac: 0, fPro: 0, perl: 1, cemPro: 0,
      story: `En la composición eutectoide (${cEut.toFixed(2)}%C), toda la austenita transformó isotérmicamente a A1 (${tA1.toFixed(0)} °C) formando 100% <b>perlita laminar</b>.`
    };
  }

  if (C < cEut) {
    const wPerl = (C - cAlpha)/(cEut - cAlpha);
    const wFpro = 1 - wPerl;
    const isWid = vel === 'moderado';
    return {
      mode: isWid ? 'widmanstatten' : 'hipoeutectoide',
      desc: `Acero Hipoeutectoide (${isWid ? 'Widmanstätten + Perlita' : 'Ferrita alotriomorfa + Perlita'})`,
      fases: [['Ferrita α total', wAtot*100, vAtot*100], ['Cementita Fe₃C total', wCtot*100, (1-vAtot)*100]],
      solidFrac: 1, martFrac: 0, fPro: wFpro, perl: wPerl, cemPro: 0,
      story: `1) Entre A3 y A1, nucleó <b>${(wFpro*100).toFixed(1)}% de ferrita α alotriomorfa</b> blanca en los bordes de grano γ${isWid ? ', proyectando <b>placas de Widmanstätten</b> hacia el interior' : ''}.<br>2) Al cruzar A1, el centro del grano transformó en <b>${(wPerl*100).toFixed(1)}% de perlita laminar oscura</b>.`
    };
  } else {
    const wPerl = (cFe3C - C)/(cFe3C - cEut);
    const wCpro = 1 - wPerl;
    return {
      mode: 'hipereutectoide',
      desc: `Acero Hipereutectoide (Perlita + Red Fe₃C borde)`,
      fases: [['Ferrita α total', wAtot*100, vAtot*100], ['Cementita Fe₃C total', wCtot*100, (1-vAtot)*100]],
      solidFrac: 1, martFrac: 0, fPro: 0, perl: wPerl, cemPro: wCpro,
      story: `1) Entre Acm y A1, precipitó una <b>red blanca continua de cementita proeutectoide (${(wCpro*100).toFixed(1)}% Fe₃C)</b> delineando los antiguos bordes de grano γ.<br>2) Al cruzar A1, el interior transformó en <b>${(wPerl*100).toFixed(1)}% de perlita laminar oscura</b>.`
    };
  }
}

function drawDendrites(ctx, solidFrac, dendColor, liqColor) {
  ctx.fillStyle = liqColor;
  ctx.fillRect(0, 0, W, H);
  const primaryW = 3.5 + solidFrac * 12.0;
  const secW = 2.2 + solidFrac * 8.5;
  const tertW = 1.2 + solidFrac * 4.5;

  const trunks = [
    { x: 75, y: 65, ang: 0.35, len: 135 },
    { x: 245, y: 55, ang: 2.15, len: 145 },
    { x: 385, y: 95, ang: 1.45, len: 130 },
    { x: 115, y: 215, ang: -0.45, len: 140 },
    { x: 295, y: 210, ang: 0.78, len: 145 },
    { x: 205, y: 135, ang: -1.15, len: 115 }
  ];

  ctx.save();
  ctx.strokeStyle = dendColor; ctx.lineCap = 'round';
  trunks.forEach(tr => {
    const cosA = Math.cos(tr.ang), sinA = Math.sin(tr.ang);
    const pCos = Math.cos(tr.ang + Math.PI/2), pSin = Math.sin(tr.ang + Math.PI/2);
    const x1 = tr.x - (tr.len/2)*cosA, y1 = tr.y - (tr.len/2)*sinA;
    const x2 = tr.x + (tr.len/2)*cosA, y2 = tr.y + (tr.len/2)*sinA;

    ctx.lineWidth = primaryW;
    ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();

    const steps = 6;
    for (let s = -steps; s <= steps; s++) {
      if (s === 0) continue;
      const frac = s / (steps + 1);
      const bx = tr.x + frac * (tr.len * 0.46) * cosA;
      const by = tr.y + frac * (tr.len * 0.46) * sinA;
      const secLen = (1 - Math.abs(frac)*0.78) * (32 + solidFrac * 18);

      [-1, 1].forEach(side => {
        const sx2 = bx + side * secLen * pCos;
        const sy2 = by + side * secLen * pSin;
        ctx.lineWidth = secW;
        ctx.beginPath(); ctx.moveTo(bx, by); ctx.lineTo(sx2, sy2); ctx.stroke();

        if (secLen > 18) {
          for (let t = 0.4; t <= 0.75; t += 0.35) {
            const tx = bx + side * secLen * t * pCos;
            const ty = by + side * secLen * t * pSin;
            const tertLen = (1 - t) * (10 + solidFrac * 8);
            ctx.lineWidth = tertW;
            ctx.beginPath();
            ctx.moveTo(tx - tertLen*cosA, ty - tertLen*sinA);
            ctx.lineTo(tx + tertLen*cosA, ty + tertLen*sinA);
            ctx.stroke();
          }
        }
      });
    }
  });
  ctx.restore();
}

// Función genérica de dibujo de micrografía (usada por Pestaña 1 y Pestaña 2)
function renderMicroToCanvas(ctx, m, opts = {}) {
  const solidFrac = opts.solidFrac || 0.5;
  const fPro = opts.fPro || 0;
  const cemPro = opts.cemPro || 0;
  const martFrac = opts.martFrac || 0.96;
  const lamFreq = opts.lamFreq || 1.35;
  const CE = opts.CE || 4.0;

  if (m === 'semisolido_g') {
    drawDendrites(ctx, solidFrac, '#cbd5e1', '#d97706');
    drawScaleBar(ctx, 'Sin ataque · 100×');
    return;
  }
  if (m === 'delta_liq') {
    drawDendrites(ctx, solidFrac, '#fde68a', '#ea580c');
    drawScaleBar(ctx, 'Sin ataque · 100×');
    return;
  }

  const imgData = ctx.createImageData(W, H);
  const data = imgData.data;

  const normFerriteThickness = 1.0 - Math.sqrt(Math.max(0.0, 1.0 - fPro));
  const normCemThickness = Math.max(0.04, 1.0 - Math.sqrt(Math.max(0.0, 1.0 - cemPro * 1.4)));

  for (let y = 0; y < H; y++) {
    for (let x = 0; x < W; x++) {
      const idx = y * W + x;
      const pIdx = idx * 4;
      const grainNoise = ((Math.sin(x*12.9898 + y*78.233) * 43758.5453) % 1) * 9;
      let r = 210, gr = 204, b = 190;

      if (m === 'liquido') {
        const wave = Math.sin(x*0.05 + y*0.04)*15;
        r = 235 + wave; gr = 100 + wave; b = 30;
      }
      else if (m === 'ferrita_delta' || m === 'delta_gamma') {
        const dId = deltaIdMap[idx];
        const dg = deltaGrains[dId];
        const dDist = deltaEdgeDist[idx];
        if (m === 'delta_gamma' && dDist < (1 - fPro)*12) {
          const gId = gammaIdMap[idx];
          const base = 185 + gammaGrains[gId].shade + grainNoise;
          r = base - 10; gr = base; b = base + 22;
        } else {
          const base = 232 + dg.shade + grainNoise;
          if (dDist < 1.3) { r = 80; gr = 55; b = 35; }
          else { r = base; gr = base - 14; b = base - 36; }
        }
      }
      else if (m === 'austenita') {
        const gId = gammaIdMap[idx];
        const gg = gammaGrains[gId];
        const gDist = gammaEdgeDist[idx];
        const u = (x - gg.x)*Math.cos(gg.angle) + (y - gg.y)*Math.sin(gg.angle);
        const isTwin = (u > -gg.twinWidth && u < 0) || (u > gg.twinWidth*1.4 && u < gg.twinWidth*2.1);
        const base = (isTwin ? 168 : 204) + gg.shade + grainNoise;
        if (gDist < 1.1) { r = 35; gr = 42; b = 55; }
        else { r = base - 12; gr = base - 4; b = base + 14; }
      }
      else if (m === 'ferrita_alfa' || m === 'globulizado') {
        const aId = alphaIdMap[idx];
        const ag = alphaGrains[aId];
        const aDist = alphaEdgeDist[idx];
        const base = 234 + ag.shade*0.7 + grainNoise;
        if (aDist < 0.9 && m === 'ferrita_alfa') { r = 55; gr = 58; b = 68; }
        else { r = base; gr = base - 2; b = base - 4; }
      }
      else if (m === 'perlita_eutectoide' || m === 'perlita_gruesa' || m === 'perlita_fina') {
        const gId = gammaIdMap[idx];
        const gg = gammaGrains[gId];
        const freq = m === 'perlita_gruesa' ? 0.95 : (m === 'perlita_fina' ? 2.15 : lamFreq);
        const u = x * Math.cos(gg.angle) + y * Math.sin(gg.angle);
        const lam = Math.sin(u * freq + Math.sin(y*0.06)*1.8);
        const val = lam > 0 ? (212 + grainNoise) : (42 + grainNoise);
        r = val; gr = val - 2; b = val - 4;
      }
      else if (m === 'perlita_martensita') {
        const gId = gammaIdMap[idx];
        const gg = gammaGrains[gId];
        const gDist = gammaEdgeDist[idx];
        if (gDist < 9.5) {
          // Perlita fina nucleada en bordes de grano gamma
          const u = x * Math.cos(gg.angle) + y * Math.sin(gg.angle);
          const lam = Math.sin(u * 2.1 + Math.sin(y*0.06)*1.5);
          const val = lam > 0 ? (150 + grainNoise) : (32 + grainNoise);
          r = val; gr = val; b = val;
        } else {
          // Interior transformado en placas de martensita
          const u = x * Math.cos(gg.angle) + y * Math.sin(gg.angle);
          const v = -x * Math.sin(gg.angle) + y * Math.cos(gg.angle);
          const p1 = Math.abs(Math.sin(u * 0.34 + v * 0.22));
          const p2 = Math.abs(Math.cos(u * 0.24 - v * 0.36));
          const val = (p1 < 0.26 || p2 < 0.26) ? (95 + grainNoise) : (182 + grainNoise);
          r = val + 8; gr = val + 2; b = val - 6;
        }
      }
      else if (m === 'hipoeutectoide' || m === 'widmanstatten' || m === 'intercritico_hipo') {
        const gId = gammaIdMap[idx];
        const gg = gammaGrains[gId];
        const normD = gammaNormDist[idx];
        
        if (normD < normFerriteThickness) {
          const aDist = alphaEdgeDist[idx];
          const base = 238 + grainNoise*0.6;
          if (aDist < 0.7 && fPro > 0.35) { r = 185; gr = 188; b = 194; }
          else { r = base; gr = base - 1; b = base - 2; }
        } else if (m === 'intercritico_hipo') {
          const u = (x - gg.x)*Math.cos(gg.angle) + (y - gg.y)*Math.sin(gg.angle);
          const isTwin = (u > -gg.twinWidth && u < 0);
          const base = (isTwin ? 148 : 178) + gg.shade + grainNoise;
          r = base - 10; gr = base - 4; b = base + 12;
        } else {
          const u = x * Math.cos(gg.angle) + y * Math.sin(gg.angle);
          const lam = Math.sin(u * lamFreq + Math.sin(y*0.05)*1.5);
          const val = lam > 0 ? (158 + grainNoise) : (32 + grainNoise);
          r = val; gr = val - 2; b = val - 4;
        }
      }
      else if (m === 'hipereutectoide' || m === 'intercritico_hiper') {
        const gId = gammaIdMap[idx];
        const gg = gammaGrains[gId];
        const normD = gammaNormDist[idx];
        
        if (normD < normCemThickness) {
          r = 250; gr = 250; b = 248;
        } else if (m === 'intercritico_hiper') {
          const u = (x - gg.x)*Math.cos(gg.angle) + (y - gg.y)*Math.sin(gg.angle);
          const isTwin = (u > -gg.twinWidth && u < 0);
          const base = (isTwin ? 145 : 175) + gg.shade + grainNoise;
          r = base - 10; gr = base - 4; b = base + 12;
        } else {
          const u = x * Math.cos(gg.angle) + y * Math.sin(gg.angle);
          const lam = Math.sin(u * 1.25 + Math.sin(y*0.05));
          const val = lam > 0 ? (122 + grainNoise) : (42 + grainNoise);
          r = val; gr = val - 2; b = val - 3;
        }
      }
      else if (m === 'martensita_listones' || m === 'martensita_placas' || m === 'martensita_rev') {
        const gId = gammaIdMap[idx];
        const gg = gammaGrains[gId];
        const gDist = gammaEdgeDist[idx];
        
        if (m === 'martensita_listones') {
          const u = x * Math.cos(gg.angle) + y * Math.sin(gg.angle);
          const v = -x * Math.sin(gg.angle) + y * Math.cos(gg.angle);
          const lath = Math.sin(u * 1.65 + Math.sin(v * 0.12) * 1.5);
          const packet = Math.sin(v * 0.18 + gId);
          let val = (lath * packet > 0.12) ? (72 + grainNoise) : (175 + grainNoise);
          if (gDist < 0.8) val = 45;
          r = val + 6; gr = val; b = val - 8;
        } else {
          const u = x * Math.cos(gg.angle) + y * Math.sin(gg.angle);
          const v = -x * Math.sin(gg.angle) + y * Math.cos(gg.angle);
          const p1 = Math.abs(Math.sin(u * 0.34 + v * 0.22));
          const p2 = Math.abs(Math.cos(u * 0.24 - v * 0.36));
          
          if (p1 < 0.26 || p2 < 0.26) {
            const val = m === 'martensita_rev' ? (68 + grainNoise) : (102 + grainNoise);
            r = val + 12; gr = val + 2; b = val - 12;
          } else {
            const isRetained = (p1 * p2 > 0.42) && (martFrac < 0.94 || m === 'martensita_placas');
            if (isRetained && m !== 'martensita_rev') {
              r = 236 + grainNoise*0.5; gr = 236 + grainNoise*0.5; b = 234 + grainNoise*0.5;
            } else {
              const val = m === 'martensita_rev' ? (125 + grainNoise) : (165 + grainNoise);
              r = val + 8; gr = val + 2; b = val - 6;
            }
          }
        }
      }
      else if (m === 'bainita' || m === 'bainita_sup' || m === 'bainita_inf') {
        const gId = gammaIdMap[idx];
        const gg = gammaGrains[gId];
        const u = x * Math.cos(gg.angle) + y * Math.sin(gg.angle);
        const v = -x * Math.sin(gg.angle) + y * Math.cos(gg.angle);
        if (m === 'bainita_inf') {
          // Agujas cruzadas muy finas (Bainita inferior)
          const n1 = Math.abs(Math.sin(u * 0.85 + v * 0.55));
          const n2 = Math.abs(Math.cos(u * 0.55 - v * 0.85));
          const val = (n1 < 0.22 || n2 < 0.22) ? (58 + grainNoise) : (175 + grainNoise);
          r = val; gr = val; b = val + 4;
        } else {
          // Plumas paralelas (Bainita superior)
          const feather = Math.sin(u * 0.75 + Math.sin(v * 0.25)*2.5);
          const val = feather > 0.05 ? (62 + grainNoise) : (198 + grainNoise);
          r = val; gr = val; b = val;
        }
      }
      else if (m === 'f_gris_ferr') {
        const aId = alphaIdMap[idx];
        const aDist = alphaEdgeDist[idx];
        const base = 228 + alphaGrains[aId].shade*0.7 + grainNoise;
        if (aDist < 0.8) { r = 130; gr = 130; b = 128; }
        else { r = base; gr = base - 3; b = base - 8; }
      }
      else if (m === 'f_gris_perl' || m === 'f_vermicular' || m === 'f_nodular_perl' || m === 'f_maleable') {
        const gId = gammaIdMap[idx];
        const gg = gammaGrains[gId];
        const u = x * Math.cos(gg.angle) + y * Math.sin(gg.angle);
        const val = 158 + Math.sin(u * 1.15)*28 + grainNoise;
        r = val; gr = val - 4; b = val - 8;
      }
      else if (m === 'f_nodular') {
        const gId = gammaIdMap[idx];
        const gg = gammaGrains[gId];
        const u = x * Math.cos(gg.angle) + y * Math.sin(gg.angle);
        const val = 115 + Math.sin(u * 1.15)*25 + grainNoise;
        r = val; gr = val - 2; b = val - 4;
      }
      else if (m === 'f_atruchada') {
        const zone = Math.sin(x*0.032 + Math.sin(y*0.025)*1.5) + Math.cos(y*0.032);
        if (zone > 0.25) {
          const led = Math.sin(x*0.35)*Math.cos(y*0.35);
          const v = led > -0.1 ? 242 : 55;
          r = v; gr = v; b = v;
        } else {
          const base = 165 + grainNoise;
          r = base; gr = base - 4; b = base - 10;
        }
      }
      else if (m === 'f_adi') {
        const n1 = Math.sin((x*0.8 + y*0.6)*0.55);
        const n2 = Math.cos((x*0.6 - y*0.8)*0.55);
        const val = Math.abs(n1 * n2) > 0.32 ? (82 + grainNoise) : (192 + grainNoise);
        r = val; gr = val; b = val;
      }
      else if (m === 'f_blanca_hipo') {
        const dend = Math.sin(x*0.065 + Math.sin(y*0.04)*2) * Math.cos(y*0.065 + Math.cos(x*0.04)*2);
        const val = dend > 0.14 ? (58 + grainNoise) : (242 + grainNoise*0.4);
        r = val; gr = val - 2; b = val - 4;
      }
      else if (m === 'f_blanca_hiper' || m === 'semisolido_c') {
        const gId = gammaIdMap[idx];
        const val = m === 'semisolido_c' ? 215 : (75 + gammaGrains[gId].shade*0.6 + grainNoise);
        r = val; gr = m === 'semisolido_c' ? 115 : val; b = m === 'semisolido_c' ? 35 : (val + 2);
      }

      data[pIdx] = Math.max(0, Math.min(255, r));
      data[pIdx+1] = Math.max(0, Math.min(255, gr));
      data[pIdx+2] = Math.max(0, Math.min(255, b));
      data[pIdx+3] = 255;
    }
  }
  ctx.putImageData(imgData, 0, 0);

  ctx.save();
  if (m === 'globulizado') {
    for (let i = 0; i < 160; i++) {
      const gx = 12 + ((i * 73) % (W - 24));
      const gy = 12 + ((i * 47) % (H - 24));
      const rad = 2.8 + (i % 3)*1.1;
      ctx.fillStyle = '#e2e8f0'; ctx.strokeStyle = '#1e293b'; ctx.lineWidth = 1.4;
      ctx.beginPath(); ctx.arc(gx, gy, rad, 0, Math.PI*2); ctx.fill(); ctx.stroke();
    }
  }
  else if (m === 'widmanstatten') {
    ctx.strokeStyle = 'rgba(245, 245, 242, 0.96)';
    ctx.lineWidth = 2.2;
    for (let i = 0; i < NUM_GAMMA; i++) {
      const gg = gammaGrains[i];
      const maxR = gammaMaxR[i];
      const rStart = maxR * (1.0 - normFerriteThickness * 0.85);
      const plateLen = Math.min(22, rStart * 0.65);
      if (plateLen > 4) {
        for (let k = -2; k <= 2; k++) {
          const bx = gg.x + Math.cos(gg.angle + Math.PI/2)*rStart + k*6*Math.cos(gg.angle);
          const by = gg.y + Math.sin(gg.angle + Math.PI/2)*rStart + k*6*Math.sin(gg.angle);
          ctx.beginPath();
          ctx.moveTo(bx, by);
          ctx.lineTo(bx - plateLen*Math.cos(gg.angle + 0.5), by - plateLen*Math.sin(gg.angle + 0.5));
          ctx.stroke();
        }
      }
    }
  }
  else if (m === 'f_gris_ferr' || m === 'f_gris_perl' || m === 'f_atruchada') {
    const count = m === 'f_atruchada' ? 18 : Math.round(28 + (CE - 2.5)*14);
    for (let i = 0; i < count; i++) {
      const gx = 20 + ((i * 97) % (W - 40));
      const gy = 20 + ((i * 53) % (H - 40));
      if (m === 'f_atruchada') {
        const zone = Math.sin(gx*0.032 + Math.sin(gy*0.025)*1.5) + Math.cos(gy*0.032);
        if (zone > 0.25) continue;
      }
      const ang = (i * 1.7) % (Math.PI * 2);
      const len = 36 + (i % 4)*10;
      ctx.beginPath();
      ctx.moveTo(gx, gy);
      ctx.bezierCurveTo(
        gx + len*0.3*Math.cos(ang) - 8, gy + len*0.3*Math.sin(ang) + 8,
        gx + len*0.7*Math.cos(ang) + 8, gy + len*0.7*Math.sin(ang) - 8,
        gx + len*Math.cos(ang), gy + len*Math.sin(ang)
      );
      ctx.strokeStyle = '#18181b'; ctx.lineWidth = 2.8; ctx.lineCap = 'round'; ctx.stroke();
    }
  }
  else if (m === 'f_vermicular') {
    for (let i = 0; i < 42; i++) {
      const gx = 20 + ((i * 83) % (W - 40));
      const gy = 20 + ((i * 61) % (H - 40));
      const ang = (i * 2.1);
      ctx.beginPath();
      ctx.moveTo(gx, gy);
      ctx.quadraticCurveTo(gx + 10*Math.cos(ang) + 5, gy + 10*Math.sin(ang) - 5, gx + 20*Math.cos(ang), gy + 20*Math.sin(ang));
      ctx.strokeStyle = '#18181b'; ctx.lineWidth = 4.6; ctx.lineCap = 'round'; ctx.stroke();
    }
  }
  else if (m === 'f_nodular' || m === 'f_nodular_perl' || m === 'f_adi') {
    for (let i = 0; i < 20; i++) {
      const nx = 32 + ((i * 113) % (W - 64));
      const ny = 30 + ((i * 79) % (H - 60));
      const rad = 8 + (i % 4)*2;
      if (m === 'f_nodular') {
        ctx.fillStyle = 'rgba(248, 248, 245, 0.96)';
        ctx.beginPath(); ctx.arc(nx, ny, rad * 1.95, 0, Math.PI*2); ctx.fill();
        ctx.strokeStyle = '#475569'; ctx.lineWidth = 0.9; ctx.stroke();
      }
      const grad = ctx.createRadialGradient(nx - 2, ny - 2, 1, nx, ny, rad);
      grad.addColorStop(0, '#475569'); grad.addColorStop(1, '#090d16');
      ctx.fillStyle = grad;
      ctx.beginPath(); ctx.arc(nx, ny, rad, 0, Math.PI*2); ctx.fill();
    }
  }
  else if (m === 'f_maleable') {
    for (let i = 0; i < 22; i++) {
      const nx = 30 + ((i * 107) % (W - 60));
      const ny = 28 + ((i * 71) % (H - 56));
      ctx.fillStyle = '#18181b';
      for (let k = 0; k < 6; k++) {
        ctx.beginPath(); ctx.arc(nx + Math.cos(k)*5, ny + Math.sin(k)*5, 4.5, 0, Math.PI*2); ctx.fill();
      }
    }
  }
  else if (m === 'f_blanca_hiper' || m === 'semisolido_c') {
    ctx.fillStyle = '#f8fafc'; ctx.strokeStyle = '#94a3b8'; ctx.lineWidth = 1;
    for (let i = 0; i < 32; i++) {
      const cx = (i * 97) % W, cy = (i * 67) % H;
      ctx.save(); ctx.translate(cx, cy); ctx.rotate((i * 0.75) % Math.PI);
      ctx.fillRect(-38, -4.5, 76, 9); ctx.strokeRect(-38, -4.5, 76, 9);
      ctx.restore();
    }
  }
  ctx.restore();
  drawScaleBar(ctx, 'Ataque Nital 3% · 500×');
}

function drawScaleBar(ctx, etchText) {
  ctx.save();
  ctx.fillStyle = 'rgba(15, 23, 42, 0.85)';
  ctx.fillRect(W - 105, H - 32, 95, 24);
  ctx.fillStyle = '#ffffff';
  ctx.fillRect(W - 95, H - 16, 50, 3);
  ctx.font = 'bold 10px sans-serif';
  ctx.fillText('20 µm · 500×', W - 95, H - 20);
  ctx.restore();
}

function drawMicrograph(p, res) {
  const freq = p.vel === 'moderado' ? 1.85 : 1.25;
  renderMicroToCanvas(mCtx, res.mode, {
    solidFrac: res.solidFrac, fPro: res.fPro, cemPro: res.cemPro,
    martFrac: res.martFrac, lamFreq: freq, CE: p.CE
  });
  document.getElementById('microTitle').textContent = res.desc;
  const obsMap = {
    'semisolido_g': 'Dendritas primarias de austenita γ inmersas en líquido interdendrítico.',
    'delta_liq': 'Dendritas gruesas de ferrita δ en crecimiento dentro del líquido de alta temperatura.',
    'ferrita_delta': 'Granos muy gruesos de Ferrita Delta (δ - BCC de alta temperatura, 1394–1538 °C).',
    'delta_gamma': 'Reacción Peritéctica: la austenita γ nuclea sobre los bordes de la ferrita δ.',
    'austenita': 'Austenita γ (FCC): granos equiaxiales con maclas de recocido.',
    'ferrita_alfa': 'Ferrita α poligonal: granos equiaxiales claros con bordes finos.',
    'perlita_eutectoide': 'Perlita 100% laminar: láminas alternadas de ferrita clara y cementita oscura.',
    'hipoeutectoide': 'Ferrita alotriomorfa blanca nucleada en los antiguos bordes de grano γ rodeando islas oscuras de perlita.',
    'intercritico_hipo': 'Zona intercrítica (A1–A3): crecimiento de ferrita proeutectoide desde los bordes hacia el interior de γ.',
    'widmanstatten': 'Ferrita proeutectoide en borde con placas de Widmanstätten proyectadas al interior del grano.',
    'hipereutectoide': 'Red blanca delgada y continua de cementita proeutectoide en antiguos bordes γ + interior perlítico.',
    'intercritico_hiper': 'Zona intercrítica (A1–Acm): red de cementita blanca precipitando en bordes de grano γ.',
    'globulizado': 'Esferoidita: glóbulos de cementita dispersos en matriz ferrítica blanda.',
    'bainita': 'Bainita: plumas/listones aciculares de ferrita bainítica con carburos finos.',
    'martensita_listones': 'Martensita en Listones (C < 0.6%): paquetes de finas agujas paralelas (BCT).',
    'martensita_placas': 'Martensita en Placas (C ≥ 0.6%): placas anchas entrecruzadas en zig-zag + austenita retenida.',
    'martensita_rev': 'Martensita Revenida: carburos finos precipitados oscurecen las placas al ataque.',
    'f_gris_ferr': 'Fundición Gris ferrítica: láminas curvas de grafito tipo A en matriz clara de ferrita α.',
    'f_gris_perl': 'Fundición Gris perlítica: láminas oscuras de grafito tipo A en matriz perlítica.',
    'f_nodular': 'Fundición Nodular ("Ojo de buey"): nódulos esféricos de grafito con halos blancos de ferrita en matriz perlítica.',
    'f_nodular_perl': 'Fundición Nodular perlítica: nódulos esféricos de grafito en matriz oscura de perlita.',
    'f_adi': 'Fundición ADI: nódulos de grafito en matriz acicular de ausferrita.',
    'f_vermicular': 'Fundición Vermicular (CGI): grafito compacto en forma de gusanos cortos.',
    'f_maleable': 'Fundición Maleable: rosetas irregulares de carbono de revenido.',
    'f_blanca_hipo': 'Fundición Blanca hipoeutéctica: dendritas oscuras de perlita en matriz blanca continua de ledeburita.',
    'f_blanca_hiper': 'Fundición Blanca alta en carburos: placas blancas de carburos eutécticos en matriz oscura.',
    'f_atruchada': 'Fundición Atruchada: colonias blancas de ledeburita mezcladas con láminas de grafito.'
  };
  document.getElementById('microDesc').textContent = obsMap[res.mode] || '';
}

function updatePanels(p, res) {
  document.getElementById('mA1').textContent = p.tA1.toFixed(0) + ' °C';
  document.getElementById('mA1d').textContent = `Ms: ${p.Ms.toFixed(0)} °C | Mf: ${Math.max(25, p.Mf).toFixed(0)} °C`;
  document.getElementById('mCeut').textContent = p.cEut.toFixed(2) + ' %';
  document.getElementById('mCE').textContent = p.CE.toFixed(2) + ' %';
  document.getElementById('estadoTexto').textContent = res.desc;

  let htmlPal = '';
  res.fases.forEach(f => {
    htmlPal += `<div class="phase-item"><span><b>${f[0]}</b></span><span><b>${f[1].toFixed(1)}%</b> masa | <b>${f[2].toFixed(1)}%</b> vol.</span></div>`;
  });
  if (p.T < p.tA1 && p.C <= p.cMaxG && p.vel !== 'rapido' && p.trat === 'ninguno' && p.C > 0.022) {
    htmlPal += `<div style="margin-top:8px; font-size:0.78rem; color:#38bdf8; font-weight:700;">Microconstituyentes:</div>`;
    htmlPal += `<div class="phase-item"><span>Ferrita proeutectoide (borde)</span><span><b>${(res.fPro*100).toFixed(1)}%</b></span></div>`;
    htmlPal += `<div class="phase-item"><span>Perlita (89% α + 11% Fe₃C)</span><span><b>${(res.perl*100).toFixed(1)}%</b></span></div>`;
    htmlPal += `<div class="phase-item"><span>Cementita proeutectoide (red)</span><span><b>${(res.cemPro*100).toFixed(1)}%</b></span></div>`;
  }
  document.getElementById('palancaLista').innerHTML = htmlPal;
  document.getElementById('historiaBox').innerHTML = `<div style="color:#38bdf8; font-weight:700; margin-bottom:4px;">📖 ¿Cómo se formó esta microestructura?</div>${res.story}`;

  let htmlAl = '';
  if (p.Si > 0.4) htmlAl += `<div class="aleante-box" style="border-color:#38bdf8;"><b>Silicio (${p.Si.toFixed(2)}%):</b> Alfágeno sustitucional. Desestabiliza la Fe₃C y promueve el diagrama estable Fe–Grafito.</div>`;
  if (p.Cr > 0.1) htmlAl += `<div class="aleante-box" style="border-color:#f97316;"><b>Cromo (${p.Cr.toFixed(2)}%):</b> Alfágeno carburígeno. Aumenta templabilidad y forma carburos duros.</div>`;
  if (p.Mn > 0.8) htmlAl += `<div class="aleante-box" style="border-color:#22c55e;"><b>Manganeso (${p.Mn.toFixed(2)}%):</b> Gamágeno sustitucional. Baja A1 y Ms, aumenta templabilidad.</div>`;
  if (p.Ni > 0.1) htmlAl += `<div class="aleante-box" style="border-color:#a855f7;"><b>Níquel (${p.Ni.toFixed(2)}%):</b> Gamágeno disuelto en matriz; baja A1 y Ms y mejora tenacidad.</div>`;
  document.getElementById('aleantesLista').innerHTML = htmlAl;
}

function updateAll() {
  const p = getParams();
  const res = analyzeAlloy(p);
  drawPhaseDiagram(p);
  drawMicrograph(p, res);
  updatePanels(p, res);
}

['slC', 'slT', 'slSi', 'slCr', 'slMn', 'slNi'].forEach(id => {
  document.getElementById(id).addEventListener('input', updateAll);
});
['selVel', 'selTrat'].forEach(id => {
  document.getElementById(id).addEventListener('change', updateAll);
});

// =========================================================================
// PESTAÑA 2: DIAGRAMA TTT Y MICROESTRUCTURAS FUERA DEL EQUILIBRIO
// =========================================================================
const tttCanvas = document.getElementById('tttCanvas');
const tttCtx = tttCanvas.getContext('2d');
const tttMicroCanvas = document.getElementById('tttMicroCanvas');
const tttMicroCtx = tttMicroCanvas.getContext('2d');

function updateTTT() {
  const ruta = document.getElementById('tttRuta').value;
  const C = parseFloat(document.getElementById('tttSlC').value);
  const Al = parseFloat(document.getElementById('tttSlAl').value);
  const tHold = parseFloat(document.getElementById('tttSlTime').value);

  document.getElementById('tttValC').textContent = C.toFixed(2) + ' %';
  document.getElementById('tttValAl').textContent = Al.toFixed(2) + ' %';
  document.getElementById('tttValTime').textContent = tHold + ' s';

  const cw = tttCanvas.width, ch = tttCanvas.height;
  tttCtx.clearRect(0, 0, cw, ch);

  const padL = 60, padR = 30, padT = 28, padB = 45;
  const plotW = cw - padL - padR;
  const plotH = ch - padT - padB;

  // Eje X logarítmico: 10^-1 (0.1s) a 10^5 (100000s) -> log10 de -1 a 5
  const logMin = -1, logMax = 5;
  const tMin = 50, tMax = 850;
  const toX = sec => padL + ((Math.log10(Math.max(0.1, sec)) - logMin) / (logMax - logMin)) * plotW;
  const toY = temp => padT + plotH - ((temp - tMin) / (tMax - tMin)) * plotH;

  // Grilla
  tttCtx.strokeStyle = '#1e293b'; tttCtx.lineWidth = 1;
  tttCtx.fillStyle = '#94a3b8'; tttCtx.font = '11px sans-serif';
  for (let t = 100; t <= 800; t += 100) {
    const y = toY(t);
    tttCtx.beginPath(); tttCtx.moveTo(padL, y); tttCtx.lineTo(cw - padR, y); tttCtx.stroke();
    tttCtx.fillText(t + '°', 14, y + 4);
  }
  const decs = [0.1, 1, 10, 100, 1000, 10000, 100000];
  const decLabels = ['10⁻¹', '10⁰ (1s)', '10¹', '10²', '10³', '10⁴', '10⁵'];
  decs.forEach((d, i) => {
    const x = toX(d);
    tttCtx.beginPath(); tttCtx.moveTo(x, padT); tttCtx.lineTo(x, ch - padB); tttCtx.stroke();
    tttCtx.fillText(decLabels[i], x - 14, ch - 22);
  });
  tttCtx.fillStyle = '#cbd5e1'; tttCtx.font = 'bold 12px sans-serif';
  tttCtx.fillText('Tiempo (segundos, escala logarítmica)', cw/2 - 95, ch - 5);

  // Temperaturas críticas dinámicas
  const A1 = 727;
  const Ms = Math.max(80, Math.min(480, 539 - 423*C - 35*Al));
  const Mf = Math.max(25, Ms - 190);
  // Desplazamiento logarítmico de la nariz perlítica por templabilidad (%C + aleantes)
  const shiftLog = (C - 0.76)*0.7 + Al*0.42;

  // Líneas horizontales A1, Ms, Mf
  function hLine(temp, col, lbl, dash=[]) {
    const y = toY(temp);
    tttCtx.save();
    tttCtx.strokeStyle = col; tttCtx.lineWidth = 2; tttCtx.setLineDash(dash);
    tttCtx.beginPath(); tttCtx.moveTo(padL, y); tttCtx.lineTo(cw - padR, y); tttCtx.stroke();
    tttCtx.fillStyle = col; tttCtx.font = 'bold 11px sans-serif';
    tttCtx.fillText(lbl, cw - padR - 115, y - 5);
    tttCtx.restore();
  }
  hLine(A1, '#ef4444', `A1 = ${A1} °C`);
  hLine(Ms, '#3b82f6', `Ms = ${Ms.toFixed(0)} °C`);
  hLine(Mf, '#60a5fa', `Mf = ${Mf.toFixed(0)} °C`, [4, 4]);

  // Curvas "C" de Inicio (Ps) y Fin (Pf)
  function getStartSec(temp) {
    if (temp >= A1 - 12 || temp <= Ms) return null;
    const dNose = (temp - 545) / 145;
    const baseLog = 0.05 + 1.55 * dNose * dNose + shiftLog;
    return Math.pow(10, baseLog);
  }
  function getEndSec(temp) {
    const s = getStartSec(temp);
    if (!s) return null;
    return s * (12 + Math.max(0, (680 - temp)*0.03));
  }

  function drawCCurve(fnSec, color, dash=[]) {
    tttCtx.save();
    tttCtx.strokeStyle = color; tttCtx.lineWidth = 3; tttCtx.setLineDash(dash);
    tttCtx.beginPath();
    let started = false;
    for (let temp = A1 - 15; temp >= Ms + 5; temp -= 5) {
      const sec = fnSec(temp);
      if (sec && sec <= 100000) {
        const px = toX(sec), py = toY(temp);
        if (!started) { tttCtx.moveTo(px, py); started = true; }
        else tttCtx.lineTo(px, py);
      }
    }
    tttCtx.stroke();
    tttCtx.restore();
  }
  drawCCurve(getStartSec, '#38bdf8');
  drawCCurve(getEndSec, '#f97316', [6, 4]);

  // Etiquetas de campos en el diagrama TTT
  const noseSec = getStartSec(545) || 1.1;
  const midX = toX(Math.min(25000, noseSec * 4.5));
  tttCtx.fillStyle = '#cbd5e1'; tttCtx.font = 'bold 12px sans-serif';
  tttCtx.fillText('Austenita γ estable', padL + 20, toY(775));
  tttCtx.fillStyle = '#94a3b8'; tttCtx.font = '11px sans-serif';
  tttCtx.fillText('γ inestable', padL + 15, toY(600));
  if (midX < cw - 120) {
    tttCtx.fillStyle = '#f8fafc'; tttCtx.font = 'bold 11px sans-serif';
    tttCtx.fillText('Perlita Gruesa', midX, toY(665));
    tttCtx.fillText('Perlita Fina', midX - 10, toY(545));
    tttCtx.fillText('Bainita', midX, toY(370));
  }
  tttCtx.fillStyle = '#60a5fa'; tttCtx.font = 'bold 12px sans-serif';
  tttCtx.fillText('Martensita (transformación atérmica)', padL + 20, toY((Ms + Mf)/2));

  // Dibujar trayectoria de la ruta seleccionada
  let pts = [];
  let microMode = 'perlita_gruesa', titleM = '', descM = '', storyM = '';
  let T_trans = 680, S_val = '0.45 µm', S_sub = 'Perlita gruesa', hrc = '18–22 HRC', hv = '~225 HV';
  let fasesTTT = [];

  if (ruta === 'recocido') {
    T_trans = 680;
    pts = [[0.1, 800], [5, 730], [50, 690], [Math.max(400, tHold), 665], [Math.max(1500, tHold*2), 300]];
    microMode = 'perlita_gruesa';
    titleM = 'Perlita Gruesa (Recocido Completo)';
    descM = 'Láminas gruesas y espaciadas de ferrita α y cementita Fe₃C (S ≈ 0.45 µm).';
    S_val = '0.45 µm'; S_sub = 'Espaciado ancho'; hrc = '18 HRC'; hv = '~220 HV';
    fasesTTT = [['Perlita gruesa (α + Fe₃C)', '100 %'], ['Austenita retenida', '0 %']];
    storyM = `Enfriamiento muy lento cruzando las curvas "C" a alta temperatura (~680 °C, bajo subenfriamiento <b>ΔT = ${(A1 - T_trans).toFixed(0)} °C</b>). La alta difusividad del carbono permite formar <b>láminas gruesas</b>, dando máxima ductilidad y maquinabilidad.`;
  } else if (ruta === 'patentado') {
    T_trans = 535;
    pts = [[0.1, 800], [0.8, 540], [Math.max(30, tHold*0.3), 535], [Math.max(80, tHold*0.6), 200]];
    microMode = 'perlita_fina';
    titleM = 'Perlita Fina (Normalizado / Patentado)';
    descM = 'Láminas muy delgadas y compactas de perlita (S ≈ 0.09 µm).';
    S_val = '0.09 µm'; S_sub = 'Espaciado fino'; hrc = '34 HRC'; hv = '~340 HV';
    fasesTTT = [['Perlita fina (α + Fe₃C)', '100 %'], ['Martensita', '0 %']];
    storyM = `Transformación en la nariz perlítica (~535 °C, <b>ΔT = ${(A1 - T_trans).toFixed(0)} °C</b>). Mayor fuerza motriz y menor tiempo para difundir producen láminas ultrafinas ($S \\propto 1/\\Delta T$), elevando resistencia y resistencia al desgaste (cables, rieles).`;
  } else if (ruta === 'bainita_sup') {
    T_trans = 420;
    pts = [[0.1, 800], [0.4, 420], [Math.max(250, tHold), 420], [Math.max(400, tHold*1.3), 100]];
    microMode = 'bainita_sup';
    titleM = 'Bainita Superior (Austemperado a 420 °C)';
    descM = 'Plumas de ferrita bainítica con carburos precipitados entre listones.';
    S_val = 'Plumas α + Fe₃C'; S_sub = 'Bainita superior'; hrc = '42 HRC'; hv = '~410 HV';
    fasesTTT = [['Bainita superior', '100 %'], ['Martensita', '0 %']];
    storyM = `Enfriamiento rápido esquivando la nariz perlítica hasta <b>420 °C</b> (sobre Ms) y mantenimiento isotérmico hasta cruzar Pf. Se forma <b>bainita plumosa</b> con buena combinación de resistencia y tenacidad.`;
  } else if (ruta === 'bainita_inf') {
    T_trans = Math.max(Ms + 25, 300);
    pts = [[0.1, 800], [0.35, T_trans], [Math.max(600, tHold), T_trans], [Math.max(900, tHold*1.3), 80]];
    microMode = 'bainita_inf';
    titleM = 'Bainita Inferior (Austemperado a ~300 °C)';
    descM = 'Agujas aciculares finas con carburos intralistón de alta tenacidad.';
    S_val = 'Acicular fina'; S_sub = 'Bainita inferior'; hrc = '52 HRC'; hv = '~540 HV';
    fasesTTT = [['Bainita inferior', '100 %'], ['Martensita', '0 %']];
    storyM = `Mantenimiento isotérmico justo por encima de Ms (${T_trans.toFixed(0)} °C, gran subenfriamiento <b>ΔT = ${(A1 - T_trans).toFixed(0)} °C</b>). Carburos ultrafinos precipitan dentro de las agujas de ferrita, logrando dureza cercana a la martensita pero con tenacidad muy superior.`;
  } else if (ruta === 'temple') {
    T_trans = Mf;
    pts = [[0.1, 800], [0.25, 550], [0.5, Ms], [1.2, 60]];
    microMode = C >= 0.60 ? 'martensita_placas' : 'martensita_listones';
    titleM = `Martensita 100% (Temple v > v_crítica)`;
    descM = C >= 0.60 ? 'Placas lenticulares BCT + austenita retenida.' : 'Listones paralelos BCT de alta dureza.';
    S_val = 'Red BCT'; S_sub = 'Sin difusión'; hrc = `${Math.round(35 + C*32)} HRC`; hv = `~${Math.round(350 + C*450)} HV`;
    fasesTTT = [['Martensita (BCT)', '96 %'], ['Austenita retenida', '4 %']];
    storyM = `La curva de enfriamiento pasa a la <b>izquierda de la nariz perlítica</b> ($v > v_{\\text{crítica}}$), evitando toda difusión. Al cruzar <b>Ms (${Ms.toFixed(0)} °C)</b> ocurre transformación cizallante instantánea hacia martensita BCT extremadamente dura.`;
  } else if (ruta === 'martemperado') {
    T_trans = Ms + 20;
    pts = [[0.1, 800], [0.3, Ms + 20], [15, Ms + 20], [35, 60]];
    microMode = C >= 0.60 ? 'martensita_placas' : 'martensita_listones';
    titleM = 'Martensita por Martemperado (Temple Escalonado)';
    descM = 'Martensita homogénea sin gradientes térmicos ni grietas de temple.';
    S_val = 'Red BCT'; S_sub = 'Baja distorsión'; hrc = `${Math.round(34 + C*31)} HRC`; hv = `~${Math.round(340 + C*440)} HV`;
    fasesTTT = [['Martensita (BCT)', '95 %'], ['Austenita retenida', '5 %']];
    storyM = `Temple en baño de sales justo sobre <b>Ms (${(Ms+20).toFixed(0)} °C)</b> para igualar la temperatura entre superficie y núcleo antes de cruzar Ms–Mf. Se obtiene la misma martensita pero eliminando tensiones residuales y fisuras.`;
  } else {
    T_trans = 540;
    const midNose = (getStartSec(540) || 1.2) * 2.5;
    pts = [[0.1, 800], [0.6, 540], [midNose, 540], [midNose * 1.8, 70]];
    microMode = 'perlita_martensita';
    titleM = 'Microestructura Mixta: Perlita Fina + Martensita';
    descM = 'Colonias oscuras de perlita fina en borde de grano + núcleos de martensita.';
    S_val = 'Dúplex P + M'; S_sub = 'Temple incompleto'; hrc = '46 HRC'; hv = '~460 HV';
    fasesTTT = [['Perlita fina (borde γ)', '50 %'], ['Martensita (centro)', '50 %']];
    storyM = `La curva penetró parcialmente entre <b>Ps y Pf</b> (transformando 50% de γ en perlita fina en los bordes de grano) y luego enfrió rápido bajo Ms, transformando el 50% restante en martensita.`;
  }

  // Dibujar ruta verde brillante
  tttCtx.save();
  tttCtx.strokeStyle = '#22c55e'; tttCtx.lineWidth = 3.5;
  tttCtx.beginPath();
  pts.forEach((pt, idx) => {
    const px = toX(pt[0]), py = toY(pt[1]);
    if (idx === 0) tttCtx.moveTo(px, py); else tttCtx.lineTo(px, py);
  });
  tttCtx.stroke();
  pts.forEach(pt => {
    tttCtx.fillStyle = '#22c55e';
    tttCtx.beginPath(); tttCtx.arc(toX(pt[0]), toY(pt[1]), 4.5, 0, Math.PI*2); tttCtx.fill();
  });
  tttCtx.restore();

  // Renderizar microscopio TTT y paneles
  renderMicroToCanvas(tttMicroCtx, microMode, { martFrac: 0.96 });
  document.getElementById('tttMicroTitle').textContent = titleM;
  document.getElementById('tttMicroDesc').textContent = descM;
  document.getElementById('tttMetDT').textContent = `${Math.max(0, A1 - T_trans).toFixed(0)} °C`;
  document.getElementById('tttMetDTsub').textContent = `T_trans ≈ ${T_trans.toFixed(0)} °C`;
  document.getElementById('tttMetS').textContent = S_val;
  document.getElementById('tttMetSsub').textContent = S_sub;
  document.getElementById('tttMetHRC').textContent = hrc;
  document.getElementById('tttMetHV').textContent = hv;
  document.getElementById('tttStoryBox').innerHTML = storyM;

  let htmlF = `<div style="font-size:0.78rem; color:#38bdf8; font-weight:700; margin-bottom:4px;">Constituyentes Obtenidos:</div>`;
  fasesTTT.forEach(f => {
    htmlF += `<div class="phase-item"><span><b>${f[0]}</b></span><span><b>${f[1]}</b></span></div>`;
  });
  document.getElementById('tttFasesLista').innerHTML = htmlF;
}

['tttSlC', 'tttSlAl', 'tttSlTime'].forEach(id => {
  document.getElementById(id).addEventListener('input', updateTTT);
});
document.getElementById('tttRuta').addEventListener('change', updateTTT);

// =========================================================================
// PESTAÑA 3: CURVAS DE ENFRIAMIENTO, CALENTAMIENTO Y SUBENFRIAMIENTO
// =========================================================================
const coolCanvas = document.getElementById('coolCanvas');
const coolCtx = coolCanvas.getContext('2d');

function updateCooling() {
  const mat = document.getElementById('coolMat').value;
  const rate = parseInt(document.getElementById('coolSlRate').value);
  const showHeat = document.getElementById('chkHeat').checked;
  const showEq = document.getElementById('chkEq').checked;

  const rateNames = [
    '1 · Muy Lenta (Horno / Equilibrio cercano)',
    '2 · Lenta (Recocido industrial)',
    '3 · Moderada (Normalizado al aire)',
    '4 · Rápida (Aire forzado / Aceite)',
    '5 · Muy Rápida (Temple severo · Alto ΔT)'
  ];
  document.getElementById('coolValRate').textContent = rateNames[rate - 1];

  const cw = coolCanvas.width, ch = coolCanvas.height;
  coolCtx.clearRect(0, 0, cw, ch);

  const padL = 60, padR = 30, padT = 28, padB = 42;
  const plotW = cw - padL - padR;
  const plotH = ch - padT - padB;
  const yMin = 500, yMax = 1620;

  const toX = frac => padL + frac * plotW;
  const toY = temp => padT + plotH - ((temp - yMin) / (yMax - yMin)) * plotH;

  // Grilla
  coolCtx.strokeStyle = '#1e293b'; coolCtx.lineWidth = 1;
  coolCtx.fillStyle = '#94a3b8'; coolCtx.font = '11px sans-serif';
  for (let t = 600; t <= 1600; t += 200) {
    const y = toY(t);
    coolCtx.beginPath(); coolCtx.moveTo(padL, y); coolCtx.lineTo(cw - padR, y); coolCtx.stroke();
    coolCtx.fillText(t + '°', 12, y + 4);
  }
  coolCtx.fillStyle = '#cbd5e1'; coolCtx.font = 'bold 12px sans-serif';
  coolCtx.fillText('Tiempo (t) →', cw/2 - 35, ch - 8);

  // Parámetros por material
  let Teq = 727, dT_cool = rate * 14, dT_heat = rate * 10;
  let eqPts = [], coolPts = [], heatPts = [];
  let puntosList = [], resDesc = '', fisDesc = '';

  if (mat === 'puro') {
    Teq = 912;
    dT_cool = rate * 12;
    dT_heat = rate * 9;
    const Ar4 = 1394 - dT_cool*0.7, Ar3 = 912 - dT_cool, Ar2 = 770;
    const Ac2 = 770, Ac3 = 912 + dT_heat, Ac4 = 1394 + dT_heat*0.7;

    eqPts = [
      [0.02, 1600], [0.12, 1538], [0.22, 1538],
      [0.32, 1394], [0.42, 1394],
      [0.58, 912],  [0.70, 912],
      [0.78, 770],  [0.84, 770], [0.98, 560]
    ];
    // Curva real de enfriamiento con subenfriamiento y recalescencia
    coolPts = [
      [0.02, 1600], [0.13, 1538 - dT_cool*0.6], [0.15, 1538 - dT_cool*0.25], [0.23, 1538 - dT_cool*0.3],
      [0.33, Ar4 - 6], [0.35, Ar4], [0.43, Ar4],
      [0.59, Ar3 - 9], [0.61, Ar3], [0.71, Ar3],
      [0.79, Ar2], [0.85, Ar2], [0.98, 560]
    ];
    heatPts = [
      [0.02, 560], [0.15, Ac2], [0.21, Ac2],
      [0.31, Ac3], [0.43, Ac3],
      [0.57, Ac4], [0.67, Ac4],
      [0.77, 1538 + dT_heat*0.4], [0.87, 1538 + dT_heat*0.4], [0.98, 1600]
    ];

    puntosList = [
      ['Fusión / Solidificación', '1538 °C', `Ar: ${(1538 - dT_cool*0.3).toFixed(0)}°C | Ac: ${(1538 + dT_heat*0.4).toFixed(0)}°C`],
      ['Alotropía δ ↔ γ (A4)', '1394 °C', `Ar4: ${Ar4.toFixed(0)}°C | Ac4: ${Ac4.toFixed(0)}°C`],
      ['Alotropía γ ↔ α (A3)', '912 °C', `Ar3: ${Ar3.toFixed(0)}°C | Ac3: ${Ac3.toFixed(0)}°C`],
      ['Punto de Curie (A2)', '770 °C', 'Sin histéresis (cambio magnético)']
    ];
    resDesc = `<b>Hierro Puro (0.00% C):</b> Presenta mesetas isotérmicas puras en cada cambio alotrópico (Líquido → Ferrita δ BCC → Austenita γ FCC → Ferrita α BCC).<br>• Con un subenfriamiento <b>ΔT = ${dT_cool.toFixed(0)} °C</b> bajo A3, se obtiene <b>Ferrita α poligonal pura</b>; a mayor velocidad de enfriamiento, aumenta la tasa de nucleación y se refina el tamaño de grano ferrítico.`;
    fisDesc = `• <b>¿Por qué A2 (770 °C) no tiene subenfriamiento?</b> Porque la transición ferromagnética ↔ paramagnética es de segundo orden (reordenamiento de espines electrónicos sin cambio de red cristalina ni nucleación).<br>• En cambio, <b>A4, A3 y la solidificación</b> sí exigen reordenar átomos (FCC ↔ BCC), generando histéresis <b>Ar < A < Ac</b>.`;
  } else if (mat === 'hipo') {
    Teq = 727;
    const A3_eq = 815;
    dT_cool = rate * 14;
    dT_heat = rate * 11;
    const Ar3 = A3_eq - dT_cool*1.1, Ar1 = 727 - dT_cool;
    const Ac1 = 727 + dT_heat, Ac3 = A3_eq + dT_heat*1.1;

    eqPts = [
      [0.02, 1000], [0.22, A3_eq], [0.46, 727], [0.66, 727], [0.96, 540]
    ];
    coolPts = [
      [0.02, 1000], [0.24, Ar3], [0.48, Ar1 - 10], [0.51, Ar1], [0.69, Ar1], [0.96, 540]
    ];
    heatPts = [
      [0.02, 540], [0.28, Ac1], [0.46, Ac1], [0.72, Ac3], [0.96, 1000]
    ];

    puntosList = [
      ['Inicio ferrita proeutectoide (A3)', `${A3_eq} °C`, `Ar3: ${Ar3.toFixed(0)}°C | Ac3: ${Ac3.toFixed(0)}°C`],
      ['Reacción eutectoide (A1)', '727 °C', `Ar1: ${Ar1.toFixed(0)}°C | Ac1: ${Ac1.toFixed(0)}°C`],
      ['Subenfriamiento eutectoide (ΔT)', '0 °C (eq)', `ΔT = -${dT_cool.toFixed(0)} °C`]
    ];
    resDesc = `<b>Acero Hipoeutectoide (0.45% C):</b><br>1) Entre <b>Ar3 (${Ar3.toFixed(0)} °C)</b> y <b>Ar1 (${Ar1.toFixed(0)} °C)</b> aparece un cambio de pendiente (sin meseta horizontal) donde nuclea <b>ferrita α proeutectoide</b> en borde de grano.<br>2) Al llegar a <b>Ar1</b>, ocurre una meseta isotérmica con recalescencia donde la austenita restante (0.76% C) transforma en <b>perlita</b> (${rate >= 3 ? 'con placas de Widmanstätten por alto ΔT' : 'ferrita alotriomorfa poligonal + perlita'}).`;
    fisDesc = `• Al aumentar la velocidad de enfriamiento (mayor <b>ΔT = ${dT_cool.toFixed(0)} °C</b>), se suprime parcialmente la difusión de largo alcance: disminuye la fracción aparente de ferrita proeutectoide, aparecen agujas de <b>Widmanstätten</b> y la perlita resultante tiene láminas más finas y duras.`;
  } else if (mat === 'eut') {
    Teq = 727;
    dT_cool = rate * 15;
    dT_heat = rate * 11;
    const Ar1 = 727 - dT_cool;
    const Ac1 = 727 + dT_heat;

    eqPts = [
      [0.02, 950], [0.30, 727], [0.65, 727], [0.96, 540]
    ];
    coolPts = [
      [0.02, 950], [0.32, Ar1 - 12], [0.35, Ar1], [0.68, Ar1], [0.96, 540]
    ];
    heatPts = [
      [0.02, 540], [0.32, Ac1], [0.65, Ac1], [0.96, 950]
    ];

    puntosList = [
      ['Reacción Eutectoide (A1)', '727 °C', 'γ (0.76%C) ↔ α + Fe₃C'],
      ['Temperatura real enfriamiento (Ar1)', '727 °C (eq)', `Ar1 = ${Ar1.toFixed(0)} °C (ΔT = -${dT_cool} °C)`],
      ['Temperatura real calentamiento (Ac1)', '727 °C (eq)', `Ac1 = ${Ac1.toFixed(0)} °C (ΔT = +${dT_heat} °C)`]
    ];
    const S_est = (18 / Math.max(10, dT_cool)).toFixed(2);
    resDesc = `<b>Acero Eutectoide (0.76% C):</b><br>Toda la transformación ocurre en una única meseta isotérmica a <b>Ar1 = ${Ar1.toFixed(0)} °C</b> (subenfriamiento <b>ΔT = ${dT_cool} °C</b>).<br>• Se obtiene <b>100% Perlita Laminar</b> con espaciado interlaminar estimado <b>S ≈ ${S_est} µm</b> (${dT_cool > 45 ? 'Perlita Fina de alta resistencia' : 'Perlita Gruesa dúctil'}).`;
    fisDesc = `• <b>Ley de Zener-Hillert (S ∝ 1/ΔT):</b> A mayor subenfriamiento ΔT, mayor energía libre disponible para crear interfaces α/Fe₃C y menor movilidad atómica del carbono.<br>• Por eso el espaciado interlaminar <b>S</b> disminuye inversamente con ΔT, elevando el límite de fluencia según $\\sigma_y = \\sigma_0 + k \\cdot S^{-1/2}$.`;
  } else {
    Teq = 1148;
    dT_cool = rate * 12;
    dT_heat = rate * 9;
    const Ar_eut = 1148 - dT_cool;
    const Ac_eut = 1148 + dT_heat;

    eqPts = [
      [0.02, 1380], [0.30, 1148], [0.65, 1148], [0.96, 920]
    ];
    coolPts = [
      [0.02, 1380], [0.32, Ar_eut - 11], [0.35, Ar_eut], [0.68, Ar_eut], [0.96, 920]
    ];
    heatPts = [
      [0.02, 920], [0.32, Ac_eut], [0.65, Ac_eut], [0.96, 1380]
    ];

    puntosList = [
      ['Reacción Eutéctica (Teut)', '1148 °C (Fe₃C)', '1154 °C (Estable Fe–Grafito)'],
      ['Solidificación real (Ar_eut)', '1148 °C (eq)', `Ar = ${Ar_eut.toFixed(0)} °C (ΔT = -${dT_cool} °C)`],
      ['Fusión real (Ac_eut)', '1148 °C (eq)', `Ac = ${Ac_eut.toFixed(0)} °C (ΔT = +${dT_heat} °C)`]
    ];
    resDesc = `<b>Fundición Eutéctica (4.30% C):</b><br>• Si el subenfriamiento es <b>bajo (ΔT < 18 °C, enfriamiento lento + Si)</b>, solidifica sobre la temperatura eutéctica estable (1154 °C) formando <b>Fundición Gris (γ + Grafito laminar)</b>.<br>• Si el subenfriamiento es <b>alto (ΔT = ${dT_cool} °C > 20 °C, enfriamiento rápido)</b>, cae bajo 1148 °C y nuclea <b>Ledeburita (Fundición Blanca dura y frágil)</b>.`;
    fisDesc = `• <b>Competencia entre dos eutécticos:</b> El diagrama estable Fe–Grafito (1154 °C) está apenas 6 °C sobre el metaestable Fe–Fe₃C (1148 °C).<br>• Basta un pequeño subenfriamiento extra (por molde metálico frío o bajo Silicio) para cruzar el umbral de 1148 °C y "blanquear" la pieza.`;
  }

  // Dibujar curvas en Canvas
  function drawPoly(pts, color, width=3, dash=[]) {
    coolCtx.save();
    coolCtx.strokeStyle = color; coolCtx.lineWidth = width; coolCtx.setLineDash(dash);
    coolCtx.beginPath();
    pts.forEach((pt, idx) => {
      const px = toX(pt[0]), py = toY(pt[1]);
      if (idx === 0) coolCtx.moveTo(px, py); else coolCtx.lineTo(px, py);
    });
    coolCtx.stroke();
    coolCtx.restore();
  }

  if (showEq) drawPoly(eqPts, '#94a3b8', 2.2, [6, 5]);
  drawPoly(coolPts, '#2dd4bf', 3.4);
  if (showHeat) drawPoly(heatPts, '#fb923c', 3.0);

  // Flecha visual de Subenfriamiento ΔT en el gráfico
  const refEqY = toY(Teq);
  const refArY = toY(Teq - dT_cool);
  const arrowX = toX(0.45);
  coolCtx.save();
  coolCtx.strokeStyle = '#ef4444'; coolCtx.lineWidth = 2;
  coolCtx.beginPath(); coolCtx.moveTo(arrowX, refEqY); coolCtx.lineTo(arrowX, refArY); coolCtx.stroke();
  coolCtx.fillStyle = '#ef4444'; coolCtx.font = 'bold 11px sans-serif';
  coolCtx.fillText(`ΔT = ${dT_cool.toFixed(0)}°C`, arrowX + 6, (refEqY + refArY)/2 + 4);
  coolCtx.restore();

  // Actualizar métricas y paneles
  document.getElementById('coolMetA').textContent = Teq + ' °C';
  document.getElementById('coolMetAr').textContent = (Teq - dT_cool).toFixed(0) + ' °C';
  document.getElementById('coolMetDT').textContent = `ΔT = -${dT_cool.toFixed(0)} °C`;
  document.getElementById('coolMetAc').textContent = (Teq + dT_heat).toFixed(0) + ' °C';
  document.getElementById('coolMetDTc').textContent = `ΔT = +${dT_heat.toFixed(0)} °C`;

  let htmlP = '';
  puntosList.forEach(pt => {
    htmlP += `<div class="phase-item"><span><b>${pt[0]}</b></span><span><b>${pt[1]}</b> · <span style="color:#94a3b8">${pt[2]}</span></span></div>`;
  });
  document.getElementById('coolPuntosLista').innerHTML = htmlP;
  document.getElementById('coolResultadoBox').innerHTML = resDesc;
  document.getElementById('coolFisicaBox').innerHTML = fisDesc;
}

['coolMat', 'chkHeat', 'chkEq'].forEach(id => {
  document.getElementById(id).addEventListener('change', updateCooling);
});
document.getElementById('coolSlRate').addEventListener('input', updateCooling);

// Inicializar todas las vistas
updateAll();
updateTTT();
updateCooling();
</script>
</body>
</html>
"""

components.html(html_simulador, height=910, scrolling=False)