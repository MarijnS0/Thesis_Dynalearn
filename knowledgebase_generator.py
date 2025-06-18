import json
from openai import OpenAI
import ast
import re
from rdflib import Graph
import networkx as nx
import matplotlib.pyplot as plt
import prompts as p
import helper_functions as helper
import streamlit as st
import io
import os


# Load API key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


# read the textfile
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
    
# extract the entities
def extract_entities(text, topic):
    prompt = p.entity_prompt(text, topic)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You extract conceptual entities from a text on a specific topic from a textbook used in secondary education. Return only a valid Python dictionary as JSON, and do NOT wrap the result in code blocks."},
            {"role": "user", "content": prompt}
        ],
        temperature=0 # Makes it not random, but very predictable
    )

    # Extract the string content from the response object properly
    content = response.choices[0].message.content.strip()


    # Clean up code block markers if present
    content = re.sub(r"```(?:json|python)?\n?", "", content).strip("` \n")

    # st.text("RAW RESPONSE:")
    # st.text(content)

    try:
        result_dict = json.loads(content)
    except json.JSONDecodeError as e:
        st.error("Could not parse the model output as JSON.")
        st.text(content)
        raise e

    # # Strip the ```python ... ``` block if present
    # if content.startswith("```python"):
    #     content = content.strip("```python").strip("```").strip()

    # # Now safely load as a Python dictionary
    # try:
    #     result_dict = json.loads(content)
    # except json.JSONDecodeError as e:
    #     print("Failed to parse GPT output. Raw content:")
    #     print(content)
    #     raise e

    # print(result_dict)
    return list(set(result_dict['entities']))

# identify the quantities from the entity list
def extract_quantities(entity_list, text):
    
    prompt = p.quantity_prompt(entity_list, text)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You extract quantities from a list of entities that is extracted from a given text from a textbook used in secondary education. Return only a valid Python dictionary as JSON, and do NOT wrap the result in code blocks. Only choose terms from the given list"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0
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


# extract the relations
def extracting_relations(text, entities, quantities):
    st.write(f"extracting_relations called with {len(text)} chars, {len(entities)} entities, {len(quantities)} quantities")


    prompt = p.relations_prompt(text, entities, quantities)
    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You extract structured scientific relations from text between entities or quantities provided. You return these triples as a tupled python list."},
        {"role": "user", "content": prompt}
    ],
    temperature=0,
    max_tokens= 3000
    )

    raw_output = response.choices[0].message.content

    # st.write(f"raw: {raw_output}")
    st.write(f"raw (repr): {repr(raw_output)}")


    # Clean raw output from code blocks and variable assignment
    cleaned = re.sub(r"^```(?:python)?\n?", "", raw_output.strip(), flags=re.IGNORECASE)
    cleaned = re.sub(r"\n?```$", "", cleaned.strip())
    cleaned = re.sub(r"^\s*\w+\s*=\s*", "", cleaned.strip())

    try:
        relations_list = ast.literal_eval(cleaned)

         # Remove duplicates from list of lists
        seen = set()
        unique_relations = []
        for rel in relations_list:
            rel_tuple = tuple(rel)
            if rel_tuple not in seen:
                unique_relations.append(rel)
                seen.add(rel_tuple)
        relations_list = unique_relations

    except Exception as e:
        print("Failed to parse cleaned model output:", e)
        print("Cleaned output:\n", cleaned)
        relations_list = []

    st.write(f"not raw: {relations_list}")

    return relations_list


# # save the knowledge representation as rdf triples into a ttl file
# def save_triples_to_ttl(relations, entities, quantities, topic):
#     """
#     Saves extracted triples, entity types, and quantity types to a TTL file.
#     """

#     filepath= f"generated_output/generated_{topic}.ttl"

#     with open(filepath, "w") as f:
#         f.write("@prefix : <http://example.org/> .\n")
#         f.write("@prefix rel: <http://example.org/relation#> .\n")
#         f.write("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n\n")

#         # Write type declarations
#         for ent in entities:
#             f.write(f":{ent.replace(' ', '_')} rdf:type :Entity .\n")
#         for quant in quantities:
#             f.write(f":{quant.replace(' ', '_')} rdf:type :Quantity .\n")

