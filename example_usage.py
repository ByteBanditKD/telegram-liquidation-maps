#!/usr/bin/env python3
"""
Example usage of the Bitcoin Liquidation Maps MCP Server

This script demonstrates how to interact with the MCP server programmatically.
In practice, you would use this server with an MCP-compatible LLM client.
"""

import asyncio
import os
from liquidation_map_server import handle_call_tool

async def example_get_bitcoin_map():
    """Example: Get Bitcoin liquidation map for 24 hours"""
    print("🔥 Getting Bitcoin liquidation map for 24 hours...")
    print("-" * 50)
    
    try:
        result = await handle_call_tool("get_liquidation_map", {
            "symbol": "BTC",
            "timeframe": "24 hour"
        })
        
        # Print the text response
        for item in result:
            if hasattr(item, 'text'):
                print(item.text)
            elif hasattr(item, 'data'):
                print(f"📊 Image captured! Size: {len(item.data)} bytes")
                print("💾 Image saved as base64 data (would be displayed in MCP client)")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()

async def example_get_ethereum_map():
    """Example: Get Ethereum liquidation map for 1 month"""
    print("🔥 Getting Ethereum liquidation map for 1 month...")
    print("-" * 50)
    
    try:
        result = await handle_call_tool("get_liquidation_map", {
            "symbol": "ETH", 
            "timeframe": "1 month"
        })
        
        # Print the text response
        for item in result:
            if hasattr(item, 'text'):
                print(item.text)
            elif hasattr(item, 'data'):
                print(f"📊 Image captured! Size: {len(item.data)} bytes")
                print("💾 Image saved as base64 data (would be displayed in MCP client)")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()

async def example_get_prices():
    """Example: Get current prices for multiple cryptocurrencies"""
    print("💰 Getting current cryptocurrency prices...")
    print("-" * 50)
    
    symbols = ["BTC", "ETH", "SOL", "ADA"]
    
    for symbol in symbols:
        try:
            result = await handle_call_tool("get_crypto_price", {"symbol": symbol})
            print(result[0].text)
        except Exception as e:
            print(f"❌ Error getting {symbol} price: {e}")
    
    print()

async def example_list_assets():
    """Example: List all supported assets"""
    print("📋 Listing supported assets...")
    print("-" * 50)
    
    try:
        result = await handle_call_tool("list_supported_assets", {})
        print(result[0].text)
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()

async def main():
    """Run all examples"""
    print("Bitcoin Liquidation Maps MCP Server - Usage Examples")
    print("=" * 60)
    print()
    
    # List supported assets first
    await example_list_assets()
    
    # Get current prices
    await example_get_prices()
    
    # Note about map examples
    print("🚨 Map Examples (Requires Internet & May Take Time)")
    print("=" * 60)
    print("The following examples will attempt to scrape liquidation maps.")
    print("This requires a stable internet connection and may take 30-60 seconds per request.")
    print("Press Ctrl+C to skip if you don't want to wait.")
    print()
    
    try:
        # Get Bitcoin map (this will take time)
        await example_get_bitcoin_map()
        
        # Get Ethereum map (this will also take time)
        await example_get_ethereum_map()
        
    except KeyboardInterrupt:
        print("\n⏭️  Map examples skipped by user.")
    
    print("✅ Examples completed!")
    print()
    print("🔗 Integration with LLM Clients:")
    print("To use this server with an LLM client, configure it to use:")
    print(f"Command: python {os.path.abspath('liquidation_map_server.py')}")
    print()
    print("Then you can make natural language requests like:")
    print("- 'Retrieve a Bitcoin map on the 24 hour timeframe'")
    print("- 'Get me an Ethereum liquidation heatmap for 1 month'")
    print("- 'Show me the current BTC price'")
    print("- 'What cryptocurrencies are supported?'")

if __name__ == "__main__":
    asyncio.run(main())