const state = {
  auth: JSON.parse(localStorage.getItem("fractal_auth") || "null"),
};

const els = {};
function $(id) { return document.getElementById(id); }

let userTags = [];
let selectedTags = ["basic"];

function parseNumber(value) {
  if (value === "" || value == null) return undefined;
  const num = Number(value);
  return isNaN(num) ? undefined : num;
}

function getInputValue(name) {
  const el = document.querySelector(`[name="${name}"]`);
  return el ? el.value : null;
}

function showAuthMsg(text, type = "info") {
  if (!els.authMsg) return;
  els.authMsg.textContent = text;
  els.authMsg.className = `msg ${type}`;
  els.authMsg.style.display = "block";
  setTimeout(() => { if (els.authMsg.textContent === text) els.authMsg.textContent = ""; }, 5000);
}

function showNotification(title, message, type = "info") {
  const container = $("notifications-container");
  if (!container) return;

  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  toast.style.cssText = `
    background: ${type === "success" ? "#22c55e" : type === "error" ? "#ef4444" : "#3b82f6"};
    color: white;
    padding: 16px;
    border-radius: 8px;
    margin-bottom: 12px;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    animation: slideIn 0.3s ease;
  `;

  const content = document.createElement("div");
  content.style.flex = "1";

  const titleEl = document.createElement("div");
  titleEl.style.cssText = "font-weight: 600; margin-bottom: 4px;";
  titleEl.textContent = title;

  const msgEl = document.createElement("div");
  msgEl.style.cssText = "font-size: 13px; opacity: 0.95;";
  msgEl.textContent = message;

  content.appendChild(titleEl);
  content.appendChild(msgEl);

  const closeBtn = document.createElement("button");
  closeBtn.className = "toast-close";
  closeBtn.textContent = "✕";
  closeBtn.style.cssText = "background: none; border: none; color: white; font-size: 18px; cursor: pointer; opacity: 0.8; padding: 0;";
  closeBtn.onclick = () => toast.remove();

  toast.appendChild(content);
  toast.appendChild(closeBtn);
  container.appendChild(toast);

  setTimeout(() => toast.remove(), 5000);
}

function updateAuthUI() {
  if (!els.currentUser) return;
  if (state.auth?.user?.username) {
    els.currentUser.textContent = state.auth.user.username;
    els.currentUser.style.color = "#86efac";
    if (els.userDisplay) els.userDisplay.classList.remove("hidden");
    if (els.username) els.username.textContent = state.auth.user.username;
    if (els.logoutBtn) els.logoutBtn.classList.remove("hidden");
    if (els.showAuthBtn) els.showAuthBtn.classList.add("hidden");
  } else {
    els.currentUser.textContent = "Не авторизован";
    els.currentUser.style.color = "#9ca3af";
    if (els.userDisplay) els.userDisplay.classList.add("hidden");
    if (els.logoutBtn) els.logoutBtn.classList.add("hidden");
    if (els.showAuthBtn) els.showAuthBtn.classList.remove("hidden");
  }
}

function validatePassword(pw, confirm) {
  if (!pw || pw.length < 4) return "Пароль должен быть минимум 4 символа";
  if (!/[A-Za-z]/.test(pw)) return "Пароль должен содержать хотя бы одну латинскую букву";
  if (!/\d/.test(pw)) return "Пароль должен содержать хотя бы одну цифру";
  if (!/[^A-Za-z\d]/.test(pw)) return "Пароль должен содержать хотя бы один спецсимвол (!@#$%^&*)";
  if (confirm && pw !== confirm) return "Пароли не совпадают";
  return null;
}

async function api(path, options = {}) {
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  if (state.auth?.token) headers.Authorization = `Bearer ${state.auth.token}`;
  const res = await fetch(path, { headers, ...options });
  const text = await res.text();
  if (!res.ok) {
    try {
      const json = JSON.parse(text);
      throw new Error(json.detail || json.message || `HTTP ${res.status}`);
    } catch {
      throw new Error(text || `HTTP ${res.status}`);
    }
  }
  const ct = res.headers.get("content-type") || "";
  return ct.includes("application/json") ? JSON.parse(text) : text;
}

