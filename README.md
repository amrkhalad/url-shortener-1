# URL Shortener

A simple and efficient URL shortener service that generates shortened URLs ending with "zag eng".

## Features

- Shorten long URLs with a custom ending "zag eng"
- Option to use custom short codes
- Copy shortened URL to clipboard
- Track number of visits for each shortened URL
- API endpoint for programmatic URL shortening
- Clean and responsive UI

## Requirements

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd url-shortener
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Enter a URL in the input field and click "Shorten URL"

## API Usage

### Shorten URL
```bash
curl -X POST http://localhost:5000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

### Get URL Statistics
```bash
curl http://localhost:5000/api/stats/<short_code>
```

## Example

Input URL:
```
https://example.com/very-long-url-that-needs-to-be-shortened
```

Output URL:
```
http://localhost:5000/abc123zageng
```

## License

MIT License 