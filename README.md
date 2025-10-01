# test2
# Legal Document Q&A App

## Deployed Application
https://assignment-1-sdqvn69jxbvxrcyfuszdey.streamlit.app/

## Test Case
1. Open the deployed application
2. Enter your OpenAI API key in the sidebar
3. Click "Update API Key"
4. Upload `Simmonds-Thatcher v Kamari.pdf`
5. Wait for processing (shows chunk count)
6. Ask: "What was the main legal issue in this case?"
7. Expected: Answer with source chunks displayed

## Technical Details
- Vector DB: ChromaDB
- Chunking: LlamaIndex SentenceWindowNodeParser (window_size=5)
- LLM: OpenAI GPT-5-mini