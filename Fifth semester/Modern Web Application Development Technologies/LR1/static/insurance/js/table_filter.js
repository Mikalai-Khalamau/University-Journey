/**
 * Поиск и сортировка таблиц на стороне фронта (без перезагрузки).
 */
(function () {
  function initTable(table) {
    const tbody = table.querySelector("tbody");
    if (!tbody) return;
    const allRows = Array.from(tbody.querySelectorAll("tr"));

    const toolbar = document.createElement("div");
    toolbar.style.marginBottom = "0.5rem";
    toolbar.innerHTML =
      '<label>Поиск: <input type="search" class="js-table-search"></label> ' +
      '<label>Сортировка: <select class="js-table-sort">' +
      '<option value="">—</option>' +
      '<option value="0-asc">Кол.1 ↑</option><option value="0-desc">Кол.1 ↓</option>' +
      '<option value="1-asc">Кол.2 ↑</option><option value="1-desc">Кол.2 ↓</option>' +
      '<option value="2-asc">Кол.3 ↑</option><option value="2-desc">Кол.3 ↓</option>' +
      '<option value="3-asc">Кол.4 ↑</option><option value="3-desc">Кол.4 ↓</option>' +
      "</select></label>";
    table.parentNode.insertBefore(toolbar, table);

    const searchInput = toolbar.querySelector(".js-table-search");
    const sortSelect = toolbar.querySelector(".js-table-sort");

    function cellKey(row, col) {
      const cell = row.cells[col];
      if (!cell) return "";
      return (cell.dataset.sort || cell.textContent || "").trim().toLowerCase();
    }

    function render() {
      const q = (searchInput.value || "").trim().toLowerCase();
      let rows = allRows.slice();
      if (q) {
        rows = rows.filter((r) => r.textContent.toLowerCase().includes(q));
      }
      const sortVal = sortSelect.value;
      if (sortVal) {
        const [col, dir] = sortVal.split("-");
        const c = parseInt(col, 10);
        rows.sort((a, b) => {
          const av = cellKey(a, c);
          const bv = cellKey(b, c);
          if (av < bv) return dir === "asc" ? -1 : 1;
          if (av > bv) return dir === "asc" ? 1 : -1;
          return 0;
        });
      }
      tbody.innerHTML = "";
      rows.forEach((r) => tbody.appendChild(r));
    }

    searchInput.addEventListener("input", render);
    sortSelect.addEventListener("change", render);
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("table.js-filter-table").forEach(initTable);
  });
})();
