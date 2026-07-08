// main.js

const API = "https://stackscope-m75j.onrender.com";

// ── LOADER ──────────────────────────────────────────────────────────
const LOADER_SKILLS = [
  "Python","React","Docker","TypeScript","AWS","Node.js","Kubernetes",
  "PostgreSQL","Go","Rust","FastAPI","GraphQL","Terraform","Redis",
  "Machine Learning","Vue","Spring","MongoDB","Azure","GCP","SQL",
  "CI/CD","Pandas","PyTorch","Linux","Git","Next.js","Elixir","Scala",
];

const LOADER_SOURCES = [
  { id: "lsrc-adzuna",     label: "Fetching Adzuna SA jobs..." },
  { id: "lsrc-remotive",   label: "Scanning Remotive..." },
  { id: "lsrc-wwr",        label: "Checking We Work Remotely..." },
  { id: "lsrc-jobspresso", label: "Loading Jobspresso..." },
];

function spawnTag(container) {
  const tag = document.createElement("span");
  tag.className = "ltag";
  tag.textContent = LOADER_SKILLS[Math.floor(Math.random() * LOADER_SKILLS.length)];
  tag.style.left = Math.random() * 92 + "%";
  const dur = 7 + Math.random() * 8;
  tag.style.animationDuration = dur + "s";
  tag.style.animationDelay = (Math.random() * -dur) + "s";
  container.appendChild(tag);
  setTimeout(() => tag.remove(), (dur + 1) * 1000);
}

function startFloatingTags() {
  const container = document.getElementById("loader-tags");
  if (!container) return;
  // seed initial tags
  for (let i = 0; i < 14; i++) spawnTag(container);
  return setInterval(() => spawnTag(container), 700);
}

async function waitForBackend() {
  const loader = document.getElementById("loader");
  const sourceEl = document.getElementById("loader-source");
  const elapsedEl = document.getElementById("loader-elapsed");
  const maxWait = 60000;
  const pollInterval = 3000;
  const start = Date.now();

  const tagTimer = startFloatingTags();

  // Cycle through source labels while waiting
  let srcIdx = 0;
  const srcTimer = setInterval(() => {
    if (sourceEl) sourceEl.textContent = LOADER_SOURCES[srcIdx % LOADER_SOURCES.length].label;
    const pill = document.getElementById(LOADER_SOURCES[srcIdx % LOADER_SOURCES.length].id);
    if (pill) pill.classList.add("active");
    srcIdx++;
  }, 2200);

  // Elapsed counter
  const clockTimer = setInterval(() => {
    const s = Math.round((Date.now() - start) / 1000);
    if (elapsedEl) elapsedEl.textContent = s + "s";
  }, 1000);

  const cleanup = () => {
    clearInterval(tagTimer);
    clearInterval(srcTimer);
    clearInterval(clockTimer);
  };

  while (Date.now() - start < maxWait) {
    try {
      const res = await fetch(`${API}/api/health`, { signal: AbortSignal.timeout(5000) });
      if (res.ok) {
        if (sourceEl) sourceEl.textContent = "Ready.";
        LOADER_SOURCES.forEach(s => {
          const el = document.getElementById(s.id);
          if (el) el.classList.add("active");
        });
        cleanup();
        await new Promise(r => setTimeout(r, 600));
        loader.classList.add("hidden");
        setTimeout(() => loader.remove(), 700);
        return;
      }
    } catch { /* still sleeping */ }
    await new Promise(r => setTimeout(r, pollInterval));
  }

  // Timed out
  if (sourceEl) sourceEl.textContent = "Taking longer than usual...";
  cleanup();
  await new Promise(r => setTimeout(r, 1200));
  loader.classList.add("hidden");
  setTimeout(() => loader.remove(), 700);
}

waitForBackend();

async function get(endpoint) {
  const res = await fetch(`${API}${endpoint}`, { signal: AbortSignal.timeout(60000) });
  if (!res.ok) throw new Error(`Failed: ${endpoint}`);
  return res.json();
}

