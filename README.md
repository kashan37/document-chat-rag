# 📄 Contexta — AI-Powered PDF Assistant

Chat with your PDFs. Upload a document, ask questions, and get answers grounded strictly in what the file actually says — no outside knowledge, no hallucinated facts, and now, no conversational amnesia either.

Built with a RAG (Retrieval-Augmented Generation) pipeline on top of Google's Gemini, wrapped in a dark UI.

---

## ✨ Features

- **Upload & chat** — drop in a PDF, ask anything about it
- **Grounded answers** — responses are built strictly from retrieved document chunks, not the model's general knowledge
- **Conversation memory** — the last 4 exchanges are sent along with each new question, so follow-ups like *"tell me more about that"* or *"what about X instead"* actually work
- **Quick follow-up chips** — one-click prompts ("Tell me more," "Simplify that," "Give me an example") appear after each answer
- **Cheerful, corny tone** — answers are warm and a little playful, without ever sacrificing accuracy for personality
- **Prompt-injection resistant** — untrusted document text is explicitly fenced off and never treated as instructions
- **Dark, premium UI** — near-black theme with a signature "ion blue" accent, glassmorphism cards, and monospace data readouts
- **Custom favicon** — a document + chat-bubble mark instead of a stock emoji

---

## 🧠 How It Works (Architecture)

```
PDF Upload
    │
    ▼
loader.py          → extracts and cleans raw text (pypdf)
    │
    ▼
chunker.py         → splits text into overlapping chunks (500 chars, 100 overlap)
    │
    ▼
embeddings.py      → encodes chunks into vectors (all-MiniLM-L6-v2)
    │
    ▼
vector_store.py    → stores vectors in a FAISS index for similarity search
    │
    ▼
chat_engine.py     → on each question: embeds it, retrieves top-5 relevant
                       chunks, and tracks the last 4 Q&A pairs as memory
    │
    ▼
rag_pipeline.py    → builds the final prompt (document context + conversation
                       history) and calls Gemini for the answer
    │
    ▼
app.py             → Streamlit UI: upload panel, chat window, follow-up chips
```

### The RAG loop, per question
1. Question gets embedded with the same model used for the document chunks
2. FAISS searches for the 5 most relevant chunks (`IndexFlatL2`, cosine-style nearest neighbor)
3. Those chunks + the last 4 conversation turns get assembled into a single prompt
4. Gemini (`gemini-2.5-flash`) generates the answer, temperature `0.4` — low enough to stay grounded, high enough to have some personality in *how* it phrases things

### Conversation memory — how it stays honest
Document context and conversation history are **kept in separate, clearly labeled blocks** in the prompt:

```
<conversation_history>   ← used only to resolve "it," "that," "what about X"
...
</conversation_history>

<document_context>       ← the ONLY source of factual claims
...
</document_context>
```

The model is explicitly instructed: history is for understanding *what you mean*, never for *what's true*. This stops a single wrong or fuzzy answer from compounding into a chain of hallucinations across a long conversation. Memory is capped at 4 turns to keep token usage (and cost) predictable — it doesn't grow forever as a conversation goes on.

---

## 📁 Project Structure

```
.
├── app.py              # Streamlit UI — upload, chat, follow-ups, favicon
├── chat_engine.py       # Orchestrates load → embed → retrieve → ask, holds memory
├── loader.py            # PDF text extraction + cleaning
├── chunker.py           # Overlapping text chunking
├── embeddings.py         # Sentence-transformer embedding model
├── vector_store.py       # FAISS similarity search wrapper
├── rag_pipeline.py       # Prompt construction + Gemini call
├── assets/
│   ├── style.css         # Dark UI theme (design tokens, components)
│   └── favicon.png       # Custom app icon
└── requirements.txt
```

---

## 🚀 Setup

1. Clone the repo and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the project root with your Gemini API key:
   ```
   GOOGLE_API_KEY=your_key_here
   ```

3. Run the app:
   ```bash
   streamlit run app.py
   ```

4. Open the local URL Streamlit gives you, upload a PDF, and start asking questions.

---

## 🎨 Design System

The UI follows a dark, instrument-panel aesthetic rather than a generic chat template:

| Token | Value | Used for |
|---|---|---|
| `--obsidian` | `#08080a` | Page background |
| `--graphite` / `--graphite-2` | `#0f0f12` / `#16161a` | Card surfaces |
| `--platinum` | `#f5f5f7` | Primary text |
| `--silver` / `--steel` | `#98989d` / `#636368` | Secondary / muted text |
| `--ion` | `#0a84ff` | Signature accent — buttons, focus states, links |
| `--emerald` | `#34d399` | Status indicators ("ready," "loaded") |

Typography splits duty deliberately: **Inter** for regular UI text, **JetBrains Mono** for anything data-like (message counts, status readouts, the filename chip) — a small detail that makes the interface feel engineered rather than templated.

---

## ⚠️ Known Limitations

- **Memory window is capped at 4 turns.** Ask about something 8 messages ago and the model genuinely won't remember it — that context has aged out.
- **No page-level citations yet.** Answers reference document content but don't currently point to specific page numbers.
- **Single document at a time.** Loading a new PDF clears the previous document and its conversation memory.
- **`st.chat_input` always docks at the bottom of the viewport** — this is a Streamlit framework behavior, not something fixable via CSS.

---

## 🛠️ Tech Stack

- **Streamlit** — UI framework
- **pypdf** — PDF text extraction
- **sentence-transformers** (`all-MiniLM-L6-v2`) — embeddings
- **FAISS** — vector similarity search
- **Google Generative AI** (`gemini-2.5-flash`) — answer generation
- **python-dotenv** — environment variable management

---

## 🔮 Possible Next Steps

- Page-number citations in answers
- Multi-document support (chat across several PDFs at once)
- Adjustable memory window / model temperature from the UI
- Streaming responses instead of a single spinner-then-answer