#         f.write("\n")

#         # Write triples
#         for subj, rel, obj in relations:
#             subj_uri = subj.replace(" ", "_")
#             obj_uri = obj.replace(" ", "_")
#             pred_uri = rel.replace(" ", "_")

#             f.write(f":{subj_uri} rel:{pred_uri} :{obj_uri} .\n")


def generate_ttl_string(relations, entities, quantities, topic):
    ttl_lines = []
    ttl_lines.append("@prefix : <http://example.org/> .")
    ttl_lines.append("@prefix rel: <http://example.org/relation#> .")
    ttl_lines.append("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n")

    # Write type declarations
    for ent in entities:
        ttl_lines.append(f":{ent.replace(' ', '_')} rdf:type :Entity .")
    for quant in quantities:
        ttl_lines.append(f":{quant.replace(' ', '_')} rdf:type :Quantity .")

    ttl_lines.append("")

    # Write triples
    for subj, rel, obj in relations:
        subj_uri = subj.replace(" ", "_")
        obj_uri = obj.replace(" ", "_")
        pred_uri = rel.replace(" ", "_")
        ttl_lines.append(f":{subj_uri} rel:{pred_uri} :{obj_uri} .")

    return "\n".join(ttl_lines)

def show_ttl_download_button(relations, entities, quantities, topic):
    ttl_string = generate_ttl_string(relations, entities, quantities, topic)
    ttl_bytes = io.BytesIO(ttl_string.encode("utf-8"))

    st.download_button(
        label="Download TTL file",
        data=ttl_bytes,
        file_name=f"generated_{topic}.ttl",
        mime="text/turtle"
    )



# plot the knowledge representation
def plot_rdf(topic):

    # Read RDF file
    g = Graph()
    g.parse(f"generated_output/generated_{topic}.ttl", format="turtle")

    # Initialize graph
    G = nx.DiGraph()

    entity_nodes = set()
    quantity_nodes = set()

    # Extract relations
    for subj, pred, obj in g:

        pred_label = pred.toPython().rsplit('/', 1)[-1].rsplit('#', 1)[-1]
        subj_label = subj.toPython().rsplit('/', 1)[-1].rsplit('#', 1)[-1]
        obj_label = obj.toPython().rsplit('/', 1)[-1].rsplit('#', 1)[-1]

        #Add nodes
        G.add_node(subj_label)

        if pred_label != 'type':
            G.add_node(obj_label)

        # Add edges
        if pred_label != 'type':
            G.add_edge(subj_label, obj_label, label=pred_label)

        # Identify node types
        if pred_label == 'type' and subj_label == "Quantity":
            quantity_nodes.add(obj_label)
        elif pred_label == 'type' and obj_label == "Quantity":
            quantity_nodes.add(subj_label)

        if pred_label == 'type' and subj_label == "Entity":
            entity_nodes.add(obj_label)
        elif pred_label == 'type' and obj_label == "Entity":
            entity_nodes.add(subj_label)

     # Visualize graph using matplotlib and streamlit
    pos = nx.spring_layout(G, seed=42, k= 2)
    edge_labels = nx.get_edge_attributes(G, 'label')

    node_colors = ['pink' if node in entity_nodes else 'yellow' if node in quantity_nodes else 'grey' for node in G.nodes]

    fig, ax = plt.subplots(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=800,
            font_size=10, font_weight='bold', edge_color='gray', ax=ax)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, ax=ax)
    ax.set_title(f"{topic} knowledge representation")
    ax.axis('off')

    # ✅ This is the key line that renders it in Streamlit:
    st.pyplot(fig)

    # # Visualize graph
    # pos = nx.spring_layout(G, seed=42, k=6.0)  # Increase k to get more space between nodes
    # edge_labels = nx.get_edge_attributes(G, 'label')

    # # Entity nodes are pink and quantity nodes are yellow, unknown nodes are grey
    # node_colors = ['pink' if node in entity_nodes  else 'yellow' if node in quantity_nodes else 'grey' for node in G.nodes]

    # plt.figure(figsize=(12, 8))
    # nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=2000, font_size=10, font_weight='bold', edge_color='gray')
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    # plt.title(f"{topic} knowledge representation")
    # plt.axis('off')
    # plt.show()


