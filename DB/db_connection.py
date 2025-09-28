from sqlalchemy import MetaData, Table,select, create_engine

# Database credentials
user = 'root'
password = 'sai06'  # fix typo
host = '127.0.0.1'
port = 3306
database = 'rag'

def get_connection():
    """Create and return SQLAlchemy engine for MySQL"""
    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")
    return engine
    
def get_employee_table(engine):
    """Reflect and return the employee table"""
    metadata = MetaData()
    employee_table = Table('employee', metadata, autoload_with=engine)
    return employee_table

def get_salary_table(engine):
    """Reflect and return the employee table"""
    metadata = MetaData()
    salary_table = Table('salary', metadata, autoload_with=engine)
    return salary_table

def get_department_table(engine):
    """Reflect and return the employee table"""
    metadata = MetaData()
    department_table = Table('department', metadata, autoload_with=engine)
    return department_table

if __name__ == '__main__':
    try:
        engine = get_connection()
        employee_table = get_employee_table(engine)
        salary_table=get_salary_table(engine)
        department_table = get_department_table(engine)
        
        # # Print column names
        # print("Columns:", employee_table.columns.keys())

        # # Fetch and print all records
        # query = select(employee_table)  # SELECT * FROM employee
        # with engine.connect() as conn:
        #     result = conn.execute(query)
        #     for row in result:
        #         print(row)  # Each row is a tuple-like object

        print(f"Connection to MySQL at {host} for user {user} created successfully.")

    except Exception as ex:
        print("Connection could not be made due to the following error:\n", ex)