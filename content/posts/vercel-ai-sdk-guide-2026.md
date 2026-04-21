---
title: "Vercel AI SDK Guide 2026: Build Production AI Apps with TypeScript"
date: 2026-04-21
draft: false
tags: ["vercel ai sdk", "typescript", "next.js", "ai agents", "tool calling", "streaming", "structured output"]
description: "A complete guide to building production AI applications with the Vercel AI SDK in 2026. Covers text generation, streaming, structured output with Zod, chat UIs, tool calling, multi-step agents, Workflows, and deployment."
cover:
  image: "/images/vercel-ai-sdk-guide-2026.png"
  alt: "Vercel AI SDK Guide 2026 — Build Production AI Apps with TypeScript"
schema:
  - "@context": https://schema.org
    "@type": BlogPosting
    headline: "Vercel AI SDK Guide 2026: Build Production AI Apps with TypeScript"
    datePublished: "2026-04-21"
    description: "A complete guide to building production AI applications with the Vercel AI SDK in 2026."
    author:
      "@type": Person
      name: "Seokjae Bae"
    publisher:
      "@type": Organization
      name: "baeseokjae.github.io"
---

The Vercel AI SDK has become the default way to build AI-powered applications in TypeScript. With 11.5 million weekly npm downloads, support for 100+ models across 16 providers, and a growing ecosystem of Workflows and Sandbox tooling, it handles the plumbing so you can focus on your product logic.

This guide covers everything you need to go from zero to a deployed, production-grade AI application. No hype — just the APIs, patterns, and tradeoffs.

## What is the Vercel AI SDK? Why It Matters in 2026

The AI SDK is a TypeScript toolkit for building AI applications with streaming, structured output, tool calling, and multi-step agent patterns. It is not a model provider — it is a unified interface that sits between your application code and any LLM provider.

### 11.5M Weekly Downloads and Growing

The npm download numbers tell the story. AI SDK crossed 11.5 million weekly downloads in April 2026, up from roughly 4 million a year prior. The SDK has 23.7K GitHub stars and 614+ contributors. This is not a niche library. It is the dominant TypeScript AI framework.

### The Unified TypeScript AI Layer: Core + UI + RSC

The SDK is organized into three layers:

| Layer | Package | Purpose |
|-------|---------|---------|
| **AI SDK Core** | `ai` | Server-side generation: `generateText`, `streamText`, `generateObject`, `streamObject` |
| **AI SDK UI** | `ai/react` (and framework equivalents) | Client-side hooks: `useChat`, `useCompletion`, `useObject` |
| **AI SDK RSC** | `ai/rsc` | React Server Components integration for streaming UI from the server |

This separation matters. Core runs anywhere — Node, Edge, Bun, Deno. UI hooks render in the browser. RSC bridges the two in Next.js App Router. You pick the layer you need and ignore the rest.

### How It Fits in the Vercel Ecosystem

The SDK is the foundation, but the ecosystem extends further in 2026:

- **AI Gateway**: One API key to access 100+ models across 16+ providers with built-in load balancing, fallbacks, and rate limiting.
- **Vercel Sandbox**: Secure execution environment for agent-generated code. Useful when your AI agent writes and runs code on behalf of users.
- **Vercel Workflows**: Durable, long-running agent execution that can suspend, resume, and survive function timeouts. New in 2026.
- **AI Elements**: A component library for AI-native UIs (message threads, artifact views, tool result renders). New in 2026.

You do not need any of these to use AI SDK Core. They are opt-in for specific use cases.

## Getting Started: Installing and Configuring AI SDK

### npm install ai + Provider Packages

```bash
npm install ai @ai-sdk/openai @ai-sdk/anthropic @ai-sdk/google
```

The `ai` package contains the core functions. Provider packages (`@ai-sdk/openai`, `@ai-sdk/anthropic`, `@ai-sdk/google`) contain model definitions and provider-specific configuration. You install only the providers you use.

### Setting Up API Keys

Store provider API keys as environment variables:

