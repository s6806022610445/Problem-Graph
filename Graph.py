import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# ตั้งค่าหน้ากระดาษ
st.set_page_config(page_title="Graph Management System", layout="wide")

# --- 1. การจัดการ State (เก็บข้อมูล Graph) ---
if 'G' not in st.session_state:
    # เริ่มต้นสร้าง Graph ตั้งต้น
    G = nx.Graph()
    G.add_weighted_edges_from([
        ("A", "B", 4), ("A", "C", 2), ("A", "G", 6),
        ("B", "C", 7), ("B", "F", 5),
        ("C", "D", 8), ("C", "H", 3),
        ("D", "A", 3),
        ("F", "G", 2), ("F", "I", 3),
        ("H", "B", 7), ("H", "E", 4)
    ])
    st.session_state.G = G

G = st.session_state.G

# --- 2. ส่วนของ UI Sidebar (เมนูจัดการ) ---
st.sidebar.title("🛠 Graph Control Panel")

# ส่วนจัดการ Node
with st.sidebar.expander("Node Management", expanded=True):
    col1, col2 = st.columns([2, 1])
    new_node = col1.text_input("Node Name", placeholder="e.g. Z").upper()
    if col2.button("Add", use_container_width=True):
        if new_node:
            G.add_node(new_node)
            st.rerun()

    del_node = col1.text_input("Delete Node", placeholder="Name").upper()
    if col2.button("Remove", use_container_width=True):
        if del_node in G.nodes:
            G.remove_node(del_node)
            st.rerun()
        else:
            st.error("Node not found!")

# ส่วนจัดการ Edge
with st.sidebar.expander("Edge Management"):
    e_u = st.text_input("From Node").upper()
    e_v = st.text_input("To Node").upper()
    e_w = st.number_input("Weight", min_value=0.1, value=1.0)
    if st.button("Add/Update Edge", use_container_width=True):
        if e_u and e_v:
            G.add_edge(e_u, e_v, weight=e_w)
            st.rerun()

# ส่วนค้นหาเส้นทาง
with st.sidebar.expander("Pathfinding"):
    p_start = st.text_input("Start Node", value="A").upper()
    p_end = st.text_input("End Node", value="I").upper()
    find_path = st.button("Find Shortest Path", use_container_width=True)

# --- 3. ส่วนการแสดงผล (Main Area) ---
st.title("🌐 Interactive Graph Management System")

col_main, col_info = st.columns([3, 1])

with col_main:
    fig, ax = plt.subplots(figsize=(10, 7))
    pos = nx.kamada_kawai_layout(G, weight='weight')
    
    # วาด Graph พื้นฐาน
    nx.draw(G, pos, with_labels=True, node_color='skyblue', 
            node_size=800, font_weight='bold', edge_color='gray', ax=ax)
    
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)

    # ถ้ามีการกดปุ่ม Find Path
    if find_path:
        try:
            path = nx.shortest_path(G, source=p_start, target=p_end, weight='weight')
            dist = nx.shortest_path_length(G, p_start, p_end, weight='weight')
            
            path_edges = list(zip(path, path[1:]))
            # ไฮไลท์เส้นทาง
            nx.draw_networkx_nodes(G, pos, nodelist=[p_start, p_end], node_color='gold', node_size=1000, ax=ax)
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='crimson', width=5, ax=ax)
            
            st.success(f"Path Found: {' ➔ '.join(path)} | Total Weight: {dist}")
        except Exception as e:
            st.error(f"Error: {e}")

    st.pyplot(fig)

with col_info:
    st.write("**Current Statistics**")
    st.write(f"Nodes: {G.number_of_nodes()}")
    st.write(f"Edges: {G.number_of_edges()}")
    
    if st.button("Reset Graph"):
        del st.session_state.G
        st.rerun()
