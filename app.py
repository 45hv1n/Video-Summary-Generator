import streamlit as st
import math
from assembly_ai import get_transcription_result_url , upload , poll , transcribe
import moviepy.editor as py
#from transformers import pipeline

with open("style.css")as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

#summarizer = pipeline("summarization")

st.title("Video Descriptor")
uploaded_file = st.file_uploader("Choose a file")

if uploaded_file:

    final_txt = "Description:\n"
    #st.write(uploaded_file.name)

    video_bytes = uploaded_file.read()
    st.video(video_bytes)

    if st.button("Generate"):

        vc = py.VideoFileClip(uploaded_file.name)
        vc.audio.write_audiofile("test1.mp3")

        response = get_transcription_result_url(upload("test1.mp3"))

        text = response[0]["summary"]

        st.write(text)


    
    
    
