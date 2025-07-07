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

  // Dark mode toggle
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

    // Show user message
    addMessage(question, "user");
    questionInput.value = "";

    // Show thinking bubble and start animation
    const thinkingBubble = addMessage("...", "bot");
    const thinkingInterval = animateThinking(thinkingBubble);

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

      const data = await response.json();
      clearInterval(thinkingInterval); // stop animation

      if (!response.ok) {
        thinkingBubble.textContent = `Error: ${data.detail || "Something went wrong."}`;
        return;
      }

      thinkingBubble.textContent = data.answer || "No response.";
    } catch (err) {
      clearInterval(thinkingInterval);
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
    const patterns = [
      /youtube\.com\/watch\?v=([^&\s]+)/,
      /youtu\.be\/([^&\s]+)/,
      /youtube\.com\/shorts\/([^?\s]+)/,
    ];
    for (const pattern of patterns) {
      const match = url.match(pattern);
      if (match) return match[1];
    }
    return null;
  }

  function animateThinking(bubble) {
    let dots = 0;
    const interval = setInterval(() => {
      if (!bubble.isConnected) return clearInterval(interval);
      dots = (dots + 1) % 4;
      bubble.textContent = "Thinking" + ".".repeat(dots);
    }, 500);
    return interval;
  }
});
