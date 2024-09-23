async function submitTest() {
    const endTime = new Date();
    const form = document.getElementById('onlineTestForm');
    const formData = new FormData(form);
    
    let score = 0;
    const totalQuestions = 6; // Update this if you add/remove questions

    // Check the answers
    if (formData.get('question1') === 'Free Town') score++;
    if (formData.get('question2') === '600') score++;
    if (formData.get('question3').toLowerCase().includes('photosynthesis')) score++;
    if (formData.get('question4') === 'False') score++; // Correct answer for Q4
    if (formData.get('question5') === 'Mars') score++;
    if (formData.get('question6').toLowerCase() === 'blue whale') score++; // Adjust for expected answer

    // Calculate score as a percentage
    const percentageScore = (score / totalQuestions) * 100; // Score out of 100
    const totalTime = Math.round((endTime - startTime) / 1000); // Time in seconds
    
    // Retrieve the user's name from the form
    const username = formData.get('name');

    // Alert the user with their score and time taken
    alert(`Hello ${username},\nYou scored ${percentageScore.toFixed(2)}/100.\nTime taken: ${totalTime} seconds.`);

    // Submit Score
    try {
        const response = await fetch('http://flask-app:5000/submit_score', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, score: percentageScore }),
        });

        if (!response.ok) {
            throw new Error('Failed to submit score: ' + response.statusText);
        }

        const data = await response.json();
        console.log('Score submitted:', data);
        alert('Score submitted successfully!');
        
    } catch (error) {
        console.error('Error:', error);
    }

    return false; // Prevent actual form submission
}
