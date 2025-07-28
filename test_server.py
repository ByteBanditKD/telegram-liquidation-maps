#!/usr/bin/env python3
"""
Test script for the Bitcoin Liquidation Map MCP Server
"""

import asyncio
import json
import sys
from liquidation_map_server import handle_list_tools, handle_call_tool, get_crypto_price

async def test_list_tools():
    """Test listing available tools"""
    print("Testing list_tools...")
    tools = await handle_list_tools()
    print(f"Available tools: {len(tools)}")
    for tool in tools:
        print(f"  - {tool.name}: {tool.description}")
    print()

async def test_get_crypto_price():
    """Test getting crypto price"""
    print("Testing get_crypto_price...")
    try:
        result = await handle_call_tool("get_crypto_price", {"symbol": "BTC"})
        print(f"BTC Price result: {result[0].text}")
    except Exception as e:
        print(f"Error getting BTC price: {e}")
    print()

async def test_list_supported_assets():
    """Test listing supported assets"""
    print("Testing list_supported_assets...")
    try:
        result = await handle_call_tool("list_supported_assets", {})
        print(f"Supported assets:\n{result[0].text}")
    except Exception as e:
        print(f"Error listing supported assets: {e}")
    print()

async def test_direct_price_fetch():
    """Test direct price fetching function"""
    print("Testing direct price fetch...")
    try:
        price = get_crypto_price("BTC")
        print(f"Direct BTC price: {price}")
    except Exception as e:
        print(f"Error in direct price fetch: {e}")
    print()

async def main():
    """Run all tests"""
    print("Bitcoin Liquidation Map MCP Server Test")
    print("=" * 50)
    
    await test_list_tools()
    await test_get_crypto_price()
    await test_list_supported_assets()
    await test_direct_price_fetch()
    
    print("Note: The get_liquidation_map test is skipped as it requires web scraping")
    print("which may take a long time and requires a stable internet connection.")
    print("\nTo test the full functionality, use an MCP client and request:")
    print("'Retrieve a Bitcoin map on the 24 hour timeframe'")

if __name__ == "__main__":
    asyncio.run(main())