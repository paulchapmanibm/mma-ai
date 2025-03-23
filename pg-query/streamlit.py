import streamlit as st
import pandas as pd
import time
import asyncio
import json

# Import our modules
from database_analyzer import DatabaseAnalyzer
from llama_interface import LlamaInterface
from utils import extract_sql_from_response

# Set page config at the top level before any other Streamlit commands
st.set_page_config(
    page_title="SQL Assistant (Using Power MMA)",
    page_icon="🤖",
    layout="wide"
)

def main():
    st.title("SQL Assistant powered by Power10 MMA")
    st.write("Ask questions about your PostgreSQL database in plain English. Enhanced with intelligent schema semantics.")

    # Initialize all session state variables
    if 'connected' not in st.session_state:
        st.session_state['connected'] = False
    if 'query_history' not in st.session_state:
        st.session_state['query_history'] = []
    if 'llm_initialized' not in st.session_state:
        st.session_state['llm_initialized'] = False
    if 'db_analyzer' not in st.session_state:
        st.session_state['db_analyzer'] = None
    if 'schema_description' not in st.session_state:
        st.session_state['schema_description'] = ""
    if 'schema_for_llm' not in st.session_state:
        st.session_state['schema_for_llm'] = ""

    # Sidebar for LLM settings
    st.sidebar.header("Runtime API Settings")

    # LLM Runtime connection settings
    llama_host = st.sidebar.text_input("LLM Runtime API Host", "llama-service")
    llama_port = st.sidebar.text_input("LLM Runtime API Port", "8080")

    # Initialize LLM button
    if st.sidebar.button("Initialize LLM Runtime Interface"):
        with st.spinner("Initializing LLM Runtime interface..."):
            try:
                # Initialize the LLM Runtime interface
                llama_interface = LlamaInterface(
                    host=llama_host,
                    port=llama_port
                )

                # Store in session state
                st.session_state['llama_interface'] = llama_interface
                st.session_state['llm_initialized'] = True

                st.sidebar.success("LLM Runtime interface initialized successfully!")
            except Exception as e:
                st.sidebar.error(f"Error initializing LLM Runtime interface: {str(e)}")

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
            st.sidebar.error("Please initialize the LLM Runtime interface first.")
        else:
            with st.spinner("Connecting to database and analyzing schema..."):
                try:
                    # Initialize the database analyzer with LLM integration
                    db_analyzer = DatabaseAnalyzer(
                        dbname=db_name,
                        user=db_user,
                        password=db_password,
                        host=db_host,
                        port=db_port,
                        llm_host=llama_host,
                        llm_port=llama_port
                    )

                    # Try to connect
                    success, message = db_analyzer.connect()

                    if success:
                        st.sidebar.success(message)

                        # Analyze the schema with LLM-enhanced semantics
                        with st.spinner("Analyzing database schema and inferring column semantics with LLM..."):
                            schema_info = db_analyzer.analyze_schema()
                            schema_description = db_analyzer.generate_schema_description()
                            schema_for_llm = db_analyzer.generate_schema_for_llm()

                        # Store components in session state
                        st.session_state['db_analyzer'] = db_analyzer
                        st.session_state['schema_description'] = schema_description
                        st.session_state['schema_for_llm'] = schema_for_llm
                        st.session_state['connected'] = True

                        st.sidebar.success("Successfully connected and analyzed the database schema with LLM-enhanced semantics!")
                    else:
                        st.sidebar.error(message)
                except Exception as e:
                    st.sidebar.error(f"Error: {str(e)}")

    # LLM-Enhanced Schema Analysis section in sidebar
    if st.session_state.get('connected', False):
        st.sidebar.header("LLM Enhanced Schema Analysis")
        st.sidebar.write("Enhance database understanding with LLM-powered semantic analysis.")

        if st.sidebar.button("Run Full Schema Analysis"):
            if st.session_state.get('llm_initialized', False):
                with st.spinner("Analyzing complete database schema with LLM..."):
                    try:
                        schema_info = st.session_state['db_analyzer'].analyze_schema_with_llm()
                        st.session_state['schema_description'] = st.session_state['db_analyzer'].generate_schema_description()
                        st.session_state['schema_for_llm'] = st.session_state['db_analyzer'].generate_schema_for_llm()
                        st.sidebar.success("Schema analysis completed with LLM enhancement!")
                    except Exception as e:
                        st.sidebar.error(f"Error in LLM schema analysis: {str(e)}")
                        st.sidebar.info("Falling back to heuristic analysis...")
                        schema_info = st.session_state['db_analyzer'].analyze_schema_heuristic()
                        st.session_state['schema_description'] = st.session_state['db_analyzer'].generate_schema_description()
                        st.session_state['schema_for_llm'] = st.session_state['db_analyzer'].generate_schema_for_llm()
            else:
                st.sidebar.error("Please initialize the LLM Runtime interface first.")

        # Allow analyzing individual tables
        tables = st.session_state['db_analyzer'].get_tables() if st.session_state.get('db_analyzer') else []
        if tables:
            selected_table = st.sidebar.selectbox("Select a table to enhance", [""] + tables)

            if selected_table and st.sidebar.button(f"Enhance table: {selected_table}"):
                if st.session_state.get('llm_initialized', False):
                    with st.spinner(f"Analyzing table {selected_table} with LLM for enhanced semantics..."):
                        try:
                            table_info = st.session_state['db_analyzer'].analyze_table_with_llm(selected_table)

                            # Update the main schema info with the enhanced table
                            if 'schema_info' in st.session_state:
                                st.session_state['schema_info']['tables'][selected_table] = table_info

                            # Regenerate schema descriptions
                            st.session_state['schema_description'] = st.session_state['db_analyzer'].generate_schema_description()
                            st.session_state['schema_for_llm'] = st.session_state['db_analyzer'].generate_schema_for_llm()

                            st.sidebar.success(f"Enhanced semantic analysis of {selected_table} completed!")
                        except Exception as e:
                            st.sidebar.error(f"Error enhancing table: {str(e)}")
                else:
                    st.sidebar.error("Please initialize the LLM Runtime interface first.")

    # Option to view database schema
    if st.session_state.get('connected', False):
        with st.sidebar.expander("View Database Schema"):
            # Add tabs for different schema views
            schema_tab1, schema_tab2 = st.tabs(["Schema Overview", "Column Semantics"])

            with schema_tab1:
                st.text(st.session_state.get('schema_description', "No schema description available"))

            with schema_tab2:
                # Display column semantics in a more structured format
                if ('db_analyzer' in st.session_state and
                    st.session_state['db_analyzer'] is not None and
                    hasattr(st.session_state['db_analyzer'], 'column_semantics') and
                    st.session_state['db_analyzer'].column_semantics):

                    semantics = st.session_state['db_analyzer'].column_semantics
                    st.subheader("Column Semantics from LLM")

                    # Group semantics by table
                    tables = {}
                    for col_key, meaning in semantics.items():
                        try:
                            table_name, col_name = col_key.split('.')
                            if table_name not in tables:
                                tables[table_name] = []
                            tables[table_name].append((col_name, meaning))
                        except ValueError:
                            # Handle case where col_key doesn't have expected format
                            continue

                    # Create a selectbox to choose which table to view
                    table_names = sorted(tables.keys())
                    if table_names:
                        selected_table = st.selectbox("Select a table", table_names)

                        # Show columns for the selected table
                        if selected_table in tables:
                            st.subheader(f"Table: {selected_table}")
                            columns = tables[selected_table]
                            semantics_df = pd.DataFrame(columns, columns=['Column', 'Semantic Meaning'])
                            st.dataframe(semantics_df)
                    else:
                        st.info("No tables with semantics found.")
                else:
                    st.info("No column semantics available. Connect to a database and analyze the schema first.")

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
            st.info("Initialize the LLM Runtime interface first.")
        elif not st.session_state['connected']:
            st.info("Connect to a database to start asking questions.")

    # Process the question when submitted
    if submit_button and question:
        if not st.session_state['connected'] or not st.session_state['llm_initialized']:
            st.error("Please make sure the LLM Runtime interface is initialized and you're connected to a database.")
        else:
            # Create a container for the results
            results_container = st.container()

            with results_container:
                with st.spinner("Generating SQL query with LLM..."):
                    try:
                        # Generate SQL with LLM using enhanced schema
                        raw_response = asyncio.run(st.session_state['llama_interface'].get_llama_response(
                            f"""
You are an expert SQL query generator for PostgreSQL databases.
Given the database schema below, generate a SQL query to answer the question.

{st.session_state['schema_for_llm']}

Question: {question}

IMPORTANT GUIDELINES:
1. Pay close attention to column semantics and meanings when choosing columns.
2. Distinguish between similar but functionally different columns (e.g., order_date vs. delivery_date vs. dispatch_date).
   - Each date column has a specific business meaning as described in the schema.
   - Always use the date column that most closely matches the business meaning in the question.
3. Use appropriate joins based on the relationships defined in the schema.
4. Ensure data types match when making comparisons.
5. Use table aliases for readability in complex queries.
6. For date/time operations, use appropriate PostgreSQL functions.
7. Use the column semantics to guide your choice of which columns to select, join, and filter on.

Format your response using triple backticks. Place the SQL query inside these backticks like this:
'''sql
SELECT * FROM table WHERE condition;
'''

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
                                with st.spinner("Generating explanation with LLM..."):
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
                                with st.spinner("Analyzing the error with LLM..."):
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

        1. **Initialize the LLM Runtime interface** by providing the host and port of your LLM Runtime API
        2. **Connect to your database** by entering your PostgreSQL credentials
        3. **Ask questions** about your data in plain English
        4. LLM Runtime will generate an SQL query, execute it, and explain the results

        ### Enhanced Column Semantics with LLM

        This improved version uses the LLM to generate detailed semantics for database columns and tables:

        - **Automatic analysis**: When connecting to a database, the tool can use LLM to analyze every column and table
        - **Interactive refinement**: You can enhance specific tables through the "LLM Enhanced Schema Analysis" panel in the sidebar
        - **Context-aware analysis**: The LLM examines relationships between tables, sample data, and column naming patterns

        These LLM-generated semantics provide much more accurate descriptions than pattern-based heuristics alone, enabling:

        - More precise SQL query generation
        - Better understanding of your database structure
        - Clearer explanations of results in business terms

        ### Understanding Column Semantics

        With LLM enhancement, the tool can understand column meanings beyond simple naming patterns:

        - It recognizes domain-specific terminology in your database
        - It understands the relationships between tables and columns
        - It can infer meaning from sample data values
        - It provides business-oriented descriptions rather than technical definitions

        ### Effective Question Tips

        - **Be specific** about what you're looking for
        - **Use business terminology** that matches your data's purpose
        - For questions involving dates, clarify which date you mean (e.g., "Find orders shipped last month but not yet delivered")
        - **Specify time periods** for time-based queries
        - **Include aggregation terms** like "total," "average," or "count" when appropriate

        ### Examples of Good Questions

        - "Show me all orders that were placed in January but not delivered until February"
        - "What is the average time between order placement and dispatch for each product category?"
        - "Which customers have placed orders but never had a delivery completed?"
        - "List the top 5 products by revenue for each month in 2023"
        - "How many customers made their first purchase in 2023 and then made a repeat purchase within 30 days?"
        """)

    # Footer
    st.sidebar.markdown("---")
    st.sidebar.info("""
    **SQL Assistant powered by Power10 MMA with Enhanced Schema Semantics**

    This app connects to your LLM Runtime API service to convert natural
    language questions into SQL queries for PostgreSQL databases.

    The app leverages LLM to generate detailed semantic descriptions of
    your database structure, tables, and columns for improved understanding
    and more accurate query generation.

    Key features:
    - LLM-powered schema analysis for detailed column semantics
    - Table-by-table semantic enhancement
    - Improved natural language understanding of your database

    Make sure your LLM Runtime API service is running and accessible at
    the host and port provided in the settings.
    """)

if __name__ == "__main__":
    main()
