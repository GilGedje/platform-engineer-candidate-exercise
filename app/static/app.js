"use strict";

const form = document.querySelector("#note-form");
const draft = document.querySelector("#note-text");
const saveButton = document.querySelector("#save-button");
const saveLabel = document.querySelector("#save-label");
const formStatus = document.querySelector("#form-status");
const listStatus = document.querySelector("#list-status");
const refreshButton = document.querySelector("#refresh-button");
const list = document.querySelector("#notes-list");
const count = document.querySelector("#note-count");
const emptyState = document.querySelector("#empty-state");
const characterCount = document.querySelector("#character-count");
const dateFormat = new Intl.DateTimeFormat(undefined, {
  month: "short", day: "numeric", hour: "numeric", minute: "2-digit",
});
let notes = [];
let saving = false;
let refreshing = false;

async function api(path, options = {}) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 8000);
  try {
    const response = await fetch(path, { ...options, signal: controller.signal });
    if (!response.ok) {
      throw new Error(response.status === 422
        ? "Please use a note between 1 and 2,000 characters."
        : "We couldn't reach your notes. Please try again.");
    }
    return await response.json();
  } catch (error) {
    if (error.name === "AbortError" || error instanceof TypeError) {
      throw new Error("The connection was interrupted. Please try again.");
    }
    throw error;
  } finally {
    clearTimeout(timeout);
  }
}

function updateComposer() {
  saveButton.disabled = saving || !draft.value.trim();
  draft.readOnly = saving;
  saveLabel.textContent = saving ? "Saving…" : "Save note";
  characterCount.textContent = `${draft.value.length.toLocaleString()} / 2,000`;
}

function renderNotes() {
  list.replaceChildren();
  count.textContent = notes.length === 100 ? "100 latest" : String(notes.length);
  emptyState.hidden = notes.length !== 0;
  for (const note of notes) {
    const item = document.createElement("li");
    item.className = "note";
    item.dataset.noteId = String(note.id);
    const text = document.createElement("p");
    text.className = "note-text";
    text.dir = "auto";
    text.textContent = note.text;
    const timestamp = document.createElement("time");
    timestamp.dateTime = note.created_at;
    timestamp.textContent = dateFormat.format(new Date(note.created_at));
    item.append(text, timestamp);
    list.append(item);
  }
}

async function loadNotes() {
  if (refreshing || saving) return;
  refreshing = true;
  refreshButton.disabled = true;
  list.setAttribute("aria-busy", "true");
  listStatus.classList.remove("error");
  listStatus.textContent = "Loading your notes…";
  try {
    notes = await api("/notes");
    renderNotes();
    listStatus.textContent = "";
  } catch (error) {
    emptyState.hidden = true;
    listStatus.classList.add("error");
    listStatus.textContent = error.message + (notes.length ? " Showing previously loaded notes." : " Select Refresh to retry.");
  } finally {
    refreshing = false;
    refreshButton.disabled = saving;
    list.removeAttribute("aria-busy");
  }
}

draft.addEventListener("input", () => {
  formStatus.textContent = "";
  formStatus.classList.remove("error");
  updateComposer();
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (saving || !draft.value.trim()) return;
  // Wait for an in-flight refresh before saving so it cannot replace a newly saved note.
  if (refreshing) {
    formStatus.textContent = "Your notes are loading. Please try saving in a moment.";
    return;
  }
  saving = true;
  refreshButton.disabled = true;
  formStatus.textContent = "";
  formStatus.classList.remove("error");
  updateComposer();
  try {
    const note = await api("/notes", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: draft.value }),
    });
    notes = [note, ...notes.filter((existing) => existing.id !== note.id)].slice(0, 100);
    renderNotes();
    listStatus.textContent = "";
    listStatus.classList.remove("error");
    draft.value = "";
    formStatus.textContent = "Note saved.";
  } catch (error) {
    formStatus.classList.add("error");
    formStatus.textContent = error.message + " Your draft is still here.";
  } finally {
    saving = false;
    refreshButton.disabled = false;
    updateComposer();
    draft.focus();
  }
});

refreshButton.addEventListener("click", loadNotes);
updateComposer();
loadNotes();
