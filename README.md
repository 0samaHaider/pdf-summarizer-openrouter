# 📄 PDF Summarizer (LLM)

Upload a PDF and get a **bullet-point summary** using an LLM via **OpenRouter**.

## ✨ Features

* Upload any PDF
* Bullet-point summaries
* Uses OpenRouter LLM (e.g. `gpt-4o-mini`)
* Handles large PDFs with chunking

## 🛠 Setup

### 1. Clone the repo

```bash
git clone <repo-url>
cd pdf-summarizer
```

### 2. Create & activate virtual environment

```bash
python -m venv .venv
.\.venv\Scripts\activate   # Windows
```

### 3. Install dependencies

```bash
pip install streamlit pypdf requests
```

### 4. Set OpenRouter API key

```bash
setx OPENROUTER_API_KEY "your_key_here"
```

## ▶ Run the app

```bash
streamlit run src/app.py
```

Upload a PDF → get a bullet-point summary 
* Add a **project structure section**
* Write a **GitHub-friendly version with badges**
