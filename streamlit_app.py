import streamlit as st
from llama_index import VectorStoreIndex, ServiceContext, Document
from llama_index.llms import OpenAI
import openai
from llama_index import SimpleDirectoryReader
import random

st.set_page_config(page_title="Healthcare Bot", page_icon="👩‍⚕️", layout="centered", initial_sidebar_state="auto", menu_items=None)

openai.api_key = "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"
st.title("Have a Convo with your Healthcare Bot")
st.write("Arguments generates heat! and discussion throws light, in argument it seen who is right and in discussion it is seen what is RIGHT!")
if "messages" not in st.session_state.keys():  # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I hope you're doing well. How may I help you?"}
    ]

@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="I am not as intelligent as you - hang tight! This should take 1-2 minutes."):
        reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
        docs = reader.load_data()
        service_context = ServiceContext.from_defaults(
            llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt="You are an expert Digital doctor who gives curing tips, Assume all input prompts to be with respect to the input data, Don't answer anything apart from Healthcare and wellness related"))
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        return index

index = load_data()

if "chat_engine" not in st.session_state.keys():  # Initialize the chat engine
    st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

if prompt := st.chat_input("Your question"):  # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:  # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from the assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            user_input = st.session_state.messages[-1]["content"].lower()

            greeting_responses = [
                                    "Hello! How can I assist you today?",
                                    "Hi there! What can I do for you?",
                                    "Greetings! How may I help you?",
                                    "Hey! I'm here to help with any healthcare questions.",
                                    "Good day! What brings you here for a chat?",
                                ]

            farewell_responses = [
                "You're welcome! If you have more questions, feel free to ask. Goodbye!",
                "Goodbye! Take care.",
                "Farewell! If you need assistance in the future, don't hesitate to reach out.",
                "Until next time! Stay healthy and happy.",
                "Take care! If you ever need advice, I'll be here.",
                                    ]
           

            # Custom responses based on user input
            if any(keyword in user_input for keyword in ["hi", "hello", "greet"]):
                response_content = random.choice(greeting_responses)

            elif any(keyword in user_input for keyword in ["bye", "thank you"]):
                response_content = random.choice(farewell_responses)
            elif any(keyword in user_input for keyword in ["book", "schedule appointment", "looking for appointment" ,"need a appointment"] ):
                esponse_content = "Our Team is still working on to import the appointments form in the same window as of now you can cilck below and get scheduled your appointment"
                st.link_button("Go to appointment form" , "https://appointments-healthbot-pes.streamlit.app/" )

            else:
                response = st.session_state.chat_engine.chat(prompt)
                response_content = response.response

            st.write(response_content)
            message = {"role": "assistant", "content": response_content}
            st.session_state.messages.append(message)
