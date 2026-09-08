# Deep Research Agent — Code Explanation

## 1. Overall Architecture

```text
User Query
    ↓
Supervisor
    ↓
Can Split?
  ├── Yes → Independent Agent
  │             ↓
  │        Sub-Queries
  │             ↓
  │        Supervisor (Recursive)
  │
  └── No → Worker
              ↓
         Tavily Web Search
              ↓
         Gemini Synthesis
              ↓
         Reports + Citations
              ↓
         Final Markdown Report
```

**Pipeline:** Plan/Route → Decompose → Search → Synthesize → Aggregate → Report

---

## 2. Shared State

`DeepResearchSharedState` stores:

- `question` → current research question
- `model` → Gemini model
- `depth` → recursion limit
- `breadth` → number of sub-queries
- `citations` → collected source URLs
- `research_topics` → researched topics
- `reports` → generated answers

---

## 3. Structured Outputs

Pydantic models make LLM output predictable.

| Model | Purpose |
|---|---|
| `QuerySplitterOutput` | Decides whether query can be split |
| `IndependentAgentOutput` | Returns sub-queries |
| `UniqueResearchTopicOutput` | Checks duplicate topics |
| `WorkerOutput` | Returns research answer |

---

## 4. Model

`build_model()` creates:

```text
Gemini 2.5 Pro
      ↓
ChatGoogleGenerativeAI
```

Gemini is used for query splitting, sub-query generation, topic checking, and research synthesis.

---

## 5. Supervisor

The **Supervisor is the main router**.

It checks:

1. Is `depth > 0`?
2. Can the query be split?
3. If yes → Independent Agent.
4. If no → check topic uniqueness.
5. If unique → Worker.
6. If already researched → skip.

```text
Supervisor
   │
   ├── Can split? ── Yes → Independent Agent
   │
   └── No
        ↓
   Unique topic?
      ├── Yes → Worker
      └── No  → Skip
```

---

## 6. Independent Agent / Distributor

It breaks a complex query into smaller, non-overlapping research tasks.

Example:

```text
Children's Healthy Growth
├── Study & Learning
├── Daily Routine
├── Physical Activity
├── Hobbies
└── Goal Setting
```

For each sub-query:

```text
depth = current_depth - 1
```

Then it recursively calls the Supervisor.

---

## 7. Recursive Research Tree

```text
Main Query
├── Sub-query 1
│   ├── Sub-sub-query
│   └── Sub-sub-query
├── Sub-query 2
│   ├── Sub-sub-query
│   └── Sub-sub-query
└── Sub-query 3
```

Research continues until:

- `depth` reaches the limit, or
- the query cannot be split.

---

## 8. Worker Agent

The Worker performs the actual research:

```text
Research Topic
      ↓
Tavily Search
      ↓
Filter Results
      ↓
Gemini
      ↓
Evidence-based Answer
```

It:

- Searches the web using Tavily.
- Gets up to 5 results.
- Filters low-relevance results.
- Synthesizes the evidence using Gemini.
- Adds citations.
- Reports conflicting information.
- Attempts to avoid hallucinations.

---

## 9. Web Search Filtering

The code uses:

```python
WEB_SEARCH_RELEVANCE_SCORE_THRESHOLD = 0.30
```

Only results satisfying:

```text
score >= 0.30
```

are retained.

Each result stores:

```text
cited_url
content
score
```

---

## 10. Topic Deduplication

Before research, the code checks whether the topic is already covered.

```text
New Topic
    ↓
Uniqueness Checker
    ↓
Already researched?
   ├── Yes → Skip
   └── No  → Worker
```

This reduces duplicate research.

---

## 11. Fan-Out / Fan-In

### Fan-Out

One query creates multiple research branches:

```text
Main Query
├── Topic A
├── Topic B
├── Topic C
└── Topic D
```

### Fan-In

Child results are merged into the parent state:

```text
Topic A ─┐
Topic B ─┤
Topic C ─┼──→ Combined Research
Topic D ─┘
```

---

## 12. Depth vs Breadth

### Depth

Controls how deeply the agent recursively decomposes the problem.

```text
Depth 0 → Worker
Depth 1 → Can split once
Depth 2 → Can split twice
```

### Breadth

Controls how many sub-queries can be generated.

```text
Breadth = 5

Query
├── Q1
├── Q2
├── Q3
├── Q4
└── Q5
```

**Depth = vertical exploration**

**Breadth = horizontal exploration**

---

## 13. Final Report

`build_deep_research_report()` combines:

- Research reports
- Research topics
- Unique citations

It generates a Markdown report with a table of contents and references.

```text
Research Report
├── Table of Contents
├── Topic 1
├── Topic 2
├── Topic 3
└── References
```

---

## 14. Main Execution Flow

`initiate_deep_research()` initializes:

```text
query
depth
breadth
model
citations = []
research_topics = []
reports = []
```

Then:

```text
initiate_deep_research()
        ↓
    Supervisor
        ↓
  Research Tree
        ↓
     Workers
        ↓
 Aggregated Results
        ↓
   Final Report
```

---

## 15. Entry Point

`start_deep_research(task)`:

1. Loads environment variables.
2. Gets task ID and prompt.
3. Starts research with:

```python
depth=2
breadth=5
```

4. Saves the final response.
5. Writes:

```text
research_output/output_final_report_<task_id>.md
```

---

# Design Patterns Used

| Pattern | Usage |
|---|---|
| Recursive Tree | Research decomposition |
| Supervisor / Router | Query routing |
| Fan-Out / Fan-In | Branch creation and aggregation |
| Worker Pattern | Actual research |
| Structured Output | Pydantic LLM responses |
| Deduplication | Topics and citations |
| Relevance Filtering | Tavily score threshold |
| Bounded Search | Maximum 5 search results |

---

# Important Interview Explanation

> I implemented a recursive Deep Research Agent using a Supervisor, Distributor, and Worker architecture. The Supervisor decides whether a query should be decomposed. The Distributor creates bounded sub-queries based on breadth, and each sub-query recursively goes through the Supervisor until the depth limit is reached. Leaf Workers use Tavily for web search and Gemini for evidence-based synthesis. Results are aggregated using fan-in, with topic deduplication, relevance filtering, and citations before generating the final report.

---

# Important Code Limitation

There is a potential issue in `supervisor()`:

If a topic is detected as non-unique, `agent_state_response` may not be assigned before it is returned.

Safer:

```python
agent_state_response = agent_state
```

Initialize it at the beginning of `supervisor()`.

Also, `sleep_thread()` uses only a fixed 1-second delay. A production system should generally use **retry + exponential backoff** for API rate limits.

---

# 5 Things to Remember

```text
Supervisor    → Decides
Distributor   → Splits
Worker        → Researches
Depth         → Controls how deep
Breadth       → Controls how wide
```

---

# One-Line Summary

**This is a recursive, bounded-depth/breadth Deep Research Agent where a Supervisor routes queries, an Independent Agent decomposes them, Workers search and synthesize evidence, and results are merged into a cited Markdown report.**
