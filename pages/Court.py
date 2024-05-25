import streamlit as st
from crewai.tasks.task_output import TaskOutput
from streamlit_extras.grid import grid as grid_layout
from streamlit_extras.row import row

from crew.Agents import AgentsFactory
from crew.Crew import CourtCrew
from crew.Tasks import TasksFactory
from crew.Tools import ToolsFactory
from enums.CourtCaseType import CourtCaseType
from state.AppState import AppState

st.set_page_config(
    page_title='Court',
    page_icon=':classical_building:',
    layout='wide',
    initial_sidebar_state='auto'
)


def chat_view(container_name: str, container, agent_output: TaskOutput | None) -> None:
    key_string = f'{AppState.get_value('task_order_counter')}{container_name}_chat_message'

    if AppState.get_value(key_string) is None:
        AppState.set_value(key_string, [])
        return

    if isinstance(agent_output, TaskOutput):
        AppState.set_value(key_string, AppState.get_value(key_string) + [
            {'role': container_name, 'content': agent_output.result()}])

    message = AppState.get_value(key_string)
    if message is not None and message != []:
        with container.chat_message(key_string):
            st.write(message[-1]['content'])  # Display only newest message

        AppState.set_value('task_order_counter', AppState.get_value('task_order_counter') + 1)


def chat_view_wrapper(container_name, container):
    def wrapper(agent_output):
        chat_view(container_name, container, agent_output)

    return wrapper


class Court:
    judge_container: st.container
    witness_container: st.container
    prosecution_container: st.container
    defense_container: st.container
    jury_container: st.container

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
        case_description = st.text_area('Description:', max_chars=5000, height=200,
                                        placeholder='Explain what the case is about. Include all important information, as it may affect the final judgment.')
        if st.button("Submit"):
            AppState.set_value('case_description', case_description)
            st.rerun()

    def judge_view(self, grid: grid_layout):
        self.judge_container = grid.container(border=True, height=500)
        with self.judge_container:
            st.subheader('Judge :judge:')
            chat_view('judge', self.judge_container, None)

    def witness_view(self, grid: grid_layout):
        self.witness_container = grid.container(border=True, height=500)
        with self.witness_container:
            st.subheader('Witness :adult:')
            chat_view('witness', self.witness_container, None)

    def prosecution_view(self, grid: grid_layout):
        self.prosecution_container = grid.container(border=True, height=500)
        with self.prosecution_container:
            st.subheader('Prosecution :crossed_swords:')
            chat_view('prosecution', self.prosecution_container, None)

    def defense_view(self, grid: grid_layout):
        self.defense_container = grid.container(border=True, height=500)
        with self.defense_container:
            st.subheader('Defense :shield:')
            chat_view('defense', self.defense_container, None)

    def jury_view(self, grid: grid_layout):
        self.jury_container = grid.container(border=True, height=500)
        with self.jury_container:
            st.subheader('Jury :memo:')
            chat_view('jury', self.jury_container, None)

    def clear_simulation(self):
        for container_name in ['judge', 'witness', 'prosecution', 'defense', 'jury']:
            AppState.clear(f'{container_name}_chat_message')
        AppState.clear('case_description')
        AppState.clear('disable_start_simulation_button')
        AppState.clear('task_order_counter')

    def start_simulation(self):
        AppState.set_value('disable_start_simulation_button', True)
        AppState.set_value('task_order_counter', 0)
        agents_factory = AgentsFactory()
        tasks_factory = TasksFactory()
        tools_factory = ToolsFactory()

        judge_agent = agents_factory.judge_agent()
        # judge_agent.tools = [
        #     tools_manager.get_duckduck_go_tool()
        # ]
        witness_agent = agents_factory.witness_agent()
        prosecution_agent = agents_factory.prosecution_agent()
        # prosecution_agent.tools = [
        #     tools_manager.get_duckduck_go_tool()
        # ]
        defense_agent = agents_factory.defense_agent()
        # defense_agent.tools = [
        #     tools_manager.get_duckduck_go_tool()
        # ]

        judge_tasks = tasks_factory.get_judge_tasks(
            judge_agent,
            chat_view_wrapper('judge', self.judge_container)
        )
        witness_tasks = tasks_factory.get_witness_task(
            witness_agent,
            chat_view_wrapper('witness', self.witness_container)
        )
        prosecution_tasks = tasks_factory.get_prosecution_task(
            prosecution_agent,
            chat_view_wrapper('prosecution', self.prosecution_container)
        )
        defense_tasks = tasks_factory.get_defense_task(
            defense_agent,
            chat_view_wrapper('defense', self.defense_container)
        )

        if AppState.get_value('court_type') == CourtCaseType.CRIMINAL:
            jury_agent = agents_factory.jury_agent()
            jury_tasks = tasks_factory.get_jury_tasks(jury_agent, chat_view_wrapper('jury', self.jury_container))
            agents = [judge_agent, jury_agent, witness_agent, prosecution_agent, defense_agent]
            tasks = [*judge_tasks, *jury_tasks, *witness_tasks, *prosecution_tasks, *defense_tasks]
        else:
            agents = [judge_agent, witness_agent, prosecution_agent, defense_agent]
            tasks = [*judge_tasks, *witness_tasks, *prosecution_tasks, *defense_tasks]

        court_crew = CourtCrew().get_crew(agents=agents, tasks=tasks)
        court_crew.kickoff()

    def view(self) -> None:
        if AppState.get_value('ready_to_start_simulation') is None:
            self.invalid_settings_modal()

        if (AppState.get_value('case_description') is None and
                AppState.get_value('ready_to_start_simulation') is not None):
            self.case_description_modal()

        with st.sidebar:
            st.button('Start simulation', on_click=self.start_simulation,
                      disabled=True if AppState.get_value('disable_start_simulation_button') else False)
            st.button('Clear case', on_click=self.clear_simulation)

        st.title("Court :speech_balloon:")
        self.empty_row()

        if AppState.get_value('court_type') == CourtCaseType.CIVIL:
            grid = grid_layout(2, 2)

            self.judge_view(grid)
            self.witness_view(grid)
            self.prosecution_view(grid)
            self.defense_view(grid)
        else:
            grid = grid_layout(2, 2, [2, 2])

            self.judge_view(grid)
            self.jury_view(grid)
            self.witness_view(grid)
            self.prosecution_view(grid)
            self.defense_view(grid)


court = Court()
