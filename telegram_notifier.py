#!/usr/bin/env python3
"""
Telegram Notification Module for $1000/Week Passive Income System
Sends alerts and notifications via Telegram Bot
"""

import os
import asyncio
import aiohttp
from datetime import datetime
from typing import Optional, Dict, Any
import json

class TelegramNotifier:
    """Telegram notification handler for business alerts"""
    
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        self.enabled = os.getenv('TELEGRAM_ENABLED', 'true').lower() == 'true'
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
        
    async def send_message(self, message: str, parse_mode: str = 'HTML') -> Dict[str, Any]:
        """Send a message to Telegram"""
        if not self.enabled or not self.bot_token or not self.chat_id:
            return {"status": "disabled", "message": "Telegram not configured"}
        
        url = f"{self.base_url}/sendMessage"
        payload = {
            'chat_id': self.chat_id,
            'text': message,
            'parse_mode': parse_mode,
            'disable_web_page_preview': False
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    result = await response.json()
                    if result.get('ok'):
                        return {"status": "success", "message_id": result['result']['message_id']}
                    else:
                        return {"status": "error", "error": result.get('description')}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    # ==================== BUSINESS ALERTS ====================
    
    async def alert_new_payment(self, amount: float, plan: str, customer_email: str) -> Dict:
        """Alert when a new payment is received"""
        message = f"""
💰 <b>NEW PAYMENT RECEIVED!</b>

Amount: <b>${amount:.2f}</b>
Plan: {plan}
Customer: {customer_email}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🎉 Keep it rolling!
"""
        return await self.send_message(message)
    
    async def alert_new_lead(self, email: str, source: str, lead_magnet: str) -> Dict:
        """Alert when a new lead is captured"""
        message = f"""
🎯 <b>NEW LEAD CAPTURED!</b>

Email: {email}
Source: {source}
Lead Magnet: {lead_magnet}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📈 Pipeline growing!
"""
        return await self.send_message(message)
    
    async def alert_new_customer(self, email: str, plan: str) -> Dict:
        """Alert when a new customer signs up"""
        message = f"""
🎉 <b>NEW CUSTOMER!</b>

Email: {email}
Plan: {plan}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🚀 Another one joins the revolution!
"""
        return await self.send_message(message)
    
    async def alert_churn(self, email: str, plan: str, reason: str) -> Dict:
        """Alert when a customer cancels"""
        message = f"""
😢 <b>CUSTOMER CHURNED</b>

Email: {email}
Plan: {plan}
Reason: {reason}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

💡 Consider reaching out for feedback.
"""
        return await self.send_message(message)
    
    # ==================== REVENUE ALERTS ====================
    
    async def alert_revenue_milestone(self, amount: float, milestone: str) -> Dict:
        """Alert when revenue milestone is hit"""
        message = f"""
🏆 <b>REVENUE MILESTONE!</b>

You've hit: <b>{milestone}</b>
Total Revenue: <b>${amount:.2f}</b>
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🎯 Next target: {self._next_milestone(amount)}
"""
        return await self.send_message(message)
    
    async def alert_daily_revenue(self, revenue: float, new_customers: int) -> Dict:
        """Daily revenue summary"""
        message = f"""
📊 <b>DAILY REVENUE REPORT</b>

Revenue: <b>${revenue:.2f}</b>
New Customers: {new_customers}
Date: {datetime.now().strftime('%Y-%m-%d')}

{self._revenue_emoji(revenue)} Keep pushing!
"""
        return await self.send_message(message)
    
    async def alert_weekly_revenue(self, revenue: float, target: float = 1000) -> Dict:
        """Weekly revenue summary"""
        percentage = (revenue / target) * 100
        progress_bar = self._progress_bar(percentage)
        
        message = f"""
📈 <b>WEEKLY REVENUE REPORT</b>

Revenue: <b>${revenue:.2f}</b>
Target: ${target:.2f}
Progress: {progress_bar} {percentage:.1f}%

{self._weekly_status(revenue, target)}
"""
        return await self.send_message(message)
    
    async def alert_revenue_drop(self, current: float, previous: float) -> Dict:
        """Alert when revenue drops significantly"""
        drop_percent = ((previous - current) / previous) * 100
        message = f"""
⚠️ <b>REVENUE DROP ALERT!</b>

Previous: ${previous:.2f}
Current: ${current:.2f}
Drop: <b>{drop_percent:.1f}%</b>

🔍 Investigate immediately!
"""
        return await self.send_message(message)
    
    # ==================== SYSTEM ALERTS ====================
    
    async def alert_system_error(self, error: str, service: str) -> Dict:
        """Alert on system errors"""
        message = f"""
🚨 <b>SYSTEM ERROR!</b>

Service: {service}
Error: {error}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

⚡ Action required!
"""
        return await self.send_message(message)
    
    async def alert_api_down(self, service: str) -> Dict:
        """Alert when external API is down"""
        message = f"""
🔴 <b>API DOWN!</b>

Service: {service}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🔄 Failover activated.
"""
        return await self.send_message(message)
    
    async def alert_high_error_rate(self, error_rate: float, threshold: float) -> Dict:
        """Alert when error rate exceeds threshold"""
        message = f"""
⚠️ <b>HIGH ERROR RATE!</b>

Current: {error_rate:.1f}%
Threshold: {threshold:.1f}%
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🔧 Check system health!
"""
        return await self.send_message(message)
    
    # ==================== CONTENT ALERTS ====================
    
    async def alert_content_published(self, title: str, url: str, platform: str) -> Dict:
        """Alert when content is published"""
        message = f"""
✍️ <b>CONTENT PUBLISHED!</b>

Title: {title}
Platform: {platform}
URL: {url}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📢 Content machine is rolling!
"""
        return await self.send_message(message)
    
    async def alert_daily_content_complete(self, articles: int, social_posts: int) -> Dict:
        """Daily content creation summary"""
        message = f"""
📝 <b>DAILY CONTENT COMPLETE!</b>

Articles: {articles}
Social Posts: {social_posts}
Date: {datetime.now().strftime('%Y-%m-%d')}

🤖 AI working 24/7!
"""
        return await self.send_message(message)
    
    # ==================== SUPPORT ALERTS ====================
    
    async def alert_support_ticket(self, email: str, issue: str, priority: str) -> Dict:
        """Alert on new support tickets"""
        emoji = "🔴" if priority == "urgent" else "🟡" if priority == "high" else "🟢"
        message = f"""
{emoji} <b>NEW SUPPORT TICKET!</b>

From: {email}
Priority: {priority}
Issue: {issue[:100]}...
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

👀 Check dashboard!
"""
        return await self.send_message(message)
    
    async def alert_support_escalation(self, email: str, reason: str) -> Dict:
        """Alert when ticket needs human escalation"""
        message = f"""
🆘 <b>SUPPORT ESCALATION!</b>

Customer: {email}
Reason: {reason}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

👤 Human intervention needed!
"""
        return await self.send_message(message)
    
    # ==================== SUMMARY REPORTS ====================
    
    async def send_daily_summary(self, stats: Dict[str, Any]) -> Dict:
        """Send daily business summary"""
        message = f"""
📅 <b>DAILY BUSINESS SUMMARY</b>
Date: {datetime.now().strftime('%Y-%m-%d')}

💰 Revenue: ${stats.get('revenue', 0):.2f}
👥 New Leads: {stats.get('new_leads', 0)}
🎉 New Customers: {stats.get('new_customers', 0)}
📝 Content Published: {stats.get('content_published', 0)}
🎫 Support Tickets: {stats.get('support_tickets', 0)}

{self._daily_status(stats)}
"""
        return await self.send_message(message)
    
    async def send_weekly_summary(self, stats: Dict[str, Any]) -> Dict:
        """Send weekly business summary"""
        message = f"""
📊 <b>WEEKLY BUSINESS SUMMARY</b>
Week: {datetime.now().strftime('%Y-%m-%d')}

💰 Total Revenue: ${stats.get('revenue', 0):.2f}
📈 vs Last Week: {stats.get('growth', 0):+.1f}%
👥 New Leads: {stats.get('new_leads', 0)}
🎉 New Customers: {stats.get('new_customers', 0)}
💔 Churned: {stats.get('churned', 0)}
📝 Content Pieces: {stats.get('content_published', 0)}
⭐ Avg Response Time: {stats.get('avg_response_time', 0)}min

{self._weekly_business_status(stats)}
"""
        return await self.send_message(message)
    
    # ==================== HELPER METHODS ====================
    
    def _progress_bar(self, percentage: float, length: int = 10) -> str:
        """Generate ASCII progress bar"""
        filled = int(length * percentage / 100)
        bar = '█' * filled + '░' * (length - filled)
        return bar
    
    def _next_milestone(self, current: float) -> str:
        """Calculate next revenue milestone"""
        milestones = [100, 500, 1000, 2000, 5000, 10000, 20000]
        for m in milestones:
            if current < m:
                return f"${m}"
        return f"${int(current * 1.5)}"
    
    def _revenue_emoji(self, revenue: float) -> str:
        """Get appropriate emoji for revenue level"""
        if revenue >= 500:
            return "🔥"
        elif revenue >= 200:
            return "💪"
        elif revenue > 0:
            return "📈"
        else:
            return "💤"
    
    def _weekly_status(self, revenue: float, target: float) -> str:
        """Generate weekly status message"""
        if revenue >= target:
            return "🎉 TARGET HIT! Amazing work!"
        elif revenue >= target * 0.8:
            return "💪 So close! Push for the finish line!"
        elif revenue >= target * 0.5:
            return "📈 Halfway there! Keep grinding!"
        else:
            return "🚀 Let's ramp it up next week!"
    
    def _daily_status(self, stats: Dict) -> str:
        """Generate daily status message"""
        revenue = stats.get('revenue', 0)
        leads = stats.get('new_leads', 0)
        
        if revenue > 100 and leads > 5:
            return "🔥 Killing it today!"
        elif revenue > 0 or leads > 0:
            return "📈 Good progress!"
        else:
            return "💤 Quiet day. Tomorrow we hustle!"
    
    def _weekly_business_status(self, stats: Dict) -> str:
        """Generate weekly business status"""
        growth = stats.get('growth', 0)
        if growth > 20:
            return "🚀 Explosive growth! Keep it up!"
        elif growth > 0:
            return "📈 Steady growth! Good momentum!"
        elif growth == 0:
            return "➡️ Flat week. Time to experiment!"
        else:
            return "📉 Dip this week. Let's analyze and improve!"


# ==================== SYNC WRAPPERS ====================

def send_telegram_alert(message: str) -> Dict:
    """Synchronous wrapper for sending alerts"""
    notifier = TelegramNotifier()
    return asyncio.run(notifier.send_message(message))

def alert_new_payment_sync(amount: float, plan: str, customer_email: str) -> Dict:
    """Synchronous wrapper for payment alerts"""
    notifier = TelegramNotifier()
    return asyncio.run(notifier.alert_new_payment(amount, plan, customer_email))

def alert_new_lead_sync(email: str, source: str, lead_magnet: str) -> Dict:
    """Synchronous wrapper for lead alerts"""
    notifier = TelegramNotifier()
    return asyncio.run(notifier.alert_new_lead(email, source, lead_magnet))


# ==================== TEST SCRIPT ====================

if __name__ == "__main__":
    async def test_telegram():
        """Test Telegram notifications"""
        print("🧪 Testing Telegram notifications...")
        
        notifier = TelegramNotifier()
        
        # Test basic message
        print("\n1. Testing basic message...")
        result = await notifier.send_message("<b>Test Message</b>\n\nYour Telegram bot is working! 🎉")
        print(f"Result: {result}")
        
        # Test new payment alert
        print("\n2. Testing payment alert...")
        result = await notifier.alert_new_payment(97.00, "Pro", "customer@example.com")
        print(f"Result: {result}")
        
        # Test new lead alert
        print("\n3. Testing lead alert...")
        result = await notifier.alert_new_lead("lead@example.com", "Twitter", "Free Guide")
        print(f"Result: {result}")
        
        # Test daily summary
        print("\n4. Testing daily summary...")
        stats = {
            'revenue': 324.00,
            'new_leads': 12,
            'new_customers': 3,
            'content_published': 2,
            'support_tickets': 1
        }
        result = await notifier.send_daily_summary(stats)
        print(f"Result: {result}")
        
        print("\n✅ All tests completed!")
    
    # Run tests
    asyncio.run(test_telegram())
