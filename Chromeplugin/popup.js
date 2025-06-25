document.addEventListener("DOMContentLoaded", function () {
  const askBtn = document.getElementById("askBtn");
  const questionInput = document.getElementById("question");
  const chatWindow = document.getElementById("chatWindow");
  const videoIdDisplay = document.getElementById("videoIdDisplay");

  // Auto-expand textarea
  questionInput.addEventListener("input", function () {
    this.style.height = "auto";
    this.style.height = this.scrollHeight + "px";
  });

  // Dark mode toggle (syncs with popup.html)
  const toggle = document.querySelector(".toggle-theme");
  if (toggle) {
    toggle.addEventListener("click", () => {
      document.body.classList.toggle("dark-mode");
    });
  }

  // Get YouTube video ID from current tab
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    const url = tabs[0]?.url || "";
    const videoId = extractYouTubeVideoId(url);
    if (videoId) {
      videoIdDisplay.textContent = `Video ID: ${videoId}`;
      window.currentVideoId = videoId;
    } else {
      videoIdDisplay.textContent = "Not a YouTube video.";
      window.currentVideoId = null;
    }
  });

  askBtn.addEventListener("click", async function () {
    const question = questionInput.value.trim();
    const videoId = window.currentVideoId;

    if (!videoId) {
      addMessage("Please open a YouTube video first.", "bot");
      return;
    }

    if (!question) {
      addMessage("Please enter a question.", "bot");
      return;
    }

    addMessage(question, "user");
    questionInput.value = "";

    const thinkingBubble = addMessage("...", "bot");
    animateThinking(thinkingBubble);

    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: "user1",
          video_id: videoId,
          question: question
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        thinkingBubble.textContent = `Error: ${errorData.detail}`;
        return;
      }

      const data = await response.json();
      thinkingBubble.textContent = data.answer;
    } catch (err) {
      thinkingBubble.textContent = "Something went wrong. Please check the backend.";
      console.error(err);
    }
  });

  function addMessage(text, sender) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", sender === "user" ? "user-message" : "bot-message");

    const bubble = document.createElement("div");
    bubble.classList.add("chat-box", sender === "user" ? "user-box" : "bot-box");
    bubble.textContent = text;

    messageDiv.appendChild(bubble);
    chatWindow.appendChild(messageDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;

    return bubble;
  }

  function extractYouTubeVideoId(url) {
    const regex = /(?:youtube\.com\/watch\?v=|youtu\.be\/)([^\s&]+)/;
    const match = url.match(regex);
    return match ? match[1] : null;
  }

  function animateThinking(bubble) {
    let dots = 0;
    const interval = setInterval(() => {
      if (!bubble.isConnected) return clearInterval(interval);
      dots = (dots + 1) % 4;
      bubble.textContent = "Thinking" + ".".repeat(dots);
    }, 500);
  }
});