```bash
# .env.local
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_GENERATIVE_AI_API_KEY=AIza...
```

Never commit these. In production, use your hosting platform's secret management.

### Project Structure for a Next.js AI App

A minimal structure:

```
src/
├── app/
│   ├── api/
│   │   └── chat/
│   │       └── route.ts      # Server-side AI route
│   ├── page.tsx              # Chat UI
│   └── layout.tsx
├── lib/
│   └── ai.ts                 # Provider setup, shared config
└── .env.local
```

The `lib/ai.ts` file centralizes provider instantiation:

```typescript
// lib/ai.ts
import { createOpenAI } from "@ai-sdk/openai";
import { createAnthropic } from "@ai-sdk/anthropic";

export const openai = createOpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

export const anthropic = createAnthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});
```

### AI Gateway: One Key for 100+ Models

If you use Vercel AI Gateway, you can replace individual provider keys with a single gateway key:

```typescript
import { createGateway } from "@ai-sdk/gateway";

const gateway = createGateway({
  apiKey: process.env.AI_GATEWAY_KEY,
});

// Access any model through the gateway
const model = gateway("gpt-4o");
const model2 = gateway("claude-sonnet-4-20250514");
```

The Gateway handles routing, rate limiting, and fallbacks across providers. This is useful when you want model flexibility without managing multiple API keys.

## AI SDK Core: Text Generation and Streaming

### generateText() for One-Shot Generation

`generateText` sends a prompt and waits for the complete response. Use it when you need the full result before proceeding.

```typescript
import { generateText } from "ai";
import { openai } from "@/lib/ai";

async function summarize(text: string) {
  const { text: summary } = await generateText({
    model: openai("gpt-4o"),
    prompt: `Summarize the following text in 2-3 sentences:\n\n${text}`,
  });

  return summary;
}
```

The return object includes `text`, `usage` (token counts), `finishReason`, and `response` (raw provider response).

### streamText() for Real-Time Streaming

`streamText` returns a stream that yields tokens as they arrive. This is the foundation for chat interfaces.

```typescript
import { streamText } from "ai";
import { openai } from "@/lib/ai";

async function streamResponse(prompt: string) {
  const result = streamText({
    model: openai("gpt-4o"),
    prompt,
  });

  // Consume as a text stream
  for await (const chunk of result.textStream) {
    process.stdout.write(chunk);
  }
}
```

In a Next.js route handler, you return the stream directly:

```typescript
// app/api/chat/route.ts
import { streamText } from "ai";
import { openai } from "@/lib/ai";

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model: openai("gpt-4o"),
    messages,
  });

  return result.toDataStreamResponse();
}
```

`toDataStreamResponse()` converts the stream into the AI SDK data stream protocol — the format that client-side hooks expect.

### Provider Switching with One Line of Code

Because models are just configuration objects, switching providers requires changing one argument:

```typescript
// OpenAI
const result = await generateText({
  model: openai("gpt-4o"),
  prompt: "Explain quantum computing",
});

// Switch to Anthropic — only the model line changes
const result = await generateText({
  model: anthropic("claude-sonnet-4-20250514"),
  prompt: "Explain quantum computing",
});
```

No other code changes. The prompt format, streaming mechanism, and response handling remain identical.

### Built-in Fallbacks and Retry Logic

When a provider fails or rate-limits, you can fall back to an alternative model:

```typescript
import { generateText } from "ai";
import { openai } from "@/lib/ai";
import { anthropic } from "@/lib/ai";

const { text } = await generateText({
  model: openai("gpt-4o"),
  fallbackModels: [anthropic("claude-sonnet-4-20250514")],
  prompt: "Explain the halting problem",
});
```

If the primary model fails, the SDK automatically retries with the first fallback. You can configure `maxRetries` and `abortSignal` for finer control.

## Structured Output with Zod Schemas

Raw LLM text is fine for chat. For application logic, you need structured data. The AI SDK integrates with Zod to enforce type-safe schemas on model output.

