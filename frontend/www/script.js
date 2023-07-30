document.addEventListener("DOMContentLoaded", function () {
    const messageInput = document.getElementById("message-input");
    const sendButton = document.getElementById("send-button");
    const chatMessages = document.getElementById("chat-messages");
  
    sendButton.addEventListener("click", function () {
      const message = messageInput.value.trim();
      if (message !== "") {
        const newMessageElement = document.createElement("div");
        newMessageElement.classList.add("message");
        newMessageElement.textContent = message;
        chatMessages.appendChild(newMessageElement);
        messageInput.value = "";
        messageInput.focus();
      }
    });
    /*
    messageInput.addEventListener("keydown", function (event) {
      if (event.key === "Enter") {
        sendButton.click();
      }
    });
    */
  });
  