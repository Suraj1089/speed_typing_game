let textToType = '';
let startTime = 0;
let timer = null;

function generateRandomText(difficulty) {
    // Add text snippets for different difficulty levels (you can modify this)
    const easyTexts = ['Type this easy text.', 'Try this simple sentence.', 'Practice typing with this text.'];
    const mediumTexts = ['This is a medium difficulty text to type.', 'Improve your speed with this passage.'];
    const hardTexts = ['Challenge yourself with this hard text.', 'Type accurately with this complex sentence.'];

    switch (difficulty) {
        case 'easy':
            return easyTexts[Math.floor(Math.random() * easyTexts.length)];
        case 'medium':
            return mediumTexts[Math.floor(Math.random() * mediumTexts.length)];
        case 'hard':
            return hardTexts[Math.floor(Math.random() * hardTexts.length)];
        default:
            return '';
    }
}

function startGame() {
    const difficulty = document.getElementById('difficulty').value;
    const duration = parseInt(document.getElementById('duration').value, 10);

    textToType = generateRandomText(difficulty);
    document.getElementById('textToType').textContent = textToType;
    document.getElementById('userInput').value = '';
    document.getElementById('userInput').disabled = false;
    document.getElementById('submitButton').disabled = false;
    document.getElementById('resultMessage').textContent = '';

    // Set a timer to end the game after the specified duration
    startTime = Date.now();
    timer = setInterval(checkTimeElapsed, 1000, duration);
}

function checkTimeElapsed(duration) {
    const elapsedSeconds = Math.floor((Date.now() - startTime) / 1000);

    if (elapsedSeconds >= duration) {
        endGame();
    }
}

function endGame() {
    document.getElementById('userInput').disabled = true;
    document.getElementById('submitButton').disabled = true;
    clearInterval(timer);

    // Calculate accuracy and typing speed
    const userTypedText = document.getElementById('userInput').value;
    const accuracy = calculateAccuracy(userTypedText, textToType);
    const typingSpeed = calculateTypingSpeed(userTypedText, startTime, Date.now());

    // Show the results to the player
    document.getElementById('resultMessage').textContent = `Game Over! Accuracy: ${accuracy}%, Typing Speed: ${typingSpeed} CPM`;
}

function calculateAccuracy(userTypedText, originalText) {
    let correctCharacters = 0;
    for (let i = 0; i < Math.min(userTypedText.length, originalText.length); i++) {
        if (userTypedText[i] === originalText[i]) {
            correctCharacters++;
        }
    }
    return ((correctCharacters / originalText.length) * 100).toFixed(2);
}

function calculateTypingSpeed(userTypedText, startTime, endTime) {
    const elapsedTimeInSeconds = (endTime - startTime) / 1000;
    const characterCount = userTypedText.length;
    const typingSpeed = (characterCount / elapsedTimeInSeconds) * 60;
    return typingSpeed.toFixed(2);
}

function submitResult() {
    endGame();
    // Handle the logic for submitting the game result to the backend
    // (e.g., use fetch() to make a POST request to the backend with accuracy and typing speed)
    // Update the page with the results after saving (optional)
}
