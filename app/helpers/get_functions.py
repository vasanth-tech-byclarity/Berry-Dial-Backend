import os
import re
import requests
import openai
from app.core.config import ELEVENLABS_API_KEY, BASE_URL, HEADERS, OPENAI_API_KEY

def get_latest_conversation(agent_id: str) -> str | None:
    url = f"{BASE_URL}/conversations"
    response = requests.get(url, headers=HEADERS)
    print("response from latest convo :",response)
    if response.status_code == 200:
        conversations = response.json().get("conversations", [])
        filtered = [conv for conv in conversations if conv.get("agent_id") == agent_id]
        return filtered[0].get("conversation_id") if filtered else None
    return None

def get_transcript(conversation_id: str) -> str | None:
    url = f"{BASE_URL}/conversations/{conversation_id}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        transcript_data = response.json().get("transcript", [])
        return "\n".join([f"{msg['role'].capitalize()}: {msg['message']}" 
                         for msg in transcript_data if msg.get("role") in ["agent", "user"]])
    return None

def download_conversation_audio(conversation_id: str) -> str | None:
    url = f"{BASE_URL}/conversations/{conversation_id}/audio"
    response = requests.get(url, headers={"xi-api-key": ELEVENLABS_API_KEY})
    if response.status_code == 200 and "audio" in response.headers.get("Content-Type", ""):
        os.makedirs("app/static/audio", exist_ok=True)
        audio_file = f"app/static/audio/audio_{conversation_id}.mp3"
        with open(audio_file, "wb") as file:
            file.write(response.content)
        return audio_file
    return None

def extract_appointment_details(transcript):
    openai.api_key = OPENAI_API_KEY
    prompt = (f"Go through the content properly and extract only the patient details formatted as follows:\n"
              f"Name: [name]\nPhone: [phone]\nMail: [mail]\n"
              f"Reason: [reason]\nGender: [gender]\nAge: [age]\n"
              f"City: [city]\nZip: [zip]\nHistory: [history]\n\n"
              f"Date: [date]\nTime: [time]\nReferral: [referral]\n\n"
              f"Appointment Status: [status]\n\n"
              f"Summary: [summary]\n\n"
              f"Transcript:\n{transcript}.\n"
              f"Note: The Date should be in DD/MM format, Time should be in hours, Referral should contain a name if referred or 'NO' otherwise. "
              f"For History, use 'New' or 'Existing'. For Appointment Status, check whether the appointment is confirmed with date and time, "
              f"then mark the status as 'Booked'. If there is no date and time, mark it as 'Pending'.For Summary give a short summary within 60 to 100 words.")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0 
        )
        extracted_text = response["choices"][0]["message"]["content"]

        def extract(pattern):
            match = re.search(pattern, extracted_text, re.IGNORECASE)
            return match.group(1).strip() if match else "N/A"

        return {
            "name": extract(r"Name:\s*(.+)"),
            "phone": extract(r"Phone:\s*(.+)"),
            "mail": extract(r"Mail:\s*(.+)"),
            "reason": extract(r"Reason:\s*(.+)"),
            "gender": extract(r"Gender:\s*(.+)"),
            "age": extract(r"Age:\s*(.+)"),
            "city": extract(r"City:\s*(.+)"),
            "zip": extract(r"Zip:\s*(.+)"),
            "history": extract(r"History:\s*(.+)"),
            "date": extract(r"Date:\s*(\d{2}/\d{2})"),  
            "time": extract(r"Time:\s*([\d:APM]+)"), 
            "referral": extract(r"Referral:\s*(.+)"),  
            "appointment_status": extract(r"Appointment Status:\s*(.+)"), 
            "summary": extract(r"Summary:\s*(.+)")
        }
    except Exception as e:
        print(f"Error extracting appointment details: {str(e)}")
        return {}



def validate_phone(phone: str) -> str:
    cleaned = re.sub(r"[^\d+]", "", phone)
    return cleaned if len(cleaned) >= 10 else "N/A"

def validate_email(email: str) -> str:
    return email if "@" in email and "." in email.split("@")[-1] else "N/A"