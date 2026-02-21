# Nanobanana Skill for Claude Code

This folder contains a [Claude Skill](https://support.anthropic.com/en/articles/11175166-what-are-skills-and-how-do-i-use-them) for using nanobanana with Claude Code.

## Installation

Run `./install.sh` from the repository root — it installs both the CLI and this skill.

```bash
git clone https://github.com/sussdorff/nanobanana.git
cd nanobanana
./install.sh
```

The skill is copied to `~/.claude/skills/nanobanana/`.

## Prerequisites

- nanobanana CLI (installed by `install.sh`)
- `GEMINI_API_KEY` or `OPENROUTER_API_KEY` environment variable

Get a Gemini API key at: https://aistudio.google.com/apikey

## What This Skill Does

When enabled, Claude will automatically use nanobanana to:

- Generate images from text descriptions
- Create slides, dashboards, wireframes, moodboards, icons, architecture diagrams
- Edit and transform existing images
- Guide you through discovery questions for complex requests
