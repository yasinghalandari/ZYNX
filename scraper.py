name: Hourly Vless Scraper

on:
  schedule:
    - cron: '1 * * * *' # اجرا سر هر ساعت
  workflow_dispatch: # امکان اجرای دستی برای تست

permissions:
  contents: write

jobs:
  scrape_and_update:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10' 

      - name: Install dependencies
        run: |
          pip install requests beautifulsoup4

      - name: Run Scraper
        run: python scraper.py

      - name: Commit and Push changes
        run: |
          git config --global user.name "GitHub Action"
          git config --global user.email "action@github.com"
          git add yasin.text
          # بررسی می‌کند آیا تغییری ایجاد شده یا خیر
          if [ -n "$(git status --porcelain)" ]; then
            git commit -m "Updated vless configs $(date)"
            git push
          else
            print("No changes to commit.")
          fi
