# API Integration Reference

## REST API Client

```python
import requests
from typing import Dict, Optional, List
from requests.auth import HTTPBasicAuth

class APIClient:
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({'Authorization': f'Bearer {api_key}'})
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """GET request."""
        try:
            response = self.session.get(
                f"{self.base_url}/{endpoint.lstrip('/')}",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"API GET error: {e}")
            return None
    
    def post(self, endpoint: str, data: Dict) -> Optional[Dict]:
        """POST request."""
        try:
            response = self.session.post(
                f"{self.base_url}/{endpoint.lstrip('/')}",
                json=data,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"API POST error: {e}")
            return None
```

## Telegram Bot Development

```python
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    await update.message.reply_text('Hello! I am a bot.')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo user message."""
    await update.message.reply_text(update.message.text)

def main():
    """Start the bot."""
    application = Application.builder().token("YOUR_BOT_TOKEN").build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # Start bot
    application.run_polling()

if __name__ == '__main__':
    main()
```
