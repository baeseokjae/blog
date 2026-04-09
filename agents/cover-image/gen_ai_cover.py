#!/usr/bin/env python3
"""
AI cover image generator using Pollinations.ai (free, no auth).
Usage: python3 gen_ai_cover.py <post-slug>
"""
import sys, os, re, hashlib, urllib.request, urllib.parse, time

BLOG_DIR = "/home/ubuntu/blog"

STYLE_KEYWORDS = {
    "vs": "split-screen showdown, two technologies facing off, electric neon lighting, dramatic contrast",
    "compare": "split-screen showdown, two technologies facing off, electric neon lighting",
    "best": "award podium, spotlight beams, ranked glowing tech elements, cinematic celebration",
    "top": "award podium, spotlight beams, ranked glowing tech elements, cinematic",
    "explain": "futuristic holographic diagram, glowing network nodes, educational infographic style",
    "what-is": "futuristic holographic diagram, glowing network nodes, clean explainer visual",
    "guide": "cinematic hands-on tech interface, step-by-step visual, tutorial scene",
    "how-to": "cinematic hands-on tech interface, step-by-step visual",
    "agent": "autonomous AI robot network, glowing neural pathways, dark tech aesthetic",
    "mcp": "connected AI architecture diagram, glowing protocol nodes, dark background",
    "rag": "vector database visualization, glowing data streams, retrieval system",
    "seo": "search engine optimization, glowing web graph, analytics dashboard",
    "local": "local AI server glowing, private network nodes, home lab aesthetic",
    "voice": "sound wave visualization, AI microphone, audio waveform glowing",
    "video": "cinematic film reel AI, glowing video frames, production studio dark",
    "image": "AI canvas painting itself, glowing generative art, creative studio",
    "coding": "holographic code editor, AI pair programming, glowing syntax",
    "security": "cybersecurity shield glowing, dark hacker aesthetic, network defense",
    "workflow": "automated pipeline visualization, connected gears glowing, orchestration",
}

def get_style(slug):
    slug_lower = slug.lower()
    for kw, style in STYLE_KEYWORDS.items():
        if kw in slug_lower:
            return style
    return "abstract AI technology, glowing circuit patterns, dark futuristic aesthetic"

def parse_title(slug):
    md = os.path.join(BLOG_DIR, "content", "posts", f"{slug}.md")
    # try with -2026 suffix variants
    candidates = [md]
    for suffix in ["-2026", "-local-ai-2026", "-local-ai"]:
        candidates.append(os.path.join(BLOG_DIR, "content", "posts", f"{slug}{suffix}.md"))
    for path in candidates:
        if os.path.exists(path):
            with open(path) as f:
                for line in f:
                    m = re.match(r'^title:\s*["\']?(.+?)["\']?\s*$', line)
                    if m:
                        return m.group(1).strip('"\'')
    return slug.replace("-", " ").title()

def build_prompt(title, style):
    return (
        f"Professional tech blog cover image for article titled '{title}'. "
        f"{style}. "
        f"16:9 aspect ratio, dark background, vivid neon colors, cinematic lighting, "
        f"ultra high quality, no text, no words, no letters, no watermark."
    )

def generate(slug):
    title = parse_title(slug)
    style = get_style(slug)
    prompt = build_prompt(title, style)

    encoded = urllib.parse.quote(prompt)
    seed = int(hashlib.md5(slug.encode()).hexdigest(), 16) % 100000
    url = (
        f"https://image.pollinations.ai/prompt/{encoded}"
        f"?width=1536&height=1024&seed={seed}&model=flux&nologo=true&enhance=true"
    )

    out_path = os.path.join(BLOG_DIR, "static", "images", f"{slug}.png")
    print(f"Generating: {title}")
    print(f"Style: {style[:60]}...")

    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = resp.read()
            if len(data) < 10000:
                raise ValueError(f"Image too small: {len(data)} bytes")
            with open(out_path, "wb") as f:
                f.write(data)
            print(f"Saved: {out_path} ({len(data)//1024}KB)")
            return True
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            if attempt < 2:
                time.sleep(15)
    return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 gen_ai_cover.py <slug>")
        sys.exit(1)
    ok = generate(sys.argv[1])
    sys.exit(0 if ok else 1)
