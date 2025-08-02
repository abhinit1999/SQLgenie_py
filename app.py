import os
import sqlite3
import time
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()

# Function to generate SQL query using Groq LLM
def get_sql_query(user_query):
    groq_sys_prompt = ChatPromptTemplate.from_template("""
        You are an expert at converting English questions into SQL queries.
        The SQL database is named STUDENT and contains the following columns: NAME, COURSE, SECTION, and MARKS.
        Examples:
        - "How many entries of records are present?" → SELECT COUNT(*) FROM STUDENT;
        - "Tell me all the students studying in Data Science COURSE?" → SELECT * FROM STUDENT WHERE COURSE = "Data Science";

        Instructions:
        - Only return valid SQL queries. Do not include any preamble, explanation, or formatting like ``` or the word "sql".
        - Never generate queries containing DELETE, DROP, or TRUNCATE.
        - If the question cannot be answered using the STUDENT table and its columns, or if it is unclear, respond with exactly:
          Sorry I do not have any idea about it
        - Do not attempt to guess or hallucinate columns or tables that are not defined.

        Now convert the following English question into a valid SQL query:
        {user_query}
    """)

    model = "llama3-8b-8192"
    groq_api_key = os.getenv("GROQ_API_KEY")

    llm = ChatGroq(
        groq_api_key=groq_api_key,
        model_name=model
    )

    chain = groq_sys_prompt | llm | StrOutputParser()
    response = chain.invoke({"user_query": user_query}).strip()

    # Safety check
    if any(keyword in response.upper() for keyword in ["DELETE", "DROP", "TRUNCATE"]) or \
       "Sorry I do not have any idea about it" in response.lower():
        return "Sorry I do not have any idea about it"
    
    return response

# Function to execute SQL query safely
def return_sql_response(sql_query):
    if sql_query == "Sorry I do not have any idea about it":
        return sql_query

    database = "student.db"
    try:
        with sqlite3.connect(database) as conn:
            return conn.execute(sql_query).fetchall()
    except Exception as e:
        return f"Error executing SQL: {e}"

# Streamlit UI
def main():
    st.set_page_config(page_title="Prompt To SQL")
    st.header("Prompt2SQL v0.1.0")

    # Sidebar
    st.sidebar.title("About This App")
    st.sidebar.subheader("This is just a POC **(v0.1.0)**")
    st.sidebar.markdown("""
    This app lets you talk to your database using natural language.  
    It converts your questions into SQL queries using LLMs and executes them on your data.  
    Here in this case, the database name is STUDENT.
    """)
    st.sidebar.markdown("#### 👨‍💻 Built by: Abhinit")
    st.sidebar.markdown("#### ⚡ Tech: Python + LangChain + Groq + Streamlit")






    # Main input
    user_query = st.text_input("Natural language query:")
    submit = st.button("Result")


    




    if submit:
        with st.spinner("🔄 Generating SQL and fetching results..."):
            time.sleep(4)

        sql_query = get_sql_query(user_query)
        retrieved_data = return_sql_response(sql_query)

        

        if sql_query == "Sorry I do not have any idea about it":
            st.warning("⚠️ Sorry, I do not have any idea about that query.")
            
        elif isinstance(retrieved_data, str) and retrieved_data.startswith("Error"):
            st.error(f"❌ SQL Execution Failed: {retrieved_data}")
        else:
            st.subheader(f"Data successfully retrieved for:- {user_query}\nSQL Query is: [{sql_query}]")
            for row in retrieved_data:
                st.write(row)
    st.write("""
                Test with Sample Table: STUDENT
                Interact with the app using our sample table STUDENT, which includes the following columns:

               - NAME — Name of the student

               - COURSE — Course name (e.g., Data Science, DEVOPS,Machine learning,AI Ethics...)

               - SECTION — Class section (e.g., A, B, C)

               - MARKS — Marks scored by the student
        """)

if __name__ == '__main__':
    main()