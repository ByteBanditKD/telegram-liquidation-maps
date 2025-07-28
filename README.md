# Cryptocurrency Liquidation Maps

This repository provides cryptocurrency liquidation heatmaps from Coinglass in two formats:
1. **Telegram Bot** - Original bot for Telegram integration
2. **MCP Server** - New Model Context Protocol server for LLM integration

## 🚀 Quick Start

### MCP Server (New!)
```bash
# Install dependencies
pip install -r requirements.txt

# Run the MCP server
python liquidation_map_server.py

# Or use the startup script
./start_server.sh

# For web demo
python web_demo.py
```

### Telegram Bot (Original)
```bash
# Create .env file with your bot token
cp example.env .env

# Start with Docker
docker-compose up -d
```

## 🔥 MCP Server Features

The new MCP server enables LLMs to retrieve liquidation maps through natural language:

- 📊 **Real-time Heatmaps**: Captures liquidation heatmaps for supported cryptocurrencies
- 💰 **Price Integration**: Fetches current cryptocurrency prices from CoinGecko
- ⏰ **Multiple Timeframes**: Supports 12 hour, 24 hour, 1 month, and 3 month views
- 🔧 **MCP Compatible**: Works with any MCP-compatible LLM client
- 🖼️ **Image Return**: Returns high-quality PNG images of the heatmaps
- 🌐 **Web Demo**: Includes a web interface for testing
- 🐳 **Docker Support**: Optional Selenium container for headless operation

### Natural Language Examples
- "Retrieve a Bitcoin map on the 24 hour timeframe"
- "Get me an Ethereum liquidation heatmap for 1 month"
- "Show me the current BTC price"
- "What cryptocurrencies are supported?"

## 🤖 Telegram Bot Features

The original Telegram bot provides:

- 📊 **Real-time Heatmaps**: Captures liquidation heatmaps for any supported cryptocurrency
- 💰 **Price Integration**: Shows current cryptocurrency prices alongside heatmaps
- ⏰ **Multiple Timeframes**: Supports 12 hour, 24 hour, 1 month, and 3 month views
- 🤖 **Easy Commands**: Simple Telegram commands for instant access
- 🔄 **Automated Symbol Selection**: Dynamically switches between different cryptocurrencies

### Telegram Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/map <SYMBOL> [TIMEFRAME]` | Get liquidation heatmap | `/map ETH 12 hour` |
| `/start` or `/help` | Show help information | `/help` |

## Supported Cryptocurrencies

- Bitcoin (BTC)
- Ethereum (ETH)
- Binance Coin (BNB)
- Cardano (ADA)
- Solana (SOL)
- Ripple (XRP)
- Polkadot (DOT)
- Dogecoin (DOGE)
- Avalanche (AVAX)
- Polygon (MATIC)

## Supported Timeframes
- `12 hour`
- `24 hour` (default)
- `1 month`
- `3 month`

## 📁 Project Structure

```
├── bot.py                     # Original Telegram bot
├── liquidation_map_server.py  # New MCP server
├── web_demo.py                # Web interface demo
├── test_server.py             # MCP server testing
├── example_usage.py           # Usage examples
├── start_server.sh            # MCP server startup script
├── requirements.txt           # Python dependencies
├── docker-compose.yml         # Docker configuration
├── mcp_config.json           # MCP client configuration
├── PROJECT_SUMMARY.md        # Detailed project summary
└── README.md                 # This file
```

## 🛠️ Setup

### Prerequisites

- Python 3.8+
- Chrome browser (for local mode) or Docker (for Selenium mode)
- For Telegram bot: Telegram Bot Token

### MCP Server Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Option 1: Local Chrome Mode (Recommended for development)**
```bash
python liquidation_map_server.py
```

3. **Option 2: Docker Selenium Mode (Recommended for production)**
```bash
docker-compose up -d selenium
python liquidation_map_server.py
```

4. **Web Demo:**
```bash
python web_demo.py
# Visit http://localhost:8000
```

### Telegram Bot Setup

1. **Create `.env` file:**
```bash
cp example.env .env
# Edit .env with your bot token and channel ID
```

2. **Start with Docker:**
```bash
docker-compose up -d
```

## 🔧 Configuration

### Environment Variables

- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token (for bot only)
- `TELEGRAM_CHANNEL_ID`: Your Telegram channel ID (for bot only)
- `SELENIUM_HOST`: Selenium server host (default: localhost)
- `SELENIUM_PORT`: Selenium server port (default: 4444)

### MCP Client Configuration

Configure your MCP client to use:
```json
{
  "mcpServers": {
    "bitcoin-liquidation-maps": {
      "command": "python",
      "args": ["liquidation_map_server.py"]
    }
  }
}
```

## 🧪 Testing

### MCP Server Testing
```bash
# Basic functionality test
python test_server.py

# Comprehensive examples (includes actual map capture)
python example_usage.py

# Web interface
python web_demo.py
```

### Telegram Bot Testing
Send `/help` to your bot to see available commands.

## 🐳 Docker Configuration

The project uses Docker Compose with services:

- **selenium**: Headless Chrome browser for web scraping
- **bot**: Python application running the Telegram bot (original setup)

For ARM devices (Apple Silicon, Raspberry Pi), use the ARM-specific configuration in `docker-compose.yml`.

## 📊 Usage Examples

### MCP Server (Natural Language)
```
User: "Retrieve a Bitcoin map on the 24 hour timeframe"
LLM: [Calls get_liquidation_map tool and returns image with price info]

User: "What's the current ETH price?"
LLM: [Calls get_crypto_price tool and returns current price]
```

### Telegram Bot (Commands)
```
/map BTC                    # BTC heatmap (24 hour default)
/map ETH 12 hour           # ETH heatmap for 12 hours
/map BTC 1 month           # BTC heatmap for 1 month
/map DOGE 3 month          # DOGE heatmap for 3 months
```

## 🔍 Technical Details

### Architecture
- **Web Scraping**: Selenium WebDriver with Chrome headless
- **Image Processing**: PIL for screenshot optimization
- **API Integration**: CoinGecko API for real-time prices
- **Bot Framework**: pyTelegramBotAPI (original)
- **MCP Protocol**: Model Context Protocol for LLM integration (new)

### Key Components
- `capture_coinglass_heatmap()`: Main scraping function with symbol selection
- `get_crypto_price()`: Fetches current cryptocurrency prices
- `handle_map_command()`: Processes Telegram commands (bot)
- `handle_call_tool()`: Processes MCP tool calls (server)

## 🚨 Troubleshooting

### Common Issues

1. **Chrome driver not found**: Install Chrome browser or use Docker Selenium mode
2. **Selenium connection failed**: Ensure Docker container is running
3. **Website changes**: The scraper may need updates if Coinglass changes their structure
4. **Bot not responding**: Check Telegram token and permissions

### Debug Mode

Enable debug logging by modifying the logging level:
```python
logging.basicConfig(level=logging.DEBUG, ...)
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with different cryptocurrencies and timeframes
5. Submit a pull request

## 📄 License

This project is for educational purposes. Please respect Coinglass's terms of service and rate limits.

## ⚠️ Disclaimer

This tool is for informational purposes only. Cryptocurrency trading involves substantial risk. Always do your own research before making investment decisions.

## 🆕 What's New in MCP Server

The MCP server adds:
- ✅ Natural language interface for LLMs
- ✅ Web demo for easy testing
- ✅ Automatic Chrome driver management
- ✅ Better error handling and fallbacks
- ✅ Comprehensive testing suite
- ✅ Production-ready deployment options

See `PROJECT_SUMMARY.md` for detailed technical information about the MCP server implementation.