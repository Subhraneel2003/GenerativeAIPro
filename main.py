import streamlit as st
import os
from datetime import datetime
import time
from agents.project_lead import ProjectLead
from agents.business_analyst import BusinessAnalyst
from agents.design_agent import DesignAgent
from agents.developer_agent import Developer
from agents.testing_agent import Tester
from utils.database import ChromaManager
from utils.templates import get_template

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "project_name" not in st.session_state:
    st.session_state.project_name = ""
if "requirements" not in st.session_state:
    st.session_state.requirements = ""
if "current_phase" not in st.session_state:
    st.session_state.current_phase = "setup"
if "artifacts" not in st.session_state:
    st.session_state.artifacts = {
        "user_stories": [],
        "design_doc": "",
        "code": {},
        "test_cases": [],
        "test_results": []
    }
if "db_manager" not in st.session_state:
    st.session_state.db_manager = ChromaManager()

# App layout and styling
st.set_page_config(page_title="AI Development Pod", layout="wide")
st.title("AI-Powered Virtual Development Pod")

# Sidebar for project info and navigation
with st.sidebar:
    st.header("Project Dashboard")
    
    if st.session_state.current_phase == "setup":
        st.session_state.project_name = st.text_input("Project Name")
        st.session_state.requirements = st.text_area("High-Level Business Requirements", height=300)
        
        if st.button("Initialize Project"):
            if st.session_state.project_name and st.session_state.requirements:
                st.session_state.current_phase = "requirements"
                st.session_state.db_manager.store_requirements(
                    st.session_state.project_name, 
                    st.session_state.requirements
                )
                st.rerun()
            else:
                st.error("Please provide both project name and requirements")
    else:
        st.write(f"**Project:** {st.session_state.project_name}")
        
        # Navigation buttons for different phases
        phases = ["requirements", "design", "development", "testing", "chat"]
        current_index = phases.index(st.session_state.current_phase)
        
        col1, col2 = st.columns(2)
        with col1:
            if current_index > 0:
                if st.button("← Previous Phase"):
                    st.session_state.current_phase = phases[current_index - 1]
                    st.rerun()
        with col2:
            if current_index < len(phases) - 1:
                if st.button("Next Phase →"):
                    st.session_state.current_phase = phases[current_index + 1]
                    st.rerun()
        
        st.divider()
        
        # Phase selection
        st.header("Phases")
        for phase in phases:
            if st.session_state.current_phase == phase:
                st.markdown(f"**▶ {phase.capitalize()}**")
            else:
                if st.button(phase.capitalize()):
                    st.session_state.current_phase = phase
                    st.rerun()

# Main area based on current phase
if st.session_state.current_phase == "requirements":
    st.header("Requirements Analysis")
    
    with st.expander("Business Requirements", expanded=True):
        st.write(st.session_state.requirements)
    
    with st.spinner("Business Analyst is generating user stories..."):
        if not st.session_state.artifacts["user_stories"]:
            ba_agent = BusinessAnalyst()
            user_stories = ba_agent.generate_user_stories(st.session_state.requirements)
            st.session_state.artifacts["user_stories"] = user_stories
            st.session_state.db_manager.store_user_stories(
                st.session_state.project_name, 
                user_stories
            )
    
    st.subheader("User Stories")
    for i, story in enumerate(st.session_state.artifacts["user_stories"]):
        with st.expander(f"User Story #{i+1}: {story['title']}", expanded=i==0):
            st.markdown(f"**As a** {story['role']}")
            st.markdown(f"**I want** {story['want']}")
            st.markdown(f"**So that** {story['so_that']}")
            st.markdown("**Acceptance Criteria:**")
            for criterion in story['acceptance_criteria']:
                st.markdown(f"- {criterion}")

elif st.session_state.current_phase == "design":
    st.header("System Design")
    
    with st.expander("User Stories Reference", expanded=False):
        for i, story in enumerate(st.session_state.artifacts["user_stories"]):
            st.markdown(f"**User Story #{i+1}:** {story['title']}")
    
    with st.spinner("Design Agent is creating system design..."):
        if not st.session_state.artifacts["design_doc"]:
            design_agent = DesignAgent()
            design_doc = design_agent.create_design(
                st.session_state.requirements,
                st.session_state.artifacts["user_stories"]
            )
            st.session_state.artifacts["design_doc"] = design_doc
            st.session_state.db_manager.store_design_doc(
                st.session_state.project_name, 
                design_doc
            )
    
    st.subheader("System Design Document")
    st.markdown(st.session_state.artifacts["design_doc"])

