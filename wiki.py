import os
import re
from dotenv import load_dotenv
load_dotenv()

# langchain dependencies
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.tools import Tool
from langchain import hub
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI

from tools import tools
import weasyprint
from pinecone import Pinecone

# Initialize Pinecone and OpenAI
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"), environment=os.getenv("PINECONE_ENVIRONMENT_REGION"))
index = pc.Index('wiki-index') 
client = OpenAI()

def get_url(topic: str):
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    
    prompt = """
    Given the topic {topic}, I want you to get the url of the wikipedia page.
    Your answer should be a url formatted like this: https://en.wikipedia.org/wiki/topic.
    """
    
    prompt_template = PromptTemplate(
        template=prompt, input_variables=["topic"]
    )
    
    tools_for_agent = [
        Tool(
            name="Crawl Wikipedia",
            func=tools.get_wiki_url,
            description="Useful for when you need to find the url of a edit section of a wikipedia page"
        )
    ]
    
    react_prompt = hub.pull("hwchase17/react")
    
    agent = create_react_agent(
        llm=llm,
        prompt=react_prompt,
        tools=tools_for_agent,
    )
    
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)
    
    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(topic=topic)}
    )
    
    wiki_url = result["output"]
    
    return wiki_url


def save_url_as_pdf(url: str, topic: str):
    """Save the wikipedia page as a pdf."""
    output_path = f"documents/{topic}.pdf"
    if os.path.exists(output_path):
        return output_path
    
    pdf = weasyprint.HTML(url).write_pdf()
    # Create the pdf file
    with open(output_path, 'wb') as f:
        f.write(pdf)
        
    return output_path


def get_answer(vectorstore, question: str) -> str:
    """Get the answer to a question."""
    qa = RetrievalQA.from_chain_type(llm=client, chain_type='stuff', retriever=vectorstore.as_retriever())
    answer = qa.invoke(question)
    return answer
        
        
def ask(path: str, question: str, topic: str) -> str:
    """Ask a question about the wikipedia page using local directories for storing vector stores (testing)."""
    vectorstore_path = f'vectorstores/faiss_index_react_{topic}'
    if os.path.exists(vectorstore_path):
        embeddings = OpenAIEmbeddings()
        new_vectorstore = FAISS.load_local(vectorstore_path, embeddings, allow_dangerous_deserialization=True)
        return get_answer(new_vectorstore, question)
    
    loader = PyPDFLoader(file_path=path)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=30, separator='\n')
    docs = text_splitter.split_documents(documents)
    
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(vectorstore_path)
    
    new_vectorstore = FAISS.load_local((vectorstore_path), embeddings, allow_dangerous_deserialization=True)
    return get_answer(new_vectorstore, question)

if __name__ == '__main__':
    topic = "LangChain"
    #url = get_url(topic)
    url = f"https://en.wikipedia.org/wiki/{topic}"
    
    path = save_url_as_pdf(url, topic)
    
    question = "How much did langchain raise in april 2023?"
    answer = ask(path, question, topic)['result']
    print(answer)
    
    