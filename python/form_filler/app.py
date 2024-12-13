from dataclasses import dataclass
from enum import Enum, auto
import time
from typing import List, Optional, Protocol
import streamlit as st
from baml_client import b
from baml_client.types import Action, Form, Message, UpdateForm


class AppState(Enum):
    FORM_FILLING = auto()
    CANCELED = auto()
    DRAFT = auto()
    SUBMITTED = auto()


@dataclass
class SessionState:
    messages: List[Message]
    current_form: Form
    error: Optional[Exception]
    debug_error: bool
    state: AppState
    needs_response: bool

    @classmethod
    def initial(cls) -> "SessionState":
        return cls(
            messages=[
                Message(
                    role="assistant",
                    content="Hello! I'd love to help you fill out this form.",
                )
            ],
            current_form=Form(leaveType=None, confidence=None),
            error=None,
            debug_error=False,
            state=AppState.FORM_FILLING,
            needs_response=True,
        )


class FormFillerHandler(Protocol):
    def handle_user_input(self, user_input: str) -> None: ...
    def handle_bot_response(self) -> None: ...


class FormFillerUI:
    def __init__(self, handler: FormFillerHandler):
        self.handler = handler
        self.init_session_state()

    @staticmethod
    def init_session_state() -> None:
        if "app_state" not in st.session_state:
            st.session_state.app_state = SessionState.initial()

    def render_chat_history(self) -> None:
        for message in st.session_state.app_state.messages:
            if message.role == "assistant":
                st.write(f"🤖 Bot: {message.content}")
            else:
                st.write(f"👤 You: {message.content}")

    def render_form_state(self) -> None:
        if st.session_state.app_state.current_form:
            state: SessionState = st.session_state.app_state
            st.write("### Vacation Request")
            form = state.current_form

            # Leave Type
            if form.leaveType:
                st.write("**Leave Type:**")
                st.info(form.leaveType.title(), icon="📝")

            # Dates
            col1, col2 = st.columns(2)
            with col1:
                if form.fromDate:
                    st.write("**From:**")
                    st.info(form.fromDate, icon="📅")
            with col2:
                if form.toDate:
                    st.write("**To:**")
                    st.info(form.toDate, icon="📅")

            # Reason
            if form.reason:
                st.write("**Reason:**")
                st.info(form.reason, icon="📝")

            # Salary Advance
            if form.salaryAdvance is not None:
                st.write(
                    "**Salary Advance Requested:** ",
                    "Yes" if form.salaryAdvance else "No",
                )

            # Confidence
            if form.confidence:
                confidence_color = {
                    "high": "green",
                    "medium": "orange",
                    "low": "red",
                }.get(form.confidence, "grey")
                st.markdown(
                    f"**Confidence:** :{confidence_color}[{form.confidence.title()}]"
                )

    def render_error(self) -> None:
        if st.session_state.app_state.error:
            with st.warning("Error: Please try again."):
                with st.expander("Error Details", expanded=True):
                    st.error(f"Error: {st.session_state.app_state.error}")

    def render_user_input(self) -> None:
        user_input = st.text_input("Your response:", key="user_input")
        if st.button("Send"):
            if user_input:
                self.handler.handle_user_input(user_input)

    def render_state_specific_ui(self) -> None:
        state = st.session_state.app_state.state

        if state == AppState.CANCELED:
            st.warning("Form filling cancelled!")
        elif state == AppState.DRAFT:
            st.write("Does this look ok?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Submit"):
                    st.session_state.app_state.state = AppState.SUBMITTED
                    st.rerun()
            with col2:
                if st.button("Edit"):
                    st.session_state.app_state.state = AppState.FORM_FILLING
                    st.rerun()
        elif state == AppState.SUBMITTED:
            st.success("Thanks for submitting!")
            st.stop()

    def render(self) -> None:
        st.title("Form Filler")
        col1, col2 = st.columns([2, 1])

        with col1:
            self.render_chat_history()

            if (
                st.session_state.app_state.needs_response
                and not st.session_state.app_state.error
            ):
                self.handler.handle_bot_response()

            self.render_error()

            if st.session_state.app_state.state == AppState.FORM_FILLING:
                self.render_user_input()

            self.render_state_specific_ui()

        with col2:
            self.render_form_state()


class FormFillerLogic:
    @staticmethod
    def handle_chat(messages: List[Message], form: Form) -> None:
        res = b.Chat(form, messages)
        app_state = st.session_state.app_state

        if isinstance(res, Action):
            if res.action == "cancel":
                app_state.state = AppState.CANCELED
                return

        elif isinstance(res, UpdateForm):
            app_state.current_form = res.form
            if res.completed:
                app_state.state = AppState.DRAFT
            else:
                next_question = res.next_question or "Does that look ok?"
                app_state.messages.append(
                    Message(role="assistant", content=next_question)
                )
            app_state.needs_response = False

        else:
            app_state.messages.append(Message(role="assistant", content=res.message))
            app_state.needs_response = False

    @staticmethod
    def handle_user_message(message: str) -> None:
        app_state = st.session_state.app_state
        app_state.error = None
        app_state.messages.append(Message(role="user", content=message))
        app_state.needs_response = True


class FormFiller:
    def __init__(self):
        self.logic = FormFillerLogic()
        self.ui = FormFillerUI(handler=self)

    def handle_user_input(self, user_input: str) -> None:
        self.logic.handle_user_message(user_input)
        st.rerun()

    def handle_bot_response(self) -> None:
        try:
            self.logic.handle_chat(
                st.session_state.app_state.messages,
                st.session_state.app_state.current_form,
            )
            st.session_state.app_state.error = None
        except Exception as e:
            st.session_state.app_state.error = e

    def run(self) -> None:
        self.ui.render()
