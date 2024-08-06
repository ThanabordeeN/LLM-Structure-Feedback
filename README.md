
# LLM Feedback Loop for Enhanced Chatbot

This project demonstrates the implementation of a feedback loop mechanism to improve the stability and accuracy of a Large Language Model (LLM) in a football-focused chatbot application.

## Key Concept: Feedback Loop

The core of this project is the feedback loop mechanism, which significantly enhances the LLM's output quality and reliability. Here's how it works:

1. **Initial Response Generation:** The LLM generates a response based on the user's input and conversation history.

2. **Validation:** The system attempts to parse the LLM's response as JSON, ensuring it meets the required structure.

3. **Error Handling:** If parsing fails, the system captures the error.

4. **Feedback:** The error is sent back to the LLM as additional context, instructing it to correct its output format.

5. **Iteration:** Steps 1-4 repeat until a valid JSON response is produced.

This process ensures that the final output adheres to the specified format, improving consistency and reducing hallucinations.

## Benefits of the Feedback Loop

- **Increased Stability:** Reduces unexpected or malformed responses.
- **Improved Accuracy:** Guides the LLM to provide more precise and relevant information.
- **Enhanced Structure:** Ensures responses consistently follow the required JSON format.
- **Reduced Hallucinations:** Minimizes instances of the LLM generating false or irrelevant information.

## Implementation

```python
def get_response(user_input):
    import json
    global chat_session

    chat_session.append({"role": "user", "content": user_input})
    while True:
        try:
            response = completion(
                model="claude-3-haiku-20240307",
                messages=chat_session,
                api_key=os.getenv("MODEL_API_KEY")
            )
            chat_session.append({"role": "assistant", "content": response.choices[0].message.content})
            data = json.loads(response.choices[0].message.content)
            # Execute functions here 
            break
        except Exception as e:
            print(f"System Error: {e}")
            chat_session.append({"role": "user", "content": f"{e} \n\n Must Answer Following System Instruct format"})
            continue
    
    return response.choices[0].message.content
```

## Usage

1. Install dependencies:
   ```bash
   pip install litellm python-dotenv
   ```

2. Set up your `.env` file with your API key:
   ```
   MODEL_API_KEY=your_api_key_here
   ```

3. Run the script:
   ```bash
   python feedback.py
   ```

## Example Interaction

```
You: What is the offside rule?
System Error: Expecting value: line 1 column 1 (char 0)
System Error: Expecting value: line 1 column 1 (char 0)
Chatbot: 
{
  "method": "direct",
  "response_msg": "The offside rule in football occurs when an attacking player is nearer to the opponent's goal line than both the ball and the second-last opponent when the ball is played to them by a teammate. This rule is designed to prevent players from simply waiting near the opponent's goal for easy scoring opportunities."
}
```

In this example, you can see the feedback loop in action. The system encountered errors twice but continued to prompt the LLM until it received a correctly formatted response.

## Customization

- Modify the `system` variable to adjust the chatbot's expertise and response format.
- Implement additional validation checks in the feedback loop for more specific requirements.

## Notes

- This implementation uses the "claude-3-haiku-20240307" model, but the feedback loop concept can be applied to other LLMs.
- The Knowledge Base (RAG) functionality is referenced but not fully implemented in this version.

## Contributing

Contributions to improve the feedback loop mechanism or extend the chatbot's capabilities are welcome. Please submit a Pull Request with your proposed changes.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
