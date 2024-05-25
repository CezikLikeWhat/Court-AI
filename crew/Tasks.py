from abc import ABC, abstractmethod
from textwrap import dedent
from typing import List, Callable, Dict, Tuple

import streamlit
from crewai import Task, Agent
from crewai.tasks.task_output import TaskOutput

from crew import models

agent_callback = Callable[[str, streamlit.container, str | TaskOutput | None], None]


class BaseTask(ABC):
    agent: Agent = NotImplemented
    callback: agent_callback = NotImplemented

    @abstractmethod
    def __init__(self, agent: Agent, callback: agent_callback) -> None:
        self.agent = agent
        self.callback = callback

    @abstractmethod
    def create(self) -> Task | List[Task]:
        raise NotImplementedError


class JudgeTask(BaseTask):
    def __init__(self, agent: Agent, callback: agent_callback) -> None:
        self.agent = agent
        self.callback = callback

    def create(self) -> List[Task]:
        return [
            Task(
                description='Open the court session, ensuring all participants are ready and present, and make an opening statement.',
                expected_output=dedent('''
                The judge announces the beginning of the court session and introduces the case to be heard. 
                Max 2 sentences.
                Plain text.
                '''),
                agent=self.agent,
                callback=self.callback
            ),
            Task(
                description='Call the prosecutor to present their opening statement and initial arguments.',
                expected_output='The judge calls the prosecutor to the stand to present their opening statement. Max 2 sentences. Plain text',
                agent=self.agent,
                callback=self.callback
            ),
            Task(
                description='Call the defense attorney to present their opening statement and initial arguments.',
                expected_output='The judge calls the defense attorney to the stand to present their opening statement. Max 2 sentences. Plain text.',
                agent=self.agent,
                callback=self.callback
            ),
            Task(
                description='Call a witness to the stand to provide their testimony regarding the case.',
                expected_output='The judge calls the witness to the stand to provide their testimony. Max 2 sentences. Plain text.',
                agent=self.agent,
                callback=self.callback
            ),
            Task(
                description='Deliver the final verdict based on the evidence and arguments presented, providing a brief explanation.',
                expected_output='The judge delivers the final verdict, stating whether the defendant is guilty or not guilty, with a brief explanation of the decision. Max 2 sentences. Plain text.',
                agent=self.agent,
                callback=self.callback
            )
        ]


class WitnessTask(BaseTask):
    def __init__(self, agent: Agent, callback: agent_callback) -> None:
        self.agent = agent
        self.callback = callback

    def create(self) -> Task:
        return Task(
            description='Provide testimony based on personal knowledge and experience related to the case. Answer questions posed by both the prosecution and the defense.',
            expected_output='The witness gives a detailed account of what they saw or know about the case, answering all questions from the prosecution and the defense clearly and truthfully.',
            agent=self.agent,
            callback=self.callback
        )


class ProsecutionTask(BaseTask):
    def __init__(self, agent: Agent, callback: agent_callback) -> None:
        self.agent = agent
        self.callback = callback

    def create(self) -> Task:
        return Task(
            description='Present the case against the defendant, including opening statements, presenting evidence, and questioning witnesses to prove the defendant’s guilt beyond a reasonable doubt.',
            expected_output='The prosecution delivers a compelling opening statement, presents strong evidence, effectively questions the witness to support the case, and delivers a persuasive closing argument.',
            agent=self.agent,
            callback=self.callback
        )


class DefenseTask(BaseTask):
    def __init__(self, agent: Agent, callback: agent_callback) -> None:
        self.agent = agent
        self.callback = callback

    def create(self) -> Task:
        return Task(
            description='Defend the accused by presenting evidence and arguments that create reasonable doubt about the defendant’s guilt. Question witnesses to challenge the prosecution’s case.',
            expected_output='The defense delivers a strong opening statement, presents exculpatory evidence, effectively cross-examines the witness to create doubt, and delivers a convincing closing argument.',
            agent=self.agent,
            callback=self.callback
        )


class JuryTask(BaseTask):
    def __init__(self, agent: Agent, callback: agent_callback) -> None:
        self.agent = agent
        self.callback = callback

    def create(self) -> Task:
        return Task(
            description='Deliberate on the evidence presented by both the prosecution and the defense, discuss with fellow jurors, and deliver a fair and impartial verdict.',
            expected_output='The jury listens carefully to all evidence and arguments, engages in thorough deliberation with fellow jurors, and finally delivers a unanimous or majority verdict based on their discussions.',
            agent=self.agent,
            callback=self.callback
        )


class TasksFactory:
    def get_judge_tasks(self, agent: Agent, callback: agent_callback) -> List[Task]:
        task = JudgeTask(
            agent,
            callback
        )

        return task.create()

    def get_jury_tasks(self, agent: Agent, callback: agent_callback) -> Task:
        task = JuryTask(
            agent,
            callback
        )

        return task.create()

    def get_witness_task(self, agent: Agent, callback: agent_callback) -> Task:
        task = WitnessTask(
            agent,
            callback
        )

        return task.create()

    def get_prosecution_task(self, agent: Agent, callback: agent_callback) -> Task:
        task = ProsecutionTask(
            agent,
            callback
        )

        return task.create()

    def get_defense_task(self, agent: Agent, callback: agent_callback) -> Task:
        task = DefenseTask(
            agent,
            callback
        )

        return task.create()
