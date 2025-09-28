from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from .main import vectordb
# Initialize the LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Create RetrievalQA chain
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectordb.as_retriever(),
    return_source_documents=True
)

# Ask a question
query = "Who is the manager of employee John Doe?"
response = qa(query)
print("Answer:", response['result'])
print("Source:", response['source_documents'])
