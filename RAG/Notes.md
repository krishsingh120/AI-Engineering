# Self-RAG flow :

Idea: The LLM checks its own work while generating the answer.

## HLD

```bash
User Query
    ↓
Retriever
    ↓
Relevant Documents
    ↓
LLM
 ↓       ↑
Generate → Self-Check
            ↓
       Good? ── No ──→ Retrieve/Generate Again
            │
           Yes
            ↓
         Final Answer

```

## Simple flow
1. User asks a question.
2. Retrieve relevant documents.
3. LLM generates an answer.
4. LLM checks its own answer:
    Is retrieval needed?
    Is the answer supported by documents?
    Is there hallucination?
    If bad → improve/retrieve again.
5. Return final answer.

- Key point: 🧠 LLM evaluates and improves itself.



# Corrective RAG :

Idea: A separate retrieval evaluator/grader checks whether retrieved documents are useful.


## HLD
```bash

User Query
    ↓
Retriever
    ↓
Retrieved Documents
    ↓
Document Grader
    ↓
 ┌───────────────┬───────────────┐
 Relevant        Not Relevant
    ↓                 ↓
Generate          Web Search /
Answer            Better Retrieval
    ↓                 ↓
    └──────→ Generate Answer
                  ↓
              Final Answer

```

## Simple flow
1. User asks a question.
2. Retriever gets documents.
3. Grader checks document quality/relevance.
      If relevant → generate answer.
      If irrelevant → perform corrective action:
4. better retrieval
5. web search
6. query transformation, etc.
7. Generate final answer.

- Key point: 🔍 It corrects bad retrieval before trusting it.