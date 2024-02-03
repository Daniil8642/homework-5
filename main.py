import aiohttp
import asyncio
import argparse
from datetime import datetime, timedelta
import json
from aiofile import AIOFile

async def fetch_currency_rates(date):
    async with aiohttp.ClientSession() as session:
        url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date}'
        async with session.get(url) as response:
            data = await response.json()
            return data['exchangeRate']

async def get_currency_rates(days):
    today = datetime.now()
    rates = []

    for i in range(days):
        date = (today - timedelta(days=i)).strftime('%d.%m.%Y')
        rates.append({date: await fetch_currency_rates(date)})

    return rates

async def save_to_log(command):
    async with AIOFile("log.txt", "a") as afp:
        await afp.write(command + '\n')

async def chat_exchange_command(days):
    rates = await get_currency_rates(days)
    formatted_rates = json.dumps(rates, indent=2, ensure_ascii=False)
    print(formatted_rates)

    await save_to_log(f"exchange {days}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Currency exchange rates utility")
    parser.add_argument("days", type=int, help="Number of days to retrieve currency rates for")
    args = parser.parse_args()

    asyncio.run(chat_exchange_command(args.days))
