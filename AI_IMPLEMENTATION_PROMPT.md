# AI Implementation Prompt - Telegram SMS/Voice Bot

## Overview
Build a complete Telegram bot that allows users to send SMS and make phone calls through Twilio/Onvoy/Google Voice, with integrated payment processing via CryptoCloud and Telegram Payments, user management, and admin dashboard.

## Full Requirements

Read the complete specification in `PROJECT_SPECIFICATION.md` for all details. Here's what to implement:

## Core Functionality

### 1. Telegram Bot (Priority: HIGH)

**Commands to implement:**
```typescript
/start - Register user, create database entry, show welcome
/help - Display all commands with descriptions
/balance - Show current credit balance
/deposit - Start payment process (show payment options)
/sendsms <number> <message> - Send SMS via Twilio
/call <number> - Initiate voice call
/history - Show last 50 SMS/calls
/pricing - Display current rates
/settings - User preferences
/cancel - Cancel current operation

// Admin commands
/admin - Admin dashboard
/users - List all users (paginated)
/userinfo <user_id> - View user details
/addcredits <user_id> <amount> - Manually add credits
/removecredits <user_id> <amount> - Remove credits
/ban <user_id> - Ban user
/unban <user_id> - Unban user
/stats - System statistics
/broadcast <message> - Send to all users
/setprice sms <amount> - Set SMS price
/setprice call <amount> - Set call price per minute
/logs - View system logs
```

**Message Flow:**
1. User sends command
2. Validate user exists (if not, auto-register)
3. Check command permissions
4. Execute command logic
5. Update database
6. Send response to user
7. Log action

### 2. SMS Functionality (Priority: HIGH)

**Implementation:**
```typescript
async function sendSMS(userId: number, phoneNumber: string, message: string) {
  // 1. Validate phone number (libphonenumber-js)
  // 2. Check user balance >= SMS_PRICE
  // 3. Deduct credits from balance
  // 4. Try sending via Twilio
  // 5. If fails, fallback to Onvoy
  // 6. If fails, fallback to Google Voice
  // 7. Log transaction to sms_history table
  // 8. Update user stats (sms_sent++)
  // 9. Send confirmation to user
  // 10. Monitor delivery status (webhook)
}
```

**Database logging:**
- Store in `sms_history` table
- Track: user_id, to_number, message, cost, provider, status, timestamps
- Update transaction in `transactions` table

### 3. Voice Call Functionality (Priority: HIGH)

**Implementation:**
```typescript
async function initiateCall(userId: number, phoneNumber: string) {
  // 1. Validate phone number
  // 2. Check minimum balance (at least 1 minute)
  // 3. Show estimated cost
  // 4. Wait for user confirmation (inline keyboard)
  // 5. Initiate call via Twilio
  // 6. Track call duration in real-time
  // 7. Deduct credits per minute
  // 8. Log to call_history table
  // 9. Send call summary when ended
}
```

**Real-time tracking:**
- Use Twilio webhooks for call events
- Update database with duration
- Calculate final cost
- Deduct from user balance

### 4. Payment System (Priority: HIGH)

**CryptoCloud Integration:**
```typescript
async function createCryptoPayment(userId: number, amount: number) {
  // 1. Calculate credits based on amount
  // 2. Create payment via CryptoCloud API
  // 3. Generate unique payment_id
  // 4. Store in payments table (status: pending)
  // 5. Return payment URL + QR code
  // 6. Send to user with inline keyboard
  // 7. Setup polling to check payment status
  // 8. On success: add credits, update status, notify user
}
```

**Telegram Payments Integration:**
```typescript
async function createTelegramInvoice(userId: number, packageId: number) {
  // 1. Get package details (price, credits)
  // 2. Create invoice using Telegram API
  // 3. Send invoice to user
  // 4. Handle pre_checkout_query (verify user, amount)
  // 5. Answer pre_checkout_query (True/False)
  // 6. Handle successful_payment
  // 7. Add credits to user balance
  // 8. Send receipt
}
```

**Credit Packages:**
```typescript
const packages = [
  { amount: 5, credits: 500, bonus: 0 },
  { amount: 10, credits: 1100, bonus: 100 },
  { amount: 25, credits: 2875, bonus: 375 },
  { amount: 50, credits: 6000, bonus: 1000 },
  { amount: 100, credits: 13000, bonus: 3000 }
];
```

### 5. Database Schema (Priority: HIGH)

**Implement these tables using Prisma:**

