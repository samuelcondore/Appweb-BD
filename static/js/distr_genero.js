window.mypage = 0;
const table = document.getElementById("search_results");

const institucion = document.getElementById("institucion");
institucion.addEventListener("change", async (e) => {
    e.preventDefault();
    const i = e.target.value;
    renderQueryResult(i);
})

async function fetchQueryResults(i) {
    const body = {
        institucion: i
    }
    try {
        const response = await fetch('/distr_genero', {
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
        table.innerHTML = "<tr><td style=\"text-align: center;\" colspan=\"3\" >Seleccione un tipo de institución</td></tr>";
        return;
    }
    const queryResult = await fetchQueryResults(i);
    if (queryResult.result === undefined || queryResult.result.length === 0){
        table.innerHTML = "<tr><td style=\"text-align: center;\" colspan=\"3\" >Seleccione un tipo de institución</td></tr>";
    } else {
        const abs_total = Number(queryResult.abs_total);
        let tablecontents = queryResult.result.map(c => {
            return `<tr><td>${c.genero}</td><td>${c.total}</td><td>${(c.total/abs_total*100).toFixed(2)}%</td></tr>`;
        }).join("");
        table.innerHTML = tablecontents;
    }
}
