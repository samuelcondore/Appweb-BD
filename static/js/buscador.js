window.mypage = 0;
const table = document.getElementById("search_results");
const paginators = document.getElementById("paginators");
paginators.addEventListener('click', (e)=>{
    const j = jornada.value;
    const n = nivel.value;
    const m = modalidad.value;
    const query = searchbar.value;
    
    if (e.target.closest('#next-page')){
        window.mypage += 1;
        renderQueryResult(query, j, n, m);
        return;
    }
    if (e.target.closest('#prev-page')){
        window.mypage -= 1;
        renderQueryResult(query, j, n, m);
        return;
    }
})

const searchbar = document.getElementById("searchbar");
searchbar.addEventListener("input", async (e) => {
    e.preventDefault();
    const query = e.target.value.trim();
    const j = jornada.value;
    const n = nivel.value;
    const m = modalidad.value;
    if (query.length < 3 && j=="" && n=="" && m=="") {
        table.innerHTML = "<tr><td style=\"text-align: center;\" colspan=\"10\" >No hay resultados</td></tr>";
    } else {
        renderQueryResult(query, j, n, m);
    }
})

const modalidad = document.getElementById("modalidad");
modalidad.addEventListener("change", async (e) => {
    e.preventDefault();
    const j = jornada.value;
    const n = nivel.value;
    const m = e.target.value;
    const query = searchbar.value;
    renderQueryResult(query, j, n, m);
})

const nivel = document.getElementById("nivel");
nivel.addEventListener("change", async (e) => {
    e.preventDefault();
    const j = jornada.value;
    const n = e.target.value;
    const m = modalidad.value;
    const query = searchbar.value;
    renderQueryResult(query, j, n, m);
})

const jornada = document.getElementById("jornada");
jornada.addEventListener("change", async (e) => {
    e.preventDefault();
    const j = e.target.value;
    const n = nivel.value;
    const m = modalidad.value;
    const query = searchbar.value;
    renderQueryResult(query, j, n, m);
})

async function fetchQueryResults(query, j, n, m) {
    const body = {
        query: query,
        jornada: j,
        nivel: n,
        modalidad: m,
        page: window.mypage
    }
    try {
        const response = await fetch('/', {
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

async function renderQueryResult(query, j, n, m) {
    if (query.length < 3 && j=="" && n=="" && m=="") {
        table.innerHTML = "<tr><td style=\"text-align: center;\" colspan=\"10\" >No hay resultados</td></tr>";
        return;
    }
    const queryResult = await fetchQueryResults(query, j, n, m);
    if (queryResult.carreras === undefined || queryResult.carreras.length === 0){
        table.innerHTML = "<tr><td style=\"text-align: center;\" colspan=\"10\" >No hay resultados</td></tr>";
    } else {
        const regex = new RegExp(query, "gi");
        let tablecontents = queryResult.carreras.map(c => {
            return `<tr><td>${c.NOMB_CARRERA}</td><td>${c.JORNADA}</td><td>${c.NOMB_S}</td><td>${c.NOMB_I}</td>
            <td>${c.MODALIDAD}</td><td>${c.DUR_TOTAL_CARR}</td><td>${c.NIVEL_CARRERA}</td><td>${c.VALOR_ARANCEL}</td>
            <td>${c.VALOR_MATRICULA}</td><td>${c.FORMATO_VALORES}</td></tr>`;
        }).join("");
        if (query.length>3){
        table.innerHTML = tablecontents.replaceAll(regex, "<mark>$&</mark>");;
        } else {
            table.innerHTML = tablecontents;
        }
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

