# EtheryaBot

EtheryaBot is a Discord bot designed to manage various functionalities such as loans, investments, and business management within a Discord server. This bot utilizes JSON files for data persistence, ensuring that user data and configurations are retained even after the bot restarts.

## Features

- **Embed Creation**: Easily create and send rich embeds to Discord channels.
- **Loan Management**: Users can request loans, check their statuses, and manage repayments.
- **Livret A Management**: Users can invest, withdraw, and check their balances in a simulated savings account.
- **Business Management**: Users can construct businesses, collect revenues, and manage their business status.
- **Automatic Role Assignment**: New members are automatically assigned roles upon joining the server.
- **Help Command**: Users can access a list of available commands and their descriptions.

## File Structure

```
EtheryaBot
├── commands
│   ├── __init__.py
│   ├── embed.py
│   ├── frags.py
│   ├── pret.py
│   ├── livret_a.py
│   ├── entreprise.py
│   ├── calcul.py
│   ├── auto_clan.py
│   └── help.py
├── data
│   ├── prets.json
│   ├── livret_a.json
│   ├── entreprises.json
│   └── config.json
├── utils
│   ├── __init__.py
│   ├── database.py
│   └── keep_alive.py
├── main.py
└── README.md
```

## Setup Instructions

1. **Clone the Repository**: 
   ```
   git clone <repository-url>
   cd EtheryaBot
   ```

2. **Install Dependencies**: 
   Ensure you have Python 3.8 or higher installed. Install the required libraries using pip:
   ```
   pip install discord.py
   ```

3. **Configure the Bot**: 
   Edit the `data/config.json` file to include your bot token and any necessary channel IDs.

4. **Run the Bot**: 
   Execute the main script to start the bot:
   ```
   python main.py
   ```

## Usage

- Use commands prefixed with `!!` to interact with the bot.
- For a list of available commands, type `!!help`.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.