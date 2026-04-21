---
title: "Pydantic AI Tutorial 2026: Type-Safe AI Agents in Python"
date: 2026-04-21
tags: ["pydantic-ai", "python", "ai-agents", "llm", "type-safety", "structured-outputs"]
description: "A hands-on tutorial covering Pydantic AI from setup to production: structured outputs, tool calling, dependency injection, multi-agent patterns, testing, and observability for type-safe AI agents in Python."
draft: false
cover:
  image: "/images/pydantic-ai-tutorial-2026.png"
  alt: "Pydantic AI Tutorial 2026: Type-Safe AI Agents in Python"
schema:
  type: "TechArticle"
  headline: "Pydantic AI Tutorial 2026: Type-Safe AI Agents in Python"
  description: "A hands-on tutorial covering Pydantic AI from setup to production: structured outputs, tool calling, dependency injection, multi-agent patterns, testing, and observability for type-safe AI agents in Python."
  author: "Baeseokjae"
  datePublished: "2026-04-21"
---

If you have spent any time building applications around LLMs, you know the pain: parsing raw text output, praying the model returns valid JSON, and debugging silent failures in production. Pydantic AI, built by the same team behind Pydantic and FastAPI, applies the type-safety and validation that made FastAPI the standard for Python web APIs to the world of AI agents.

This tutorial walks through building type-safe AI agents with Pydantic AI, from first setup to production deployment. Every code example runs. Every pattern is one you would use in a real application.

## What is Pydantic AI?

Pydantic AI is an agent framework for Python that enforces type safety at every layer: model inputs, tool definitions, structured outputs, and dependency injection. It is model-agnostic, supporting 20+ providers including OpenAI, Anthropic, Gemini, DeepSeek, Groq, Ollama, and Azure AI Foundry.

The framework exists because the Pydantic team noticed something: Pydantic had already become the validation layer under most of the AI ecosystem (OpenAI SDK, Anthropic SDK, LangChain, LlamaIndex, CrewAI, Google ADK). Building the agent framework on top of that same validation infrastructure was a natural step.

### Why not just use LangChain or CrewAI?

This is the question most developers ask first. Here is a direct comparison:

| Feature | Pydantic AI | LangChain | CrewAI |
|---|---|---|---|
| Type safety | Full static type checking, mypy-compatible | Partial; many dynamic patterns | Partial; role-based but loosely typed |
| Validation | Automatic Pydantic validation on all inputs/outputs | Optional; requires manual validation chains | Optional; relies on structured parsers |
| Dependency injection | Built-in `deps_type` with full type inference | None built-in; pass context manually | Limited; crew-level context sharing |
| Structured outputs | First-class; BaseModel as `result_type` | Requires output parsers; error-prone | Requires output parsers |
| Model support | 20+ providers, same API | 20+ providers, same API | OpenAI-primary, others secondary |
| Observability | Built-in Logfire (OpenTelemetry) | Requires LangSmith or manual integration | Limited |
| Evals | Built-in eval framework | Requires external tools | Minimal |
| Learning curve | Low if you know Pydantic/FastAPI | Steep; many abstractions | Medium; role-based concepts |
| Philosophy | Minimal abstractions, explicit code | Abstract chains and agents | Role-based autonomous agents |

The key difference: Pydantic AI does not hide what happens. You see the model calls, the tool invocations, the validation steps. There is no magic chain abstraction obscuring the flow. For production systems where you need to understand and debug every step, this matters.

### The FastAPI-of-AI promise

FastAPI succeeded because it made the common case (define a route, validate input, return typed output) trivially easy while keeping the hard case possible. Pydantic AI aims for the same: define an agent, declare its output type, register its tools, and the framework handles validation, retries, and model communication. You write regular Python functions with regular Python type hints. The framework does the rest.

## Setting Up Your First Pydantic AI Project

### Installation and prerequisites

```bash
pip install pydantic-ai
```

Pydantic AI requires Python 3.10+. The package pulls in `pydantic`, `pydantic-graph`, and provider-specific dependencies as optional extras:

```bash
# Install with specific provider support
pip install pydantic-ai[openai]
pip install pydantic-ai[anthropic]
pip install pydantic-ai[groq]

# Or install all providers
pip install pydantic-ai[all]
```

