import json
from openai import OpenAI
import ast
import re
import prompts as p
import streamlit as st


# Load API key
client = OpenAI(api_key="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")

# Entity functions
def expand_entity_list(text, entity_list, topic):
    print("expand entity")

    # increase = input("please insert an input between 0 and 100: ")
    increase = 20
    # expand the list
    prompt = p.expansion_entities(text, entity_list, topic, increase)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You expand an entity list extracted from a text based on a specific topic from a textbook used in secondary education. Return only a valid Python dictionary as JSON, and do NOT wrap the result in code blocks. Return in this format: 'entities: []'"},
            {"role": "user", "content": prompt}
        ],
        temperature=0, # Makes it not random, but very predictable
    )

    # Extract the string content from the response object properly
    content = response.choices[0].message.content

    # Strip the ```python ... ``` block if present
    if content.startswith("```python"):
        content = content.strip("```python").strip("```").strip()

    # Now safely load as a Python dictionary
    try:
        result_dict = json.loads(content)
    except json.JSONDecodeError as e:
        print("Failed to parse GPT output. Raw content:")
        print(content)
        raise e

    print(result_dict)
    return list(set(result_dict['entities']))


def contract_entity_list(text, entity_list, topic):
    print("contract entity")

    # decrease = input("please insert an input between 0 and 100: ")
    decrease = 20
    # expand the list
    prompt = p.contraction_entities(text, entity_list, topic, decrease)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You contract an entity list extracted from a text based on a specific topic from a textbook used in secondary education. Return only a valid Python dictionary as JSON, and do NOT wrap the result in code blocks. Return in this format: 'entities: []'"},
            {"role": "user", "content": prompt}
        ],
        temperature=0, # Makes it not random, but very predictable
    )

    # Extract the string content from the response object properly
    content = response.choices[0].message.content

    # Strip the ```python ... ``` block if present
    if content.startswith("```python"):
        content = content.strip("```python").strip("```").strip()

    # Now safely load as a Python dictionary
    try:
        result_dict = json.loads(content)
    except json.JSONDecodeError as e:
        print("Failed to parse GPT output. Raw content:")
        print(content)
        raise e

    print(result_dict)
    return list(set(result_dict['entities']))


def add_entities(entity_list, new_entities_input):
    print("add entity")

    # new_entities_input = input("Please insert the entities you would like to add seperated by a comma: ")

    new_entities = new_entities_input.lower().split(",")

    return list(set(entity_list + new_entities))


def remove_entities(entity_list, remove_entities_input):
    print("remove entity")
    st.write("in function")

    # remove_entities_input = input("Please insert the entities you would like to remove seperated by a comma: ")

    remove_entities = remove_entities_input.lower().split(",")

    not_removed = []

    for entity in remove_entities:
        
        if entity in entity_list:
            entity_list.remove(entity)
        else:
            not_removed.append(entity)

    print(f"These entities are not removed, since they are misspelled or not in the list: {not_removed}")
    return entity_list



#Quantity functions


def expand_quantity_list(text, entity_list, quantity_list, topic):
    print("expand quantity")

    # increase = input("please insert an input between 0 and 100: ")
    increase = 20
    # expand the list
    prompt = p.expansion_quantities(text, entity_list, quantity_list, topic, increase)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You expand an quantity list extracted where the quantities are identified from an entity list based on a provided entry in a textbook used in secondary education. Return only a valid Python dictionary as JSON, and do NOT wrap the result in code blocks. Return in this format: 'quantities: []'"},
            {"role": "user", "content": prompt}
        ],
        temperature=0, # Makes it not random, but very predictable
    )

    # Extract the string content from the response object properly
    content = response.choices[0].message.content

    # Strip the ```python ... ``` block if present
    if content.startswith("```python"):
        content = content.strip("```python").strip("```").strip()

    # Now safely load as a Python dictionary
    try:
        result_dict = json.loads(content)
    except json.JSONDecodeError as e:
        print("Failed to parse GPT output. Raw content:")
        print(content)
        raise e
    print(result_dict)
    return list(set(result_dict['quantities']))


