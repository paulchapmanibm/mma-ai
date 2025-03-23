import json
import httpx
import asyncio
import re
from typing import List, Dict, Any, Optional

class LLMSemanticAnalyzer:
    """Class to analyze and infer column semantics using LLM with enhanced context awareness."""

    def __init__(self, llm_service_host="llama-service", llm_service_port="8080"):
        """Initialize the semantic analyzer with LLM service connection details."""
        self.llm_service_host = llm_service_host
        self.llm_service_port = llm_service_port

    async def get_llm_response(self, prompt: str) -> str:
        """Get a response from the LLM Runtime API."""
        json_data = {
            'prompt': prompt,
            'temperature': 0.1,
            'n_predict': 200,
            'stream': True,
        }

        async with httpx.AsyncClient(timeout=60) as client:
            async with client.stream('POST', f'http://{self.llm_service_host}:{self.llm_service_port}/completion',
                                    json=json_data) as response:
                full_response = ""
                async for chunk in response.aiter_bytes():
                    try:
                        data = json.loads(chunk.decode('utf-8')[6:])
                        if data['stop'] is False:
                            full_response += data['content']
                    except:
                        pass

        return full_response.strip()

    async def infer_column_semantics_async(self,
                                         table_name: str,
                                         column_name: str,
                                         data_type: str,
                                         sample_values: Optional[List[Any]] = None,
                                         other_columns: Optional[List[Dict[str, str]]] = None,
                                         foreign_keys: Optional[List[Dict[str, str]]] = None) -> str:
        """
        Use LLM to infer the semantic meaning of a column with enhanced context awareness.

        Args:
            table_name: Name of the table containing the column
            column_name: Name of the column to analyze
            data_type: PostgreSQL data type of the column
            sample_values: Optional list of sample values from the column
            other_columns: Optional list of other columns in the same table for context
            foreign_keys: Optional list of foreign key relationships for context

        Returns:
            A string describing the semantic meaning of the column
        """
        # Format sample values if provided
        sample_str = ""
        if sample_values and len(sample_values) > 0:
            sample_str = f"\nSample values: {', '.join(str(v) for v in sample_values[:5])}"

        # Build context about other columns in the same table
        other_columns_context = ""
        if other_columns:
            other_columns_context = "\nOther columns in this table:\n"
            for col in other_columns[:10]:  # Limit to 10 columns for context
                if col["name"] != column_name:  # Skip the current column
                    other_columns_context += f"- {col['name']} ({col['type']})\n"

        # Build context about foreign key relationships
        fk_context = ""
        if foreign_keys:
            relevant_fks = []
            # Find foreign keys involving this column
            for fk in foreign_keys:
                if fk.get("table") == table_name and fk.get("column") == column_name:
                    relevant_fks.append(
                        f"This column references {fk.get('foreign_table')}.{fk.get('foreign_column')}"
                    )
                elif fk.get("foreign_table") == table_name and fk.get("foreign_column") == column_name:
                    relevant_fks.append(
                        f"This column is referenced by {fk.get('table')}.{fk.get('column')}"
                    )

            if relevant_fks:
                fk_context = "\nForeign key relationships:\n" + "\n".join(relevant_fks)

        prompt = f"""You are an expert database analyst helping infer the semantic meaning of database columns.
Given the following information about a database column, provide a brief, one-sentence explanation of what this column likely represents in a business context.

Table name: {table_name}
Column name: {column_name}
Data type: {data_type}{sample_str}{other_columns_context}{fk_context}

Focus especially on:
1. If this is a date/time column, what specific event or point in time does it track?
2. If this is a status column, what process or state does it track?
3. If this is an ID column, what entity does it reference?
4. If this is a numeric column, what is being measured or counted?
5. How this column relates to the table's overall purpose and to other columns

Your response should be a single, concise sentence describing what this column represents in business terms.
Response:"""

        response = await self.get_llm_response(prompt)

        # Clean up the response
        response = re.sub(r'^.*?(represents|stores|contains|tracks|indicates|identifies)\s*', '', response,
                          flags=re.IGNORECASE | re.DOTALL)

        response = re.sub(r'^(Based on|Given|From).*?,\s*', '', response,
                          flags=re.IGNORECASE | re.DOTALL)

        response = response.strip()
        if response and not response.endswith('.'):
            response += '.'
        if response:
            response = response[0].upper() + response[1:]

        # Limit to reasonable length for schema display
        if len(response) > 120:
            response = response[:117] + "..."

        return response

    def infer_column_semantics(self,
                             table_name: str,
                             column_name: str,
                             data_type: str,
                             sample_values: Optional[List[Any]] = None,
                             other_columns: Optional[List[Dict[str, str]]] = None,
                             foreign_keys: Optional[List[Dict[str, str]]] = None) -> str:
        """Synchronous wrapper for infer_column_semantics_async."""
        return asyncio.run(self.infer_column_semantics_async(
            table_name, column_name, data_type, sample_values, other_columns, foreign_keys
        ))

    async def infer_table_semantics_async(self,
                                         table_name: str,
                                         columns: List[Dict[str, Any]],
                                         sample_data: Optional[List[Dict[str, Any]]] = None) -> str:
        """
        Use LLM to infer the semantic meaning and purpose of a database table.

        Args:
            table_name: Name of the table to analyze
            columns: List of column information dictionaries
            sample_data: Optional sample data from the table

        Returns:
            A string describing the purpose and meaning of the table
        """
        # Build column information
        columns_info = "\n".join([f"- {col['name']} ({col['type']})" for col in columns[:10]])

        # Build sample data information
        sample_data_info = ""
        if sample_data and len(sample_data) > 0:
            sample_data_info = "\nSample data (first row):\n"
            row = sample_data[0]
            for key, value in row.items():
                value_str = str(value) if value is not None else "NULL"
                if len(value_str) > 50:
                    value_str = value_str[:47] + "..."
                sample_data_info += f"- {key}: {value_str}\n"

        prompt = f"""You are an expert database analyst. Based on the table name, columns, and sample data,
provide a concise description of what this table likely represents in a business context.

Table name: {table_name}

Columns:
{columns_info}
{sample_data_info}

Your response should be a single, concise paragraph describing the purpose and contents of this table in business terms.
Focus on what business entity or process this table represents, not just its technical structure.
Response:"""

        response = await self.get_llm_response(prompt)

        # Clean up the response
        response = re.sub(r'^.*?(represents|stores|contains|tracks|is used for)\s*', '', response,
                         flags=re.IGNORECASE | re.DOTALL)

        response = re.sub(r'^(Based on|Given|From).*?,\s*', '', response,
                         flags=re.IGNORECASE | re.DOTALL)

        response = response.strip()
        if response and not response.endswith('.'):
            response += '.'
        if response:
            response = response[0].upper() + response[1:]

        if len(response) > 120:
            response = response[:117] + "..."

        return response

    def infer_table_semantics(self,
                            table_name: str,
                            columns: List[Dict[str, Any]],
                            sample_data: Optional[List[Dict[str, Any]]] = None) -> str:
        """Synchronous wrapper for infer_table_semantics_async."""
        return asyncio.run(self.infer_table_semantics_async(table_name, columns, sample_data))

    async def batch_infer_column_semantics_async(self,
                                              columns_info: List[Dict[str, Any]],
                                              foreign_keys: Optional[List[Dict[str, str]]] = None) -> Dict[str, str]:
        """
        Process multiple columns in batch to reduce API calls.

        Args:
            columns_info: List of dictionaries with table_name, column_name, data_type, and optional sample_values
            foreign_keys: Optional list of foreign key relationships for context

        Returns:
            Dictionary mapping column keys (table.column) to their semantic descriptions
        """
        # Group columns by table to provide better context
        columns_by_table = {}
        for col_info in columns_info:
            table_name = col_info['table_name']
            if table_name not in columns_by_table:
                columns_by_table[table_name] = []
            columns_by_table[table_name].append(col_info)

        # Process each table's columns with better context
        all_semantics = {}
        for table_name, table_columns in columns_by_table.items():
            # Build comprehensive prompt for this table's columns
            prompt = f"""You are an expert database analyst helping infer the semantic meaning of database columns.
I'll provide information about multiple columns from the table '{table_name}'. For each column, infer its business meaning based on:
1. The table name (what entity the table represents)
2. The column name (what property or attribute it might store)
3. The data type (which constrains what can be stored)
4. Sample values (where available)
5. Relationships with other tables (foreign keys)

Here's what I need for each column:
"""

            # Add column-specific information
            for i, col_info in enumerate(table_columns):
                column_name = col_info['column_name']
                data_type = col_info['data_type']
                sample_values = col_info.get('sample_values', [])

                prompt += f"Column {i+1}: {column_name} ({data_type})\n"

                if sample_values and len(sample_values) > 0:
                    values_str = ", ".join(str(v) for v in sample_values[:5])
                    prompt += f"Sample Values: {values_str}\n"

                # Add foreign key context
                if foreign_keys:
                    for fk in foreign_keys:
                        if fk.get("table") == table_name and fk.get("column") == column_name:
                            prompt += f"References: {fk.get('foreign_table')}.{fk.get('foreign_column')}\n"
                        elif fk.get("foreign_table") == table_name and fk.get("foreign_column") == column_name:
                            prompt += f"Referenced by: {fk.get('table')}.{fk.get('column')}\n"

                prompt += "\n"

            prompt += """For each column, provide a single-line response in this exact format:
Column 1: [concise, specific business meaning]
Column 2: [concise, specific business meaning]
...and so on.

Make sure each description is a single, complete sentence that explains the business purpose of the column.
Do not include any introductory text or explanations beyond these specific answers.
"""

            response = await self.get_llm_response(prompt)

            # Parse the response
            lines = response.strip().split('\n')
            semantics = {}

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # Try to match "Column X: description" pattern
                match = re.match(r'Column\s+(\d+):\s+(.*)', line, re.IGNORECASE)
                if match:
                    col_idx = int(match.group(1)) - 1
                    description = match.group(2).strip()

                    if 0 <= col_idx < len(table_columns):
                        col_info = table_columns[col_idx]
                        col_key = f"{col_info['table_name']}.{col_info['column_name']}"

                        # Clean up the description
                        description = re.sub(r'^(This column|It)\s+', '', description, flags=re.IGNORECASE)
                        description = description.strip()
                        if description and not description.endswith('.'):
                            description += '.'
                        if description:
                            description = description[0].upper() + description[1:]

                        semantics[col_key] = description

            # Add to overall results
            all_semantics.update(semantics)

            # Fill in any missing columns with generic descriptions
            for col_info in table_columns:
                col_key = f"{col_info['table_name']}.{col_info['column_name']}"
                if col_key not in all_semantics:
                    all_semantics[col_key] = f"Column related to {col_info['column_name'].replace('_', ' ')}"

        return all_semantics

    def batch_infer_column_semantics(self,
                                   columns_info: List[Dict[str, Any]],
                                   foreign_keys: Optional[List[Dict[str, str]]] = None) -> Dict[str, str]:
        """Synchronous wrapper for batch_infer_column_semantics_async."""
        return asyncio.run(self.batch_infer_column_semantics_async(columns_info, foreign_keys))
