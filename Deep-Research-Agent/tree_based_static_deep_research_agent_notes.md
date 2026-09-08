# Tree-Based Static Deep Research Agent — Short Interview Notes

## 1. Definition

A **Tree-Based Static Deep Research Agent** is a research system with a **predefined hierarchical tree** of research tasks.

Instead of dynamically deciding what to research next, the system follows a fixed workflow:

**Query → Tree → Parallel Research → Verify → Aggregate → Synthesize → Cite**

### Main Goals
- Predictable execution
- Controlled cost
- Low latency
- Reliable research
- Easy testing and debugging
- Horizontal scalability

---

# 2. HLD

```text
                         User Query
                              ↓
                         API Gateway
                              ↓
                      Research Controller
                              ↓
                    Static Research Tree
                              ↓
             ┌────────────────┼────────────────┐
             ↓                ↓                ↓
          Branch A         Branch B         Branch C
             ↓                ↓                ↓
         Leaf Tasks        Leaf Tasks        Leaf Tasks
             └────────────────┼────────────────┘
                              ↓
                     Source Evaluation
                              ↓
                       Branch Aggregator
                              ↓
                       Root Synthesizer
                              ↓
                    Citation / Fact Check
                              ↓
                       Final Response
```

---

# 3. Static Research Tree

Example:

```text
Backend Comparison
├── Performance
│   ├── Throughput
│   └── Latency
├── Ecosystem
│   ├── Libraries
│   └── Frameworks
├── Job Market
│   ├── Go
│   └── Java
└── Development
    ├── Productivity
    └── Learning Curve
```

### Node Types

- **Root** → complete research problem
- **Branch** → research category
- **Leaf** → executable research task
- **Aggregator** → combines child results
- **Synthesizer** → generates final answer

---

# 4. Execution Model

### Independent nodes

Run in parallel:

```text
          Root
       /    |    \
     A      B      C
     ↓      ↓      ↓
       Parallel
```

### Dependent nodes

Run sequentially:

```text
A → B → C
```

### Recommended

Use **parallel execution for independent sibling nodes** and sequential execution only when there is dependency.

---

# 5. Core Pipeline

```text
1. Receive Query
2. Select Static Tree
3. Create Research Job
4. Traverse Tree
5. Execute Leaf Tasks
6. Search / Retrieve Data
7. Evaluate Sources
8. Aggregate Results
9. Verify Evidence
10. Synthesize Final Answer
11. Validate Citations
12. Return Response
```

---

# 6. Important Design Patterns

## A. Tree / Composite Pattern

Represent research as hierarchical nodes.

```text
ResearchNode
├── ResearchNode
├── ResearchNode
└── ResearchNode
```

Useful for:
- Recursive execution
- Nested research tasks
- Bottom-up aggregation

---

## B. Strategy Pattern

Different research tasks can use different strategies.

```text
ResearchStrategy
├── WebSearchStrategy
├── RAGStrategy
├── DatabaseStrategy
└── APIResearchStrategy
```

Useful when different nodes require different data sources.

---

## C. Template Method Pattern

Define a common research workflow:

```text
Research
 ↓
Retrieve
 ↓
Evaluate
 ↓
Summarize
```

Individual node types can customize specific steps.

---

## D. Chain of Responsibility

Pass research results through validation stages:

```text
Retrieve
  ↓
Relevance Check
  ↓
Source Check
  ↓
Fact Check
  ↓
Citation Check
```

Each stage can reject or modify the result.

---

## E. Fan-Out / Fan-In

### Fan-Out

Split work into parallel tasks.

```text
             Root
          /   |   \
        A     B     C
```

### Fan-In

Merge results.

```text
A ─┐
B ─┼──→ Aggregator
C ─┘
```

Very important for **performance and scalable research**.

---

## F. Producer-Consumer Pattern

Use a queue between controllers and workers.

```text
Controller
    ↓
   Queue
 ↓   ↓   ↓
W1  W2  W3
```

Useful for:
- Scaling
- Backpressure
- Async execution
- Failure isolation

---

## G. Retry Pattern

Retry failed leaf tasks independently.

