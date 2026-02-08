#!/usr/bin/env python3
"""
MCP Browser Server for CarConnectivity WebUI Testing
Provides browser automation tools for visual testing and UI verification
"""

import asyncio
import base64
import json
from typing import Optional, Dict, Any
from playwright.async_api import async_playwright, Browser, Page
import mcp.server.stdio
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions

# Global browser instance
_browser: Optional[Browser] = None
_page: Optional[Page] = None

server = Server("carconnectivity-browser")


async def get_browser() -> Browser:
    """Get or create browser instance"""
    global _browser
    if _browser is None:
        playwright = await async_playwright().start()
        _browser = await playwright.chromium.launch(headless=True)
    return _browser


async def get_page() -> Page:
    """Get or create page instance"""
    global _page
    if _page is None:
        browser = await get_browser()
        _page = await browser.new_page(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        )
    return _page


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available browser automation tools"""
    return [
        types.Tool(
            name="navigate",
            description="Navigate to a URL and capture screenshot",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL to navigate to (e.g., http://localhost:8080/)"
                    },
                    "wait_for": {
                        "type": "string",
                        "description": "CSS selector to wait for before screenshot (optional)",
                        "default": "body"
                    },
                    "full_page": {
                        "type": "boolean",
                        "description": "Capture full page screenshot",
                        "default": True
                    }
                },
                "required": ["url"]
            }
        ),
        types.Tool(
            name="click",
            description="Click an element and capture result",
            inputSchema={
                "type": "object",
                "properties": {
                    "selector": {
                        "type": "string",
                        "description": "CSS selector of element to click"
                    },
                    "wait_after": {
                        "type": "number",
                        "description": "Milliseconds to wait after click",
                        "default": 1000
                    }
                },
                "required": ["selector"]
            }
        ),
        types.Tool(
            name="type_text",
            description="Type text into an input field",
            inputSchema={
                "type": "object",
                "properties": {
                    "selector": {
                        "type": "string",
                        "description": "CSS selector of input field"
                    },
                    "text": {
                        "type": "string",
                        "description": "Text to type"
                    }
                },
                "required": ["selector", "text"]
            }
        ),
        types.Tool(
            name="get_console_logs",
            description="Get browser console logs (errors, warnings, info)",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        types.Tool(
            name="get_network_errors",
            description="Get failed network requests (404, 500, etc)",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        types.Tool(
            name="check_accessibility",
            description="Run accessibility checks using axe-core",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL to check (optional, uses current page if not provided)"
                    }
                }
            }
        ),
        types.Tool(
            name="get_element_info",
            description="Get detailed information about an element",
            inputSchema={
                "type": "object",
                "properties": {
                    "selector": {
                        "type": "string",
                        "description": "CSS selector of element"
                    }
                },
                "required": ["selector"]
            }
        ),
        types.Tool(
            name="screenshot_element",
            description="Take screenshot of specific element",
            inputSchema={
                "type": "object",
                "properties": {
                    "selector": {
                        "type": "string",
                        "description": "CSS selector of element"
                    }
                },
                "required": ["selector"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool execution"""
    
    if name == "navigate":
        url = arguments.get("url")
        wait_for = arguments.get("wait_for", "body")
        full_page = arguments.get("full_page", True)
        
        page = await get_page()
        
        # Capture console logs
        console_logs = []
        page.on("console", lambda msg: console_logs.append({
            "type": msg.type,
            "text": msg.text
        }))
        
        # Capture network errors
        network_errors = []
        page.on("response", lambda response: (
            network_errors.append({
                "url": response.url,
                "status": response.status,
                "statusText": response.status_text
            }) if response.status >= 400 else None
        ))
        
        # Navigate
        await page.goto(url, wait_until="networkidle")
        await page.wait_for_selector(wait_for, timeout=10000)
        
        # Take screenshot
        screenshot = await page.screenshot(full_page=full_page)
        screenshot_b64 = base64.b64encode(screenshot).decode()
        
        # Get page title
        title = await page.title()
        
        return [
            types.TextContent(
                type="text",
                text=f"Navigated to: {url}\nTitle: {title}\n\nConsole Logs: {len(console_logs)}\nNetwork Errors: {len(network_errors)}"
            ),
            types.ImageContent(
                type="image",
                data=screenshot_b64,
                mimeType="image/png"
            )
        ]
    
    elif name == "click":
        selector = arguments.get("selector")
        wait_after = arguments.get("wait_after", 1000)
        
        page = await get_page()
        await page.click(selector)
        await page.wait_for_timeout(wait_after)
        
        screenshot = await page.screenshot(full_page=True)
        screenshot_b64 = base64.b64encode(screenshot).decode()
        
        return [
            types.TextContent(
                type="text",
                text=f"Clicked: {selector}"
            ),
            types.ImageContent(
                type="image",
                data=screenshot_b64,
                mimeType="image/png"
            )
        ]
    
    elif name == "type_text":
        selector = arguments.get("selector")
        text = arguments.get("text")
        
        page = await get_page()
        await page.fill(selector, text)
        
        return [
            types.TextContent(
                type="text",
                text=f"Typed '{text}' into {selector}"
            )
        ]
    
    elif name == "get_console_logs":
        page = await get_page()
        
        # Collect console logs
        logs = []
        async def log_handler(msg):
            logs.append({
                "type": msg.type,
                "text": msg.text,
                "location": msg.location
            })
        
        page.on("console", log_handler)
        await page.wait_for_timeout(1000)  # Wait a bit to collect logs
        
        return [
            types.TextContent(
                type="text",
                text=json.dumps(logs, indent=2)
            )
        ]
    
    elif name == "get_network_errors":
        page = await get_page()
        
        errors = []
        async def response_handler(response):
            if response.status >= 400:
                errors.append({
                    "url": response.url,
                    "status": response.status,
                    "statusText": response.status_text,
                    "method": response.request.method
                })
        
        page.on("response", response_handler)
        await page.wait_for_timeout(2000)
        
        return [
            types.TextContent(
                type="text",
                text=json.dumps(errors, indent=2)
            )
        ]
    
    elif name == "check_accessibility":
        url = arguments.get("url")
        page = await get_page()
        
        if url:
            await page.goto(url, wait_until="networkidle")
        
        # Inject axe-core
        await page.add_script_tag(url="https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.7.2/axe.min.js")
        
        # Run axe
        results = await page.evaluate("""
            async () => {
                const results = await axe.run();
                return {
                    violations: results.violations.map(v => ({
                        id: v.id,
                        impact: v.impact,
                        description: v.description,
                        nodes: v.nodes.length,
                        help: v.help,
                        helpUrl: v.helpUrl
                    }))
                };
            }
        """)
        
        return [
            types.TextContent(
                type="text",
                text=f"Accessibility Issues Found: {len(results['violations'])}\n\n" + 
                     json.dumps(results, indent=2)
            )
        ]
    
    elif name == "get_element_info":
        selector = arguments.get("selector")
        page = await get_page()
        
        info = await page.evaluate(f"""
            () => {{
                const el = document.querySelector('{selector}');
                if (!el) return null;
                const rect = el.getBoundingClientRect();
                const styles = window.getComputedStyle(el);
                return {{
                    tagName: el.tagName,
                    className: el.className,
                    id: el.id,
                    text: el.textContent?.substring(0, 100),
                    visible: rect.width > 0 && rect.height > 0,
                    position: {{
                        top: rect.top,
                        left: rect.left,
                        width: rect.width,
                        height: rect.height
                    }},
                    styles: {{
                        display: styles.display,
                        position: styles.position,
                        color: styles.color,
                        backgroundColor: styles.backgroundColor,
                        fontSize: styles.fontSize
                    }}
                }};
            }}
        """)
        
        return [
            types.TextContent(
                type="text",
                text=json.dumps(info, indent=2)
            )
        ]
    
    elif name == "screenshot_element":
        selector = arguments.get("selector")
        page = await get_page()
        
        element = await page.query_selector(selector)
        if not element:
            return [types.TextContent(type="text", text=f"Element not found: {selector}")]
        
        screenshot = await element.screenshot()
        screenshot_b64 = base64.b64encode(screenshot).decode()
        
        return [
            types.ImageContent(
                type="image",
                data=screenshot_b64,
                mimeType="image/png"
            )
        ]
    
    else:
        raise ValueError(f"Unknown tool: {name}")


async def main():
    """Run the MCP server"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="carconnectivity-browser",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
