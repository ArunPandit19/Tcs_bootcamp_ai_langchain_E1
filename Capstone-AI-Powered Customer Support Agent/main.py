from dotenv import load_dotenv
load_dotenv()
from models import EmailInput
from workflow import app

email = EmailInput(
    subject="I was charged twice for my subscription!",
    body="Hi team, I noticed two identical charges on my card.",
    from_email="customer@example.com"
)
print("Starting")
result = app.invoke({"email": email})

print("\n=== FINAL OUTPUT ===")
print(result["workflow_output"].model_dump())