### Configuring model providers

Set your API keys as environment variables:

```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPHIC_API_KEY="sk-ant-..."
export GEMINI_API_KEY="AIza..."
```

Pydantic AI detects keys from the environment automatically. You can also pass them in code, but environment variables are the standard practice.

### Project structure

A minimal but organized project looks like this:

```
my-agent/
├── pyproject.toml
├── .env
├── src/
│   └── my_agent/
│       ├── __init__.py
│       ├── agent.py
│       ├── models.py
│       ├── tools.py
│       └── deps.py
└── tests/
    └── test_agent.py
```

The separation of `models.py` (Pydantic schemas), `tools.py` (tool functions), and `deps.py` (dependency definitions) keeps things clean as the project grows.

## Building Your First AI Agent

### Creating an Agent

The simplest agent takes a system prompt and a model:

```python
from pydantic_ai import Agent

agent = Agent(
    "openai:gpt-4o",
    system_prompt="You are a helpful coding assistant. Answer concisely.",
)
```

The model string format is `provider:model_name`. Supported prefixes include `openai:`, `anthropic:`, `gemini:`, `groq:`, `ollama:`, `deepseek:`, and `bedrock:`.

### Running your first query

```python
result = agent.run_sync("What is the difference between a list and a tuple in Python?")
print(result.data)
```

`run_sync` is the simplest execution method. It blocks until the model responds. `result.data` contains the model's output as a string by default.

### Streaming responses

For interactive applications, streaming is essential:

```python
async def stream_response():
    async with agent.run_stream("Explain async/await in Python") as stream:
        async for chunk in stream.stream_text():
            print(chunk, end="", flush=True)
```

The async API mirrors the sync API: `agent.run()` is the async equivalent of `run_sync()`, and `agent.run_stream()` returns an async context manager that yields text chunks as they arrive.

## Structured Outputs with Pydantic Models

This is where Pydantic AI separates itself from frameworks that treat structured output as an afterthought. Instead of parsing raw model output, you declare the expected shape as a Pydantic model and the framework guarantees the output conforms.

### Defining BaseModel classes for type-safe responses

```python
from pydantic import BaseModel, Field
from pydantic_ai import Agent

class CodeReview(BaseModel):
    summary: str = Field(description="Brief summary of the code change")
    issues: list[str] = Field(default_factory=list, description="List of issues found")
    severity: str = Field(description="Overall severity: low, medium, high, critical")
    suggested_fix: str | None = Field(default=None, description="Suggested fix if issues found")

review_agent = Agent(
    "openai:gpt-4o",
    result_type=CodeReview,
    system_prompt="You are a code reviewer. Analyze the provided code and return a structured review.",
)

result = review_agent.run_sync("""
Review this Python function:
def get_user(id):
    user = db.query("SELECT * FROM users WHERE id = " + id)
    return user
""")

print(result.data.summary)
print(result.data.issues)       # list of issues
print(result.data.severity)     # "high" or "critical" — SQL injection
print(result.data.suggested_fix) # parameterized query suggestion
```

The model output is automatically validated against the `CodeReview` schema. If the LLM returns a severity value that is not a string, or omits a required field, Pydantic raises a `ValidationError` before the result reaches your code.

### Automatic validation and retry on invalid output

Pydantic AI does not just validate and crash. When the model returns invalid data, the framework automatically retries the query, informing the model of the validation error so it can self-correct:

```python
agent = Agent(
    "openai:gpt-4o",
    result_type=CodeReview,
    retries=3,  # Retry up to 3 times on validation failure
)
```

The retry mechanism sends the validation error back to the model as additional context. In practice, models correct themselves on the first retry in most cases, especially with clear field descriptions. Setting `retries=3` handles edge cases.

### Complex nested models

Real-world data extraction often involves nested structures:

