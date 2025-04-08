async function uploadFile() {
    const fileInput = document.getElementById('csvFile');
    const file = fileInput.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    const res = await fetch('/upload', {
        method: 'POST',
        body: formData
    });

    const data = await res.json();
    showMessage("You", "File uploaded successfully.");
    showMessage("Bot", data.message || "File processed.");
}

async function askChatbot() {
    const question = document.getElementById('question').value;
    if (!question.trim()) return;

    showMessage("You", question);
    document.getElementById('question').value = "";

    const res = await fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question })
    });

    const data = await res.json();
    showMessage("Bot", data.response);
}

function showMessage(sender, text) {
    const chatbox = document.getElementById('chatbox');
    const msgDiv = document.createElement('div');
    msgDiv.className = 'message ' + (sender === "You" ? 'user' : 'bot');
    msgDiv.innerHTML = `<strong>${sender}:</strong> ${text}`;
    chatbox.appendChild(msgDiv);
    chatbox.scrollTop = chatbox.scrollHeight;
}
