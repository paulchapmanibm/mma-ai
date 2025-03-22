import streamlit as st
import psycopg2
import psycopg2.extras
import os
from typing import List, Dict, Any, Tuple
import json
import pandas as pd
import time
import httpx
import asyncio
import re


# Set page config at the top level before any other Streamlit commands
st.set_page_config(
    page_title="SQL Assistant (Llama)",
    page_icon="🤖",
    layout="wide"
)

class DatabaseAnalyzer:
    """Class to analyze PostgreSQL database schema and execute queries."""

    def __init__(self, dbname: str, user: str, password: str, host: str = "localhost", port: str = "5432"):
        """Initialize with database connection parameters."""
        self.connection_params = {
            "dbname": dbname,
            "user": user,
            "password": password,
            "host": host,
            "port": port
        }
        self.connection = None
        self.schema_info = {}

    def connect(self) -> Tuple[bool, str]:
        """Establish connection to the database."""
        try:
            self.connection = psycopg2.connect(**self.connection_params)
            return True, "Connected to PostgreSQL database successfully!"
        except Exception as e:
            return False, f"Error connecting to PostgreSQL database: {e}"

    def close(self) -> str:
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            return "Database connection closed."

    def get_tables(self) -> List[str]:
        """Get all table names in the database."""
        if not self.connection:
            self.connect()

        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
        """)
        tables = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return tables

    def get_table_columns(self, table_name: str) -> List[Dict[str, str]]:
        """Get column details for a specific table."""
        if not self.connection:
            self.connect()

        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = %s
        """, (table_name,))

        columns = []
        for row in cursor.fetchall():
            columns.append({
                "name": row["column_name"],
                "type": row["data_type"],
                "nullable": row["is_nullable"]
            })

        cursor.close()
        return columns

    def get_foreign_keys(self) -> List[Dict[str, str]]:
        """Get all foreign key relationships in the database."""
        if not self.connection:
            self.connect()

        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("""
            SELECT
                tc.table_name AS table_name,
                kcu.column_name AS column_name,
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name
            FROM
                information_schema.table_constraints AS tc
                JOIN information_schema.key_column_usage AS kcu
                    ON tc.constraint_name = kcu.constraint_name
                JOIN information_schema.constraint_column_usage AS ccu
                    ON ccu.constraint_name = tc.constraint_name
            WHERE tc.constraint_type = 'FOREIGN KEY'
        """)

        foreign_keys = []
        for row in cursor.fetchall():
            foreign_keys.append({
                "table": row["table_name"],
                "column": row["column_name"],
                "foreign_table": row["foreign_table_name"],
                "foreign_column": row["foreign_column_name"]
            })

        cursor.close()
        return foreign_keys

    def get_sample_data(self, table_name: str, limit: int = 3) -> List[Dict[str, Any]]:
        """Get sample data from a table."""
        if not self.connection:
            self.connect()

        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
            columns = [desc[0] for desc in cursor.description]

            results = []
            for row in cursor.fetchall():
                result_dict = {}
                for i, column in enumerate(columns):
                    result_dict[column] = row[i]
                results.append(result_dict)

            return results
        except Exception as e:
            print(f"Error getting sample data: {e}")
            return []
        finally:
            cursor.close()

    def analyze_schema(self) -> Dict[str, Any]:
        """Analyze the database schema and store the information."""
        tables = self.get_tables()
        foreign_keys = self.get_foreign_keys()

        schema_info = {
            "tables": {},
            "relationships": [],
            "sample_data": {}
        }

        # Get information about each table and its columns
        for table in tables:
            columns = self.get_table_columns(table)
            schema_info["tables"][table] = columns

            # Get sample data
            sample_data = self.get_sample_data(table)
            if sample_data:
                schema_info["sample_data"][table] = sample_data

        # Add relationship information
        for fk in foreign_keys:
            schema_info["relationships"].append({
                "table": fk["table"],
                "column": fk["column"],
                "references_table": fk["foreign_table"],
                "references_column": fk["foreign_column"]
            })

        self.schema_info = schema_info
        return schema_info

    def generate_schema_description(self) -> str:
        """Generate a human-readable description of the database schema."""
        if not self.schema_info:
            self.analyze_schema()

        description = "Database Schema:\n\n"

        # Describe each table and its columns
        for table_name, columns in self.schema_info["tables"].items():
            description += f"Table: {table_name}\n"
            description += "Columns:\n"

            for column in columns:
                nullable = "NULL" if column["nullable"] == "YES" else "NOT NULL"
                description += f"  - {column['name']} ({column['type']}, {nullable})\n"

            # Add sample data if available
            if table_name in self.schema_info.get("sample_data", {}):
                description += "Sample data:\n"
                for i, row in enumerate(self.schema_info["sample_data"][table_name][:2]):
                    description += f"  Row {i+1}: {row}\n"

            description += "\n"

        # Describe relationships
        if self.schema_info["relationships"]:
            description += "Relationships:\n"
            for rel in self.schema_info["relationships"]:
                description += f"  - {rel['table']}.{rel['column']} references {rel['references_table']}.{rel['references_column']}\n"

        return description

    def generate_schema_for_llm(self) -> str:
        """Generate a comprehensive schema description for the LLM."""
        if not self.schema_info:
            self.analyze_schema()

        schema_text = "# Database Schema\n\n"

        # Describe each table and its columns
        for table_name, columns in self.schema_info["tables"].items():
            schema_text += f"## Table: {table_name}\n"

            # Create a markdown table for columns
            schema_text += "| Column Name | Data Type | Nullable |\n"
            schema_text += "|------------|-----------|----------|\n"

            for column in columns:
                nullable = "YES" if column["nullable"] == "YES" else "NO"
                schema_text += f"| {column['name']} | {column['type']} | {nullable} |\n"

            # Add sample data if available
            if table_name in self.schema_info.get("sample_data", {}) and self.schema_info["sample_data"][table_name]:
                schema_text += "\nSample data:\n```\n"
                sample_data = self.schema_info["sample_data"][table_name]
                if sample_data:
                    keys = sample_data[0].keys()
                    schema_text += ", ".join(keys) + "\n"
                    for row in sample_data[:2]:  # Just show first 2 rows
                        schema_text += ", ".join(str(row[k]) for k in keys) + "\n"
                schema_text += "```\n"

            schema_text += "\n"

        # Describe relationships
        if self.schema_info["relationships"]:
            schema_text += "## Relationships\n"
            for rel in self.schema_info["relationships"]:
                schema_text += f"- {rel['table']}.{rel['column']} → {rel['references_table']}.{rel['references_column']}\n"

        return schema_text

    def execute_query(self, query: str) -> Tuple[List[Dict[str, Any]], List[str]]:
        """Execute an SQL query and return the results as a list of dictionaries."""
        if not self.connection:
            self.connect()

        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute(query)

            # Get column names
            columns = [desc[0] for desc in cursor.description] if cursor.description else []

            # Fetch all results
            results = []
            for row in cursor.fetchall():
                result_dict = {}
                for i, column in enumerate(columns):
                    result_dict[column] = row[i]
                results.append(result_dict)

            return results, columns
        except Exception as e:
            raise Exception(f"Error executing query: {e}")
        finally:
            cursor.close()

