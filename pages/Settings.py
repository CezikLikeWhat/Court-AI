import streamlit as st
from streamlit_extras.grid import grid as grid_layout

from enums.AiModel import AiModel
from enums.AiProvider import AiProvider
from enums.CourtCaseType import CourtCaseType
from state.AppState import AppState
from validators.ApiKeyValidator import ApiKeyValidator
from validators.SettingsFormValidator import SettingsFormValidator


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

    def view(self) -> None:
        main_container = st.container(border=True)

        # AI Section
        main_container.title('AI :dna:')

        with main_container.container():
            st.subheader('OpenAI')
            self.openai_api_key_value = st.text_input(f'OpenAI API Key',
                                                      key='openai_api_key_input',
                                                      type='password',
                                                      value=st.session_state.openai_api_key if 'openai_api_key' in st.session_state else ''
                                                      )

        with main_container.container():
            st.subheader('Anthropic')
            self.anthropic_api_key_value = st.text_input(f'Anthropic API Key',
                                                         key='anthropic_api_key_input',
                                                         type='password',
                                                         value=st.session_state.anthropic_api_key if 'anthropic_api_key' in st.session_state else ''
                                                         )

        # Simulation
        main_container.title('Simulation :magic_wand:')
        type_of_court_case = main_container.selectbox('Type of court case', CourtCaseType.get_all())

        if CourtCaseType.get_by_name(type_of_court_case) == CourtCaseType.CIVIL:
            with main_container.container():
                grid = grid_layout(2, 2, [1, 1])

                with grid.container(border=True):
                    st.subheader('Supervisor :brain:')
                    self.supervisor_provider = st.selectbox('Supervisor provider', AiProvider.get_all())
                    self.supervisor_model = st.selectbox('Supervisor model',
                                                         AiModel.get_all_by_provider(self.supervisor_provider))
                with grid.container(border=True):
                    st.subheader('Judge :judge:')
                    self.judge_provider = st.selectbox('Judge provider', AiProvider.get_all())
                    self.judge_model = st.selectbox('Judge model', AiModel.get_all_by_provider(self.judge_provider))

                with grid.container(border=True):
                    st.subheader('Witness :adult:')
                    self.witness_provider = st.selectbox('Witness provider', AiProvider.get_all())
                    self.witness_model = st.selectbox('Witness model',
                                                      AiModel.get_all_by_provider(self.witness_provider))

                with grid.container(border=True):
                    st.subheader('Defense :shield:')
                    self.defense_provider = st.selectbox('Defense provider', AiProvider.get_all())
                    self.defense_model = st.selectbox('Defense model',
                                                      AiModel.get_all_by_provider(self.defense_provider))

                with grid.container(border=True):
                    st.subheader('Prosecutor :crossed_swords:')
                    self.prosecutor_provider = st.selectbox('Prosecutor provider', AiProvider.get_all())
                    self.prosecutor_model = st.selectbox('Prosecutor model',
                                                         AiModel.get_all_by_provider(self.prosecutor_provider))

        else:
            with main_container.container():
                grid = grid_layout(2, 2, 2)

                with grid.container(border=True):
                    st.subheader('Supervisor :brain:')
                    self.supervisor_provider = st.selectbox('Supervisor provider', AiProvider.get_all())
                    self.supervisor_model = st.selectbox('Supervisor model',
                                                         AiModel.get_all_by_provider(self.supervisor_provider))
                with grid.container(border=True):
                    st.subheader('Judge :judge:')
                    self.judge_provider = st.selectbox('Judge provider', AiProvider.get_all())
                    self.judge_model = st.selectbox('Judge model', AiModel.get_all_by_provider(self.judge_provider))

                with grid.container(border=True):
                    st.subheader('Witness :adult:')
                    self.witness_provider = st.selectbox('Witness provider', AiProvider.get_all())
                    self.witness_model = st.selectbox('Witness model',
                                                      AiModel.get_all_by_provider(self.witness_provider))

                with grid.container(border=True):
                    st.subheader('Defense :shield:')
                    self.defense_provider = st.selectbox('Defense provider', AiProvider.get_all())
                    self.defense_model = st.selectbox('Defense model',
                                                      AiModel.get_all_by_provider(self.defense_provider))

                with grid.container(border=True):
                    st.subheader('Prosecutor :crossed_swords:')
                    self.prosecutor_provider = st.selectbox('Prosecutor provider', AiProvider.get_all())
                    self.prosecutor_model = st.selectbox('Prosecutor model',
                                                         AiModel.get_all_by_provider(self.prosecutor_provider))

                with grid.container(border=True):
                    st.subheader('Jury :shield:')
                    self.jury_provider = st.selectbox('Jury provider', AiProvider.get_all())
                    self.jury_model = st.selectbox('Jury model', AiModel.get_all_by_provider(self.jury_provider))
                    self.amount_of_juries = st.slider('Amount of juries', min_value=1, max_value=10, step=1,
                                                      format='%d')

        # Form Submit
        with main_container.columns([3, 3, 1])[2]:
            submitted = st.button('Submit')

        if submitted:
            if self.validate_form():
                st.success('Saved')
                AppState.save_open_ai_key(self.openai_api_key_value)
                AppState.save_anthropic_key(self.anthropic_api_key_value)
                AppState.save_court_type(CourtCaseType.get_by_name(type_of_court_case))
                AppState.save_supervisor_provider(self.supervisor_provider)
                AppState.save_judge_provider(self.judge_provider)
                AppState.save_witness_provider(self.witness_provider)
                AppState.save_defense_provider(self.defense_provider)
                AppState.save_prosecutor_provider(self.prosecutor_provider)
                AppState.save_supervisor_model(self.supervisor_model)
                AppState.save_judge_model(self.judge_model)
                AppState.save_witness_model(self.witness_model)
                AppState.save_defense_model(self.defense_model)
                AppState.save_prosecutor_model(self.prosecutor_model)

                if self.amount_of_juries is not None:
                    AppState.save_jury_provider(self.jury_provider)
                    AppState.save_jury_model(self.jury_model)
                    AppState.save_juries_amount(self.amount_of_juries)


settings = Settings()
