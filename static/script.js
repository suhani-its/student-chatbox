document.getElementById("send-btn").addEventListener("click", function() {
    let userMessage = document.getElementById("user-input").value;
    if (userMessage === "") return;

    // User ka message show karo
    document.getElementById("chatbox").innerHTML += "<p><b>You:</b> " + userMessage + "</p>";
    document.getElementById("user-input").value = "";

    // Server ko bhejo
    fetch("/get", {
        method: "POST",
        body: new FormData(document.getElementById("chat-form"))
    })
    .then(response => response.json())
    .then(data => {
        // Bot ka reply show karo
        document.getElementById("chatbox").innerHTML += "<p><b>Bot:</b> " + data.reply + "</p>";
    });
});