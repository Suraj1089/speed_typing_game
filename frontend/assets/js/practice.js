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
const tenmin = document.getElementById("tenmin");
const tmin = document.getElementById("tmin");
const xitymin = document.getElementById("xitymin");
const infinit = document.getElementById("infinit");
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



function getDiffLevel() {
    if (easyLvlBtn.checked) {
        selectedDifficultyLevel = "Easy";
    } else if (interLvlBtn.checked) {
        selectedDifficultyLevel = "Medium";
    } else if (hardLvlBtn.checked) {
        selectedDifficultyLevel = "Hard";
    }
    console.log(selectedDifficultyLevel);
    return selectedDifficultyLevel;
}


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
    else if (tenmin.checked){
        selectedTime = 10
        return selectedTime;
    }
    else if (tmin.checked){
        selectedTime = 30
        return selectedTime;
    }
    else if (xitymin.checked){
        selectedTime = 60
        return selectedTime;
    }
    // check infinit input text is not empty
    else if (infinit.value != null && infinit.value != ""){
        selectedTime = infinit.value
        return selectedTime;
    }
    else{
        return 0;
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
    const typingTime = getTime();
    const difficultyLevel = getDiffLevel();
    console.log(typingTime, difficultyLevel);
    window.location.href = `/practice/typing?time=${typingTime}&difficulty=${difficultyLevel}`;
});



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
        levelSelector.style.display = "block";
        timingSessionChoose.style.display = "flex";
        // nameModalEle.style.display = "block";
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
    if (e.target.name === "radio-button" && (onemin.checked || twomin.checked || fivemin.checked || tenmin.checked || tmin.checked || xitymin.checked || infinit.value != null && infinit.value != "")) {
        startBtn.style.display = 'block';
        // startInstruction.style.display = 'block'
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