async function post(endpoint, body) {
  const res = await fetch(`${API}${endpoint}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`Failed: ${endpoint}`);
  return res.json();
}

// ── SKILL MATCHER ────────────────────────────────────────────────────
// [value sent to API, display label]
const SKILL_GROUPS = [
  { label: "Languages", chips: [
    ["python","Python"],["javascript","JavaScript"],["typescript","TypeScript"],
    ["java","Java"],["c#","C#"],["c++","C++"],["go","Go"],["rust","Rust"],
    ["ruby","Ruby"],["php","PHP"],["swift","Swift"],["kotlin","Kotlin"],
    ["scala","Scala"],["elixir","Elixir"],["bash","Bash"],["clojure","Clojure"],
  ]},
  { label: "Frontend", chips: [
    ["react","React"],["vue","Vue"],["angular","Angular"],["next.js","Next.js"],
    ["svelte","Svelte"],["html","HTML"],["css","CSS"],["tailwind","Tailwind"],
    ["webpack","Webpack"],["vite","Vite"],
  ]},
  { label: "Backend", chips: [
    ["node.js","Node.js"],["django","Django"],["flask","Flask"],["fastapi","FastAPI"],
    ["spring","Spring"],["rails","Rails"],["laravel","Laravel"],["express","Express"],
    ["graphql","GraphQL"],["rest api","REST API"],["grpc","gRPC"],
  ]},
  { label: "Data and AI", chips: [
    ["machine learning","Machine Learning"],["deep learning","Deep Learning"],
    ["tensorflow","TensorFlow"],["pytorch","PyTorch"],["scikit-learn","scikit-learn"],
    ["pandas","Pandas"],["numpy","NumPy"],["spark","Spark"],["airflow","Airflow"],
    ["dbt","dbt"],["llm","LLM"],["openai","OpenAI"],["langchain","LangChain"],
    ["data engineering","Data Engineering"],["data science","Data Science"],
  ]},
  { label: "Databases", chips: [
    ["postgresql","PostgreSQL"],["mysql","MySQL"],["mongodb","MongoDB"],
    ["redis","Redis"],["elasticsearch","Elasticsearch"],["sqlite","SQLite"],
    ["dynamodb","DynamoDB"],["cassandra","Cassandra"],["snowflake","Snowflake"],
    ["bigquery","BigQuery"],["supabase","Supabase"],["sql","SQL"],
  ]},
  { label: "DevOps and Cloud", chips: [
    ["docker","Docker"],["kubernetes","Kubernetes"],["aws","AWS"],
    ["azure","Azure"],["gcp","GCP"],["terraform","Terraform"],
    ["ansible","Ansible"],["github actions","GitHub Actions"],["jenkins","Jenkins"],
    ["linux","Linux"],["git","Git"],["ci/cd","CI/CD"],
  ]},
  { label: "Other", chips: [
    ["cybersecurity","Cybersecurity"],["microservices","Microservices"],
    ["api design","API Design"],["system design","System Design"],
    ["blockchain","Blockchain"],["solidity","Solidity"],
    ["embedded","Embedded"],["iot","IoT"],
  ]},
];

const selected = new Set();
let matcherLevel  = "all";
let matcherRegion = "all";

function setMatchLevel(val, btn) {
  matcherLevel = val;
  document.getElementById("level-row").querySelectorAll(".level-btn")
    .forEach(b => b.classList.remove("active"));
  btn.classList.add("active");
}

function setMatchRegion(val, btn) {
  matcherRegion = val;
  document.getElementById("region-row").querySelectorAll(".level-btn")
    .forEach(b => b.classList.remove("active"));
  btn.classList.add("active");
}

function updateSelCount() {
  const n = selected.size;
  document.getElementById("sel-count").textContent =
    n === 0 ? "0 skills selected" :
    n === 1 ? "1 skill selected" : `${n} skills selected`;
}

// Build skill chip groups
(function buildSkillGroups() {
  const container = document.getElementById("skill-groups");
  if (!container) return;
  SKILL_GROUPS.forEach(group => {
    const groupEl = document.createElement("div");
    groupEl.className = "skill-group";
    groupEl.innerHTML = `<div class="group-label">${group.label}</div>`;
    const row = document.createElement("div");
    row.className = "chip-row";
    group.chips.forEach(([value, label]) => {
      const chip = document.createElement("span");
      chip.className = "skill-chip";
      chip.textContent = label;
      chip.addEventListener("click", () => {
        if (selected.has(value)) {
          selected.delete(value);
          chip.classList.remove("selected");
        } else {
          selected.add(value);
          chip.classList.add("selected");
        }
        updateSelCount();
      });
      row.appendChild(chip);
    });
    groupEl.appendChild(row);
    container.appendChild(groupEl);
  });
})();

// Skill frequency bars
async function loadBars() {
  try {
    const data = await get("/api/skills/frequency?limit=8");
    renderBars(data);
    if (data.length > 0) {
      document.getElementById("stat-skill").textContent = data[0].skill;
    }
  } catch {
    // fallback demo data if API not running
    renderBars([
      { skill: "Python",     count: 847 },
      { skill: "JavaScript", count: 763 },
      { skill: "SQL",        count: 698 },
      { skill: "React",      count: 612 },
      { skill: "Docker",     count: 534 },
      { skill: "TypeScript", count: 489 },
      { skill: "Git",        count: 471 },
      { skill: "Java",       count: 398 },
    ]);
  }
}

function renderBars(data) {
  const el = document.getElementById("bars");
  if (!el || !data.length) return;
  const max = data[0].count;
  el.innerHTML = data.map(d => {
    const pct = Math.round((d.count / max) * 100);
    return `
      <div class="bar-row">
        <span class="bar-label">${d.skill}</span>
        <div class="bar-track">
          <div class="bar-fill" style="width:${pct}%">
            <span>${d.count}</span>
          </div>
        </div>
      </div>`;
  }).join("");
}

// Stats
async function loadStats() {
  try {
    const health = await get("/api/health");
    if (health.jobs_tracked !== undefined) {
      document.getElementById("stat-jobs").textContent =
        health.jobs_tracked.toLocaleString();
    }
  } catch { /* keep placeholder */ }

  try {
    const salary = await get("/api/salary/stats");
    const avg = salary?.avg_salary_min ?? salary?.avg ?? null;
    if (avg) {
      const el = document.getElementById("stat-salary");
      if (el) el.textContent = "R" + Math.round(avg).toLocaleString();
    } else {
      const el = document.getElementById("stat-salary");
      if (el) el.textContent = "No data yet";
    }
  } catch {
    const el = document.getElementById("stat-salary");
    if (el) el.textContent = "No data yet";
  }
}

// Trends
async function loadTrends() {
  const el = document.getElementById("trend-list");
  const risingEl = document.getElementById("stat-rising");
  if (!el) return;

  try {
    const data = await get("/api/trends");

    if (!data || !data.length) {
      el.innerHTML = `<p style="color:#475569;font-size:13px;padding:8px 0">Trends appear after 2 weeks of data have been collected.</p>`;
      if (risingEl) risingEl.textContent = "No data yet";
      return;
    }

    const rising   = data.filter(d => d.direction === "rising");
    const declining = data.filter(d => d.direction === "declining");

    if (risingEl) risingEl.textContent = rising.length
      ? rising.length + " rising"
      : "0 rising";

    // Show top 4 rising + top 3 declining
    const rows = [
      ...rising.slice(0, 4),
      ...declining.slice(-3).reverse(),
    ];

    el.innerHTML = rows.map(d => {
      const up = d.direction === "rising";
      const pct = Math.abs(d.change_percent);
      return `
        <div class="trend-row">
          <span>${cap(d.skill)}</span>
          <span class="badge ${up ? "up" : "dn"}">${up ? "↑" : "↓"} ${pct}%</span>
        </div>`;
    }).join("");

  } catch {
    el.innerHTML = `<p style="color:#475569;font-size:13px;padding:8px 0">Could not load trends.</p>`;
    if (risingEl) risingEl.textContent = "...";
  }
}

// ── JOBS TABLE ───────────────────────────────────────────────────────
let allJobs    = [];
let currentPage = 1;
const PAGE_SIZE = 20;

async function loadJobs() {
  try {
    allJobs = await get("/api/jobs?limit=500");
    currentPage = 1;
    renderJobTable();
  } catch {
    // keep placeholder row
  }
}

function getFiltered() {
  const region = document.getElementById("filter-region")?.value || "all";
  const level  = document.getElementById("filter-level")?.value  || "all";
  const source = document.getElementById("filter-source")?.value || "all";

  return allJobs.filter(j => {
    const country = (j.country || "").toUpperCase();
    const lvl     = (j.experience_level || "").toLowerCase();
    const src     = (j.source || "");

    if (region !== "all" && country !== region) return false;
    if (level  !== "all" && lvl    !== level)  return false;
    if (source !== "all" && src    !== source) return false;
    return true;
  });
}

function onFilterChange() {
  currentPage = 1;
  renderJobTable();
}

function renderJobTable() {
  const tbody     = document.getElementById("jobs-body");
  const countEl   = document.getElementById("jobs-count");
  const pagEl     = document.getElementById("pagination");
  if (!tbody) return;

  const filtered  = getFiltered();
  const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  if (currentPage > totalPages) currentPage = totalPages;

  const start  = (currentPage - 1) * PAGE_SIZE;
  const page   = filtered.slice(start, start + PAGE_SIZE);

  if (countEl) countEl.textContent = filtered.length
    ? `${filtered.length} job${filtered.length === 1 ? "" : "s"}`
    : "";

  if (!filtered.length) {
    tbody.innerHTML = `<tr><td colspan="6" style="text-align:center;padding:28px;color:#475569">No jobs match these filters.</td></tr>`;
    if (pagEl) pagEl.innerHTML = "";
    return;
  }

  tbody.innerHTML = page.map(j => {
    const region = (j.country || "").toUpperCase() === "ZA" ? "South Africa" : "Remote";
    const skills = (j.skills || "").split(",").filter(s => s.trim()).slice(0, 3);
    return `
      <tr>
        <td class="td-title"><a href="${j.url || "#"}" target="_blank" rel="noopener" style="color:inherit;text-decoration:none">${j.title}</a></td>
        <td class="td-co">${j.company}</td>
        <td class="td-loc">${region}</td>
        <td><div class="skill-tags">${skills.map(s => `<span class="stag">${s.trim()}</span>`).join("")}</div></td>
        <td><span class="lvl ${lvlClass(j.experience_level)}">${cap(j.experience_level)}</span></td>
        <td>
          <a class="src-link" href="${srcUrl(j.source)}" target="_blank" rel="noopener">
            <img class="src-ico" src="https://www.google.com/s2/favicons?domain=${srcDomain(j.source)}&sz=32" alt="${j.source}" />
            <span>${j.source}</span>
          </a>
        </td>
      </tr>`;
  }).join("");

  // Pagination
  if (pagEl) {
    if (totalPages <= 1) {
      pagEl.innerHTML = "";
    } else {
      pagEl.innerHTML = `
        <button class="page-btn" onclick="goPage(${currentPage - 1})" ${currentPage === 1 ? "disabled" : ""}>Previous</button>
        <span class="page-info">Page ${currentPage} of ${totalPages}</span>
        <button class="page-btn" onclick="goPage(${currentPage + 1})" ${currentPage === totalPages ? "disabled" : ""}>Next</button>
      `;
    }
  }
}

function goPage(n) {
  currentPage = n;
  renderJobTable();
  document.getElementById("jobs")?.scrollIntoView({ behavior: "smooth", block: "start" });
}

function lvlClass(level) {
  if (!level) return "mid";
  if (level === "junior") return "jun";
  if (level === "senior") return "sen";
  return "mid";
}

function cap(str) {
  if (!str) return "Unspecified";
  return str.charAt(0).toUpperCase() + str.slice(1);
}

function srcDomain(source) {
  const map = {
    "Adzuna SA":        "adzuna.com",
    "Remotive":         "remotive.com",
    "We Work Remotely": "weworkremotely.com",
    "Jobspresso":       "jobspresso.co",
    "Indeed SA":        "indeed.com",
    "PNet":             "pnet.co.za",
    "Careers24":        "careers24.com",
  };
  return map[source] || "google.com";
}

function srcUrl(source) {
  const map = {
    "Adzuna SA":        "https://www.adzuna.co.za",
    "Remotive":         "https://remotive.com",
    "We Work Remotely": "https://weworkremotely.com",
    "Jobspresso":       "https://jobspresso.co",
    "Indeed SA":        "https://za.indeed.com",
    "PNet":             "https://www.pnet.co.za",
    "Careers24":        "https://www.careers24.com",
  };
  return map[source] || "#";
}

// Analyse
async function analyse() {
  if (selected.size === 0) {
    alert("Select at least one skill first.");
    return;
  }

  const skills = [...selected];
  const btn = document.querySelector(".btn-primary");
  if (btn) { btn.textContent = "Analysing..."; btn.disabled = true; }

  try {
    const [gap, matches] = await Promise.all([
      post("/api/gap",   { skills, experience_level: matcherLevel, region: matcherRegion }),
      post("/api/match", { skills, experience_level: matcherLevel, region: matcherRegion, top_n: 5 }),
    ]);
    renderResults(gap, matches);
  } catch {
    renderResults(
      { score: 0, have: [], missing: [], summary: "Could not load results. Make sure the backend is awake." },
      []
    );
  } finally {
    if (btn) { btn.textContent = "See my results"; btn.disabled = false; }
  }
}

function summaryText(score) {
  if (score >= 75) return "Strong market alignment. You cover most of what employers are hiring for right now.";
  if (score >= 50) return "Good foundation. A few targeted additions would open up significantly more roles.";
  if (score >= 25) return "Solid start. The skills below are your fastest path to more job matches.";
  return "Early stage. Focus on the top missing skills to build market relevance quickly.";
}

function renderResults(gap, matches) {
  document.getElementById("score-big").textContent  = gap.score + "%";
  document.getElementById("score-desc").textContent = gap.summary || summaryText(gap.score);

  document.getElementById("have-chips").innerHTML =
    (gap.have || []).length
      ? (gap.have).map(s => `<span class="chip-have">${cap(s)}</span>`).join("")
      : `<span style="font-size:12px;color:#94a3b8">None of the top skills matched yet</span>`;

  document.getElementById("miss-chips").innerHTML =
    (gap.missing || []).slice(0, 8).map(s => `<span class="chip-miss">${cap(s)}</span>`).join("");

  document.getElementById("job-cards").innerHTML =
    (matches || []).length
      ? matches.map(j => `
          <div class="job-card">
            <span class="job-pct">${j.match_score}% match</span>
            ${j.experience_level && j.experience_level !== "unspecified"
              ? `<span class="job-level-badge">${cap(j.experience_level)}</span>` : ""}
            <div class="job-title-c">${j.title}</div>
            <div class="job-co-c">${j.company} &middot; ${j.location}</div>
            ${(j.missing_skills || []).length
              ? `<div class="job-card-missing">${j.missing_skills.slice(0,3).map(s => `<span class="chip-gap">${cap(s)}</span>`).join("")}</div>`
              : ""}
            <a class="job-link" href="${j.url || "#"}" target="_blank" rel="noopener">View posting</a>
          </div>`).join("")
      : `<p style="font-size:13px;color:#94a3b8;padding:4px 0">No matching jobs found for these filters. Try broadening your level or region.</p>`;

  const box = document.getElementById("result-box");
  box.style.display = "block";
  box.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

// Init
async function init() {
  await Promise.all([loadStats(), loadBars(), loadTrends(), loadJobs()]);
}

init();