```python
class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str

class Company(BaseModel):
    name: str
    industry: str
    headquarters: Address
    employee_count: int
    founded_year: int

class ExtractionResult(BaseModel):
    companies: list[Company]
    confidence: float = Field(ge=0.0, le=1.0, description="Extraction confidence 0-1")

extraction_agent = Agent(
    "anthropic:claude-sonnet-4-20250514",
    result_type=ExtractionResult,
    system_prompt="Extract company information from the provided text.",
)

result = extraction_agent.run_sync("""
Tesla is headquartered at 3500 Deer Creek Road, Palo Alto, CA 94304.
Founded in 2003, it has approximately 140,000 employees and operates in the automotive industry.
SpaceX, founded 2002, is based at 1 Rocket Road, Hawthorne, CA 90250,
with about 13,000 employees in the aerospace industry.
""")

for company in result.data.companies:
    print(f"{company.name}: {company.headquarters.city}, {company.industry}")
```

Nested models work exactly as they do in regular Pydantic usage. The framework passes the full JSON schema (including nested definitions) to the model as the output format specification.

## Tool Calling and Function Integration

Tools are how agents interact with the outside world. Pydantic AI makes tool registration explicit and type-safe.

### Registering tools with the @agent.tool decorator

```python
from pydantic_ai import Agent

weather_agent = Agent(
    "openai:gpt-4o",
    system_prompt="You are a weather assistant. Use tools to get weather data.",
)

@weather_agent.tool
def get_temperature(ctx, city: str) -> str:
    """Get the current temperature for a city.

    Args:
        city: The city name, e.g. 'New York'

    Returns:
        Current temperature as a string like '72°F'
    """
    # In production, call a real weather API
    temperatures = {"New York": "58°F", "London": "48°F", "Tokyo": "65°F"}
    return temperatures.get(city, "Temperature data unavailable")

@weather_agent.tool
def get_forecast(ctx, city: str, days: int = 3) -> str:
    """Get a multi-day weather forecast for a city.

    Args:
        city: The city name
        days: Number of forecast days (1-7), defaults to 3

    Returns:
        Forecast summary string
    """
    return f"{days}-day forecast for {city}: Partly cloudy with occasional rain"
```

The `ctx` parameter is the run context; we will cover it in the dependency injection section. The docstring is critical — the LLM uses it to decide when and how to call the tool. Clear parameter descriptions lead to correct tool invocation.

### How LLMs choose which tool to call

When a user asks "What is the weather in Tokyo tomorrow?", the model sees the available tool schemas and docstrings, determines that `get_forecast(city="Tokyo", days=1)` is the right call, and the framework executes it. The result feeds back to the model, which then formulates its response. This happens transparently — your code calls `agent.run_sync()`, and tool calls happen as needed within the agent loop.

### Runtime tool context

The `ctx` parameter carries the dependencies and run-time state:

```python
from pydantic_ai import RunContext

@weather_agent.tool
def get_temperature(ctx: RunContext, city: str) -> str:
    # Access dependencies through ctx.deps
    api_key = ctx.deps
    # Use api_key to call real weather service
    return f"72°F (via API)"
```

We will cover dependency injection in depth next.

## Dependency Injection for Type-Safe Context

Hard-coded API keys, global database connections, and singleton patterns make agents hard to test and hard to run in different environments. Pydantic AI solves this with typed dependency injection.

### What is deps_type and why it matters

The `deps_type` parameter on an Agent declares the type of dependencies that tools can access. This is not a dictionary or a loose bag of values — it is a fully typed Pydantic model, and mypy checks that tools use it correctly.

```python
from pydantic_ai import Agent, RunContext
from pydantic import BaseModel

class DatabaseDeps(BaseModel):
    connection_string: str
    api_key: str
    cache_enabled: bool = True

db_agent = Agent(
    "openai:gpt-4o",
    deps_type=DatabaseDeps,
    system_prompt="You are a database assistant. Use tools to query the database.",
)

@db_agent.tool
def execute_query(ctx: RunContext[DatabaseDeps], query: str) -> str:
    """Execute a SQL query against the database.

    Args:
        query: SQL query to execute

    Returns:
        Query results as a formatted string
    """
    conn_str = ctx.deps.connection_string
    # Use conn_str to connect and execute
    return f"Results from {conn_str}: (mock data)"

@db_agent.tool
def check_cache(ctx: RunContext[DatabaseDeps], key: str) -> str | None:
    """Check if a query result is cached.

    Args:
        key: Cache key to look up

    Returns:
        Cached result or None
    """
    if not ctx.deps.cache_enabled:
        return None
    return f"Cached result for {key}"
```

