import streamlit as st
from streamlit_extras.grid import grid as grid_layout

from enums.AiModel import AiModel
from enums.AiProvider import AiProvider
from enums.CourtCaseType import CourtCaseType
from state.AppState import AppState
from validators.ApiKeyValidator import ApiKeyValidator
from validators.SettingsFormValidator import SettingsFormValidator

st.set_page_config(
    page_title='Settings',
    page_icon=':gear:',
    layout='wide',
    initial_sidebar_state='auto'
)


class Settings:
    openai_api_key_value = None
    anthropic_api_key_value = None
    supervisor_provider = None
    judge_provider = None
    witness_provider = None
    defense_provider = None
    prosecutor_provider = None
    jury_provider = None
    amount_of_juries = None
    supervisor_model = None
    judge_model = None
    witness_model = None
    defense_model = None
    prosecutor_model = None
    jury_model = None
    type_of_court_case = None

    def __init__(self) -> None:
        self.view()

    def validate_form(self) -> bool:
        form_validator = SettingsFormValidator(
            self.openai_api_key_value,
            self.anthropic_api_key_value,
            self.supervisor_provider,
            self.judge_provider,
            self.witness_provider,
            self.defense_provider,
            self.jury_provider
        )
        message = form_validator.validate_all()
        if message is not None:
            st.error(message)
            return False

        if self.openai_api_key_value != '':
            message = ApiKeyValidator.is_valid_open_ai_key(self.openai_api_key_value)
            if message is not None:
                st.error(message)
                return False

        if self.anthropic_api_key_value != '':
            message = ApiKeyValidator.is_valid_anthropic_key(self.anthropic_api_key_value)
            if message is not None:
                st.error(message)
                return False

        return True

    def supervisor_view(self):
        st.subheader('Supervisor :brain:')
        self.supervisor_provider = st.selectbox('Supervisor provider',
                                                AiProvider.get_all(),
                                                AiProvider.index_of(
                                                    st.session_state.supervisor_provider) if 'supervisor_provider' in st.session_state else 0
                                                )
        self.supervisor_model = st.selectbox('Supervisor model',
                                             AiModel.get_all_by_provider(self.supervisor_provider),
                                             AiModel.index_of(
                                                 st.session_state.supervisor_model,
                                                 self.supervisor_provider) if 'supervisor_model' in st.session_state else 0
                                             )

    def judge_view(self):
        st.subheader('Judge :judge:')
        self.judge_provider = st.selectbox('Judge provider',
                                           AiProvider.get_all(),
                                           AiProvider.index_of(
                                               st.session_state.judge_provider) if 'judge_provider' in st.session_state else 0
                                           )
        self.judge_model = st.selectbox('Judge model',
                                        AiModel.get_all_by_provider(self.judge_provider),
                                        AiModel.index_of(
                                            st.session_state.judge_model,
                                            self.judge_provider) if 'judge_model' in st.session_state else 0
                                        )

    def witness_view(self):
        st.subheader('Witness :adult:')
        self.witness_provider = st.selectbox('Witness provider',
                                             AiProvider.get_all(),
                                             AiProvider.index_of(
                                                 st.session_state.witness_provider) if 'witness_provider' in st.session_state else 0
                                             )
        self.witness_model = st.selectbox('Witness model',
                                          AiModel.get_all_by_provider(self.witness_provider),
                                          AiModel.index_of(
                                              st.session_state.witness_model,
                                              self.witness_provider) if 'witness_model' in st.session_state else 0
                                          )

    def defense_view(self):
        st.subheader('Defense :shield:')
        self.defense_provider = st.selectbox('Defense provider',
                                             AiProvider.get_all(),
                                             AiProvider.index_of(
                                                 st.session_state.defense_provider) if 'defense_provider' in st.session_state else 0
                                             )
        self.defense_model = st.selectbox('Defense model',
                                          AiModel.get_all_by_provider(self.defense_provider),
                                          AiModel.index_of(
                                              st.session_state.defense_model,
                                              self.defense_provider) if 'defense_model' in st.session_state else 0
                                          )

    def prosecutor_view(self):
        st.subheader('Prosecutor :crossed_swords:')
        self.prosecutor_provider = st.selectbox('Prosecutor provider',
                                                AiProvider.get_all(),
                                                AiProvider.index_of(
                                                    st.session_state.prosecutor_provider) if 'prosecutor_provider' in st.session_state else 0
                                                )
        self.prosecutor_model = st.selectbox('Prosecutor model',
                                             AiModel.get_all_by_provider(self.prosecutor_provider),
                                             AiModel.index_of(
                                                 st.session_state.prosecutor_model,
                                                 self.prosecutor_provider) if 'prosecutor_model' in st.session_state else 0
                                             )

    def jury_view(self):
        st.subheader('Jury :memo:')
        self.jury_provider = st.selectbox('Jury provider',
                                          AiProvider.get_all(),
                                          AiProvider.index_of(
                                              st.session_state.jury_provider) if 'jury_provider' in st.session_state else 0
                                          )
        self.jury_model = st.selectbox('Jury model',
                                       AiModel.get_all_by_provider(self.jury_provider),
                                       AiModel.index_of(
                                           st.session_state.jury_model,
                                           self.jury_provider) if 'jury_model' in st.session_state else 0
                                       )
        self.amount_of_juries = st.slider('Amount of juries', min_value=1, max_value=10, step=1,
                                          format='%d',
                                          value=st.session_state.juries_amount if 'juries_amount' in st.session_state else 1)

    def submit_form(self):
        st.success('Saved')
        AppState.set_value('ready_to_start_simulation', True)
        AppState.set_value('openai_key', self.openai_api_key_value)
        AppState.set_value('anthropic_key', self.anthropic_api_key_value)
        AppState.set_value('court_type', CourtCaseType.get_by_name(self.type_of_court_case))
        AppState.set_value('supervisor_provider', self.supervisor_provider)
        AppState.set_value('judge_provider', self.judge_provider)
        AppState.set_value('witness_provider', self.witness_provider)
        AppState.set_value('defense_provider', self.defense_provider)
        AppState.set_value('prosecutor_provider', self.prosecutor_provider)
        AppState.set_value('supervisor_model', self.supervisor_model)
        AppState.set_value('judge_model', self.judge_model)
        AppState.set_value('witness_model', self.witness_model)
        AppState.set_value('defense_model', self.defense_model)
        AppState.set_value('prosecutor_model', self.prosecutor_model)

        if self.amount_of_juries is not None:
            AppState.set_value('jury_provider', self.jury_provider)
            AppState.set_value('jury_model', self.jury_model)
            AppState.set_value('juries_amount', self.amount_of_juries)

    def view(self) -> None:
        main_container = st.container(border=True)

        # AI Section
        main_container.title('AI :dna:')

        with main_container.container():
            st.subheader('OpenAI')
            self.openai_api_key_value = st.text_input(f'OpenAI API Key',
                                                      type='password',
                                                      value=st.session_state.openai_key if 'openai_key' in st.session_state else ''
                                                      )

        with main_container.container():
            st.subheader('Anthropic')
            self.anthropic_api_key_value = st.text_input(f'Anthropic API Key',
                                                         type='password',
                                                         value=st.session_state.anthropic_key if 'anthropic_key' in st.session_state else ''
                                                         )

        # Simulation
        main_container.title('Simulation :magic_wand:')
        self.type_of_court_case = main_container.selectbox('Type of court case',
                                                           CourtCaseType.get_all(),
                                                           CourtCaseType.index_of(
                                                               st.session_state.court_type) if 'court_type' in st.session_state else 0
                                                           )

        if CourtCaseType.get_by_name(self.type_of_court_case) == CourtCaseType.CIVIL:
            with main_container.container():
                grid = grid_layout(2, 2, [1, 1])

                with grid.container(border=True):
                    self.supervisor_view()
                with grid.container(border=True):
                    self.judge_view()
                with grid.container(border=True):
                    self.witness_view()
                with grid.container(border=True):
                    self.defense_view()
                with grid.container(border=True):
                    self.prosecutor_view()

        else:
            with main_container.container():
                grid = grid_layout(2, 2, 2)

                with grid.container(border=True):
                    self.supervisor_view()
                with grid.container(border=True):
                    self.judge_view()
                with grid.container(border=True):
                    self.witness_view()
                with grid.container(border=True):
                    self.defense_view()
                with grid.container(border=True):
                    self.prosecutor_view()

                with grid.container(border=True):
                    self.jury_view()

        # Form Submit
        with main_container.columns([3, 3, 1])[2]:
            submitted = st.button('Submit')

        if submitted:
            if self.validate_form():
                self.submit_form()


settings = Settings()
