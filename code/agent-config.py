import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ListSortOrder

# Read config from environment variables
PROJECT_ENDPOINT = os.environ["AZURE_AI_PROJECT_ENDPOINT"]  # e.g. https://<resource>.services.ai.azure.com/api/projects/<project>
AGENT_ID = os.environ["AZURE_AI_AGENT_ID"]                  # e.g. asst_...

project = AIProjectClient(
    credential=DefaultAzureCredential(),
    endpoint=PROJECT_ENDPOINT,
)

agent = project.agents.get_agent(AGENT_ID)

thread = project.agents.threads.create()
print(f"Created thread, ID: {thread.id}")

project.agents.messages.create(
    thread_id=thread.id,
    role="user",
    content="Hi Crystal Hotels Assistant",
)

run = project.agents.runs.create_and_process(
    thread_id=thread.id,
    agent_id=agent.id,
)

if run.status == "failed":
    print(f"Run failed: {run.last_error}")
else:
    messages = project.agents.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
    for msg in messages:
        if msg.text_messages:
            print(f"{msg.role}: {msg.text_messages[-1].text.value}")