function initEls() {
  els.authForm = $("auth-form");
  els.authMsg = $("auth-msg");
  els.currentUser = $("current-user");
  els.loginBtn = $("login-btn");
  els.registerBtn = $("register-btn");
  els.logoutBtn = $("logout-btn");
  els.showAuthBtn = $("show-auth-btn");
  els.userDisplay = $("user-display");
  els.username = $("username");

  els.generateForm = $("generate-form");
  els.taskBox = $("task-box");
  els.resultImg = $("result-img");
  els.resultPlaceholder = $("result-placeholder");
  els.miniGallery = $("mini-gallery");
  els.fractalType = $("fractal_type");

  els.fractalFields = {
    mandelbrot: $("mandelbrot-fields"),
    julia: $("julia-fields"),
    burning_ship: $("burning-ship-fields"),
    ifs: $("ifs-fields"),
  };

  els.customParams = $("custom-params");
  els.transformsContainer = $("transforms-container");
  els.addTransformBtn = $("add-transform");
  els.loadPresetBtn = $("load-preset");
  els.presetSelect = $("ifs-preset");

  els.tagInput = $("tag-input");
  els.tagSuggestions = $("tag-suggestions");
  els.selectedTagsDiv = $("selected-tags");

  els.statsDetails = $("stats-details");
}

function showFractalParams(type) {
  for (const [key, el] of Object.entries(els.fractalFields)) {
    if (!el) continue;
    if (key === type) {
      el.removeAttribute("hidden");
    } else {
      el.setAttribute("hidden", "");
    }
  }

  if (type === "ifs") {
    const isCustom = !els.presetSelect?.value || els.presetSelect.value === "custom";
    if (els.customParams) {
      if (isCustom) els.customParams.removeAttribute("hidden");
      else els.customParams.setAttribute("hidden", "");
    }
  }
}

function clearIrrelevantFields(currentType) {
  if (currentType !== "mandelbrot" && currentType !== "julia" && currentType !== "burning_ship") {
    ['center_x', 'center_y', 'scale'].forEach(n => {
      const el = document.querySelector(`[name="${n}"]`);
      if (el) el.value = '';
    });
  }
  if (currentType !== "julia") {
    ['c_re', 'c_im'].forEach(n => {
      const el = document.querySelector(`[name="${n}"]`);
      if (el) el.value = '';
    });
  }
  if (currentType !== "ifs") {
    ['preset_name', 'variation_name', 'seed', 'samples'].forEach(n => {
      const el = document.querySelector(`[name="${n}"]`);
      if (el) el.value = '';
    });
    if (els.transformsContainer) els.transformsContainer.innerHTML = '';
  }
}

function buildPayload() {
  if (!els.generateForm) return {};

  const type = els.fractalType?.value;

  const base = {
    fractal_type: type,
    width: parseNumber(getInputValue("width")) || 1024,
    height: parseNumber(getInputValue("height")) || 768,
    max_iter: parseNumber(getInputValue("max_iter")) || 300,
    gamma: parseNumber(getInputValue("gamma")) || 2.2,
    name: getInputValue("name")?.trim() || undefined,
    tags: selectedTags.length > 0 ? selectedTags : ["basic"],
  };

  if (type === "ifs") {
    const presetVal = els.presetSelect?.value?.trim();
    const variationVal = getInputValue("variation_name")?.trim();
    if (!presetVal || presetVal === "custom") {
      return {
        ...base,
        preset_name: "custom",
        variation_name: variationVal || undefined,
        custom_transforms: buildCustomTransforms(),
        seed: parseNumber(getInputValue("seed")) || 42,
        samples: parseNumber(getInputValue("samples")) || 300000,
      };
    }
    return {
      ...base,
      preset_name: presetVal,
      variation_name: variationVal || undefined,
      seed: parseNumber(getInputValue("seed")) || 42,
      samples: parseNumber(getInputValue("samples")) || 300000,
    };
  }

  const payload = { ...base };

  if (type === "mandelbrot" || type === "julia" || type === "burning_ship") {
    payload.center_x = parseNumber(getInputValue("center_x"));
    payload.center_y = parseNumber(getInputValue("center_y"));
    payload.scale = parseNumber(getInputValue("scale"));
  }

  if (type === "julia") {
    payload.c_re = parseNumber(getInputValue("c_re"));
    payload.c_im = parseNumber(getInputValue("c_im"));
  }

  return payload;
}

