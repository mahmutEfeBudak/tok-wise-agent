# TokWise Agent

A custom **Byte Pair Encoding (BPE)** tokenizer built from scratch in Python. It processes UTF-8 text and creates token vocabularies, demonstrating how tokenization works in Large Language Models (LLMs).

## 📁 Project Structure

- `tools.py`: Core BPE algorithm functions (encoding, decoding, frequency counting, and merging).
- `train.py`: The main script to train the tokenizer and build the vocabulary.
- `app.py`: Streamlit web application for interactive tokenization.
- `corpus.txt`: The text data used to train the BPE model.

## 🚀 How to Use

**1. Train the Tokenizer**
Run the training script to read `corpus.txt` and generate the BPE rules:

``` python train.py ```

**2. Launch the Web Interface**
Run the Streamlit app to interactively test tokenization:

``` streamlit run app.py ```

**3. Use in Python**
You can import `tools.py` directly in your Python code:

```import tools

# Text to Token IDs
text = "Hello world"
tokens = tools.encode(text)

# Token IDs to Text
decoded_text = tools.decode(tokens)
```