```prisma
model User {
  id                  Int       @id @default(autoincrement())
  telegramId          BigInt    @unique
  username            String?
  firstName           String?
  lastName            String?
  phoneNumber         String?
  email               String?
  balance             Decimal   @default(0)
  role                String    @default("user")
  status              String    @default("active")
  language            String    @default("en")
  notificationsEnabled Boolean  @default(true)
  totalSpent          Decimal   @default(0)
  smsSent             Int       @default(0)
  callsMade           Int       @default(0)
  registrationDate    DateTime  @default(now())
  lastActive          DateTime  @default(now())
  createdAt           DateTime  @default(now())
  updatedAt           DateTime  @updatedAt

  transactions        Transaction[]
  payments            Payment[]
  smsHistory          SmsHistory[]
  callHistory         CallHistory[]
}

model Transaction {
  id             Int       @id @default(autoincrement())
  userId         Int
  telegramId     BigInt
  type           String
  amount         Decimal
  balanceBefore  Decimal?
  balanceAfter   Decimal?
  description    String?
  metadata       Json?
  status         String    @default("completed")
  createdAt      DateTime  @default(now())

  user           User      @relation(fields: [userId], references: [id])
}

model Payment {
  id                String    @id @default(uuid())
  userId            Int
  telegramId        BigInt
  paymentId         String    @unique
  paymentMethod     String
  amount            Decimal
  credits           Int
  currency          String    @default("USD")
  status            String    @default("pending")
  paymentUrl        String?
  paymentAddress    String?
  providerData      Json?
  completedAt       DateTime?
  createdAt         DateTime  @default(now())
  updatedAt         DateTime  @updatedAt

  user              User      @relation(fields: [userId], references: [id])
}

model SmsHistory {
  id                  Int       @id @default(autoincrement())
  userId              Int
  telegramId          BigInt
  toNumber            String
  message             String
  messageLength       Int?
  cost                Decimal
  provider            String
  providerMessageId   String?
  status              String    @default("pending")
  errorMessage        String?
  countryCode         String?
  sentAt              DateTime  @default(now())
  deliveredAt         DateTime?
  createdAt           DateTime  @default(now())

  user                User      @relation(fields: [userId], references: [id])
}

model CallHistory {
  id                Int       @id @default(autoincrement())
  userId            Int
  telegramId        BigInt
  toNumber          String
  duration          Int       @default(0)
  cost              Decimal   @default(0)
  provider          String
  providerCallId    String?
  status            String    @default("initiated")
  recordingUrl      String?
  errorMessage      String?
  countryCode       String?
  startedAt         DateTime  @default(now())
  endedAt           DateTime?
  createdAt         DateTime  @default(now())

  user              User      @relation(fields: [userId], references: [id])
}

model SystemSettings {
  id          Int       @id @default(autoincrement())
  key         String    @unique
  value       String
  dataType    String    @default("string")
  description String?
  updatedBy   Int?
  updatedAt   DateTime  @default(now())
}
```

### 6. Admin Panel (Priority: MEDIUM)

**Implement these functions:**
```typescript
// List users with pagination
async function listUsers(page: number, limit: number)

// View user details
async function getUserDetails(userId: number)

// Modify user balance
async function modifyBalance(userId: number, amount: number, reason: string)

// Ban/unban user
async function toggleUserBan(userId: number)

// System statistics
async function getSystemStats()

// Broadcast message
async function broadcastMessage(message: string, adminId: number)

// Update pricing
async function updatePricing(service: 'sms' | 'call', price: number)
```

### 7. Twilio Integration (Priority: HIGH)

**Required services:**
```typescript
// SMS Service
class TwilioSmsService {
  async sendSMS(to: string, message: string): Promise<{
    success: boolean;
    messageId?: string;
    error?: string;
  }>;

  async getDeliveryStatus(messageId: string): Promise<string>;
}

// Voice Service
class TwilioVoiceService {
  async initiateCall(to: string): Promise<{
    success: boolean;
    callId?: string;
    error?: string;
  }>;

  async getCallStatus(callId: string): Promise<{
    status: string;
    duration: number;
  }>;
}
```

### 8. Security & Validation (Priority: HIGH)

**Implement:**
- Rate limiting (max 30 requests/minute per user)
- Phone number validation using libphonenumber-js
- SQL injection prevention (Prisma handles this)
- Input sanitization for all text inputs
- Webhook signature verification
- Admin permission checks
- API key security (environment variables)

