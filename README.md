# AI-Agent-workshop-demo

## Setup Guide
0. Git clone and navigate to the directory where you have placed the code.
1. Create a virtual environment using the following commands:

```bash
python3 -m venv venv 
source venv/bin/activate
```

2. Install the libraries
```bash 
pip install -r requirements.txt
```

3. Change directory to src and run the application
```bash
cd src
streamlit run streamlit_app.py
```


If for some reason the above snippets don't work, use the following:
```bash 
pip install python-dotenv langchain langchain-huggingface huggingface_hub transformers pandas openpyxl
```

### Tokens
- Create a .env file in the src folder
```
HF_API_TOKEN=<Your token here>
HF_ENDPOINT_URL=<Your endpoint url here>
```
