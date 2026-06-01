import os
import io
import html

import streamlit as st
from pypdf import PdfReader
from dotenv import load_dotenv

from summarizer import make_client, summarise, compare

load_dotenv()

st.set_page_config(
    page_title="Policy Summarizer",
    page_icon="📋",
    layout="wide",
)

st.markdown("""
<style>
    .summary-box {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1.25rem 1.5rem;
        font-size: 0.9rem;
        line-height: 1.7;
    }
    .badge {
        display: inline-block;
        background: #dbeafe;
        color: #1e40af;
        border-radius: 4px;
        padding: 0.15rem 0.5rem;
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────

for k, v in {"client": None, "provider": None, "docs": {}, "result": None, "mode": "summarize"}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Sidebar ────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.header("Setup")

    provider_label = st.selectbox("LLM Provider", ["Groq (free)", "OpenAI"])
    provider = "groq" if "Groq" in provider_label else "openai"

    if provider == "groq":
        api_key = st.text_input(
            "Groq API Key", type="password",
            placeholder="gsk_...",
            value=os.getenv("GROQ_API_KEY", ""),
        )
        st.caption("Free key at [console.groq.com/keys](https://console.groq.com/keys)")
    else:
        api_key = st.text_input(
            "OpenAI API Key", type="password",
            placeholder="sk-...",
            value=os.getenv("OPENAI_API_KEY", ""),
        )

    ready = bool(api_key)
    if ready:
        st.session_state.client = make_client(api_key, provider)
        st.session_state.provider = provider

    st.divider()
    st.subheader("Mode")
    mode = st.radio("", ["Summarize", "Compare documents"], label_visibility="collapsed")
    st.session_state.mode = "compare" if "Compare" in mode else "summarize"

    st.divider()
    st.subheader("Upload documents")

    MAX_PDF_MB = 10
    uploaded = st.file_uploader(
        "PDF files",
        type="pdf",
        accept_multiple_files=(st.session_state.mode == "compare"),
        label_visibility="collapsed",
    )

    paste_label = st.text_input("Document name (for paste)", value="Policy")
    pasted = st.text_area("Or paste text", height=140, label_visibility="collapsed")

    if st.button("Add pasted text", use_container_width=True, disabled=not pasted.strip()):
        st.session_state.docs[paste_label] = pasted.strip()
        st.success(f"Added: {paste_label}")

    if uploaded:
        files = uploaded if isinstance(uploaded, list) else [uploaded]
        for f in files:
            if f.name not in st.session_state.docs:
                if f.size > MAX_PDF_MB * 1024 * 1024:
                    st.error(f"{f.name} exceeds {MAX_PDF_MB} MB limit.")
                else:
                    text = "\n\n".join(
                        page.extract_text() or ""
                        for page in PdfReader(io.BytesIO(f.read())).pages
                    )
                    st.session_state.docs[f.name] = text
                    st.success(f"Loaded: {f.name}")

    if st.session_state.docs:
        st.caption(f"{len(st.session_state.docs)} document(s) loaded:")
        for name in st.session_state.docs:
            col1, col2 = st.columns([4, 1])
            col1.write(f"- {name}")
            if col2.button("x", key=f"del_{name}"):
                del st.session_state.docs[name]
                st.rerun()

    if st.button("Clear all", use_container_width=True):
        st.session_state.docs = {}
        st.session_state.result = None
        st.rerun()

# ── Main ────────────────────────────────────────────────────────────────────────

st.title("Policy Summarizer")
st.caption("Upload dense policy documents — get plain-language summaries, key actions, and side-by-side comparisons.")

if not ready:
    st.info("Enter your API key in the sidebar to get started.")
    st.stop()

if not st.session_state.docs:
    st.info("Upload a PDF or paste policy text in the sidebar.")
    st.stop()

col_run, col_dl = st.columns([3, 1])

with col_run:
    if st.session_state.mode == "summarize":
        doc_name = st.selectbox("Select document to summarize", list(st.session_state.docs.keys()))
        run_label = "Summarize"
    else:
        if len(st.session_state.docs) < 2:
            st.warning("Load at least 2 documents to compare.")
            st.stop()
        run_label = f"Compare {len(st.session_state.docs)} documents"

if st.button(run_label, type="primary", use_container_width=True):
    with st.spinner("Analysing..."):
        try:
            if st.session_state.mode == "summarize":
                result = summarise(
                    st.session_state.docs[doc_name],
                    st.session_state.client,
                    st.session_state.provider,
                )
            else:
                result = compare(
                    st.session_state.docs,
                    st.session_state.client,
                    st.session_state.provider,
                )
            st.session_state.result = result
        except RuntimeError as e:
            st.error(str(e))

if st.session_state.result:
    st.divider()
    st.markdown(
        f'<div class="badge">{"Summary" if st.session_state.mode == "summarize" else "Comparison"}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(st.session_state.result)
    st.download_button(
        "Download as Markdown",
        data=st.session_state.result,
        file_name="policy_summary.md",
        mime="text/markdown",
    )
