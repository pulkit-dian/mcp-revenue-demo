# Demo MCP Server

## 🚀 Running the Server

### Standard Mode
```bash
poetry run uvicorn app.main:app --reload
```

### Production Mode
```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The server will start on http://localhost:8000

## 🔧 Configuration for Claude Desktop / MCP Clients

### Using mcp-remote (Recommended)

First, start the server:
```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Then configure your MCP client:

**For macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
**For Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "payment-revenue-server": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "http://localhost:8000/mcp"
      ]
    }
  }
}
```

**Important:** Make sure the server is running before starting Claude Desktop!

## 💡 Usage Examples with Claude

Once configured, you can ask Claude natural language questions:

### Example 1: Current Month Revenue
**You:** "What's the total revenue this month?"

**Claude will use:** `get_revenue_this_month()`

### Example 2: Year-to-Date Analysis
**You:** "Show me the year-to-date revenue"

**Claude will use:** `get_revenue_year_to_date()`

### Example 3: Specific Time Window
**You:** "What was the revenue last Monday between 10 AM and 12 PM?"

**Claude will use:** `get_revenue_custom_range(start_date="2024-10-07T10:00:00", end_date="2024-10-07T12:00:00")`

### Example 4: Category Breakdown
**You:** "Break down revenue by product category for this month"

**Claude will use:** `get_revenue_by_category(start_date="2024-10-01", end_date="2024-10-31")`

### Example 5: Last 30 Days
**You:** "How much revenue did we generate in the last 30 days?"

**Claude will use:** `get_revenue_last_n_days(days=30)`

### Example 6: Monthly Comparison
**You:** "Show me monthly revenue for 2024"

**Claude will use:** `get_revenue_by_month(year=2024)`

## 🧪 Testing the Server

Visit http://localhost:8000/docs to test all endpoints interactively.
