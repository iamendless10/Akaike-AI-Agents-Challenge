import os
import time
import pandas as pd
from dotenv import load_dotenv

import autogen
from autogen import GroupChat, GroupChatManager
from langfuse import Langfuse

## WILL BE USING LANGMEM AND REDIS FOR MEMORY MANAGEMENT AND PAST CONVERSATION REMEBERANCE


load_dotenv()

langfuse = Langfuse(
    secret_key=os.getenv("LANGFUSE_PRIVATE_KEY"),
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    host="https://cloud.langfuse.com"
)

config_list = [{
    "model": "llama3-70b-8192",
    "api_key": os.getenv("GROQ_API_KEY"),
    "base_url": "https://api.groq.com/openai/v1",
    "api_type": "openai",
    "price": [0, 0]
}]

def load_data(csv_file: str):
    df = pd.read_csv(csv_file)
    return df

# USING MICROSOFT AUTOGEN 0.4 FOR AI AGENT CREATION

def setup_agents(df: pd.DataFrame):
    user_proxy = autogen.UserProxyAgent(
        name="User_Proxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=6,
        code_execution_config=False,
    )

    data_query_agent = autogen.AssistantAgent(
        name="Data_Query_Agent",
        system_message=f"""You are a data analyst.
You have access to the following dataset:
{df.head(25).to_string()}

Based on this dataset, you can calculate and return insights. If needed, simulate calculations based on the sample data shown.
""",
        llm_config={"config_list": config_list},
        code_execution_config=False, 
    )

    return [user_proxy, data_query_agent]

## AGENT TRACING USING LANGFUSE FOR PRODUCTION MONITORING AND OBSERVABILITY 
def wrap_agent_with_tracing(agent, trace_id):
    original_generate_reply = agent.generate_reply
    def wrapped_generate_reply(messages=None, sender=None, **kwargs):
        start_time = time.time()
        span = langfuse.span(
            name=f"{agent.name}_Execution",
            trace_id=trace_id,
            metadata={"input_messages": str(messages[-1]["content"])[:200] if messages else None}
        )
        try:
            response = original_generate_reply(messages=messages, sender=sender, **kwargs)
            span.end(metadata={"duration_ms": (time.time() - start_time) * 1000, "output": str(response)[:200]})
            return response
        except Exception as e:
            span.end(status_message="Failed", level="ERROR", metadata={"error": str(e)})
            raise
    agent.generate_reply = wrapped_generate_reply
    return agent

def main_logic():
    df = load_data('D:/Extensa_Files/Akaike_Project/Dataset/myntra.csv') 

    agents = setup_agents(df)

    groupchat = GroupChat(
        agents=agents,
        messages=[],
        max_round=20,
        speaker_selection_method="round_robin"
    )

    manager = GroupChatManager(
        groupchat=groupchat,
        llm_config={"config_list": config_list}  
    )

    trace = langfuse.trace(name="DataQuery", metadata={"task": "Query customer data from CSV"})

    for agent in agents:
        wrap_agent_with_tracing(agent, trace.id)

    user_proxy = agents[0]

    user_proxy.initiate_chat(
        recipient=manager,
        message="Please provide the product name with the highest price on the data you have."
    )

    langfuse.flush()

if __name__ == "__main__":
    main_logic()
