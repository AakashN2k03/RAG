from sqlalchemy import select
from ..DB.db_connection import get_connection, get_employee_table, get_department_table, get_salary_table
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

def fetch_table_metadata(table):
    """Return table schema and sample data as string for vector DB"""
    columns = ", ".join(table.columns.keys())
    return f"table: {table.name}, columns: {columns}"

# --- Connect and get tables ---
engine = get_connection()
employee_table = get_employee_table(engine)
department_table = get_department_table(engine)
salary_table = get_salary_table(engine)

# --- Prepare docs for Chroma ---
docs = []
for table in [employee_table, department_table, salary_table]:
    docs.append(fetch_table_metadata(table))

print("Table metadata prepared for vector DB.",docs)
# --- Load embeddings ---
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)

# --- Store table metadata in Chroma ---
vectordb = Chroma.from_texts(docs, embeddings, collection_name="table_metadata")
print("Vector DB for table metadata ready.")


from langchain_groq import ChatGroq

llm = ChatGroq(
    model="gemma2-9b-it",
    temperature=0,
    groq_api_key="GROQ_API_KEY"
)


def generate_sql(user_query, schema_info):
    prompt = f"""
    You are an SQL assistant. Tables and columns:
    {schema_info}

    User question: "{user_query}"

    Generate an SQL query for MySQL. Only give SQL, no explanations.
    """
    response = llm.invoke(prompt)   # use .invoke instead of calling directly
    print(f"Generated SQL: {response.content.strip()}")
    return response.content.strip()

def get_relevant_schema(user_query, k=2):
    results = vectordb.similarity_search(user_query, k=k)
    return "\n".join([doc.page_content for doc in results])

from sqlalchemy import text

def execute_sql(sql_query):
    with engine.connect() as conn:
        result = conn.execute(text(sql_query)).all()
    return result

user_query = "Return employees who do not have a manager (top-level employees). Include employee_id, name, dept_name, salary"

# Step 1: Get relevant table metadata from vector DB
schema_info = get_relevant_schema(user_query)

# Step 2: Generate SQL using LLM
sql_query = generate_sql(user_query, schema_info)
print("Generated SQL:", sql_query)

# Step 3: Execute SQL
results = execute_sql(sql_query)
print("Results:", results)


























# # --- Query vector DB ---
# query = "list the employee ids who got amount > 90000.00 as salary"
# # results = vectordb.similarity_search(query, k=3)
# results = vectordb.similarity_search(query,k=3)

# print(f"Query: {query}")
# for i, doc in enumerate(results):
#     print(f"{i+1}. {doc.page_content}")