### generateObject() for Type-Safe JSON Responses

```typescript
import { generateObject } from "ai";
import { openai } from "@/lib/ai";
import { z } from "zod";

const RecipeSchema = z.object({
  name: z.string(),
  ingredients: z.array(z.object({
    item: z.string(),
    amount: z.string(),
  })),
  steps: z.array(z.string()),
  cookTimeMinutes: z.number(),
});

async function getRecipe(dish: string) {
  const { object } = await generateObject({
    model: openai("gpt-4o"),
    schema: RecipeSchema,
    prompt: `Generate a recipe for ${dish}`,
  });

  // object is fully typed as z.infer<typeof RecipeSchema>
  return object;
}
```

The return value `object` has the TypeScript type inferred from the Zod schema. If the model produces output that does not conform, the SDK throws a `AI_TypeError`.

### streamObject() for Streaming Structured Data

When generating large structured objects, `streamObject` returns partial results as they arrive:

```typescript
import { streamObject } from "ai";
import { openai } from "@/lib/ai";
import { z } from "zod";

const result = streamObject({
  model: openai("gpt-4o"),
  schema: z.object({
    analysis: z.string(),
    score: z.number(),
    recommendations: z.array(z.string()),
  }),
  prompt: "Analyze the following code for security vulnerabilities: ...",
});

for await (const partialObject of result.partialObjectStream) {
  // partialObject contains the fields that have been generated so far
  console.log(partialObject);
}
```

Use `partialObjectStream` for real-time UI updates as the model fills in each field.

### Zod Schema Definitions and Validation

The SDK supports most Zod types: strings, numbers, booleans, arrays, objects, enums, unions, and optional fields. It does not support transforms or refinements — those apply after the model output is validated.

```typescript
// Supported
const schema = z.object({
  status: z.enum(["active", "inactive", "pending"]),
  tags: z.array(z.string()),
  metadata: z.record(z.string(), z.any()).optional(),
});

// Not supported in schema (apply after)
const schema = z.object({
  email: z.string(), // validate format after with .transform()
  score: z.number().min(0).max(100), // .min/.max work but are hints, not hard guards
});
```

### Practical Example: Extracting Structured Data from Unstructured Text

```typescript
import { generateObject } from "ai";
import { openai } from "@/lib/ai";
import { z } from "zod";

const ContactSchema = z.object({
  name: z.string(),
  email: z.string().optional(),
  phone: z.string().optional(),
  company: z.string().optional(),
  title: z.string().optional(),
});

async function extractContacts(emailText: string) {
  const { object: contacts } = await generateObject({
    model: openai("gpt-4o"),
    schema: z.array(ContactSchema),
    prompt: `Extract all people and their contact information from this email:\n\n${emailText}`,
  });

  return contacts;
}

// Input: "Hi, I'm Sarah Chen (VP Eng at Acme, sarah@acme.co). 
//         CC'd: John Park (john.park@beta.dev)"
// Output: [
//   { name: "Sarah Chen", email: "sarah@acme.co", company: "Acme", title: "VP Eng" },
//   { name: "John Park", email: "john.park@beta.dev", company: undefined, title: undefined }
// ]
```

No regex. No parsing. The model extracts structured data from freeform text, and the Zod schema guarantees the output shape.

## Building Chat UIs with AI SDK UI Hooks

### useChat() for Chat Interfaces

`useChat` manages conversation state, sends messages to your API route, and streams responses back to the UI:

```typescript
// app/page.tsx
"use client";
import { useChat } from "ai/react";

export default function ChatPage() {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: "/api/chat",
  });

  return (
    <div className="max-w-2xl mx-auto p-4">
      <div className="space-y-4 mb-4">
        {messages.map((m) => (
          <div key={m.id} className={m.role === "user" ? "text-right" : "text-left"}>
            <div
              className={`inline-block rounded-lg px-4 py-2 ${
                m.role === "user" ? "bg-blue-600 text-white" : "bg-gray-100 text-gray-900"
              }`}
            >
              {m.content}
            </div>
          </div>
        ))}
      </div>

      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          value={input}
          onChange={handleInputChange}
          placeholder="Ask something..."
          className="flex-1 rounded border px-3 py-2"
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading} className="rounded bg-blue-600 px-4 py-2 text-white">
          Send
        </button>
      </form>
    </div>
  );
}
```

