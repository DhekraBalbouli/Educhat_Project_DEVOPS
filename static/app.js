/* ═══════════════════════════════════════════
   EduChat — app.js
   Gère toutes les vues : Chat, Quiz, Exercices, Exécuter
═══════════════════════════════════════════ */
 
const API = "";  // même origine — FastAPI sert le HTML

// ── Utilitaires ───────────────────────────────────────────────────────────────
const $ = (sel, ctx = document) => ctx.querySelector(sel);
const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];
const show = el => el?.classList.remove("hidden");
const hide = el => el?.classList.add("hidden");
const loading = (on) => document.getElementById("loadingOverlay").classList.toggle("hidden", !on);
 
async function apiFetch(path, opts = {}) {
  loading(true);
  try {
    const res = await fetch(API + path, {
      headers: { "Content-Type": "application/json" },
      ...opts,
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Erreur réseau" }));
      throw new Error(err.detail || "Erreur inconnue");
    }
    return await res.json();
  } finally {
    loading(false);
  }
}
 
// ── Navigation ────────────────────────────────────────────────────────────────
$$(".nav-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    $$(".nav-btn").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    const view = btn.dataset.view;
    $$(".view").forEach(v => v.classList.remove("active"));
    $(`#view-${view}`).classList.add("active");
  });
});
 
// ── Chargement des langages ───────────────────────────────────────────────────
let LANGAGES = [];
 
async function initLangages() {
  try {
    const data = await apiFetch("/api/langages");
    LANGAGES = data.langages;
    // Sidebar chips
    const chips = document.getElementById("langagesList");
    chips.innerHTML = LANGAGES.map(l => `<span class="lang-chip">${l}</span>`).join("");
    // Boutons quiz
    renderLangBtns("quizLangBtns", LANGAGES, selectQuizLangage);
    // Boutons exercices
    renderLangBtns("exoLangBtns", LANGAGES, selectExoLangage);
    // Boutons exécuter
    renderLangBtns("execLangBtns", LANGAGES, selectExecLangage);
  } catch (e) {
    console.error("Impossible de charger les langages:", e);
  }
}
 
function renderLangBtns(containerId, langages, handler) {
  const container = document.getElementById(containerId);
  container.innerHTML = langages.map((l, i) =>
    `<button class="lang-btn${i === 0 ? " active" : ""}" data-lang="${l}">${l.charAt(0).toUpperCase() + l.slice(1)}</button>`
  ).join("");
  $$(".lang-btn", container).forEach(btn => {
    btn.addEventListener("click", () => {
      $$(".lang-btn", container).forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      handler(btn.dataset.lang);
    });
  });
  if (langages.length) handler(langages[0]);
}
 
// ════════════════════════════════════════════════
// CHAT
// ════════════════════════════════════════════════
const chatWindow = document.getElementById("chatWindow");
const chatInput  = document.getElementById("chatInput");
const chatSend   = document.getElementById("chatSend");
 
function addMsg(text, role = "bot") {
  const div = document.createElement("div");
  div.className = `msg ${role}`;
  const avatar = role === "bot" ? "🤖" : "👤";
  div.innerHTML = `
    <div class="msg-avatar">${avatar}</div>
    <div class="msg-bubble">${text}</div>
  `;
  chatWindow.appendChild(div);
  chatWindow.scrollTop = chatWindow.scrollHeight;
  return div;
}
 
function showTyping() {
  const div = document.createElement("div");
  div.className = "msg bot typing";
  div.innerHTML = `
    <div class="msg-avatar">🤖</div>
    <div class="msg-bubble">
      <span class="typing-dot"></span>
      <span class="typing-dot"></span>
      <span class="typing-dot"></span>
    </div>`;
  chatWindow.appendChild(div);
  chatWindow.scrollTop = chatWindow.scrollHeight;
  return div;
}
 
async function sendChat() {
  const msg = chatInput.value.trim();
  if (!msg) return;
  chatInput.value = "";
  chatInput.style.height = "auto";
  addMsg(escapeHtml(msg), "user");
  const typingEl = showTyping();
  try {
    const data = await fetch(API + "/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: msg }),
    });
    const json = await data.json();
    typingEl.remove();
    const langTag = json.langage ? ` <em>(${json.langage})</em>` : "";
    addMsg(escapeHtml(json.response) + langTag, "bot");
  } catch (e) {
    typingEl.remove();
    addMsg("❌ Erreur de connexion au serveur.", "bot");
  }
}
 
