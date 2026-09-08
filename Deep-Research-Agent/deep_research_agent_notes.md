# Deep Research Agent — Interview Notes

## 1. What is a Deep Research Agent?

An AI agent that performs **multi-step research** by:
- Planning sub-tasks
- Searching multiple sources
- Verifying information
- Synthesizing a final answer
- Providing citations

### Simple Example

**User asks:**  
> Which is better for a backend developer in 2026: Go or Java?

Instead of answering directly:

```text
User Query
    ↓
Research Agent
    ↓
Break into tasks
 ┌──────────────┬──────────────┐
 ↓              ↓              ↓
Job Market    Performance    Ecosystem
 ↓              ↓              ↓
Search Web    Search Docs    Search Reports
 └──────────────┴──────────────┘
              ↓
        Compare & Verify
              ↓
        Final Research
              ↓
     Sources + Recommendation
```

---

# 2. HLD

```text
User Query
    ↓
Planner Agent
    ↓
Research Tasks
    ↓
Search / Web / RAG
    ↓
Source Evaluator
    ↓
 ┌───────────────┐
 │ Enough Info?  │
 └───────┬───────┘
      No ↓     ↑
    Search More
      ↓
   Synthesizer
      ↓
Final Answer
+ Citations
```

### Core Pipeline

**Plan → Search → Evaluate → Iterate → Synthesize → Cite**

---

# 3. Cost & Latency Optimization

### Interview Question

**Q: How would you reduce the cost and latency of a Deep Research Agent?**

### Answer

> I would use parallel research tasks, caching, smaller models for planning/grading, limit the number of iterations, deduplicate sources, and stop research early once sufficient evidence is collected.

### Techniques

1. **Parallel search** — execute independent searches simultaneously.
2. **Async processing** — don't block on independent tasks.
3. **Caching** — cache repeated queries/results.
4. **Smaller models** — use cheap/fast models for routing, grading, and summarization.
5. **Early stopping** — stop when enough reliable evidence is collected.
6. **Streaming** — stream the final response to the user.

**Key:** Parallelism + Caching + Smaller Models + Early Stopping

---

# 4. Scalable Deep Research Agent

```text
                    User Query
                        ↓
                     Planner
                        ↓
              ┌─────────┼─────────┐
              ↓         ↓         ↓
           Search     Search     Search
              └─────────┼─────────┘
                        ↓
                 Rank / Evaluate
                        ↓
                 Research Loop
                        ↓
                  Synthesizer
                        ↓
                 Final + Citations
```

---

# 5. Performance / Latency

### Goal
**Reduce response time.**

### Techniques
- Parallel search
- Async processing
- Caching
- Smaller/faster models
- Early stopping
- Streaming

**Key:** Parallelism + Caching + Smaller Models + Early Stopping

---

# 6. Scale

### Goal
Handle **many users/research jobs simultaneously**.

```text
             API Gateway
                  ↓
              Job Queue
          ↙       ↓       ↘
     Worker 1  Worker 2  Worker 3
          ↓       ↓       ↓
       Search / LLM / RAG
                  ↓
              Aggregator
```

### Techniques

1. **Queue** → RabbitMQ / Kafka / SQS
2. **Horizontal workers** → scale research workers
3. **Stateless services** → easy horizontal scaling
4. **Redis** → caching + rate limiting
5. **DB / Vector DB** → persistent research data
6. **Rate limits** → protect external APIs

**Key:** Queue + Horizontal Scaling + Stateless Workers

---

# 7. Accuracy

### Goal
Improve reliability and reduce hallucinations.

### Techniques
- Multiple independent sources
- Source credibility scoring
- Fact verification
- Cross-check conflicting information
- Query decomposition
- Citation grounding
- Retrieval quality evaluation
- Final answer validation

### Accuracy Flow

```text
Search
  ↓
Relevant?
  ↓
Reliable Source?
  ↓
Cross-check
  ↓
Generate
  ↓
Fact / Citation Check
```

**Key:** Don't trust a single source or a single LLM generation.

---

# 8. Improvement / Feedback Loop

Use an **evaluation + feedback loop**.

```text
Research
   ↓
Answer
   ↓
Evaluator
   ↓
 ┌──────────────┐
 │ Good enough? │
 └──────┬───────┘
      No ↓
Improve Search / Prompt / Sources
      ↓
Research Again
```

### Track These Metrics

- Accuracy / Factuality
- Citation correctness
- Retrieval precision / recall
- Latency
- Cost per query
- Task success rate
- User feedback

---

# 9. Interview Cheat Sheet

| Area | Key Concepts |
|---|---|
| Performance | Parallel + Cache |
| Scale | Queue + Workers |
| Accuracy | Verify + Ground |
| Improvement | Evaluate + Feedback |
| Core Pipeline | Plan → Search → Evaluate → Iterate → Synthesize → Cite |

## One-Line Interview Answer

> A production-ready Deep Research Agent should use **parallel and cached research for performance, queues and horizontal workers for scale, multi-source verification and citation grounding for accuracy, and continuous evaluation and feedback for improvement.**
