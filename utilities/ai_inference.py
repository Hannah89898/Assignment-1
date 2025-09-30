"""
ai_inference.py - GPT inference functions that accept user's API key
"""
from openai import OpenAI

def gpt5_mini_inference(system_prompt, instruction_prompt, api_key):
    """
    Generate inference using user-provided API key
    
    Args:
        system_prompt: System message for the AI
        instruction_prompt: User prompt/question
        api_key: OpenAI API key from user
    
    Returns:
        String response from GPT
    """
    client = OpenAI(api_key=api_key)
    
    completion = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": instruction_prompt}
        ]
    )
    
    inference = completion.choices[0].message.content
    return inference

def gpt5_mini_inference_yes_no(system_prompt, instruction_prompt, api_key):
    """
    Generate yes/no inference using user-provided API key
    
    Args:
        system_prompt: System message for the AI
        instruction_prompt: User prompt/question
        api_key: OpenAI API key from user
    
    Returns:
        String response ("Yes" or "No")
    """
    client = OpenAI(api_key=api_key)
    
    yes_token = 6763
    no_token = 1750
    
    completion = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": instruction_prompt}
        ],
        logit_bias={
            yes_token: 100,
            no_token: 100
        },
        max_tokens=1
    )
    
    inference = completion.choices[0].message.content
    return inference