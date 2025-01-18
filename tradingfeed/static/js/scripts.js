// Function to create a popup message
function createPopupMessage(message, type = 'info') {
  const popupContainer = document.getElementById('popup-container');
  const popupMessage = document.createElement('div');
  popupMessage.classList.add('popup-message', type);
  popupMessage.innerText = message;

  popupContainer.appendChild(popupMessage);

  setTimeout(() => {
      popupMessage.style.opacity = '0';
      setTimeout(() => {
          popupContainer.removeChild(popupMessage);
      }, 1000); // Ensure the message is removed after the fade-out transition
  }, 10000); // 10 seconds
}