chatSend.addEventListener("click", sendChat);
chatInput.addEventListener("keydown", e => {
  if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); sendChat(); }
});
chatInput.addEventListener("input", () => {
  chatInput.style.height = "auto";
  chatInput.style.height = Math.min(chatInput.scrollHeight, 120) + "px";
});
 
// ════════════════════════════════════════════════
// QUIZ
// ════════════════════════════════════════════════
let quizData       = [];
let quizIndex      = 0;
let quizScore      = 0;
let quizLangage    = "";
let quizAnswered   = false;
 
async function selectQuizLangage(langage) {
  quizLangage = langage;
  hide(document.getElementById("quizContainer"));
  try {
    const data = await apiFetch(`/api/quiz/${langage}`);
    quizData  = data.questions;
    quizIndex = 0;
    quizScore = 0;
    show(document.getElementById("quizContainer"));
    hide(document.getElementById("quizResult"));
    show(document.getElementById("quizCard"));
    renderQuizQuestion();
  } catch (e) {
    alert(`Quiz non disponible : ${e.message}`);
  }
}
 
function renderQuizQuestion() {
  quizAnswered = false;
  const q = quizData[quizIndex];
  const total = quizData.length;
 
  document.getElementById("quizProgressText").textContent = `Question ${quizIndex + 1} / ${total}`;
  document.getElementById("progressFill").style.width = `${((quizIndex) / total) * 100}%`;
 
  document.getElementById("quizQuestion").textContent = q.question;
 
  const letters = ["A", "B", "C", "D"];
  const optionsEl = document.getElementById("quizOptions");
  optionsEl.innerHTML = q.options.map((opt, i) => `
    <button class="quiz-option" data-opt="${escapeAttr(opt)}">
      <span class="option-letter">${letters[i] || i + 1}</span>
      ${escapeHtml(opt)}
    </button>`).join("");
 
  $$(".quiz-option", optionsEl).forEach(btn => {
    btn.addEventListener("click", () => handleQuizAnswer(btn, q.answer));
  });
}
 
function handleQuizAnswer(btn, correctAnswer) {
  if (quizAnswered) return;
  quizAnswered = true;
 
  const selected = btn.dataset.opt;
  const isCorrect = selected.toLowerCase() === correctAnswer.toLowerCase();
 
  $$(".quiz-option").forEach(b => {
    b.disabled = true;
    if (b.dataset.opt.toLowerCase() === correctAnswer.toLowerCase()) b.classList.add("correct");
  });
 
  if (!isCorrect) {
    btn.classList.add("wrong");
  } else {
    quizScore++;
  }
 
  setTimeout(() => {
    quizIndex++;
    if (quizIndex < quizData.length) {
      renderQuizQuestion();
    } else {
      showQuizResult();
    }
  }, 1200);
}
 
function showQuizResult() {
  hide(document.getElementById("quizCard"));
  const resultEl = document.getElementById("quizResult");
  show(resultEl);
  const total = quizData.length;
  document.getElementById("resultScore").textContent = `${quizScore} / ${total}`;
  const pct = Math.round((quizScore / total) * 100);
  let msg = pct === 100 ? "🏆 Parfait ! Tu maîtrises ce langage !" :
            pct >= 60  ? "👍 Bon travail, continue comme ça !" :
                         "📚 Révise encore, tu peux faire mieux !";
  document.getElementById("resultMsg").textContent = msg;
  document.getElementById("progressFill").style.width = "100%";
}
 
document.getElementById("quizRetry").addEventListener("click", () => selectQuizLangage(quizLangage));
 
// ════════════════════════════════════════════════
// EXERCICES
// ════════════════════════════════════════════════
let exoList    = [];
let exoIndex   = 0;
let exoLangage = "";
 
async function selectExoLangage(langage) {
  exoLangage = langage;
  hide(document.getElementById("exerciceContainer"));
  try {
    const data = await apiFetch(`/api/exercices/${langage}`);
    exoList  = data.exercices;
    exoIndex = 0;
    if (exoList.length === 0) { alert("Aucun exercice disponible pour ce langage."); return; }
    show(document.getElementById("exerciceContainer"));
    document.getElementById("exoEditorLang").textContent = langage;
    document.getElementById("exoEditor").value = "";
    hide(document.getElementById("exoOutput"));
    renderExo();
  } catch (e) {
    alert(`Exercices non disponibles : ${e.message}`);
  }
}
 
