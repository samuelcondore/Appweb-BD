const table = document.getElementById("search_results");

const institucion = document.getElementById("nivel");
institucion.addEventListener("change", async (e) => {
    e.preventDefault();
    const i = e.target.value;
    renderQueryResult(i);
})

async function fetchQueryResults(i) {
    const body = {
        nivel: i
    }
    try {
        const response = await fetch('/carreras_caras', {
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

async function renderQueryResult(i) {
    if (i == "") {
        table.innerHTML = "<tr><td style=\"text-align: center;\" colspan=\"3\" >Seleccione un nivel de carrera</td></tr>";
        return;
    }
    const queryResult = await fetchQueryResults(i);
    if (queryResult.result === undefined || queryResult.result.length === 0){
        table.innerHTML = "<tr><td style=\"text-align: center;\" colspan=\"3\" >Seleccione un nivel de carrera</td></tr>";
    } else {
        const abs_total = Number(queryResult.abs_total);
        let tablecontents = queryResult.result.map(c => {
            return `<tr><td>${c.nomb_carrera}</td><td>${c.institucion}</td><td>$${c.arancel_promedio}%</td></tr>`;
        }).join("");
        table.innerHTML = tablecontents;
    }
}
