# Ai chat analysis with DBT
This is meant to be a quick, short project to learn dbt by using it to process my
ai chat data.


## Initial scope
* Learn the basics of dbt
* Learn how dbt terminal works
* Learn basic structure of dbt projects
* Use duckdb to store local data
* Setup initial seed data somehow (may need extract scripts)
* Leverage jinja templating
* process ai chat data from claude and open ai
* have one table depending on 2 others


## Nice to haves
* Use it with athena and s3: https://docs.getdbt.com/guides/athena?step=1
* Use sql fluff for sql linting and formatting


## Outcome
* Built a dbt project on DuckDB with raw → staging → mart model layers for Claude Chat and Claude Code data
* Wrote Python extract scripts (`extract_claude_chat.py`, `extract_claude_code.py`) to pull raw data from Cloudflare R2, transform it, and push it back
* Set up Cloudflare R2 (S3-compatible) as the storage backend for raw JSON/JSONL files and the DuckDB output file
* Configured dbt-duckdb with the httpfs extension to read directly from R2 using S3 path-style URLs
* Created an Evidence dashboard with a calendar heatmap of daily Claude Chat and Claude Code usage, filterable by date range and year
* Deployed the Evidence static site to GitHub Pages via GitHub Actions with a two-job pipeline: one job to run the data pipeline and push the updated DuckDB to R2, another to pull it and build the site
* Set up a macOS launchctl cron job to sync `~/.claude/projects` to R2 hourly
