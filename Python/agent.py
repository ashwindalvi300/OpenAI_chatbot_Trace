# agent.py
from logger import logger
import re
from memory import get_session, store_session
from tools.sub_trace_tool import fetch_traceability_data
from openai_client import ask_llm

SALUTATION_PATTERNS = [
    r"\bhi\b", r"\bhello\b", r"\bhey\b", r"\bhiya\b", r"\bhey there\b", r"\bhow are you\b",
    r"\bhowdy\b", r"\bgreetings\b", r"\bgood to see you\b",
    r"\bgood morning\b", r"\bgood afternoon\b", r"\bgood evening\b",
    r"\bgood day\b", r"\bgood night\b", r"\bmorning\b", r"\bafternoon\b", r"\bevening\b",
    r"\bnight\b",
    r"\bwhat's up\b", r"\bwhats up\b", r"\bsup\b", r"\byo\b",
    r"\bhowdy\b", r"\bhey ya\b", r"\bhey you\b", r"\bhiya\b",
    r"\bgreetings\b", r"\bpleased to meet you\b",
    r"\bnice to meet you\b", r"\bgood to see you\b", r"\bhow do you do\b", r"\bit's a pleasure\b",
    r"\bthanks\b", r"\bthank you\b", r"\bthanks a lot\b",
    r"\bthank you very much\b", r"\bmuch appreciated\b",
    r"\bappreciate it\b", r"\bappreciated\b", r"\bcheers\b", r"\bthx\b", r"\bty\b",
    r"\bok\b", r"\bokay\b", r"\bokay then\b",
    r"\ball right\b", r"\balright\b",
    r"\bgreat\b", r"\bsure\b", r"\byep\b", r"\byeah\b", r"\bbye\b", r"\bgoodbye\b",
    r"\bsee you\b", r"\bsee ya\b", r"\blater\b", r"\bgood bye\b", r"\bfarewell\b",
    r"\byes\b", r"\bgot it\b", r"\bunderstood\b", r"\broger that\b", r"\bcopy that\b",
    r"\bexcuse me\b", r"\bpardon\b", r"\bpardon me\b",
    r"\bif you don't mind\b", r"\bif you dont mind\b"
]


def is_salutation_only(text: str) -> bool:
    text = text.lower().strip()
    return any(re.fullmatch(p, text) for p in SALUTATION_PATTERNS)


def remove_salutations(text: str) -> str:
    cleaned = text
    for p in SALUTATION_PATTERNS:
        cleaned = re.sub(p, "", cleaned, flags=re.IGNORECASE)
    return cleaned.strip()


def run_agent(userId, stationId, imei, query):
    session_id = f"{userId}_{imei}"

    logger.info(f"\n📩 Incoming Query: '{query}'")
    logger.info(f"🆔 Session ID: {session_id}")

    # Only greeting → NO TOOL, NO MEMORY, NO DATA
    if is_salutation_only(query):
        logger.info("👋 Detected SALUTATION ONLY → Tool NOT called, Session NOT used")
        return "<p>Hello! I am a traceability assistant. How can I help you?</p>"

    cleaned_query = remove_salutations(query)
    logger.info(f"🧹 Cleaned Query: '{cleaned_query}'")

    session, is_expired = get_session(session_id)

    # Fetch tool ONLY when required
    if not session:
        logger.info("🆕 No session found → CALLING TOOL")
        activity_data = fetch_traceability_data(userId, stationId, imei)
        store_session(session_id, activity_data)

    elif is_expired:
        logger.info("⏰ Session expired → CALLING TOOL again")
        activity_data = fetch_traceability_data(userId, stationId, imei)
        store_session(session_id, activity_data)

    else:
        logger.info("✅ Session found & valid → Tool NOT called (using memory)")
        activity_data = session["activity_data"]

    # Decide if activity data should go to LLM
    if len(cleaned_query.split()) <= 3:
        logger.info("💬 Short / small-talk query → Activity data NOT sent to LLM")
        prompt = f"""
        Respond politely to the user message and also ask the user that what you want to know regarding traceability data.
Respond to the user in pure HTML format only.

STRICT RULES:
- Give answers in bullet points or tables where applicable
- Do NOT use \\n or \n
- Do NOT use Markdown
- Do NOT add headings, or lists unless necessary
- Use only <p>, <b>, <br>, <span>
- For table data you can use the <table> tag : <tr>, <td>, <th>
- Output must be a single-line HTML string

User Message:
{query}
"""
    else:
        logger.info("📦 Real query → Activity data SENT to LLM")
        prompt = f"""
        Using the available activity data for this session, answer the question below.
Answer the user's question using the activity data in pure HTML format only.

STRICT RULES:
- Give answers in bullet points or tables where applicable
- Do NOT use \\n or \n
- Do NOT use line breaks
- Do NOT use Markdown
- Do NOT add headings, or decorative elements
- Use only <p>, <b>, <br>, <span>
- For table data you can use the <table> tag : <tr>, <td>, <th>
- Keep it minimal and UI-friendly
- Output must be a single-line HTML string

Question:
{cleaned_query}

Activity Data:
{activity_data}
"""

    llm_response = ask_llm(prompt)

    logger.info("🤖 LLM Response:")
    logger.info(llm_response)

    return llm_response
