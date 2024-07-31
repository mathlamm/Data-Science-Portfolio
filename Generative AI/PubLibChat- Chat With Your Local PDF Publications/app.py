import pandas as pd
import streamlit as st
from langchain.llms import LlamaCpp
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain, ConversationalRetrievalChain
from langchain.vectorstores import FAISS
from langchain import PromptTemplate
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, PyPDFDirectoryLoader

from functions import sources


# llm
@st.cache_resource
def init_llm():
  return LlamaCpp(model_path = "models/mistral-7b-instruct-v0.1.Q4_K_M.gguf",
                  max_tokens = 2000,
                  temperature = 0.1,
                  top_p = 1,
                  n_ctx = 4096)
llm = init_llm()

# embeddings
embedding_model = "sentence-transformers/all-MiniLM-l6-v2"
embeddings_folder = "models/"
embeddings = HuggingFaceEmbeddings(model_name=embedding_model,
                                   cache_folder=embeddings_folder)

# load vector Database
# allow_dangerous_deserialization is needed. Pickle files can be modified to deliver a malicious payload that results in execution of arbitrary code on your machine
vector_db = FAISS.load_local("data/PubLib_faiss_index", embeddings, allow_dangerous_deserialization=True)


##### streamlit #####
st.title("PubLibChat")
st.markdown("Chat with your local publication library")

# Sidebar with options
with st.sidebar:

    # Info about source
    st.markdown("## Library \nGut-brain interactions in Bariatric Surgery.\n#### Source folder: `Referenzen`\nNr of PDF files included: 465")

    # an "Open Folder" button - does not seem to work atm
    #st.download_button("Open folder", Path("C:\Users\nix-n\Nextcloud\Beruf\Promotion\Referenzen").read_text(), "test.log")
    # folder_path = Path("")
    # if st.button('Open folder'):
    #     check_output("start C:/Users/nix-n/Nextcloud/Beruf/Promotion/Referenzen/", shell=True)
    #     #os.startfile(folder_path)("start C:/Users/nix-n/Nextcloud/Beruf/Promotion/Referenzen" + folder_path, shell=True)
    
    # slider
    n_sources = st.slider(label="#### Number of source chunks", min_value=4, max_value=20, value=5, step=1)




# Define retriever
retriever = vector_db.as_retriever(search_kwargs={"k": n_sources})

# memory
@st.cache_resource
def init_memory(_llm):
    return ConversationBufferMemory(
        llm=llm,
        output_key='answer',
        memory_key='chat_history',
        return_messages=True)
memory = init_memory(llm)

# prompt
template = """
<s> [INST]
You are polite and professional question-answering AI assistant. You must provide a helpful response to the user.

In your response, PLEASE ALWAYS:
  (0) Be a detail-oriented reader: read the question and context and understand both before answering
  (1) Start your answer with a friendly tone, and reiterate the question so the user is sure you understood it
  (2) If the context enables you to answer the question, write a detailed, helpful, and easily understandable answer. If you can't find the answer, respond with an explanation, starting with: "I couldn't find the answer in the information I have access to".
  (3) Ensure your answer answers the question, is helpful, professional, and formatted to be easily readable.
[/INST]
[INST]
Answer the following question using the context provided.
The question is surrounded by the tags <q> </q>.
The context is surrounded by the tags <c> </c>.
<q>
{question}
</q>
<c>
{context}
</c>
[/INST]
</s>
[INST]
Helpful Answer:
[INST]
"""

prompt = PromptTemplate(template=template,
                        input_variables=["context", "question"])


# Model chain
chain = ConversationalRetrievalChain.from_llm(llm,
                                              retriever=retriever,
                                              memory=memory,
                                              return_source_documents=True,
                                              combine_docs_chain_kwargs={"prompt": prompt})




# Initialise chat history
# Chat history saves the previous messages to be displayed
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Whats your question?"):

    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Begin spinner before answering question so it's there for the duration
    with st.spinner("Thinking.. this might take a minute or two"):

        # send question to chain to get answer
        answer = chain(prompt)

        # extract answer from dictionary returned by chain
        response = answer["answer"]

        # generate sources
        answer_sources = sources(answer, format="md")

        # Display chatbot response in chat message container
        with st.chat_message("assistant"):
            st.markdown(answer["answer"]+answer_sources)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response+answer_sources})