Note the `RunContext[DatabaseDeps]` type annotation. Mypy knows that `ctx.deps` is a `DatabaseDeps` instance, so `ctx.deps.connection_string` is a `str` and `ctx.deps.cache_enabled` is a `bool`. If you try to access a property that does not exist on `DatabaseDeps`, you get a type error at write time, not a runtime `AttributeError` in production.

### Running with dependencies

```python
deps = DatabaseDeps(
    connection_string="postgresql://localhost:5432/mydb",
    api_key="sk-...",
    cache_enabled=True,
)

result = db_agent.run_sync("Show me the top 5 customers by revenue", deps=deps)
print(result.data)
```

Dependencies are passed per-run, not per-agent. This means the same agent definition can run with different dependencies — production credentials, test mocks, development configs — without modification.

### Practical example: SQL-backed agent

Here is a more complete pattern for a database agent:

```python
from pydantic_ai import Agent, RunContext
from pydantic import BaseModel
import psycopg2

class SQLDeps(BaseModel):
    db_url: str
    max_rows: int = 100

    class Config:
        arbitrary_types_allowed = True

sql_agent = Agent(
    "openai:gpt-4o",
    deps_type=SQLDeps,
    result_type=str,
    system_prompt="You are a SQL expert. Generate and execute safe SELECT queries only.",
)

@sql_agent.tool
def run_query(ctx: RunContext[SQLDeps], sql: str) -> str:
    """Execute a SELECT query and return results.

    Args:
        sql: A SELECT query to execute

    Returns:
        Results as a formatted table string
    """
    if not sql.strip().upper().startswith("SELECT"):
        return "Error: Only SELECT queries are allowed"

    conn = psycopg2.connect(ctx.deps.db_url)
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchmany(ctx.deps.max_rows)
        columns = [desc[0] for desc in cursor.description]
        return str(columns) + "\n" + "\n".join(str(row) for row in rows)
    finally:
        conn.close()

# Production
prod_deps = SQLDeps(db_url="postgresql://prod-host/analytics", max_rows=50)
# Testing
test_deps = SQLDeps(db_url="postgresql://localhost/test_db", max_rows=10)
```

The type safety flows through: `ctx.deps.max_rows` is typed as `int`, `ctx.deps.db_url` is typed as `str`. No casting, no `Any`, no guessing.

## Multi-Agent Patterns and Orchestration

Real applications often need multiple agents with different specializations. Pydantic AI supports agent delegation natively.

### Delegating tasks between agents

```python
from pydantic_ai import Agent
from pydantic import BaseModel

class ResearchResult(BaseModel):
    topic: str
    key_findings: list[str]
    sources: list[str]

class SummaryResult(BaseModel):
    title: str
    summary: str
    key_points: list[str]

research_agent = Agent(
    "openai:gpt-4o",
    result_type=ResearchResult,
    system_prompt="You are a research assistant. Find key information about the given topic.",
)

summary_agent = Agent(
    "anthropic:claude-sonnet-4-20250514",
    result_type=SummaryResult,
    system_prompt="You are a summarizer. Create concise summaries of research findings.",
)

# The orchestrator delegates to specialized agents
@summary_agent.tool
def research_topic(ctx, topic: str) -> str:
    """Research a topic using the research agent.

    Args:
        topic: Topic to research

    Returns:
        Research findings as a structured string
    """
    result = research_agent.run_sync(f"Research: {topic}")
    r = result.data
    return f"Topic: {r.topic}\nFindings: {'; '.join(r.key_findings)}\nSources: {'; '.join(r.sources)}"
```

When the summary agent needs research data, it calls the `research_topic` tool, which invokes the research agent. The result flows back to the summary agent as tool output.

### Agent handoff patterns

For more explicit orchestration, you can use a coordinator agent that decides which specialist to invoke:

