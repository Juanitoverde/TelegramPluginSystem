from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

def register(application, api, hooks):
    async def process_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.message.from_user.id
        amount = int(context.args[0])
        transaction_id = context.args[1]
        if api.execute_action('wallet', 'modify_wallet_balance', user_id, amount):
            api.db.set(f'transaction_{transaction_id}', {'user_id': user_id, 'amount': amount, 'verified': True})
            await update.message.reply_text(f'Payment of {amount} processed successfully.')
        else:
            await update.message.reply_text('Payment failed.')

    application.add_handler(CommandHandler('process_payment', process_payment))
