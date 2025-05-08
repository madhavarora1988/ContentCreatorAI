# Content Creator AI

A comprehensive agentic content creation suite demonstrating common agent patterns using OpenAI and Pydantic. This project covers:

- Deterministic flows
- Handoffs and routing
- Agents as tools
- LLM-as-a-judge
- Parallelization
- Guardrails (input & output)

## Features
- **Blog post generation** (deterministic, professional style)
- **Social media summaries** (Twitter, LinkedIn)
- **SEO keyword extraction**
- **Quality judging** (LLM-as-a-judge)
- **Video script generation** (YouTube, TikTok)
- **Input and output guardrails** for safety and compliance

## Agentic Patterns Demonstrated

### 1. Deterministic Flows
Breaks down content creation into clear steps: topic analysis, structure, and content generation.

### 2. Handoffs and Routing
Routes content requests to specialized agents (e.g., Twitter, LinkedIn) based on user choice.

### 3. Agents as Tools
Uses agents as callable tools (e.g., SEO keyword extractor) within the main workflow.

### 4. LLM-as-a-Judge
A judge agent reviews the blog post and provides a quality score and feedback.

### 5. Parallelization
Runs multiple agents in parallel (e.g., social summaries, SEO, judge, and video scripts) for efficiency.

### 6. Guardrails
Input and output guardrail agents ensure topics and generated content are appropriate and compliant.

## Quickstart

1. **Install dependencies** (ensure you have Python 3.10+ and [uv](https://github.com/astral-sh/uv) installed):
   ```bash
   uv pip install -r pyproject.toml
   ```

2. **Run the main orchestrator script:**
   ```bash
   python main.py
   ```

3. **Follow the menu prompts** to select a pattern or run the full suite.

## Menu Options
- Deterministic Blog Creator
- Blog + Social Summaries (Blog, Tweet, LinkedIn)
- Blog + Social + SEO Keywords
- Blog + Social + SEO + Judge
- Blog Parallelization (Multiple Styles)
- Full Suite: Blog + Social + SEO + Judge + Parallel Video Scripts
- Full Suite + Guardrails (Input & Output)

## Folder Structure
- `content_creator_ai/` — Main codebase and orchestrator
- `agent_patterns/` — Reference agent pattern examples

## Extending
You can add new agent patterns, tools, or guardrails by following the modular structure in `main.py` and `content_creator_ai/`.

---

**Inspired by OpenAI agentic pattern demos.**