### 9. Error Handling (Priority: MEDIUM)

**Implement global error handler:**
```typescript
class BotError extends Error {
  constructor(
    message: string,
    public code: string,
    public userMessage?: string
  ) {
    super(message);
  }
}

// Usage
try {
  await sendSMS(userId, phone, message);
} catch (error) {
  if (error instanceof BotError) {
    await bot.sendMessage(userId, error.userMessage);
  }
  logger.error('SMS send failed', error);
}
```

### 10. Logging (Priority: MEDIUM)

**Winston logger setup:**
```typescript
import winston from 'winston';

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' }),
  ],
});

// Log all important actions
logger.info('SMS sent', { userId, phone, cost });
logger.error('Payment failed', { userId, paymentId, error });
```

## Tech Stack to Use

```json
{
  "dependencies": {
    "node-telegram-bot-api": "^0.64.0",
    "express": "^4.18.2",
    "prisma": "^5.0.0",
    "@prisma/client": "^5.0.0",
    "twilio": "^4.19.0",
    "axios": "^1.6.0",
    "redis": "^4.6.0",
    "ioredis": "^5.3.0",
    "bull": "^4.11.0",
    "winston": "^3.11.0",
    "dotenv": "^16.3.1",
    "libphonenumber-js": "^1.10.0",
    "express-rate-limit": "^7.1.0",
    "helmet": "^7.1.0",
    "cors": "^2.8.5"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "typescript": "^5.3.0",
    "ts-node": "^10.9.0",
    "nodemon": "^3.0.0",
    "@types/express": "^4.17.0"
  }
}
```

## File Structure to Create

```
telegram-sms-bot/
├── src/
│   ├── index.ts                    # Main entry point
│   ├── bot.ts                      # Telegram bot setup
│   ├── app.ts                      # Express app
│   ├── config/
│   │   ├── database.ts             # Prisma client
│   │   ├── redis.ts                # Redis client
│   │   └── telegram.ts             # Bot config
│   ├── services/
│   │   ├── twilioService.ts        # Twilio SMS/Voice
│   │   ├── cryptoCloudService.ts   # CryptoCloud payments
│   │   ├── paymentService.ts       # Payment orchestration
│   │   └── balanceService.ts       # Credit management
│   ├── handlers/
│   │   ├── commandHandler.ts       # Bot commands
│   │   ├── callbackHandler.ts      # Inline keyboard callbacks
│   │   └── paymentHandler.ts       # Payment webhooks
│   ├── controllers/
│   │   ├── userController.ts       # User operations
│   │   ├── smsController.ts        # SMS operations
│   │   ├── callController.ts       # Call operations
│   │   └── adminController.ts      # Admin operations
│   ├── middlewares/
│   │   ├── auth.ts                 # Authentication
│   │   ├── rateLimit.ts            # Rate limiting
│   │   └── errorHandler.ts         # Error handling
│   └── utils/
│       ├── logger.ts               # Winston logger
│       ├── validator.ts            # Input validation
│       └── phoneNumber.ts          # Phone formatting
├── prisma/
│   └── schema.prisma               # Database schema
├── .env.example                    # Environment template
├── package.json
├── tsconfig.json
└── ecosystem.config.js             # PM2 config
```

## Implementation Steps

### Step 1: Project Setup
1. Initialize Node.js project with TypeScript
2. Install all dependencies
3. Setup Prisma with PostgreSQL
4. Configure environment variables
5. Create basic Express app
6. Setup Winston logger

### Step 2: Database
1. Create Prisma schema with all models
2. Run migrations
3. Create seed data (admin user, default settings)
4. Test database connections

### Step 3: Telegram Bot
1. Setup bot with node-telegram-bot-api
2. Configure webhook
3. Implement /start command (user registration)
4. Implement /help command
5. Implement /balance command
6. Test basic bot functionality

### Step 4: SMS Functionality
1. Integrate Twilio SDK
2. Implement sendSMS function
3. Add phone number validation
4. Add balance checking
5. Create SMS history logging
6. Setup delivery status webhook
7. Test with real phone number

### Step 5: Voice Calls
1. Implement Twilio Voice
2. Create initiateCall function
3. Add call duration tracking
4. Implement per-minute billing
5. Setup call status webhooks
6. Test voice calling

### Step 6: Payments
1. Integrate CryptoCloud API
2. Implement payment creation
3. Setup payment webhooks
4. Integrate Telegram Payments
5. Create credit packages
6. Test full payment flow

