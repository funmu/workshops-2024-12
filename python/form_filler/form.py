from baml_client import b
from baml_client.types import Action, Form, Message, UpdateForm
from . import utils


def terminal_app():
    print("Hello from form-filler!")
    current_form = Form(leaveType=None, confidence=None)
    messages = []
    while True:
        res = b.Chat(current_form, messages)
        if isinstance(res, Action):
            if res.action == "cancel":
                print("Form filling cancelled.")
                return
        elif isinstance(res, UpdateForm):
            current_form = res.form
            utils.print_form(current_form)
            if res.completed:
                print("Thanks for submitting!")
                return
            next_question = res.next_question or "Does that look ok?"
            messages.append(Message(role="assistant", content=next_question))
            response = input("User: ")
            messages.append(
                Message(
                    content=response,
                    role="user",
                )
            )
        else:
            print("Bot:", res.message)
            response = input("User: ")
            messages.append(Message(role="assistant", content=res.message))
            messages.append(
                Message(
                    content=response,
                    role="user",
                )
            )


if __name__ == "__main__":
    terminal_app()
