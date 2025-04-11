import json
import traceback
from fastapi import APIRouter,FastAPI, Request, WebSocket
from fastapi.responses import FileResponse,HTMLResponse
import mysql.connector
from mysql.connector import Error
from app.core.config import DB_CONFIG
from app.services.processor import process_conversations_post
import threading
from twilio.twiml.voice_response import VoiceResponse, Connect
from elevenlabs import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from app.services.twilio_audio_interface import TwilioAudioInterface
from starlette.websockets import WebSocketDisconnect
from app.core.config import ELEVENLABS_API_KEY, BASE_URL, HEADERS, OPENAI_API_KEY,AGENT_ID

router = APIRouter()

def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Database connection error: {e}")
        return None

@router.post("/api/twilio/inbound_call")
async def handle_incoming_call(request: Request):
    form_data = await request.form()
    call_sid = form_data.get("CallSid", "Unknown")
    from_number = form_data.get("From", "Unknown")
    print(f"Incoming call: CallSid={call_sid}, From={from_number}")

    response = VoiceResponse()
    connect = Connect()
    connect.stream(url=f"wss://{request.url.hostname}/media-stream")
    response.append(connect)
    return HTMLResponse(content=str(response), media_type="application/xml")


@router.websocket("/media-stream")
async def handle_media_stream(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket connection opened")

    audio_interface = TwilioAudioInterface(websocket)
    eleven_labs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

    try:
        conversation = Conversation(
            client=eleven_labs_client,
            agent_id=AGENT_ID,
            requires_auth=True, # Security > Enable authentication
            audio_interface=audio_interface,
            callback_agent_response=lambda text: print(f"Agent: {text}"),
            callback_user_transcript=lambda text: print(f"User: {text}"),
        )

        conversation.start_session()
        print("Conversation started")

        async for message in websocket.iter_text():
            if not message:
                continue
            await audio_interface.handle_twilio_message(json.loads(message))

    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception:
        print("Error occurred in WebSocket handler:")
        traceback.print_exc()
    finally:
        try:
            conversation.end_session()
            conversation.wait_for_session_end()
            print("Conversation ended")
            user_details = process_conversations_post()
        except Exception:
            print("Error ending conversation session:")
            traceback.print_exc()

@router.get("/api/process_conversation")
async def process_conversation():
    try:
        result = process_conversations_post()
        
        if result["success"]:
            return {
                "status": "completed",
                "data": result["data"]
            }
        else:
            raise HTTPException(
                status_code=400,
                detail=result.get("error", "Processing failed")
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Server error: {str(e)}"
        )


@router.get("/api/conversations")
def get_all_conversations():
    connection = None
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            query = """
            select id, conversation_id, transcript, audio_file, name, phone, email, reason, gender, age, city, zip, history, app_date, app_time,
                referral, appointment_status, summary from appoinments order by id desc
            """
            cursor.execute(query)
            results = cursor.fetchall()
            return {"conversations": results}
        return {"error": "Database connection failed"}
    except Error as e:
        print(f"Database query error: {e}")
        return {"error": str(e)}
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

@router.get("/api/audio/{conversation_id}")
def get_audio(conversation_id: str):
    connection = None
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            query = "select audio_file from appoinments where conversation_id = %s"
            cursor.execute(query, (conversation_id,))
            result = cursor.fetchone()
            if result and result['audio_file']:
                return FileResponse(result['audio_file'], media_type="audio/mpeg")
        return {"message": "No audio available"}
    except Error as e:
        print(f"Database query error: {e}")
        return {"error": str(e)}
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

@router.get("/api/date")
def get_all_dates():
    connection = None
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            query = "select conversation_id, app_date from appoinments order by app_date desc"
            cursor.execute(query)
            results = cursor.fetchall()
            return {"dates": results}
        return {"error": "Database connection failed"}
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

@router.get("/api/time")
def get_all_times():
    connection = None
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            query = "select conversation_id, app_time from appoinments order by app_time desc"
            cursor.execute(query)
            results = cursor.fetchall()
            return {"dates": results}
        return {"error": "Database connection failed"}
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

@router.get("/api/referral")
def get_all_referrals():
    connection = None
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            query = "select conversation_id, referral from appoinments"
            cursor.execute(query)
            results = cursor.fetchall()
            return {"dates": results}
        return {"error": "Database connection failed"}
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


@router.get("/api/appointment")
def get_all_appointments():
    connection = None
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            query = "select conversation_id, appointment_status from appoinments"
            cursor.execute(query)
            results = cursor.fetchall()
            return {"appointments": results}
        return {"error": "Database connection failed"}
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
