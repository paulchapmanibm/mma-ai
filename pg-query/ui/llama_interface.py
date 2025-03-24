import json
import httpx
import asyncio
import re
from typing import List, Dict, Any

from utils import extract_sql_from_response

class LlamaInterface:
    """Interface for LLM-based natural language to SQL conversion using LLM Runtime API."""

    def __init__(self, host="llama-service", port="8080"):
        """Initialize the LLM Runtime interface with host and port."""
        self.host = host
        self.port = port

    async def get_llama_response(self, prompt):
        """Get a response from the LLM Runtime API."""
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
        """Generate SQL from natural language using LLM Runtime with enhanced schema awareness."""
        prompt = f"""
You are an expert SQL query generator for PostgreSQL databases.
Given the database schema below, generate a SQL query to answer the question.

{schema_description}

Question: {question}

IMPORTANT GUIDELINES:
1. Pay close attention to column semantics and meanings when choosing columns.
2. Distinguish between similar but functionally different columns (e.g., order_date vs. delivery_date vs. dispatch_date).
   - Each date column has a specific business meaning that has been inferred by the LLM and included in the schema.
   - Always use the date column that most closely matches the business meaning in the question.
3. Use appropriate joins based on the relationships defined in the schema.
4. Ensure data types match when making comparisons.
5. Use table aliases for readability in complex queries.
6. For date/time operations, use appropriate PostgreSQL functions.
7. Use the column semantics to guide your choice of:
   - Which columns to select to answer the business question
   - Which tables to join and on which columns
   - Which columns to filter or aggregate

Format your response using triple backticks. Place the SQL query inside these backticks like this:
'''sql
SELECT * FROM table WHERE condition;
'''

Make sure the query inside the backticks is valid PostgreSQL syntax with no comments or additional text.
"""

        sql_query = await self.get_llama_response(prompt)
        return extract_sql_from_response(sql_query)

    def generate_sql(self, question: str, schema_description: str) -> str:
        """Synchronous wrapper for generate_sql_async."""
        return asyncio.run(self.generate_sql_async(question, schema_description))

    async def explain_results_async(self, question: str, sql_query: str, results: List[Dict[str, Any]], error: str = None) -> str:
        """Explain the results in natural language with enhanced semantic awareness."""
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
When explaining the results:
1. Connect column names to their actual business meaning (e.g., "order_date refers to when the order was placed").
2. Distinguish between similar date columns if multiple are used (e.g., "delivery_date represents when the items were delivered to the customer, while dispatch_date shows when they left the warehouse").
3. Be clear about what each number or value represents in business terms.
4. Explain any aggregations or calculations performed.
5. Focus on answering the specific business question that was asked.

Keep your explanation clear, concise, and focused on what the user actually asked.
If the results contain a lot of data, summarize the key points.
"""

        explanation = await self.get_llama_response(prompt)
        return explanation.strip()

    def explain_results(self, question: str, sql_query: str, results: List[Dict[str, Any]], error: str = None) -> str:
        """Synchronous wrapper for explain_results_async."""
        return asyncio.run(self.explain_results_async(question, sql_query, results, error))
