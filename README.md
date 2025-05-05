# Watsonx × CrewAI Demo

This project is a live walkthrough of IBM's [official tutorial](https://developer.ibm.com/tutorials/awb-build-ai-agents-integrating-crewai-watsonx) on building intelligent multi-agent systems by integrating [CrewAI](https://github.com/joaomdmoura/crewAI) with IBM's `watsonx.ai` platform.

## 🚀 Project Goal

To create a collaborative AI agent workflow where multiple agents with defined roles (e.g., Researcher, Writer, Reviewer) work together to:

- Generate a detailed response to a user query  
- Incorporate feedback loops for refinement  
- Show the potential of orchestration between watsonx models and CrewAI agent management

## 🔧 Tech Stack

- **Python 3.10+**
- **CrewAI** (Agent orchestration framework)
- **IBM watsonx.ai** (Foundation model inference)
- **LangChain** (optional for prompt structuring)
- **Streamlit** (optional for frontend demo interface)

## 📁 Project Structure

\`\`\`
watsonx-crewai-demo/
├── agents/
│   ├── researcher.py
│   ├── writer.py
│   └── reviewer.py
├── prompts/
│   └── templates.yaml
├── main.py
├── requirements.txt
└── README.md
\`\`\`

## ✅ How to Run

1. **Clone the repository**
   \`\`\`bash
   git clone https://github.com/yourusername/watsonx-crewai-demo.git
   cd watsonx-crewai-demo
   \`\`\`

2. **Install dependencies**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

3. **Set your API keys**  
   (Use a `.env` file or insert directly in the script)
   - IBM watsonx API key  
   - Optional fallback LLM API key

4. **Run the main script**
   \`\`\`bash
   python main.py
   \`\`\`

## 🧠 Use Case

This demo simulates a real-world scenario such as drafting a marketing report or research summary, where multiple AI agents collaborate under defined roles—mirroring how human teams operate in structured organizations.

## 🎯 Key Learnings

- How to assign roles and responsibilities to AI agents  
- How to integrate watsonx foundation models into agent workflows  
- How to manage coordination and feedback among agents  

## 📚 Reference

- [IBM Developer Tutorial](https://developer.ibm.com/tutorials/awb-build-ai-agents-integrating-crewai-watsonx/)  
- [CrewAI GitHub](https://github.com/joaomdmoura/crewAI)
