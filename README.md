# Resume Screening System

## 🔍 Overview
The **Resume Screening System** is an AI-powered tool that helps recruiters and hiring managers efficiently evaluate resumes against job descriptions. Using NLP and machine learning techniques, this tool provides a **match percentage, missing keywords, and personalized recommendations** to assess a candidate's suitability for a role.

---

## 🚀 Features
- **🔢 Match Percentage**: Calculates how well a resume matches a job description.
- **🔍 Keyword Analysis**: Identifies missing skills or domain-specific terms.
- **💡 AI-Powered Recommendation**: (Optional) Uses OpenAI's GPT to generate insightful feedback.
- **📄 Multiple Input Methods**: Supports both text input and file uploads.
- **📊 Detailed Results**: Provides structured output, including a JSON summary.

---

## 🛠️ Installation
### Prerequisites
- **Python 3.7+** installed on your system.
- Virtual environment (recommended but optional).

### 1️⃣ Clone the Repository
```sh
 git clone https://github.com/your-username/resume-screening-system.git
 cd resume-screening-system
```

### 2️⃣ Install Dependencies
```sh
 pip install -r requirements.txt
```

### 3️⃣ Download NLP Model (One-time setup)
```sh
 python -c "import nltk; nltk.download('punkt')"
 python -c "import spacy; spacy.cli.download('en_core_web_sm')"
```

---

## 🎯 Usage
### Run the Streamlit App
```sh
 streamlit run main.py
```

### Input Options
1. **Paste Resume & Job Description** in the text boxes.
2. **Upload Resume & Job Description** as `.txt` files.
3. (Optional) **Enable AI Recommendation** by providing an OpenAI API key.

### Output
- **Match Percentage** 📊
- **Missing Keywords** ❌
- **Recommendation** ✅
- **Detailed Thoughts** 📄
- **JSON Summary** 📝

---

## 📂 File Structure
```
resume-screening-system/
│── main.py                # Streamlit application
│── matcher.py             # Core NLP and ML processing
│── openai_helper.py       # AI-powered recommendation (OpenAI API)
│── requirements.txt       # Dependencies list
│── README.md              # Documentation
```

---

## 🧩 Dependencies
- `streamlit`
- `nltk`
- `spacy`
- `scikit-learn`
- `openai` (if AI recommendations are enabled)

Install using:
```sh
pip install streamlit nltk spacy scikit-learn openai
```

---

## 💡 Future Improvements
- 📌 Support for PDF and DOCX file formats.
- 🎯 More advanced AI recommendations.
- 📊 Enhanced visualization for match analysis.

---

## 🤝 Contributing
Feel free to fork this repository and contribute! For major changes, please open an issue first.

---

## 📜 License
This project is open-source and available under the **MIT License**.

---

### 🚀 Happy Screening! 🎯