def entities_human_loop(text, topic):

    # Initialize session state
    if "entity_state" not in st.session_state:
        st.session_state.entity_state = False
    if "entity_list" not in st.session_state:
        st.session_state.entity_list = []
    if "extract_clicked" not in st.session_state:
        st.session_state.extract_clicked = False
    if "show_add_input" not in st.session_state:
        st.session_state.show_add_input = False
    if "new_entities_input" not in st.session_state:
        st.session_state.new_entities_input = ""
    if "show_remove_input" not in st.session_state:
        st.session_state.show_remove_input = False
    if "remove_entities_input" not in st.session_state:
        st.session_state.remove_entities_input = ""
    if "entities_finalized" not in st.session_state:
        st.session_state.entities_finalized = False


    # Extract button
    if not st.session_state.extract_clicked:
        if st.button("Extract entities-quantities"):
            st.session_state.entity_state = True
            st.session_state.entity_list = extract_entities(text, topic)
            st.session_state.extract_clicked = True
            st.rerun()
    else:
        st.button("Extract entities-quantities", disabled=True)

    # Entity manipulation buttons
    if st.session_state.entity_state and not st.session_state.entities_finalized:
        # Expand
        if st.button("Expand entity-quantity list"):
            st.session_state.entity_list = helper.expand_entity_list(text, st.session_state.entity_list, topic)
            st.session_state.expand_success = True
        
        # Contract
        if st.button("Contract entity-quantity list"):
            st.session_state.entity_list = helper.contract_entity_list(text, st.session_state.entity_list, topic)
            st.session_state.contract_success = True

        # Show Add input on button press
        if not st.session_state.show_add_input:
            if st.button("Add entities/quantities"):
                st.session_state.show_add_input = True
                st.rerun()
        else:
            st.session_state.new_entities_input = st.text_input("Add new entities or quantities, comma-separated:", value=st.session_state.new_entities_input, key="add_input_box")
            if st.button("Confirm add"):
                # new_entities = [e.strip().lower() for e in st.session_state.new_entities_input.split(",") if e.strip()]
                st.session_state.entity_list = helper.add_entities(st.session_state.entity_list, st.session_state.new_entities_input)
                # st.success(f"Added {len(new_entities)} entities.")
                st.session_state.new_entities_input = ""
                st.session_state.show_add_input = False
                st.rerun()

        # Show remove input on button press
        if not st.session_state.show_remove_input:
            if st.button("Remove entities/quantities"):
                st.session_state.show_remove_input = True
                st.rerun()
        else:
            st.session_state.remove_entities_input = st.text_input("Enter the entities or quantities you want to remove, comma-separated:", value=st.session_state.remove_entities_input, key="remove_input_box")
            if st.button("Confirm removal"):
                # new_entities = [e.strip().lower() for e in st.session_state.new_entities_input.split(",") if e.strip()]
                st.session_state.entity_list = helper.remove_entities(st.session_state.entity_list, st.session_state.remove_entities_input)
                # st.success(f"Added {len(new_entities)} entities.")
                st.session_state.remove_entities_input = ""
                st.session_state.show_remove_input = False
                st.rerun()

    # Display entity list
    st.write("### Current entity-quantity list:")
    st.write(st.session_state.entity_list if st.session_state.entity_list else "[No entities extracted yet]")

    # Optional success messages
    if st.session_state.get("expand_success", False):
        st.success("Entity-quantity list expanded!")
        st.session_state.expand_success = False

    if st.session_state.get("contract_success", False):
        st.success("Entity-quantity list contracted!")
        st.session_state.contract_success = False
    
    if st.session_state.entity_state and not st.session_state.entities_finalized:
        if st.button("Finished"):
            st.session_state.entities_finalized = True
            st.rerun()
    
    if st.session_state.entities_finalized:
        return st.session_state.entity_list

    return None



