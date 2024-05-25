from typing import Any, Dict

import streamlit as st

from state.SingletonMeta import SingletonMeta


class AppState(metaclass=SingletonMeta):
    @staticmethod
    def get_value(key: str) -> Any | None:
        return st.session_state[key] if key in st.session_state else None

    @staticmethod
    def set_value(key: str, value: Any) -> None:
        st.session_state[key] = value

    @staticmethod
    def set_multiple_values(values: Dict[str, Any]) -> None:
        for key, value in values.items():
            AppState.set_value(key, value)

    @staticmethod
    def clear(key: str) -> None:
        st.session_state[key] = None
