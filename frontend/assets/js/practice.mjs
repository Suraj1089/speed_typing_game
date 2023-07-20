// get elements from DOM
const startBtn = document.getElementById("startBtn");
const resetBtn = document.getElementById("resetBtn");
const userInput = document.getElementById("userInput");
const messageEle = document.getElementById("message");
const speedEle = document.getElementById("speed");
const quoteEle = document.getElementById("quote");
const greetEle = document.getElementById("greetUser");
const levelSelector = document.getElementById("levelSelector");
const easyLvlBtn = document.getElementById("easyLvlBtn");
const interLvlBtn = document.getElementById("interLvlBtn");
const hardLvlBtn = document.getElementById("hardLvlBtn");
const userHeader = document.getElementById("user-header");
const onemin = document.getElementById("onemin");
const twomin = document.getElementById("twomin");
const fivemin = document.getElementById("fivemin");
const startBtn2 = document.getElementById("startBtn2");
// import functions
import { makeSentence } from './sentence.mjs'

// get elements from DOM
const nameModalEle = document.querySelector(".nameModal");
const startInstruction = document.querySelector(".startIns")

// hiding elements in DOM
levelSelector.style.display = 'none';
timingSessionChoose.style.display = 'none';
nameModalEle.style.display = 'none';
userInputBox.style.display = 'none';
messages.style.display = 'none';
resetBtn.style.display = 'none';
startBtn.style.display = 'none';

// initializing variables
let extracted_words = [];
let words = "";
let timeout = false
let wordIndex = 0, extracted_words_length = 0, quoteLength = 0;
let startTime = Date.now();
let selectedDifficultyLevel = "";
let selectedTime = 0;
let char_you_typed = 0
let characters;

startBtn2.addEventListener("click", () => {
    // getting quote and time
    const quote = makequote()
    
    // get time choosed by user and convert it into milliseconds
    const time = getTime() * 60 * 1000;

    // splitting quote into words
    extracted_words = quote.split(' ');
    extracted_words_length = extracted_words.length;
    wordIndex = 0;
    
    // hiding and showing elements in DOM
    userHeader.style.display = "none";
    levelSelector.style.display = 'none';
    userInputBox.style.display = 'block';
    userInput.style.display = 'inline';
    startBtn.style.display = 'none';
    timingSessionChoose.style.display = "none";
    resetBtn.style.display = 'inline-block';

    // making the quote in span tags
    const spanWords = extracted_words.map(word => {
        return `<span>${word} </span>`;
    });

    // setting up the quote in DOM
    quoteEle.innerHTML = spanWords.join('');
    quoteEle.childNodes[0].className = 'highlight';
    userInput.innerText = '';
    userInput.focus();


    // create a div and add this html to it
    const speedResultCalc = document.createElement("div");
    speedResultCalc.classList.add("speedResultCalc");
    speedResultCalc.style.textAlign = "center";
    speedResultCalc.style.backgroundColor = "#f1f1f1";
    speedResultCalc.style.border = "1px solid #ccc";
    speedResultCalc.style.borderRadius = "4px";
    speedResultCalc.style.padding = "10px";

    speedResultCalc.innerHTML = `
    <ul class="result-details" style="list-style: none; padding: 0; margin: 0;">
        <li class="time" style="display: inline-block; margin: 5px;">
            <p style="font-size: 14px; margin: 0; color: #333;">Time Left:</p>
            <span style="font-size: 16px; font-weight: bold;"><b>60</b>s</span>
        </li>
        <li class="mistake" style="display: inline-block; margin: 5px;">
            <p style="font-size: 14px; margin: 0; color: #333;">Mistakes:</p>
            <span style="font-size: 16px; font-weight: bold;">0</span>
        </li>
        <li class="wpm" style="display: inline-block; margin: 5px;">
            <p style="font-size: 14px; margin: 0; color: #333;">WPM:</p>
            <span style="font-size: 16px; font-weight: bold;">0</span>
        </li>
        <li class="cpm" style="display: inline-block; margin: 5px;">
            <p style="font-size: 14px; margin: 0; color: #333;">CPM:</p>
            <span style="font-size: 16px; font-weight: bold;">0</span>
        </li>
    </ul>
    `;
    // append the div to the body
    resetBtn.insertAdjacentElement("afterend", speedResultCalc);


    // setting up the timer
    startTime = new Date().getTime();
    startTimer(time);
});

const getwpm = () => {
    // access history from local storage
    history = localStorage.getItem("typerHistory");
    if (history != null) {
        // parse history into array
        historyArray = JSON.parse(history);
        // initialize variables
        let highestSpeed = 0;
        let speed = 0;
        // loop through history array to find highest speed
        historyArray.forEach((item) => {
            speed =  Math.ceil((item.char / 5) / (item.timeSession));
            // if speed is higher than highest speed, set it as highest speed
            if (speed > highestSpeed) {
                highestSpeed = speed;
            }
        });
        return highestSpeed;
    } else {
        // if user has no history, return 0
        return 0;
        
    }
};


