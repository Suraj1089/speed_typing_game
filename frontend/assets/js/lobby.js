$(document).ready(function () {
  
  var usersInLobby = []; // Array to store the list of users in the lobby
  var lobby_id = getLobbyIdFromURL();
  var username = getUserNameFromUrl();
  
  // var socket = new WebSocket(`ws://localhost:8000/ws/?${username}`);
  var socket = new WebSocket(`ws://localhost:8000/ws/${username}`);

  // Function to get lobby_id from URL query parameters
  function getLobbyIdFromURL() {
    var url = new URL(window.location.href);
    return url.searchParams.get("lobby_id");
  }
  function getUserNameFromUrl() {
    var url = new URL(window.location.href);
    return url.searchParams.get("username");
  }

  // Function to add a new user to the user_component div
  function addUserToComponent(user) {
    var userDiv = document.createElement("div");
    userDiv.className = "user";
    userDiv.id = user.id; // Use a unique ID for each user element
    userDiv.innerHTML = `<b> Username: ${user.name} &nbsp &nbsp &nbsp &nbsp  WPM: ${user.wpm} </b>`;
    document.querySelector(".user_component").appendChild(userDiv);
  }

  // Function to remove a user from the user_component div
  function removeUserFromComponent(userId) {
    var userDiv = document.getElementById(userId);
    if (userDiv) {
      userDiv.remove();
    }

  }

  function startTimer(minutes) {
    var timerElement = document.getElementById("time-left");

    var totalSeconds = minutes * 60;

    function updateTimer() {
      timerElement.textContent = totalSeconds;

      if (totalSeconds <= 0) {
        clearInterval(timer);
        alert("Time's up!");
      } else {
        totalSeconds--;
      }
    }

    updateTimer(); // Update the timer immediately before waiting for 1 second.

    var timer = setInterval(updateTimer, 1000); // Update the timer every 1 second (1000 ms).
  }

 
  // WebSocket onopen event
  socket.onopen = function (e) {
    // Fetch the list of players in the lobby
    $.ajax({
      type: "GET",
      url: `http://localhost:8000/getplayers?lobby_id=${lobby_id}`,
      dataType: "json",
      success: function (data) {
        usersInLobby = data.players;
        usersInLobby.forEach((user) => {
          addUserToComponent(user);
        })
      },
      error: function (error) {
        console.log(error);
      },
    });
    socket.send(JSON.stringify({ action: "join", lobby_id: lobby_id, username: username }));
  }


  socket.onmessage = event => {
    const data = JSON.parse(event.data);
    console.log('socket data ', data);
    console.log('type of data ', typeof data);
    usersInLobby.push({username: data.username, wpm: 0});
};
});