def extract_sql_from_response(response: str) -> str:
    """
    Extract SQL query from the LLM response, focusing on the content inside triple backticks.
    If triple backticks are present, extract the content within them.
    Otherwise, use the entire response with minimal cleaning.
    """
    # Look for SQL code blocks with triple backticks
    # The pattern matches ```sql ... ``` or just ``` ... ```
    sql_block_pattern = r'```(?:sql)?(.*?)```'
    matches = re.findall(sql_block_pattern, response, re.DOTALL)

    if matches:
        # Use the first code block found
        sql_query = matches[0].strip()
    else:
        # If no code blocks, use the whole response
        sql_query = response.strip()

    # Remove any "SQL query:" prefix or similar text
    sql_query = re.sub(r'^(?:SQL query|Query|SQL):?\s*', '', sql_query, flags=re.IGNORECASE)

    # Remove any lingering backticks
    sql_query = sql_query.replace('`', '')

    return sql_query

class LlamaInterface:
    """Interface for LLM-based natural language to SQL conversion using Llama API."""

    def __init__(self, host="llama-service", port="8080"):
        """Initialize the Llama interface with host and port."""
        self.host = host
        self.port = port

    async def get_llama_response(self, prompt):
        """Get a response from the Llama API."""
        json_data = {
            'prompt': prompt,
            'temperature': 0.1,
            'n_predict': 500,
            'stream': True,
        }

        async with httpx.AsyncClient(timeout=120) as client:
            async with client.stream('POST', f'http://{self.host}:{self.port}/completion', json=json_data) as response:
                full_response = ""
                async for chunk in response.aiter_bytes():
                    try:
                        data = json.loads(chunk.decode('utf-8')[6:])
                        if data['stop'] is False:
                            full_response += data['content']
                    except:
                        pass

        return full_response

    async def generate_sql_async(self, question: str, schema_description: str) -> str:
        """Generate SQL from natural language using Llama."""
        prompt = f"""
You are an expert SQL query generator for PostgreSQL databases.
Given the database schema below, generate a SQL query to answer the question.

{schema_description}

Question: {question}

IMPORTANT:
I want you to format your response using triple backticks. Place the SQL query inside these backticks like this:
```sql
SELECT * FROM table WHERE condition;
```

Make sure the query inside the backticks is valid PostgreSQL syntax with no comments or additional text.
"""

        sql_query = await self.get_llama_response(prompt)
        return extract_sql_from_response(sql_query)

    def generate_sql(self, question: str, schema_description: str) -> str:
        """Synchronous wrapper for generate_sql_async."""
        return asyncio.run(self.generate_sql_async(question, schema_description))

    async def explain_results_async(self, question: str, sql_query: str, results: List[Dict[str, Any]], error: str = None) -> str:
        """Explain the results in natural language."""
        if error:
            prompt = f"""
Question: {question}

SQL Query: {sql_query}

Error: {error}

Please explain what went wrong with this query in simple terms and suggest how to fix it.
Be specific about any syntax errors or invalid references.
"""
        else:
            # Convert results to a string - limit to 10 results to manage context length
            results_str = json.dumps(results[:10], indent=2, default=str)

            prompt = f"""
Question: {question}

SQL Query: {sql_query}

Results: {results_str}

Provide a natural language explanation of these results that directly answers the original question.
Keep your explanation clear, concise, and focused on what the user actually asked.
If the results contain a lot of data, summarize the key points.
"""

        explanation = await self.get_llama_response(prompt)
        return explanation.strip()

    def explain_results(self, question: str, sql_query: str, results: List[Dict[str, Any]], error: str = None) -> str:
        """Synchronous wrapper for explain_results_async."""
        return asyncio.run(self.explain_results_async(question, sql_query, results, error))

