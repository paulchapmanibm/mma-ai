import re
from typing import List, Dict, Any, Optional

def extract_sql_from_response(response: str) -> str:
    """
    Extract SQL query from the LLM response, focusing strictly on the content inside triple backticks.
    If triple backticks are present, extract ONLY the content within them.
    If no triple backticks are found, return an empty string to avoid executing potentially unsafe queries.
    """
    # Look specifically for SQL code blocks with triple backticks
    # The pattern matches ```sql ... ``` or just ``` ... ```
    sql_block_pattern = r'```(?:sql)?(.*?)```'
    matches = re.findall(sql_block_pattern, response, re.DOTALL)

    if matches and len(matches) > 0:
        # Use the first code block found
        sql_query = matches[0].strip()
        return sql_query
    else:
        # Safer to return empty string if no triple backtick block is found
        return ""



def infer_column_semantics_heuristic(table_name: str, column_name: str, data_type: str) -> str:
    """
    Infer the semantic meaning of a column based on its name and type using heuristics.
    This is a fallback method when LLM is not available.
    """
    # Common naming patterns for date/time fields
    date_created_patterns = ['created_at', 'creation_date', 'date_created', 'created_on']
    date_updated_patterns = ['updated_at', 'modification_date', 'date_updated', 'modified_on', 'last_updated']
    date_deleted_patterns = ['deleted_at', 'deletion_date', 'date_deleted', 'removed_on']

    # Common patterns for specific types of dates
    delivery_patterns = ['delivery_date', 'delivered_at', 'date_delivered']
    dispatch_patterns = ['dispatch_date', 'dispatched_at', 'date_dispatched', 'shipped_date', 'shipped_at']
    order_patterns = ['order_date', 'ordered_at', 'date_ordered']
    payment_patterns = ['payment_date', 'paid_at', 'date_paid']

    # Id patterns
    id_patterns = ['_id', 'id', '_key', 'uuid', 'guid']

    # Status patterns
    status_patterns = ['status', 'state', 'condition']

    # Lowercased for case-insensitive matching
    col_lower = column_name.lower()

    # Infer meanings based on patterns
    meaning = ""

    # Date semantics
    if data_type in ('date', 'timestamp', 'timestamptz', 'datetime'):
        if any(pattern in col_lower for pattern in date_created_patterns):
            meaning = "Timestamp when the record was created"
        elif any(pattern in col_lower for pattern in date_updated_patterns):
            meaning = "Timestamp when the record was last updated"
        elif any(pattern in col_lower for pattern in date_deleted_patterns):
            meaning = "Timestamp when the record was deleted (for soft deletes)"
        elif any(pattern in col_lower for pattern in delivery_patterns):
            meaning = "Date when items were actually delivered to the customer"
        elif any(pattern in col_lower for pattern in dispatch_patterns):
            meaning = "Date when items were dispatched from the warehouse/facility"
        elif any(pattern in col_lower for pattern in order_patterns):
            meaning = "Date when the order was placed"
        elif any(pattern in col_lower for pattern in payment_patterns):
            meaning = "Date when payment was received"
        elif 'due' in col_lower:
            meaning = "Due date or deadline"
        elif 'start' in col_lower:
            meaning = "Start date of an event or period"
        elif 'end' in col_lower:
            meaning = "End date of an event or period"

    # Numeric semantics
    elif data_type in ('integer', 'bigint', 'numeric', 'decimal', 'double precision'):
        if 'price' in col_lower or 'cost' in col_lower or 'amount' in col_lower:
            meaning = "Monetary value"
        elif 'quantity' in col_lower or 'count' in col_lower or 'number' in col_lower:
            meaning = "Quantity or count"
        elif 'discount' in col_lower:
            meaning = "Discount value (possibly percentage if between 0-1 or 0-100)"
        elif 'total' in col_lower:
            meaning = "Total calculated value"
        elif any(col_lower.endswith(suffix) for suffix in id_patterns):
            meaning = "Identifier or foreign key"

    # Boolean semantics
    elif data_type == 'boolean':
        if 'is_' in col_lower or 'has_' in col_lower:
            attribute = col_lower.replace('is_', '').replace('has_', '')
            meaning = f"Indicates if the record {attribute}"
        elif 'active' in col_lower or 'enabled' in col_lower:
            meaning = "Indicates if the record is active or enabled"

    # String semantics
    elif data_type in ('character varying', 'varchar', 'text', 'char'):
        if any(pattern in col_lower for pattern in status_patterns):
            meaning = "Status or state of the record"
        elif 'name' in col_lower:
            meaning = "Name or title"
        elif 'description' in col_lower or 'desc' in col_lower:
            meaning = "Descriptive text"
        elif 'code' in col_lower:
            meaning = "Code or identifier"
        elif 'address' in col_lower:
            meaning = "Address information"
        elif 'email' in col_lower:
            meaning = "Email address"
        elif 'phone' in col_lower:
            meaning = "Phone number"

    # If no specific meaning was inferred
    if not meaning:
        if any(col_lower.endswith(suffix) for suffix in id_patterns):
            if col_lower == 'id' or col_lower.endswith('_id'):
                relation = col_lower.replace('_id', '')
                if relation:
                    meaning = f"Identifier for a {relation}"
                else:
                    meaning = "Primary identifier"

    return meaning