```python
from pydantic_ai import Agent
from pydantic import BaseModel
from enum import Enum

class Department(str, Enum):
    sales = "sales"
    support = "support"
    billing = "billing"

class RoutingDecision(BaseModel):
    department: Department
    reasoning: str

router_agent = Agent(
    "openai:gpt-4o",
    result_type=RoutingDecision,
    system_prompt="Route the customer query to the correct department.",
)

support_agent = Agent("openai:gpt-4o", system_prompt="You are a technical support agent.")
sales_agent = Agent("openai:gpt-4o", system_prompt="You are a sales representative.")
billing_agent = Agent("openai:gpt-4o", system_prompt="You are a billing specialist.")

agents = {
    Department.sales: sales_agent,
    Department.support: support_agent,
    Department.billing: billing_agent,
}

def handle_query(query: str) -> str:
    routing = router_agent.run_sync(query)
    specialist = agents[routing.data.department]
    result = specialist.run_sync(query)
    return result.data
```

This pattern is composable: each specialist can itself have tools that call other agents. The type system ensures that routing decisions are constrained to valid departments.

## Testing and Evaluating Your Agents

Testing non-deterministic systems is fundamentally different from testing regular software. Pydantic AI provides two mechanisms: deterministic test helpers and a built-in eval framework.

### Writing deterministic tests for non-deterministic agents

The `TestModel` replaces the real LLM with a configurable mock that returns predictable responses:

```python
import pytest
from pydantic_ai import Agent
from pydantic_ai.models.test import TestModel

class Greeting(BaseModel):
    message: str
    tone: str

agent = Agent(result_type=Greeting, system_prompt="Generate greetings")

def test_greeting_structure():
    # TestModel returns predictable output conforming to result_type
    with agent.override(model=TestModel()):
        result = agent.run_sync("Say hello")
        assert isinstance(result.data, Greeting)
        assert isinstance(result.data.message, str)
        assert isinstance(result.data.tone, str)
```

`TestModel` generates output that conforms to the `result_type` schema without hitting any API. This lets you test your tool logic, dependency injection, and output validation without network calls or API costs.

### Mock model responses for reproducible testing

For more control over what the mock model returns, use `FunctionModel`:

```python
from pydantic_ai.models.function import FunctionModel

def mock_response(messages, tools, deps):
    return Greeting(message="Hello, world!", tone="friendly")

def test_greeting_with_known_output():
    model = FunctionModel(mock_response)
    with agent.override(model=model):
        result = agent.run_sync("Say hello")
        assert result.data.message == "Hello, world!"
        assert result.data.tone == "friendly"
```

`FunctionModel` takes a function that receives the agent's messages, tools, and dependencies, and returns a known result. This is how you test specific edge cases: invalid tool responses, unexpected model output, empty results.

### Built-in eval framework

Pydantic AI includes an eval system for measuring agent quality over time:

```python
from pydantic_ai import Agent
from pydantic_ai.eval import EvalCase, evaluate

agent = Agent("openai:gpt-4o", system_prompt="Answer math questions accurately.")

cases = [
    EvalCase(
        inputs="What is 15 * 23?",
        expected_output="345",
    ),
    EvalCase(
        inputs="What is the square root of 144?",
        expected_output="12",
    ),
]

report = evaluate(agent, cases)
for case_result in report.case_results:
    print(f"Input: {case_result.inputs}")
    print(f"Expected: {case_result.expected_output}")
    print(f"Actual: {case_result.output}")
    print(f"Correct: {case_result.correct}")
```

Evals run against real models (not mocks) and measure whether the agent produces expected outputs. They track correctness over time, so you can detect regressions when you change prompts, tools, or models.

## Observability: Debugging with Pydantic Logfire

Agent applications are opaque by default: a user asks a question, something happens inside the model, and an answer comes out. When the answer is wrong, you need to see what happened.

### Integrating Logfire for real-time agent tracing

```python
import logfire
from pydantic_ai import Agent

logfire.configure(
    send_to_logfire=True,
    token="your-logfire-token",
)

agent = Agent("openai:gpt-4o", system_prompt="You are a helpful assistant.")
result = agent.run_sync("Explain recursion")
```

With Logfire configured, every model call, tool invocation, validation step, and retry is traced and visible in the Logfire dashboard. You see the full conversation including system prompts, tool calls, tool results, model reasoning, and final output.

### OpenTelemetry with alternative backends

