const naturalForm = document.getElementById("naturalForm");
const resumeFileInput = document.getElementById("resumeFile");
const recommendBtn = document.getElementById("recommendBtn");
const downloadTxtBtn = document.getElementById("downloadTxtBtn");
const resultBox = document.getElementById("result");
const confidenceChip = document.getElementById("confidenceChip");
const learningResourcesBox = document.getElementById("learningResources");
const ytVideosBox = document.getElementById("ytVideos");
const nextPlanBox = document.getElementById("nextPlan");
const chatToggleBtn = document.getElementById("chatToggleBtn");
const chatWidget = document.getElementById("chatWidget");
const chatMessages = document.getElementById("chatMessages");
const chatForm = document.getElementById("chatForm");
const chatInput = document.getElementById("chatInput");
const chatSendBtn = document.getElementById("chatSendBtn");

let typingTimer = null;
let latestResponseText = "";
let chatOpen = false;

function setLoading(message) {
  if (!resultBox) {
    return;
  }
  latestResponseText = "";
  updateDownloadAvailability();
  stopTyping();
  resultBox.classList.remove("empty");
  resultBox.classList.remove("typing");
  resultBox.textContent = message;
  resetLearningResources();
  resetYoutubeVideos();
  resetNextPlan();
}

function setResult(text) {
  if (!resultBox) {
    return;
  }
  latestResponseText = typeof text === "string" ? text : "";
  updateDownloadAvailability();
  stopTyping();
  resultBox.classList.remove("empty");
  typeText(formatRecommendationForDisplay(text));
  renderLearningResources(text);
  void renderYoutubePlaylists(text);
  renderNextPlan(text);
}

function setError(text) {
  if (!resultBox) {
    return;
  }
  latestResponseText = "";
  updateDownloadAvailability();
  stopTyping();
  resultBox.classList.remove("empty");
  resultBox.classList.remove("typing");
  resultBox.textContent = `Error: ${text}`;
  resetLearningResources();
  resetYoutubeVideos();
  resetNextPlan();
}

function setConfidence(value) {
  if (!confidenceChip) {
    return;
  }
  if (typeof value !== "number") {
    confidenceChip.textContent = "Confidence: --";
    return;
  }
  const normalized = value <= 1 ? value * 100 : value;
  const percent = Math.max(0, Math.min(100, Math.round(normalized)));
  confidenceChip.textContent = `Confidence: ${percent}%`;
}

function stopTyping() {
  if (typingTimer !== null) {
    clearInterval(typingTimer);
    typingTimer = null;
  }
}

function typeText(text) {
  if (!resultBox) {
    return;
  }
  resultBox.textContent = "";
  resultBox.classList.add("typing");
  let i = 0;
  const charsPerTick = 2;
  const speedMs = 12;
  typingTimer = setInterval(() => {
    i += charsPerTick;
    resultBox.textContent = text.slice(0, i);
    if (i >= text.length) {
      stopTyping();
      resultBox.classList.remove("typing");
    }
  }, speedMs);
}

