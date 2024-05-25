from langchain_community.tools import DuckDuckGoSearchRun


class ToolsFactory:
    @staticmethod
    def get_duckduck_go_tool() -> DuckDuckGoSearchRun:
        return DuckDuckGoSearchRun()

    @staticmethod
    def get_browserless_tool() -> None:
        pass
