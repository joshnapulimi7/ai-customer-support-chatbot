import os
from dotenv import load_dotenv

load_dotenv()

def classify_query(message: str) -> str:
    msg = message.lower()
    if any(word in msg for word in ["refund", "bill", "payment", "invoice", "charge", "subscription", "price"]):
        return "Billing & Payments"
    elif any(word in msg for word in ["error", "bug", "crash", "login", "password", "not working", "issue", "slow"]):
        return "Technical Support"
    elif any(word in msg for word in ["account", "profile", "delete", "email", "update", "username"]):
        return "Account Management"
    elif any(word in msg for word in ["human", "agent", "manager", "escalate", "complaint", "urgent"]):
        return "Escalation Request"
    return "General Inquiry"

def generate_ai_response(message: str, category: str) -> tuple[str, bool]:
    if category == "Escalation Request":
        return (
            "I understand this requires specialized attention. I have escalated your request to a Tier-2 human support specialist and generated a priority support ticket. Our team will reach out shortly.",
            True
        )

    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            prompt = (
                f"You are a helpful Tier-1 Customer Support AI Agent. "
                f"The user's query is classified under '{category}'. "
                f"Provide a clear, polite, and concise resolution (under 3 sentences). "
                f"User Query: {message}"
            )
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text.strip(), False
        except Exception:
            pass

    fallback_responses = {
        "Billing & Payments": "For billing or refund queries, you can view and download your invoices under Account > Billing. Refunds typically reflect within 3–5 business days. Would you like me to raise a billing ticket for you?",
        "Technical Support": "Let's troubleshoot this! Please try clearing your browser cache, verifying your internet connection, and logging back in. If the error persists, share the error code or type 'escalate' to connect with an engineer.",
        "Account Management": "You can update your profile details, registered email, or password anytime from Settings > Security. Let me know if you're locked out of your account!",
        "General Inquiry": "Thank you for reaching out! I can help you with Billing, Technical Support, and Account Management queries. Could you share a bit more detail about what you need assistance with?"
    }
    return fallback_responses.get(category, fallback_responses["General Inquiry"]), False
