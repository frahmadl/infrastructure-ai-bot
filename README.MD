# 🤖 Infrastructure AI Query Bot

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-412991.svg)](https://openai.com/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458.svg)](https://pandas.pydata.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An intelligent backend service built with **FastAPI**, **Pandas**, and **OpenAI GPT-4** that ingests infrastructure dataset (Excel) and enables natural language querying, automated intent extraction, and real-time infrastructure analytics.

---

## 🎯 Project Overview

This project serves as an AI-driven Assistant for Infrastructure and System Operations teams. Instead of manually filtering server inventories, operators can query server attributes, network configurations, ports, and environments using natural language or direct REST APIs.

### Key Highlights
- **Automated Data Ingestion:** Loads and normalizes server configuration datasets (`.xlsx`) on application startup.
- **Natural Language Understanding (NLU):** Extracts operational intent and filtering parameters from natural queries via OpenAI API.
- **RESTful Search & Filter Endpoints:** Granular search capabilities across `Server Name`, `Hostname`, `Source IP`, `NAT IP`, `Port`, `Environment`, and `Destination`.
- **Infrastructure Analytics:** Aggregates real-time metrics and environmental distribution stats.
- **Conversational Context Window (Bonus):** Supports multi-turn contextual chat powered by live server data (`/api/chat`).
- **Interactive Documentation:** Out-of-the-box OpenAPI (Swagger UI) documentation.

---

## 🏗 System Architecture

```text
┌────────────────┐          HTTP Request          ┌──────────────────────┐
│  Client / App  │ ─────────────────────────────► │   FastAPI Engine     │
└────────────────┘                                └──────────┬───────────┘
                                                             │
                         ┌───────────────────────────────────┼───────────────────────────────────┐
                         ▼                                   ▼                                   ▼
              ┌─────────────────────┐             ┌─────────────────────┐             ┌─────────────────────┐
              │ Pandas Data Engine  │             │ Intent Extractor    │             │ Contextual Chat Bot │
              │ (Server Inventory)  │             │ (OpenAI GPT-4)      │             │ (OpenAI GPT-4)      │
              └─────────────────────┘             └─────────────────────┘             └─────────────────────┘