# codex-test

This repository contains a small example of an email assistant inspired by Pete Koomen's essay on AI-native software. The assistant processes a list of dummy emails and applies simple rules to label messages, draft short replies and optionally archive spam.

## Command line usage

Run the assistant with Python:

```bash
python3 email_assistant.py
```

The output shows the actions the agent would take for each email.

## Web UI

A minimal Flask app provides a simple interface with a "Go" button on the left and the processed emails on the right. Draft replies are generated for each email and you can edit them before hitting **Send**. Install Flask and run:

```bash
pip install Flask
python3 web_app.py
```

Then open [http://localhost:5000](http://localhost:5000) in your browser.

## PredictIt Trading Agent

`predictit_agent.py` fetches price data from the official PredictIt API and
simulates buying a random contract. Subsequent price updates are logged to a
CSV file called `trading_log.csv`.

Run it with:

```bash
pip install requests
python3 predictit_agent.py --iterations 5 --delay 2 --log mylog.csv
```

If market data can't be fetched due to network restrictions, the log will be
empty and a warning message will be printed.
