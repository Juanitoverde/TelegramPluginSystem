from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

def register(application, api, hooks):
    async def add_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
        item_name = ' '.join(context.args)
        store = api.db.get('store', [])
        store.append({'name': item_name, 'price': 100})  # Example price
        api.db.set('store', store)
        await update.message.reply_text(f'Item {item_name} has been added to the store.')

    async def buy_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.message.from_user.id
        item_name = ' '.join(context.args)
        store = api.db.get('store', [])
        for item in store:
            if (item['name'] == item_name):
                if api.execute_action('wallet', 'modify_wallet_balance', user_id, -item['price']):
                    store.remove(item)
                    api.db.set('store', store)
                    await update.message.reply_text(f'You have bought {item_name}.')
                else:
                    await update.message.reply_text('Insufficient balance.')
                break
        else:
            await update.message.reply_text('Item not found.')

    application.add_handler(CommandHandler('add_item', add_item))
    application.add_handler(CommandHandler('buy_item', buy_item))