```text
Task
 ↓
Failed?
 ↓
Retry
 ↓
Success / Fallback
```

Use **exponential backoff** and a maximum retry count.

---

## H. Circuit Breaker

Protect the system from failing external APIs.

```text
Worker → External API
             ↓
          Failures
             ↓
       Circuit Open
```

Useful for:
- Search APIs
- LLM APIs
- Third-party services

---

## I. Cache-Aside Pattern

```text
Request
  ↓
Redis Cache?
 ↙      ↘
Yes      No
 ↓        ↓
Return   Search
          ↓
        Cache
```

Useful for reducing:
- Latency
- API calls
- LLM cost

---

## J. Bulkhead Pattern

Isolate failures between workers/resources.

```text
Research Pool A
Research Pool B
Research Pool C
```

Failure in one pool should not take down the entire system.

---

# 7. Performance / Latency

### Techniques

- Parallel sibling execution
- Async I/O
- Caching
- Batch requests
- Smaller models for simple tasks
- Early stopping
- Search result deduplication
- Streaming final response

### Key

**Parallel + Async + Cache + Early Stop**

---

# 8. Scalability

```text
                 API Gateway
                      ↓
                  Job Queue
               ↙     ↓     ↘
             W1      W2      W3
             ↓       ↓       ↓
          Leaf Tasks / Search / LLM
               ↘     ↓     ↙
                 Aggregator
                     ↓
                 Synthesizer
```

### Use

- RabbitMQ / Kafka / SQS
- Stateless workers
- Horizontal scaling
- Redis
- Database
- Object storage
- Rate limiting
- Load balancing

### Key

**Queue + Stateless Workers + Horizontal Scaling**

---

# 9. Accuracy

### Techniques

- Multiple independent sources
- Source credibility scoring
- Relevance grading
- Cross-source verification
- Fact checking
- Citation grounding
- Final answer validation
- Conflict detection

### Flow

```text
Search
 ↓
Relevant?
 ↓
Reliable?
 ↓
Cross-check
 ↓
Extract Evidence
 ↓
Generate
 ↓
Citation / Fact Check
```

### Key

**Verify + Ground + Cross-check**

---

# 10. Reliability

### Important Concepts

- Retry with exponential backoff
- Timeout
- Circuit breaker
- Idempotency
- Dead-letter queue
- Failure isolation
- Fallback source
- Partial-result handling

### Node State

```text
PENDING
RUNNING
COMPLETED
FAILED
RETRYING
SKIPPED
```

---

# 11. Cost Optimization

- Fixed tree → predictable number of tasks
- Cache repeated searches
- Deduplicate documents
- Use smaller models for leaf tasks
- Strong model only for synthesis
- Limit search results
- Limit retries
- Early stopping
- Reuse previous research

### Key

**Control LLM calls + Search calls + Tokens**

---

# 12. State Management

Store research job state:

```text
Job
├── job_id
├── query
├── tree_id
├── node_status
├── results
├── citations
├── errors
└── timestamps
```

Possible storage:

- PostgreSQL / MongoDB → job state
- Redis → temporary state/cache
- Object Storage → large reports/artifacts

---

# 13. Observability

Track:

### Metrics
- End-to-end latency
- Node latency
- Token usage
- Cost per query
- Search API usage
- Success/failure rate
- Retry count
- Cache hit rate
- Citation accuracy
- Research quality

### Logging

Use `job_id` + `node_id` for distributed tracing.

---

# 14. Evaluation

Evaluate at 3 levels:

```text
Leaf Evaluation
      ↓
Branch Evaluation
      ↓
Final Answer Evaluation
```

### Metrics

- Factuality
- Citation correctness
- Source relevance
- Retrieval precision / recall
- Task success rate
- Latency
- Cost
- User feedback

---

# 15. Security

Important in production:

- Authentication / Authorization
- API rate limiting
- Input validation
- Prompt-injection protection
- Untrusted web-content isolation
- Secrets management
- Tool permission control
- SSRF protection for URL fetching
- Output sanitization

---

# 16. Static vs Dynamic Research Agent

