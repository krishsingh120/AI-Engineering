# Agent2Agent (A2A) Protocol — Short Notes

## 1. What is A2A?

**A2A (Agent2Agent) Protocol** is an open standard that allows AI agents to communicate, collaborate, and delegate tasks to other AI agents.

The main goal is **agent interoperability**.

> **MCP = Agent ↔ Tool**  
> **A2A = Agent ↔ Agent**

A2A allows agents built with different frameworks, technologies, or hosted by different organizations to work together.

---

## 2. Why do we need A2A?

Without a common protocol, every agent may need a custom integration with every other agent.

```text
Agent A ── custom API ──> Agent B
Agent A ── custom API ──> Agent C
Agent B ── custom API ──> Agent D
```

This becomes difficult to maintain.

With A2A:

```text
Agent A ──┐
Agent B ──┼── A2A Standard
Agent C ──┤
Agent D ──┘
```

### Main benefits

- **Interoperability** — agents using different frameworks can communicate.
- **Collaboration** — agents can delegate and combine work.
- **Autonomy** — agents can perform specialized tasks independently.
- **Security** — communication can follow controlled authentication and authorization.
- **Modularity** — each agent can be developed and deployed separately.

---

# 3. Basic A2A Architecture

A2A commonly has two important roles:

### Client Node

The client/orchestrator agent starts communication.

It can:

- Discover another agent
- Send a task/request
- Receive status/results
- Continue the conversation when needed

### Server Node

The server node exposes an agent that can perform a task.

It:

- Receives requests
- Executes the agent
- Sends results/status back

### HLD

```text
                         User
                           |
                           v
                  +------------------+
                  |  Client Agent    |
                  |  / Client Node   |
                  +--------+---------+
                           |
                           | A2A Protocol
                           |
                           v
                  +------------------+
                  |  Server Agent    |
                  |  / Server Node   |
                  +--------+---------+
                           |
                           v
                  +------------------+
                  | Agent Tools/Data |
                  +------------------+
```

---

# 4. Multi-Agent HLD

Example: a Travel Assistant.

```text
                         User
                           |
                           v
                  +-------------------+
                  |  Travel Agent     |
                  |  Orchestrator     |
                  +---------+---------+
                            |
                     A2A Protocol
            +---------------+---------------+
            |               |               |
            v               v               v
     +-------------+ +-------------+ +-------------+
     | Flight      | | Hotel       | | Weather     |
     | Agent       | | Agent       | | Agent       |
     +-------------+ +-------------+ +-------------+
            |               |               |
            v               v               v
       Flight API       Hotel DB       Weather API
```

The Travel Agent does not need to implement every capability itself.

It delegates specialized work to other agents.

---

# 5. Agent-to-Agent Flow of Execution

Suppose the user asks:

> "Plan a trip to Mumbai."

### Step 1 — User request

```text
User
  |
  v
Travel Agent
```

### Step 2 — Agent decides what it needs

The Travel Agent determines:

```text
Need:
1. Flights
2. Hotel
3. Weather
```

### Step 3 — Agent-to-agent requests

```text
Travel Agent
    |
    +---- A2A ----> Flight Agent
    |
    +---- A2A ----> Hotel Agent
    |
    +---- A2A ----> Weather Agent
```

### Step 4 — Specialized agents work

```text
Flight Agent  → searches flights
Hotel Agent   → searches hotels
Weather Agent → checks weather
```

### Step 5 — Results return

```text
Flight Agent  ──> Travel Agent
Hotel Agent   ──> Travel Agent
Weather Agent ──> Travel Agent
```

### Step 6 — Final response

Travel Agent combines the results and responds to the user.

```text
User
  ↑
Travel Agent
  ↑
Results from multiple agents
```

---

# 6. Alice & Bob Example

Imagine two agents:

```text
Agent Alice                     Agent Bob
(Client Node)                  (Server Node)
     |                              |
     | ---- A2A Request ----------> |
     |                              |
     |                         Process Task
     |                              |
     | <---- A2A Response --------- |
     |                              |
```

For example:

```text
Alice:
"Can you summarize this document?"

Bob:
"Sure, I will process it."

Bob:
"Summary: ..."
```

The important point is that Alice does not need to know Bob's internal implementation.

---

# 7. Agent Discovery

Before communicating, a client may need to know:

- What agent is available?
- What tasks can it perform?
- How can I communicate with it?
- What authentication/security is required?

A2A supports standardized ways for agents to expose their capabilities.

Think:

```text
Client
  |
  | "What can you do?"
  v
Server Agent
  |
  | "I can analyze documents and return summaries."
  v
Client
```

---

# 8. Tasks

An A2A interaction can be thought of as a **task**.

Example:

```text
Task:
"Analyze this resume for a Backend Engineer role."
```

The task may have different states depending on the work:

```text
submitted
   ↓
working
   ↓
completed
```

For longer operations, the client may receive status updates instead of waiting for an immediate final answer.

---

# 9. Synchronous vs Asynchronous Communication

### Synchronous

Client waits for the result:

```text
Client
  |
  | Request
  v
Server Agent
  |
  | Result
  v
Client
```

Good for short tasks.

### Asynchronous

Server may continue working and provide updates/results later:

```text
Client
  |
  | Start Task
  v
Server Agent
  |
  | Status: Working
  |
  | Status: Working
  |
  | Final Result
  v
Client
```

