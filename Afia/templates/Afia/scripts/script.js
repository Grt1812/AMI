// Affiche l'image uploadée
function previewImage(event) {
  const input = event.target;
  const preview = document.getElementById('profile-pic-preview');

  if (input.files && input.files[0]) {
    const reader = new FileReader();

    reader.onload = function() {
      preview.src = reader.result;
      preview.style.display = 'block';
    };

    reader.readAsDataURL(input.files[0]);
  } else {
    preview.src = '';
    preview.style.display = 'none';
  }
}

// Contrôle de la date de naissance : max = aujourd'hui et min = aujourd'hui - 200 ans
document.addEventListener('DOMContentLoaded', () => {
  const dobInput = document.getElementById('dob');
  const today = new Date();
  const maxDate = today.toISOString().split('T')[0];
  const minDate = new Date(today.setFullYear(today.getFullYear() - 200)).toISOString().split('T')[0];

  dobInput.setAttribute('max', maxDate);
  dobInput.setAttribute('min', minDate);
});

// Chat
let isUser1 = true;

function goBack() {
  window.history.back();
}

function sendMessage() {
  const chatBox = document.getElementById('chat-box');
  const messageInput = document.getElementById('message-input');
  const messageText = messageInput.value.trim();

  if (messageText === '') {
    return; // Ne pas envoyer de message vide
  }

  // Crée un nouveau div pour le message envoyé
  const newMessage = document.createElement('div');
  newMessage.classList.add('message', isUser1 ? 'sent' : 'received');

  const profilePic = document.createElement('img');
  profilePic.src = isUser1 ? 'user1.jpg' : 'user2.jpg';
  profilePic.alt = 'Profil';
  profilePic.classList.add('profile-pic');

  const messageContent = document.createElement('span');
  messageContent.textContent = messageText;

  newMessage.appendChild(profilePic);
  newMessage.appendChild(messageContent);

  // Ajoute le nouveau message à la boîte de chat
  chatBox.appendChild(newMessage);

  // Efface le champ de saisie
  messageInput.value = '';

  // Défile la boîte de chat vers le bas pour voir le nouveau message
  chatBox.scrollTop = chatBox.scrollHeight;

  // Change de user pour le prochain message
  isUser1 = !isUser1;
}

// Vérifie le stockage local pour l'état du mode sombre
document.addEventListener('DOMContentLoaded', () => {
  const modeToggle = document.getElementById('mode-toggle');
  const body = document.body;

  if (localStorage.getItem('dark-mode') === 'true') {
    body.classList.add('dark-mode');
    modeToggle.textContent = 'Mode sombre';
  } else {
    body.classList.remove('dark-mode');
    modeToggle.textContent = 'Mode clair';
  }
});

// Bascule le mode sombre/clair
const modeToggle = document.getElementById('mode-toggle');
modeToggle.addEventListener('click', () => {
  document.body.classList.toggle('dark-mode');

  if (document.body.classList.contains('dark-mode')) {
    modeToggle.textContent = 'Mode sombre';
    localStorage.setItem('dark-mode', 'true');
  } else {
    modeToggle.textContent = 'Mode clair';
    localStorage.setItem('dark-mode', 'false');
  }
});

// Affichage/masquage du menu
const hamburger = document.getElementById('menu-toggle');
const menuDroite = document.querySelector('.menu-droite');

hamburger.addEventListener('click', () => {
  menuDroite.classList.toggle('active');
  hamburger.classList.toggle('is-open');
});