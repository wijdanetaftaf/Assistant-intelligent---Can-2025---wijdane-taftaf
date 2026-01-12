function sendMessage() {
    const input = document.getElementById("userInput");
    const chatBox = document.getElementById("chatBox");

    if (input.value.trim() === "") return;

    // Message utilisateur
    const userMsg = document.createElement("div");
    userMsg.className = "chat-user";
    userMsg.innerText = "Vous : " + input.value;
    chatBox.appendChild(userMsg);

    // Réponse bot (temporaire)
    const botMsg = document.createElement("div");
    botMsg.className = "chat-bot";
    botMsg.innerText = "Assistant : Analyse en cours...";
    chatBox.appendChild(botMsg);

    // ICI -> appel API FastAPI plus tard
    setTimeout(() => {
        botMsg.innerText = "Assistant : Réponse générée depuis l’API CAN 2025";
    }, 1000);

    input.value = "";
}
