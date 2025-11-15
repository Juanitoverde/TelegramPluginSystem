# Telegram SMS/Voice Bot - Complete Project

A powerful Telegram bot that enables users to send SMS messages and make voice calls through integrated telephony services, with built-in payment processing and credit management.

## 🚀 Features

- **📱 SMS Sending**: Send text messages to any phone number worldwide
- **📞 Voice Calls**: Make phone calls with real-time duration tracking
- **💳 Multiple Payment Methods**: CryptoCloud (crypto) and Telegram Payments (cards/Stars)
- **👥 User Management**: Complete admin dashboard for user oversight
- **💰 Credit System**: Flexible credit-based billing
- **📊 Analytics**: Comprehensive statistics and reporting
- **🌍 Multi-Provider**: Twilio, Onvoy, and Google Voice integration with automatic fallback
- **🔒 Secure**: Enterprise-grade security and encryption
- **⚡ Fast**: Redis caching for optimal performance

## 📋 Quick Start

### Prerequisites

- Node.js 18+
- PostgreSQL 14+
- Redis 6+
- Telegram Bot Token
- Twilio Account
- CryptoCloud Account

### Installation

```bash
# Clone repository
git clone <repository-url>
cd telegram-sms-bot

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Setup database
npx prisma migrate dev

# Start bot
npm run dev
```

## 💳 Payment Configuration

### CryptoCloud
1. Register at cryptocloud.plus
2. Get API key and Shop ID
3. Configure webhook URL

### Telegram Payments
1. Talk to @BotFather
2. Connect payment provider
3. Get provider token

## 📱 Bot Commands

**User Commands:**
- `/start` - Register
- `/balance` - Check credits
- `/deposit` - Add credits
- `/sendsms +1234567890 message` - Send SMS
- `/call +1234567890` - Make call
- `/history` - View history

**Admin Commands:**
- `/admin` - Admin panel
- `/users` - List users
- `/stats` - Statistics
- `/addcredits <user_id> <amount>` - Add credits

## 🏗️ Architecture

See `PROJECT_SPECIFICATION.md` for complete technical details.

## 📄 License

MIT License - See LICENSE file

## 🆘 Support

See documentation in `docs/` folder