| Static Tree | Dynamic Agent |
|---|---|
| Predefined plan | LLM creates plan |
| Predictable cost | Variable cost |
| Predictable latency | Variable latency |
| Easier testing | Harder testing |
| More controlled | More autonomous |
| Good for repeated tasks | Good for open-ended research |
| Easier debugging | More complex debugging |

### When to use Static?

Use static trees when:
- Research categories are known
- Workflow is repeated
- Reliability matters
- Cost must be predictable
- Compliance/control matters

Use dynamic agents when:
- Questions are highly open-ended
- Research path changes frequently
- Unexpected discoveries are valuable

---

# 17. Important Interview Questions

### Q1. Why static tree?

> It provides predictable execution, cost, latency, testing, and control.

### Q2. How do you reduce latency?

> Parallelize independent nodes, use async I/O, caching, batching, and early stopping.

### Q3. How do you scale?

> Use queues, stateless workers, horizontal scaling, load balancing, and rate limiting.

### Q4. How do you improve accuracy?

> Use source ranking, multi-source verification, citation grounding, and final validation.

### Q5. What if one node fails?

> Retry that node independently with backoff; use fallback or partial results if necessary.

### Q6. How do you prevent duplicate work?

> Use caching, source/document deduplication, and idempotency keys.

### Q7. Why use a queue?

> To decouple task creation from execution, support horizontal scaling, handle bursts, and provide retry/failure isolation.

### Q8. How do you prevent infinite research?

> A static tree naturally limits the search space; additionally use node limits, retry limits, timeouts, and budgets.

### Q9. How do you handle conflicting sources?

> Rank source credibility, compare evidence, identify the conflict, and explicitly mention uncertainty in the final answer.

### Q10. How do you make it production-ready?

> Combine scalable workers, queues, caching, retries, observability, rate limits, source verification, citation validation, and evaluation.

---

# 18. Final Architecture Cheat Sheet

```text
                  ┌──────────────┐
                  │    Client    │
                  └──────┬───────┘
                         ↓
                  ┌──────────────┐
                  │ API Gateway  │
                  └──────┬───────┘
                         ↓
                  ┌──────────────┐
                  │  Controller  │
                  └──────┬───────┘
                         ↓
                  ┌──────────────┐
                  │ Static Tree  │
                  └──────┬───────┘
                         ↓
                  ┌──────────────┐
                  │    Queue     │
                  └──────┬───────┘
                         ↓
              ┌──────────┼──────────┐
              ↓          ↓          ↓
           Worker 1   Worker 2   Worker 3
              ↓          ↓          ↓
           Search      RAG        APIs
              └──────────┼──────────┘
                         ↓
                  ┌──────────────┐
                  │   Verifier   │
                  └──────┬───────┘
                         ↓
                  ┌──────────────┐
                  │  Aggregator  │
                  └──────┬───────┘
                         ↓
                  ┌──────────────┐
                  │ Synthesizer  │
                  └──────┬───────┘
                         ↓
                  Final + Citations
```

---

# 19. Ultimate Interview Formula

**Architecture:**  
`Static Tree → Fan-Out → Workers → Fan-In → Synthesizer`

**Performance:**  
`Parallel + Async + Cache + Early Stop`

**Scale:**  
`Queue + Stateless Workers + Horizontal Scaling`

**Accuracy:**  
`Source Ranking + Verification + Grounding + Citation Check`

**Reliability:**  
`Retry + Timeout + Circuit Breaker + DLQ + Idempotency`

**Cost:**  
`Caching + Small Models + Fixed Tree + Token/Search Budgets`

**Observability:**  
`Logs + Metrics + Tracing + Evaluation`

**Security:**  
`Auth + Rate Limit + Prompt-Injection Defense + Tool Isolation`

**Design Patterns:**  
`Composite + Strategy + Template Method + Fan-Out/Fan-In + Producer-Consumer + Retry + Circuit Breaker + Cache-Aside + Bulkhead`

## ⭐ One-Line Answer

> A **Tree-Based Static Deep Research Agent** is a predefined hierarchical research workflow that executes independent tasks in parallel, verifies and aggregates their results bottom-up, and uses a final synthesizer to produce a cited answer, providing predictable **cost, latency, scalability, reliability, and control**.
