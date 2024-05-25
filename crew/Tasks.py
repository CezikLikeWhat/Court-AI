from abc import ABC, abstractmethod
from textwrap import dedent
from typing import List, Callable

import streamlit
from crewai import Task, Agent
from crewai.tasks.task_output import TaskOutput

agent_callback = Callable[[str, streamlit.container, str | TaskOutput | None], None]


def add_prompt_contraints(sentences: int = 2, text_type: str = 'plain'):
    return dedent(f'''
                  Max {sentences} sentences. 
                  Return {text_type} text.
                  DO NOT include any quotes.
                  ''')


class BaseTask(ABC):
    agent: Agent = NotImplemented
    callback: agent_callback = NotImplemented

    @abstractmethod
    def __init__(self, agent: Agent, callback: agent_callback) -> None:
        self.agent = agent
        self.callback = callback

    @abstractmethod
    def create(self) -> List[Task]:
        raise NotImplementedError


class JudgeTask(BaseTask):
    def __init__(self, agent: Agent, callback: agent_callback) -> None:
        self.agent = agent
        self.callback = callback

    def create(self) -> List[Task]:
        return [
            Task(
                description='Open the court session, ensuring all participants are ready and present, and make an opening statement.',
                expected_output=dedent(f'''
                The judge announces the beginning of the court session and introduces the case to be heard. 
                Example output:
                The court is now in session. We are here to hear the case of [Case Name].
                
                Output constraints:
                {add_prompt_contraints()}
                '''),
                agent=self.agent,
                callback=self.callback
            ),
            Task(
                description='Call the prosecutor to present their opening statement and initial arguments.',
                expected_output=dedent(f'''
                The judge calls the prosecutor to the stand to present their opening statement.
                Example output:
                The court will now hear the opening statement from the prosecution.
                
                Output constraints:
                {add_prompt_contraints()}
                '''),
                agent=self.agent,
                callback=self.callback
            ),
            Task(
                description='Call the defense attorney to present their opening statement and initial arguments.',
                expected_output=dedent(f'''
                The judge calls the defense attorney to the stand to present their opening statement.
                Example output: 
                The court will now hear the opening statement from the defense. 
                
                Output constraints:
                {add_prompt_contraints()}
                '''),
                agent=self.agent,
                callback=self.callback
            ),
            Task(
                description='Call a witness to the stand to provide their testimony regarding the case.',
                expected_output=dedent(f'''
                The judge calls the witness to the stand to provide their testimony.
                Example output: 
                The court calls [Witness Name] to the stand.
                
                Output constraints:
                {add_prompt_contraints()}
                '''),
                agent=self.agent,
                callback=self.callback
            ),
            Task(
                description='Deliver the final verdict based on the evidence and arguments presented, providing a brief explanation.',
                expected_output=dedent(f'''
                The judge delivers the final verdict, stating whether the defendant is guilty or not guilty, with a brief explanation of the decision.
                Example output: 
                The court finds the defendant [guilty/not guilty]. This decision is based on [brief explanation].
                
                Output constraints:
                {add_prompt_contraints(5)}
                '''),
                agent=self.agent,
                callback=self.callback
            )
        ]


class WitnessTask(BaseTask):
    def __init__(self, agent: Agent, callback: agent_callback) -> None:
        self.agent = agent
        self.callback = callback

    def create(self) -> List[Task]:
        return [
            Task(
                description='Provide testimony based on personal knowledge and experience related to the case. Answer questions posed by both the prosecution and the defense.',
                expected_output=dedent(f'''
                The witness gives a detailed account of what they saw or know about the case, answering all questions from the prosecution and the defense clearly and truthfully.
                Example output: 
                I saw [event] on [date]. In my opinion, [brief personal insight].
                
                Output constraints:
                {add_prompt_contraints(sentences=6)}
                '''),
                agent=self.agent,
                callback=self.callback
            )
        ]


class ProsecutionTask(BaseTask):
    def __init__(self, agent: Agent, callback: agent_callback) -> None:
        self.agent = agent
        self.callback = callback

    def create(self) -> List[Task]:
        return [
            Task(
                description='Present the case against the defendant, including opening statements, presenting evidence, and questioning witnesses to prove the defendant’s guilt beyond a reasonable doubt.',
                expected_output=dedent(f'''
                The prosecution delivers a compelling opening statement, presents strong evidence, effectively questions the witness to support the case, and delivers a persuasive closing argument.
                Example output: 
                The prosecution will show that the defendant is guilty through the following evidence: [brief description of evidence]. We will prove beyond a reasonable doubt that the defendant committed the crime.
                
                Output constraints:
                {add_prompt_contraints(5)}
                '''),
                agent=self.agent,
                callback=self.callback
            )
        ]


class DefenseTask(BaseTask):
    def __init__(self, agent: Agent, callback: agent_callback) -> None:
        self.agent = agent
        self.callback = callback

    def create(self) -> List[Task]:
        return [
            Task(
                description='Defend the accused by presenting evidence and arguments that create reasonable doubt about the defendant’s guilt. Question witnesses to challenge the prosecution’s case.',
                expected_output=dedent(f'''
                The defense delivers a strong opening statement, presents exculpatory evidence, effectively cross-examines the witness to create doubt, and delivers a convincing closing argument.
                Example output: 
                The defense will demonstrate that there is reasonable doubt about the defendant's guilt through the following evidence: [brief description of evidence]. We will show that the prosecution's case does not hold up under scrutiny.
                
                Output constraints:
                {add_prompt_contraints(5)}
                '''),
                agent=self.agent,
                callback=self.callback
            )
        ]


class JuryTask(BaseTask):
    def __init__(self, agent: Agent, callback: agent_callback) -> None:
        self.agent = agent
        self.callback = callback

    def create(self) -> List[Task]:
        return [
            Task(
                description='Deliberate on the evidence presented by both the prosecution and the defense, discuss with fellow jurors, and deliver a fair and impartial verdict.',
                expected_output=dedent(f'''
                The jury listens carefully to all evidence and arguments, engages in thorough deliberation with fellow jurors, and finally delivers a unanimous or majority verdict based on their discussions.
                Example output: 
                After thorough deliberation, the jury finds the defendant [guilty/not guilty] based on the presented evidence and discussions.
                
                Output constraints:
                {add_prompt_contraints(3)}
                '''),
                agent=self.agent,
                callback=self.callback
            )
        ]


class TasksFactory:
    def get_judge_tasks(self, agent: Agent, callback: agent_callback) -> List[Task]:
        task = JudgeTask(
            agent,
            callback
        )

        return task.create()

    def get_jury_tasks(self, agent: Agent, callback: agent_callback) -> List[Task]:
        task = JuryTask(
            agent,
            callback
        )

        return task.create()

    def get_witness_task(self, agent: Agent, callback: agent_callback) -> List[Task]:
        task = WitnessTask(
            agent,
            callback
        )

        return task.create()

    def get_prosecution_task(self, agent: Agent, callback: agent_callback) -> List[Task]:
        task = ProsecutionTask(
            agent,
            callback
        )

        return task.create()

    def get_defense_task(self, agent: Agent, callback: agent_callback) -> List[Task]:
        task = DefenseTask(
            agent,
            callback
        )

        return task.create()