The hook handles message history, loading state, error state, and automatic scrolling. The server route from the previous section (`/api/chat`) handles the model call and streaming.

### useCompletion() for Auto-Complete

`useCompletion` is for single-turn generation patterns — autocomplete, suggestions, summarization — where you do not need conversation history:

```typescript
"use client";
import { useCompletion } from "ai/react";

export default function Summarizer() {
  const { completion, input, handleInputChange, handleSubmit } = useCompletion({
    api: "/api/completion",
  });

  return (
    <form onSubmit={handleSubmit}>
      <textarea value={input} onChange={handleInputChange} placeholder="Paste text to summarize" />
      <button type="submit">Summarize</button>
      {completion && <div className="mt-4">{completion}</div>}
    </form>
  );
}
```

### useObject() for Streaming Structured Responses

When your API route returns a streamed object (via `streamObject`), use `useObject` on the client:

```typescript
"use client";
import { useObject } from "ai/react";
import { z } from "zod";

const AnalysisSchema = z.object({
  summary: z.string(),
  sentiment: z.enum(["positive", "negative", "neutral"]),
  keywords: z.array(z.string()),
});

export default function Analyzer() {
  const { object, submit, isLoading } = useObject({
    api: "/api/analyze",
    schema: AnalysisSchema,
  });

  return (
    <div>
      <button onClick={() => submit({ text: "Product is great but shipping was slow" })} disabled={isLoading}>
        Analyze
      </button>
      {object && (
        <div className="mt-4 space-y-2">
          <p><strong>Summary:</strong> {object.summary}</p>
          <p><strong>Sentiment:</strong> {object.sentiment}</p>
          <p><strong>Keywords:</strong> {object.keywords?.join(", ")}</p>
        </div>
      )}
    </div>
  );
}
```

### Framework Support

The UI hooks are not React-only. AI SDK ships framework-specific packages:

| Framework | Package | Hooks |
|-----------|---------|-------|
| React | `ai/react` | `useChat`, `useCompletion`, `useObject` |
| Vue | `ai/vue` | `useChat`, `useCompletion`, `useObject` |
| Svelte | `ai/svelte` | `useChat`, `useCompletion`, `useObject` |
| Solid | `ai/solid` | `useChat`, `useCompletion`, `useObject` |

The server-side `streamText` and `streamObject` functions are framework-agnostic. Only the client hooks differ.

## Tool Calling: Giving Your AI Agent Superpowers

Tool calling lets the model invoke functions you define. Instead of just generating text, the model can trigger actions — fetch data, run calculations, query databases — then incorporate the results into its response.

### Defining Tools with Execute Functions

```typescript
import { generateText, tool } from "ai";
import { openai } from "@/lib/ai";
import { z } from "zod";

const result = await generateText({
  model: openai("gpt-4o"),
  tools: {
    weather: tool({
      description: "Get current weather for a location",
      parameters: z.object({
        city: z.string(),
        unit: z.enum(["celsius", "fahrenheit"]).optional(),
      }),
      execute: async ({ city, unit = "celsius" }) => {
        const res = await fetch(`https://api.weather.example/current?city=${city}&unit=${unit}`);
        return res.json();
      },
    }),
    calculator: tool({
      description: "Evaluate a mathematical expression",
      parameters: z.object({
        expression: z.string(),
      }),
      execute: async ({ expression }) => {
        // Simple eval for demo — use a safe math parser in production
        const result = Function(`"use strict"; return (${expression})`)();
        return { result };
      },
    }),
  },
  prompt: "What's the weather in Seoul, and what is 15% of 340?",
});