function buildCustomTransforms() {
  const transforms = [];
  const items = els.transformsContainer?.querySelectorAll('.transform-item') || [];
  items.forEach((item) => {
    const t = {
      a: parseNumber(item.querySelector('[name="t_a"]')?.value) || 0,
      b: parseNumber(item.querySelector('[name="t_b"]')?.value) || 0,
      c: parseNumber(item.querySelector('[name="t_c"]')?.value) || 0,
      d: parseNumber(item.querySelector('[name="t_d"]')?.value) || 0,
      e: parseNumber(item.querySelector('[name="t_e"]')?.value) || 0,
      f: parseNumber(item.querySelector('[name="t_f"]')?.value) || 0,
      weight: parseNumber(item.querySelector('[name="t_weight"]')?.value) || 1,
    };
    const color = item.querySelector('[name="t_color"]')?.value;
    if (color) {
      const match = color.match(/^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i);
      if (match) t.color = [parseInt(match[1], 16), parseInt(match[2], 16), parseInt(match[3], 16)];
    }
    transforms.push(t);
  });
  return transforms.length > 0 ? transforms : null;
}

function createTransformTemplate(index = 0, data = {}) {
  const d = { a: 0.5, b: 0, c: 0, d: 0.5, e: 0, f: 0, weight: 1, color: '#64ffda', ...data };
  return `<div class="transform-item" data-idx="${index}">
    <div class="transform-header"><strong>Трансформация #${index + 1}</strong><button type="button" class="remove-transform">✕</button></div>
    <div class="grid-3">
      <label>a <input type="number" step="0.01" name="t_a" value="${d.a}"></label>
      <label>b <input type="number" step="0.01" name="t_b" value="${d.b}"></label>
      <label>c <input type="number" step="0.01" name="t_c" value="${d.c}"></label>
    </div>
    <div class="grid-3">
      <label>d <input type="number" step="0.01" name="t_d" value="${d.d}"></label>
      <label>e <input type="number" step="0.01" name="t_e" value="${d.e}"></label>
      <label>f <input type="number" step="0.01" name="t_f" value="${d.f}"></label>
    </div>
    <div class="grid-2">
      <label>weight <input type="number" step="0.01" min="0.01" name="t_weight" value="${d.weight}"></label>
      <label>color <input type="color" name="t_color" value="${d.color}"></label>
    </div>
  </div>`;
}

function loadPresetIntoCustom(presetName) {
  const PRESETS = {
    fern: [{a:0,b:0,c:0,d:0.16,e:0,f:0,weight:0.01},{a:0.85,b:0.04,c:-0.04,d:0.85,e:0,f:1.6,weight:0.85},{a:0.2,b:-0.26,c:0.23,d:0.22,e:0,f:1.6,weight:0.07},{a:-0.15,b:0.28,c:0.26,d:0.24,e:0,f:0.44,weight:0.07}],
    spiral: [{a:0.7,b:-0.3,c:0.3,d:0.7,e:0.8,f:0.8,weight:0.5},{a:0.7,b:0.3,c:-0.3,d:0.7,e:-0.8,f:-0.8,weight:0.5}],
    heart_flame: [{a:0.5,b:0,c:0,d:0.5,e:0,f:0.3,weight:0.4},{a:0.5,b:0,c:0,d:0.5,e:-0.6,f:-0.4,weight:0.3},{a:0.5,b:0,c:0,d:0.5,e:0.6,f:-0.4,weight:0.3}],
    fisheye_grid: [{a:0.4,b:0,c:0,d:0.4,e:1,f:1,weight:0.25},{a:0.4,b:0,c:0,d:0.4,e:-1,f:1,weight:0.25},{a:0.4,b:0,c:0,d:0.4,e:-1,f:-1,weight:0.25},{a:0.4,b:0,c:0,d:0.4,e:1,f:-1,weight:0.25}],
  };
  const transforms = PRESETS[presetName];
  if (!transforms) return false;
  if (els.transformsContainer) {
    els.transformsContainer.innerHTML = '';
    transforms.forEach((t, i) => els.transformsContainer.insertAdjacentHTML('beforeend', createTransformTemplate(i, t)));
  }
  return true;
}