If you use a different observability stack (Jaeger, Datadog, Honeycomb, Graf Tempo), Pydantic AI emits OpenTelemetry spans that any OTel-compatible backend can receive:

```python
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

provider = TracerProvider()
provider.add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint="http://localhost:4317"))
)
```

Pydantic AI's tracing is built on OpenTelemetry, so you are not locked into Logfire. The spans include model name, token counts, latency, and whether retries occurred.

## Production Best Practices

### Error handling and fallback models

Models fail. Rate limits hit. APIs go down. Production agents need fallback strategies:

```python
from pydantic_ai import Agent
from pydantic_ai.models import Model

primary_agent = Agent(
    "openai:gpt-4o",
    system_prompt="You are a helpful assistant.",
)

fallback_agent = Agent(
    "anthropic:claude-sonnet-4-20250514",
    system_prompt="You are a helpful assistant.",
)

async def run_with_fallback(prompt: str, deps=None):
    try:
        return await primary_agent.run(prompt, deps=deps)
    except Exception as e:
        # Log the failure
        print(f"Primary model failed: {e}")
        return await fallback_agent.run(prompt, deps=deps)
```

For more sophisticated fallback, Pydantic AI supports the model gateway (covered below).

### Rate limiting and concurrency management

```python
import asyncio

async def run_concurrent_queries(queries: list[str], max_concurrent: int = 5):
    semaphore = asyncio.Semaphore(max_concurrent)

    async def bounded_run(query):
        async with semaphore:
            return await agent.run(query)

    results = await asyncio.gather(*[bounded_run(q) for q in queries])
    return results
```

Use semaphores or connection pools to avoid overwhelming model providers. Rate limit errors (429) are common when running many concurrent agent invocations.

### Model gateway for cost optimization

Pydantic AI includes a gateway feature that can route requests to different models based on cost, latency, or task complexity:

```python
# Use a cheaper model for simple tasks, expensive model for complex ones
simple_agent = Agent("groq:llama-3.3-70b-versatile", system_prompt="Answer simple questions.")
complex_agent = Agent("openai:gpt-4o", system_prompt="Answer complex questions.")
```

The gateway pattern — routing to different models based on request characteristics — is something you implement at the application layer. The framework's model-agnostic design makes this straightforward: swap the model string, keep everything else identical.

## Complete Project: Build a Production-Ready AI Agent

Let us combine all the concepts into a single project: a customer support agent that categorizes tickets, looks up information, and returns structured responses.

```python
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from enum import Enum

# --- Models ---

class Category(str, Enum):
    technical = "technical"
    billing = "billing"
    general = "general"

class TicketResponse(BaseModel):
    category: Category
    response: str
    escalation_needed: bool = Field(
        default=False,
        description="Whether this ticket needs human escalation"
    )
    confidence: float = Field(ge=0.0, le=1.0)

# --- Dependencies ---

class SupportDeps(BaseModel):
    knowledge_base: dict[str, str] = Field(
        default_factory=dict,
        description="Knowledge base articles keyed by topic"
    )
    customer_tier: str = Field(description="Customer tier: free, pro, enterprise")

# --- Tools ---

support_agent = Agent(
    "openai:gpt-4o",
    deps_type=SupportDeps,
    result_type=TicketResponse,
    system_prompt="""You are a customer support agent. Classify tickets and provide
    helpful responses. Use tools to look up information before responding.""",
    retries=3,
)

@support_agent.tool
def search_knowledge_base(ctx: RunContext[SupportDeps], topic: str) -> str:
    """Search the knowledge base for information on a topic.

    Args:
        topic: Topic to search for

    Returns:
        Relevant knowledge base article or 'No results found'
    """
    return ctx.deps.knowledge_base.get(topic.lower(), "No results found")

@support_agent.tool
def check_escalation_rules(ctx: RunContext[SupportDeps], issue_type: str) -> str:
    """Check if this issue type requires escalation based on customer tier.

    Args:
        issue_type: Type of issue (technical, billing, general)

    Returns:
        Escalation guidance
    """
    if ctx.deps.customer_tier == "enterprise":
        return "Enterprise customers: escalate any billing or critical technical issue"
    if ctx.deps.customer_tier == "pro":
        return "Pro customers: escalate billing disputes only"
    return "Free tier: no automatic escalation"

# --- Running the agent ---

deps = SupportDeps(
    knowledge_base={
        "api authentication": "API keys are found in Settings > API Keys. Rotate keys every 90 days.",
        "rate limits": "Free tier: 100 req/hr. Pro: 1000 req/hr. Enterprise: 10000 req/hr.",
        "billing cycle": "Billing occurs on the 1st of each month. Pro tier is $49/mo.",
    },
    customer_tier="pro",
)

result = support_agent.run_sync(
    "I'm getting rate limit errors even though I'm on the Pro plan. My API calls are failing.",
    deps=deps,
)

# --- Output ---

print(f"Category: {result.data.category}")
print(f"Response: {result.data.response}")
print(f"Escalation: {result.data.escalation_needed}")
print(f"Confidence: {result.data.confidence}")
```