console.log(result.text);
// "The current weather in Seoul is 12°C with partly cloudy skies.
//  15% of 340 is 51."
```

The model decides which tools to call based on the user's prompt. You do not hardcode the invocation logic.

### Multi-Step Agent Loops with maxSteps

A single model call with tools might not finish the job. The model might need to call a tool, read the result, then decide to call another tool. `maxSteps` enables this multi-step loop:

```typescript
import { generateText, tool } from "ai";
import { openai } from "@/lib/ai";
import { z } from "zod";

const result = await generateText({
  model: openai("gpt-4o"),
  maxSteps: 5,
  tools: {
    searchDatabase: tool({
      description: "Search the product database",
      parameters: z.object({
        query: z.string(),
        category: z.string().optional(),
      }),
      execute: async ({ query, category }) => {
        // Simulated database query
        return db.query(query, { category });
      },
    }),
    checkInventory: tool({
      description: "Check inventory for a product ID",
      parameters: z.object({
        productId: z.string(),
      }),
      execute: async ({ productId }) => {
        return inventoryAPI.check(productId);
      },
    }),
  },
  prompt: "Find wireless headphones under $100 and check if the top result is in stock",
});
```

With `maxSteps: 5`, the model can make up to 5 tool calls in sequence. After each tool result, it decides whether to call another tool or produce a final text response.

### Tool Result Streaming to the Client

When using `streamText` with tools, tool invocations and results are included in the data stream. On the client, `useChat` exposes tool state:

```typescript
"use client";
import { useChat } from "ai/react";

export default function ChatWithTools() {
  const { messages, input, handleInputChange, handleSubmit } = useChat({
    api: "/api/chat",
    maxSteps: 3,
  });

  return (
    <div>
      {messages.map((m) => (
        <div key={m.id}>
          {m.role === "assistant" && m.toolInvocations?.map((invocation) => (
            <div key={invocation.toolCallId} className="bg-yellow-50 p-2 rounded text-sm">
              {invocation.state === "call" && <span>Calling {invocation.toolName}...</span>}
              {invocation.state === "result" && (
                <span>Result: {JSON.stringify(invocation.result)}</span>
              )}
            </div>
          ))}
          {m.content && <div>{m.content}</div>}
        </div>
      ))}
      <form onSubmit={handleSubmit}>
        <input value={input} onChange={handleInputChange} />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}
```

## Building AI Agents with Multi-Step Reasoning

### The Agent Loop Pattern with Tool Calling

An agent is a loop: the model reasons, calls tools, observes results, and repeats until the task is done. The AI SDK handles the loop via `maxSteps`. Your job is to define the tools and the system prompt.

```typescript
import { generateText, tool } from "ai";
import { openai } from "@/lib/ai";
import { z } from "zod";

const researchAgent = async (query: string) => {
  const result = await generateText({
    model: openai("gpt-4o"),
    maxSteps: 10,
    system: `You are a research assistant. Use the available tools to find, verify, and summarize information.
    Always cite your sources. If you cannot find a definitive answer, say so explicitly.`,
    tools: {
      webSearch: tool({
        description: "Search the web for information",
        parameters: z.object({ query: z.string() }),
        execute: async ({ query }) => {
          const results = await searchAPI.search(query);
          return results.slice(0, 5);
        },
      }),
      getPageContent: tool({
        description: "Fetch the content of a web page",
        parameters: z.object({ url: z.string() }),
        execute: async ({ url }) => {
          const resp = await fetch(url);
          return resp.text().slice(0, 5000); // Truncate for context limits
        },
      }),
    },
    prompt: query,
  });

  return result.text;
};
```

### Memory and Conversation History Management

For multi-turn agents, you pass the full message history on each request:

```typescript
// app/api/agent/route.ts
import { streamText } from "ai";
import { openai } from "@/lib/ai";

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model: openai("gpt-4o"),
    maxSteps: 5,
    system: "You are a helpful coding assistant with access to a codebase search tool.",
    messages, // Full conversation history
    tools: {
      searchCode: tool({
        description: "Search the codebase for code matching a query",
        parameters: z.object({ query: z.string() }),
        execute: async ({ query }) => codebaseIndex.search(query),
      }),
    },
  });

  return result.toDataStreamResponse();
}
```

Manage history size to stay within context windows. A common pattern: keep the system prompt + the last N messages, or implement a summarization step for older messages.

```typescript
function truncateMessages(messages: Message[], maxMessages: number = 20): Message[] {
  if (messages.length <= maxMessages) return messages;
  // Keep system message (if any) + last N messages
  const systemMessages = messages.filter((m) => m.role === "system");
  const nonSystem = messages.filter((m) => m.role !== "system");
  return [...systemMessages, ...nonSystem.slice(-maxMessages)];
}
```

### RAG Integration Pattern

Retrieval-Augmented Generation injects relevant context into the prompt before the model responds. With tool calling, the model can decide when to retrieve:

```typescript
import { generateText, tool } from "ai";
import { openai } from "@/lib/ai";
import { z } from "zod";

