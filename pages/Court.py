from functools import partial
from typing import List, Tuple, Dict

import streamlit as st
from langchain_core.agents import AgentFinish
from streamlit_extras.grid import grid as grid_layout
from streamlit_extras.row import row

from crew.Agents import AgentsManager
from crew.Crew import CourtCrew
from crew.Tasks import TasksManager
from crew.Tools import ToolsManager
from enums.CourtCaseType import CourtCaseType
from state.AppState import AppState

st.set_page_config(
    page_title='Court',
    page_icon=':classical_building:',
    layout='wide',
    initial_sidebar_state='auto'
)

global_counter = 0


def chat_view(container_name: str, container, agent_output: str | List[Tuple[Dict, str]] | AgentFinish) -> None:
    global global_counter
    with open('chat_view.txt', mode='a') as log_file:
        print(f'{container_name} | {agent_output}', file=log_file)

    key_string = f'{container_name}_chat_message'

    if AppState.get_value(key_string) is None:
        AppState.set_value(key_string, [])
        return

    if isinstance(agent_output, AgentFinish):
        AppState.set_value(key_string, AppState.get_value(key_string) + [
            {'role': container_name, 'content': agent_output.return_values['output']}])

    for message in AppState.get_value(key_string):
        with container.chat_message(str(global_counter)):
            st.write(message['content'])
            global_counter += 1


class Court:
    def __init__(self):
        self.view()

    def empty_row(self, grid: grid_layout = None) -> None:
        if grid is None:
            with row(1).container():
                st.write('‎')
                return

        with grid.container():
            st.write('‎')

    @st.experimental_dialog('Warning!')
    def invalid_settings_modal(self) -> None:
        st.write('You must visit the **Settings** tab to fill in the information needed to run the simulation')
        if st.button('Redirect to settings'):
            st.switch_page('pages/Settings.py')

    @st.experimental_dialog('Case description', width='large')
    def case_description_modal(self) -> None:
        user_case_description = st.text_area('Description:', max_chars=10000, height=200,
                                             placeholder='Explain what the case is about. Include all important information, as it may affect the final judgment.')
        if st.button("Submit"):
            AppState.set_value('user_case_description', user_case_description)
            st.rerun()

    # def chat_view(self, container_name: str) -> None:
    #     key_string = f'{container_name}_chat_message'
    #     if AppState.get_value(key_string) is None:
    #         AppState.set_value(key_string, [])
    #
    #     for message in AppState.get_value(key_string):
    #         with st.chat_message(message['role']):
    #             st.markdown(message['content'])

    def view(self) -> None:
        if AppState.get_value('ready_to_start_simulation') is None:
            self.invalid_settings_modal()

        if (AppState.get_value('user_case_description') is None and
                AppState.get_value('ready_to_start_simulation') is not None):
            self.case_description_modal()

        st.title("Court :speech_balloon:")
        self.empty_row()

        if AppState.get_value('court_type') == CourtCaseType.CIVIL:
            grid = grid_layout(2, 2)

            judge_container = grid.container(border=True)
            with judge_container:
                st.subheader('Judge :judge:')
                chat_view('judge', judge_container, '')

            witness_container = grid.container(border=True)
            with witness_container:
                st.subheader('Witness :adult:')
                chat_view('witness', witness_container, '')

            prosecution_container = grid.container(border=True)
            with prosecution_container:
                st.subheader('Prosecution :crossed_swords:')
                chat_view('prosecution', prosecution_container, '')

            defense_container = grid.container(border=True)
            with defense_container:
                st.subheader('Defense :shield:')
                chat_view('defense', defense_container, '')
        else:
            grid = grid_layout(2, 2, [2, 2])

            judge_container = grid.container(border=True)
            with judge_container:
                st.subheader('Judge :judge:')
                chat_view('judge', judge_container, '')

            jury_container = grid.container(border=True)
            with jury_container:
                st.subheader('Jury :memo:')
                chat_view('jury', jury_container, '')

            witness_container = grid.container(border=True)
            with witness_container:
                st.subheader('Witness :adult:')
                chat_view('witness', witness_container, '')

            prosecution_container = grid.container(border=True)
            with prosecution_container:
                st.subheader('Prosecution :crossed_swords:')
                chat_view('prosecution', prosecution_container, '')

            defense_container = grid.container(border=True)
            with defense_container:
                st.subheader('Defense :shield:')
                chat_view('defense', defense_container, '')

        start = st.button('Start simulation')
        if start:
            agents_manager = AgentsManager()
            tasks_manager = TasksManager()
            tools_manager = ToolsManager()

            judge_agent = agents_manager.get_judge_agent(partial(chat_view, 'judge', judge_container))
            # judge_agent.tools = [
            #     tools_manager.get_duckduck_go_tool()
            # ]
            # witness_agent = agents_manager.get_witness_agent(partial(self.chat_view, 'witness'))
            # prosecution_agent = agents_manager.get_prosecution_agent(partial(self.chat_view, 'prosecution'))
            # prosecution_agent.tools = [
            #     tools_manager.get_duckduck_go_tool()
            # ]
            # defense_agent = agents_manager.get_defense_agent(partial(self.chat_view, 'defense'))
            # defense_agent.tools = [
            #     tools_manager.get_duckduck_go_tool()
            # ]

            judge_tasks = tasks_manager.get_judge_tasks(judge_agent)
            # witness_tasks = tasks_manager.get_witness_task(witness_agent)
            # prosecution_tasks = tasks_manager.get_prosecution_task(prosecution_agent)
            # defense_tasks = tasks_manager.get_defense_task(defense_agent)

            # if AppState.get_value('court_type') == CourtCaseType.CRIMINAL:
            #     jury_agent = agents_manager.get_jury_agent(partial(self.chat_view, 'jury'))
            #     jury_tasks = tasks_manager.get_jury_tasks(jury_agent)
            #     agents = [judge_agent, jury_agent, witness_agent, prosecution_agent, defense_agent]
            #     tasks = [judge_tasks, jury_tasks, witness_tasks, prosecution_tasks, defense_tasks]
            # else:
            #     agents = [judge_agent, witness_agent, prosecution_agent, defense_agent]
            #     tasks = [judge_tasks, witness_tasks, prosecution_tasks, defense_tasks]

            # court_crew = CourtCrew().get_crew(agents=agents, tasks=tasks)
            court_crew = CourtCrew().get_crew(agents=[judge_agent], tasks=judge_tasks)
            court_crew.kickoff()


court = Court()
