# CSV Agent System

This project is a data query agent system that interacts with a dataset and provides insights using AI models. The system employs Langfuse for tracing and monitoring, Autogen for agent-based conversation management, and Redis for memory management. This setup is intended for production-level applications, providing performance tracking and real-time observation.

## Overview

The system is designed to perform the following tasks:

- Load data from a CSV file using pandas.
- Set up agents that can query the dataset and provide insights.
- Track the performance and execution of agents with Langfuse.
- Use Redis for memory management, specifically LangMem to manage agent data and states.
- The conversation is managed by Autogen 0.4, enabling dynamic interactions between agents.

## Approach

The system utilizes several key technologies to achieve the desired functionality:

### 1. **Data Loading and Setup**
- The system loads data from a CSV file into a pandas DataFrame. 
- The dataset is passed to the agents to allow them to calculate and return insights.
  
### 2. **Agent Setup**
- The system sets up two primary agents:
  - **User Proxy Agent:** This agent handles user inputs and forwards the requests to the manager.
  - **Data Query Agent:** This agent queries the dataset and returns insights based on the input data.

### 3. **Langfuse Monitoring and Tracing**
- **Langfuse** is used to monitor and trace the performance of the agents.
- The system creates a trace for each user request and logs execution time, status, and response for better visibility into agent performance.
- This enables efficient tracking of interactions and helps optimize the model's performance.

### 4. **Autogen and Group Chat Management**
- **Autogen** is responsible for managing the conversation between the agents. It supports dynamic agent roles and controls the interaction flow.
- **GroupChat** and **GroupChatManager** handle message routing and execution within the agent system.
- A round-robin approach is used for agent participation, ensuring that all agents have a chance to respond.

### 5. **Redis and LangMem for Memory Management**
- **Redis** is utilized to store and manage data persistently between interactions.
- **LangMem** provides in-memory storage for agent data and states, making the conversation context-aware and enabling agents to use previous interactions to influence their responses.

### 6. **Production Monitoring and Observation**
- With **Langfuse**, the system provides robust production monitoring and observation, ensuring that all executions are traced and performance is consistently tracked.
- This setup is ideal for real-time production systems where continuous monitoring is essential.

## Key Components

### 1. **Autogen 0.4**
- Autogen is an agent-based system for building conversational AI. It allows you to define multiple agents, each with specific tasks, and manage their interactions seamlessly.

### 2. **Langfuse (Model Production Observability & Monitoring)**
- Langfuse is a powerful tool for monitoring and tracing the execution of AI models in production. It enables performance tracking and logging, helping you optimize your system.

### 3. **Redis and LangMem (Memory Interference)**
- Redis is an in-memory data store used for fast and persistent storage of data between agent interactions.
- LangMem is an extension to Redis that helps manage the state of agents dynamically, ensuring that the conversation is context-aware.

## Running the System

### Prerequisites

- Python 3.7 or above
- Required Python libraries (can be installed using `pip install -r requirements.txt`)
  - pandas
  - dotenv
  - autogen
  - langfuse
  - redis
  - langmem

### Setup

1. Clone the repository.
2. Create a `.env` file in the root directory and add the following environment variables:
    ```env
    LANGFUSE_PRIVATE_KEY=<your_langfuse_private_key>
    LANGFUSE_PUBLIC_KEY=<your_langfuse_public_key>
    GROQ_API_KEY=<your_groq_api_key>
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the script to start the system:
    ```bash
    python -u path_to_script.py
    ```

### Configuration

- **CSV File:** The dataset file is located at `'D:/Extensa_Files/Akaike_Project/Dataset/myntra.csv'`. Modify the path as needed.
- **Autogen Configuration:** The system uses Autogen 0.4, which manages the conversation between agents and allows them to process the dataset and respond to queries.

## Monitoring and Tracing

The system uses **Langfuse** to trace the execution of agents. It tracks:
- **Execution Time**: How long each agent takes to respond.
- **Status**: Whether the response was successful or failed.
- **Error Details**: If any error occurs, it is logged with the error message.

These traces provide insight into agent performance, allowing for quick identification and resolution of issues.

## Memory Interference with LangMem and Redis

- **LangMem** ensures that the system has access to the most recent agent states.
- **Redis** stores the state of each agent persistently, enabling the system to recover agent data after restarts and maintain consistent state across multiple runs.