function showTask(text, status = "pending") {
  if (!els.taskBox) return;
  els.taskBox.classList.remove("hidden", "pending", "error", "success");
  els.taskBox.classList.add(status);
  els.taskBox.textContent = text;
  els.taskBox.style.display = "block";
}

let generationStartTime = null;

async function pollTask(taskId) {
  generationStartTime = Date.now();
  showTask(`Генерация... (0с)`, "pending");

  for (let i = 0; i < 300; i++) {
    try {
      const data = await api(`/api/tasks/${taskId}`);
      const elapsedSec = ((Date.now() - generationStartTime) / 1000).toFixed(1);

      if (data.status === "completed") {
        showTask(`Готово! (${elapsedSec}с)`, "success");
        if (els.resultImg && data.fractal_id) {
          els.resultImg.src = `/api/fractals/${data.fractal_id}/image?t=${Date.now()}`;
          els.resultImg.classList.remove("hidden");
        }
        if (els.resultPlaceholder) els.resultPlaceholder.classList.add("hidden");

        await loadUserStats();
        showNotification("Фрактал готов!", `Генерация заняла ${elapsedSec}с`, "success");

        await loadCollectionPreview();
        return;
      }
      if (data.status === "failed") {
        showTask(`Ошибка: ${data.message || "неизвестная"}`, "error");
        showNotification("Ошибка генерации", data.message || "Неизвестная ошибка", "error");
        return;
      }
      showTask(`Генерация... (${elapsedSec}с)`, "pending");
    } catch (err) {
      showTask(`${err.message}`, "error");
      showNotification("Ошибка", err.message, "error");
      return;
    }
    await new Promise(r => setTimeout(r, 1000));
  }
  showTask("Таймаут", "error");
  showNotification("Таймаут", "Генерация заняла слишком много времени", "error");
}

async function loadCollectionPreview() {
  if (!els.miniGallery || !state.auth?.token) {
    if (els.miniGallery) els.miniGallery.innerHTML = "<p class='meta'>Войдите для просмотра</p>";
    return;
  }
  try {
    const items = await api("/api/fractals");
    els.miniGallery.innerHTML = "";
    if (!items?.length) { els.miniGallery.innerHTML = "<p class='meta'>Коллекция пуста</p>"; return; }
    items.slice(0, 6).forEach(item => {
      const card = document.createElement("div");
      card.className = "mini-card";
      card.innerHTML = `<img src="/api/fractals/${item.id}/image" alt="${item.name || item.fractal_type}">`;
      card.onclick = () => {
        if (els.resultImg) {
          els.resultImg.src = `/api/fractals/${item.id}/image?t=${Date.now()}`;
          els.resultImg.classList.remove("hidden");
        }
        if (els.resultPlaceholder) els.resultPlaceholder.classList.add("hidden");
      };
      els.miniGallery.appendChild(card);
    });
  } catch (err) { els.miniGallery.innerHTML = `<p class="meta error">Ошибка: ${err.message}</p>`; }
}

async function handleAuth(action) {
  if (!els.authForm) { showAuthMsg("Ошибка: форма не найдена", "error"); return; }
  const fd = new FormData(els.authForm);
  const username = fd.get("username")?.trim();
  const password = fd.get("password");
  const confirm = fd.get("confirm_password");
  const email = fd.get("email")?.trim() || undefined;

  const pwdErr = validatePassword(password, action === "register" ? confirm : null);
  if (pwdErr) { showAuthMsg(`${pwdErr}`, "error"); return; }

  if (els.loginBtn) els.loginBtn.disabled = true;
  if (els.registerBtn) els.registerBtn.disabled = true;
  showAuthMsg("Обработка...", "info");

  try {
    const body = action === "register" ? { username, password, confirm_password: confirm, email } : { username, password };
    const data = await api(`/api/auth/${action}`, { method: "POST", body: JSON.stringify(body) });

    if (action === "register") {
      showAuthMsg("Регистрация успешна! Теперь войдите.", "success");
      showNotification("Регистрация", "Аккаунт создан успешно!", "success");
      els.authForm.querySelectorAll('input[type="password"]').forEach(f => f.value = "");
      const formTitle = els.authForm.querySelector("h3");
      if (formTitle) formTitle.textContent = "Вход в аккаунт";
      if (els.registerBtn) els.registerBtn.style.display = "none";
      if (els.loginBtn) { els.loginBtn.textContent = "Войти"; els.loginBtn.onclick = () => handleAuth("login"); }
      const closeBtn = $("close-auth");
      if (closeBtn) closeBtn.style.display = "inline-block";
    } else {
      state.auth = data;
      localStorage.setItem("fractal_auth", JSON.stringify(data));
      showAuthMsg(`Добро пожаловать, ${data.user.username}!`, "success");
      showNotification("Добро пожаловать!", `Вошли как ${data.user.username}`, "success");
      updateAuthUI();
      const modal = $("auth-modal");
      if (modal?.close) modal.close();
      await loadUserStats();
      await loadCollectionPreview();
    }
  } catch (err) {
    const msg = err.message?.includes("detail") ? JSON.parse(err.message).detail : err.message;
    showAuthMsg(`${msg}`, "error");
    showNotification("Ошибка", msg, "error");
  } finally {
    if (els.loginBtn) els.loginBtn.disabled = false;
    if (els.registerBtn) els.registerBtn.disabled = false;
  }
}

