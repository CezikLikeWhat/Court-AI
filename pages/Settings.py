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
    openai_api_key_value: str = None
    anthropic_api_key_value: str = None
    supervisor_provider: AiProvider = None
    supervisor_model: AiModel = None
    supervisor_temperature: float = None
    judge_provider: AiProvider = None
    judge_model: AiModel = None
    judge_temperature: float = None
    witness_provider: AiProvider = None
    witness_model: AiModel = None
    witness_temperature: float = None
    defense_provider: AiProvider = None
    defense_model: AiModel = None
    defense_temperature: float = None
    prosecutor_provider: AiProvider = None
    prosecutor_model: AiModel = None
    prosecutor_temperature: float = None
    jury_provider: AiProvider = None
    jury_model: AiModel = None
    jury_temperature: float = None
    amount_of_juries: int = None
    type_of_court_case: CourtCaseType = None

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
        self.supervisor_provider = st.selectbox('Provider',
                                                options=AiProvider.get_all(),
                                                index=AiProvider.index_of(
                                                    st.session_state.supervisor_provider) if 'supervisor_provider' in st.session_state else 2,
                                                help='Select a LLM (Large Language Model) provider.',
                                                key=1
                                                )
        self.supervisor_model = st.selectbox('Model',
                                             options=AiModel.get_all_by_provider(self.supervisor_provider),
                                             index=AiModel.index_of(
                                                 st.session_state.supervisor_model,
                                                 self.supervisor_provider) if 'supervisor_model' in st.session_state else 0,
                                             help='Select a specific LLM (Large Language Model) model.',
                                             key=2
                                             )
        self.supervisor_temperature = st.slider('Temperature',
                                                min_value=0.0,
                                                max_value=1.0,
                                                value=0.7,
                                                step=0.1,
                                                format='%.1f',
                                                help='Controls randomness: Lowering results in less random completions. As the temperature approaches zero, the model will become deterministic and repetitive.',
                                                key=3
                                                )

    def judge_view(self):
        st.subheader('Judge :judge:')
        self.judge_provider = st.selectbox('Provider',
                                           options=AiProvider.get_all(),
                                           index=AiProvider.index_of(
                                               st.session_state.judge_provider) if 'judge_provider' in st.session_state else 2,
                                           help='Select a LLM (Large Language Model) provider.',
                                           key=4
                                           )
        self.judge_model = st.selectbox('Model',
                                        options=AiModel.get_all_by_provider(self.judge_provider),
                                        index=AiModel.index_of(
                                            st.session_state.judge_model,
                                            self.judge_provider) if 'judge_model' in st.session_state else 0,
                                        help='Select a specific LLM (Large Language Model) model.',
                                        key=5
                                        )
        self.judge_temperature = st.slider('Temperature',
                                           min_value=0.0,
                                           max_value=1.0,
                                           value=0.7,
                                           step=0.1,
                                           format='%.1f',
                                           help='Controls randomness: Lowering results in less random completions. As the temperature approaches zero, the model will become deterministic and repetitive.',
                                           key=6
                                           )

    def witness_view(self):
        st.subheader('Witness :adult:')
        self.witness_provider = st.selectbox('Provider',
                                             options=AiProvider.get_all(),
                                             index=AiProvider.index_of(
                                                 st.session_state.witness_provider) if 'witness_provider' in st.session_state else 2,
                                             help='Select a LLM (Large Language Model) provider.',
                                             key=7
                                             )
        self.witness_model = st.selectbox('Model',
                                          options=AiModel.get_all_by_provider(self.witness_provider),
                                          index=AiModel.index_of(
                                              st.session_state.witness_model,
                                              self.witness_provider) if 'witness_model' in st.session_state else 0,
                                          help='Select a specific LLM (Large Language Model) model.',
                                          key=8
                                          )
        self.witness_temperature = st.slider('Temperature',
                                             min_value=0.0,
                                             max_value=1.0,
                                             value=0.7,
                                             step=0.1,
                                             format='%.1f',
                                             help='Controls randomness: Lowering results in less random completions. As the temperature approaches zero, the model will become deterministic and repetitive.',
                                             key=9
                                             )

    def defense_view(self):
        st.subheader('Defense :shield:')
        self.defense_provider = st.selectbox('Provider',
                                             options=AiProvider.get_all(),
                                             index=AiProvider.index_of(
                                                 st.session_state.defense_provider) if 'defense_provider' in st.session_state else 2,
                                             help='Select a LLM (Large Language Model) provider.',
                                             key=10
                                             )
        self.defense_model = st.selectbox('Model',
                                          options=AiModel.get_all_by_provider(self.defense_provider),
                                          index=AiModel.index_of(
                                              st.session_state.defense_model,
                                              self.defense_provider) if 'defense_model' in st.session_state else 0,
                                          help='Select a specific LLM (Large Language Model) model.',
                                          key=11
                                          )
        self.defense_temperature = st.slider('Temperature',
                                             min_value=0.0,
                                             max_value=1.0,
                                             value=0.7,
                                             step=0.1,
                                             format='%.1f',
                                             help='Controls randomness: Lowering results in less random completions. As the temperature approaches zero, the model will become deterministic and repetitive.',
                                             key=12
                                             )

    def prosecutor_view(self):
        st.subheader('Prosecutor :crossed_swords:')
        self.prosecutor_provider = st.selectbox('Provider',
                                                options=AiProvider.get_all(),
                                                index=AiProvider.index_of(
                                                    st.session_state.prosecutor_provider) if 'prosecutor_provider' in st.session_state else 2,
                                                help='Select a LLM (Large Language Model) provider.',
                                                key=13
                                                )
        self.prosecutor_model = st.selectbox('Model',
                                             options=AiModel.get_all_by_provider(self.prosecutor_provider),
                                             index=AiModel.index_of(
                                                 st.session_state.prosecutor_model,
                                                 self.prosecutor_provider) if 'prosecutor_model' in st.session_state else 0,
                                             help='Select a specific LLM (Large Language Model) model.',
                                             key=14
                                             )
        self.prosecutor_temperature = st.slider('Temperature',
                                                min_value=0.0,
                                                max_value=1.0,
                                                value=0.7,
                                                step=0.1,
                                                format='%.1f',
                                                help='Controls randomness: Lowering results in less random completions. As the temperature approaches zero, the model will become deterministic and repetitive.',
                                                key=15
                                                )

    def jury_view(self):
        st.subheader('Jury :memo:')
        self.jury_provider = st.selectbox('Provider',
                                          options=AiProvider.get_all(),
                                          index=AiProvider.index_of(
                                              st.session_state.jury_provider) if 'jury_provider' in st.session_state else 2,
                                          help='Select a LLM (Large Language Model) provider.',
                                          key=16
                                          )
        self.jury_model = st.selectbox('Model',
                                       options=AiModel.get_all_by_provider(self.jury_provider),
                                       index=AiModel.index_of(
                                           st.session_state.jury_model,
                                           self.jury_provider) if 'jury_model' in st.session_state else 0,
                                       help='Select a specific LLM (Large Language Model) model.',
                                       key=17
                                       )
        self.jury_temperature = st.slider('Temperature',
                                          min_value=0.0,
                                          max_value=1.0,
                                          value=0.7,
                                          step=0.1,
                                          format='%.1f',
                                          help='Controls randomness: Lowering results in less random completions. As the temperature approaches zero, the model will become deterministic and repetitive.',
                                          key=18
                                          )
        self.amount_of_juries = st.slider('Amount of juries',
                                          min_value=1,
                                          max_value=10,
                                          value=st.session_state.juries_amount if 'juries_amount' in st.session_state else 1,
                                          step=1,
                                          format='%d',
                                          help='Determines the number of agents created to act as members of the jury (the greater the number, the greater the cost of the simulation may be).'
                                          )

    def submit_form(self):
        st.success('Saved')
        AppState.set_multiple_values({
            'ready_to_start_simulation': True,
            'openai_key': self.openai_api_key_value,
            'anthropic_key': self.anthropic_api_key_value,
            'supervisor_provider': self.supervisor_provider,
            'supervisor_model': self.supervisor_model,
            'supervisor_temperature': self.supervisor_temperature,
            'judge_provider': self.judge_provider,
            'judge_model': self.judge_model,
            'judge_temperature': self.judge_temperature,
            'witness_provider': self.witness_provider,
            'witness_model': self.witness_model,
            'witness_temperature': self.witness_temperature,
            'defense_provider': self.defense_provider,
            'defense_model': self.defense_model,
            'defense_temperature': self.defense_temperature,
            'prosecutor_provider': self.prosecutor_provider,
            'prosecutor_model': self.prosecutor_model,
            'prosecutor_temperature': self.prosecutor_temperature,
            'court_type': CourtCaseType.get_by_name(self.type_of_court_case)
        })

        if self.amount_of_juries is not None:
            AppState.set_multiple_values({
                'jury_provider': self.jury_provider,
                'jury_model': self.jury_model,
                'jury_temperature': self.jury_temperature,
                'juries_amount': self.amount_of_juries
            })

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