const ragAgent = async (query: string) => {
  const result = await generateText({
    model: openai("gpt-4o"),
    maxSteps: 3,
    system: "Answer questions based on the documentation. Use the search tool to find relevant docs before answering.",
    tools: {
      searchDocs: tool({
        description: "Search the product documentation",
        parameters: z.object({ query: z.string() }),
        execute: async ({ query }) => {
          const results = await vectorStore.search(query, { topK: 5 });
          return results.map((r) => ({ content: r.text, source: r.metadata.source }));
        },
      }),
    },
    prompt: query,
  });

  return result.text;
};
```

The alternative is "always-retrieve" — fetch context on every request and inject it into the system prompt. The tool-calling approach is more efficient because the model retrieves only when needed.

## Vercel Workflows: Long-Running Agents That Survive

### What Are Vercel Workflows and When to Use Them

Serverless functions have timeout limits — 10 seconds on Vercel Hobby, 300 seconds on Pro. An agent that needs to call multiple tools, wait for external APIs, or generate long content can easily exceed these limits.

Vercel Workflows solve this by providing durable execution. A workflow can:
- **Suspend** execution and resume when an event occurs (user approval, external API callback)
- **Survive** function restarts — state is persisted, not lost
- **Run** for minutes or hours, not seconds

Use Workflows when your agent needs to:
- Wait for human approval before acting
- Chain many tool calls that exceed function timeout
- Process long-running tasks (content generation pipelines, data analysis)

### Suspend, Resume, and Survive Timeouts

```typescript
import { workflow } from "@vercel/orchestration";
import { generateText, tool } from "ai";
import { openai } from "@/lib/ai";
import { z } from "zod";

