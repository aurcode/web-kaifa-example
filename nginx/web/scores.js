async function fetchScores() {
    try {
        //const response = await fetch('http://flask-app:5000/scores');
        const response = await fetch('http://127.0.0.1:5000/scores');
        if (!response.ok) {
            throw new Error('Failed to fetch scores: ' + response.statusText);
        }

        const scores = await response.json();
        const scoresTableBody = document.getElementById('scoresTableBody');

        // Clear existing rows
        scoresTableBody.innerHTML = '';

        // Populate the table with scores
        scores.forEach(score => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${score.username}</td>
                <td>${score.score}</td>
            `;
            scoresTableBody.appendChild(row);
        });
    } catch (error) {
        console.error('Error:', error);
        alert('Error fetching scores: ' + error.message);
    }
}

// Call fetchScores when the script loads
fetchScores();
