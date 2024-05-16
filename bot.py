import os
import json
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from utils.database import Database
from core.api import CoreAPI
from core.hooks import Hooks
from core.commands import help_command

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration
with open('config.json') as config_file:
    config = json.load(config_file)

# Initialize the bot
application = Application.builder().token(config['telegram_token']).build()

# Initialize database and core API
db = Database('data/database.json')
api = CoreAPI(db)

# Initialize hooks
hooks = Hooks()

# Load plugins
loaded_plugins = set()
plugin_folder = 'plugins'

def load_plugins():
    for filename in os.listdir(plugin_folder):
        if filename.endswith('.py') and filename != '__init__.py':
            plugin_name = filename[:-3]
            if plugin_name not in loaded_plugins:
                try:
                    module = __import__(f'plugins.{plugin_name}', fromlist=[''])
                    if hasattr(module, 'register'):
                        module.register(application, api, hooks)
                        loaded_plugins.add(plugin_name)
                        logger.info(f'Plugin {plugin_name} loaded successfully.')
                except Exception as e:
                    logger.error(f'Failed to load plugin {plugin_name}: {e}')

load_plugins()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! I am your bot. How can I assist you today?')

application.add_handler(CommandHandler('start', start))
application.add_handler(CommandHandler('help', help_command))

# Define a custom error handler
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
    # Notify the user about the error
    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text("An error occurred while processing your request. Please try again later.")

# Add the error handler to the application
application.add_error_handler(error_handler)

# Start the bot
application.run_polling()