### Step 7: Admin Panel
1. Implement admin commands
2. Create user listing with pagination
3. Add balance modification
4. Implement statistics
5. Add broadcast messaging
6. Test all admin functions

### Step 8: Error Handling & Logging
1. Setup global error handler
2. Add try-catch blocks everywhere
3. Implement user-friendly error messages
4. Add comprehensive logging
5. Test error scenarios

### Step 9: Testing
1. Write unit tests
2. Test all commands
3. Test payment flows
4. Test SMS/call sending
5. Load testing

### Step 10: Deployment
1. Setup VPS server
2. Install PostgreSQL, Redis, Nginx
3. Configure SSL
4. Deploy code
5. Start with PM2
6. Monitor logs

## Environment Variables Needed

```env
# Telegram
TELEGRAM_BOT_TOKEN=
TELEGRAM_ADMIN_IDS=

# Database
DATABASE_URL=
REDIS_URL=

# Twilio
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=

# CryptoCloud
CRYPTOCLOUD_API_KEY=
CRYPTOCLOUD_SHOP_ID=
CRYPTOCLOUD_WEBHOOK_SECRET=

# Telegram Payments
TELEGRAM_PAYMENT_PROVIDER_TOKEN=

# Pricing
SMS_PRICE_DOMESTIC=1
SMS_PRICE_INTERNATIONAL=3
CALL_PRICE_DOMESTIC_PER_MINUTE=2
CALL_PRICE_INTERNATIONAL_PER_MINUTE=5

# System
NODE_ENV=production
PORT=3000
```

## Testing Checklist

- [ ] User can register with /start
- [ ] User can check balance
- [ ] User can initiate payment
- [ ] CryptoCloud payment works
- [ ] Telegram payment works
- [ ] Credits added after payment
- [ ] User can send SMS
- [ ] SMS delivered successfully
- [ ] Balance deducted correctly
- [ ] User can make call
- [ ] Call duration tracked
- [ ] Per-minute billing works
- [ ] History shows transactions
- [ ] Admin can list users
- [ ] Admin can modify balance
- [ ] Admin can ban users
- [ ] Statistics accurate
- [ ] Broadcast works
- [ ] Rate limiting works
- [ ] Error messages clear
- [ ] Logs captured properly

## Success Criteria

1. Bot responds to all commands
2. SMS successfully sent and delivered
3. Voice calls connect and track duration
4. Payments process correctly (crypto & Telegram)
5. Credits added to user balance
6. Admin panel fully functional
7. Database logging complete
8. No critical errors in logs
9. System handles 100+ concurrent users
10. Response time < 2 seconds

## Additional Features (Optional)

- Scheduled SMS
- Bulk SMS from CSV
- Message templates
- Contact management
- Call recording
- Two-way SMS
- Email notifications
- Referral program
- API for developers
- Mobile app

## Support Documents

- Full specification: `PROJECT_SPECIFICATION.md`
- README: `TELEGRAM_SMS_BOT_README.md`
- API docs: Create OpenAPI spec
- User guide: Write step-by-step guide
- Admin manual: Document all admin functions

---

## Start Implementation Now

Begin with Step 1 and work sequentially. Focus on core functionality first (Steps 1-6), then add admin panel and polish (Steps 7-10).

**First Code to Write:**

```typescript
// src/index.ts
import TelegramBot from 'node-telegram-bot-api';
import express from 'express';
import dotenv from 'dotenv';
import { PrismaClient } from '@prisma/client';

dotenv.config();

const bot = new TelegramBot(process.env.TELEGRAM_BOT_TOKEN!, { polling: true });
const app = express();
const prisma = new PrismaClient();

// Start command
bot.onText(/\/start/, async (msg) => {
  const chatId = msg.chat.id;
  const telegramId = msg.from!.id;

  // Check if user exists
  let user = await prisma.user.findUnique({
    where: { telegramId }
  });

  // Create user if doesn't exist
  if (!user) {
    user = await prisma.user.create({
      data: {
        telegramId,
        username: msg.from!.username,
        firstName: msg.from!.first_name,
        lastName: msg.from!.last_name,
      }
    });
  }

  await bot.sendMessage(chatId, `Welcome! Your balance: ${user.balance} credits`);
});

// Start server
app.listen(process.env.PORT || 3000, () => {
  console.log('Bot started');
});
```

**Now implement the rest following the specification!**
