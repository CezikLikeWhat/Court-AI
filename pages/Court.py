import streamlit as st
from streamlit_extras.grid import grid as grid_layout
from streamlit_extras.row import row

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

    def empty_tile(self, grid: grid_layout) -> None:
        with grid.container(border=True):
            pass

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

    def view(self) -> None:
        if AppState.get_value('ready_to_start_simulation') is None:
            self.invalid_settings_modal()

        st.title("Court :speech_balloon:")
        self.empty_row()

        if AppState.get_value('court_type') == CourtCaseType.CIVIL:
            grid = grid_layout(3, 1, [3, 1], 1, [1, 2, 2, 1])

            self.empty_tile(grid)
            with grid.container(border=True):
                st.write('Judge')
            self.empty_tile(grid)

            self.empty_row(grid)

            self.empty_tile(grid)
            with grid.container(border=True):
                st.write('Witness')

            self.empty_row(grid)

            self.empty_tile(grid)
            with grid.container(border=True):
                st.write('Prosecution')
            with grid.container(border=True):
                st.write('Defense')
            self.empty_tile(grid)
            self.empty_tile(grid)

        else:
            grid = grid_layout(3, 1, [3, 3, 3], 1, [1, 2, 2, 1])

            self.empty_tile(grid)
            with grid.container(border=True):
                st.write('Judge')
            self.empty_tile(grid)

            self.empty_row(grid)
            with grid.container(border=True):
                st.write('Jury')
            self.empty_tile(grid)

            with grid.container(border=True):
                st.write('Witness')

            self.empty_row(grid)

            self.empty_tile(grid)
            with grid.container(border=True):
                st.write('Prosecution')
            with grid.container(border=True):
                st.write('Defense')
            self.empty_tile(grid)
            self.empty_tile(grid)

        # if "messages" not in st.session_state:
        #     st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
        #
        # for msg in st.session_state.messages:
        #     st.chat_message(msg["role"]).write(msg["content"])

        # if prompt := st.chat_input():
        #     if not openai_api_key:
        #         st.info("Please add your OpenAI API key to continue.")
        #         st.stop()


court = Court()
