# Pipeline Health Check
Date: 2026-04-27 12:02 UTC

## Actions Taken
- DISABLED-AGENT: ROC-1661 assigned to disabled agent — GSC Analytics: Monitor for striking distance keywords
- Cancelled issue ROC-1661 (disabled agent)

## Warnings
- Missing cover image: n8n-ai-agent-nodes-guide-2026.png (expected at /home/ubuntu/blog/static/images/n8n-ai-agent-nodes-guide-2026.png)
- Missing cover image: cursor-3-glass-agents-window-deep-dive-2026.png (expected at /home/ubuntu/blog/static/images/cursor-3-glass-agents-window-deep-dive-2026.png)

## Full Log
```
[2026-04-27 12:02:49 UTC] [INFO] ============================================================
[2026-04-27 12:02:49 UTC] [INFO] Pipeline Health Check starting 
[2026-04-27 12:02:49 UTC] [INFO] Fetching Paperclip data...
[2026-04-27 12:02:49 UTC] [INFO] Pipeline: done=1204 backlog=81 todo=17 in_progress=3 cancelled=418
[2026-04-27 12:02:49 UTC] [INFO] 
[2026-04-27 12:02:49 UTC] [INFO] Check 1: Stuck subtask issues (>6h, no active run)
[2026-04-27 12:02:49 UTC] [INFO] Stuck subtasks cancelled: 0
[2026-04-27 12:02:49 UTC] [INFO] 
[2026-04-27 12:02:49 UTC] [INFO] Check 2: Zombie subtask issues (null executionRunId >30 min)
[2026-04-27 12:02:49 UTC] [INFO] Zombie subtasks cancelled: 0
[2026-04-27 12:02:49 UTC] [INFO] 
[2026-04-27 12:02:49 UTC] [INFO] Check 3: Topic queue watermark
[2026-04-27 12:02:49 UTC] [INFO] Queued topics: 906 (watermark: 10)
[2026-04-27 12:02:49 UTC] [INFO] Topic queue healthy, no action needed
[2026-04-27 12:02:49 UTC] [INFO] 
[2026-04-27 12:02:49 UTC] [INFO] Check 4: Missing cover images for published posts
[2026-04-27 12:02:49 UTC] [WARN] Missing cover image: n8n-ai-agent-nodes-guide-2026.png (expected at /home/ubuntu/blog/static/images/n8n-ai-agent-nodes-guide-2026.png)
[2026-04-27 12:02:49 UTC] [WARN] Missing cover image: cursor-3-glass-agents-window-deep-dive-2026.png (expected at /home/ubuntu/blog/static/images/cursor-3-glass-agents-window-deep-dive-2026.png)
[2026-04-27 12:02:49 UTC] [INFO] Missing cover images: 2
[2026-04-27 12:02:49 UTC] [INFO] 
[2026-04-27 12:02:49 UTC] [INFO] Check 5: Missing schema files
[2026-04-27 12:02:49 UTC] [INFO] All published posts have schema files
[2026-04-27 12:02:49 UTC] [INFO] 
[2026-04-27 12:02:49 UTC] [INFO] Check 6: Issues assigned to disabled agents (SEO/Thumbnail)
[2026-04-27 12:02:49 UTC] [ACTION] DISABLED-AGENT: ROC-1661 assigned to disabled agent — GSC Analytics: Monitor for striking distance keywords
[2026-04-27 12:02:49 UTC] [ACTION] Cancelled issue ROC-1661 (disabled agent)
[2026-04-27 12:02:49 UTC] [INFO] Disabled-agent issues cancelled: 1
[2026-04-27 12:02:49 UTC] [INFO] 
[2026-04-27 12:02:49 UTC] [INFO] ============================================================
[2026-04-27 12:02:49 UTC] [INFO] Summary: 1 actions taken
[2026-04-27 12:02:49 UTC] [INFO]   Stuck subtasks cancelled: 0
[2026-04-27 12:02:49 UTC] [INFO]   Zombie subtasks cancelled: 0
[2026-04-27 12:02:49 UTC] [INFO]   Strategist wakes: 0
[2026-04-27 12:02:49 UTC] [INFO]   Disabled-agent issues cancelled: 1
[2026-04-27 12:02:49 UTC] [INFO]   Missing cover images (warnings): 2
[2026-04-27 12:02:49 UTC] [INFO]   Missing schema files (warnings): 0
[2026-04-27 12:02:49 UTC] [INFO] Pipeline Health Check complete
```