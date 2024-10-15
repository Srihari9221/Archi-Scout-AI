// Get references to DOM elements
const messageBox = document.querySelector("#message");
const sendButton = document.querySelector(".send-button");
const messageForm = document.querySelector("#message-form");
const conversationView = document.querySelector(".conversation-view");

// Function to add messages to the chat window
function addMessage(content, sender) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add(sender, "message");

    const identityDiv = document.createElement("div");
    identityDiv.classList.add("identity");

    const userIcon = document.createElement("i");
    userIcon.classList.add("user-icon");
    userIcon.textContent = sender === "user" ? "U" : "G"; // "U" for user, "G" for AI assistant

    identityDiv.appendChild(userIcon);
    messageDiv.appendChild(identityDiv);

    const contentDiv = document.createElement("div");
    contentDiv.classList.add("content");
    const paragraph = document.createElement("p");
    paragraph.textContent = content;
    contentDiv.appendChild(paragraph);

    messageDiv.appendChild(contentDiv);
    conversationView.appendChild(messageDiv);

    // Scroll to the bottom of the conversation view
    conversationView.scrollTop = conversationView.scrollHeight;
}

// Event listener for the send button
sendButton.addEventListener("click", function(event) {
    event.preventDefault(); // Prevent form submission
    const userInput = messageBox.value.trim(); // Get user input and trim whitespace
    if (userInput === "") return; // If input is empty, do nothing

    addMessage(userInput, "user"); // Add user's message to the chat
    messageBox.value = ""; // Clear the input field

    // Send the message to the backend via fetch
    fetch("/get_response/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"), // Include CSRF token
        },
        body: JSON.stringify({ message: userInput }), // Send the user's message
    })
    .then(response => response.json())
    .then(data => {
        addMessage(data.response, "assistant"); // Add assistant's response to the chat
    })
    .catch(error => {
        console.error("Error:", error); // Handle errors
    });
});

// Function to get the CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Handle form submission with Enter key
messageBox.addEventListener("keydown", function(event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault(); // Prevent adding a new line
        sendButton.click(); // Trigger the send button
    }
});

// Adjust the message box height as the user types
messageBox.addEventListener("input", function() {
    messageBox.style.height = "auto"; // Reset the height
    let height = messageBox.scrollHeight + 2; // Calculate the new height based on content
    if (height > 200) {
        height = 200; // Limit the height to 200px
    }
    messageBox.style.height = height + "px"; // Set the new height
});
