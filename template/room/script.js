let currentFriend = '';

function selectFriend(friendName) {
    currentFriend = friendName;
    document.getElementById('chat-header').innerText = `Chat with ${currentFriend}`;
    document.getElementById('messages').innerHTML = ''; // Clear previous messages
}

function sendMessage() {
    const messageInput = document.getElementById('message-input');
    const messageText = messageInput.value;

    if (messageText && currentFriend) {
        const messageDiv = document.createElement('div');
        messageDiv.textContent = `${currentFriend}: ${messageText}`;
        document.getElementById('messages').appendChild(messageDiv);
        messageInput.value = ''; // Clear input after sending
    } else {
        alert('Please select a friend and type a message!');
    }
}