import typing
from abc import ABC, abstractmethod

from crewai import Agent
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

from enums.AgentPurpose import AgentPurpose
from enums.AiModel import AiModel
from state.AppState import AppState

agent_callback = typing.Callable[[str], None]
llm_type = ChatAnthropic | ChatOpenAI


class BaseAgent(ABC):
    # temperature: int = NotImplemented
    callback: agent_callback = NotImplemented
    llm: llm_type = NotImplemented

    @abstractmethod
    def __init__(self,
                 callback: agent_callback,
                 llm: llm_type,
                 ) -> None:
        self.callback = callback
        self.llm = llm

    @abstractmethod
    def create(self) -> Agent:
        raise NotImplementedError


class JudgeAgent(BaseAgent):
    def __init__(self,
                 callback: agent_callback,
                 llm: llm_type
                 ) -> None:
        self.callback = callback
        self.llm = llm

    def create(self) -> Agent:
        return Agent(
            role='',
            goal='',
            backstory='',
            tools=[],
            llm=self.llm,
            max_iter=5,
            max_rpm=5,
            verbose=True,
            allow_delegation=True,
            step_callback=self.callback,
            cache=True
        )


class WitnessAgent(BaseAgent):
    def __init__(self,
                 callback: agent_callback,
                 llm: llm_type
                 ) -> None:
        self.callback = callback
        self.llm = llm

    def create(self) -> Agent:
        return Agent(
            role='',
            goal='',
            backstory='',
            tools=[],
            llm=self.llm,
            max_iter=5,
            max_rpm=5,
            verbose=True,
            allow_delegation=True,
            step_callback=self.callback,
            cache=True
        )


class ProsecutionAgent(BaseAgent):
    def __init__(self,
                 callback: agent_callback,
                 llm: llm_type
                 ) -> None:
        self.callback = callback
        self.llm = llm

    def create(self) -> Agent:
        return Agent(
            role='',
            goal='',
            backstory='',
            tools=[],
            llm=self.llm,
            max_iter=5,
            max_rpm=5,
            verbose=True,
            allow_delegation=True,
            step_callback=self.callback,
            cache=True
        )


class DefenseAgent(BaseAgent):
    def __init__(self,
                 callback: agent_callback,
                 llm: llm_type
                 ) -> None:
        self.callback = callback
        self.llm = llm

    def create(self) -> Agent:
        return Agent(
            role='',
            goal='',
            backstory='',
            tools=[],
            llm=self.llm,
            max_iter=5,
            max_rpm=5,
            verbose=True,
            allow_delegation=True,
            step_callback=self.callback,
            cache=True
        )


class JuryAgent(BaseAgent):
    def __init__(self,
                 callback: agent_callback,
                 llm: llm_type
                 ) -> None:
        self.callback = callback
        self.llm = llm

    def create(self) -> Agent:
        return Agent(
            role='',
            goal='',
            backstory='',
            tools=[],
            llm=self.llm,
            max_iter=5,
            max_rpm=5,
            verbose=True,
            allow_delegation=True,
            step_callback=self.callback,
            cache=True
        )


class AgentsManager:
    # temperature = AppState.get_value(f'{agent_name}_temperature') # TODO: Dodać w całej aplikacji i dodać do obiektów poniżej

    def get_judge_agent(self, callback: agent_callback) -> Agent:
        agent = JudgeAgent(
            callback,
            self._get_llm_by_choose(AgentPurpose.JUDGE)
        )

        return agent.create()

    def get_jury_agent(self, callback: agent_callback) -> Agent:
        agent = JuryAgent(
            callback,
            self._get_llm_by_choose(AgentPurpose.JURY)
        )

        return agent.create()

    def get_witness_agent(self, callback: agent_callback) -> Agent:
        agent = WitnessAgent(
            callback,
            self._get_llm_by_choose(AgentPurpose.WITNESS)
        )

        return agent.create()

    def get_prosecution_agent(self, callback: agent_callback) -> Agent:
        agent = ProsecutionAgent(
            callback,
            self._get_llm_by_choose(AgentPurpose.PROSECUTOR)
        )

        return agent.create()

    def get_defense_agent(self, callback: agent_callback) -> Agent:
        agent = DefenseAgent(
            callback,
            self._get_llm_by_choose(AgentPurpose.DEFENSE)
        )

        return agent.create()

    def _get_llm_by_choose(self, agent_name: AgentPurpose):
        model = AppState.get_value(f'{agent_name.value.lower()}_model')
        open_ai_api_key = AppState.get_value('openai_key')
        anthropic_api_key = AppState.get_value('anthropic_key')

        match model:
            case AiModel.OPEN_AI_GPT_35_TURBO:
                return ChatOpenAI(
                    api_key=open_ai_api_key,
                    model=AiModel.get_tech_name(AiModel.OPEN_AI_GPT_35_TURBO)
                )
            case AiModel.OPEN_AI_GPT_4_TURBO:
                return ChatOpenAI(
                    api_key=open_ai_api_key,
                    model=AiModel.get_tech_name(AiModel.OPEN_AI_GPT_4_TURBO)
                )
            case AiModel.OPEN_AI_GPT_4_O:
                return ChatOpenAI(
                    api_key=open_ai_api_key,
                    model=AiModel.get_tech_name(AiModel.OPEN_AI_GPT_4_O)
                )
            case AiModel.ANTHROPIC_CLAUDE_HAIKU:
                return ChatAnthropic(
                    api_key=anthropic_api_key,
                    model_name=AiModel.get_tech_name(AiModel.ANTHROPIC_CLAUDE_HAIKU)
                )
            case AiModel.ANTHROPIC_CLAUDE_SONNET:
                return ChatAnthropic(
                    api_key=anthropic_api_key,
                    model_name=AiModel.get_tech_name(AiModel.ANTHROPIC_CLAUDE_SONNET)
                )
            case AiModel.ANTHROPIC_CLAUDE_OPUS:
                return ChatAnthropic(
                    api_key=anthropic_api_key,
                    model_name=AiModel.get_tech_name(AiModel.ANTHROPIC_CLAUDE_OPUS)
                )
