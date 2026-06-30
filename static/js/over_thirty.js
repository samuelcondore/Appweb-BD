window.mypage = 0;
const table = document.getElementById("search_results");
const paginators = document.getElementById("paginators");
paginators.addEventListener('click', (e)=>{
    const m = threshold.value;
    
    if (e.target.closest('#next-page')){
        window.mypage += 1;
        renderQueryResult(m);
        return;
    }
    if (e.target.closest('#prev-page')){
        window.mypage -= 1;
        renderQueryResult(m);
        return;
    }
})

const threshold = document.getElementById("threshold");
threshold.addEventListener("change", async (e) => {
    e.preventDefault();
    const m = e.target.value;
    renderQueryResult(m);
})

async function fetchQueryResults(m) {
    const body = {
        min: m,
        page: window.mypage
    }
    try {
        const response = await fetch('/over_thirty', {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(body)
        });
        if (!response.ok) {
            throw new Error("Error de html");
        }
        return response.json();
    } catch (error) {
        console.error('Error al llamar "fetch()"', error);
    }
}

async function renderQueryResult(m) {
    if (m=="") {
        table.innerHTML = "<tr><td style=\"text-align: center;\" colspan=\"3\" >Seleccione un mínimo de alumnos</td></tr>";
        return;
    }
    const queryResult = await fetchQueryResults(query, j, n, m);
    if (queryResult.data === undefined || queryResult.data.length === 0){
        table.innerHTML = "<tr><td style=\"text-align: center;\" colspan=\"3\" >Seleccione un mínimo de alumnos</td></tr>";
    } else {
        let tablecontents = queryResult.data.map(c => {
            return `<tr><td>${c.total_alumnos}</td><td>${c.nomb_i}</td><td>${c.jorn}</td></tr>`;
        }).join("");
        table.innerHTML = tablecontents;
    }
    let page_buttons = "";
    const total_paginas = Number(queryResult.total_paginas);
    const has_prev = window.mypage-1>=0;
    const has_next = window.mypage+1<=total_paginas;
    console.log(total_paginas, window.mypage, has_prev, has_next);
    if (has_prev || has_next){
        page_buttons += " <br>";
        if (has_prev){
        page_buttons += "<a id='prev-page' class='paginator'>previa</a>";
    }
        if (has_next){
            page_buttons += "<a id='next-page' class='paginator'>siguiente</a>";
    }
    paginators.innerHTML = page_buttons;

    } else {
        paginators.innerHTML = "";
    }
}

