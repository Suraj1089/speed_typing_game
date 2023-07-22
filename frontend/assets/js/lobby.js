$(document).ready(function() {
    var usersInLobby = null;
    var lobby_id = getLobbyIdFromURL();
    var socket = new WebSocket("ws://localhost:8000/sio");
  
    // Function to get lobby_id from URL query parameters
    function getLobbyIdFromURL() {
      var url = new URL(window.location.href);
      return url.searchParams.get("lobby_id");
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
    socket.onopen = function(e) {
      // Fetch the list of players in the lobby
      $.ajax({
        type: "GET",
        url: `http://localhost:8000/getplayers?lobby_id=${lobby_id}`,
        dataType: "json",
        success: function(data) {
          usersInLobby = data.players;
          console.log(usersInLobby);

          // get players count from server at http://localhost:8000
            $.ajax({
                type: "GET",
                url: `http://localhost:8000/getlobby?lobby_id=${lobby_id}`,
                dataType: "json",
                success: function(data) {
                    console.log('playes dta')
                    console.log(data);
                    var players = data.players;
                   
                    if (usersInLobby.length >= players) {
                        console.log("Game Started");
                        // get game status 
                        $.ajax({
                            type: "GET",
                            url: `http://localhost:8000/gamestatus?lobby_id=${lobby_id}&time=${data.time}`,
                            dataType: "json",
                            success: function (data) {
                                alert('Game already Started');
                                startTimer(data.time);
                            }, 
                            error: function (error) {
                                console.log('error');
                            }
                        })
                    } else {
                        alert(`Waiting for required ${players} in lobby: ${usersInLobby.length}`);
                    }
                },
                error: function(error) {
                    console.error('Error getting players data:', error);
                }
            });
  
          // Add existing users to the user_component div
          usersInLobby.forEach(user => {
            addUserToComponent(user);
          });
        },
        error: function(error) {
          console.error('Error getting players data:', error);
        }
      });

    };
  
    // WebSocket onmessage event (Handle real-time updates)
    socket.onmessage = function(event) {
      var messageData = JSON.parse(event.data);
  
      // Handle different message types from the server
      switch (messageData.type) {
        case "user_joined":
          // A new user joined the lobby
          var newUser = messageData.user;
          addUserToComponent(newUser);
          break;
        case "user_left":
          // A user left the lobby
          var userId = messageData.userId;
          removeUserFromComponent(userId);
          break;
        // Add more cases as needed for other message types
        default:
          console.log("Unknown message type:", messageData.type);
          break;
      }
    };
  });
  