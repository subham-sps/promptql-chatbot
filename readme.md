
# 🚀 PromptQL Chatbot Builder  

This project allows you to build a chatbot with any **PromptQL** project in minutes! It provides a **Streamlit-based frontend** that interacts with users and an **LLM using the PromptQL API**.  

## ✨ Features  
- Quickly set up a chatbot with **any PromptQL project**.  
- **Streamlit UI** for an intuitive and interactive user experience.  
- **PromptQL API integration** for seamless communication with LLMs.  
- Requires just **three environment variables** for setup.  

## 🛠️ Setup Instructions  

### 1️⃣ **Clone the Repository**  
```sh
git clone <repo-url>
cd <project-folder>
```

### 2️⃣ **Set Up Environment Variables**  
Before running the chatbot, create a `.env` file in the project root and add the following:  

#### **📄 `.env` file sample:**  
```ini
PROMPTQL_API_KEY=your-api-key
PROMPTQL_PROJECT_URL=your-project-url
PROMPTQL_API_URL=your-api-url
```

Alternatively, you can set them manually in your terminal:  

```sh
export PROMPTQL_API_KEY="your-api-key"
export PROMPTQL_PROJECT_URL="your-project-url"
export PROMPTQL_API_URL="your-api-url"
```
*(For Windows, use `set` instead of `export` in cmd.)*  

### 3️⃣ **Install Dependencies**  
```sh
pip install -r requirements.txt
```

### 4️⃣ **Run the Chatbot**  
```sh
streamlit run app.py
```

## 🎯 Usage  
- Open the **Streamlit UI** in your browser.  
- Enter your queries, and the chatbot will **respond using the configured PromptQL project**.  
- Modify the **PromptQL project URL** to switch between different chatbot implementations.  

## 🔧 Customization  
- Modify `app.py` to customize chatbot behavior.  
- Update **Streamlit UI elements** to match your use case.  

## 📌 Contributing  
Feel free to submit issues or contribute via PRs to improve the project!  
