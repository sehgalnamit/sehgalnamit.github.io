# namitsehgal-site

Welcome to the **namitsehgal-site** project! This repository hosts a website for publishing articles and guides.

## Project Structure

- **_config.yml**: Site configuration (title, metadata, social links).
- **index.md**: The professional landing page / homepage.
- **_posts/**: Directory where your articles (Markdown files) are stored.
- **.github/workflows/pages.yml**: The CI/CD pipeline that builds and deploys your site to GitHub Pages.
- **CNAME**: Your custom domain configuration (`namitsehgal.com`).
- **.gitignore**: Specifies files to be ignored by Git.
- **README.md**: Documentation for the project.

## How to Publish Articles & Update the Site

Follow these steps to write a new article and update your website:

### 1. Create a New Article
Navigate to the `_posts/` directory and create a new Markdown file. The filename **must** follow the format `YYYY-MM-DD-title.md`.
Example: `_posts/2026-01-01-welcome.md`

### 2. Add Content with Front Matter
Every article needs "front matter" at the very top to tell Jekyll how to handle it:

```markdown
---
layout: post
title: "Your Article Title"
date: 2026-01-01
---
Your article content goes here...
```

### 3. Deploy the Changes
To update the live website, run these commands in your terminal from the root of the project:

```bash
# Stage your changes
git add .

# Commit your changes
git commit -m "Add new article: Your Article Title"

# Push to the main branch
git push origin main
```

Once you push, the GitHub Actions workflow will automatically trigger, build your site, and deploy the updates to `https://namitsehgal.com/`.

Happy publishing!
