import streamlit as st, json, os
from dotenv import load_dotenv
from db_inspector import DBInspector
from ai_generator import generate_with_claude, generate_with_gemini
from metadata_store import save_doc, get_doc, get_all_docs, export_markdown
from seed_demo_db import seed

load_dotenv()

st.set_page_config(
    page_title="GenAI Metadata Manager",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 GenAI Metadata Manager")
st.caption("Auto-generate data documentation using Claude & Gemini")

# ── Sidebar ──────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Configuration")

    db_choice = st.radio(
        "Database", ["Demo SQLite (healthcare RCM)", "Custom URL"])

    if db_choice == "Demo SQLite (healthcare RCM)":
        if not os.path.exists("demo.db"):
            with st.spinner("Seeding demo database..."):
                seed()
            st.success("Demo DB created!")
        db_url = "sqlite:///demo.db"
    else:
        db_url = st.text_input(
            "SQLAlchemy URL",
            placeholder="postgresql://user:pass@host/db")

    st.divider()
    ai_model = st.radio(
        "AI Model",
        ["Claude Sonnet (Anthropic)", "Gemini Flash (Google)"]
    )
    model_name = (
        "claude-sonnet-4-5"
        if "Claude" in ai_model
        else "gemini-1.5-flash"
    )
    st.caption(f"Model: `{model_name}`")

    st.divider()
    st.header("📊 Coverage")
    all_docs = get_all_docs()
    st.metric("Tables documented", len(all_docs))

# ── Main tabs ─────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(
    ["📝 Generate Docs", "✅ Approved Docs", "📤 Export"])

# Tab 1 — Generate
with tab1:
    if not db_url:
        st.info("Enter a database URL in the sidebar to begin.")
        st.stop()

    try:
        inspector = DBInspector(db_url)
        tables = inspector.get_tables()
    except Exception as e:
        st.error(f"Connection failed: {e}")
        st.stop()

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Select Table")
        for t in tables:
            approved = "✅" if get_doc(t) else "⬜"
            if st.button(f"{approved} {t}", key=f"btn_{t}",
                         use_container_width=True):
                st.session_state["selected_table"] = t

    with col2:
        tbl = st.session_state.get("selected_table")
        if not tbl:
            st.info("← Select a table to begin")
        else:
            st.subheader(f"Table: `{tbl}`")
            with st.spinner("Fetching schema..."):
                ctx = inspector.get_table_context(tbl)

            with st.expander("📋 Raw schema context sent to AI"):
                st.json(ctx)

            if st.button(f"🚀 Generate docs with {ai_model}",
                         type="primary", use_container_width=True):
                with st.spinner(f"Asking {ai_model}..."):
                    try:
                        if "Claude" in ai_model:
                            doc = generate_with_claude(ctx)
                        else:
                            doc = generate_with_gemini(ctx)
                        st.session_state["generated_doc"] = doc
                        st.session_state["doc_table"] = tbl
                        st.success("Documentation generated!")
                    except Exception as e:
                        st.error(f"AI generation failed: {e}")

            if st.session_state.get("generated_doc") and \
               st.session_state.get("doc_table") == tbl:
                doc = st.session_state["generated_doc"]
                st.markdown("---")

                # Editable table description
                new_desc = st.text_area(
                    "Table description (edit if needed)",
                    value=doc.get("table_description",""),
                    height=100)
                doc["table_description"] = new_desc

                st.markdown("**Column definitions:**")
                for i, col in enumerate(doc.get("columns",[])):
                    with st.expander(f"`{col['name']}`"):
                        doc["columns"][i]["description"] = st.text_input(
                            "Description", col["description"],
                            key=f"col_{i}")

                st.markdown("**Data quality notes:**")
                doc["data_quality_notes"] = st.text_area(
                    "Notes", doc.get("data_quality_notes",""),
                    height=60, label_visibility="collapsed")

                st.markdown("**Tags:**")
                st.write(", ".join(
                    [f"`{t}`" for t in doc.get("suggested_tags",[])]))

                if st.button("✅ Approve & Save", type="primary"):
                    save_doc(tbl, doc, model_name)
                    st.success(f"Documentation for `{tbl}` approved!")
                    st.balloons()

# Tab 2 — Approved docs
with tab2:
    docs = get_all_docs()
    if not docs:
        st.info("No approved documentation yet. Generate and approve some!")
    else:
        sel = st.selectbox("Select table", list(docs.keys()))
        if sel:
            doc = docs[sel]
            st.markdown(f"### `{sel}`")
            st.info(doc.get("table_description",""))

            df_cols = [{
                "Column": c["name"],
                "Description": c["description"],
                "Example": c.get("example_value","")
            } for c in doc.get("columns",[])]
            st.dataframe(df_cols, use_container_width=True,
                         hide_index=True)

            st.markdown("**Business Glossary**")
            for g in doc.get("business_glossary",[]):
                st.markdown(f"**{g['term']}**: {g['definition']}")

            meta = doc.get("_meta",{})
            st.caption(
                f"Generated by `{meta.get('generated_by','')}` · "
                f"Approved {meta.get('approved_at','')[:10]} · "
                f"v{meta.get('version',1)}")

# Tab 3 — Export
with tab3:
    docs = get_all_docs()
    if not docs:
        st.info("Approve some documentation first.")
    else:
        sel_exp = st.selectbox(
            "Table to export", list(docs.keys()), key="exp_sel")
        if sel_exp:
            md = export_markdown(sel_exp)
            st.markdown(md)
            st.download_button(
                "⬇️ Download Markdown",
                md,
                file_name=f"{sel_exp}_docs.md",
                mime="text/markdown"
            )
            st.download_button(
                "⬇️ Download JSON",
                json.dumps(docs[sel_exp], indent=2, default=str),
                file_name=f"{sel_exp}_docs.json",
                mime="application/json"
            )