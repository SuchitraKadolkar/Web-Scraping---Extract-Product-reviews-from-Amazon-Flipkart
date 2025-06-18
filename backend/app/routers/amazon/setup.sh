# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers (chromium)
python -m playwright install chromium