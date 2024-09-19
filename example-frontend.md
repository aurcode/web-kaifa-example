### Example JavaScript Code

#### HTML Structure (Optional)

You might want to include a simple HTML structure for a better understanding of how to integrate the JavaScript code. Here’s a basic example:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Score Tracker</title>
</head>
<body>
    <h1>Score Tracker</h1>
    <form id="scoreForm">
        <input type="text" id="username" placeholder="Username" required />
        <input type="number" id="score" placeholder="Score" required />
        <button type="submit">Submit Score</button>
    </form>

    <h2>Scores</h2>
    <ul id="scoresList"></ul>

    <script src="script.js"></script>
</body>
</html>
```

#### JavaScript Code (script.js)

```javascript
document.getElementById('scoreForm').addEventListener('submit', async function (event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const score = parseFloat(document.getElementById('score').value);

    // Submit Score
    try {
        const response = await fetch('http://localhost:5000/submit_score', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, score }),
        });

        if (!response.ok) {
            throw new Error('Failed to submit score: ' + response.statusText);
        }

        const data = await response.json();
        console.log('Score submitted:', data);
        alert('Score submitted successfully!');

        // Clear input fields
        document.getElementById('username').value = '';
        document.getElementById('score').value = '';

        // Fetch scores after submission
        fetchScores();
    } catch (error) {
        console.error('Error:', error);
        alert('Error submitting score: ' + error.message);
    }
});

// Function to fetch and display scores
async function fetchScores() {
    try {
        const response = await fetch('http://localhost:5000/scores');
        if (!response.ok) {
            throw new Error('Failed to fetch scores: ' + response.statusText);
        }

        const scores = await response.json();
        const scoresList = document.getElementById('scoresList');
        scoresList.innerHTML = ''; // Clear the list before adding new scores

        scores.forEach(score => {
            const li = document.createElement('li');
            li.textContent = `${score.username}: ${score.score}`;
            scoresList.appendChild(li);
        });
    } catch (error) {
        console.error('Error:', error);
        alert('Error fetching scores: ' + error.message);
    }
}

// Fetch scores on initial load
fetchScores();
```

### How It Works

1. **HTML Form**: The form collects a username and score, and submits it when the user clicks the "Submit Score" button.

2. **JavaScript Code**:
   - The form submission is handled by adding an event listener.
   - When the form is submitted, it prevents the default behavior, collects the input values, and sends a `POST` request to the `/submit_score` endpoint with the score data.
   - If the score submission is successful, it alerts the user and calls the `fetchScores` function to update the displayed scores.
   - The `fetchScores` function sends a `GET` request to the `/scores` endpoint and updates the list of scores displayed on the page.

### Running the Example

1. Make sure your Flask application is running on `http://localhost:5000`.
2. Open the HTML file in a web browser.
3. Enter a username and score, then submit the form to see the scores update.

Feel free to customize the UI and add any additional features as needed! If you have any further questions or need assistance, let me know!