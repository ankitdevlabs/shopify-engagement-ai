# Shopify Engagement AI 🚀

## Overview

Shopify Engagement AI is a lightweight AI-powered engagement system for Shopify stores.

It tracks user behavior (like page views, clicks, and time spent) and uses a language model (LLM) to decide:

* **When** to show a message
* **What** message to show

The goal is simple: engage users at the right moment and boost conversions.

---

## Features ⚙️

* Track user activity:

  * Page views
  * Clicks (Add to Cart, etc.)
  * Time on site
* Send session data to backend
* AI decides if engagement is needed
* Generates short, personalized messages
* Displays popup on the frontend

---

## Tech Stack 🛠

* **Backend:** FastAPI (Python)
* **LLM:** HuggingFace
* **Frontend:** JavaScript snippet
* **HTTP Client:** httpx

---

## How It Works 🧪

1. JavaScript snippet tracks user actions on the Shopify store
2. Sends data to the backend API
3. Backend builds a prompt and sends it to the LLM
4. LLM returns:

   * Whether to show a message
   * Message content
5. Frontend displays a popup if needed

---

## Setup 🔧

### 1. Install Dependencies

```bash
poetry install
```

### 2. Configure Settings
Add production.yaml file inside src/shopify_backend

Update `production.yaml`:

```yaml
hf_api_key: "your_key"
hf_base_uri: "https://api-inference.huggingface.co"
hf_model: "your_model"
```

### 3. Run Server

```bash
poetry run cli serve --host 0.0.0.0 --port 9000
```

---

## API Endpoint 📡

### POST `/api/engagement/analyze`

#### Request

```json
{
  "current_page": "Product",
  "cart_items": 1,
  "time_on_site": 150,
  "event_type": "click",
  "element": "add_to_cart"
}
```

#### Response

```json
{
  "show_message": true,
  "message": "Complete your purchase now!",
  "priority": "high",
  "reason": "User active and has items in cart"
}
```

---

## Shopify Integration 🛍

* Add your JS snippet to `theme.liquid`
* Or use Shopify ScriptTag
* Ensure your backend API is publicly accessible

---

## Environment Variables 🔑

* `hf_api_key`
* `hf_base_uri`
* `hf_model`

---

## Notes 💡

* Keep responses from the LLM short for better UX
* Avoid showing too many popups (rate limit on frontend recommended)
* Optimize backend latency for real-time engagement

---

## License

MIT License
