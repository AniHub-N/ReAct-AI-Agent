#  ReAct AI Agent — Reasoning + Acting System Built From Scratch

A modular AI agent that **reasons, takes actions, validates itself, and handles failure**, inspired by the ReAct paradigm.

This project is based on the paper:

> **ReAct: Synergizing Reasoning and Acting in Language Models**  
> *Published as a conference paper at ICLR 2023*
(Refer to it here : https://arxiv.org/pdf/2210.03629)

This project is not just about getting answers — it is about **controlling how an AI system thinks, acts, and recovers when things go wrong**.

---

##  Overview

**Traditional LLM usage**

Prompt → Answer


**This system implements**

Thought → Action → Observation → Thought → Final Answer


The agent:
- reasons step-by-step  
- uses external tools  
- validates outputs  
- retries on failure  
- manages its own memory  

---

##  Core Features

###  ReAct Reasoning Loop
- Structured reasoning pipeline  
- Enforced format: Thought → Action → Observation  

---

###  Tool Integration
- `search` → external knowledge (DuckDuckGo API)  
- `calculator` → safe expression evaluation  

---

###  Robust Validation Layer
- Invalid format detection  
- Tool name normalization  
- Action/Input enforcement  
- Prevention of malformed outputs  

---

###  Failure-Aware Control Loop
- Detects repeated failures (refusals, bad outputs)  
- Stops intelligently instead of looping forever  
- Supports retry-based correction  

---

###  Memory Management (Sliding Window)
- Maintains recent reasoning context only  
- Prevents context explosion  
- Improves performance + reasoning clarity  

---

###  Observation Quality Control
- Detects unreliable or low-quality tool outputs  
- Rejects misleading data before it corrupts reasoning  

---

###  Conflict Detection (Multi-Step Reasoning)
- Identifies contradictory observations  
- Avoids blindly trusting single tool outputs  

---

###  Self-Critique Layer (Self-Refine)
- Evaluates final answer  
- Improves response if necessary  
- Includes validation of critic output (no blind trust)

---

###  Layered Architecture


LLM → Parser → Validator → Tool → Observation → Memory → Loop → Critic → Validator


Every layer is **explicitly controlled**, not blindly trusted.

---

##  Project Structure

```bash
ReAct-Agent/
│
├── agent.py          # Core agent loop + control logic
├── parser.py         # Parses LLM outputs into structured actions
├── tools.py          # Tool implementations 
├── llm.py            
├── main.py           
├── requirements.txt
└── README.md

```
---

##  Example Run


Thought: I need to find the CEO of OpenAI
Action: search
Action Input: CEO of OpenAI

Observation: Sam Altman is the CEO of OpenAI

Thought: I now have the answer
Final Answer: Sam Altman


---

##  Key Engineering Challenges (and What We Solved)

### 1. LLM Output is Unreliable

**Problem:**
- Outputs malformed actions  
- Combines steps incorrectly  
- Hallucinates structure  

**Solution:**
- Built a strict parser  
- Enforced protocol rules  
- Rejected invalid outputs and retried  

---

### 2. Infinite Loops

**Problem:**
- Agent keeps retrying forever  
- No notion of progress  

**Solution:**
- Added failure counter  
- Detected repeated refusal patterns  
- Introduced intelligent stopping  

---

### 3. Tools Return Incorrect Data

**Problem:**
- External APIs give wrong or outdated info  
- Agent trusts them blindly  

**Solution:**
- Observation validation layer  
- Rejected weak or conflicting results  
- Introduced conflict detection  

---

### 4. Premature Final Answers

**Problem:**
- LLM gives answer without using tools  

**Solution:**
- Enforced:

Action → Observation → THEN Final Answer


---

### 5. Context Explosion

**Problem:**
- Context grows indefinitely  
- Slows system + reduces accuracy  

**Solution:**
- Sliding window memory  
- Retains only relevant steps  

---

### 6. Critic Hallucination

**Problem:**
- Self-critique can generate incorrect improvements  

**Solution:**
- Added critic validation layer  
- Only accept clean, meaningful improvements  

---

### 7. Conflicting Information

**Problem:**
- Different tool calls return different answers  

**Solution:**
- Detect contradictions  
- Avoid premature conclusions  
- Retry with better queries  

---

## Key Insights

> LLMs are not reliable executors — they are suggestion generators.  
> Tools can lie. Reasoning must verify.  
> Structure and control matter more than prompting.  
> Reliability > correctness in one-shot.  
> A good agent knows when to **retry, adapt, or stop**.

---

## Future Improvements

- 🔹 Tool selection policy (intelligent routing)  
- 🔹 Multi-query search + ranking  
- 🔹 Long-term memory (fact storage)  
- 🔹 Reflection / planning layer  
- 🔹 Multi-agent collaboration  

---

## What This Project Demonstrates

This project shows:

- understanding of **AI system design**  
- ability to build **modular architectures**  
- handling of **real-world failure modes**  
- bridging theory (ReAct) → practical implementation  

---

## Final Thought

 Building AI systems is not about generating answers.  
 It’s about **designing systems that can handle uncertainty, failure, and imperfect information**.

---

## ⭐ If you found this interesting

Feel free to:
- ⭐ Star the repo  
- 🍴 Fork and experiment  
- 💬 Share feedback and insights
