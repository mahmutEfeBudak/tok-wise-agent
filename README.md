# TokWise Agent
 
A custom **Byte Pair Encoding (BPE)** tokenizer built from scratch in Python. It processes UTF-8 text and builds token vocabularies, demonstrating how tokenization works under the hood in Large Language Models (LLMs).
 
## 📁 Project Structure
 
| File | Description |
|---|---|
| `tools.py` | Core BPE algorithm functions (encoding, decoding, frequency counting, and merging). |
| `train.py` | Main script to train the tokenizer and build the vocabulary. |
| `app.py` | Streamlit web app for interactive tokenization. |
| `corpus.txt` | Text data used to train the BPE model. |
 
## 🚀 Getting Started
 
### 1. Train the Tokenizer
 
Run the training script to read `corpus.txt` and generate the BPE merge rules:
 
```bash
python train.py
```
 
### 2. Launch the Web Interface
 
Run the Streamlit app to interactively test tokenization in your browser:
 
```bash
streamlit run app.py
```
 
### 3. Use in Python
 
Import `tools.py` directly in your own code:
 
```python
import tools
 
# Text to Token IDs
text = "Hello world"
tokens = tools.encode(text)
 
# Token IDs to Text
decoded_text = tools.decode(tokens)
```
 
## 📝 Notes
 
- Make sure `corpus.txt` is populated with representative text before running `train.py`, since the tokenizer's vocabulary quality depends on it.
- Re-run `train.py` any time `corpus.txt` changes, so `app.py` and `tools.py` use an up-to-date vocabulary.