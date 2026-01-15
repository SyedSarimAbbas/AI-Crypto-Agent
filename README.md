# 🪙 AI Crypto Agent: The Knowledge-First Cryptocurrency Assistant

## 📖 Project Overview

The **AI Crypto Agent** is a specialized, high-integrity conversational assistant designed to provide accurate, factual information about cryptocurrencies. In an era where Generative AI can often hallucinate or confidently state incorrect facts, this project serves as a crucial experiment in **Retrieval-Augmented Generation (RAG)** principles, specifically tailored for the high-stakes domain of finance.

Unlike generic Large Language Models (LLMs) that may offer unsolicited financial advice or speculative predictions, the AI Crypto Agent is built upon a strict **"Knowledge-First" architecture**. It is engineered to prioritize verified local data and real-time market metrics over generative speculation. The core philosophy of this project is **Safety and Accuracy**. In the volatile world of cryptocurrency, misinformation can be costly. This agent acts as a guardrail, answering questions about coin origins, mechanics, and current prices while explicitly rejecting requests for price predictions, investment strategies, or "hot tips."

## 🏗️ System Architecture

The application is built as a hybrid system that intelligently sources data from two distinct layers, ensuring robustness and reliability:

1.  **Local Knowledge Base (The Source of Truth):**
    The agent first consults a curated JSON-based Knowledge Base (`crypto_kb.json`). This ensures that static metadata—such as a coin's founder, launch year, consensus mechanism, and utility—is always consistent and factually correct. This layer protects against the "hallucinations" common in pure AI models, ensuring that Bitcoin is always identified as created by Satoshi Nakamoto and not by a random entity.

2.  **Live API Integration (The Real-Time Layer):**
    For dynamic data like current price (`USD`), the agent bridges the gap between static knowledge and the live market. It utilizes the **CoinGecko API** to fetch real-time market data. The system includes a smart fallback mechanism: if the API is unreachable or rate-limited, it gracefully degrades to simulated mock data or cached values, ensuring the application never crashes during a demo or outage.

## ✨ Key Features

### 🛡️ Strict Hallucination Guards
The agent is programmed with a rigid policy layer using intent detection algorithms. If a user asks speculative questions like *"Will Solana go up next week?"* or *"Should I buy Bitcoin?"*, the agent detects the **"Speculative"** or **"Financial Advice"** intent. It then firmly refuses to answer, reminding the user of its factual, non-advisory mandate. This feature is critical for compliance and user safety.

### ⚡ Real-Time Market Data
Users can ask for the price of major assets (BTC, ETH, SOL, ADA, XRP, etc.), and the agent will retrieve the latest live price via the CoinGecko `simple/price` endpoint. This data is timestamped to the second, ensuring users know exactly how fresh the information is.

### 🎨 Premium User Experience
The frontend is built with **Streamlit**, but it is heavily customized to break away from the standard "data science script" look.
- **Dynamic Background:** A subtle, high-quality video background sets a futuristic, tech-forward tone.
- **Glassmorphism UI:** Chat bubbles and sidebars feature a translucent, frosted-glass effect using `backdrop-filter: blur`, creating a sense of depth and modernity.
- **Smooth Animations:** CSS transitions and hover effects make the interface feel alive and responsive.
- **Responsive Design:** The layout automatically adjusts for different screen sizes, ensuring a seamless experience on both desktop and mobile.

## 🛠️ Technical Stack & Dependencies

This project leverages a robust and modern technology stack:

- **Language:** Python 3.8+
- **Frontend Framework:** Streamlit (v1.30+)
- **API Client:** `requests` library interacting with CoinGecko V3 API
- **Data Storage:** Local JSON (lightweight, fast, no SQL database required)
- **Styling:** Custom CSS injection for advanced UI customisation
- **Concurrency:** Basic session state management for chat history persistence

**Key Dependencies:**
- `streamlit`: The core framework for the web interface.
- `requests`: Handling HTTP requests to external APIs.

## 🚀 Installation & Usage Guide

Follow these simple steps to set up the project locally on your machine.

### 1. Clone the Repository
Bring the code to your local machine using git:
```bash
git clone https://github.com/SyedSarimAbbas/AI-Crypto-Agent.git
cd AI-Crypto-Agent
```

### 2. Set Up the Environment
It is recommended to use a virtual environment to keep your system clean. Install the necessary dependencies:
```bash
pip install streamlit requests
```

### 3. Run the Application
You can verify the installation by running the agent. We have provided a convenience script for Windows users:

**Option A: Using the Batch Script (Windows)**
Simply double-click `run.bat` or execute it in the terminal:
```bash
.\run.bat
```

**Option B: Using the Command Line**
```bash
streamlit run app.py
```

Once running, the application will open in your default web browser at `http://localhost:8501`.

## 📄 License

This project is licensed under the **MIT License**.

Current Year: 2026
Copyright (c) Syed Sarim Abbas

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files, to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
