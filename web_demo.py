#!/usr/bin/env python3
"""
Simple web demo for the Bitcoin Liquidation Maps MCP Server
"""

import asyncio
import base64
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from liquidation_map_server import handle_call_tool, handle_list_tools

app = FastAPI(title="Bitcoin Liquidation Maps MCP Server Demo")

@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the demo homepage"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Bitcoin Liquidation Maps MCP Server Demo</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; text-align: center; }
            .section { margin: 30px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
            .button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
            .button:hover { background: #0056b3; }
            .result { margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 5px; }
            .error { background: #f8d7da; color: #721c24; }
            .success { background: #d4edda; color: #155724; }
            .loading { color: #856404; background: #fff3cd; }
            select, input { padding: 8px; margin: 5px; border: 1px solid #ddd; border-radius: 3px; }
            img { max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔥 Bitcoin Liquidation Maps MCP Server Demo</h1>
            
            <div class="section">
                <h2>📋 Available Tools</h2>
                <button class="button" onclick="listTools()">List Available Tools</button>
                <div id="tools-result" class="result" style="display:none;"></div>
            </div>
            
            <div class="section">
                <h2>💰 Get Cryptocurrency Price</h2>
                <select id="price-symbol">
                    <option value="BTC">Bitcoin (BTC)</option>
                    <option value="ETH">Ethereum (ETH)</option>
                    <option value="BNB">Binance Coin (BNB)</option>
                    <option value="ADA">Cardano (ADA)</option>
                    <option value="SOL">Solana (SOL)</option>
                    <option value="XRP">Ripple (XRP)</option>
                    <option value="DOT">Polkadot (DOT)</option>
                    <option value="DOGE">Dogecoin (DOGE)</option>
                    <option value="AVAX">Avalanche (AVAX)</option>
                    <option value="MATIC">Polygon (MATIC)</option>
                </select>
                <button class="button" onclick="getPrice()">Get Price</button>
                <div id="price-result" class="result" style="display:none;"></div>
            </div>
            
            <div class="section">
                <h2>📊 Get Liquidation Heatmap</h2>
                <p><strong>⚠️ Warning:</strong> This may take 30-60 seconds and requires a stable internet connection.</p>
                <select id="map-symbol">
                    <option value="BTC">Bitcoin (BTC)</option>
                    <option value="ETH">Ethereum (ETH)</option>
                    <option value="BNB">Binance Coin (BNB)</option>
                    <option value="ADA">Cardano (ADA)</option>
                    <option value="SOL">Solana (SOL)</option>
                    <option value="XRP">Ripple (XRP)</option>
                    <option value="DOT">Polkadot (DOT)</option>
                    <option value="DOGE">Dogecoin (DOGE)</option>
                    <option value="AVAX">Avalanche (AVAX)</option>
                    <option value="MATIC">Polygon (MATIC)</option>
                </select>
                <select id="map-timeframe">
                    <option value="12 hour">12 Hour</option>
                    <option value="24 hour" selected>24 Hour</option>
                    <option value="1 month">1 Month</option>
                    <option value="3 month">3 Month</option>
                </select>
                <button class="button" onclick="getMap()">Get Liquidation Map</button>
                <div id="map-result" class="result" style="display:none;"></div>
            </div>
            
            <div class="section">
                <h2>ℹ️ About This Demo</h2>
                <p>This is a demonstration of the Bitcoin Liquidation Maps MCP Server. The server provides tools for:</p>
                <ul>
                    <li>Retrieving cryptocurrency liquidation heatmaps from Coinglass</li>
                    <li>Getting current cryptocurrency prices from CoinGecko</li>
                    <li>Listing supported assets and timeframes</li>
                </ul>
                <p>In a real MCP setup, you would use this server with an LLM client that supports the Model Context Protocol.</p>
            </div>
        </div>
        
        <script>
            async function listTools() {
                const resultDiv = document.getElementById('tools-result');
                resultDiv.style.display = 'block';
                resultDiv.className = 'result loading';
                resultDiv.innerHTML = 'Loading available tools...';
                
                try {
                    const response = await fetch('/api/tools');
                    const data = await response.json();
                    
                    if (data.success) {
                        resultDiv.className = 'result success';
                        let html = '<h3>Available Tools:</h3><ul>';
                        data.tools.forEach(tool => {
                            html += `<li><strong>${tool.name}</strong>: ${tool.description}</li>`;
                        });
                        html += '</ul>';
                        resultDiv.innerHTML = html;
                    } else {
                        resultDiv.className = 'result error';
                        resultDiv.innerHTML = `Error: ${data.error}`;
                    }
                } catch (error) {
                    resultDiv.className = 'result error';
                    resultDiv.innerHTML = `Error: ${error.message}`;
                }
            }
            
            async function getPrice() {
                const symbol = document.getElementById('price-symbol').value;
                const resultDiv = document.getElementById('price-result');
                resultDiv.style.display = 'block';
                resultDiv.className = 'result loading';
                resultDiv.innerHTML = `Getting ${symbol} price...`;
                
                try {
                    const response = await fetch(`/api/price/${symbol}`);
                    const data = await response.json();
                    
                    if (data.success) {
                        resultDiv.className = 'result success';
                        resultDiv.innerHTML = `<h3>${data.result}</h3>`;
                    } else {
                        resultDiv.className = 'result error';
                        resultDiv.innerHTML = `Error: ${data.error}`;
                    }
                } catch (error) {
                    resultDiv.className = 'result error';
                    resultDiv.innerHTML = `Error: ${error.message}`;
                }
            }
            
            async function getMap() {
                const symbol = document.getElementById('map-symbol').value;
                const timeframe = document.getElementById('map-timeframe').value;
                const resultDiv = document.getElementById('map-result');
                resultDiv.style.display = 'block';
                resultDiv.className = 'result loading';
                resultDiv.innerHTML = `Getting ${symbol} liquidation map for ${timeframe}... This may take 30-60 seconds.`;
                
                try {
                    const response = await fetch(`/api/map/${symbol}/${encodeURIComponent(timeframe)}`);
                    const data = await response.json();
                    
                    if (data.success) {
                        resultDiv.className = 'result success';
                        let html = `<h3>${data.message}</h3>`;
                        if (data.image) {
                            html += `<img src="data:image/png;base64,${data.image}" alt="${symbol} Liquidation Map">`;
                        }
                        resultDiv.innerHTML = html;
                    } else {
                        resultDiv.className = 'result error';
                        resultDiv.innerHTML = `Error: ${data.error}`;
                    }
                } catch (error) {
                    resultDiv.className = 'result error';
                    resultDiv.innerHTML = `Error: ${error.message}`;
                }
            }
        </script>
    </body>
    </html>
    """

@app.get("/api/tools")
async def api_list_tools():
    """API endpoint to list available tools"""
    try:
        tools = await handle_list_tools()
        return {
            "success": True,
            "tools": [{"name": tool.name, "description": tool.description} for tool in tools]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/price/{symbol}")
async def api_get_price(symbol: str):
    """API endpoint to get cryptocurrency price"""
    try:
        result = await handle_call_tool("get_crypto_price", {"symbol": symbol.upper()})
        return {
            "success": True,
            "result": result[0].text
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/map/{symbol}/{timeframe}")
async def api_get_map(symbol: str, timeframe: str):
    """API endpoint to get liquidation map"""
    try:
        result = await handle_call_tool("get_liquidation_map", {
            "symbol": symbol.upper(),
            "timeframe": timeframe
        })
        
        message = ""
        image_data = None
        
        for item in result:
            if hasattr(item, 'text'):
                message = item.text
            elif hasattr(item, 'data'):
                image_data = item.data
        
        return {
            "success": True,
            "message": message,
            "image": image_data
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    print("Starting Bitcoin Liquidation Maps MCP Server Web Demo...")
    print("Demo will be available at: http://localhost:8000")
    print("Press Ctrl+C to stop the server.")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)