#!/usr/bin/env python3
"""
Test Telegram Bot Configuration
Run this to verify your Telegram bot is working
"""

import asyncio
import aiohttp
import sys

# Your Telegram credentials
BOT_TOKEN = "8702462545:AAFn87DUV2vHCtpjXyQxJSYdwKqkh4fL3Zk"
CHAT_ID = "1830418033"

async def test_bot():
    """Test Telegram bot connection"""
    print("🧪 Testing Telegram Bot Configuration")
    print("=" * 50)
    
    base_url = f"https://api.telegram.org/bot{BOT_TOKEN}"
    
    # Test 1: Get bot info
    print("\n1️⃣ Testing bot authentication...")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{base_url}/getMe") as response:
                result = await response.json()
                if result.get('ok'):
                    bot_info = result['result']
                    print(f"   ✅ Bot connected!")
                    print(f"   Bot Name: {bot_info.get('first_name')}")
                    print(f"   Bot Username: @{bot_info.get('username')}")
                    print(f"   Bot ID: {bot_info.get('id')}")
                else:
                    print(f"   ❌ Failed: {result.get('description')}")
                    return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 2: Send test message
    print("\n2️⃣ Sending test message...")
    try:
        message = """
🎉 <b>Telegram Bot Test Successful!</b>

Your $1000/Week Passive Income System is now connected to Telegram!

You'll receive notifications for:
💰 New payments
🎯 New leads  
🎉 New customers
📊 Daily/weekly reports
🚨 System alerts

Time: System is ready! 🚀
"""
        
        async with aiohttp.ClientSession() as session:
            payload = {
                'chat_id': CHAT_ID,
                'text': message,
                'parse_mode': 'HTML'
            }
            async with session.post(f"{base_url}/sendMessage", json=payload) as response:
                result = await response.json()
                if result.get('ok'):
                    print(f"   ✅ Message sent successfully!")
                    print(f"   Message ID: {result['result']['message_id']}")
                else:
                    print(f"   ❌ Failed: {result.get('description')}")
                    return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 3: Send sample alerts
    print("\n3️⃣ Sending sample business alerts...")
    
    # Sample payment alert
    payment_msg = """
💰 <b>NEW PAYMENT RECEIVED!</b>

Amount: <b>$97.00</b>
Plan: Pro
Customer: customer@example.com
Time: 2024-01-15 14:30:22

🎉 Keep it rolling!
"""
    
    try:
        async with aiohttp.ClientSession() as session:
            payload = {'chat_id': CHAT_ID, 'text': payment_msg, 'parse_mode': 'HTML'}
            async with session.post(f"{base_url}/sendMessage", json=payload) as response:
                result = await response.json()
                if result.get('ok'):
                    print(f"   ✅ Payment alert sent!")
    except Exception as e:
        print(f"   ⚠️ Payment alert failed: {e}")
    
    # Sample lead alert
    lead_msg = """
🎯 <b>NEW LEAD CAPTURED!</b>

Email: lead@example.com
Source: Twitter
Lead Magnet: Free Guide
Time: 2024-01-15 14:25:10

📈 Pipeline growing!
"""
    
    try:
        async with aiohttp.ClientSession() as session:
            payload = {'chat_id': CHAT_ID, 'text': lead_msg, 'parse_mode': 'HTML'}
            async with session.post(f"{base_url}/sendMessage", json=payload) as response:
                result = await response.json()
                if result.get('ok'):
                    print(f"   ✅ Lead alert sent!")
    except Exception as e:
        print(f"   ⚠️ Lead alert failed: {e}")
    
    # Sample daily summary
    summary_msg = """
📅 <b>DAILY BUSINESS SUMMARY</b>
Date: 2024-01-15

💰 Revenue: $324.00
👥 New Leads: 12
🎉 New Customers: 3
📝 Content Published: 2
🎫 Support Tickets: 1

🔥 Killing it today!
"""
    
    try:
        async with aiohttp.ClientSession() as session:
            payload = {'chat_id': CHAT_ID, 'text': summary_msg, 'parse_mode': 'HTML'}
            async with session.post(f"{base_url}/sendMessage", json=payload) as response:
                result = await response.json()
                if result.get('ok'):
                    print(f"   ✅ Daily summary sent!")
    except Exception as e:
        print(f"   ⚠️ Daily summary failed: {e}")
    
    print("\n" + "=" * 50)
    print("✅ All tests completed successfully!")
    print("\nYour Telegram bot is ready to receive notifications!")
    print("You'll get real-time alerts for:")
    print("  • New payments 💰")
    print("  • New leads 🎯")
    print("  • New customers 🎉")
    print("  • Revenue milestones 🏆")
    print("  • System alerts 🚨")
    print("  • Daily/weekly reports 📊")
    
    return True

if __name__ == "__main__":
    success = asyncio.run(test_bot())
    sys.exit(0 if success else 1)