def main():

    st.title("SQL Assistant powered by Llama")
    st.write("Ask questions about your PostgreSQL database in plain English.")

    # Check for session state initialization
    if 'connected' not in st.session_state:
        st.session_state['connected'] = False
    if 'query_history' not in st.session_state:
        st.session_state['query_history'] = []
    if 'llm_initialized' not in st.session_state:
        st.session_state['llm_initialized'] = False

    # Sidebar for LLM settings
    st.sidebar.header("Llama API Settings")

    # Llama connection settings
    llama_host = st.sidebar.text_input("Llama API Host", "llama-service")
    llama_port = st.sidebar.text_input("Llama API Port", "8080")

    # Initialize LLM button
    if st.sidebar.button("Initialize Llama Interface"):
        with st.spinner("Initializing Llama interface..."):
            try:
                # Initialize the Llama interface
                llama_interface = LlamaInterface(
                    host=llama_host,
                    port=llama_port
                )

                # Store in session state
                st.session_state['llama_interface'] = llama_interface
                st.session_state['llm_initialized'] = True

                st.sidebar.success("Llama interface initialized successfully!")
            except Exception as e:
                st.sidebar.error(f"Error initializing Llama interface: {str(e)}")

    # Database connection inputs
    st.sidebar.header("Database Connection")
    db_host = st.sidebar.text_input("Host", "localhost")
    db_port = st.sidebar.text_input("Port", "5432")
    db_name = st.sidebar.text_input("Database Name")
    db_user = st.sidebar.text_input("Username")
    db_password = st.sidebar.text_input("Password", type="password")

    # Connect button
    if st.sidebar.button("Connect to Database"):
        if not all([db_name, db_user, db_password]):
            st.sidebar.error("Please provide all required database connection details.")
        elif not st.session_state['llm_initialized']:
            st.sidebar.error("Please initialize the Llama interface first.")
        else:
            with st.spinner("Connecting to database and analyzing schema..."):
                try:
                    # Initialize the database analyzer
                    db_analyzer = DatabaseAnalyzer(
                        dbname=db_name,
                        user=db_user,
                        password=db_password,
                        host=db_host,
                        port=db_port
                    )

                    # Try to connect
                    success, message = db_analyzer.connect()

                    if success:
                        st.sidebar.success(message)

                        # Analyze the schema
                        with st.spinner("Analyzing database schema..."):
                            schema_info = db_analyzer.analyze_schema()
                            schema_description = db_analyzer.generate_schema_description()
                            schema_for_llm = db_analyzer.generate_schema_for_llm()

                        # Store components in session state
                        st.session_state['db_analyzer'] = db_analyzer
                        st.session_state['schema_description'] = schema_description
                        st.session_state['schema_for_llm'] = schema_for_llm
                        st.session_state['connected'] = True

                        st.sidebar.success("Successfully connected and analyzed the database schema!")
                    else:
                        st.sidebar.error(message)
                except Exception as e:
                    st.sidebar.error(f"Error: {str(e)}")

    # Option to view database schema
    if st.session_state['connected']:
        with st.sidebar.expander("View Database Schema"):
            st.text(st.session_state['schema_description'])

    # Main area for question input
    st.header("Ask a Question")

    # Query input and submission
    question = st.text_area("Enter your question in plain English:", height=100,
                            placeholder="e.g., 'What were the top 5 selling products last month?' or 'How many users signed up in 2023?'")

    col1, col2 = st.columns([1, 5])
    with col1:
        ready_to_query = st.session_state['connected'] and st.session_state['llm_initialized']
        submit_button = st.button("Generate SQL", type="primary", disabled=not ready_to_query)
    with col2:
        if not st.session_state['llm_initialized']:
            st.info("Initialize the Llama interface first.")
        elif not st.session_state['connected']:
            st.info("Connect to a database to start asking questions.")

    # Process the question when submitted
    if submit_button and question:
        if not st.session_state['connected'] or not st.session_state['llm_initialized']:
            st.error("Please make sure the Llama interface is initialized and you're connected to a database.")
        else:
            # Create a container for the results
            results_container = st.container()

            with results_container:
                with st.spinner("Generating SQL query with Llama..."):
                    try:
                        # Generate SQL with Llama
                        raw_response = asyncio.run(st.session_state['llama_interface'].get_llama_response(
                            f"""
You are an expert SQL query generator for PostgreSQL databases.
Given the database schema below, generate a SQL query to answer the question.

{st.session_state['schema_for_llm']}

Question: {question}

IMPORTANT:
I want you to format your response using triple backticks. Place the SQL query inside these backticks like this:
```sql
SELECT * FROM table WHERE condition;
```

Make sure the query inside the backticks is valid PostgreSQL syntax with no comments or additional text.
"""
                        ))

                        # Display the raw response in an expander for debugging
                        with st.expander("Raw LLM Response", expanded=False):
                            st.text(raw_response)

                        # Extract SQL query from the response
                        sql_query = extract_sql_from_response(raw_response)

                        # Display the extracted SQL
                        st.subheader("Generated SQL Query")
                        st.code(sql_query, language="sql")

                        # Execute the query
                        with st.spinner("Executing query..."):
                            try:
                                results, columns = st.session_state['db_analyzer'].execute_query(sql_query)

                                # Generate explanation
                                with st.spinner("Generating explanation with Llama..."):
                                    explanation = st.session_state['llama_interface'].explain_results(
                                        question,
                                        sql_query,
                                        results
                                    )

                                # Display explanation
                                st.subheader("Answer")
                                st.write(explanation)

                                # Display results as a table if available
                                if results and columns:
                                    with st.expander("View Detailed Results", expanded=True):
                                        st.subheader("Query Results")
                                        df = pd.DataFrame(results)
                                        st.dataframe(df)

                                        # Option to download results as CSV
                                        csv = df.to_csv(index=False)
                                        st.download_button(
                                            label="Download results as CSV",
                                            data=csv,
                                            file_name="query_results.csv",
                                            mime="text/csv"
                                        )

                                # Add to query history
                                st.session_state['query_history'].append({
                                    "question": question,
                                    "sql_query": sql_query,
                                    "results_count": len(results),
                                    "explanation": explanation,
                                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                                })

                            except Exception as e:
                                st.error(f"Error executing the query: {str(e)}")

                                # Generate explanation for the error
                                with st.spinner("Analyzing the error with Llama..."):
                                    error_explanation = st.session_state['llama_interface'].explain_results(
                                        question,
                                        sql_query,
                                        [],
                                        error=str(e)
                                    )

                                st.subheader("Error Analysis")
                                st.write(error_explanation)

                                # Offer manual edit option
                                st.subheader("Fix the Query")
                                fixed_query = st.text_area("Edit the SQL query to fix the error:", value=sql_query, height=150)

                                if st.button("Execute Fixed Query"):
                                    with st.spinner("Executing fixed query..."):
                                        try:
                                            results, columns = st.session_state['db_analyzer'].execute_query(fixed_query)

                                            st.success("Query executed successfully!")

                                            # Display results
                                            if results and columns:
                                                st.subheader("Query Results")
                                                df = pd.DataFrame(results)
                                                st.dataframe(df)

                                                # Option to download results as CSV
                                                csv = df.to_csv(index=False)
                                                st.download_button(
                                                    label="Download results as CSV",
                                                    data=csv,
                                                    file_name="fixed_query_results.csv",
                                                    mime="text/csv"
                                                )
                                            else:
                                                st.info("Query executed successfully but returned no results.")

                                            # Add to query history
                                            st.session_state['query_history'].append({
                                                "question": f"FIXED: {question}",
                                                "sql_query": fixed_query,
                                                "results_count": len(results),
                                                "explanation": "Manually fixed query",
                                                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                                            })

                                        except Exception as e:
                                            st.error(f"Error executing fixed query: {str(e)}")

                    except Exception as e:
                        st.error(f"Error generating SQL: {str(e)}")

    # Option to manually edit and execute a query
    st.header("Manual SQL Query")

    # Only allow editing if connected to a database
    if st.session_state.get('connected', False):
        manual_query = st.text_area("Enter SQL query manually:", height=100)

        if st.button("Execute Manual Query"):
            if not manual_query:
                st.error("Please enter a SQL query.")
            else:
                with st.spinner("Executing query..."):
                    try:
                        # Execute the query
                        results, columns = st.session_state['db_analyzer'].execute_query(manual_query)

                        # Display results
                        st.success("Query executed successfully!")

                        if results and columns:
                            st.subheader("Query Results")
                            df = pd.DataFrame(results)
                            st.dataframe(df)

                            # Option to download results as CSV
                            csv = df.to_csv(index=False)
                            st.download_button(
                                label="Download results as CSV",
                                data=csv,
                                file_name="manual_query_results.csv",
                                mime="text/csv"
                            )
                        else:
                            st.info("Query executed successfully but returned no results.")

                        # Add to query history
                        st.session_state['query_history'].append({
                            "question": "MANUAL QUERY",
                            "sql_query": manual_query,
                            "results_count": len(results) if results else 0,
                            "explanation": "Manually entered query",
                            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                        })

                    except Exception as e:
                        st.error(f"Error executing the query: {str(e)}")
    else:
        st.info("Connect to a database to manually execute SQL queries.")

    # Display query history
