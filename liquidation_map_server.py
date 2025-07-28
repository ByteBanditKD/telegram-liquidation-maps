#!/usr/bin/env python3
"""
Bitcoin Liquidation Map MCP Server

This MCP server provides tools to retrieve cryptocurrency liquidation heatmaps
from Coinglass. It supports multiple cryptocurrencies and timeframes.
"""

import os
import logging
import requests
import time
import base64
import asyncio
from datetime import datetime
from typing import Any, Sequence
from io import BytesIO

from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

import mcp.types as types
from mcp.server import Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize MCP server
server = Server("bitcoin-liquidation-maps")

# Supported cryptocurrencies and timeframes
SUPPORTED_SYMBOLS = ["BTC", "ETH", "BNB", "ADA", "SOL", "XRP", "DOT", "DOGE", "AVAX", "MATIC"]
SUPPORTED_TIMEFRAMES = ["12 hour", "24 hour", "1 month", "3 month"]

def setup_webdriver(max_retries=5, retry_delay=2):
    """Configure and return a Chrome WebDriver instance with retries"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=5400,2950")
    chrome_options.add_argument("--force-device-scale-factor=2")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    
    selenium_host = os.getenv('SELENIUM_HOST', 'localhost')
    selenium_port = os.getenv('SELENIUM_PORT', '4444')
    
    for attempt in range(max_retries):
        try:
            logger.info(f"Connecting to Selenium at http://{selenium_host}:{selenium_port}/wd/hub (attempt {attempt+1}/{max_retries})")
            driver = webdriver.Remote(
                command_executor=f'http://{selenium_host}:{selenium_port}/wd/hub',
                options=chrome_options
            )
            logger.info("Successfully connected to Selenium")
            return driver
        except Exception as e:
            logger.warning(f"Failed to connect to Selenium: {e}")
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                # Fallback to local Chrome if remote fails
                try:
                    logger.info("Attempting to use local Chrome driver")
                    service = Service(ChromeDriverManager().install())
                    driver = webdriver.Chrome(service=service, options=chrome_options)
                    logger.info("Successfully connected to local Chrome")
                    return driver
                except Exception as local_e:
                    logger.error(f"Failed to connect to local Chrome: {local_e}")
                    raise Exception("Could not connect to either remote or local Chrome driver")

def get_crypto_price(symbol):
    """Fetch the current crypto price from CoinGecko API"""
    try:
        # Map common symbols to CoinGecko IDs
        symbol_map = {
            'BTC': 'bitcoin',
            'ETH': 'ethereum',
            'BNB': 'binancecoin',
            'ADA': 'cardano',
            'SOL': 'solana',
            'XRP': 'ripple',
            'DOT': 'polkadot',
            'DOGE': 'dogecoin',
            'AVAX': 'avalanche-2',
            'MATIC': 'matic-network'
        }
        
        coin_id = symbol_map.get(symbol, symbol.lower())
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            price = data.get(coin_id, {}).get('usd')
            if price:
                return f"${price:,.2f}"
        
        return None
    except Exception as e:
        logger.error(f"Error fetching {symbol} price: {e}")
        return None

def capture_coinglass_heatmap(symbol="BTC", time_period="24 hour"):
    """
    Capture the Coinglass liquidation heatmap
    
    Args:
        symbol (str): Cryptocurrency symbol (e.g., "BTC", "ETH")
        time_period (str): Time period to select (e.g., "24 hour", "1 month", "3 month")
    
    Returns:
        tuple: (image_path, success_message) or (None, error_message)
    """
    driver = None
    try:
        logger.info(f"Starting capture of Coinglass {symbol} heatmap with {time_period} timeframe")
        driver = setup_webdriver()
        
        # Navigate to Coinglass liquidation page
        driver.get("https://www.coinglass.com/pro/futures/LiquidationHeatMap")
        wait = WebDriverWait(driver, 20)
        
        # Optimize page for screenshot
        driver.execute_script("""
            var style = document.createElement('style');
            style.innerHTML = `
                * {
                    transition: none !important;
                    animation: none !important;
                }
                .echarts-for-react {
                    width: 100% !important;
                    height: 100% !important;
                }
                canvas {
                    image-rendering: -webkit-optimize-contrast !important;
                    image-rendering: crisp-edges !important;
                }
            `;
            document.head.appendChild(style);
            window.devicePixelRatio = 2;
        """)
        
        # Wait for page to load
        time.sleep(5)
        
        # Use JavaScript to force symbol change
        if symbol != "BTC":
            try:
                # Click Symbol tab first
                symbol_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@role='tab' and contains(text(), 'Symbol')]")))
                symbol_tab.click()
                time.sleep(2)
                logger.info("Clicked Symbol tab")
                
                # Find the input element
                input_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.MuiAutocomplete-input")))
                
                # Clear the input by selecting all and typing
                actions = ActionChains(driver)
                actions.click(input_element)
                actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL)
                actions.send_keys(symbol)
                actions.perform()
                
                time.sleep(2)
                logger.info(f"Typed {symbol} into input field")
                
                # Try to click on dropdown option or press Enter
                try:
                    # Wait for dropdown to appear and click option
                    option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//li[@role='option' and text()='{symbol}']")))
                    option.click()
                    logger.info(f"Clicked {symbol} option from dropdown")
                except:
                    # Fallback: press Enter
                    actions = ActionChains(driver)
                    actions.send_keys(Keys.ENTER)
                    actions.perform()
                    logger.info(f"Pressed Enter to select {symbol}")
                
                # Wait for chart to update
                time.sleep(15)
                logger.info(f"Waited for chart to update with {symbol} data")
                
            except Exception as symbol_e:
                logger.warning(f"Could not select symbol {symbol}: {symbol_e}")
        else:
            logger.info("Using default BTC symbol")
        
        # Find and click the time period dropdown button
        time_dropdown = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, "div.MuiSelect-root button.MuiSelect-button"
        )))
        
        if time_dropdown.text.strip() != time_period:
            time_dropdown.click()
            time.sleep(2)
            
            driver.execute_script(f"""
                var options = document.querySelectorAll('li[role="option"]');
                for(var i = 0; i < options.length; i++) {{
                    if(options[i].textContent.includes('{time_period}')) {{
                        options[i].click();
                        break;
                    }}
                }}
            """)
            time.sleep(3)
        
        # Find and capture the chart
        try:
            heatmap_container = wait.until(EC.presence_of_element_located((
                By.CSS_SELECTOR, "div.echarts-for-react"
            )))
        except Exception:
            heatmap_container = wait.until(EC.presence_of_element_located((
                By.XPATH, "//div[contains(@class, 'echarts-for-react')]"
            )))
        
        time.sleep(3)
        
        rect = driver.execute_script("""
            var rect = arguments[0].getBoundingClientRect();
            return {
                x: rect.left,
                y: rect.top,
                width: rect.width,
                height: rect.height
            };
        """, heatmap_container)
        
        # Capture screenshot with CDP
        result = driver.execute_cdp_cmd('Page.captureScreenshot', {
            'clip': {
                'x': rect['x'],
                'y': rect['y'],
                'width': rect['width'],
                'height': rect['height'],
                'scale': 2
            },
            'captureBeyondViewport': True,
            'fromSurface': True
        })
        
        png_data = base64.b64decode(result['data'])
        image = Image.open(BytesIO(png_data))
        
        # Create output directory if it doesn't exist
        os.makedirs("output", exist_ok=True)
        
        temp_file = f"output/{symbol.lower()}_liquidation_heatmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{time_period.replace(' ', '_')}.png"
        image.save(temp_file, format='PNG', optimize=True, quality=100)
        
        logger.info(f"Heatmap captured and saved as {temp_file}")
        
        # Get price information
        price = get_crypto_price(symbol)
        price_info = f" Current {symbol} price: {price}" if price else ""
        
        success_message = f"Successfully captured {symbol} liquidation heatmap for {time_period} timeframe.{price_info}"
        return temp_file, success_message
        
    except Exception as e:
        error_message = f"Error capturing heatmap: {str(e)}"
        logger.error(error_message)
        return None, error_message
    finally:
        if driver:
            driver.quit()

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools"""
    return [
        types.Tool(
            name="get_liquidation_map",
            description="Retrieve a cryptocurrency liquidation heatmap from Coinglass",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": f"Cryptocurrency symbol. Supported: {', '.join(SUPPORTED_SYMBOLS)}",
                        "enum": SUPPORTED_SYMBOLS,
                        "default": "BTC"
                    },
                    "timeframe": {
                        "type": "string", 
                        "description": f"Time period for the heatmap. Supported: {', '.join(SUPPORTED_TIMEFRAMES)}",
                        "enum": SUPPORTED_TIMEFRAMES,
                        "default": "24 hour"
                    }
                },
                "required": []
            }
        ),
        types.Tool(
            name="get_crypto_price",
            description="Get the current price of a cryptocurrency",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": f"Cryptocurrency symbol. Supported: {', '.join(SUPPORTED_SYMBOLS)}",
                        "enum": SUPPORTED_SYMBOLS
                    }
                },
                "required": ["symbol"]
            }
        ),
        types.Tool(
            name="list_supported_assets",
            description="List all supported cryptocurrency symbols and timeframes",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any] | None) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool calls"""
    if arguments is None:
        arguments = {}
    
    if name == "get_liquidation_map":
        symbol = arguments.get("symbol", "BTC").upper()
        timeframe = arguments.get("timeframe", "24 hour")
        
        # Validate inputs
        if symbol not in SUPPORTED_SYMBOLS:
            return [types.TextContent(
                type="text",
                text=f"Error: Unsupported symbol '{symbol}'. Supported symbols: {', '.join(SUPPORTED_SYMBOLS)}"
            )]
        
        if timeframe not in SUPPORTED_TIMEFRAMES:
            return [types.TextContent(
                type="text", 
                text=f"Error: Unsupported timeframe '{timeframe}'. Supported timeframes: {', '.join(SUPPORTED_TIMEFRAMES)}"
            )]
        
        # Capture the heatmap
        image_path, message = capture_coinglass_heatmap(symbol, timeframe)
        
        if image_path and os.path.exists(image_path):
            # Read the image file and encode it
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            # Convert to base64 for embedding
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            # Clean up the temporary file
            os.remove(image_path)
            
            return [
                types.TextContent(
                    type="text",
                    text=message
                ),
                types.ImageContent(
                    type="image",
                    data=image_base64,
                    mimeType="image/png"
                )
            ]
        else:
            return [types.TextContent(
                type="text",
                text=message
            )]
    
    elif name == "get_crypto_price":
        symbol = arguments.get("symbol", "").upper()
        
        if not symbol:
            return [types.TextContent(
                type="text",
                text="Error: Symbol is required"
            )]
        
        if symbol not in SUPPORTED_SYMBOLS:
            return [types.TextContent(
                type="text",
                text=f"Error: Unsupported symbol '{symbol}'. Supported symbols: {', '.join(SUPPORTED_SYMBOLS)}"
            )]
        
        price = get_crypto_price(symbol)
        if price:
            return [types.TextContent(
                type="text",
                text=f"Current {symbol} price: {price}"
            )]
        else:
            return [types.TextContent(
                type="text",
                text=f"Failed to fetch price for {symbol}"
            )]
    
    elif name == "list_supported_assets":
        return [types.TextContent(
            type="text",
            text=f"""Supported Cryptocurrency Symbols:
{', '.join(SUPPORTED_SYMBOLS)}

Supported Timeframes:
{', '.join(SUPPORTED_TIMEFRAMES)}

Usage Examples:
- get_liquidation_map(symbol="BTC", timeframe="24 hour")
- get_liquidation_map(symbol="ETH", timeframe="1 month")
- get_crypto_price(symbol="BTC")"""
        )]
    
    else:
        return [types.TextContent(
            type="text",
            text=f"Error: Unknown tool '{name}'"
        )]

async def main():
    """Main entry point for the MCP server"""
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="bitcoin-liquidation-maps",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None,
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())