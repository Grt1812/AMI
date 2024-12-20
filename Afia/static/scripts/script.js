// Gestion de la sidebar (responsive avec bouton hamburger)
document.addEventListener("DOMContentLoaded", () => {
  const menuToggle = document.querySelector(".menu-toggle");
  const sidebar = document.querySelector(".sidebar");

  // Vérifier si les éléments existent avant d'ajouter les événements
  if (menuToggle && sidebar) {
    menuToggle.addEventListener("click", () => {
      sidebar.classList.toggle("open"); // Toggle de la classe "open"
    });

    // Masquer la sidebar si l'utilisateur clique en dehors (mode mobile)
    document.addEventListener("click", (event) => {
      if (!sidebar.contains(event.target) && !menuToggle.contains(event.target)) {
        sidebar.classList.remove("open");
      }
    });
  }
});

// Afficher l'image uploadée
function previewImage(event) {
  const input = event.target;
  const preview = document.getElementById("profile-pic-preview");

  if (input.files && input.files[0]) {
    const reader = new FileReader();

    reader.onload = () => {
      preview.src = reader.result;
      preview.style.display = "block";
    };

    reader.readAsDataURL(input.files[0]);
  } else {
    preview.src = "";
    preview.style.display = "none";
  }
}

// Contrôle des limites pour la date de naissance (max = aujourd'hui, min = -200 ans)
document.addEventListener("DOMContentLoaded", () => {
  const dobInput = document.getElementById("dob");

  if (dobInput) {
    const today = new Date();
    const maxDate = today.toISOString().split("T")[0];
    const minDate = new Date(today.setFullYear(today.getFullYear() - 200)).toISOString().split("T")[0];

    dobInput.setAttribute("max", maxDate);
    dobInput.setAttribute("min", minDate);
  }
});

// Fonction pour envoyer un message dans la boîte de chat
function sendMessage() {
  const chatBox = document.getElementById("chat-box");
  const messageInput = document.getElementById("message-input");
  const messageText = messageInput.value.trim();

  if (messageText === "") {
    return; // Ne pas envoyer de message vide
  }

  const newMessage = document.createElement("div");
  newMessage.classList.add("message", isUser1 ? "sent" : "received");

  const profilePic = document.createElement("img");
  profilePic.src = isUser1 ? "user1.jpg" : "user2.jpg";
  profilePic.alt = "Profil";
  profilePic.classList.add("profile-pic");

  const messageContent = document.createElement("span");
  messageContent.textContent = messageText;

  newMessage.appendChild(profilePic);
  newMessage.appendChild(messageContent);

  chatBox.appendChild(newMessage);
  messageInput.value = "";

  // Scroll automatique pour voir le dernier message
  chatBox.scrollTop = chatBox.scrollHeight;

  // Alterne entre les utilisateurs pour simuler une conversation
  isUser1 = !isUser1;
}

// Gestion du mode sombre/clair avec stockage local
document.addEventListener("DOMContentLoaded", () => {
  const modeToggle = document.getElementById("mode-toggle");

  if (modeToggle) {
    const body = document.body;

    // Appliquer le mode en fonction du stockage local
    const isDarkMode = localStorage.getItem("dark-mode") === "true";
    body.classList.toggle("dark-mode", isDarkMode);
    modeToggle.textContent = isDarkMode ? "Mode clair" : "Mode sombre";

    // Écouter les clics pour basculer entre les modes
    modeToggle.addEventListener("click", () => {
      const darkModeEnabled = body.classList.toggle("dark-mode");
      modeToggle.textContent = darkModeEnabled ? "Mode clair" : "Mode sombre";
      localStorage.setItem("dark-mode", darkModeEnabled);
    });
  }
});

// Responsivité : affichage/masquage du menu droit
document.addEventListener("DOMContentLoaded", () => {
  const hamburger = document.getElementById("menu-toggle");
  const menuDroite = document.querySelector(".menu-droite");

  if (hamburger && menuDroite) {
    hamburger.addEventListener("click", () => {
      menuDroite.classList.toggle("active");
      hamburger.classList.toggle("is-open");
    });
  }
});

// Charts.js : gestion des graphiques responsive
document.addEventListener("DOMContentLoaded", () => {
  const casesChartCtx = document.getElementById("casesChart").getContext("2d");
  const pathologiesChartCtx = document.getElementById("pathologiesChart").getContext("2d");

  if (casesChartCtx && pathologiesChartCtx) {
    // Exemple de graphique pour l'évolution des cas
    new Chart(casesChartCtx, {
      type: "line",
      data: {
        labels: ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin"],
        datasets: [
          {
            label: "Cas Critiques",
            data: [30, 40, 25, 50, 60, 45],
            backgroundColor: "rgba(255, 99, 132, 0.2)",
            borderColor: "rgba(255, 99, 132, 1)",
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
      },
    });

    // Exemple de graphique pour la distribution des pathologies
    new Chart(pathologiesChartCtx, {
      type: "doughnut",
      data: {
        labels: ["Hypertension", "Diabète", "Arrêt Cardiaque", "Autres"],
        datasets: [
          {
            label: "Pathologies",
            data: [40, 20, 25, 15],
            backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0"],
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
      },
    });
  }
});
