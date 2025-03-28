import requests
import os


def summarize_note(text: str):
    url = "https://api.google.com/aistudio/summarize"  # Replace with the actual Gemini API endpoint
    headers = {
        "Authorization": f"Bearer {os.getenv('GOOGLE_API')}",  # Replace with your API key
        "Content-Type": "application/json"
    }
    data = {
        "text": text  # Note content to be summarized
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["summary"]  # Assuming the response contains a "summary" field
    else:
        return f"Error: {response.status_code}, {response.text}"

# Example usage
note_text = "Your long note text here."
summary = summarize_note(note_text)
print("Summary:", summary)
