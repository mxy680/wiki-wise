# Import necessary modules
import os
from tools import tools
from dotenv import load_dotenv
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
from pyhtml2pdf import converter
from supabase import create_client

# Load environment variables from .env file
load_dotenv()

# Create Supabase client
supabase_client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))


def get_url(topic: str):
    """
    Get the URL of the Wikipedia page based on the given topic.
    """
    # Initialize ChatOpenAI with specific parameters
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    
    # Define the prompt template for querying the Wikipedia URL
    prompt = """
    Given the topic {topic}, I want you to get the url of the wikipedia page.
    Your answer should be a url formatted like this: https://en.wikipedia.org/wiki/topic.
    """
    
    prompt_template = PromptTemplate(
        template=prompt, input_variables=["topic"]
    )
    
    # Define tools for agent
    tools_for_agent = [
        Tool(
            name="Crawl Wikipedia",
            func=tools.get_wiki_url,
            description="Useful for when you need to find the url of a edit section of a wikipedia page"
        )
    ]
    
    # Pull react prompt from hub
    react_prompt = hub.pull("hwchase17/react")
    
    # Create a reactive agent
    agent = create_react_agent(
        llm=llm,
        prompt=react_prompt,
        tools=tools_for_agent,
    )
    
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)
    
    # Invoke the agent to get the Wikipedia URL
    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(topic=topic)}
    )
    
    wiki_url = result["output"]
    
    return wiki_url


def save_url_as_pdf(url: str, topic: str):
    """
    Save the Wikipedia page as a PDF and upload it to Supabase storage.
    """
    output_path = f"documents/{topic}.pdf"
    
    # Convert URL to PDF
    converter.convert(url, output_path)
    
    # Upload the PDF to Supabase storage
    with open(output_path, 'rb') as f:
        try:
            supabase_client.storage.from_("wikiwise").upload(file=f, path=f"documents/{topic}.pdf")
        except:
            pass
            
    # Delete the PDF from the local directory
    os.remove(output_path)
        
    return output_path  


def get_answer(vectorstore, question: str) -> str:
    """
    Get the answer to a question using the provided vector store.
    """
    # Initialize RetrievalQA object
    qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type='stuff', retriever=vectorstore.as_retriever())
    
    # Invoke the QA system to get the answer
    answer = qa.invoke(question)
    return answer
        
        
def ask(question: str, topic: str) -> str:
    """
    Ask a question about the Wikipedia page using local directories for storing vector stores (testing).
    """
    # Download the PDF document from Supabase storage
    res = supabase_client.storage.from_('wikiwise').download(path=f"documents/{topic}.pdf")
    with open(f"documents/{topic}.pdf", 'wb') as f:
        f.write(res)
        
    # Load PDF document
    loader = PyPDFLoader(file_path=f"documents/{topic}.pdf")
    documents = loader.load()
    
    # Split document into smaller chunks of text
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=30, separator='\n')
    docs = text_splitter.split_documents(documents)
    
    # Remove the downloaded PDF document
    os.remove(f"documents/{topic}.pdf")
    
    # Generate embeddings for the document
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    
    # Get the answer to the question using the vector store
    return get_answer(vectorstore, question)
