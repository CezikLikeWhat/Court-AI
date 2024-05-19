from functools import partial

import streamlit as st
from streamlit_extras.grid import grid as grid_layout
from streamlit_extras.row import row

from crew.Agents import AgentsManager
from crew.Crew import CourtCrew
from crew.Tasks import TasksManager
from enums.CourtCaseType import CourtCaseType
from state.AppState import AppState

st.set_page_config(
    page_title='Court',
    page_icon=':classical_building:',
    layout='wide',
    initial_sidebar_state='auto'
)


class Court:
    def __init__(self):
        self.view()

    def empty_row(self, grid: grid_layout = None) -> None:
        if grid is None:
            with row(1).container():
                st.write('‎')  # Invisible character
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
        user_case_description = st.text_area('Description:', max_chars=500, height=200,
                                             placeholder='Explain what the case is about. Include all important information, as it may affect the final judgment.')
        if st.button("Submit"):
            AppState.set_value('user_case_description', user_case_description)
            st.rerun()

    def chat_view(self, container_name: str) -> None:
        key_string = f'{container_name}_chat_message'
        if AppState.get_value(key_string) is None:
            AppState.set_value(key_string, [])

        for message in AppState.get_value(key_string):
            with st.chat_message(message['role']):
                st.markdown(message['content'])

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

            with grid.container(border=True):
                st.subheader('Judge :judge:')
                self.chat_view('judge')

            with grid.container(border=True):
                st.subheader('Witness :adult:')
                self.chat_view('witness')

            with grid.container(border=True):
                st.subheader('Prosecution :crossed_swords:')
                self.chat_view('prosecution')

            with grid.container(border=True):
                st.subheader('Defense :shield:')
                self.chat_view('defense')
        else:
            grid = grid_layout(2, 2, [2, 2])

            with grid.container(border=True):
                st.subheader('Judge :judge:')
                self.chat_view('judge')

            with grid.container(border=True):
                st.subheader('Jury :memo:')
                self.chat_view('jury')

            with grid.container(border=True):
                st.subheader('Witness :adult:')
                self.chat_view('witness')

            with grid.container(border=True):
                st.subheader('Prosecution :crossed_swords:')
                self.chat_view('prosecution')

            with grid.container(border=True):
                st.subheader('Defense :shield:')
                self.chat_view('defense')

        start = st.button('Start simulation')
        if start:
            agents_manager = AgentsManager()
            tasks_manager = TasksManager()

            judge_agent = agents_manager.get_judge_agent(partial(self.chat_view, 'judge'))
            witness_agent = agents_manager.get_witness_agent(partial(self.chat_view, 'witness'))
            prosecution_agent = agents_manager.get_prosecution_agent(partial(self.chat_view, 'prosecution'))
            defense_agent = agents_manager.get_defense_agent(partial(self.chat_view, 'defense'))

            judge_tasks = tasks_manager.get_judge_tasks(judge_agent)
            witness_tasks = tasks_manager.get_witness_task(witness_agent)
            prosecution_tasks = tasks_manager.get_prosecution_task(prosecution_agent)
            defense_tasks = tasks_manager.get_defense_task(defense_agent)

            if AppState.get_value('court_type') == CourtCaseType.CRIMINAL:
                jury_agent = agents_manager.get_jury_agent(partial(self.chat_view, 'jury'))
                jury_tasks = tasks_manager.get_jury_tasks(jury_agent)
                agents = [judge_agent, jury_agent, witness_agent, prosecution_agent, defense_agent]
                tasks = [judge_tasks, jury_tasks, witness_tasks, prosecution_tasks, defense_tasks]
            else:
                agents = [judge_agent, witness_agent, prosecution_agent, defense_agent]
                tasks = [judge_tasks, witness_tasks, prosecution_tasks, defense_tasks]

            # tools = Tools().all()
            court_crew = CourtCrew(agents=agents, tasks=tasks).get_crew()
            court_crew.crew.kickoff()


court = Court()
