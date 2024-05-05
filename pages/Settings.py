import streamlit as st
from streamlit_extras.grid import grid as grid_layout

from enums.AiModels import AiModels
from enums.AiProvider import AiProvider
from enums.CourtCaseType import CourtCaseType


class Settings:
    openai_api_key_value = None
    anthropic_api_key_value = None

    def __init__(self) -> None:
        self.view()

    def validate_form(self) -> bool:
        if self.openai_api_key_value == '' and self.anthropic_api_key_value == '':
            st.error('Provide either an OpenAI or Anthropic API key')
            return False

        # TODO: Miejsca na walidacje kluczy
        # chat_singleton = Chat(anthropic_api_key, openai_api_key)
        # one_from_keys_is_valid = chat_singleton.validate_keys()
        # if (one_from_keys_is_valid):
        #     st.success('Good job!')
        # else:
        #     st.error('None of the given keys is corrent!')

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
                    supervisor_provider = st.selectbox('Supervisor provider', AiProvider.get_all())
                    supervisor_model = st.selectbox('Supervisor model',
                                                    AiModels.get_all_by_provider(supervisor_provider))
                with grid.container(border=True):
                    st.subheader('Judge :judge:')
                    judge_provider = st.selectbox('Judge provider', AiProvider.get_all())
                    judge_model = st.selectbox('Judge model', AiModels.get_all_by_provider(judge_provider))

                with grid.container(border=True):
                    st.subheader('Witness :adult:')
                    witness_provider = st.selectbox('Witness provider', AiProvider.get_all())
                    witness_model = st.selectbox('Witness model', AiModels.get_all_by_provider(witness_provider))
                with grid.container(border=True):
                    st.subheader('Defense :shield:')
                    defense_provider = st.selectbox('Defense provider', AiProvider.get_all())
                    defense_model = st.selectbox('Defense model', AiModels.get_all_by_provider(defense_provider))

                with grid.container(border=True):
                    st.subheader('Prosecutor :crossed_swords:')
                    prosecutor_provider = st.selectbox('Prosecutor provider', AiProvider.get_all())
                    prosecutor_model = st.selectbox('Prosecutor model',
                                                    AiModels.get_all_by_provider(prosecutor_provider))

        else:
            with main_container.container():
                grid = grid_layout(2, 2, 2)

                with grid.container(border=True):
                    st.subheader('Supervisor :brain:')
                    supervisor_provider = st.selectbox('Supervisor provider', AiProvider.get_all())
                    supervisor_model = st.selectbox('Supervisor model',
                                                    AiModels.get_all_by_provider(supervisor_provider))
                with grid.container(border=True):
                    st.subheader('Judge :judge:')
                    judge_provider = st.selectbox('Judge provider', AiProvider.get_all())
                    judge_model = st.selectbox('Judge model', AiModels.get_all_by_provider(judge_provider))

                with grid.container(border=True):
                    st.subheader('Witness :adult:')
                    witness_provider = st.selectbox('Witness provider', AiProvider.get_all())
                    witness_model = st.selectbox('Witness model', AiModels.get_all_by_provider(witness_provider))
                with grid.container(border=True):
                    st.subheader('Defense :shield:')
                    defense_provider = st.selectbox('Defense provider', AiProvider.get_all())
                    defense_model = st.selectbox('Defense model', AiModels.get_all_by_provider(defense_provider))

                with grid.container(border=True):
                    st.subheader('Prosecutor :crossed_swords:')
                    prosecutor_provider = st.selectbox('Prosecutor provider', AiProvider.get_all())
                    prosecutor_model = st.selectbox('Prosecutor model',
                                                    AiModels.get_all_by_provider(prosecutor_provider))
                with grid.container(border=True):
                    st.subheader('Jury :shield:')
                    jury_provider = st.selectbox('Jury provider', AiProvider.get_all())
                    jury_model = st.selectbox('Jury model', AiModels.get_all_by_provider(jury_provider))
                    amount_of_juries = st.slider('Amount of juries', min_value=1, max_value=10, step=1, format='%d')

        # Form Submit
        with main_container.columns([3, 3, 1])[2]:
            submitted = st.button('Submit')

        if submitted:
            if self.validate_form():
                st.success('Saved')
                st.session_state.openai_api_key = self.openai_api_key_value
                st.session_state.anthropic_api_key = self.anthropic_api_key_value
                st.session_state.settings_court_type = CourtCaseType.get_by_name(type_of_court_case)


settings = Settings()