Useful for long-running tasks.

---

# 10. Security

A2A is designed for communication between potentially independent agents.

Important concerns include:

- Authentication
- Authorization
- Secure communication
- Identity of the agent
- Access control
- Data privacy
- Trust between agents

Example:

```text
Client Agent
     |
     | Authentication
     v
Server Agent
     |
     | Authorization
     v
Accept / Reject Task
```

---

# 11. Framework Independence

One of the important ideas behind A2A is that agents do not need to use the same framework.

For example:

```text
LangGraph Agent
       |
       | A2A
       v
   Python Agent
       |
       | A2A
       v
Another Agent built using a different framework
```

The protocol provides a common communication layer.

---

# 12. A2A vs MCP

This is an important interview topic.

| Feature | MCP | A2A |
|---|---|---|
| Main communication | Agent ↔ Tool | Agent ↔ Agent |
| Purpose | Access tools/data | Agent collaboration |
| Example | Agent → Database | Agent → Research Agent |
| Focus | Capability access | Agent interoperability |
| Typical use | Search, DB, APIs, files | Delegation, collaboration |

### Simple memory trick

```text
MCP → "Give me a tool."

A2A → "Ask another agent to do the work."
```

---

# 13. A2A + MCP Together

They are **not competitors**.

They can work together.

```text
                         User
                           |
                           v
                    Orchestrator
                       Agent
                     /       \
                  A2A         A2A
                   /           \
                  v             v
          Research Agent    Coding Agent
               |                 |
              MCP               MCP
           /  |  \            /  |  \
          DB API Search      Git DB Tools
```

### Example

The Orchestrator uses **A2A** to ask the Research Agent for research.

The Research Agent uses **MCP** to access a search tool.

So:

```text
A2A = communication between agents

MCP = communication between agent and tools
```

---

# 14. Hands-on Code Concept

The video mentions a Python `ChatAgent` served through an A2A framework.

The conceptual server looks like:

```python
# Server Agent

agent = ChatAgent()

# Expose agent through A2A
server = A2AServer(agent)

server.start()
```

The client conceptually does:

```python
# Client Node

client = A2AClient(server_url)

response = client.send_task(
    "Hello, Agent Bob!"
)

print(response)
```

The exact APIs depend on the A2A framework/library used in the tutorial.

The important architecture is:

```text
Client Python Program
        |
        | A2A Request
        v
A2A Server
        |
        v
ChatAgent
        |
        v
Response
        |
        | A2A Response
        v
Client
```

---

# 15. End-to-End HLD

```text
                         +-------------+
                         |    User     |
                         +------+------+
                                |
                                v
                    +----------------------+
                    | Orchestrator Agent   |
                    |    Client Node       |
                    +----------+-----------+
                               |
                         A2A Protocol
                 +-------------+-------------+
                 |             |             |
                 v             v             v
          +-----------+ +-----------+ +-----------+
          | Research  | | Coding    | | Data      |
          | Agent     | | Agent     | | Agent     |
          | Server    | | Server    | | Server    |
          +-----+-----+ +-----+-----+ +-----+-----+
                |             |             |
               MCP           MCP           MCP
                |             |             |
                v             v             v
             Tools         Tools         Tools
```

---

# 16. Flow of Execution — Interview Version

```text
1. User sends request
        ↓
2. Orchestrator Agent analyzes the task
        ↓
3. It discovers/selects suitable agents
        ↓
4. Sends task using A2A
        ↓
5. Remote agent authenticates/accepts task
        ↓
6. Remote agent performs the task
        ↓
7. Remote agent may use MCP/tools internally
        ↓
8. Result/status is returned through A2A
        ↓
9. Orchestrator combines results
        ↓
10. Final response is sent to user
```

---

# 17. Key Terms to Remember

### A2A
Standard for **agent-to-agent communication**.

### Client Node
The side that **requests/delegates work**.

### Server Node
The side that **provides an agent/capability**.

### Agent Discovery
Finding what an agent can do and how to communicate with it.

### Task
A unit of work requested from another agent.

### Status
Information about the task's progress.

### Interoperability
Different agents/frameworks can work together.

### Delegation
One agent asks another agent to perform specialized work.

---

# 18. A2A vs API

A normal API might look like:

```text
Application → /search → Search Service
```

A2A is designed around **agents and agent capabilities**, where the remote side can be an autonomous agent capable of handling a task rather than just returning a fixed API response.

```text
Agent A → A2A → Agent B
```

Agent B can reason, use its own tools, perform multi-step work, and return the result.

---

# 19. Interview Answer

### What is A2A?

> **A2A, or Agent2Agent Protocol, is an open standard that enables AI agents to communicate, discover capabilities, delegate tasks, and exchange results across different frameworks and environments.**

### Why A2A?

> **It solves interoperability in multi-agent systems, allowing independently built agents to collaborate without requiring custom integrations for every agent pair.**

### A2A vs MCP?

> **MCP standardizes how agents interact with tools and external data, while A2A standardizes how agents communicate and collaborate with other agents.**

---

# 20. One-Line Mental Model

```text
MCP:
Agent ──────────> Tools

A2A:
Agent ──────────> Agent

Together:
Agent ── A2A ──> Agent ── MCP ──> Tools
```

This is the core concept you need to remember for **Agentic AI interviews**.
