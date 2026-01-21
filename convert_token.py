import pickle
import json
import os
from google.oauth2.credentials import Credentials

def convert():
    token_path = 'token.json'
    
    if not os.path.exists(token_path):
        print(f"Error: {token_path} not found.")
        return

    try:
        # Try reading as Pickle (Legacy)
        with open(token_path, 'rb') as f:
            creds = pickle.load(f)
        
        print("\n✅ Successfully loaded binary token.")
        json_content = creds.to_json()
        print("\n👇 COPY THIS JSON CONTENT BELOW 👇\n")
        print(json_content)
        print("\n👆 COPY THIS JSON ABOVE 👆\n")
        
        # Save it back as JSON for future use
        with open(token_path, 'w') as f:
            f.write(json_content)
        print(f"ℹ️ Converted {token_path} to JSON format locally as well.")

    except Exception:
        # Maybe it's already JSON?
        try:
            with open(token_path, 'r') as f:
                content = f.read()
                # Validate JSON
                json.loads(content)
                print("\n✅ Your token.json is ALREADY in valid JSON format.")
                print("\n👇 CONTENT 👇\n")
                print(content)
        except Exception as e:
            print(f"❌ Failed to parse token: {e}")

if __name__ == "__main__":
    convert()
