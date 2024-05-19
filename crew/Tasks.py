from abc import ABC, abstractmethod

from crewai import Task, Agent


class BaseTask(ABC):
    agent: Agent = NotImplemented

    @abstractmethod
    def __init__(self, agent: Agent) -> None:
        self.agent = agent

    @abstractmethod
    def create(self) -> Task:
        raise NotImplementedError


class JudgeTask(BaseTask):
    def __init__(self, agent: Agent) -> None:
        self.agent = agent

    def create(self) -> Task:
        return Task(
            description='',
            expected_output='',
            agent=self.agent
        )


class WitnessTask(BaseTask):
    def __init__(self, agent: Agent) -> None:
        self.agent = agent

    def create(self) -> Task:
        return Task(
            description='',
            expected_output='',
            agent=self.agent
        )


class ProsecutionTask(BaseTask):
    def __init__(self, agent: Agent) -> None:
        self.agent = agent

    def create(self) -> Task:
        return Task(
            description='',
            expected_output='',
            agent=self.agent
        )


class DefenseTask(BaseTask):
    def __init__(self, agent: Agent) -> None:
        self.agent = agent

    def create(self) -> Task:
        return Task(
            description='',
            expected_output='',
            agent=self.agent
        )


class JuryTask(BaseTask):
    def __init__(self, agent: Agent) -> None:
        self.agent = agent

    def create(self) -> Task:
        return Task(
            description='',
            expected_output='',
            agent=self.agent
        )


class TasksManager:
    def get_judge_tasks(self, agent: Agent) -> Task:
        task = JudgeTask(
            agent
        )

        return task.create()

    def get_jury_tasks(self, agent: Agent) -> Task:
        task = JuryTask(
            agent
        )

        return task.create()

    def get_witness_task(self, agent: Agent) -> Task:
        task = WitnessTask(
            agent
        )

        return task.create()

    def get_prosecution_task(self, agent: Agent) -> Task:
        task = ProsecutionTask(
            agent
        )

        return task.create()

    def get_defense_task(self, agent: Agent) -> Task:
        task = DefenseTask(
            agent
        )

        return task.create()
