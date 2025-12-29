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

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser(description="Publish article to Telegraph and Telegram")
    parser.add_argument("--file", required=True, help="Path to the article markdown file")
    parser.add_argument("--chat-id", required=True, help="Telegram Chat ID")
    parser.add_argument("--token", help="Telegram Bot Token (or use env TELEGRAM_BOT_TOKEN)")
    return parser.parse_args()

def split_content(content):
    """
    Splits the content into Article Body and Telegram Post.
    Looks for specific markers.
    """
    # Marker used in article_draft.md
    marker = "# Пост для Telegram-канала"
    
    if marker in content:
        parts = content.split(marker)
        article_md = parts[0].strip()
        telegram_post_md = parts[1].strip()
        return article_md, telegram_post_md
    
    # Fallback if no marker
    logger.warning(f"Marker '{marker}' not found. Treating entire file as article.")
    return content, None

def markdown_to_html(md_text):
    """
    Converts Markdown to HTML using the markdown library.
    Telegraph doesn't support h1/h2 in content (Title is h1).
    We map:
    # -> h3
    ## -> h4
    ### -> h5
    """
    html = markdown.markdown(md_text)
    
    # Simple tag replacement for Telegraph compatibility
    html = html.replace('<h1>', '<h3>').replace('</h1>', '</h3>')
    html = html.replace('<h2>', '<h4>').replace('</h2>', '</h4>')
    html = html.replace('<h3>', '<h5>').replace('</h3>', '</h5>')
    
    return html

def publish_to_telegraph(title, author, html_content):
    try:
        telegraph = Telegraph()
        # Create a new account or use an existing token if we stored it
        # For now, create a new one for each run (anonymous) or use a fixed one if configured
        # To persist, we'd need to save the token. For this simple bot, creating a new one is fine 
        # but editing won't be possible later. 
        # Better: Allow passing a Telegraph token via env.
        
        telegraph_token = os.environ.get('TELEGRAPH_TOKEN')
        if telegraph_token:
            telegraph = Telegraph(access_token=telegraph_token)
        else:
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
            parse_mode=ParseMode.HTML, # Telegram supports HTML or MarkdownV2. The draft is MD.
            # However, the draft might contain **bold** which is MD. 
            # Let's simple parse bold/italic manually or just send as text if we are lazy.
            # But the user expects formatting.
            # Let's convert basic MD symbols to HTML tags for Telegram
        )
        logger.info(f"Message sent to {chat_id}")
    except Exception as e:
        logger.error(f"Telegram sending failed: {e}")
        sys.exit(1)

def format_telegram_message(text, url):
    """
    Formats the Telegram message:
    1. Replaces [Ссылка] with the actual URL.
    2. Converts basic Markdown (**bold**, *italic*) to HTML for Telegram.
    """
    text = text.replace('[Ссылка]', url)
    
    # Basic Markdown to HTML for Telegram
    # Note: python-telegram-bot's HTML parse mode supports <b>, <i>, <a>, <code>, <pre>
    
    # Bold **text** -> <b>text</b>
    # We use a simple replacement, assuming no nested weirdness
    import re
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    
    # Italic *text* -> <i>text</i> (be careful not to break bullets)
    # We only match * pairs, not single * at start of line
    text = re.sub(r'(?<!\*)\*(?!\*)(.*?)(?<!\*)\*(?!\*)', r'<i>\1</i>', text)
    
    return text

def extract_title_author(md_text):
    """
    Tries to extract Title and Author from the first lines or metadata.
    Default: First H1 line.
    """
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

    # 1. Read File
    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        logger.error(f"File not found: {args.file}")
        sys.exit(1)

    # 2. Split Content
    article_md, telegram_post_md = split_content(content)
    
    # 3. Publish to Telegraph
    title, author = extract_title_author(article_md)
    html_content = markdown_to_html(article_md)
    
    logger.info(f"Publishing article '{title}' to Telegraph...")
    article_url = publish_to_telegraph(title, author, html_content)
    
    if not article_url:
        logger.error("Failed to get Article URL. Aborting.")
        sys.exit(1)
        
    logger.info(f"Article published: {article_url}")

    # 4. Send to Telegram
    if telegram_post_md:
        logger.info("Sending summary to Telegram...")
        final_message = format_telegram_message(telegram_post_md, article_url)
        await send_telegram_message(bot_token, args.chat_id, final_message)
    else:
        logger.warning("No Telegram post content found. Skipping Telegram message.")

if __name__ == "__main__":
    asyncio.run(main())

