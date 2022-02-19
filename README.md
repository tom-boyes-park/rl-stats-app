# 🚀 Rocket League Gameplay Stats

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/tom-boyes-park/rl-stats-app/main/app.py)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

Web app to allow users to retrieve their recent Rocket League game statistics and view radar charts comparing statistics
between game wins and losses.

Relies on users having their game replays uploaded to [ballchasing.com](https://ballchasing.com/)

![app-screenshot](./images/app-screenshot.png)

## Running Locally

Install requirements:
```commandline
pip install -r requirements.txt
```

Set environment variable for ballchasing API token:
```commandline
export BC_API_TOKEN=<your-token>
```

Run the app:
```commandline
streamlit run app.py
```
