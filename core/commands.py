from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
import logging

# Configure logger for debugging
logger = logging.getLogger(__name__)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = "Available commands:\n"
    try:
        # Logging the total number of handler groups
        logger.debug(f"Total handler groups: {len(context.application.handlers)}")

        # Iterate over all handler groups in the dispatcher
        for idx, group in enumerate(context.application.handlers.values()):
            logger.debug(f"Processing handler group {idx} with {len(group)} handlers")
            for handler in group:
                if isinstance(handler, CommandHandler):
                    # Extract the list of commands from the handler
                    commands = handler.commands
                    command_list = '/'.join(commands) if commands else "unknown"
                    description = handler.callback.__doc__.strip() if handler.callback.__doc__ else "No description available"
                    help_text += f"/{command_list} - {description}\n"

    except Exception as e:
        logger.error("Failed to generate help text", exc_info=True)
        help_text = f"Error generating help text: {e}"

    await update.message.reply_text(help_text)
