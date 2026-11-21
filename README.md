# 🎸 Sarang AI

### AI-Powered Guitar Shopping & Recommendation Assistant

Sarang AI is an intelligent guitar shopping assistant that helps users discover, explore, compare, and choose guitars through natural-language conversations.

Instead of manually browsing a catalogue, users can ask questions about guitar models, brands, categories, budgets, specifications, and playing experience.

## ✨ Features

- AI-powered conversational guitar assistant
- Natural-language product search
- Guitar recommendations based on budget and experience
- Guitar model comparison
- Search by brand, category, and price range
- Structured catalogue containing 60 guitar entries
- Conversation context support
- Guitar-related information and guidance
- Responsive web interface

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, FastAPI |
| AI Model | GPT-OSS-20B |
| AI Provider | Groq API |
| Product Catalogue | JSON |
| API Server | Uvicorn |
| Version Control | Git and GitHub |
| Deployment | Vercel (planned/configured deployment) |

## 🧠 How It Works

1. The user enters a question through the web interface.
2. The frontend sends the request to the FastAPI backend.
3. The AI model interprets the user's intent.
4. Function calling allows the AI to request relevant catalogue operations.
5. Python searches the structured guitar catalogue.
6. The AI generates a conversational response using the retrieved information.
7. The frontend displays the response.

## 📂 Project Structure

```text
SarangAI/
│
├── backend/
│   ├── main.py
│   ├── ai.py
│   ├── config.py
│   └── products.py
│
├── data/
│   └── guitars.json
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/SarangAI.git
cd SarangAI
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-20b
```

Never publish your actual API key.

### 6. Start the backend

From the project root:

```bash
python -m uvicorn backend.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### 7. Start the frontend

Open another terminal:

```powershell
cd frontend
python -m http.server 5500
```

Open:

```text
http://127.0.0.1:5500
```

## 🔌 API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Backend welcome message |
| GET | `/health` | Backend health check |
| POST | `/api/chat` | AI chatbot interaction |

## 📦 Guitar Catalogue

The application uses a structured JSON catalogue containing 60 guitar entries:

- 20 Acoustic guitars
- 10 Classical guitars
- 20 Electric guitars
- 10 Bass guitars

Catalogue prices and availability are illustrative demonstration data and do not represent verified live inventory.

## 🔐 Security

- API keys are stored in environment variables.
- `.env` is excluded from Git tracking.
- The Groq API key is used by the backend, not exposed in frontend JavaScript.
- Never commit private credentials to GitHub.

## 🚀 Future Improvements

- Expand the guitar catalogue.
- Add product images and detailed specifications.
- Implement retrieval-augmented generation (RAG) for product documentation.
- Integrate a database for persistent product management.
- Add user preferences and personalized recommendations.
- Improve deployment and production monitoring.

## 👨‍💻 Project

**Sarang AI — Intelligent Guitar Shopping Assistant**

Built as an AI application demonstrating LLM integration, function calling, backend development, and structured product retrieval.