def contract_quantity_list(text, entity_list, quantity_list, topic):
    print("contract quantity")

    # decrease = input("please insert an input between 0 and 100: ")
    decrease = 20
    # expand the list
    prompt = p.contraction_quantities(text, entity_list, quantity_list, topic, decrease)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You contract an quantity list extracted where the quantities are identified from an entity list based on a provided entry in a textbook used in secondary education. Return only a valid Python dictionary as JSON, and do NOT wrap the result in code blocks. Return in this format: 'quantities: []'"},
            {"role": "user", "content": prompt}
        ],
        temperature=0, # Makes it not random, but very predictable
    )

    # Extract the string content from the response object properly
    content = response.choices[0].message.content

    # Strip the ```python ... ``` block if present
    if content.startswith("```python"):
        content = content.strip("```python").strip("```").strip()

    # Now safely load as a Python dictionary
    try:
        result_dict = json.loads(content)
    except json.JSONDecodeError as e:
        print("Failed to parse GPT output. Raw content:")
        print(content)
        raise e

    print(result_dict)
    return list(set(result_dict['quantities']))


def add_quantities(quantity_list, new_quantity_input):
    print("add quantity")

    # new_quantity_input = input("Please insert the quantities you would like to add seperated by a comma: ")

    new_quantities = new_quantity_input.lower().split(",")

    return list(set(quantity_list + new_quantities))


def remove_quantities(quantity_list, remove_quantity_input):
    print("remove quantity")

    # remove_quantity_input = input("Please insert the quantities you would like to remove seperated by a comma: ")

    remove_quantity = remove_quantity_input.lower().split(",")

    not_removed = []

    for quantity in remove_quantity:
        
        if quantity in quantity_list:
            quantity_list.remove(quantity)
        else:
            not_removed.append(quantity)

    print(f"These quantities are not removed, since they are misspelled or not in the list: {not_removed}")
    return quantity_list



# Relation functions