if st.session_state.get('connected', False) and st.session_state.get('query_history', []):
    st.header("Query History")

    # Create tabs for each history item
    history_items = list(reversed(st.session_state['query_history']))
    tab_labels = [f"Query {i+1}: {item['timestamp']}" for i, item in enumerate(history_items)]

    # Use tabs instead of nested expanders
    tabs = st.tabs(tab_labels)

    for i, (tab, item) in enumerate(zip(tabs, history_items)):
        with tab:
            st.markdown(f"**Question:** {item['question']}")
            st.markdown(f"**Time:** {item['timestamp']}")

            # Show SQL
            st.subheader("SQL Query")
            st.code(item['sql_query'], language="sql")

            # Show results info
            st.markdown(f"**Results:** {item['results_count']} rows returned")
            st.markdown(f"**Explanation:** {item['explanation']}")

            # Add a "Use this query" button
            if st.button(f"Use this query", key=f"use_query_{i}"):
                st.session_state['reuse_query'] = item['sql_query']
                st.experimental_rerun()

    # Check if there's a query to reuse
    if 'reuse_query' in st.session_state:
        # Pre-fill the manual query area
        st.session_state['manual_query'] = st.session_state['reuse_query']
        # Clear the reuse flag
        del st.session_state['reuse_query']

    # Display help information
    with st.expander("Help & Tips"):
        st.markdown("""
        ### How to Use This Tool

        1. **Initialize the Llama interface** by providing the host and port of your Llama API
        2. **Connect to your database** by entering your PostgreSQL credentials
        3. **Ask questions** about your data in plain English
        4. Llama will generate an SQL query, execute it, and explain the results

        ### Troubleshooting SQL Errors

        If you encounter SQL errors, you can:

        1. **Fix the query directly** in the error section
        2. **Use the manual query editor** to write your own SQL
        3. **Check query history** for examples of working queries

        ### Effective Question Tips

        - **Be specific** about what you're looking for
        - **Mention table or column names** if you know them
        - **Specify time periods** for time-based queries
        - **Include aggregation terms** like "total," "average," or "count" when appropriate
        """)

    # Footer
    st.sidebar.markdown("---")
    st.sidebar.info("""
    **SQL Assistant powered by Llama**

    This app connects to your Llama API service to convert natural
    language questions into SQL queries for PostgreSQL databases.

    Make sure your Llama API service is running and accessible at
    the host and port provided in the settings.
    """)

if __name__ == "__main__":
    main()