const contentPipeline = workflow.define({
  id: "content-generation",
  timeout: "1h",
  async run(ctx) {
    // Step 1: Generate outline
    const { object: outline } = await generateObject({
      model: openai("gpt-4o"),
      schema: z.object({
        title: z.string(),
        sections: z.array(z.object({
          heading: z.string(),
          keyPoints: z.array(z.string()),
        })),
      }),
      prompt: ctx.request.topic,
    });

    // Step 2: Suspend for human review
    const approval = await ctx.waitForEvent("approval", {
      timeout: "24h",
      data: { outline },
    });

    if (!approval.approved) {
      return { status: "rejected", reason: approval.reason };
    }

    // Step 3: Generate full content from approved outline
    const sections = [];
    for (const section of outline.sections) {
      const { text } = await generateText({
        model: openai("gpt-4o"),
        prompt: `Write a detailed section based on: ${JSON.stringify(section)}`,
      });
      sections.push({ heading: section.heading, content: text });
    }

    return { status: "complete", content: { title: outline.title, sections } };
  },
});
```

### Building Durable AI Agents

The key difference between a standard `maxSteps` agent and a workflow agent is durability. A `maxSteps` agent runs in a single function invocation. If the function is interrupted, the agent loses all progress. A workflow agent persists state at each step. If the function restarts, the workflow picks up where it left off.

This makes Workflows appropriate for:
- Content generation pipelines with human review steps
- Data analysis agents that run queries over minutes
- Multi-agent systems where one agent delegates to another and waits for results
- Any agent that interacts with asynchronous external systems

## Production Deployment and Scaling

### Deploying to Vercel vs Self-Hosting

| Aspect | Vercel | Self-Hosted (Node/Docker) |
|--------|--------|---------------------------|
| Streaming | Native (Edge + Node) | Requires proper streaming server setup |
| Cold starts | Edge: ~50ms, Serverless: ~200ms | Depends on your infrastructure |
| Timeouts | 10s (Hobby), 300s (Pro), Workflows for longer | No limit (configure yourself) |
| AI Gateway | Built-in | Self-host or skip |
| Sandbox | Built-in | Bring your own sandbox |
| Scaling | Automatic | Manual or Kubernetes |

For many teams, Vercel is the fastest path to production. The Edge runtime handles streaming with minimal latency. Self-hosting gives you more control over timeouts and compute resources.

### Edge Runtime Considerations

AI SDK runs on the Edge runtime. This means:

- No Node.js-specific APIs (fs, child_process, native modules) in edge functions
- Tool `execute` functions that depend on Node APIs must run on the Node runtime
- You can mix: stream on Edge, execute tools on Node

```typescript
// If your tools need Node.js APIs, use the Node runtime
export const runtime = "nodejs"; // not "edge"

export async function POST(req: Request) {
  // This function can use fs, child_process, etc.
  const result = streamText({
    model: openai("gpt-4o"),
    messages: await req.json(),
    tools: { /* node-dependent tools */ },
  });
  return result.toDataStreamResponse();
}
```

### Rate Limiting and Cost Management

LLM API calls cost money. Without limits, a single user can rack up significant charges. Implement rate limiting at the API route level:

```typescript
import { Ratelimit } from "@upstash/ratelimit";
import { Redis } from "@upstash/redis";

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, "1m"), // 10 requests per minute
});

export async function POST(req: Request) {
  const ip = req.headers.get("x-forwarded-for") ?? "anonymous";
  const { success } = await ratelimit.limit(ip);

  if (!success) {
    return new Response("Rate limit exceeded", { status: 429 });
  }

  // ... AI SDK call
}
```

Track token usage from the result object to monitor costs:

```typescript
const result = await generateText({
  model: openai("gpt-4o"),
  prompt: "...",
});

console.log(result.usage);
// { promptTokens: 124, completionTokens: 89, totalTokens: 213 }
```

Log this to your observability system. Vercel logs capture request metadata automatically. For custom tracking, send `result.usage` to your analytics endpoint.

### Monitoring with Vercel Logs and Observability

The AI SDK supports OpenTelemetry for distributed tracing. In Vercel, request-level logs are available in the dashboard. For deeper observability:

```typescript
import { generateText } from "ai";
import { openai } from "@/lib/ai";