function logout() {
  state.auth = null;
  localStorage.removeItem("fractal_auth");
  updateAuthUI();
  if (els.resultImg) els.resultImg.classList.add("hidden");
  if (els.resultPlaceholder) els.resultPlaceholder.classList.remove("hidden");
  if (els.miniGallery) els.miniGallery.innerHTML = "";
  showAuthMsg("Вы вышли из аккаунта", "success");
  showNotification("До встречи!", "Вы вышли из аккаунта", "success");
}

async function loadUserStats() {
  const statsDetails = $("stats-details");

  if (!state.auth?.token) {
    if (statsDetails) statsDetails.style.display = "none";
    console.log("[Stats] Not authenticated, hiding stats block");
    return;
  }

  if (statsDetails) statsDetails.style.display = "block";

  try {
    console.log("[Stats] Loading stats...");
    const stats = await api('/api/user/stats');
    console.log("[Stats] Received:", stats);

    const statTotal = $("stat-total");
    const statFav = $("stat-fav");
    const statAvg = $("stat-avg");
    const statTotalTime = $("stat-total-time");

    if (statTotal) statTotal.textContent = stats.total_generated;
    if (statFav) statFav.textContent = stats.favorite_type
      ? stats.favorite_type.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
      : '—';
    if (statAvg) statAvg.textContent = (stats.avg_generation_time_ms / 1000).toFixed(1) + 'с';
    if (statTotalTime) statTotalTime.textContent = (stats.total_time_ms / 1000).toFixed(1) + 'с';

    console.log("[Stats] Rendered successfully");
  } catch (err) {
    console.error('[Stats] Error loading stats:', err);
    const statTotal = $("stat-total");
    if (statTotal) statTotal.textContent = "—";
  }
}

async function loadUserTags() {
  if (!state.auth?.token) return;
  try {
    const data = await api("/api/fractals/tags");
    userTags = (data.tags || []).filter(t => t !== "basic");
    console.log("[Tags] Loaded:", userTags);
  } catch (err) {
    console.warn('Не удалось загрузить теги:', err);
  }
}

function renderSelectedTags() {
  if (!els.selectedTagsDiv) return;
  els.selectedTagsDiv.innerHTML = selectedTags.map(tag => `
    <div class="selected-tag">
      ${tag}
      <span class="remove" onclick="removeTag('${tag}')">×</span>
    </div>
  `).join('');
}

function removeTag(tag) {
  selectedTags = selectedTags.filter(t => t !== tag);
  renderSelectedTags();
}

function addTag(tag) {
  const normalized = tag.trim().toLowerCase();
  if (!normalized || selectedTags.includes(normalized)) return;
  selectedTags.push(normalized);
  renderSelectedTags();
  if (els.tagInput) els.tagInput.value = '';
  if (els.tagSuggestions) els.tagSuggestions.classList.remove('show');
}

