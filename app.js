let selectedGrade = "all";
let selectedCategory = "all";
let searchQuery = "";

const gradeButtons = document.querySelectorAll("#grade-filters .pill");
const categoryButtons = document.querySelectorAll("#category-filters .pill");
const searchInput = document.getElementById("search-input");
const resultsCount = document.getElementById("results-count");
const grid = document.getElementById("opportunities-grid");

function getCategoryBadgeClass(category) {
  if (category === "Scholarship") return "badge-scholarship";
  if (category === "Summer Program") return "badge-summer";
  return "badge-research";
}

function formatGrades(grades) {
  return grades.map((g) => `Grade ${g}`).join(", ");
}

function matchesFilters(item) {
  const gradeMatch =
    selectedGrade === "all" || item.grades.includes(Number(selectedGrade));
  const categoryMatch =
    selectedCategory === "all" || item.category === selectedCategory;

  const q = searchQuery.trim().toLowerCase();
  const textMatch =
    !q ||
    item.title.toLowerCase().includes(q) ||
    item.category.toLowerCase().includes(q) ||
    item.focus.toLowerCase().includes(q) ||
    item.description.toLowerCase().includes(q) ||
    item.award.toLowerCase().includes(q);

  return gradeMatch && categoryMatch && textMatch;
}

function renderOpportunities() {
  const filtered = OPPORTUNITIES.filter(matchesFilters);
  resultsCount.textContent = `Showing ${filtered.length} ${
    filtered.length === 1 ? "opportunity" : "opportunities"
  }`;

  if (filtered.length === 0) {
    grid.innerHTML = `
      <div class="empty-state">
        <h2>No matching opportunities found</h2>
        <p>Try switching back to <strong>All Grades</strong> or <strong>All Types</strong>, or clear your search box.</p>
      </div>
    `;
    return;
  }

  grid.innerHTML = filtered
    .map(
      (item) => `
      <article class="card">
        <div>
          <div class="card-top">
            <span class="badge ${getCategoryBadgeClass(item.category)}">${item.category}</span>
            <span class="grades-text">${formatGrades(item.grades)}</span>
          </div>
          <h2>${item.title}</h2>
          <p>${item.description}</p>
          <ul class="meta-list">
            <li><strong>Award / Program:</strong> ${item.award}</li>
            <li><strong>Focus:</strong> ${item.focus}</li>
          </ul>
        </div>
        <div class="card-footer">
          <span class="deadline-text">Window: ${item.deadlineWindow}</span>
          <a class="apply-btn" href="${item.url}" target="_blank" rel="noopener noreferrer">Official Site</a>
        </div>
      </article>
    `
    )
    .join("");
}

gradeButtons.forEach((btn) => {
  btn.addEventListener("click", () => {
    gradeButtons.forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    selectedGrade = btn.dataset.grade;
    renderOpportunities();
  });
});

categoryButtons.forEach((btn) => {
  btn.addEventListener("click", () => {
    categoryButtons.forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    selectedCategory = btn.dataset.category;
    renderOpportunities();
  });
});

searchInput.addEventListener("input", (e) => {
  searchQuery = e.target.value;
  renderOpportunities();
});

renderOpportunities();
