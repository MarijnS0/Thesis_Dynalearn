# import streamlit as st
# import uuid
# from pyvis.network import Network
# import streamlit.components.v1 as components

# # Initialize session state
# for key in ["entities", "quantities", "relations"]:
#     if key not in st.session_state:
#         st.session_state[key] = []

# st.title("Text Modeler Interface")

# # 1. Text Input
# text = st.text_area("Insert your text here", height=200)

# if st.button("Extract"):
#     # Simulated extraction (replace with real NLP here)
#     st.session_state.entities = [{"id": str(uuid.uuid4()), "name": "Calcium"}, {"id": str(uuid.uuid4()), "name": "Muscle"}]
#     st.session_state.quantities = [{"id": str(uuid.uuid4()), "name": "Calcium concentration"}]
#     st.session_state.relations = [{"id": str(uuid.uuid4()), "source": "Calcium", "target": "Muscle", "type": "Positive influence"}]

# # Helper function to display editable items
# def editable_list(title, items, key):
#     st.subheader(title)
#     for i, item in enumerate(items):
#         col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
#         with col1:
#             st.text_input("Name", item["name"], key=f"{key}_{i}_name", label_visibility="collapsed")
#         with col2:
#             if st.button("🔍", key=f"{key}_expand_{i}"):
#                 st.info(f"Expanded: {item['name']}")
#         with col3:
#             if st.button("❌", key=f"{key}_delete_{i}"):
#                 st.session_state[key].pop(i)
#                 st.experimental_rerun()
#         with col4:
#             if st.button("🔽", key=f"{key}_contract_{i}"):
#                 st.warning(f"Contracted: {item['name']}")
#     if st.button(f"➕ Add {title[:-1]}", key=f"add_{key}"):
#         st.session_state[key].append({"id": str(uuid.uuid4()), "name": f"New {title[:-1]}"})

# # 2. Entity, Quantity, Relation editors
# editable_list("Entities", st.session_state.entities, "entities")
# editable_list("Quantities", st.session_state.quantities, "quantities")

# # Custom interface for relations
# st.subheader("Relations")
# for i, rel in enumerate(st.session_state.relations):
#     col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 1, 1])
#     with col1:
#         rel["source"] = st.text_input("Source", rel["source"], key=f"rel_src_{i}", label_visibility="collapsed")
#     with col2:
#         rel["type"] = st.text_input("Type", rel["type"], key=f"rel_type_{i}", label_visibility="collapsed")
#     with col3:
#         rel["target"] = st.text_input("Target", rel["target"], key=f"rel_tgt_{i}", label_visibility="collapsed")
#     with col4:
#         if st.button("❌", key=f"rel_delete_{i}"):
#             st.session_state.relations.pop(i)
#             st.experimental_rerun()
#     with col5:
#         if st.button("🔽", key=f"rel_contract_{i}"):
#             st.warning(f"Contracted relation {rel['type']}")

# if st.button("➕ Add Relation"):
#     st.session_state.relations.append({"id": str(uuid.uuid4()), "source": "", "target": "", "type": "New relation"})

# # 3. Graph Visualization
# st.subheader("Visual Representation")

# net = Network(height="400px", width="100%", directed=True)
# added = set()

# for entity in st.session_state.entities + st.session_state.quantities:
#     if entity["name"] not in added:
#         net.add_node(entity["name"], label=entity["name"])
#         added.add(entity["name"])

# for rel in st.session_state.relations:
#     net.add_edge(rel["source"], rel["target"], label=rel["type"])

# net.save_graph("graph.html")
# components.html(open("graph.html", "r").read(), height=500)

import streamlit as st
from pathlib import Path
import knowledgebase_generator as knowgen

# Import your core functions here
# from your_module import read_text_file, entities_human_loop, quantities_human_loop, relations_human_loop, save_triples_to_ttl, plot_rdf

def main():
    st.set_page_config(page_title="Knowledge Representation Tool", layout="wide")
    st.title("Knowledge Representation from Educational Text")
    st.markdown("This tool extracts **entities**, **quantities**, and **relations** from text and builds a visual knowledge graph.")

    # Step 1: Text Upload
    st.header("1 Upload Educational Text")
    uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])
    topic = st.text_input("Topic name (used for saving files)", "biology_example").strip().replace(" ", "_")

    if uploaded_file and topic:
        text = uploaded_file.read().decode("utf-8")
        st.text_area("Text Preview", value=text, height=200)
    
    
        # # Step 2: Entity Extraction
        st.header("2 Entity Extraction")
        entities = knowgen.entities_human_loop(text, topic)


        if entities:
            st.success("Entity extraction complete!")
            st.header("3️⃣ Quantity Extraction")
            quantities = knowgen.quantities_human_loop(text, entities, topic)

            if quantities:
                st.success("Quantity extraction complete!")
                st.header("3 Relation Extraction")
                relations = knowgen.relations_human_loop(text, entities, quantities, topic)

                if relations:
                    st.success("Relation extraction complete!")

                    if relations:

                        # Step 5: Save & Visualize
                        st.header("4 Save")
                        # if st.button("Save RDF and Visualize"):
                            # with st.spinner("Saving TTL and generating graph..."):
                                # knowgen.save_triples_to_ttl(relations, entities, quantities, topic)
                        knowgen.show_ttl_download_button(relations, entities, quantities, topic)
                                # knowgen.plot_rdf(topic)
                            # st.success("Knowledge graph saved and visualized!")
                            # graph_path = f"{topic}_graph.png"
                            # if Path(graph_path).exists():
                            #     st.image(graph_path, caption="Knowledge Graph", use_container_width=True)
        

if __name__ == "__main__":
    main()
