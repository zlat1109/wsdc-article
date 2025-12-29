#!/usr/bin/env python3
"""
WSDC Article Publisher Bot
Publishes Markdown articles to Telegra.ph and sends a summary to Telegram.
"""
import os
import sys
import argparse
import asyncio
import markdown
import logging
from telegraph import Telegraph
from telegram import Bot
from telegram.constants import ParseMode
from bs4 import BeautifulSoup, NavigableString

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

ALLOWED_TAGS = {
    'a', 'aside', 'b', 'blockquote', 'br', 'code', 'em', 'figcaption', 'figure', 
    'h3', 'h4', 'hr', 'i', 'iframe', 'img', 'li', 'ol', 'p', 'pre', 's', 
    'strong', 'u', 'ul', 'video'
}

def parse_args():
    parser = argparse.ArgumentParser(description="Publish article to Telegraph and Telegram")
    parser.add_argument("--file", required=True, help="Path to the article markdown file")
    parser.add_argument("--chat-id", required=True, help="Telegram Chat ID")
    parser.add_argument("--token", help="Telegram Bot Token (or use env TELEGRAM_BOT_TOKEN)")
    return parser.parse_args()

def split_content(content):
    marker = "# Пост для Telegram-канала"
    if marker in content:
        parts = content.split(marker)
        article_md = parts[0].strip()
        telegram_post_md = parts[1].strip()
        return article_md, telegram_post_md
    return content, None

def clean_html_for_telegraph(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # 1. Handle Tables: Convert to <pre> ASCII-like
    for table in soup.find_all('table'):
        rows_text = []
        # Get headers
        headers = [th.get_text().strip() for th in table.find_all('th')]
        if headers:
            rows_text.append(" | ".join(headers))
            rows_text.append("-" * len(rows_text[0]))
        
        # Get rows
        for tr in table.find_all('tr'):
            cells = [td.get_text().strip() for td in tr.find_all('td')]
            if cells:
                rows_text.append(" | ".join(cells))
        
        pre_tag = soup.new_tag('pre')
        pre_tag.string = "\n".join(rows_text)
        table.replace_with(pre_tag)

    # 2. Handle Headers
    for tag in soup.find_all(['h1', 'h2', 'h5', 'h6']):
        if tag.name in ['h1', 'h2']:
            tag.name = 'h3'
        elif tag.name in ['h5', 'h6']:
            tag.name = 'h4'

    # 3. Unwrap unsupported tags
    for tag in soup.find_all(True):
        if tag.name not in ALLOWED_TAGS:
            tag.unwrap()

    return str(soup)

def markdown_to_html(md_text):
    # Enable tables extension
    html = markdown.markdown(md_text, extensions=['tables'])
    return clean_html_for_telegraph(html)

def publish_to_telegraph(title, author, html_content):
    try:
        telegraph_token = os.environ.get('TELEGRAPH_TOKEN')
        if telegraph_token:
            telegraph = Telegraph(access_token=telegraph_token)
        else:
            telegraph = Telegraph()
            telegraph.create_account(short_name='WSDC_Bot')
        
        response = telegraph.create_page(
            title=title,
            html_content=html_content,
            author_name=author
        )
        return response['url']
    except Exception as e:
        logger.error(f"Telegraph publishing failed: {e}")
        return None

async def send_telegram_message(bot_token, chat_id, message):
    try:
        bot = Bot(token=bot_token)
        await bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False
        )
        logger.info(f"Message sent to {chat_id}")
    except Exception as e:
        logger.error(f"Telegram sending failed: {e}")
        sys.exit(1)

def format_telegram_message(text, url):
    text = text.replace('[Ссылка]', url)
    import re
    # Bold **text** -> <b>text</b>
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # Italic *text* -> <i>text</i>
    text = re.sub(r'(?<!\*)\*(?!\*)(.*?)(?<!\*)\*(?!\*)', r'<i>\1</i>', text)
    return text

def extract_title_author(md_text):
    lines = md_text.split('\n')
    title = "New Article"
    author = "WSDC Analytics"
    for line in lines:
        if line.startswith('# '):
            title = line[2:].strip()
            break
    return title, author

async def main():
    args = parse_args()
    bot_token = args.token or os.environ.get('TELEGRAM_BOT_TOKEN')
    
    if not bot_token:
        logger.error("TELEGRAM_BOT_TOKEN is missing")
        sys.exit(1)

    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        logger.error(f"File not found: {args.file}")
        sys.exit(1)

    article_md, telegram_post_md = split_content(content)
    title, author = extract_title_author(article_md)
    html_content = markdown_to_html(article_md)
    
    logger.info(f"Publishing article '{title}' to Telegraph...")
    article_url = publish_to_telegraph(title, author, html_content)
    
    if not article_url:
        logger.error("Failed to get Article URL. Aborting.")
        sys.exit(1)
        
    logger.info(f"Article published: {article_url}")

    if telegram_post_md:
        logger.info("Sending summary to Telegram...")
        final_message = format_telegram_message(telegram_post_md, article_url)
        await send_telegram_message(bot_token, args.chat_id, final_message)
    else:
        logger.warning("No Telegram post content found. Skipping Telegram message.")

if __name__ == "__main__":
    asyncio.run(main())