// making the quote from the words
const makequote = () => {

    // get highest wpm of user
    let wpm = getwpm();

    // get time choosed by user
    const time = getTime();

    // if user has no history ie. new user
    if (wpm == 0) {
        // setting up default difficulty level for new user
        if (easyLvlBtn.checked) {
            selectedDifficultyLevel = "easy";
            quoteLength = 70 * time
        } else if (interLvlBtn.checked) {
            selectedDifficultyLevel = "medium";
            quoteLength = 55 * time
        } else if (hardLvlBtn.checked) {
            selectedDifficultyLevel = "hard";
            quoteLength = 40 * time
        }
    }
    else {
        // setting up difficulty level according to user's wpm
        if (easyLvlBtn.checked) {
            selectedDifficultyLevel = "easy";
            quoteLength = (wpm + 8) * time 
        } else if (interLvlBtn.checked) {
            selectedDifficultyLevel = "medium";
            quoteLength = (wpm + 4) * time
        } else if (hardLvlBtn.checked) {
            selectedDifficultyLevel = "hard";
            quoteLength = (wpm + 2) * time
        }
    }
    return makeSentence(selectedDifficultyLevel,quoteLength);
};

// getting time choosed by user
const getTime = () => {
    if (onemin.checked){
        selectedTime = 1
        return selectedTime;
    }
    else if (twomin.checked){
        selectedTime = 2
        return selectedTime;
    }
    else if (fivemin.checked){
        selectedTime = 5
        return selectedTime;
    }
};

// flag after time goes off
const startTimer = (time) => {
    setTimeout(() => {
        timeout = true
        completedSession();
    }, time);
}

// start the typing game
startBtn.addEventListener("click", () => {
    // getting quote and time
    // return to the practice/typing page
    return window.location.href = "/practice/typing";
});

// function to call when the session is completed 
// either by writting all words or time goes off
const completedSession = () => {
    // calculating speed
    const timeTaken = ((new Date().getTime() - startTime) / 1000).toFixed(2); // in seconds
    const speed_word_pm = Math.ceil((char_you_typed / 5) / (timeTaken / 60)); // formula taken from google
    const message = `Congratulations! You have typed in ${timeTaken} seconds`;
    const speedMessage = `Your speed is ${speed_word_pm} words per minutes`;

    // display results
    messages.style.display = 'inline';
    messageEle.innerText = message;
    speedEle.innerText = speedMessage;
    userInput.style.display = 'none';
    saveHistory();
}


// Reset the typing game
resetBtn.addEventListener("click", () => {
    // hiding and showing elements in DOM
    levelSelector.style.display = 'block';
    startBtn.style.display = 'block';
    timingSessionChoose.style.display = "flex";
    userHeader.style.display = "block"

    // resetting variables
    quoteEle.innerText = "";
    timeout = false;
    words = "";
    userInput.value = '';

    // hiding elements
    resetBtn.style.display = 'none';
    userInput.style.display = 'none';
    userInputBox.style.display = 'none';
    messages.style.display = 'none';
})

// Popup to ask for Name of user 
// if not entered before & display name from local Storage

const nameInput = document.getElementById("userName");
const nameSubmitBtn = document.getElementById("nameSubmitBtn");

// getting and setting username in localStorage
const getAndSetUserName = () => {
    const name = localStorage.getItem("typerName");
    if (name) {
        // greet user
        greetEle.innerText = `Hello, ${name}!`;
        levelSelector.style.display = "block";
        timingSessionChoose.style.display = "flex";
    }
    else {
        nameModalEle.style.display = "block";
    }
};

// Function to save username to localStorage
nameSubmitBtn.addEventListener("click", () => {
    console.log(nameInput.value);
    if (nameInput.value != null && nameInput.value != "") {
        localStorage.setItem("typerName", nameInput.value);
        nameModalEle.style.display = "none";
        getAndSetUserName();
    }
    else {
        console.log("Enter Username");
    }
})

// Listen for timer select
document.getElementById("timingSessionChoose").addEventListener("click", (e) => {
    if (e.target.name === "time-button" && (easyLvlBtn.checked || interLvlBtn.checked || hardLvlBtn.checked)) {
        startBtn.style.display = 'block';
        // startInstruction.style.display = 'block'
    }
})

// listen for level select
document.getElementById("levelSelector").addEventListener("click", (e) => {
    if (e.target.name === "radio-button" && (onemin.checked || twomin.checked || fivemin.checked)) {
        startBtn.style.display = 'block';
        startInstruction.style.display = 'block'
    }
})

// // function to start typing session after pressing space key 
// document.addEventListener('keypress', (e) => {
//     if (e.code === "Space") {
//         if (startBtn.style.display !== "none")
//             startBtn.click();
//         else if (userInput.style.display === "none")
//             resetBtn.click();
//     }
// })

// function to automatically click on submit button with Enter key
nameInput.addEventListener('keypress', (e) => {
    if (e.code === "Enter")
        nameSubmitBtn.click()
})

getAndSetUserName();

let history = [];
let historyArray = [];

// Saving History of typing sessions to localStorage
const saveHistory = () => {
    history = localStorage.getItem("typerHistory");
    // check if history is already present
    // if yes then parse the history and push the new session
    // else create a new history
    if (history) {
        // parse the history and push the new session
        historyArray = JSON.parse(history);
        historyArray.push({ char:char_you_typed, difficultyLevel: selectedDifficultyLevel, timeSession: selectedTime });
        localStorage.setItem("typerHistory", JSON.stringify(historyArray));
    }
    else {
        localStorage.setItem("typerHistory", JSON.stringify([{ char:char_you_typed, difficultyLevel: selectedDifficultyLevel, timeSession: selectedTime }]));
    }
}
