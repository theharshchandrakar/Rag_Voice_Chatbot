# pipeline/llm.py

import ollama

# --- Configuration ---
# The model name must match what you pulled in the terminal (e.g., 'llama3')
LLM_MODEL = "llama3"

def generate_answer(query: str, context_chunks: list) -> str:
    """
    Constructs a prompt with the retrieved context and sends it to the local LLM.
    
    :param query: The user's original question.
    :param context_chunks: A list of text strings (the 'knowledge' found in the DB).
    :return: The LLM's final answer as a string.
    """
    
    # 1. Prepare the Context
    # Join all the messy text chunks into one big block of text
    context_block = "\n\n---\n\n".join(context_chunks)
    
    # 2. Construct the Prompt
    # We tell the AI strictly to use ONLY the provided context.
    prompt = f"""
    You are a helpful AI assistant capable of reading documents.
    Use the following pieces of context to answer the user's question at the end.
    
    If the answer is not in the context, say "I don't know based on the provided documents."
    Do not make up information.
    
    CONTEXT:
    {context_block}
    
    USER QUESTION:
    {query}
    
    ANSWER:
    """
    
    print("\n[LLM] Thinking... (Generating response with Llama 3)\n")
    
    try:
        # 3. Call Ollama
        response = ollama.chat(model=LLM_MODEL, messages=[
            {
                'role': 'user',
                'content': prompt,
            },
        ])
        
        # 4. Extract the actual text answer
        return response['message']['content']
        
    except Exception as e:
        return f"[ERROR] Could not talk to Ollama. Is the app running? Error: {e}"