import time
import threading
from app.helpers.get_functions import *
from app.services.database import save_to_database
from app.core.config import AGENT_ID


def process_conversations_post():
    try: 
        conversation_id = get_latest_conversation(AGENT_ID)                      
        transcript = get_transcript(conversation_id)
        time.sleep(8) 
        audio_file = download_conversation_audio(conversation_id)
        details = extract_appointment_details(transcript) if transcript else {}
        
        appointment_data = {
            "conversation_id": conversation_id,
            "transcript": transcript,
            "audio_file": audio_file,
            "name": details.get("name", "N/A"),
            "phone": validate_phone(details.get("phone", "N/A")),
            "email": validate_email(details.get("mail", "N/A")),
            "reason": details.get("reason", "Checkup"),
            "gender": details.get("gender", "Male"),
            "age": details.get("age", "30"),
            "city": details.get("city", "Unknown"),
            "zip": details.get("zip", "N/A"),
            "history": details.get("history", "New"),
            "date": details.get("date", "15/06"),
            "time": details.get("time", "14:00"),
            "referral": details.get("referral", "NO"),
            "appointment_status": details.get("appointment_status", "Pending"),
            "summary": details.get("summary", "N/A")
        }
        
        saved_data = save_to_database([appointment_data])
        return {
            "success": True,
            "data": saved_data[0] if saved_data else None  
        }
                
    except Exception as e:
        print(f"Error in processing loop: {e}")
    finally:
        time.sleep(5)

def process_conversations():
    while True:
        try:
            conversation_id = get_latest_conversation(AGENT_ID)
            if conversation_id:  
                transcript = get_transcript(conversation_id)
                time.sleep(8) 
                audio_file = download_conversation_audio(conversation_id)
                details = extract_appointment_details(transcript) if transcript else {}
                
                appointment_data = {
                        "conversation_id": conversation_id,
                        "transcript": transcript or "N/A",
                        "audio_file": audio_file or "N/A",                       
                        "name": details.get("name", "N/A").strip(),
                        "phone": validate_phone(details.get("phone", "N/A")),  
                        "email": validate_email(details.get("mail", details.get("email", "N/A"))),                        
                        "reason": details.get("reason", "N/A"),
                        "gender": details.get("gender", "N/A"),
                        "age": details.get("age", "N/A"),                        
                        "city": details.get("city", "N/A"),
                        "zip": details.get("zip", "N/A"),                        
                        "history": details.get("history", "N/A"),                        
                        "date": details.get("date", "N/A"),
                        "time": details.get("time", "N/A"),
                        "referral": details.get("referral", "NO"),                        
                        "appointment_status": details.get("appointment_status", "Pending"),
                        "summary": details.get("summary", "N/A")
                    }
             
                save_to_database([appointment_data])
                
        except Exception as e:
            print(f"Error in processing loop: {e}")
        finally:
            time.sleep(5)


#thread = threading.Thread(target=process_conversations, daemon=True)
#thread.start()