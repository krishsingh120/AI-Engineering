# Agenda

1. Add Memory to LLMs
2. With vs without equipped Memory
3. Case 1: Chat History as a Context
4. Case 2: Summarizing chat history
5. Conclusion!

---

# LLM Memory

## Memory Approaches

1. **Full Chat History Memory** → Send previous messages with every new query.
2. **Summarized Memory** → Once history becomes large, summarize it and send only the summary + current query.

---

## 1. Full Chat History Memory

```text
User
  │
  │ "Explain Dynamic Programming"
  ▼
LLM
  │
  │ response
  ▼
chatHistory
  │
  ├── HumanMessage
  └── AIMessage
          │
          ▼
New question:
"What did I ask earlier?"
          │
          ▼
Send BOTH to LLM
          │
          ▼
LLM remembers from context
```

**Key idea:** The LLM does not permanently remember the conversation. The application sends the previous messages again as context with the new query.

---

## 2. Summarized Memory

```text
Chat History

Human → Explain DP
AI    → DP explanation

Human → Explain Graphs
AI    → Graph explanation

        ↓

History >= 4 messages

        ↓

LLM summarizes everything

        ↓

"User asked about Dynamic Programming
and Graph data structures..."
```

**Key idea:** Instead of sending the entire chat history, the application creates a compact summary and sends the summary + current query to the LLM.

### Why use summarization?

- Reduces token usage.
- Prevents the context window from growing indefinitely.
- Can preserve important information from older messages.
- Some details may be lost during summarization.
