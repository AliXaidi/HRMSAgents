from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.memory import ConversationBufferMemory
from langchain_openai import AzureChatOpenAI, AzureOpenAI
from core.db import execute_query
from core.config import AZURE_OPENAI_API_KEY,AZURE_OPENAI_API_VERSION,AZURE_OPENAI_DEPLOYMENT,AZURE_OPENAI_ENDPOINT
import datetime

EMPLOYEE_ID = 1001  # Replace with dynamic ID from login/session

def mark_attendance(employee_id, action):
    now = datetime.datetime.now()
    if action == "check-in":
        execute_query(
            "INSERT INTO EmployeeAttendance (EmployeeId, CheckInTime) VALUES (?, ?)",
            [employee_id, now]
        )
        return f"✅ Checked in at {now}"
    if action == "check-out":
        execute_query(
            "UPDATE EmployeeAttendance SET CheckOutTime=? WHERE EmployeeId=? AND CheckOutTime IS NULL",
            [now, employee_id]
        )
        return f"✅ Checked out at {now}"

def get_attendance(employee_id):
    rows = execute_query(
        "SELECT CheckInTime, CheckOutTime FROM EmployeeAttendance WHERE EmployeeId=? ORDER BY CheckInTime DESC",
        [employee_id],
        fetch=True
    )
    return "\n".join([f"Check-in: {r[0]} | Check-out: {r[1] or 'Not checked out'}" for r in rows[:10]]) or "No records"

tools = [
    Tool(name="Clock In", func=lambda _: mark_attendance(EMPLOYEE_ID, "check-in"), description="Mark check-in."),
    Tool(name="Clock Out", func=lambda _: mark_attendance(EMPLOYEE_ID, "check-out"), description="Mark check-out."),
    Tool(name="View Attendance", func=lambda _: get_attendance(EMPLOYEE_ID), description="View attendance logs.")
]

# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm = AzureChatOpenAI(
    openai_api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    deployment_name=AZURE_OPENAI_DEPLOYMENT,   
    openai_api_version=AZURE_OPENAI_API_VERSION,
    temperature=1.0
)
# llm = AzureOpenAI(
#     api_version=AZURE_OPENAI_API_VERSION,
#     azure_endpoint=AZURE_OPENAI_ENDPOINT,
#     api_key=AZURE_OPENAI_API_KEY,
#     temperature=1.0
# )
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
attendance_agent = initialize_agent(tools, llm, agent="chat-conversational-react-description", memory=memory, verbose=True)