### Testing the complete agent

```python
from pydantic_ai.models.test import TestModel

def test_support_agent_structure():
    test_deps = SupportDeps(
        knowledge_base={"api authentication": "API keys are in Settings"},
        customer_tier="free",
    )
    with support_agent.override(model=TestModel()):
        result = support_agent.run_sync("How do I find my API key?", deps=test_deps)
        assert isinstance(result.data, TicketResponse)
        assert isinstance(result.data.category, Category)
        assert 0.0 <= result.data.confidence <= 1.0

def test_escalation_for_enterprise():
    enterprise_deps = SupportDeps(
        knowledge_base={},
        customer_tier="enterprise",
    )
    model = FunctionModel(lambda messages, tools, deps: TicketResponse(
        category=Category.billing,
        response="Escalating billing issue for enterprise customer",
        escalation_needed=True,
        confidence=0.95,
    ))
    with support_agent.override(model=model):
        result = support_agent.run_sync("I was charged twice", deps=enterprise_deps)
        assert result.data.escalation_needed is True
```

### FastAPI integration

Serving the agent behind an API endpoint:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class SupportRequest(BaseModel):
    message: str
    customer_tier: str
    knowledge_base: dict[str, str] | None = None

class SupportResponse(BaseModel):
    category: str
    response: str
    escalation_needed: bool
    confidence: float

@app.post("/support", response_model=SupportResponse)
async def handle_support(request: SupportRequest):
    deps = SupportDeps(
        knowledge_base=request.knowledge_base or get_default_knowledge_base(),
        customer_tier=request.customer_tier,
    )
    result = await support_agent.run(request.message, deps=deps)
    return SupportResponse(
        category=result.data.category.value,
        response=result.data.response,
        escalation_needed=result.data.escalation_needed,
        confidence=result.data.confidence,
    )
```

FastAPI and Pydantic AI share the same validation foundation. The request model, the dependency model, and the result model are all Pydantic `BaseModel` classes. FastAPI validates the incoming request. Pydantic AI validates the model output. There is no impedance mismatch.

## Resources and Next Steps

**Official documentation**: [ai.pydantic.dev](https://ai.pydantic.dev/) — covers every provider, tool, and pattern in detail. Start here for anything not covered in this tutorial.

**GitHub repository**: [github.com/pydantic/pydantic-ai](https://github.com/pydantic/pydantic-ai) — 16,500+ stars, actively maintained. The `pydantic_ai_examples` package contains working examples for weather agents, bank support, SQL agents, RAG, and more.

**Pydantic Logfire**: [pydantic.dev/logfire](https://pydantic.dev/logfire) — observability platform built for Pydantic AI. Free tier available.

**MCP (Model Context Protocol)**: [modelcontextprotocol.io](https://modelcontextprotocol.io/) — Pydantic AI supports MCP for connecting to external tool servers. This is the extensibility path for connecting agents to third-party services without writing custom tool code.

**Community**: GitHub Discussions on the pydantic-ai repo and the Pydantic Slack workspace are active and responsive to questions.

The next thing to build: take the customer support agent from this tutorial and extend it with a RAG tool that queries your own documentation, add a multi-agent routing layer that handles different product lines, and wire it into your existing FastAPI application. The type system will catch errors before your users do.