from baml_client.types import Form
from prettytable import PrettyTable
from termcolor import colored


def print_form(form: Form):
    table = PrettyTable()
    table.field_names = ["Field", "Value"]
    table.add_row(["Leave Type", form.leaveType or colored("missing", "yellow")])
    table.add_row(["From Date", form.fromDate or colored("missing", "yellow")])
    table.add_row(["To Date", form.toDate or colored("missing", "yellow")])
    table.add_row(["Reason", form.reason or colored("missing", "yellow")])
    table.add_row(
        [
            "Salary Advance",
            (
                form.salaryAdvance
                if form.salaryAdvance is not None
                else colored("missing", "yellow")
            ),
        ]
    )
    table.add_row(["Confidence", form.confidence or colored("missing", "yellow")])
    print(table)