function formatRecommendationTextBetter(text) {
  if (typeof text !== "string") {
    return "";
  }

  return text
    .replace(/\r\n/g, "\n")
    .replace(/\*\*(.*?)\*\*/g, "$1")
    .replace(/^\s{0,3}#{1,6}\s+(.+)$/gm, "$1")
    .replace(/^(\s*)\*\s+/gm, "$1- ")
    .replace(/([^\n])\n(\d+\.\s+)/g, "$1\n\n$2")
    .replace(/([^\n])\n([A-Za-z][^\n:]{1,60}:)/g, "$1\n\n$2")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

function stripLearningResourceLines(text) {
  const lines = text.split("\n");
  const removeIndexes = new Set();

  const isResourceHeader = (line) => {
    const cleaned = line.trim().toLowerCase();
    return (
      cleaned.includes("learning resources") ||
      cleaned.includes("relevant skills") ||
      cleaned.includes("following courses") ||
      cleaned.includes("recommended courses") ||
      cleaned.includes("youtube channels") ||
      cleaned.includes("courses:")
    );
  };

  const isResourceItem = (line) => {
    const trimmed = line.trim();
    const lower = trimmed.toLowerCase();
    if (!trimmed) return false;
    if (/^[-*+]\s+/.test(trimmed) || /^\d+\.\s+/.test(trimmed)) return true;
    if (/(?:https?:\/\/|www\.|coursera\.org|youtube\.com|youtu\.be)\S*/i.test(trimmed)) return true;
    if (lower.includes("youtube") || lower.includes("coursera")) return true;
    return false;
  };

  for (let i = 0; i < lines.length; i += 1) {
    if (!isResourceHeader(lines[i])) {
      continue;
    }
    removeIndexes.add(i);

    for (let j = i + 1; j < lines.length; j += 1) {
      const current = lines[j].trim();
      if (!current) {
        removeIndexes.add(j);
        continue;
      }
      if (looksLikeNewSection(current) || isPlanStartLine(current)) {
        break;
      }
      if (isResourceItem(current)) {
        removeIndexes.add(j);
        continue;
      }
      break;
    }
  }

  const filtered = lines.filter((_, idx) => !removeIndexes.has(idx));
  return filtered.join("\n").replace(/\n{3,}/g, "\n\n").trim();
}

function formatRecommendationForDisplay(text) {
  const normalized = formatRecommendationTextBetter(text);
  const noResources = stripLearningResourceLines(normalized);
  const noPlan = stripSixMonthPlanLines(noResources);
  return noPlan
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, "$1")
    .replace(/https?:\/\/\S+/gi, "")
    .replace(/(?:www\.)?(?:coursera\.org|youtube\.com|youtu\.be)\S*/gi, "")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

function resetLearningResources() {
  if (!learningResourcesBox) {
    return;
  }
  learningResourcesBox.classList.add("empty");
  learningResourcesBox.textContent = "Learning resources will appear here.";
}

function resetNextPlan() {
  if (!nextPlanBox) {
    return;
  }
  nextPlanBox.classList.add("empty");
  nextPlanBox.textContent = "6-month action plan will appear here.";
}

function resetYoutubeVideos() {
  if (!ytVideosBox) {
    return;
  }
  ytVideosBox.classList.add("empty");
  ytVideosBox.textContent = "Playlist suggestions based on your recommendation will appear here.";
}

function isPlanStartLine(line) {
  const lower = line.toLowerCase();
  return (
    lower.includes("next steps") ||
    lower.includes("6 months strategy") ||
    lower.includes("6-month strategy") ||
    lower.includes("6 month strategy") ||
    lower.includes("six month strategy") ||
    lower.includes("6 month plan") ||
    lower.includes("6-month plan") ||
    lower.includes("six month plan") ||
    lower.includes("roadmap")
  );
}

function looksLikeNewSection(line) {
  const trimmed = line.trim();
  if (!trimmed) {
    return false;
  }

  if (/^#{1,6}\s+/.test(trimmed)) {
    return true;
  }

  // Top-level numbered section headers like "1. Top Career Recommendations"
  if (/^\d+\.\s+[A-Za-z]/.test(trimmed) && !/^\d+\.\s*(month|week|phase|quarter)\b/i.test(trimmed)) {
    return true;
  }

  // Explicit section labels that indicate non-plan content
  if (
    /^(top career recommendations|skills match analysis|career path details|learning resources?)\s*:?\s*$/i.test(
      trimmed.replace(/^\**\s*|\s*\**$/g, "")
    )
  ) {
    return true;
  }

  return false;
}

function extractSixMonthPlanLines(text) {
  if (typeof text !== "string" || !text.trim()) {
    return [];
  }

  const lines = text.split("\n");
  const start = lines.findIndex((line) => isPlanStartLine(line));
  if (start === -1) {
    return [];
  }

  const isTimelineLine = (line) =>
    /^[-*]?\s*(month|week|phase|quarter)\b/i.test(line) ||
    /^\d+\.\s*(month|week|phase|quarter)\b/i.test(line);

  let end = lines.length;
  for (let i = start + 1; i < lines.length; i += 1) {
    const current = lines[i].trim();
    if (!current) {
      continue;
    }

    // Month/Week/Phase timeline lines belong to the plan section.
    if (isTimelineLine(current)) {
      continue;
    }

    if (looksLikeNewSection(current) && !isPlanStartLine(current)) {
      end = i;
      break;
    }
  }

  const selected = lines.slice(start, end).map((line) => line.trim());
  return selected.filter((line) => line.length > 0);
}

function stripSixMonthPlanLines(text) {
  const planLines = extractSixMonthPlanLines(text);
  if (!planLines.length) {
    return text;
  }

  let cleaned = text;
  planLines.forEach((line) => {
    const escaped = line.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    cleaned = cleaned.replace(new RegExp(`^\\s*${escaped}\\s*$`, "m"), "");
  });

  return cleaned.replace(/\n{3,}/g, "\n\n").trim();
}

function extractLinks(text) {
  if (typeof text !== "string" || !text.trim()) {
    return [];
  }

  const links = [];
  const seen = new Set();
  const markdownRe = /\[([^\]]+)\]\(((?:https?:\/\/)?(?:www\.)?(?:coursera\.org|youtube\.com|youtu\.be)[^\s)]*)\)/gi;
  const urlRe = /(?:https?:\/\/)?(?:www\.)?(?:coursera\.org|youtube\.com|youtu\.be)[^\s<>"')\]]*/gi;
  let match = null;

  const normalizeUrl = (raw) => {
    const value = (raw || "").trim();
    if (!value) {
      return "";
    }
    if (/^https?:\/\//i.test(value)) {
      return value;
    }
    return `https://${value.replace(/^\/+/, "")}`;
  };

  while ((match = markdownRe.exec(text)) !== null) {
    const label = match[1].trim();
    const url = normalizeUrl(match[2]);
    if (!seen.has(url)) {
      links.push({ label, url });
      seen.add(url);
    }
  }

  while ((match = urlRe.exec(text)) !== null) {
    const url = normalizeUrl(match[0]);
    if (!seen.has(url)) {
      links.push({ label: url, url });
      seen.add(url);
    }
  }

  return links;
}

function isSafeHttpUrl(url) {
  try {
    const parsed = new URL(url);
    return parsed.protocol === "http:" || parsed.protocol === "https:";
  } catch (error) {
    return false;
  }
}

function renderLearningResources(text) {
  if (!learningResourcesBox) {
    return;
  }

  const allLinks = extractLinks(text);
  const preferred = allLinks.filter((item) => {
    const lower = item.url.toLowerCase();
    return (
      lower.includes("youtube.com") ||
      lower.includes("youtu.be") ||
      lower.includes("coursera.org")
    );
  });

  if (!preferred.length) {
    learningResourcesBox.classList.add("empty");
    learningResourcesBox.textContent = "No YouTube or Coursera links found in this recommendation.";
    return;
  }

  preferred.sort((a, b) => {
    const platformRank = (url) => {
      const lower = url.toLowerCase();
      if (lower.includes("coursera.org")) return 0;
      if (lower.includes("youtube.com") || lower.includes("youtu.be")) return 1;
      return 2;
    };
    return platformRank(a.url) - platformRank(b.url);
  });

  learningResourcesBox.classList.remove("empty");
  learningResourcesBox.textContent = "";

  const list = document.createElement("ol");
  list.className = "resource-list";

  preferred.forEach((item) => {
    if (!isSafeHttpUrl(item.url)) {
      return;
    }

    const row = document.createElement("li");
    row.className = "resource-item";

    const link = document.createElement("a");
    link.className = "resource-link";
    link.href = item.url;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    link.textContent = item.label === item.url ? item.url : item.label;

    row.appendChild(link);
    list.appendChild(row);
  });

  if (!list.children.length) {
    learningResourcesBox.classList.add("empty");
    learningResourcesBox.textContent = "No valid learning resources found in this recommendation.";
    return;
  }

  learningResourcesBox.appendChild(list);
}

async function renderYoutubePlaylists(text) {
  if (!ytVideosBox) {
    return;
  }

  if (typeof text !== "string" || !text.trim()) {
    ytVideosBox.classList.add("empty");
    ytVideosBox.textContent = "No playlist suggestions found for this recommendation.";
    return;
  }

  ytVideosBox.classList.add("empty");
  ytVideosBox.textContent = "Finding matching YouTube playlists...";

  try {
    const playlists = await callApi("/youtube/playlists", {
      method: "POST",
      body: JSON.stringify({
        recommendation: text,
        max_results: 6,
      }),
    });

    if (!Array.isArray(playlists) || !playlists.length) {
      ytVideosBox.classList.add("empty");
      ytVideosBox.textContent = "No YouTube playlists found for this recommendation.";
      return;
    }

    ytVideosBox.classList.remove("empty");
    ytVideosBox.textContent = "";

    const list = document.createElement("ol");
    list.className = "playlist-list";

    playlists.forEach((item) => {
      if (!item?.url || !isSafeHttpUrl(item.url)) {
        return;
      }

      const row = document.createElement("li");
      row.className = "playlist-item";

      if (item.thumbnail && isSafeHttpUrl(item.thumbnail)) {
        const img = document.createElement("img");
        img.className = "playlist-thumb";
        img.src = item.thumbnail;
        img.alt = item.title ? `${item.title} thumbnail` : "Playlist thumbnail";
        img.loading = "lazy";
        row.appendChild(img);
      }

      const meta = document.createElement("div");
      meta.className = "playlist-meta";

      const link = document.createElement("a");
      link.className = "resource-link";
      link.href = item.url;
      link.target = "_blank";
      link.rel = "noopener noreferrer";
      link.textContent = item.title || "YouTube Playlist";

      const reason = document.createElement("p");
      reason.className = "playlist-reason";
      reason.textContent = item.channel ? `Channel: ${item.channel}` : "Recommended based on your career recommendation.";

      meta.appendChild(link);
      meta.appendChild(reason);
      row.appendChild(meta);
      list.appendChild(row);
    });

    if (!list.children.length) {
      ytVideosBox.classList.add("empty");
      ytVideosBox.textContent = "No valid YouTube playlists found.";
      return;
    }

    ytVideosBox.appendChild(list);
  } catch (error) {
    ytVideosBox.classList.add("empty");
    ytVideosBox.textContent = `Could not load YouTube playlists: ${error.message}`;
  }
}

function renderNextPlan(text) {
  if (!nextPlanBox) {
    return;
  }

  const normalized = formatRecommendationTextBetter(text);
  const lines = extractSixMonthPlanLines(normalized);

  if (!lines.length) {
    nextPlanBox.classList.add("empty");
    nextPlanBox.textContent = "No 6-month plan found in this recommendation.";
    return;
  }

  const cleanedLines = lines
    .map((line) =>
      line
        .replace(/^[-*]\s+/, "")
        .replace(/^\d+\.\s+/, "")
        .trim()
    )
    .filter((line) => line.length > 0)
    .filter((line) => !isPlanStartLine(line));

  nextPlanBox.classList.remove("empty");
  nextPlanBox.textContent = "";

  const list = document.createElement("ol");
  list.className = "plan-list";

  cleanedLines.forEach((line) => {
    const item = document.createElement("li");
    item.className = "plan-item";
    item.textContent = line;
    list.appendChild(item);
  });

  nextPlanBox.appendChild(list);
}

function setStatus(ready, errText = "") {
  void ready;
  void errText;
}

function toggleChatWidget() {
  chatOpen = !chatOpen;
  if (!chatWidget || !chatToggleBtn) {
    return;
  }
  chatWidget.hidden = !chatOpen;
  chatToggleBtn.setAttribute("aria-expanded", String(chatOpen));
  chatToggleBtn.setAttribute("aria-label", chatOpen ? "Close AI chat" : "Open AI chat");
  if (chatOpen) {
    chatInput?.focus();
  }
}

function appendChatMessage(role, text, options = {}) {
  if (!chatMessages) {
    return null;
  }
  const bubble = document.createElement("div");
  bubble.className = `chat-bubble ${role}`;
  if (options.loading) {
    bubble.classList.add("loading");
  }
  bubble.textContent = text;
  chatMessages.appendChild(bubble);
  chatMessages.scrollTop = chatMessages.scrollHeight;
  return bubble;
}

function setChatLoading(isLoading) {
  if (!chatInput || !chatSendBtn) {
    return;
  }
  chatInput.disabled = isLoading;
  chatSendBtn.disabled = isLoading;
  chatSendBtn.textContent = isLoading ? "..." : "Send";
}

async function submitChat(event) {
  if (event) {
    event.preventDefault();
  }
  if (!chatInput) {
    return;
  }
  const question = chatInput.value.trim();
  if (!question) {
    return;
  }

  appendChatMessage("user", question);
  chatInput.value = "";
  setChatLoading(true);
  const loadingBubble = appendChatMessage("bot", "Thinking...", { loading: true });

  try {
    const data = await callApi("/chat", {
      method: "POST",
      body: JSON.stringify({ question }),
    });

    if (loadingBubble?.remove) {
      loadingBubble.remove();
    }

    appendChatMessage("bot", data?.answer || "No answer generated.");
  } catch (error) {
    if (loadingBubble?.remove) {
      loadingBubble.remove();
    }
    appendChatMessage("bot", `Error: ${error.message}`);
  } finally {
    setChatLoading(false);
    chatInput?.focus();
  }
}

function updateDownloadAvailability() {
  if (!downloadTxtBtn) {
    return;
  }
  downloadTxtBtn.disabled = !latestResponseText.trim();
}

function setRecommendButtonLoading(isLoading) {
  if (!recommendBtn) {
    return;
  }

  if (isLoading) {
    recommendBtn.classList.add("loading");
    recommendBtn.disabled = true;
    recommendBtn.textContent = "Generating...";
    return;
  }

  recommendBtn.classList.remove("loading");
  recommendBtn.disabled = false;
  recommendBtn.textContent = "Get Recommendation";
}

function getLearningResourcesForExport(text) {
  const allLinks = extractLinks(text);
  const preferredLinks = allLinks.filter((item) => {
    const lower = item.url.toLowerCase();
    return (
      lower.includes("youtube.com") ||
      lower.includes("youtu.be") ||
      lower.includes("coursera.org")
    );
  });

  preferredLinks.sort((a, b) => {
    const platformRank = (url) => {
      const lower = url.toLowerCase();
      if (lower.includes("coursera.org")) return 0;
      if (lower.includes("youtube.com") || lower.includes("youtu.be")) return 1;
      return 2;
    };
    return platformRank(a.url) - platformRank(b.url);
  });

  const lines = preferredLinks.map((item) => {
    const label = item.label === item.url ? item.url : item.label;
    return `${label} - ${item.url}`;
  });

  return lines;
}

function getPlanLinesForExport(text) {
  const normalized = formatRecommendationTextBetter(text);
  const rawLines = extractSixMonthPlanLines(normalized);
  return rawLines
    .map((line) =>
      line
        .replace(/^[-*+]\s+/, "")
        .replace(/^\d+\.\s+/, "")
        .trim()
    )
    .filter((line) => line.length > 0)
    .filter((line) => !isPlanStartLine(line));
}

function downloadTxtReport() {
  const sourceText = latestResponseText.trim();
  if (!sourceText) {
    setError("Generate a recommendation first, then download the report.");
    return;
  }

  const recommendation = formatRecommendationForDisplay(sourceText) || "N/A";
  const resources = getLearningResourcesForExport(sourceText);
  const plan = getPlanLinesForExport(sourceText);

  const now = new Date();
  const timestamp = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, "0")}-${String(now.getDate()).padStart(2, "0")} ${String(now.getHours()).padStart(2, "0")}:${String(now.getMinutes()).padStart(2, "0")}`;
  const fileStamp = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, "0")}-${String(now.getDate()).padStart(2, "0")}_${String(now.getHours()).padStart(2, "0")}${String(now.getMinutes()).padStart(2, "0")}`;

  const content = [
    "Career Recommendation Report",
    `Generated: ${timestamp}`,
    "",
    "Recommendation",
    recommendation,
    "",
    "Learning Resources",
    resources.length ? resources.map((item, idx) => `${idx + 1}. ${item}`).join("\n") : "No learning resources found.",
    "",
    "Next 6 Months Plan",
    plan.length ? plan.map((item, idx) => `${idx + 1}. ${item}`).join("\n") : "No 6-month plan found.",
    "",
  ].join("\n");

  const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `career_recommendation_${fileStamp}.txt`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

