# AI-Powered Price Tracker & BrowserUse Integration

🚀 **A New AI Agent Every Day! Series - Day 14/21 - BrowserUse-Powered Price Tracker Agent**

## Overview

**BrowserUse-Price-Tracker-Agent** is a powerful AI-powered price tracker that scrapes multiple e-commerce websites for product prices using **BrowserUse**. This agent displays the best deals in a user-friendly UI and can be easily extended using the Upsonic Framework.

## Installation

### Install dependencies

Ensure you have Python 3.9+ installed. Then, install the required dependencies:

```bash
pip install -r requirements.txt
```

### Install `browser-use` and `playwright`

BrowserUse requires Playwright for web scraping capabilities. Run the following commands:

```bash
pip install browser-use
playwright install
```

## Running the Application

### Start the FastAPI Server

```bash
upsonicai:app --reload
```

### Open the UI

Go to **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** in your browser.

## API Endpoints

| Method | Endpoint                              | Description                       |
| ------ | ------------------------------------- | --------------------------------- |
| `GET`  | `http://127.0.0.1:8000/`                  | Loads the web interface           |
| `GET`  | `http://127.0.0.1:8000/track_price?product=product_name`   | Tracks prices for a given product |

## Example Usage

1. Enter a product name (e.g., "The Art of War") in the UI.
2. Click **Track Price** to search Amazon, eBay, and AliExpress.
3. View the product prices in a detailed and clean format.

## Who Can Use This?

- Shoppers looking for the **best deals**.
- Developers testing **BrowserUse** and web scraping capabilities.
- Businesses monitoring **competitor pricing**.

## Requirements

All necessary dependencies are listed in the `requirements.txt` file. Make sure to install them before running the application.

## Future Improvements

- Add historical price tracking & trend analysis.
- Multi-platform notifications (e.g., Telegram, Discord).
- Broader e-commerce site support.

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss the changes.

## License

This project is licensed under the MIT License.

