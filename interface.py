import streamlit as st
from pathlib import Path
import knowledgebase_generator as knowgen


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
            st.header("3 Quantity Extraction")
            quantities = knowgen.quantities_human_loop(text, entities, topic)

            if quantities:
                st.success("Quantity extraction complete!")
                st.header("4 Relation Extraction")
                
                entities = [item for item in entities if item not in quantities]
                relations = knowgen.relations_human_loop(text, entities, quantities, topic)

                if relations:
                    st.success("Relation extraction complete!")

                    if relations:

                        # Step 5: Save & Visualize
                        st.header("5 Save")
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
