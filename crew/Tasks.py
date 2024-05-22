from abc import ABC, abstractmethod
from typing import List

from crewai import Task, Agent

from crew import models


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

    def create(self) -> List[Task]:
        return [
            Task(
                description='Open the court session, ensuring all participants are ready and present, and make an opening statement.',
                expected_output='The judge announces the beginning of the court session and introduces the case to be heard. Max 2 sentences. Plain text.',
                expected_json=models.WelcomeObject,
                agent=self.agent
            ),
            Task(
                description='Call the prosecutor to present their opening statement and initial arguments.',
                expected_output='The judge calls the prosecutor to the stand to present their opening statement. Max 2 sentences. Plain text.',
                expected_json=models.WelcomeObject,
                agent=self.agent
            ),
            Task(
                description='Call the defense attorney to present their opening statement and initial arguments.',
                expected_output='The judge calls the defense attorney to the stand to present their opening statement. Max 2 sentences. Plain text.',
                expected_json=models.WelcomeObject,
                agent=self.agent
            ),
            Task(
                description='Call a witness to the stand to provide their testimony regarding the case.',
                expected_output='The judge calls the witness to the stand to provide their testimony. Max 2 sentences. Plain text.',
                expected_json=models.WelcomeObject,
                agent=self.agent
            ),
            Task(
                description='Deliver the final verdict based on the evidence and arguments presented, providing a brief explanation.',
                expected_output='The judge delivers the final verdict, stating whether the defendant is guilty or not guilty, with a brief explanation of the decision. Max 2 sentences. Plain text.',
                expected_json=models.WelcomeObject,
                agent=self.agent
            ),
        ]
        # return Task(
        #     description='Conduct the court hearing by ensuring all procedures are followed, manage the courtroom, and issue a final verdict based on the evidence presented.',
        #     expected_output='The judge opens the court session, ensures both sides present their arguments, oversees witness questioning, and finally delivers a verdict of either guilty or not guilty based on the evidence and arguments presented. Max 2 sentence. Plain text.',
        #     expected_json=models.WelcomeObject,
        #     agent=self.agent
        # )
        # return Task(
        #     description='Greeting the user',
        #     expected_output='Text welcoming the user. Max 2 sentence. Plain text.',
        #     expected_json=models.WelcomeObject,
        #     agent=self.agent
        # )


class WitnessTask(BaseTask):
    def __init__(self, agent: Agent) -> None:
        self.agent = agent

    def create(self) -> Task:
        return Task(
            description='Provide testimony based on personal knowledge and experience related to the case. Answer questions posed by both the prosecution and the defense.',
            expected_output='The witness gives a detailed account of what they saw or know about the case, answering all questions from the prosecution and the defense clearly and truthfully.',
            agent=self.agent
        )


class ProsecutionTask(BaseTask):
    def __init__(self, agent: Agent) -> None:
        self.agent = agent

    def create(self) -> Task:
        return Task(
            description='Present the case against the defendant, including opening statements, presenting evidence, and questioning witnesses to prove the defendant’s guilt beyond a reasonable doubt.',
            expected_output='The prosecution delivers a compelling opening statement, presents strong evidence, effectively questions the witness to support the case, and delivers a persuasive closing argument.',
            agent=self.agent
        )


class DefenseTask(BaseTask):
    def __init__(self, agent: Agent) -> None:
        self.agent = agent

    def create(self) -> Task:
        return Task(
            description='Defend the accused by presenting evidence and arguments that create reasonable doubt about the defendant’s guilt. Question witnesses to challenge the prosecution’s case.',
            expected_output='The defense delivers a strong opening statement, presents exculpatory evidence, effectively cross-examines the witness to create doubt, and delivers a convincing closing argument.',
            agent=self.agent
        )


class JuryTask(BaseTask):
    def __init__(self, agent: Agent) -> None:
        self.agent = agent

    def create(self) -> Task:
        return Task(
            description='Deliberate on the evidence presented by both the prosecution and the defense, discuss with fellow jurors, and deliver a fair and impartial verdict.',
            expected_output='The jury listens carefully to all evidence and arguments, engages in thorough deliberation with fellow jurors, and finally delivers a unanimous or majority verdict based on their discussions.',
            agent=self.agent
        )


class TasksManager:
    def get_judge_tasks(self, agent: Agent) -> List[Task]:
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
