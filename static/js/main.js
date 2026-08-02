/**
 * Algebrify Solver Portal — Main JavaScript
 * Handles: Dark mode, Matrix grid builder, Vector inputs,
 *          System grid, 2D Transformation Canvas, Smooth UX
 */

// ══════════════════════════════════════════
// THEME (Dark / Light Mode)
// ══════════════════════════════════════════

(function () {
  const saved = localStorage.getItem('algebrify_theme') || 'dark';
  document.documentElement.setAttribute('data-bs-theme', saved);
  document.documentElement.setAttribute('data-theme', saved);
})();

document.addEventListener('DOMContentLoaded', function () {
  updateThemeUI();

  const btn = document.getElementById('themeToggle');
  const mobileBtn = document.getElementById('themeToggleMobile');

  function toggleTheme() {
    const curr = document.documentElement.getAttribute('data-bs-theme') || 'dark';
    const next = curr === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-bs-theme', next);
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('algebrify_theme', next);
    updateThemeUI();

    // Redraw 2D canvas if visualizer is open
    if (typeof draw2DTransformation === 'function' && document.getElementById('transformCanvas')) {
      const M = typeof readMatrixGrid === 'function' ? readMatrixGrid(2, 2, 'tf') : [[1,0],[0,1]];
      draw2DTransformation('transformCanvas', M);
    }
  }

  if (btn) btn.addEventListener('click', toggleTheme);
  if (mobileBtn) mobileBtn.addEventListener('click', toggleTheme);
});

function updateThemeUI() {
  const theme = document.documentElement.getAttribute('data-bs-theme') || 'dark';
  const isDark = theme === 'dark';

  const icon = document.getElementById('themeIcon');
  const text = document.getElementById('themeText');
  const mobileIcon = document.getElementById('themeIconMobile');

  if (icon) icon.className = isDark ? 'bi bi-sun-fill text-warning' : 'bi bi-moon-stars-fill text-primary';
  if (text) text.textContent = isDark ? 'Light Mode' : 'Dark Mode';
  if (mobileIcon) mobileIcon.className = isDark ? 'bi bi-sun-fill text-warning' : 'bi bi-moon-stars-fill text-primary';
}



// ══════════════════════════════════════════
// MATRIX GRID BUILDER
// ══════════════════════════════════════════

/**
 * Render a rows×cols matrix input table inside `containerId`.
 * prefix is used for element IDs to avoid collisions.
 * defaultFn(i,j) returns the default value for cell (i,j).
 */
function buildMatrixGrid(containerId, rows, cols, prefix, defaultFn) {
  const el = document.getElementById(containerId);
  if (!el) return;

  defaultFn = defaultFn || function (i, j) { return i === j ? 1 : 0; };

  let html = '<div class="matrix-grid">';
  for (let i = 0; i < rows; i++) {
    html += '<div class="matrix-row">';
    for (let j = 0; j < cols; j++) {
      html += `<input type="number" step="any" class="matrix-cell"
                      id="${prefix}_${i}_${j}" value="${defaultFn(i, j)}"
                      data-row="${i}" data-col="${j}" aria-label="Row ${i+1} Col ${j+1}">`;
    }
    html += '</div>';
  }
  html += '</div>';
  el.innerHTML = html;
}

/** Read all cell values from a grid into a 2-D array. */
function readMatrixGrid(rows, cols, prefix) {
  const M = [];
  for (let i = 0; i < rows; i++) {
    const row = [];
    for (let j = 0; j < cols; j++) {
      const el = document.getElementById(`${prefix}_${i}_${j}`);
      row.push(el ? parseFloat(el.value) || 0 : 0);
    }
    M.push(row);
  }
  return M;
}

/** Read a flat vector from individual inputs with id pattern `prefix_i`. */
function readVector(dim, prefix) {
  const v = [];
  for (let i = 0; i < dim; i++) {
    const el = document.getElementById(`${prefix}_${i}`);
    v.push(el ? parseFloat(el.value) || 0 : 0);
  }
  return v;
}