def quantities_human_loop(text, entity_list, topic):

    # quantity_list = extract_quantities(entity_list, text)
    # print(f"quantity list: {quantity_list}")

    # while True:
    #     action = input("""Please enter a number corresponding to the action:
    #                    0: quit
    #                    1: add quantities
    #                    2: remove quantities
    #                    3: expand quantity list
    #                    4: contract quantity list
    #                    """)

    #     if action == '0':
    #         return quantity_list
    #     elif action == '1':
    #         quantity_list = helper.add_quantities(quantity_list)
    #         print(quantity_list)
    #     elif action == '2':
    #         quantity_list = helper.remove_quantities(quantity_list)
    #         print(quantity_list)
    #     elif action == '3': 
    #         quantity_list = helper.expand_quantity_list(text, entity_list, quantity_list, topic)
    #         print(quantity_list)
    #     elif action == '4':
    #         quantity_list = helper.contract_quantity_list(text, entity_list, quantity_list, topic)
    #         print(quantity_list)
    #     else:
    #         print("invalid action")

    # Initialize session state
    if "quantity_state" not in st.session_state:
        st.session_state.quantity_state = False
    if "quantity_list" not in st.session_state:
        st.session_state.quantity_list = []
    if "extract_quantity_clicked" not in st.session_state:
        st.session_state.extract_quantity_clicked = False
    if "show_add_quantity_input" not in st.session_state:
        st.session_state.show_add_quantity_input = False
    if "new_quantity_input" not in st.session_state:
        st.session_state.new_quantity_input = ""
    if "show_remove_quantity_input" not in st.session_state:
        st.session_state.show_remove_quantity_input = False
    if "remove_quantity_input" not in st.session_state:
        st.session_state.remove_quantity_input = ""
    if "quantity_finalized" not in st.session_state:
        st.session_state.quantity_finalized = False


    # Extract button
    if not st.session_state.extract_quantity_clicked:
        if st.button("Extract quantities"):
            st.session_state.quantity_state = True
            st.session_state.quantity_list = extract_quantities(entity_list, text)
            st.session_state.extract_quantity_clicked = True
            st.rerun()
    else:
        st.button("Extract quantities", disabled=True)

    # Entity manipulation buttons
    if st.session_state.quantity_state and not st.session_state.quantity_finalized:
        # Expand
        if st.button("Expand quantity list"):
            st.session_state.quantity_list = helper.expand_quantity_list(text, entity_list, st.session_state.quantity_list, topic)
            st.session_state.expand_quantity_success = True
        
        # Contract
        if st.button("Contract quantity list"):
            st.session_state.quantity_list = helper.contract_quantity_list(text, entity_list, st.session_state.quantity_list, topic)
            st.session_state.contract_quantity_success = True

        # Show Add input on button press
        if not st.session_state.show_add_quantity_input:
            if st.button("Add quantities"):
                st.session_state.show_add_quantity_input = True
                st.rerun()
        else:
            st.session_state.new_quantity_input = st.text_input("Add new quantities, comma-separated:", value=st.session_state.new_quantity_input, key="add_quantity_input_box")
            if st.button("Confirm add", key="confirm_quantity_add"):
                # new_entities = [e.strip().lower() for e in st.session_state.new_entities_input.split(",") if e.strip()]
                st.session_state.quantity_list = helper.add_quantities(st.session_state.quantity_list, st.session_state.new_quantity_input)
                # st.success(f"Added {len(new_entities)} entities.")
                st.session_state.new_quantity_input = ""
                st.session_state.show_add_quantity_input = False
                st.rerun()

        # Show remove input on button press
        if not st.session_state.show_remove_quantity_input:
            if st.button("Remove quantities"):
                st.session_state.show_remove_quantity_input = True
                st.rerun()
        else:
            st.session_state.remove_quantity_input = st.text_input("Enter the quantities you want to remove, comma-separated:", value=st.session_state.remove_quantity_input, key="remove_quantity_input_box")
            if st.button("Confirm removal", key="confirm_quantity_removal"):
                # new_entities = [e.strip().lower() for e in st.session_state.new_entities_input.split(",") if e.strip()]
                st.session_state.quantity_list = helper.remove_quantities(st.session_state.quantity_list, st.session_state.remove_quantity_input)
                # st.success(f"Added {len(new_entities)} entities.")
                st.session_state.remove_quantity_input = ""
                st.session_state.show_remove_quantity_input = False
                st.rerun()

    # Display entity list
    st.write("### Current quantities:")
    st.write(st.session_state.quantity_list if st.session_state.quantity_list else "[No quantities extracted yet]")

    # Optional success messages
    if st.session_state.get("expand_quantity_success", False):
        st.success("Quantity list expanded!")
        st.session_state.expand_quantity_success = False

    if st.session_state.get("contract_quantity_success", False):
        st.success("Quantity list contracted!")
        st.session_state.contract_quantity_success = False
    
    if st.session_state.quantity_state and not st.session_state.quantity_finalized:
        if st.button("Finished", key="finished_quantity"):
            st.session_state.quantity_finalized = True
            st.rerun()
    
    if st.session_state.quantity_finalized:
        return st.session_state.quantity_list

    return None



