# 🚀 ProScanner: OSINT Username Reconnaissance Tool

[![GitHub license](https://img.shields.io/github/license/FJ-cyberzilla/pro_scanner?style=flat-square)](https://github.com/FJ-cyberzilla/pro_scanner/blob/main/LICENSE)
[![PyPI version](https://img.shields.io/pypi/v/pro-scanner?style=flat-square)](https://pypi.org/project/pro-scanner/)
[![GitHub stars](https://img.shields.io/github/stars/FJ-cyberzilla/pro_scanner?style=flat-square)](https://github.com/FJ-cyberzilla/pro_scanner/stargazers)

> Powered by Cyberzilla™ - Osint Reconnaissance - MMXXV - V 5.1.3

ProScanner is a modern, production-ready OSINT (Open-Source Intelligence) tool designed to efficiently scan for a given username across a wide range of social media and online platforms. It's built with a focus on speed, reliability, and ease of use.

## ✨ Key Features

* **⚡ Blazing Fast Asynchronous Scanning:** Utilizes `asyncio` and `httpx` to perform non-blocking, concurrent network requests.
* **🌐 Broad Platform Coverage:** Scans popular platforms including Instagram, Twitter, Bluesky, Reddit, Twitch, and more.
* **🛡️ Stealthy & Robust:** Employs intelligent user-agent rotation and rate limiting to avoid detection and IP bans.
* **💾 Caching & Persistence:** Stores scan results in a local SQLite database, so you don't have to re-scan the same username.
* **🎨 Intuitive CLI:** Features a user-friendly, interactive menu and beautifully formatted, colored output.
* **🔧 Modular & Extensible:** Add new platforms by simply editing the `config/platforms.yaml` file—no code changes required.

---

## 💻 Installation

ProScanner requires **Python 3.10** or higher.

### 1. Clone the repository

```bash
git clone [https://github.com/FJ-cyberzilla/pro_scanner.git](https://github.com/FJ-cyberzilla/pro_scanner.git)
cd pro_scanner


```
### 2. Install despendicies 

```bash
# Create a virtual environment
python3 -m venv .venv
# Activate it
source .venv/bin/activate
# Install the required packages
pip install -r requirements.txt