def expand_relation_list(text, entity_list, quantity_list, relation_list, topic):
    print("expand relation")

    # increase = input("please insert an input between 0 and 100: ")
    increase = 20
    # expand the list
    prompt = p.expansion_relations(text, entity_list, quantity_list, relation_list, topic, increase)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": """You expand a list of triples, where each triple represents a relation between entities, quantities, or both.
                                            Return only a valid Python list of lists, e.g. [[subject, relation, object], ...].
                                            Do not return explanations, variable names, or code blocks.
                                            Do not use parentheses or tuples. Only return the list."""},
            {"role": "user", "content": prompt}
        ],
        temperature=0, # Makes it not random, but very predictable
    )

    raw_output = response.choices[0].message.content

    try:
        relations_list = ast.literal_eval(raw_output.strip())
        relations_list = [list(r) for r in relations_list]  # Ensure all are lists

        seen = set()
        unique_relations = []
        for rel in relations_list:
            rel_tuple = tuple(rel)
            if rel_tuple not in seen:
                unique_relations.append(rel)
                seen.add(rel_tuple)
        relations_list = unique_relations

    except Exception as e:
        print("Failed to parse model output:", e)
        print("Raw output:\n", raw_output)
        relations_list = []

    return relations_list


def contract_relation_list(text, entity_list, quantity_list, relation_list, topic):
    print("contract relation")

    # decrease = input("please insert an input between 0 and 100: ")
    decrease = 20
    # expand the list
    prompt = p.contraction_relations(text, entity_list, quantity_list, relation_list, topic, decrease)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": """You contract a list of triples, where each triple represents a relation between entities, quantities, or both.
                                            Return only a valid Python list of lists, e.g. [[subject, relation, object], ...].
                                            Do not return explanations, variable names, or code blocks.
                                            Do not use parentheses or tuples. Only return the list."""},
            {"role": "user", "content": prompt}
        ],
        temperature=0, # Makes it not random, but very predictable
    )

    raw_output = response.choices[0].message.content

    
    try:
        relations_list = ast.literal_eval(raw_output.strip())
        relations_list = [list(r) for r in relations_list]  # Ensure all are lists

        seen = set()
        unique_relations = []
        for rel in relations_list:
            rel_tuple = tuple(rel)
            if rel_tuple not in seen:
                unique_relations.append(rel)
                seen.add(rel_tuple)
        relations_list = unique_relations

    except Exception as e:
        print("Failed to parse model output:", e)
        print("Raw output:\n", raw_output)
        relations_list = []

    return relations_list


def add_relations(relation_list, new_relation_input):
    # print("add relation")

    # #new_relation_input = input("Please insert the relation you would like to add, as a rdf tuple (subject, predicate, object), seperated by a comma: ")

    # new_relation = new_relation_input.lower().split(",")

    # return relation_list + new_relation
    valid_predicates = {
        'configuration',
        'positive influence',
        'negative influence',
        'proportionally positive',
        'proportionally negative',
        'has property'
    }

    # Prepare input string
    input_str = new_relation_input.strip()
    if input_str.startswith('[') and input_str.endswith(']'):
        input_str = input_str[1:-1]

    # Split into raw triples
    triples_raw = re.split(r'\]\s*,\s*\[', input_str)

    raw_triples = []
    for triple_raw in triples_raw:
        triple_clean = triple_raw.strip(' []')
        parts = [p.strip().lower() for p in triple_clean.split(',')]
        if len(parts) != 3:
            continue  # invalid triple length, skip
        subj, pred, obj = parts
        if pred not in valid_predicates:
            continue  # invalid predicate, skip
        raw_triples.append((subj, pred, obj))

    # Convert existing relations inner lists to tuples (if any)
    existing_relations = set(tuple(r) if isinstance(r, list) else r for r in relation_list)
    new_relations = set(raw_triples)

    combined = list(existing_relations.union(new_relations))
    return combined


def remove_relations(relation_list, remove_relation_input):
    # print("remove relation")

    # #remove_relation_input = input("Please insert the relation you would like to remove, as a rdf tuple (subject, predicate, object), seperated by a comma: ")

    # remove_relation = remove_relation_input.lower().split(",")

    # not_removed = []

    # for relation in remove_relation:
        
    #     if relation in relation_list:
    #         relation_list.remove(relation)
    #     else:
    #         not_removed.append(relation)

    # print(f"These relations are not removed, since they are misspelled or not in the list: {not_removed}")
    # return relation_list

    
    # Normalize input by stripping whitespace and removing surrounding brackets if present
    clean_input = remove_relation_input.strip()
    if clean_input.startswith('[') and clean_input.endswith(']'):
        clean_input = clean_input[1:-1]

    # Split into relation triples by ']['
    raw_relations = clean_input.split('][')

    relations_to_remove = []
    for raw_rel in raw_relations:
        parts = [part.strip().lower() for part in raw_rel.split(',')]
        # Validate triple format
        if len(parts) == 3:
            relations_to_remove.append(tuple(parts))

    # Filter relation_list to remove matching relations
    # Normalize relation_list to tuples of lowercase stripped strings for comparison
    normalized_relation_list = [tuple(r.lower().strip() for r in rel) if isinstance(rel, (list, tuple)) else tuple(rel.lower().strip() for rel in rel.split(',')) for rel in relation_list]

    updated_list = [rel for rel in normalized_relation_list if rel not in relations_to_remove]

    # If original relation_list contained strings, convert tuples back to strings
    if relation_list and isinstance(relation_list[0], str):
        updated_list = [", ".join(rel) for rel in updated_list]

    return updated_list
