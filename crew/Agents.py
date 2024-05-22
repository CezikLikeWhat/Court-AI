import os
from abc import ABC, abstractmethod
from typing import Callable, List

from crewai import Agent
from langchain_anthropic import ChatAnthropic
from langchain_community.chat_models import ChatOllama
from langchain_core.language_models import BaseChatModel
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI

from enums.AgentPurpose import AgentPurpose
from enums.AiModel import AiModel
from state.AppState import AppState

agent_callback = Callable[[str], None]


class BaseAgent(ABC):
    callback: agent_callback = NotImplemented
    llm: BaseChatModel = NotImplemented
    tools: List[BaseTool] = NotImplemented

    @abstractmethod
    def __init__(self,
                 callback: agent_callback,
                 llm: BaseChatModel,
                 tools: List[BaseTool]
                 ) -> None:
        self.callback = callback
        self.llm = llm
        self.tools = tools

    @abstractmethod
    def create(self) -> Agent:
        raise NotImplementedError


class JudgeAgent(BaseAgent):
    def __init__(self,
                 callback: agent_callback,
                 llm: BaseChatModel,
                 tools: List[BaseTool]
                 ) -> None:
        self.callback = callback
        self.llm = llm
        self.tools = tools

    def create(self) -> Agent:
        return Agent(
            role='A Judge in the supreme court',
            goal='Conduct a court hearing and issue a final verdict based on the evidence presented by the prosecution and the witness defense',
            backstory='As a top supreme court judge, you have honed your skills in law and have handled a huge number of court cases. Thanks to them, you are able to make a final judgment based on the evidence in the case',
            tools=self.tools,
            llm=self.llm,
            max_iter=1,
            max_rpm=20,
            verbose=True,
            memory=True,
            allow_delegation=True,
            step_callback=self.callback,
            cache=True
        )


class WitnessAgent(BaseAgent):
    def __init__(self,
                 callback: agent_callback,
                 llm: BaseChatModel,
                 tools: List[BaseTool]
                 ) -> None:
        self.callback = callback
        self.llm = llm
        self.tools = tools

    def create(self) -> Agent:
        return Agent(
            role='Witness at court hearing',
            goal='You were at the scene and based on your knowledge you are able to answer the questions asked by the prosecution and the defense of the accused',
            backstory='',
            tools=self.tools,
            llm=self.llm,
            max_iter=5,
            max_rpm=20,
            verbose=True,
            memory=True,
            allow_delegation=True,
            step_callback=self.callback,
            cache=True
        )


class ProsecutionAgent(BaseAgent):
    def __init__(self,
                 callback: agent_callback,
                 llm: BaseChatModel,
                 tools: List[BaseTool]
                 ) -> None:
        self.callback = callback
        self.llm = llm
        self.tools = tools

    def create(self) -> Agent:
        return Agent(
            role='Prosecutor at court hearing',
            goal='Present evidence and arguments that prove the guilt of the accused beyond a reasonable doubt',
            backstory='As a seasoned prosecutor with a track record of high-profile cases, you are known for your meticulous preparation and compelling arguments. You firmly believe in the justice system and your role in ensuring that criminals are held accountable for their actions.',
            tools=self.tools,
            llm=self.llm,
            max_iter=5,
            max_rpm=20,
            verbose=True,
            memory=True,
            allow_delegation=True,
            step_callback=self.callback,
            cache=True
        )


class DefenseAgent(BaseAgent):
    def __init__(self,
                 callback: agent_callback,
                 llm: BaseChatModel,
                 tools: List[BaseTool]
                 ) -> None:
        self.callback = callback
        self.llm = llm
        self.tools = tools

    def create(self) -> Agent:
        return Agent(
            role='Defense attorney at court hearing',
            goal='Present evidence and arguments that create reasonable doubt about the guilt of the accused and ensure they receive a fair trial',
            backstory='With years of experience in defending clients in criminal cases, you are known for your tenacity and skill in the courtroom. You are committed to protecting the rights of the accused and ensuring that the burden of proof lies with the prosecution.',
            tools=self.tools,
            llm=self.llm,
            max_iter=5,
            max_rpm=20,
            verbose=True,
            memory=True,
            allow_delegation=True,
            step_callback=self.callback,
            cache=True
        )


