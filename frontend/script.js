
async function loadResults(documentId) {

    const response = await fetch(
        `http://127.0.0.1:8000/results/${documentId}`
    );

    const data = await response.json();

    const container = document.getElementById("results");

    container.innerHTML = "";

    data.forEach(item => {

        container.innerHTML += `

        <div class="card">

            <h2>Requirement</h2>

            <p>${item.requirement}</p>

            <h3>Issue</h3>

            <p>${item.issue}</p>

            <h3>Suggestion</h3>

            <p>${item.suggestion}</p>

            <h3>Confidence</h3>

            <p>${item.confidence}</p>

        </div>

        `;

    });

}

// Replace with your latest document id
loadResults("8cef78ee-cfdd-47e9-81e1-4da3b36b0a2f");