elif st.session_state.current_phase == "development":
    st.header("Development")
    
    tab1, tab2 = st.tabs(["References", "Code Generation"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            with st.expander("User Stories", expanded=False):
                for i, story in enumerate(st.session_state.artifacts["user_stories"]):
                    st.markdown(f"**User Story #{i+1}:** {story['title']}")
        with col2:
            with st.expander("Design Document", expanded=False):
                st.markdown(st.session_state.artifacts["design_doc"])
    
    with tab2:
        if not st.session_state.artifacts["code"]:
            st.subheader("Generating Code")
            with st.spinner("Developer Agent is writing code..."):
                dev_agent = Developer()
                code_files = dev_agent.generate_code(
                    st.session_state.artifacts["user_stories"],
                    st.session_state.artifacts["design_doc"]
                )
                st.session_state.artifacts["code"] = code_files
                st.session_state.db_manager.store_code(
                    st.session_state.project_name, 
                    code_files
                )
                st.rerun()
        else:
            st.subheader("Generated Code")
            for filename, code in st.session_state.artifacts["code"].items():
                with st.expander(filename, expanded=False):
                    st.code(code)

elif st.session_state.current_phase == "testing":
    st.header("Testing")
    
    tab1, tab2, tab3 = st.tabs(["References", "Test Cases", "Test Execution"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            with st.expander("User Stories", expanded=False):
                for i, story in enumerate(st.session_state.artifacts["user_stories"]):
                    st.markdown(f"**User Story #{i+1}:** {story['title']}")
            with st.expander("Design Document", expanded=False):
                st.markdown(st.session_state.artifacts["design_doc"])
        with col2:
            with st.expander("Code Files", expanded=False):
                for filename, code in st.session_state.artifacts["code"].items():
                    st.markdown(f"**{filename}**")
    
    with tab2:
        if not st.session_state.artifacts["test_cases"]:
            st.subheader("Generating Test Cases")
            with st.spinner("Testing Agent is creating test cases..."):
                test_agent = Tester()
                test_cases = test_agent.create_test_cases(
                    st.session_state.artifacts["user_stories"],
                    st.session_state.artifacts["design_doc"],
                    st.session_state.artifacts["code"]
                )
                st.session_state.artifacts["test_cases"] = test_cases
                st.session_state.db_manager.store_test_cases(
                    st.session_state.project_name, 
                    test_cases
                )
                st.rerun()
        else:
            st.subheader("Test Cases")
            for i, test in enumerate(st.session_state.artifacts["test_cases"]):
                with st.expander(f"Test #{i+1}: {test['title']}", expanded=(i==0)):
                    st.markdown(f"**Description:** {test['description']}")
                    st.markdown("**Test Steps:**")
                    for j, step in enumerate(test['steps']):
                        st.markdown(f"{j+1}. {step}")
                    st.markdown(f"**Expected Result:** {test['expected_result']}")
    
    with tab3:
        if not st.session_state.artifacts["test_results"]:
            if st.button("Execute Tests"):
                with st.spinner("Testing Agent is executing tests..."):
                    test_agent = Tester()
                    test_results = test_agent.execute_tests(
                        st.session_state.artifacts["test_cases"],
                        st.session_state.artifacts["code"]
                    )
                    st.session_state.artifacts["test_results"] = test_results
                    st.session_state.db_manager.store_test_results(
                        st.session_state.project_name, 
                        test_results
                    )
                    st.rerun()
        else:
            st.subheader("Test Results")
            
            passed = sum(1 for result in st.session_state.artifacts["test_results"] if result["status"] == "PASS")
            total = len(st.session_state.artifacts["test_results"])
            pass_rate = (passed / total) * 100 if total > 0 else 0
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Tests", total)
            col2.metric("Tests Passed", passed)
            col3.metric("Pass Rate", f"{pass_rate:.1f}%")
            
            for i, result in enumerate(st.session_state.artifacts["test_results"]):
                status_color = "green" if result["status"] == "PASS" else "red"
                with st.expander(
                    f"Test #{i+1}: {result['title']} - {result['status']}", 
                    expanded=(result["status"] == "FAIL")
                ):
                    st.markdown(f"**Status:** :{status_color}[{result['status']}]")
                    st.markdown(f"**Description:** {result['description']}")
                    if result["status"] == "FAIL":
                        st.markdown(f"**Error Details:** {result['details']}")

elif st.session_state.current_phase == "chat":
    st.header("Project Manager Chat")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Input for new messages
    if prompt := st.chat_input("Ask Project Manager about the project..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        # Generate project lead response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                project_lead = ProjectLead()
                response = project_lead.respond(
                    prompt,
                    st.session_state.project_name,
                    st.session_state.requirements,
                    st.session_state.artifacts
                )
                st.write(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})