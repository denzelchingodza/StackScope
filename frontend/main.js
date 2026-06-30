// main.js

const API = "https://stackscope-m75j.onrender.com";

async function get(endpoint) {
  const res = await fetch(`${API}${endpoint}`);
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

// Skill selector setup
const skillGroups = {
  "g-lang":  ["Python", "JavaScript", "TypeScript", "Java", "Go", "C#", "SQL", "Rust"],
  "g-fw":    ["React", "Node.js", "Django", "FastAPI", "Flask", "Vue", "Angular", "Spring"],
  "g-tools": ["PostgreSQL", "MongoDB", "Docker", "AWS", "Git", "Linux", "Redis", "Kubernetes"],
};

const selected = new Set();

Object.entries(skillGroups).forEach(([id, skills]) => {
  const container = document.getElementById(id);
  if (!container) return;
  skills.forEach(skill => {
    const chip = document.createElement("span");
    chip.className = "skill-chip";
    chip.textContent = skill;
    chip.addEventListener("click", () => {
      const key = skill.toLowerCase();
      if (selected.has(key)) {
        selected.delete(key);
        chip.classList.remove("selected");
      } else {
        selected.add(key);
        chip.classList.add("selected");
      }
      const count = selected.size;
      document.getElementById("sel-count").textContent =
        count === 0 ? "0 skills selected" :
        count === 1 ? "1 skill selected" :
        `${count} skills selected`;
    });
    container.appendChild(chip);
  });
});

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
    const [health, salary] = await Promise.all([
      get("/api/health"),
      get("/api/salary/stats"),
    ]);
    if (health.jobs_tracked !== undefined) {
      document.getElementById("stat-jobs").textContent =
        health.jobs_tracked.toLocaleString();
    }
  } catch {
    // keep default values already in the HTML
  }
}

// Jobs table
async function loadJobs() {
  try {
    const jobs = await get("/api/jobs?limit=50");
    const tbody = document.getElementById("jobs-body");
    if (!tbody || !jobs.length) return;
    tbody.innerHTML = jobs.map(j => `
      <tr>
        <td class="td-title">${j.title}</td>
        <td class="td-co">${j.company}</td>
        <td class="td-loc">${j.location}</td>
        <td>
          <div class="skill-tags">
            ${(j.skills || "").split(",").slice(0, 3).map(s =>
              `<span class="stag">${s.trim()}</span>`
            ).join("")}
          </div>
        </td>
        <td><span class="lvl ${lvlClass(j.experience_level)}">${cap(j.experience_level)}</span></td>
        <td>
          <a class="src-link" href="${j.url || srcUrl(j.source)}" target="_blank" rel="noopener">
            <img class="src-ico" src="https://www.google.com/s2/favicons?domain=${srcDomain(j.source)}&sz=32" alt="${j.source}" />
            <span>${j.source}</span>
          </a>
        </td>
      </tr>`).join("");
  } catch {
    // keep demo rows already in the HTML
  }
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
  const map = { "Indeed": "indeed.com", "PNet": "pnet.co.za", "Careers24": "careers24.com" };
  return map[source] || "indeed.com";
}

function srcUrl(source) {
  const map = { "Indeed": "https://za.indeed.com", "PNet": "https://www.pnet.co.za", "Careers24": "https://www.careers24.com" };
  return map[source] || "#";
}

// Analyse
async function analyse() {
  if (selected.size === 0) {
    alert("Select at least one skill first.");
    return;
  }

  const skills = [...selected];

  try {
    const [gap, matches] = await Promise.all([
      post("/api/gap",   { skills }),
      post("/api/match", { skills, top_n: 3 }),
    ]);
    renderResults(gap, matches);
  } catch {
    // fallback demo result
    const allSkills = ["python","javascript","sql","react","docker","typescript","git","java","postgresql","aws","node.js","linux","mongodb","redis","django"];
    const have    = skills.filter(s => allSkills.includes(s));
    const missing = allSkills.filter(s => !skills.includes(s)).slice(0, 6);
    const score   = Math.min(96, Math.round((have.length / allSkills.length) * 100 * 3 + 8));
    renderResults(
      { score: Math.min(96, score), have, missing, summary: summaryText(score) },
      [
        { title: "Junior Python Developer", company: "DataCore",   location: "Remote",     match_score: 91, url: "#" },
        { title: "Backend Engineer",        company: "FinTech SA", location: "Cape Town",  match_score: 84, url: "#" },
        { title: "Full Stack Developer",    company: "BuildCo",    location: "Joburg",     match_score: 76, url: "#" },
      ]
    );
  }
}

function summaryText(score) {
  if (score >= 70) return "Strong alignment with the market. You match most of what employers are asking for right now.";
  if (score >= 45) return "Solid foundation. A few additions would open up significantly more roles.";
  return "Good start. The skills below are your fastest path to more job matches.";
}

function renderResults(gap, matches) {
  document.getElementById("score-big").textContent  = gap.score + "%";
  document.getElementById("score-desc").textContent = gap.summary || summaryText(gap.score);

  document.getElementById("have-chips").innerHTML =
    (gap.have || []).map(s => `<span class="chip-have">${s}</span>`).join("") ||
    `<span class="chip-miss">none matched yet</span>`;

  document.getElementById("miss-chips").innerHTML =
    (gap.missing || []).map(s => `<span class="chip-miss">${s}</span>`).join("");

  document.getElementById("job-cards").innerHTML =
    (matches || []).map(j => `
      <div class="job-card">
        <span class="job-pct">${j.match_score}% match</span>
        <div class="job-title-c">${j.title}</div>
        <div class="job-co-c">${j.company} &middot; ${j.location}</div>
        <a class="job-link" href="${j.url || "#"}" target="_blank" rel="noopener">View posting</a>
      </div>`).join("");

  const box = document.getElementById("result-box");
  box.style.display = "block";
  box.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

// Init
async function init() {
  await Promise.all([loadStats(), loadBars(), loadJobs()]);
}

init();
