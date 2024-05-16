from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

def register(application, api, hooks):
    async def create_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.message.from_user.id
        wallet = api.execute_action('wallet', 'get_wallet', user_id)
        if wallet is None:
            wallet = {'balance': 0}
            api.execute_action('wallet', 'set_wallet', user_id, wallet)
        await update.message.reply_text(f'Your wallet has been created with a balance of {wallet["balance"]}.')

    def get_wallet(user_id):
        return api.db.get(f'wallet_{user_id}', {'balance': 0})

    def set_wallet(user_id, wallet):
        api.db.set(f'wallet_{user_id}', wallet)

    def modify_wallet_balance(user_id, amount):
        wallet = get_wallet(user_id)
        wallet['balance'] += amount
        set_wallet(user_id, wallet)

    # Register actions with the core API
    api.register_action('wallet', 'get_wallet', get_wallet)
    api.register_action('wallet', 'set_wallet', set_wallet)
    api.register_action('wallet', 'modify_wallet_balance', modify_wallet_balance)

    application.add_handler(CommandHandler('create_wallet', create_wallet))
