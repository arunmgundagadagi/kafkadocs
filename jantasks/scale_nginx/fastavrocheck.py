import fastavro 
schema = {
    "type": "record",
    "name": "section_A_schema",
    "fields": [
        {"name": "name", "type": {"type": "enum", "name": "NameEnum", "symbols": ["Peter", "Alice", "Bob"]}},
        {"name": "section", "type": "string", "default": "A"},
        {"name": "english", "type": "int"},
        {"name": "math", "type": "int"},
        {"name": "physics", "type": "int"},
        {"name": "chemistry", "type": "int"},
        {"name": "biology", "type": "int"}
    ]
}

record = {
    "name": "Peter",
    "section": "A",
    "english": 6,
    "math": 33,
    "physics": 47,
    "chemistry": 26,
    "biology": 72
}

fastavro.validate(record, schema)
print("Validation Passed!")