async function callApi(path, options = {}) {
  const isFormData = options.body instanceof FormData;
  const headers = isFormData ? {} : { "Content-Type": "application/json" };
  const response = await fetch(path, {
    headers,
    ...options,
  });

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data.detail || `Request failed (${response.status})`);
  }
  return data;
}

async function checkStatus() {
  try {
    const data = await callApi("/status");
    setStatus(Boolean(data.ready), data.error || "");
  } catch (error) {
    setStatus(false, error.message);
  }
}

async function submitNatural(event) {
  if (!naturalForm) {
    return;
  }
  event.preventDefault();
  const file = resumeFileInput?.files?.[0];
  const form = new FormData(naturalForm);
  const description = String(form.get("description") || "").trim();

  if (!file && !description) {
    setError("Please add a profile description or upload a resume.");
    return;
  }

  setLoading(file ? "Reading resume and generating recommendation..." : "Generating recommendation from your description...");
  setConfidence(undefined);
  setRecommendButtonLoading(true);
  try {
    let data;
    if (file) {
      const payload = new FormData();
      payload.append("file", file);
      data = await callApi("/recommend/resume", {
        method: "POST",
        body: payload,
      });
    } else {
      const payload = { description };
      data = await callApi("/recommend/natural", {
        method: "POST",
        body: JSON.stringify(payload),
      });
    }
    setResult(data.recommendation || "No recommendation returned.");
    setConfidence(data.confidence);
  } catch (error) {
    setError(error.message);
  } finally {
    setRecommendButtonLoading(false);
  }
}

naturalForm?.addEventListener("submit", submitNatural);
downloadTxtBtn?.addEventListener("click", downloadTxtReport);
chatToggleBtn?.addEventListener("click", toggleChatWidget);
chatForm?.addEventListener("submit", submitChat);
checkStatus();
resetLearningResources();
resetYoutubeVideos();
resetNextPlan();
updateDownloadAvailability();
