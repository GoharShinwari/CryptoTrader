# CryptoTrader

CryptoTrader is a Python script that simulates a simple cryptocurrency trading environment using the CoinMarketCap API. This program allows users to buy and sell Bitcoin (BTC) and Ethereum (ETH) based on their bank balance and current market prices.

## Features

- Initializes bank balance and cryptocurrency balances (BTC and ETH) using a JSON file.
- Retrieves real-time cryptocurrency prices from CoinMarketCap API.
- Allows users to:
  - View their bank balance and cryptocurrency balances.
  - Buy BTC or ETH using their bank balance.
  - Sell BTC or ETH to increase their bank balance.
- Periodically updates cryptocurrency prices to reflect current market conditions.

## Prerequisites

Before running the script, ensure you have the following installed:

- Python 3.x
- Required Python libraries (`coinmarketcapapi`, `twython`)

## Setup

1. Clone the repository:

   git clone https://github.com/GoharShinwari/CryptoTrader.git

2. Obtain API Keys:

   - CoinMarketCap API Key: Sign up on the CoinMarketCap website and obtain an API key. Add this key to your config.py file or set it as an environment variable.

3. Configure config.py:

   - Create a config.py file in the root directory and add your API keys:

     api_key = "YOUR_COINMARKETCAP_API_KEY_HERE"

   Note: Ensure you keep this file secure and do not expose your API keys publicly.

## Usage:

Run the script by executing the following command:

python crypto_trader.py

Follow the on-screen instructions to interact with the CryptoTrader application. Input 'Y' or 'N' to make buying or selling decisions and follow the prompts.

Disclaimer:

This script is for educational purposes and simulates cryptocurrency trading in a controlled environment. Be cautious when dealing with real investments and always do thorough research before making financial decisions.