def relations_human_loop(text, entity_list, quantity_list, topic):

    # relation_list = extracting_relations(text, entity_list, quantity_list)
    # print(f"relation list: {relation_list}")

    # while True:
    #     action = input("""Please enter a number corresponding to the action:
    #                    0: quit
    #                    1: add relations
    #                    2: remove relations
    #                    3: expand relation list
    #                    4: contract relation list
    #                    """)

    #     if action == '0':
    #         return relation_list
    #     elif action == '1':
    #         relation_list = helper.add_relations(relation_list)
    #         print(relation_list)
    #     elif action == '2':
    #         relation_list = helper.remove_relations(relation_list)
    #         print(relation_list)
    #     elif action == '3': 
    #         relation_list = helper.expand_relation_list(text, entity_list, quantity_list, relation_list, topic)
    #         print(relation_list)
    #     elif action == '4':
    #         relation_list = helper.contract_relation_list(text, entity_list, quantity_list, relation_list, topic)
    #         print(relation_list)
    #     else:
    #         print("invalid action")

    # Initialize session state
    if "relation_state" not in st.session_state:
        st.session_state.relation_state = False
    if "relation_list" not in st.session_state:
        st.session_state.relation_list = []
    if "extract_relation_clicked" not in st.session_state:
        st.session_state.extract_relation_clicked = False
    if "show_add_relation_input" not in st.session_state:
        st.session_state.show_add_relation_input = False
    if "new_relation_input" not in st.session_state:
        st.session_state.new_relation_input = ""
    if "show_remove_relation_input" not in st.session_state:
        st.session_state.show_remove_relation_input = False
    if "remove_relation_input" not in st.session_state:
        st.session_state.remove_relation_input = ""
    if "relation_finalized" not in st.session_state:
        st.session_state.relation_finalized = False


    # Extract button
    if not st.session_state.extract_relation_clicked:
        if st.button("Extract relations"):
            st.session_state.relation_state = True
            st.session_state.relation_list = extracting_relations(text, entity_list, quantity_list)
            st.session_state.extract_relation_clicked = True
            st.rerun()
    else:
        st.button("Extract relations", disabled=True)

    # relation manipulation buttons
    if st.session_state.relation_state and not st.session_state.relation_finalized:
        # Expand
        if st.button("Expand relation list"):
            st.session_state.relation_list = helper.expand_relation_list(text, entity_list, quantity_list,st.session_state.relation_list, topic)
            st.session_state.expand_relation_success = True
        
        # Contract
        if st.button("Contract relation list"):
            st.session_state.relation_list = helper.contract_relation_list(text, entity_list, quantity_list, st.session_state.relation_list, topic)
            st.session_state.contract_relation_success = True

        # Show Add input on button press
        if not st.session_state.show_add_relation_input:
            if st.button("Add relations"):
                st.session_state.show_add_relation_input = True
                st.rerun()
        else:
            st.session_state.new_relation_input = st.text_input("Add new relations as : [object, predicate, subject], where predicate is the relation type (see description). Please use the right format, otherwise the relation will not be added.", value=st.session_state.new_relation_input, key="add_relation_input_box")
            if st.button("Confirm add", key="confirm_relation_add"):
                # new_entities = [e.strip().lower() for e in st.session_state.new_entities_input.split(",") if e.strip()]
                st.session_state.relation_list = helper.add_relations(st.session_state.relation_list, st.session_state.new_relation_input)
                # st.success(f"Added {len(new_entities)} entities.")
                st.session_state.new_relation_input = ""
                st.session_state.show_add_relation_input = False
                st.rerun()

        # Show remove input on button press
        if not st.session_state.show_remove_relation_input:
            if st.button("Remove relations"):
                st.session_state.show_remove_relation_input = True
                st.rerun()
        else:
            st.session_state.remove_relation_input = st.text_input("Enter the relations you want to remove as: [object, predicate, subject], where predicate is the relation type (see description). Please use the right format, otherwise the relation will not be removed", value=st.session_state.remove_relation_input, key="remove_relation_input_box")
            if st.button("Confirm removal", key="confirm_relation_removal"):
                # new_entities = [e.strip().lower() for e in st.session_state.new_entities_input.split(",") if e.strip()]
                st.session_state.relation_list = helper.remove_relations(st.session_state.relation_list, st.session_state.remove_relation_input)
                # st.success(f"Added {len(new_entities)} entities.")
                st.session_state.remove_relation_input = ""
                st.session_state.show_remove_relation_input = False
                st.rerun()

    # Display entity list
    st.write("### Current relations:")
    st.write(st.session_state.relation_list if st.session_state.relation_list else "[No relations extracted yet]")

    # Optional success messages
    if st.session_state.get("expand_relation_success", False):
        st.success("Relation list expanded!")
        st.session_state.expand_relation_success = False

    if st.session_state.get("contract_relation_success", False):
        st.success("Relation list contracted!")
        st.session_state.contract_relation_success = False
    
    if st.session_state.relation_state and not st.session_state.relation_finalized:
        if st.button("Finished", key="finished_relation"):
            st.session_state.relation_finalized = True
            st.rerun()
    
    if st.session_state.relation_finalized:
        return st.session_state.relation_list

    return None


