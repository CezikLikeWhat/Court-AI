import json
from typing import List, Union, Tuple, Dict

from crewai import Crew, Agent, Task, Process
from langchain_community.chat_models import ChatOllama
from langchain_core.agents import AgentFinish

agent_finishes = []
call_number = 0

OLLAMA = ChatOllama(
    base_url='http://localhost:11434',
    model='llama3'
)


def print_output(agent_output: Union[str, List[Tuple[Dict, str]], AgentFinish], agent_name: str = 'Generic call'):
    global call_number
    call_number += 1
    with open('../logs/callback_logs.txt', 'a') as log_file:
        if isinstance(agent_output, str):
            try:
                agent_output = json.loads(agent_output)
            except json.JSONDecodeError:
                pass

        if isinstance(agent_output, list) and all(isinstance(item, tuple) for item in agent_output):
            print(f'-{call_number}----Dict------------------------------------------', file=log_file)
            for action, description in agent_output:
                print(f'Agent Name: {agent_name}', file=log_file)
                print(f'Tool used: {getattr(action, 'tool', 'Unknown')}', file=log_file)
                print(f'Tool input: {getattr(action, 'tool_input', 'Unknown')}', file=log_file)
                print(f'Action log: {getattr(action, 'log', 'Unknown')}', file=log_file)
                print(f'Description: {description}', file=log_file)
                print('--------------------------------------------------', file=log_file)

        elif isinstance(agent_output, AgentFinish):
            print(f'-{call_number}----AgentFinish---------------------------------------', file=log_file)
            print(f'Agent Name: {agent_name}', file=log_file)
            agent_finishes.append(agent_output)
            output = agent_output.return_values
            print(f'AgentFinish Output: {output['output']}', file=log_file)
            print('--------------------------------------------------', file=log_file)

        else:
            print(f'-{call_number}-Unknown format of agent_output:', file=log_file)
            print(type(agent_output), file=log_file)
            print(agent_output, file=log_file)


class CourtCrew:
    def get_crew(self, agents: List[Agent], tasks: List[Task]):
        return Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=2,
            share_crew=False,
            full_output=True,
            manager_llm=OLLAMA,
            max_iter=15,
            step_callback=lambda x: print_output(x, 'SuperVisor')
        )
