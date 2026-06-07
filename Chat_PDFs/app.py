import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub
from profile_1 import myprofile
from langchain.prompts import SystemMessagePromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
logo = ''
general_system_template = r""" 
Given a specific context, please give an effective answer to the question, covering the required advices in general and then provide the names all of relevant(even if it relates a bit) products. 
 ----
{context}
----
"""
general_user_template = "Question:```{question}```"
messages = [
            SystemMessagePromptTemplate.from_template(general_system_template),
            HumanMessagePromptTemplate.from_template(general_user_template)
]
qa_prompt = ChatPromptTemplate.from_messages( messages )

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
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

def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


general_system_template = r""" 
You are my assistant. Respond to the user questions only based on the provided content.
 IF THE QUESTION, WHATSOEVER, IS NOT SIMILAR TO WHAT IS MENTIONED IN THE PROVIDED CONTEXT, PROVIDE SUGGESTIONS OF QUESTIONS THE USER CAN ASK AND RESPOND TO THEM.'
 VERIFY THE RESPONSE AND RESPOND WHEN YOU ARE CONFIDENT THAT THE RESPONSE IS ACCURATE. ANYTHING OUTSIDE THE CONTEXT SHOULD BE NOTIFIED.
 ----
{context}
----
"""
general_user_template = "Question:```{question}```"
messages = [
            SystemMessagePromptTemplate.from_template(general_system_template),
            HumanMessagePromptTemplate.from_template(general_user_template)
]
qa_prompt = ChatPromptTemplate.from_messages( messages )

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=vectorstore.as_retriever(), memory=memory, combine_docs_chain_kwargs={'prompt': qa_prompt})
    return conversation_chain

def handle_userinput(user_question, chat_container):
    if st.session_state.conversation is None:
        st.error(":red[Please process the documents first.]")
        return
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            # Remove prompt from user question to be displayed 
            chat_container.markdown(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
            # chat_container.markdown(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            chat_container.markdown(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with multiple Resumes", page_icon="logo.png")
    st.write(css, unsafe_allow_html=True)
    
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.header(":blue[Retrieval Augmented Generation (RAG)]")
    
    # Container for chat history
    chat_container = st.container()  # This will precede the user input to ensure it's always at the bottom

    # Place the user input below the chat history
    user_question = st.text_input(":orange[Ask a question about your documents:]", key="user_input")
    
    # Update chat container with history upon receiving input
    if user_question:
        handle_userinput(user_question , chat_container)

    with st.sidebar:
        st.image(logo, caption='')
        st.write('\n')
        st.write('\n')
        # st.subheader("Uploaded Documents")
        pdf_docs = st.file_uploader(":blue[Upload your PDFs here and click on 'Process']", accept_multiple_files=True)
        if pdf_docs:
            if st.button(":green[Process files]"):
                with st.spinner(":red[Wait while processing files]"):
                    # Get pdf text
                    raw_text = get_pdf_text(pdf_docs)

                    # Get the text chunks
                    text_chunks = get_text_chunks(raw_text)

                    # Create vector store
                    vectorstore = get_vectorstore(text_chunks)

                    # Create conversation chain
                    st.session_state.conversation = get_conversation_chain(vectorstore)

if __name__ == '__main__':
    main()