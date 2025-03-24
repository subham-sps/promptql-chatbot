import os
import streamlit as st
import requests
import re
from dotenv import load_dotenv

# Load API key and Project URL from environment variables
# Load environment variables from .env file
load_dotenv()

PROMPTQL_API_KEY = os.getenv("PROMPTQL_API_KEY")
PROMPTQL_PROJECT_URL = os.getenv("PROMPTQL_PROJECT_URL")
PROMPTQL_API_URL = os.getenv("PROMPTQL_API_URL")

st.set_page_config(page_title="💬 PromptQL Chat", layout="wide")

def extract_message(json_data):
    # Get the last message from assistant_actions
    last_message_block = json_data["assistant_actions"][-1]
    last_message = last_message_block.get("message", "")

    # Find all artifact identifiers in the message
    artifact_pattern = r"<artifact identifier='(.*?)'[^>]*>"
    artifact_identifiers = re.findall(artifact_pattern, last_message)

    # Process each artifact identifier
    for artifact_id in artifact_identifiers:
        artifact = next((art for art in json_data["modified_artifacts"] if art["identifier"] == artifact_id), None)

        if artifact:
            # Format the artifact data
            formatted_artifact = f"\n📌 **{artifact['title']}**\n"
            for item in artifact["data"]:
                formatted_artifact += "\n".join([f"🔹 {key}: {value}" for key, value in item.items()])
                formatted_artifact += "\n\n"

            # Replace all occurrences of this artifact in the message
            last_message = re.sub(
                f"<artifact identifier='{artifact_id}'[^>]*>", 
                formatted_artifact.strip(),
                last_message
            )

    return last_message.strip()

# Function to send user input to PromptQL
def query_promptql(user_message):
    payload = {
        "version": "v1",
        "llm": {"provider": "hasura"},
        "ddn": {
            "url": PROMPTQL_PROJECT_URL,
            "headers": {}
        },
        "artifacts": [],
        "timezone": "America/Los_Angeles",
        "interactions": [
            {
                "user_message": {"text": user_message},
                "assistant_actions": []
            }
        ],
        "stream": False
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {PROMPTQL_API_KEY}"
    }

    try:
        response = requests.post(PROMPTQL_API_URL, json=payload, headers=headers, timeout=10000)

        # If the response status code is not 200, log it
        if response.status_code != 200:
            st.error(f"Error {response.status_code}: {response.text}")
            return f"❌ Error {response.status_code}: {response.text}"

        # Try parsing the response
        try:
            response_json = response.json()
        except requests.exceptions.JSONDecodeError:
            st.error("Invalid JSON response from the server.")
            return "❌ Error: Invalid JSON response from the server."

        # Extract response message
        assistant_actions = response_json.get("assistant_actions", [])
        if assistant_actions and isinstance(assistant_actions, list):
            assistant_response = extract_message(response_json)
        else:
            assistant_response = "No valid response received from the assistant."

        return assistant_response

    except requests.exceptions.Timeout:
        st.error("The request timed out. Please try again.")
        return "❌ Error: The request timed out."

    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
        return f"❌ Error: Request failed: {e}"

# Streamlit UI
st.title("💬 PromptQL Chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for chat in st.session_state.messages:
    with st.chat_message(chat["role"]):
        st.text(chat["message"])

# Input field
user_input = st.chat_input("Ask me something...")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "message": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get response from PromptQL
    response = query_promptql(user_input)

    # Add bot response to chat history
    st.session_state.messages.append({"role": "assistant", "message": response})
    with st.chat_message("assistant"):
        st.text(response)