# if __name__=="__main__":

#     text_calcium = read_text_file("input_text/calciumhomeostasis.txt")
#     topic_calcium = "calcium_homeostasis"

#     entities_calcium = entities_human_loop(text_calcium, topic_calcium)
#     quantities_calcium = quantities_human_loop(text_calcium, entities_calcium, topic_calcium)

#     # entities_calcium = ['calcium ions', 'secondary messenger', 'cells', 'transmission of impulses', 'nervous system', 'muscle contraction', 'bone loss', 'osteoporosis', 'stomach complaints', 'intestinal complaints', 'thyroid gland', 'parathyroid glands', 'receptors', 'cell membranes', 'thyroid cells', 'calcitonin', 'bone cells', 'blood plasma', 'nephron cells', 'pre-urine', 'parathyroid hormone', 'pth', 'active vitamin d', 'calcitriol', 'intestinal cells', 'food', 'skin cells', 'prohormone vitamin d', 'cholesterol', 'sunlight', 'liver', 'kidneys', 'blood', 'bones', 'hormone', 'vitamin d', 'ca²⁺ concentration', 'secretion', 'thyroid', 'parathyroid', 'vitamin d formation', 'calcium homeostasis', 'calcium regulation', 'calcium absorption', 'calcium reabsorption', 'blood level', 'normal range', 'ca²⁺ level', 'bone', 'thyroid cells', 'parathyroid cells', 'vitamin d', 'calcitriol', 'prohormone vitamin d']
    
#     # quantities_calcium = ['calcium ions', 'transmission of impulses', 'muscle contraction', 'ca²⁺ concentration', 'ca²⁺ level', 'bone loss', 'stomach complaints', 'intestinal complaints', 'normal range', 'calcium absorption', 'calcium reabsorption', 'calcitonin', 'parathyroid hormone', 'active vitamin d', 'vitamin d formation', 'calcium homeostasis', 'calcitriol', 'cholesterol', 'sunlight', 'prohormone vitamin d']
    
#     entities_calcium = [item for item in entities_calcium if item not in quantities_calcium]
#     relations_calcium = relations_human_loop(text_calcium, entities_calcium, quantities_calcium, topic_calcium)

#     save_triples_to_ttl(relations_calcium, entities_calcium, quantities_calcium, topic_calcium)
#     plot_rdf(topic_calcium)


    # text_bones = read_text_file("input_text/bone_formation.txt")
    # topic_bones = "bone_formation"
    # entities_bones = entities_human_loop(text_bones, topic_bones)
    # quantities_bones = quantities_human_loop(text_bones, entities_bones, topic_bones)


