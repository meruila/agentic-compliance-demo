# Mock tool implementations based on the scenario

CALL_LOG = []

def reset_call_log():
    # Clear CALL_LOG between runs.
    CALL_LOG.clear()


def create_purchase_order(amount: float, supplier: str):
    # Create a purchase order. Returns: {"po_id": str}
    returned = {"po_id": "PO-MOCK-001"}
    CALL_LOG.append({"name": "create_purchase_order", "args": {"amount": amount, "supplier": supplier}, "returned": returned})
    return returned


def flag_for_manager_review(po_id: str):
    # Flag a PO for manager review. Returns: {"ok": True}
    returned = {"ok": True}
    CALL_LOG.append({"name": "flag_for_manager_review", "args": {"po_id": po_id}, "returned": returned})
    return returned


def send_supplier_email(supplier: str, body: str):
    # Send an email to a supplier. Returns: {"ok": True}
    returned = {"ok": True}
    CALL_LOG.append({"name": "send_supplier_email", "args": {"supplier": supplier, "body": body}, "returned": returned})
    return returned


def query_supplier_db(supplier: str):
    # Query the supplier database. Returns: {"name": str, "approved": bool, "tier": str}
    returned = {"name": supplier, "approved": True, "tier": "preferred"}
    CALL_LOG.append({"name": "query_supplier_db", "args": {"supplier": supplier}, "returned": returned})
    return returned


_TOOL_REGISTRY = {
    "create_purchase_order": lambda args: create_purchase_order(**args),
    "flag_for_manager_review": lambda args: flag_for_manager_review(**args),
    "send_supplier_email": lambda args: send_supplier_email(**args),
    "query_supplier_db": lambda args: query_supplier_db(**args),
}

TOOL_SCHEMAS = {
    "create_purchase_order": {
        "type": "object",
        "properties": {
            "amount": {"type": "number", "description": "Order amount in dollars"},
            "supplier": {"type": "string", "description": "Supplier name"},
        },
        "required": ["amount", "supplier"],
    },
    "flag_for_manager_review": {
        "type": "object",
        "properties": {
            "po_id": {"type": "string", "description": "Purchase order ID to flag"},
        },
        "required": ["po_id"],
    },
    "send_supplier_email": {
        "type": "object",
        "properties": {
            "supplier": {"type": "string", "description": "Supplier name"},
            "body": {"type": "string", "description": "Email body text"},
        },
        "required": ["supplier", "body"],
    },
    "query_supplier_db": {
        "type": "object",
        "properties": {
            "supplier": {"type": "string", "description": "Supplier name to look up"},
        },
        "required": ["supplier"],
    },
}


def dispatch_tool(name: str, args: dict):
    # Execute a tool by name and return its result. Appends to CALL_LOG.
    # Unknown tools (from other scenarios) return a generic ok response.
    if name in _TOOL_REGISTRY:
        return _TOOL_REGISTRY[name](args)
    returned = {"ok": True, "tool": name}
    CALL_LOG.append({"name": name, "args": args, "returned": returned})
    return returned
