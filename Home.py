import streamlit as st
from dotenv import load_dotenv

st.set_page_config(
    page_title='Home',
    page_icon=':wave:',
    layout='centered',
    initial_sidebar_state='collapsed'
)

load_dotenv()


class Home:
    def __init__(self):
        self.view()

    def view(self):
        with st.container(border=True):
            st.title('Hello :wave:')
            st.markdown('''
            The CourtAI project was created for the defense of a master's thesis at Nicolaus Copernicus University in Torun, Poland. 
            It is designed to simulate a court hearing using AI agents.
        
            Based on the innovative CrewAI framework, the project provides a dynamic experience in which each of the artificial intelligence agents will assume a specific role in the courtroom - from the judge, to the prosecution agent, to the witness agent and the defendant agent. 
            This allows you to learn about the trial based on the decisions made by the AI.
            ''')

            with st.columns(3)[1]:
                st.image('static/logo.png')

            st.subheader('Source code and contact')
            st.markdown('GitHub: **[Court-AI](https://github.com/CezikLikeWhat/Court-AI)**')
            st.markdown(
                'LinkedIn: **[Cezary Maćkowski](https://www.linkedin.com/in/cezary-ma%C4%87kowski-662194223/)**')
            st.markdown('Email: **<cezarymackowski99@gmail.com>**')


home = Home()
