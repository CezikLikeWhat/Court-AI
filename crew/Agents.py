import os
from abc import ABC, abstractmethod
from textwrap import dedent
from typing import List

from crewai import Agent
from langchain_anthropic import ChatAnthropic
from langchain_community.chat_models import ChatOllama
from langchain_core.language_models import BaseChatModel
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI

from enums.AgentPurpose import AgentPurpose
from enums.AiModel import AiModel
from state.AppState import AppState


class BaseAgent(ABC):
    llm: BaseChatModel = NotImplemented
    tools: List[BaseTool] = NotImplemented
    case_description: str = NotImplemented

    @abstractmethod
    def __init__(self,
                 llm: BaseChatModel,
                 tools: List[BaseTool],
                 case_description: str
                 ) -> None:
        self.llm = llm
        self.tools = tools
        self.case_description = case_description

    @abstractmethod
    def create(self) -> Agent:
        raise NotImplementedError


class JudgeAgent(BaseAgent):
    def __init__(self,
                 llm: BaseChatModel,
                 tools: List[BaseTool],
                 case_description: str
                 ) -> None:
        self.llm = llm
        self.tools = tools
        self.case_description = case_description

    def create(self) -> Agent:
        return Agent(
            role='A Judge in the supreme court',
            goal='Conduct a court hearing and issue a final verdict based on the evidence presented by the prosecution and the defense.',
            backstory=dedent(f'''
            As a top supreme court judge, you have honed your skills in law and have handled numerous court cases.
            Your extensive experience allows you to make fair and informed judgments based on the evidence and arguments presented.
            
            Case description:
            {self.case_description}
            '''),
            tools=self.tools,
            llm=self.llm,
            max_iter=1,
            max_rpm=20,
            verbose=True,
            memory=True,
            allow_delegation=True,
            cache=True
        )


class WitnessAgent(BaseAgent):
    def __init__(self,
                 llm: BaseChatModel,
                 tools: List[BaseTool],
                 case_description: str
                 ) -> None:
        self.llm = llm
        self.tools = tools
        self.case_description = case_description

    def create(self) -> Agent:
        return Agent(
            role='Witness at court hearing',
            goal='Provide truthful testimony based on personal knowledge and experience, answering questions posed by both the prosecution and the defense.',
            backstory=dedent(f'''
            You were at the scene of the incident and have firsthand knowledge of what transpired.
            Your testimony is crucial in helping the court understand the facts of the case.
            
            Case description:
            {self.case_description}
            '''),
            tools=self.tools,
            llm=self.llm,
            max_iter=5,
            max_rpm=20,
            verbose=True,
            memory=True,
            allow_delegation=True,
            cache=True
        )


class ProsecutionAgent(BaseAgent):
    def __init__(self,
                 llm: BaseChatModel,
                 tools: List[BaseTool],
                 case_description: str
                 ) -> None:
        self.llm = llm
        self.tools = tools
        self.case_description = case_description

    def create(self) -> Agent:
        return Agent(
            role='Prosecutor at court hearing',
            goal='Present evidence and arguments that prove the guilt of the accused beyond a reasonable doubt.',
            backstory=dedent(f'''
            As a seasoned prosecutor with a track record of high-profile cases, you are known for your meticulous preparation and compelling arguments.
            You believe in the justice system and your role in ensuring that criminals are held accountable for their actions.
            
            Case description:
            {self.case_description}
            '''),
            tools=self.tools,
            llm=self.llm,
            max_iter=5,
            max_rpm=20,
            verbose=True,
            memory=True,
            allow_delegation=True,
            cache=True
        )


class DefenseAgent(BaseAgent):
    def __init__(self,
                 llm: BaseChatModel,
                 tools: List[BaseTool],
                 case_description: str
                 ) -> None:
        self.llm = llm
        self.tools = tools
        self.case_description = case_description

    def create(self) -> Agent:
        return Agent(
            role='Defense attorney at court hearing',
            goal='Present evidence and arguments that create reasonable doubt about the guilt of the accused and ensure they receive a fair trial.',
            backstory=dedent(f'''
            With years of experience defending clients in criminal cases, you are known for your tenacity and skill in the courtroom.
            You are committed to protecting the rights of the accused and ensuring that the burden of proof lies with the prosecution.
            
            Case description:
            {self.case_description}
            '''),
            tools=self.tools,
            llm=self.llm,
            max_iter=5,
            max_rpm=20,
            verbose=True,
            memory=True,
            allow_delegation=True,
            cache=True
        )


class JuryAgent(BaseAgent):
    def __init__(self,
                 llm: BaseChatModel,
                 tools: List[BaseTool],
                 case_description: str
                 ) -> None:
        self.llm = llm
        self.tools = tools
        self.case_description = case_description

    def create(self) -> Agent:
        return Agent(
            role='Jury member at court hearing',
            goal='Listen to the evidence presented by both the prosecution and the defense, deliberate with fellow jurors, and deliver a fair and impartial verdict based on the evidence.',
            backstory=dedent(f'''
            You are part of a diverse group of citizens selected to serve as a juror in this case.
            Your background and experiences bring a unique perspective to the jury deliberation process.
            You understand the gravity of your duty and are committed to delivering a just verdict based on the evidence presented.
            
            Case description:
            {self.case_description}
            '''),
            tools=self.tools,
            llm=self.llm,
            max_iter=5,
            max_rpm=20,
            verbose=True,
            memory=True,
            allow_delegation=True,
            cache=True
        )


class AgentsFactory:
    def judge_agent(self) -> Agent:
        agent = JudgeAgent(
            self._get_llm_by_choose(AgentPurpose.JUDGE),
            [],
            AppState.get_value('case_description')
        )

        return agent.create()

    def jury_agent(self) -> Agent:
        agent = JuryAgent(
            self._get_llm_by_choose(AgentPurpose.JURY),
            [],
            AppState.get_value('case_description')
        )

        return agent.create()

    def witness_agent(self) -> Agent:
        agent = WitnessAgent(
            self._get_llm_by_choose(AgentPurpose.WITNESS),
            [],
            AppState.get_value('case_description')
        )

        return agent.create()

    def prosecution_agent(self) -> Agent:
        agent = ProsecutionAgent(
            self._get_llm_by_choose(AgentPurpose.PROSECUTOR),
            [],
            AppState.get_value('case_description')
        )

        return agent.create()

    def defense_agent(self) -> Agent:
        agent = DefenseAgent(
            self._get_llm_by_choose(AgentPurpose.DEFENSE),
            [],
            AppState.get_value('case_description')
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
