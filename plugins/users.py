from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

def register(application, api, hooks):

    async def register_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Registers a new user."""
        user_id = update.message.from_user.id
        user_data = {'id': user_id, 'username': update.message.from_user.username}
        api.execute_action('users', 'set_user', user_id, user_data)
        await update.message.reply_text('You have been registered!')

    async def admin_modify_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Allows admin to modify a user's balance. (Admin only)"""

        if len(context.args) != 2:
            await update.message.reply_text("Usage: /admin_modify_balance <user_id> <amount>")
            return

        try:
            user_id = int(context.args[0])
            amount = int(context.args[1])
        except ValueError:
            await update.message.reply_text("Invalid user ID or amount. Please use integers.")
            return

        api.execute_action('wallet', 'modify_wallet_balance', user_id, amount)
        await update.message.reply_text(f'User {user_id} balance modified by {amount}.')

    def get_user(user_id):
        return api.db.get(f'user_{user_id}')

    def set_user(user_id, user_data):
        api.db.set(f'user_{user_id}', user_data)

    def update_user(user_id, user_data):
        api.db.update(f'user_{user_id}', user_data)

    def delete_user(user_id):
        api.db.delete(f'user_{user_id}')

    api.register_action('users', 'get_user', get_user)
    api.register_action('users', 'set_user', set_user)
    api.register_action('users', 'update_user', update_user)
    api.register_action('users', 'delete_user', delete_user)

    # Define the plugin commands
    plugin_commands = [
        CommandHandler('register', register_user),
        CommandHandler('admin_modify_balance', admin_modify_balance)
    ]

    # Registering plugin commands with the application and hooks
    for handler in plugin_commands:
        application.add_handler(handler)
    
    # Register the plugin commands with hooks
    hooks.set_plugin_commands("users", plugin_commands)
