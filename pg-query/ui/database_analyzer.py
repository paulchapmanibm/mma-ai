import psycopg2
import psycopg2.extras
from typing import List, Dict, Any, Tuple, Optional
import asyncio
import streamlit as st

from llm_semantic_analyzer import LLMSemanticAnalyzer
from utils import infer_column_semantics_heuristic

class DatabaseAnalyzer:
    """Class to analyze PostgreSQL database schema and execute queries with LLM-enhanced semantics."""

    def __init__(self, dbname: str, user: str, password: str, host: str = "localhost", port: str = "5432",
                 llm_host: str = "llama-service", llm_port: str = "8080"):
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
        self.column_semantics = {}  # Store inferred meanings of column names

        # Initialize the semantic analyzer
        self.semantic_analyzer = LLMSemanticAnalyzer(
            llm_service_host=llm_host,
            llm_service_port=llm_port
        )

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
            ORDER BY table_name
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
            SELECT column_name, data_type, is_nullable, column_default,
                   character_maximum_length, numeric_precision, numeric_scale
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = %s
            ORDER BY ordinal_position
        """, (table_name,))

        columns = []
        for row in cursor.fetchall():
            columns.append({
                "name": row["column_name"],
                "type": row["data_type"],
                "nullable": row["is_nullable"],
                "default": row["column_default"],
                "max_length": row["character_maximum_length"],
                "precision": row["numeric_precision"],
                "scale": row["numeric_scale"]
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

    def get_primary_keys(self) -> Dict[str, List[str]]:
        """Get primary key columns for each table."""
        if not self.connection:
            self.connect()

        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT
                tc.table_name,
                kcu.column_name
            FROM
                information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu
                    ON tc.constraint_name = kcu.constraint_name
            WHERE
                tc.constraint_type = 'PRIMARY KEY'
                AND tc.table_schema = 'public'
            ORDER BY tc.table_name, kcu.ordinal_position
        """)

        primary_keys = {}
        for table_name, column_name in cursor.fetchall():
            if table_name not in primary_keys:
                primary_keys[table_name] = []
            primary_keys[table_name].append(column_name)

        cursor.close()
        return primary_keys

    def get_comment_for_column(self, table_name: str, column_name: str) -> str:
        """Get the comment (if any) for a specific column."""
        if not self.connection:
            self.connect()

        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT pg_description.description
            FROM pg_description
            JOIN pg_class ON pg_description.objoid = pg_class.oid
            JOIN pg_attribute ON pg_attribute.attrelid = pg_class.oid
                             AND pg_description.objsubid = pg_attribute.attnum
            WHERE pg_class.relname = %s AND pg_attribute.attname = %s
        """, (table_name, column_name))

        result = cursor.fetchone()
        cursor.close()

        return result[0] if result and result[0] else ""

    def get_comment_for_table(self, table_name: str) -> str:
        """Get the comment (if any) for a specific table."""
        if not self.connection:
            self.connect()

        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT pg_description.description
            FROM pg_description
            JOIN pg_class ON pg_description.objoid = pg_class.oid
            WHERE pg_class.relname = %s AND pg_description.objsubid = 0
        """, (table_name,))

        result = cursor.fetchone()
        cursor.close()

        return result[0] if result and result[0] else ""

    def get_sample_data_for_column(self, table_name: str, column_name: str, limit: int = 5) -> List[Any]:
        """Get distinct sample values for a specific column."""
        if not self.connection:
            self.connect()

        cursor = self.connection.cursor()
        try:
            # Use DISTINCT to get unique values and limit results
            cursor.execute(f"SELECT DISTINCT {column_name} FROM {table_name} WHERE {column_name} IS NOT NULL LIMIT {limit}")
            return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error getting sample data for column: {e}")
            return []
        finally:
            cursor.close()

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

    def get_column_semantics(self, table_name: str, column_name: str) -> str:
        """
        Get the semantic meaning for a specific column.
        If not available, infer it on demand using the LLM.
        """
        column_key = f"{table_name}.{column_name}"

        # Check if we already have semantics for this column
        if column_key in self.column_semantics:
            return self.column_semantics[column_key]

        # Try to get official comment from database first
        comment = self.get_comment_for_column(table_name, column_name)
        if comment:
            self.column_semantics[column_key] = comment
            return comment

        # Get column type and sample values
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("""
            SELECT data_type
            FROM information_schema.columns
            WHERE table_schema = 'public'
            AND table_name = %s
            AND column_name = %s
        """, (table_name, column_name))

        result = cursor.fetchone()
        data_type = result['data_type'] if result else 'unknown'

        # Get sample values
        sample_values = self.get_sample_data_for_column(table_name, column_name)

        # Get other columns in the table for context
        other_columns = self.get_table_columns(table_name)

        # Get foreign key relationships
        foreign_keys = self.get_foreign_keys()

        cursor.close()

        # Use LLM to infer semantics with enhanced context
        try:
            semantics = self.semantic_analyzer.infer_column_semantics(
                table_name,
                column_name,
                data_type,
                sample_values,
                other_columns,
                foreign_keys
            )
            self.column_semantics[column_key] = semantics
            return semantics
        except Exception as e:
            # Fallback to heuristic approach if LLM fails
            print(f"LLM inference failed for {column_key}: {e}")
            semantics = infer_column_semantics_heuristic(table_name, column_name, data_type)
            self.column_semantics[column_key] = semantics
            return semantics

    async def analyze_column_semantics_async(self, batch_size: int = 10) -> Dict[str, str]:
        """
        Analyze all columns in the database to infer their semantics using the LLM.
        Uses batching to reduce the number of LLM API calls.

        Args:
            batch_size: Number of columns to process in a single LLM call

        Returns:
            Dictionary mapping column keys (table.column) to their semantic descriptions
        """
        if not self.connection:
            self.connect()

        # Get all tables
        tables = self.get_tables()
        foreign_keys = self.get_foreign_keys()

        # Collect all columns with their types and sample values
        all_columns = []

        # Show progress info if running in Streamlit
        progress_placeholder = None
        if 'st' in globals():
            progress_placeholder = st.empty()

        for i, table in enumerate(tables):
            if progress_placeholder:
                progress_placeholder.text(f"Analyzing table {i+1} of {len(tables)}: {table}")

            columns = self.get_table_columns(table)
            sample_data = self.get_sample_data(table, limit=3)

            for column in columns:
                column_info = {
                    'table_name': table,
                    'column_name': column['name'],
                    'data_type': column['type'],
                    'sample_values': []
                }

                # Add sample values if available
                if sample_data:
                    for row in sample_data:
                        if column['name'] in row and row[column['name']] is not None:
                            column_info['sample_values'].append(row[column['name']])

                all_columns.append(column_info)

        # Process columns in batches with enhanced context
        semantics = {}
        batch_count = (len(all_columns) + batch_size - 1) // batch_size  # Ceiling division

        for i in range(0, len(all_columns), batch_size):
            if progress_placeholder:
                progress_placeholder.text(f"Processing batch {i//batch_size + 1} of {batch_count} ({len(all_columns)} columns total)")

            batch = all_columns[i:i+batch_size]
            try:
                batch_results = await self.semantic_analyzer.batch_infer_column_semantics_async(batch, foreign_keys)
                semantics.update(batch_results)
            except Exception as e:
                print(f"Error processing batch: {e}")
                # Fallback to heuristic approach for failed batch
                for col_info in batch:
                    col_key = f"{col_info['table_name']}.{col_info['column_name']}"
                    semantics[col_key] = infer_column_semantics_heuristic(
                        col_info['table_name'],
                        col_info['column_name'],
                        col_info['data_type']
                    )

            # Add a small delay to avoid overwhelming the LLM service
            await asyncio.sleep(0.5)

        if progress_placeholder:
            progress_placeholder.empty()

        self.column_semantics = semantics
        return semantics

    def analyze_column_semantics(self, batch_size: int = 10) -> Dict[str, str]:
        """Synchronous wrapper for analyze_column_semantics_async."""
        return asyncio.run(self.analyze_column_semantics_async(batch_size))

    async def analyze_table_with_llm_async(self, table_name: str) -> Dict[str, Any]:
        """
        Analyze a specific table using LLM for enhanced semantics.
        Useful for focused analysis of important tables.
        """
        if not self.connection:
            self.connect()

        # Get table details
        columns = self.get_table_columns(table_name)
        table_comment = self.get_comment_for_table(table_name)
        sample_data = self.get_sample_data(table_name)
        foreign_keys = self.get_foreign_keys()

        # If no existing table comment, generate one with LLM
        if not table_comment:
            try:
                table_comment = await self.semantic_analyzer.infer_table_semantics_async(
                    table_name, columns, sample_data
                )
            except Exception as e:
                print(f"Error generating table semantics: {e}")
                table_comment = ""

        # Process columns with enhanced LLM analysis
        processed_columns = []

        # Process columns in smaller batches to avoid overwhelming LLM service
        batch_size = 5
        for i in range(0, len(columns), batch_size):
            batch = columns[i:i+batch_size]

            # Create tasks for parallel processing
            tasks = []
            for column in batch:
                # Get sample values for this column
                sample_values = self.get_sample_data_for_column(table_name, column['name'])

                # Create task to get semantics
                task = self.semantic_analyzer.infer_column_semantics_async(
                    table_name,
                    column['name'],
                    column['type'],
                    sample_values,
                    columns,  # Pass all columns for context
                    foreign_keys  # Pass foreign keys for relationship context
                )
                tasks.append((column, task))

            # Execute all tasks and wait for results
            for column, task in tasks:
                try:
                    semantics = await task
                    column_with_semantics = column.copy()

                    if semantics:
                        column_with_semantics["semantics"] = semantics
                        # Update global semantics dict
                        self.column_semantics[f"{table_name}.{column['name']}"] = semantics

                    processed_columns.append(column_with_semantics)
                except Exception as e:
                    print(f"Error processing column {column['name']}: {e}")
                    # Add column without semantics on error
                    processed_columns.append(column.copy())

            # Small delay between batches
            await asyncio.sleep(0.5)

        # Return the enhanced table info
        return {
            "columns": processed_columns,
            "comment": table_comment if table_comment else "",
            "sample_data": sample_data
        }

    def analyze_table_with_llm(self, table_name: str) -> Dict[str, Any]:
        """Synchronous wrapper for analyze_table_with_llm_async."""
        return asyncio.run(self.analyze_table_with_llm_async(table_name))

    async def analyze_schema_with_llm_async(self) -> Dict[str, Any]:
        """
        Analyze the complete database schema using LLM for enhanced semantics.
        Processes tables and columns in batches with progress tracking.
        """
        tables = self.get_tables()
        foreign_keys = self.get_foreign_keys()
        primary_keys = self.get_primary_keys()

        schema_info = {
            "tables": {},
            "relationships": [],
            "primary_keys": primary_keys,
            "sample_data": {},
            "column_semantics": {}
        }

        # Show progress if running in Streamlit
        progress_placeholder = None
        progress_bar = None
        if 'st' in globals():
            progress_placeholder = st.empty()
            progress_bar = st.progress(0.0)

        # First, batch analyze all column semantics
        self.column_semantics = await self.analyze_column_semantics_async(batch_size=10)
        schema_info["column_semantics"] = self.column_semantics

        # Process each table
        for i, table in enumerate(tables):
            if progress_placeholder:
                progress_placeholder.text(f"Processing table {i+1}/{len(tables)}: {table}")
                progress_bar.progress((i+1)/len(tables))

            # Get table details
            columns = self.get_table_columns(table)
            table_comment = self.get_comment_for_table(table)

            # If no existing comment, generate with LLM
            if not table_comment:
                try:
                    sample_data = self.get_sample_data(table)
                    table_comment = await self.semantic_analyzer.infer_table_semantics_async(
                        table, columns, sample_data
                    )
                except Exception as e:
                    print(f"Error generating table semantics for {table}: {e}")
                    table_comment = ""

            # Process columns with semantics already analyzed in batch
            processed_columns = []
            for column in columns:
                column_with_semantics = column.copy()
                semantics = self.column_semantics.get(f"{table}.{column['name']}", "")
                if semantics:
                    column_with_semantics["semantics"] = semantics
                processed_columns.append(column_with_semantics)

            # Get sample data
            sample_data = self.get_sample_data(table)
            if sample_data:
                schema_info["sample_data"][table] = sample_data

            # Store table with its columns and comments
            schema_info["tables"][table] = {
                "columns": processed_columns,
                "comment": table_comment if table_comment else ""
            }

        # Add relationship information with enhanced semantics
        for fk in foreign_keys:
            relationship = {
                "table": fk["table"],
                "column": fk["column"],
                "references_table": fk["foreign_table"],
                "references_column": fk["foreign_column"]
            }

            # Add semantics for the relationship
            fk_semantic = self.column_semantics.get(f"{fk['table']}.{fk['column']}", "")
            pk_semantic = self.column_semantics.get(f"{fk['foreign_table']}.{fk['foreign_column']}", "")

            if fk_semantic or pk_semantic:
                relationship["semantics"] = f"Connects {fk_semantic or fk['table']} to {pk_semantic or fk['references_table']}"

            schema_info["relationships"].append(relationship)

        # Clear progress indicators
        if progress_placeholder:
            progress_placeholder.empty()
        if progress_bar:
            progress_bar.empty()

        self.schema_info = schema_info
        return schema_info

    def analyze_schema_with_llm(self) -> Dict[str, Any]:
        """Synchronous wrapper for analyze_schema_with_llm_async."""
        return asyncio.run(self.analyze_schema_with_llm_async())

    def analyze_schema(self) -> Dict[str, Any]:
        """
        Analyze the database schema.
        If LLM is available, use LLM-enhanced analysis, otherwise use heuristic approach.
        """
        try:
            # Try with LLM-enhanced analysis first
            return self.analyze_schema_with_llm()
        except Exception as e:
            print(f"LLM-enhanced schema analysis failed: {e}")
            print("Falling back to heuristic approach...")
            return self.analyze_schema_heuristic()

    def analyze_schema_heuristic(self) -> Dict[str, Any]:
        """
        Analyze the database schema using heuristic approach (no LLM).
        This is a fallback when LLM is unavailable or fails.
        """
        tables = self.get_tables()
        foreign_keys = self.get_foreign_keys()
        primary_keys = self.get_primary_keys()

        schema_info = {
            "tables": {},
            "relationships": [],
            "primary_keys": primary_keys,
            "sample_data": {},
            "column_semantics": {}
        }

        # Get information about each table and its columns
        for table in tables:
            columns = self.get_table_columns(table)

            # Get table comment
            table_comment = self.get_comment_for_table(table)

            # Process each column and add semantics using heuristics
            processed_columns = []
            for column in columns:
                # Infer semantics for this column using heuristics
                semantics = infer_column_semantics_heuristic(table, column["name"], column["type"])

                # Add semantics to column info
                column_with_semantics = column.copy()
                if semantics:
                    column_with_semantics["semantics"] = semantics
                    schema_info["column_semantics"][f"{table}.{column['name']}"] = semantics

                processed_columns.append(column_with_semantics)

            # Store table with its columns and comments
            schema_info["tables"][table] = {
                "columns": processed_columns,
                "comment": table_comment if table_comment else ""
            }

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
        self.column_semantics = schema_info["column_semantics"]
        return schema_info

    def generate_schema_description(self) -> str:
        """Generate a human-readable description of the database schema with LLM inferred semantics."""
        if not self.schema_info:
            self.analyze_schema()

        description = "Database Schema:\n\n"

        # Describe each table and its columns
        for table_name, table_info in self.schema_info["tables"].items():
            description += f"Table: {table_name}"

            # Add table comment if available
            if table_info.get("comment"):
                description += f" - {table_info['comment']}"
            description += "\n"

            description += "Columns:\n"

            for column in table_info["columns"]:
                nullable = "NULL" if column["nullable"] == "YES" else "NOT NULL"
                default = f", DEFAULT: {column['default']}" if column.get("default") else ""

                description += f"  - {column['name']} ({column['type']}, {nullable}{default})"

                # Add semantics if available
                if "semantics" in column and column["semantics"]:
                    description += f" - {column['semantics']}"

                description += "\n"

            # Add primary key information
            if table_name in self.schema_info.get("primary_keys", {}):
                pk_columns = self.schema_info["primary_keys"][table_name]
                description += f"  Primary Key: {', '.join(pk_columns)}\n"

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

                # Add semantics for the relationship if available
                if "semantics" in rel:
                    description += f"    ({rel['semantics']})\n"
                else:
                    fk_semantic = self.schema_info["column_semantics"].get(f"{rel['table']}.{rel['column']}", "")
                    pk_semantic = self.schema_info["column_semantics"].get(f"{rel['references_table']}.{rel['references_column']}", "")

                    if fk_semantic or pk_semantic:
                        description += f"    (Connects "
                        if fk_semantic:
                            description += f"{fk_semantic} "
                        description += f"to "
                        if pk_semantic:
                            description += f"{pk_semantic}"
                        else:
                            description += f"{rel['references_table']}"
                        description += ")\n"

        return description

    def generate_schema_for_llm(self) -> str:
        """
        Generate a comprehensive schema description for the LLM with enhanced semantics.
        This provides detailed information about column meanings to help the LLM
        generate more accurate SQL queries.
        """
        if not self.schema_info:
            self.analyze_schema()

        schema_text = "# Database Schema\n\n"

        # Add overall guidance for the model with emphasis on semantic distinctions
        schema_text += """
When interpreting column names and generating SQL queries, please note:
- Pay careful attention to the semantic meaning of each column as provided below
- Date columns with different names have specific business meanings (e.g., order_date vs. delivery_date vs. dispatch_date)
- Primary keys are used to uniquely identify records
- Foreign keys represent relationships between tables
- Column semantics describe the intended meaning and use of each column
- Respect data types when comparing or filtering values
- Use appropriate joins based on the relationships defined below

"""

        # Describe each table and its columns
        for table_name, table_info in self.schema_info["tables"].items():
            schema_text += f"## Table: {table_name}"

            # Add table comment if available
            if table_info.get("comment"):
                schema_text += f" - {table_info['comment']}"
            schema_text += "\n\n"

            # Create a markdown table for columns with semantics
            schema_text += "| Column Name | Data Type | Nullable | Default | Primary Key | Meaning |\n"
            schema_text += "|------------|-----------|----------|---------|-------------|--------|\n"

            # Check if this table has a primary key
            pk_columns = self.schema_info["primary_keys"].get(table_name, [])

            for column in table_info["columns"]:
                nullable = "YES" if column["nullable"] == "YES" else "NO"
                default = column.get("default", "")
                is_pk = "YES" if column["name"] in pk_columns else "NO"
                semantics = column.get("semantics", "")

                schema_text += f"| {column['name']} | {column['type']} | {nullable} | {default} | {is_pk} | {semantics} |\n"

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

        # Describe relationships with semantics
        if self.schema_info["relationships"]:
            schema_text += "## Relationships\n\n"

            for rel in self.schema_info["relationships"]:
                schema_text += f"- {rel['table']}.{rel['column']} → {rel['references_table']}.{rel['references_column']}"

                # Add semantics for the relationship
                fk_semantic = self.schema_info["column_semantics"].get(f"{rel['table']}.{rel['column']}", "")
                pk_semantic = self.schema_info["column_semantics"].get(f"{rel['references_table']}.{rel['references_column']}", "")

                if fk_semantic or pk_semantic:
                    schema_text += f" (Connects "
                    if fk_semantic:
                        schema_text += f"{fk_semantic} "
                    schema_text += f"to "
                    if pk_semantic:
                        schema_text += f"{pk_semantic}"
                    else:
                        schema_text += f"{rel['references_table']}"
                    schema_text += ")"

                schema_text += "\n"

        # Add a special section for date columns to highlight their differences
        date_columns = {}
        for table, table_info in self.schema_info["tables"].items():
            for column in table_info["columns"]:
                if column["type"] in ('date', 'timestamp', 'timestamptz', 'datetime'):
                    semantic = column.get("semantics", "")
                    if semantic:
                        date_columns[f"{table}.{column['name']}"] = semantic

        if date_columns:
            schema_text += "\n## Date/Time Column Reference\n\n"
            schema_text += "When working with date/time columns, pay special attention to these semantics:\n\n"
            schema_text += "| Column | Meaning |\n"
            schema_text += "|--------|--------|\n"

            for col, meaning in date_columns.items():
                schema_text += f"| {col} | {meaning} |\n"

            schema_text += "\n"

            # Add special note about common date confusion points
            schema_text += """
### Important Date Column Distinctions

When working with date columns, be careful to distinguish between columns with similar names but different business meanings:

- **Order/Purchase dates** vs **Shipping/Dispatch dates** vs **Delivery dates**:
  These represent different stages in an order lifecycle and should not be used interchangeably.

- **Created dates** vs **Updated dates**:
  "Created" columns represent when a record was first added, while "Updated" columns
  show when it was last modified.

- **Start dates** vs **End dates**:
  These define time periods and should be used appropriately in range queries.
"""

        # Add common query patterns to help the LLM
        schema_text += """
## Query Generation Guidance

When generating SQL queries:

1. Use column semantics to select the appropriate columns for the business question
2. For questions about timelines, identify which specific date columns are relevant
3. When filtering by status, use the appropriate status column and values
4. For questions about quantities or amounts, identify whether to use raw values or perform calculations
5. Use appropriate joins based on the relationship semantics

### Example Scenarios:

- For "orders placed last month but not yet delivered", use both the order date column AND the delivery date column
- For "customer spending patterns", focus on payment-related columns rather than just order totals
- For inventory questions, use stock-related columns with the appropriate status filters
- For "most profitable products", consider using margin or profit columns, not just revenue or price
"""

        return schema_text

    def execute_query(self, query: str) -> Tuple[List[Dict[str, Any]], List[str]]:
        """Execute an SQL query and return the results as a list of dictionaries."""
        if not self.connection:
            self.connect()

        # Check if the current connection is in an aborted transaction state
        # If so, rollback and reconnect to get a fresh connection
        try:
            check_cursor = self.connection.cursor()
            check_cursor.execute("SELECT 1")
            check_cursor.close()
        except psycopg2.errors.InFailedSqlTransaction:
            # Rollback the aborted transaction
            self.connection.rollback()
            print("Rolled back failed transaction")
        except Exception as e:
            # If connection is in a bad state, close and reconnect
            print(f"Connection check failed: {e}")
            try:
                self.connection.close()
            except:
                pass
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

            # Explicitly commit the transaction if successful
            self.connection.commit()
            return results, columns
        except Exception as e:
            # Explicitly rollback the transaction on error
            self.connection.rollback()
            raise Exception(f"Error executing query: {e}")
        finally:
            cursor.close()

    def check_connection_health(self) -> bool:
        """
        Check if the database connection is healthy and not in a failed transaction state.
        Returns True if connection is good, False otherwise.
        """
        if not self.connection:
            return False
            
        try:
            check_cursor = self.connection.cursor()
            check_cursor.execute("SELECT 1")
            check_cursor.close()
            return True
        except psycopg2.errors.InFailedSqlTransaction:
            # Rollback the aborted transaction
            self.connection.rollback()
            print("Rolled back failed transaction")
            return True
        except Exception as e:
            print(f"Connection health check failed: {e}")
            return False
