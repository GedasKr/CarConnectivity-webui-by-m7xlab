# MCP Browser Server Setup

This MCP server enables Cursor to actually see and interact with your CarConnectivity WebUI!

## Features

- 🖼️ **Visual Testing**: Capture screenshots and analyze UI
- 🖱️ **Browser Automation**: Click, type, navigate
- 🐛 **Debug Tools**: Console logs, network errors
- ♿ **Accessibility**: Run axe-core checks
- 🎯 **Element Inspection**: Get detailed element info

## Installation

### 1. Install Dependencies

```bash
cd "CarConnectivity-plugin-webui"

# Install Python dependencies
pip install -r mcp_requirements.txt

# Install Playwright browsers
playwright install chromium
```

### 2. Configure Cursor

Add to your VsCode settings (`.vscode/settings.json`):

```json
{
  "mcpServers": {
    "carconnectivity-browser": {
      "command": "python3",
      "args": [
        "CarConnectivity-plugin-webui/mcp_browser_server.py"
      ]
    }
  }
}
```

### 3. Restart Cursor

Restart Cursor to load the MCP server.

## Usage Examples

Once configured, I (the AI) can use these tools:

### Navigate and Screenshot
```
navigate to http://localhost:8080/
→ Returns screenshot + page info
```

### Test Login Flow
```
1. navigate to https://cars.m7xlab.top/login
2. type_text in 'input[name="username"]' with 'admin'
3. type_text in 'input[name="password"]' with 'admin'
4. click 'button[type="submit"]'
→ See the result!
```

### Check for Errors
```
get_console_logs
→ See JavaScript errors

get_network_errors
→ See 404s, 500s, etc.
```

### Accessibility Check
```
check_accessibility at http://localhost:8080/
→ Get WCAG violations
```

### Inspect Elements
```
get_element_info for '.vehicle-card'
→ See size, position, styles

screenshot_element for '.vehicle-card'
→ Get just that element's screenshot
```

## Benefits

### Before (Current Workflow)
1. You deploy
2. You test manually
3. You screenshot issues
4. You paste to me
5. I fix blindly
6. Repeat

### After (With MCP)
1. You deploy
2. I navigate and see it myself
3. I identify issues visually
4. I fix with full context
5. I verify the fix
6. Done!

## Available Tools

| Tool | Description |
|------|-------------|
| `navigate` | Go to URL, wait for load, capture screenshot |
| `click` | Click element by CSS selector |
| `type_text` | Type into input fields |
| `get_console_logs` | Get browser console output |
| `get_network_errors` | Get failed HTTP requests |
| `check_accessibility` | Run axe-core WCAG checks |
| `get_element_info` | Get element properties, position, styles |
| `screenshot_element` | Screenshot specific element |

## Workflow Example

### Testing the Vehicle Detail Page

```
Me: "Let me check the vehicle detail page"

1. navigate to http://localhost:8080/garage/
   → I see the garage page, vehicle card looks good
   
2. click '.vehicle-card'
   → I see it navigated to detail page
   → Screenshot shows the layout
   
3. get_console_logs
   → Check for any JavaScript errors
   
4. check_accessibility
   → Verify WCAG compliance
   
5. screenshot_element '.vehicle-card-image'
   → See just the car image
   → "The image looks too small, let me fix the CSS..."
```
