let allOpportunities = [];
let selectedGrade = "all";
let selectedCategory = "All";
let searchQuery = "";
let showSavedOnly = false;
let savedIds = JSON.parse(localStorage.getItem("scholarhub_saved") || "[]");

const cardsGrid = document.getElementById("cardsGrid");
const resultsCount = document.getElementById("resultsCount");
const searchInput = document.getElementById("searchInput");
const gradeFilters = document.getElementById("gradeFilters");
const categoryFilters = document.getElementById("categoryFilters");
const resetFiltersBtn = document.getElementById("resetFiltersBtn");
const savedToggleBtn = document.getElementById("savedToggleBtn");
const savedCount = document.getElementById("savedCount");

async function init() {
  updateSavedCounter();
  try {
    const response = await fetch("./scholarhub-opportunities.json");
    allOpportunities = await response.json();
    renderCards();
  } catch (err) {
    cardsGrid.innerHTML = `
      <div class="empty-state">
        <h3>Unable to load opportunities</h3>
        <p>Make sure <code>scholarhub-opportunities.json</code> is in the same folder as <code>index.html</code>.</p>
      </div>
    `;
  }
}

function getBadgeClass(category) {
  if (category === "Scholarship") return "badge-scholarship";
  if (category === "Research") return "badge-research";
  return "badge-summer";
}

function toggleSave(id) {
  if (savedIds.includes(id)) {
    savedIds = savedIds.filter(item => item !== id);
  } else {
    savedIds.push(id);
  }
  localStorage.setItem("scholarhub_saved", JSON.stringify(savedIds));
  updateSavedCounter();
  renderCards();
}

function updateSavedCounter() {
  savedCount.textContent = savedIds.length;
}

function renderCards() {
  const filtered = allOpportunities.filter(item => {
    const matchesGrade =
      selectedGrade === "all" || item.grades.includes(Number(selectedGrade));
    const matchesCategory =
      selectedCategory === "All" || item.category === selectedCategory;
    const matchesSaved = !showSavedOnly || savedIds.includes(item.id);
    const q = searchQuery.toLowerCase().trim();
    const matchesSearch =
      !q ||
      item.title.toLowerCase().includes(q) ||
      item.description.toLowerCase().includes(q) ||
      item.category.toLowerCase().includes(q) ||
      item.amountOrCost.toLowerCase().includes(q);

    return matchesGrade && matchesCategory && matchesSaved && matchesSearch;
  });

  resultsCount.textContent = `Showing ${filtered.length} opportunit${
    filtered.length === 1 ? "y" : "ies"
  }`;

  if (filtered.length === 0) {
    cardsGrid.innerHTML = `
      <div class="empty-state">
        <h3>No matching opportunities found</h3>
        <p>Try selecting a different grade level, clearing your search, or resetting filters.</p>
      </div>
    `;
    return;
  }

  cardsGrid.innerHTML = filtered
    .map(item => {
      const isSaved = savedIds.includes(item.id);
      const gradeBadges = item.grades
        .map(g => `<span class="grade-tag">${g}th Grade</span>`)
        .join("");

      return `
        <article class="card">
          <div>
            <div class="card-top">
              <span class="badge ${getBadgeClass(item.category)}">${item.category}</span>
              <button class="bookmark-btn ${isSaved ? "saved" : ""}" onclick="toggleSave(${item.id})">
                ${isSaved ? "♥ Saved" : "♡ Save"}
              </button>
            </div>
            <h3>${item.title}</h3>
            <p class="card-desc">${item.description}</p>
          </div>

          <div>
            <div class="grade-tags">${gradeBadges}</div>
            <div class="meta-list">
              <div class="meta-row">
                <span class="meta-key">Award / Cost:</span>
                <span class="meta-val">${item.amountOrCost}</span>
              </div>
              <div class="meta-row">
                <span class="meta-key">Typical Deadline:</span>
                <span class="meta-val">${item.deadline}</span>
              </div>
            </div>
            <a href="${item.link}" target="_blank" rel="noopener noreferrer" class="apply-btn">
              Visit Official Website ↗
            </a>
          </div>
        </article>
      `;
    })
    .join("");
}

// Event Listeners
gradeFilters.addEventListener("click", e => {
  if (!e.target.classList.contains("filter-btn")) return;
  document.querySelectorAll("#gradeFilters .filter-btn").forEach(btn => btn.classList.remove("active"));
  e.target.classList.add("active");
  selectedGrade = e.target.dataset.grade;
  renderCards();
});

categoryFilters.addEventListener("click", e => {
  if (!e.target.classList.contains("filter-btn")) return;
  document.querySelectorAll("#categoryFilters .filter-btn").forEach(btn => btn.classList.remove("active"));
  e.target.classList.add("active");
  selectedCategory = e.target.dataset.category;
  renderCards();
});

searchInput.addEventListener("input", e => {
  searchQuery = e.target.value;
  renderCards();
});

savedToggleBtn.addEventListener("click", () => {
  showSavedOnly = !showSavedOnly;
  savedToggleBtn.classList.toggle("active", showSavedOnly);
  renderCards();
});

resetFiltersBtn.addEventListener("click", () => {
  selectedGrade = "all";
  selectedCategory = "All";
  searchQuery = "";
  showSavedOnly = false;
  searchInput.value = "";
  savedToggleBtn.classList.remove("active");

  document.querySelectorAll("#gradeFilters .filter-btn").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.grade === "all");
  });
  document.querySelectorAll("#categoryFilters .filter-btn").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.category === "All");
  });

  renderCards();
});

init();