function renderExo() {
  const exo = exoList[exoIndex];
  document.getElementById("exoEnonce").textContent = exo.enonce;
  document.getElementById("exoCounter").textContent = `${exoIndex + 1} / ${exoList.length}`;
  document.getElementById("exoPrev").disabled = exoIndex === 0;
  document.getElementById("exoNext").disabled = exoIndex === exoList.length - 1;
  document.getElementById("exoEditor").value = "";
  hide(document.getElementById("exoOutput"));
}
 
document.getElementById("exoPrev").addEventListener("click", () => { if (exoIndex > 0) { exoIndex--; renderExo(); }});
document.getElementById("exoNext").addEventListener("click", () => { if (exoIndex < exoList.length - 1) { exoIndex++; renderExo(); }});
 
document.getElementById("exoRun").addEventListener("click", async () => {
  const code = document.getElementById("exoEditor").value.trim();
  if (!code) { alert("Écris du code avant d'exécuter !"); return; }
  const btn = document.getElementById("exoRun");
  btn.disabled = true;
  btn.textContent = "⏳ En cours…";
  try {
    const data = await apiFetch("/api/exercices/check", {
      method: "POST",
      body: JSON.stringify({ code, langage: exoLangage, exercice_index: exoList[exoIndex].index }),
    });
    const outputEl = document.getElementById("exoOutput");
    const outputText = document.getElementById("exoOutputText");
    const verdictEl = document.getElementById("exoVerdict");
    show(outputEl);
    outputText.textContent = data.output || "(aucune sortie)";
    verdictEl.className = "verdict " + (data.correct ? "success" : "error");
    verdictEl.textContent = data.correct
      ? "✅ Correct ! Bravo !"
      : `❌ Incorrect. Attendu : ${data.expected}`;
  } catch (e) {
    alert(`Erreur : ${e.message}`);
  } finally {
    btn.disabled = false;
    btn.textContent = "▶ Exécuter";
  }
});
 
// ════════════════════════════════════════════════
// EXÉCUTER (bac à sable)
// ════════════════════════════════════════════════
let execLangage = "python";
 
function selectExecLangage(langage) {
  execLangage = langage;
  document.getElementById("execEditorLang").textContent = langage;
  const placeholder = {
    python: "# Exemple :\nprint('Hello, World!')",
    javascript: "// Exemple :\nconsole.log('Hello, World!');",
    c: '#include <stdio.h>\nint main() {\n    printf("Hello, World!\\n");\n    return 0;\n}',
  };
  document.getElementById("execEditor").placeholder = placeholder[langage] || "// Écris ton code ici…";
}
 
document.getElementById("execRun").addEventListener("click", async () => {
  const code = document.getElementById("execEditor").value.trim();
  if (!code) { alert("Écris du code avant d'exécuter !"); return; }
  const btn = document.getElementById("execRun");
  btn.disabled = true;
  btn.textContent = "⏳ En cours…";
  try {
    const data = await apiFetch("/api/execute", {
      method: "POST",
      body: JSON.stringify({ code, langage: execLangage }),
    });
    document.getElementById("execOutputText").textContent = data.output || "(aucune sortie)";
  } catch (e) {
    document.getElementById("execOutputText").textContent = `❌ Erreur : ${e.message}`;
  } finally {
    btn.disabled = false;
    btn.textContent = "▶ Exécuter";
  }
});
 
// Tab key in editors
["exoEditor", "execEditor"].forEach(id => {
  document.getElementById(id).addEventListener("keydown", e => {
    if (e.key === "Tab") {
      e.preventDefault();
      const el = e.target;
      const start = el.selectionStart;
      const end   = el.selectionEnd;
      el.value = el.value.substring(0, start) + "  " + el.value.substring(end);
      el.selectionStart = el.selectionEnd = start + 2;
    }
  });
});
 
// ── Escape helpers ────────────────────────────────────────────────────────────
function escapeHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}
function escapeAttr(str) {
  return String(str).replace(/"/g, "&quot;");
}
 
// ── Init ──────────────────────────────────────────────────────────────────────
initLangages();
 