/** Render vector component inputs inside `containerId`. */
function buildVectorInputs(containerId, dim, prefix, defaults) {
  const el = document.getElementById(containerId);
  if (!el) return;
  defaults = defaults || [];
  const labels = ['x', 'y', 'z', 'w'];
  let html = '<div class="d-flex gap-2 flex-wrap justify-content-center">';
  for (let i = 0; i < dim; i++) {
    const lbl = labels[i] || `v${i+1}`;
    const val = defaults[i] !== undefined ? defaults[i] : (i + 1);
    html += `
      <div class="text-center">
        <div class="form-label" style="font-size:.75rem;">${lbl}</div>
        <input type="number" step="any" class="matrix-cell" style="width:56px"
               id="${prefix}_${i}" value="${val}" aria-label="${lbl} component">
      </div>`;
  }
  html += '</div>';
  el.innerHTML = html;
}


// ══════════════════════════════════════════
// 2D TRANSFORMATION CANVAS
// ══════════════════════════════════════════

/**
 * Draw original unit square + transformed square on a canvas.
 * transformMatrix is [[a,b],[c,d]].
 */
function draw2DTransformation(canvasId, transformMatrix) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  const W = canvas.width;
  const H = canvas.height;
  const ox = W / 2;   // origin X
  const oy = H / 2;   // origin Y
  const scale = 55;   // pixels per unit

  // --- background ---
  ctx.clearRect(0, 0, W, H);

  // grid
  const isDark = document.documentElement.getAttribute('data-bs-theme') === 'dark';
  const gridColor = isDark ? 'rgba(255,255,255,.07)' : 'rgba(0,0,0,.06)';
  const axisColor = isDark ? 'rgba(255,255,255,.35)' : 'rgba(0,0,0,.35)';

  ctx.strokeStyle = gridColor;
  ctx.lineWidth = 1;
  for (let x = ox % scale; x < W; x += scale) {
    ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke();
  }
  for (let y = oy % scale; y < H; y += scale) {
    ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke();
  }

  // axes
  ctx.strokeStyle = axisColor;
  ctx.lineWidth = 1.5;
  ctx.beginPath(); ctx.moveTo(0, oy); ctx.lineTo(W, oy); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(ox, 0); ctx.lineTo(ox, H); ctx.stroke();

  // --- helpers ---
  function toCanvas(px, py) {
    return [ox + px * scale, oy - py * scale];
  }

  function drawPolygon(points, stroke, fill) {
    ctx.beginPath();
    const [fx, fy] = toCanvas(points[0][0], points[0][1]);
    ctx.moveTo(fx, fy);
    for (let i = 1; i < points.length; i++) {
      const [cx, cy] = toCanvas(points[i][0], points[i][1]);
      ctx.lineTo(cx, cy);
    }
    ctx.closePath();
    ctx.fillStyle = fill;
    ctx.fill();
    ctx.strokeStyle = stroke;
    ctx.lineWidth = 2;
    ctx.stroke();
  }

  function applyTransform(pt) {
    const m = transformMatrix;
    return [
      m[0][0] * pt[0] + m[0][1] * pt[1],
      m[1][0] * pt[0] + m[1][1] * pt[1]
    ];
  }

  function drawVector(vx, vy, color, label) {
    const [cx, cy] = toCanvas(vx, vy);
    ctx.strokeStyle = color;
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.moveTo(ox, oy);
    ctx.lineTo(cx, cy);
    ctx.stroke();

    // arrowhead
    const angle = Math.atan2(-(cy - oy), cx - ox);
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.lineTo(cx - 10 * Math.cos(angle - 0.35), cy + 10 * Math.sin(angle - 0.35));
    ctx.lineTo(cx - 10 * Math.cos(angle + 0.35), cy + 10 * Math.sin(angle + 0.35));
    ctx.fill();

    // label
    ctx.fillStyle = color;
    ctx.font = 'bold 13px Inter, sans-serif';
    ctx.fillText(label, cx + 5, cy - 5);
  }

  // unit square corners
  const sq = [[0,0],[1,0],[1,1],[0,1]];
  const sqT = sq.map(applyTransform);

  // original (semi-transparent blue)
  drawPolygon(sq, 'rgba(99,102,241,.6)', 'rgba(99,102,241,.12)');

  // transformed (semi-transparent purple)
  drawPolygon(sqT, 'rgba(139,92,246,.85)', 'rgba(139,92,246,.25)');

  // draw transformed basis vectors
  drawVector(sqT[1][0], sqT[1][1], '#ef4444', "i'");
  drawVector(sqT[3][0], sqT[3][1], '#10b981', "j'");

  // original origin dot
  ctx.fillStyle = isDark ? '#fff' : '#000';
  ctx.beginPath();
  ctx.arc(ox, oy, 4, 0, Math.PI * 2);
  ctx.fill();
}