class JuryAgent(BaseAgent):
    def __init__(self,
                 callback: agent_callback,
                 llm: BaseChatModel,
                 tools: List[BaseTool]
                 ) -> None:
        self.callback = callback
        self.llm = llm
        self.tools = tools

    def create(self) -> Agent:
        return Agent(
            role='Jury member at court hearing',
            goal='Listen to the evidence presented by both the prosecution and the defense, deliberate with fellow jurors, and deliver a fair and impartial verdict based on the evidence',
            backstory='You are part of a diverse group of citizens selected to serve as a juror in this case. Your background and experiences bring a unique perspective to the jury deliberation process. You understand the gravity of your duty and are committed to delivering a just verdict based on the evidence presented.',
            tools=self.tools,
            llm=self.llm,
            max_iter=5,
            max_rpm=20,
            verbose=True,
            memory=True,
            allow_delegation=True,
            step_callback=self.callback,
            cache=True
        )


class AgentsManager:
    def get_judge_agent(self, callback: agent_callback) -> Agent:
        agent = JudgeAgent(
            callback,
            self._get_llm_by_choose(AgentPurpose.JUDGE),
            []
        )

        return agent.create()

    def get_jury_agent(self, callback: agent_callback) -> Agent:
        agent = JuryAgent(
            callback,
            self._get_llm_by_choose(AgentPurpose.JURY),
            []
        )

        return agent.create()

    def get_witness_agent(self, callback: agent_callback) -> Agent:
        agent = WitnessAgent(
            callback,
            self._get_llm_by_choose(AgentPurpose.WITNESS),
            []
        )

        return agent.create()

    def get_prosecution_agent(self, callback: agent_callback) -> Agent:
        agent = ProsecutionAgent(
            callback,
            self._get_llm_by_choose(AgentPurpose.PROSECUTOR),
            []
        )

        return agent.create()

    def get_defense_agent(self, callback: agent_callback) -> Agent:
        agent = DefenseAgent(
            callback,
            self._get_llm_by_choose(AgentPurpose.DEFENSE),
            []
        )

        return agent.create()

    def _get_llm_by_choose(self, agent_name: AgentPurpose) -> BaseChatModel:
        model = AppState.get_value(f'{agent_name.value.lower()}_model')
        open_ai_api_key = AppState.get_value('openai_key')
        anthropic_api_key = AppState.get_value('anthropic_key')
        temperature = AppState.get_value(f'{agent_name.value.lower()}_temperature')

        match model:
            case AiModel.OPEN_AI_GPT_35_TURBO:
                return ChatOpenAI(
                    api_key=open_ai_api_key,
                    model=AiModel.get_tech_name(AiModel.OPEN_AI_GPT_35_TURBO),
                    temperature=temperature
                )
            case AiModel.OPEN_AI_GPT_4_TURBO:
                return ChatOpenAI(
                    api_key=open_ai_api_key,
                    model=AiModel.get_tech_name(AiModel.OPEN_AI_GPT_4_TURBO),
                    temperature=temperature
                )
            case AiModel.OPEN_AI_GPT_4_O:
                return ChatOpenAI(
                    api_key=open_ai_api_key,
                    model=AiModel.get_tech_name(AiModel.OPEN_AI_GPT_4_O),
                    temperature=temperature
                )
            case AiModel.ANTHROPIC_CLAUDE_HAIKU:
                return ChatAnthropic(
                    api_key=anthropic_api_key,
                    model_name=AiModel.get_tech_name(AiModel.ANTHROPIC_CLAUDE_HAIKU),
                    temperature=temperature
                )
            case AiModel.ANTHROPIC_CLAUDE_SONNET:
                return ChatAnthropic(
                    api_key=anthropic_api_key,
                    model_name=AiModel.get_tech_name(AiModel.ANTHROPIC_CLAUDE_SONNET),
                    temperature=temperature
                )
            case AiModel.ANTHROPIC_CLAUDE_OPUS:
                return ChatAnthropic(
                    api_key=anthropic_api_key,
                    model_name=AiModel.get_tech_name(AiModel.ANTHROPIC_CLAUDE_OPUS),
                    temperature=temperature
                )
            case AiModel.LLAMA_3_8B:
                return ChatOllama(
                    base_url=os.getenv('OLLAMA_URL'),
                    model='llama3',
                    temperature=temperature,
                    stream=False
                )