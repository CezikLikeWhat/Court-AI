import streamlit as st

from enums.AiModel import AiModel
from enums.AiProvider import AiProvider
from enums.CourtCaseType import CourtCaseType
from state.SingletonMeta import SingletonMeta


class AppState(metaclass=SingletonMeta):

    @staticmethod
    def get_open_ai_key() -> str:
        return st.session_state.open_ai_key

    @staticmethod
    def save_open_ai_key(key_value: str) -> None:
        st.session_state.open_ai_key = key_value

    @staticmethod
    def get_anthropic_key() -> str:
        return st.session_state.anthropic_key

    @staticmethod
    def save_anthropic_key(key_value: str) -> None:
        st.session_state.anthropic_key = key_value

    @staticmethod
    def get_court_type() -> CourtCaseType:
        return st.session_state.court_type

    @staticmethod
    def save_court_type(court_type: CourtCaseType) -> None:
        st.session_state.court_type = court_type

    @staticmethod
    def get_supervisor_provider() -> AiProvider:
        return st.session_state.supervisor_provider

    @staticmethod
    def save_supervisor_provider(supervisor_provider: AiProvider) -> None:
        st.session_state.supervisor_provider = supervisor_provider

    @staticmethod
    def get_judge_provider() -> AiProvider:
        return st.session_state.judge_provider

    @staticmethod
    def save_judge_provider(judge_provider: AiProvider) -> None:
        st.session_state.judge_provider = judge_provider

    @staticmethod
    def get_witness_provider() -> AiProvider:
        return st.session_state.witness_provider

    @staticmethod
    def save_witness_provider(witness_provider: AiProvider) -> None:
        st.session_state.witness_provider = witness_provider

    @staticmethod
    def get_defense_provider() -> AiProvider:
        return st.session_state.defense_provider

    @staticmethod
    def save_defense_provider(defense_provider: AiProvider) -> None:
        st.session_state.defense_provider = defense_provider

    @staticmethod
    def get_prosecutor_provider() -> AiProvider:
        return st.session_state.prosecutor_provider

    @staticmethod
    def save_prosecutor_provider(prosecutor_provider: AiProvider) -> None:
        st.session_state.prosecutor_provider = prosecutor_provider

    @staticmethod
    def get_jury_provider() -> AiProvider:
        return st.session_state.jury_provider

    @staticmethod
    def save_jury_provider(jury_provider: AiProvider) -> None:
        st.session_state.jury_provider = jury_provider

    @staticmethod
    def get_supervisor_model() -> AiProvider:
        return st.session_state.supervisor_model

    @staticmethod
    def save_supervisor_model(supervisor_model: AiModel) -> None:
        st.session_state.supervisor_model = supervisor_model

    @staticmethod
    def get_judge_model() -> AiProvider:
        return st.session_state.judge_model

    @staticmethod
    def save_judge_model(judge_model: AiModel) -> None:
        st.session_state.judge_model = judge_model

    @staticmethod
    def get_witness_model() -> AiProvider:
        return st.session_state.witness_model

    @staticmethod
    def save_witness_model(witness_model: AiModel) -> None:
        st.session_state.witness_model = witness_model

    @staticmethod
    def get_defense_model() -> AiProvider:
        return st.session_state.defense_model

    @staticmethod
    def save_defense_model(defense_model: AiModel) -> None:
        st.session_state.defense_model = defense_model

    @staticmethod
    def get_prosecutor_model() -> AiProvider:
        return st.session_state.prosecutor_model

    @staticmethod
    def save_prosecutor_model(prosecutor_model: AiModel) -> None:
        st.session_state.prosecutor_model = prosecutor_model

    @staticmethod
    def get_jury_model() -> AiProvider:
        return st.session_state.jury_model

    @staticmethod
    def save_jury_model(jury_model: AiModel) -> None:
        st.session_state.jury_model = jury_model

    @staticmethod
    def get_juries_amount() -> int:
        return st.session_state.juries_amount

    @staticmethod
    def save_juries_amount(juries_amount: int) -> None:
        st.session_state.juries_amount = juries_amount
