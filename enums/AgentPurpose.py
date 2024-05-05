from enum import Enum


class AgentPurpose(str, Enum):
    CREW_SUPERVISOR = 'Crew Supervisor'
    JUDGE = 'Judge'
    WITNESS = 'Witness'
    DEFENSE = 'Defense'
    PROSECUTOR = 'Prosecutor'
    JURY = 'Jury'
