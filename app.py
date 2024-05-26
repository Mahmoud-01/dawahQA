import streamlit as st
import os
from dotenv import load_dotenv
from pypdf import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings 
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from templates import css, bot_template, user_template

def get_pdf_text(pdfs_docs):
    text = ""
    for pdf in pdfs_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    vector_store = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vector_store

def get_conversation_chain(vector_store):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(),
        memory=memory
    )
    return conversation_chain

def handle_user_input(user_question):
    if st.session_state.conversation is None:
        st.error("Conversation chain is not initialized.")
        return

    response = st.session_state.conversation.respond({'question': user_question})
    st.session_state.chat_history = response['chat_history']
 
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)


   

def main():
    load_dotenv()
    st.set_page_config(page_title="DawahQA", page_icon=":books:")

    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

 
    st.header("Dawah Question and Answer :books:")
    st.text("Your one-stop platform to ask any question about Islam")
    user_question = st.text_input("Asalamualaikum! Kindly ask your question below:")
    if user_question:
        handle_user_input(user_question)

    st.write(user_template.replace("{{MSG}}", "hello Robot"), unsafe_allow_html=True)
    st.write(bot_template.replace("{{MSG}}", "Hello Human"), unsafe_allow_html=True)

    with st.sidebar:
        st.subheader("Your documents")
        pdfs_docs = st.file_uploader("Upload your PDfs here and click process", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("processing"):
                #get pdf text
                raw_texts = get_pdf_text(pdfs_docs)

                #get text chunk
                text_chunks = get_text_chunks(raw_texts)
                #st.write(text_chunks)

                #create vector store
                vectore_store = get_vector_store(text_chunks)

                #create conversation chain
                st.session_state.conversation = get_conversation_chain(vectore_store)
if __name__ == '__main__':
    main()