const result = await generateText({
  model: openai("gpt-4o"),
  prompt: "...",
  experimental_telemetry: {
    isEnabled: true,
    functionId: "chat-completion",
    metadata: { userId: "user-123" },
  },
});
```

This exports spans and metrics to your OpenTelemetry collector. You can trace the full lifecycle: request received, model called, tokens streamed, response completed.

## AI SDK vs LangChain vs Mastra: Framework Comparison

Three frameworks dominate TypeScript AI development in 2026. Here is how they compare.

### Feature Matrix

| Feature | AI SDK | LangChain.ts | Mastra |
|---------|--------|--------------|--------|
| Streaming | First-class, built-in | Supported, requires config | Built-in |
| Tool calling | Native, Zod-based | Native, Zod-based | Native, Zod-based |
| Structured output | generateObject/streamObject | StructuredOutputParser | generateObject |
| Multi-step agents | maxSteps | AgentExecutor | Agent loops |
| UI hooks | Built-in (React, Vue, Svelte, Solid) | None (bring your own) | Built-in (React) |
| Provider count | 16+ / 100+ models | 30+ providers | 10+ providers |
| Durable workflows | Vercel Workflows integration | LangGraph for state machines | Built-in workflow engine |
| Bundle size | ~15KB core | ~200KB+ | ~25KB core |
| Edge runtime | Yes | Partial | Yes |
| RSC support | Built-in | None | Partial |

### Performance: Bundle Size and Latency

AI SDK is significantly lighter than LangChain. The core `ai` package is roughly 15KB minified. LangChain.ts with its dependency chain can exceed 200KB. This matters for client-side imports and cold start times.

For latency, the overhead added by each framework is negligible compared to model inference time (hundreds of milliseconds to seconds). The real latency difference comes from streaming architecture. AI SDK streams are optimized for Edge runtime with minimal buffering, which translates to lower time-to-first-token on Vercel.

### When to Choose Each Framework

| Choose AI SDK when | Choose LangChain when | Choose Mastra when |
|--------------------|-----------------------|--------------------|
| Building on Next.js/Vercel | You need LangGraph's state machine model | You want an all-in-one agent framework |
| You want minimal bundle size | You're porting from LangChain Python | You need built-in RAG pipelines |
| Streaming is a priority | You need 30+ niche providers | You prefer convention over configuration |
| You want UI hooks out of the box | Your team already uses LangChain | You want built-in MCP server support |
| Edge/runtime compatibility matters | You need LangSmith for observability | You want a hosted agent dashboard |

The honest answer: for most TypeScript AI apps in 2026, AI SDK is the practical default. LangChain is the right choice for teams that need its larger ecosystem or are migrating from Python. Mastra is worth evaluating if you want a more opinionated framework with built-in infrastructure.

## Conclusion and Resources

### Key Takeaways

1. **AI SDK Core** handles text generation, streaming, structured output, and tool calling with a provider-agnostic API. Switch models by changing one argument.
2. **Structured output** with `generateObject` and Zod schemas gives you type-safe JSON from LLM responses — no more parsing raw text.
3. **UI hooks** (`useChat`, `useCompletion`, `useObject`) handle client-side state, streaming, and rendering across React, Vue, Svelte, and Solid.
4. **Tool calling + maxSteps** turns a text generator into a multi-step agent. The model decides when and which tools to call.
5. **Vercel Workflows** add durability for long-running agents that exceed function timeouts or need human-in-the-loop patterns.
6. **Production readiness** means rate limiting, token usage tracking, and runtime selection (Edge vs Node). The SDK gives you the hooks; you add the guardrails.

### Official Docs, Templates, and Cookbooks

- [AI SDK Documentation](https://ai-sdk.dev/docs) — the canonical reference for all APIs
- [AI SDK GitHub](https://github.com/vercel/ai) — source, issues, and releases
- [Next.js AI Chatbot Template](https://vercel.com/templates/next.js/nextjs-ai-chatbot) — production-starter with auth, persistence, and multi-model support
- [AI SDK Cookbooks](https://ai-sdk.dev/docs/cookbook) — patterns for RAG, agents, and structured output

### Community

- [GitHub Discussions](https://github.com/vercel/ai/discussions) — questions, feature requests, and architecture discussions
- [Vercel Discord](https://vercel.com/discord) — real-time help from the community and maintainers

### What's Next

Two developments to watch in the second half of 2026:

- **AI Elements**: The new component library for AI-native UIs (message threads, tool result renderers, artifact views). Currently in beta, expected to reach stable by Q3.
- **Workflows evolution**: Vercel Workflows are new. Expect more patterns, better debugging, and tighter AI SDK integration as the API matures.

The AI SDK has reached the point where the core APIs are stable and production-proven. The ecosystem around it — Workflows, Sandbox, AI Elements — is still evolving rapidly. Start with Core, add pieces as your use case demands them.