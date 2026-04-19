#!/usr/bin/env python3
import os
import re
import json
from pathlib import Path
from datetime import datetime
import frontmatter

def extract_faq_section(content):
    """Extract FAQ entries from the content"""
    faqs = []
    # Look for FAQ section with pattern ## FAQ or similar
    faq_match = re.search(r'##\s*FAQ.*?\n(.*?)(?=\n##|\Z)', content, re.IGNORECASE | re.DOTALL)

    if not faq_match:
        return faqs

    faq_content = faq_match.group(1)
    # Extract Q&A pairs - look for **Q: question?** pattern followed by A: answer
    q_pattern = r'\*\*Q:\s*([^*]+\?)\*\*\s*\n\s*A:\s*([^\n]+(?:\n(?!\*\*Q:)[^\n]+)*)'

    for match in re.finditer(q_pattern, faq_content):
        question = match.group(1).strip()
        answer = match.group(2).strip()
        if question and answer:
            faqs.append({
                "question": question,
                "answer": answer
            })

    return faqs

def sanitize_url(url):
    """Ensure URL is valid"""
    if url and not url.startswith('http'):
        url = f"https://rocketcontent.ai{url if url.startswith('/') else '/' + url}"
    return url

def generate_article_schema(post_data, slug):
    """Generate Article schema from post metadata"""
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": post_data.get('title', ''),
        "description": post_data.get('description', ''),
        "image": post_data.get('image', f"https://rocketcontent.ai/images/{slug}.png"),
        "datePublished": post_data.get('date', ''),
        "dateModified": post_data.get('dateModified', post_data.get('date', '')),
        "author": {
            "@type": "Organization",
            "name": "RocketContent",
            "url": "https://rocketcontent.ai"
        },
        "publisher": {
            "@type": "Organization",
            "name": "RocketContent",
            "url": "https://rocketcontent.ai",
            "logo": {
                "@type": "ImageObject",
                "url": "https://rocketcontent.ai/images/logo.png"
            }
        },
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": f"https://rocketcontent.ai/posts/{slug}/"
        },
        "articleSection": post_data.get('articleSection', 'AI'),
        "keywords": post_data.get('tags', []),
        "wordCount": post_data.get('wordCount', 1000)
    }
    return schema

def generate_faqpage_schema(faqs):
    """Generate FAQPage schema from FAQ entries"""
    if not faqs:
        return None

    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": faq["question"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": faq["answer"]
                }
            }
            for faq in faqs
        ]
    }
    return schema

def process_post(post_path):
    """Process a single blog post file"""
    slug = post_path.stem

    with open(post_path, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)

    front_matter = post.metadata
    content = post.content

    # Extract description and validate length
    description = front_matter.get('description', '')
    if len(description) > 155:
        # Truncate and add ellipsis
        description = description[:152] + '...'
        front_matter['description'] = description

    # Get image path
    cover = front_matter.get('cover', {})
    image_path = cover.get('image', f"/images/{slug}.png")

    # Extract FAQs
    faqs = extract_faq_section(content)

    # Prepare post data for schemas
    post_data = {
        'title': front_matter.get('title', ''),
        'description': description,
        'image': image_path,
        'date': str(front_matter.get('date', '')),
        'dateModified': str(datetime.now().isoformat()),
        'tags': front_matter.get('tags', []),
        'wordCount': len(content.split()),
        'articleSection': 'AI'
    }

    # Generate schemas
    article_schema = generate_article_schema(post_data, slug)
    faqpage_schema = generate_faqpage_schema(faqs) if faqs else None

    # Create schema HTML file
    schema_path = Path('/home/ubuntu/blog/layouts/partials') / f'schema-{slug}.html'
    schema_html = f'<script type="application/ld+json">\n{json.dumps(article_schema, indent=2)}\n</script>\n'

    if faqpage_schema:
        schema_html += f'<script type="application/ld+json">\n{json.dumps(faqpage_schema, indent=2)}\n</script>\n'

    schema_path.write_text(schema_html, encoding='utf-8')

    # Update frontmatter to include schema reference
    if 'schema' not in front_matter:
        front_matter['schema'] = f'schema-{slug}'

    # Save updated post
    post.metadata = front_matter
    with open(post_path, 'w', encoding='utf-8') as f:
        f.write(frontmatter.dumps(post))

    print(f"✓ {slug}: {len(faqs)} FAQs, article schema")
    return True

def main():
    posts_dir = Path('/home/ubuntu/blog/content/posts')
    success = 0
    failed = 0

    for post_path in sorted(posts_dir.glob('*.md')):
        try:
            if process_post(post_path):
                success += 1
        except Exception as e:
            print(f"✗ {post_path.stem}: {e}")
            failed += 1

    print(f"\nProcessed: {success} success, {failed} failed")

if __name__ == '__main__':
    main()
