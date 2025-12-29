import os
import sys
import argparse
import asyncio
from pathlib import Path
from telegram import Bot
from telegram.constants import ParseMode

# GitHub Pages URL for this repository
GITHUB_PAGES_URL = "https://zlat1109.github.io/wsdc-article/"

def extract_teaser(file_path: Path) -> str:
    """
    Extracts the Telegram teaser from the markdown file.
    Assumes the teaser starts after '# Пост для Telegram-канала'
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the teaser section
    teaser_marker = "# Пост для Telegram-канала"
    if teaser_marker not in content:
        raise ValueError(f"Marker '{teaser_marker}' not found in {file_path}")

    teaser_content = content.split(teaser_marker)[1].strip()
    
    # Remove header lines if present (like **Заголовок:**) to clean it up, 
    # or just keep it as is if the user formatted it specifically.
    # The user's format:
    # **Заголовок:**
    # **Статистика...**
    # ...
    # 🔗 [Ссылка]
    
    # Replace the placeholder link with the actual URL
    teaser_content = teaser_content.replace("[Ссылка]", GITHUB_PAGES_URL)
    
    return teaser_content

async def send_telegram_message(chat_id: str, token: str, message: str):
    """
    Sends the message to Telegram.
    """
    bot = Bot(token=token)
    print(f"Sending message to {chat_id}...")
    try:
        await bot.send_message(chat_id=chat_id, text=message, parse_mode=ParseMode.MARKDOWN)
        print("Successfully sent message to Telegram!")
    except Exception as e:
        print(f"Failed to send message: {e}")
        sys.exit(1)

async def main():
    parser = argparse.ArgumentParser(description='Publish article teaser to Telegram with GitHub Pages link')
    parser.add_argument('--file', type=Path, required=True, help='Path to the article Markdown file source')
    parser.add_argument('--chat-id', type=str, required=True, help='Telegram Chat ID')
    
    args = parser.parse_args()
    
    if not args.file.exists():
        print(f"Error: File {args.file} not found")
        sys.exit(1)

    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        print("Error: TELEGRAM_BOT_TOKEN environment variable not set")
        sys.exit(1)

    try:
        teaser_text = extract_teaser(args.file)
        print("--- Teaser Preview ---")
        print(teaser_text)
        print("----------------------")
        
        await send_telegram_message(args.chat_id, bot_token, teaser_text)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