function showTagSuggestions(input) {
  if (!els.tagSuggestions) return;
  const filtered = userTags.filter(t =>
    t.toLowerCase().startsWith(input.toLowerCase()) &&
    !selectedTags.includes(t)
  );

  if (input.length === 0 || filtered.length === 0) {
    els.tagSuggestions.classList.remove('show');
    return;
  }

  els.tagSuggestions.innerHTML = filtered.map(tag =>
    `<div class="tag-suggestion" onclick="addTag('${tag}')">${tag}</div>`
  ).join('');
  els.tagSuggestions.classList.add('show');
}

function bindEvents() {
  if (els.fractalType) {
    showFractalParams(els.fractalType.value);

    els.fractalType.addEventListener("change", (e) => {
      const newType = e.target.value;
      clearIrrelevantFields(newType);
      showFractalParams(newType);
    });
  }

  if (els.generateForm) {
    els.generateForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      document.querySelectorAll("#generate-form details").forEach(d => d.open = true);

      if (!state.auth?.token) { showTask("Сначала войдите", "error"); return; }
      try {
        const payload = buildPayload();
        const data = await api("/api/fractals/generate", { method: "POST", body: JSON.stringify(payload) });
        if (data.task_id) await pollTask(data.task_id);
      } catch (err) {
        showTask(`${err.message}`, "error");
        showNotification("Ошибка запроса", err.message, "error");
      }
    });
  }

  if (els.loginBtn) els.loginBtn.onclick = () => handleAuth("login");
  if (els.registerBtn) els.registerBtn.onclick = () => handleAuth("register");
  if (els.logoutBtn) els.logoutBtn.onclick = logout;
  if (els.showAuthBtn) {
    els.showAuthBtn.onclick = () => { const m = $("auth-modal"); if (m?.showModal) m.showModal(); };
  }

  const modal = $("auth-modal");
  if (modal) {
    modal.onclick = (e) => {
      const rect = modal.getBoundingClientRect();
      if (e.clientX < rect.left || e.clientX > rect.right || e.clientY < rect.top || e.clientY > rect.bottom) {
        if (modal.close) modal.close();
      }
    };
  }
  const closeAuth = $("close-auth");
  if (closeAuth && modal?.close) closeAuth.onclick = () => { modal.close(); showAuthMsg(""); };

  if (els.presetSelect) {
    els.presetSelect.onchange = (e) => {
      const isCustom = !e.target.value || e.target.value === "custom";
      if (els.customParams) {
        if (isCustom) els.customParams.removeAttribute("hidden");
        else els.customParams.setAttribute("hidden", "");
      }
    };
  }

  if (els.addTransformBtn && els.transformsContainer) {
    els.addTransformBtn.onclick = () => {
      const idx = els.transformsContainer.querySelectorAll('.transform-item').length;
      els.transformsContainer.insertAdjacentHTML('beforeend', createTransformTemplate(idx));
    };
  }
  if (els.transformsContainer) {
    els.transformsContainer.onclick = (e) => {
      if (e.target.classList.contains('remove-transform')) {
        const item = e.target.closest('.transform-item');
        if (item) {
          item.remove();
          els.transformsContainer.querySelectorAll('.transform-item').forEach((el, i) => {
            const h = el.querySelector('.transform-header strong');
            if (h) h.textContent = `Трансформация #${i + 1}`;
          });
        }
      }
    };
  }
  if (els.loadPresetBtn) {
    els.loadPresetBtn.onclick = () => {
      const p = prompt("Пресет (fern, spiral, heart_flame, fisheye_grid):", "fern");
      if (p && loadPresetIntoCustom(p)) showAuthMsg(`Пресет '${p}' загружен`, "success");
      else if (p) showAuthMsg(`Неизвестный пресет: ${p}`, "error");
    };
  }

  if (els.tagInput) {
    els.tagInput.addEventListener("input", (e) => showTagSuggestions(e.target.value));
    els.tagInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        addTag(e.target.value);
      }
    });
    els.tagInput.addEventListener("blur", () => {
      setTimeout(() => {
        if (els.tagSuggestions) els.tagSuggestions.classList.remove('show');
      }, 200);
    });
  }
}

document.addEventListener("DOMContentLoaded", async () => {
  initEls();
  updateAuthUI();
  bindEvents();

  if (state.auth?.token) {
    await loadUserTags();
    await loadUserStats();
    await loadCollectionPreview();
  }
});