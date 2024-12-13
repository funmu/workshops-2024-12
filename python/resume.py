from baml_client import b
from baml_client.types import Resume


def print_resume(resume: Resume):
    print(f"Name: {resume.name}")
    print(f"Email: {resume.email}")
    print()

    print(f"Experiences: {len(resume.experience)}")
    for experience in resume.experience:
        print(f"• {experience}")
    print()

    print("Skills:")
    for skill in resume.skills:
        print(f"• {skill}")
    print()

    print("Reasons to hire:")
    for reason in resume.reason_to_hire:
        print(f"• {reason.reason}")
    print()


def main():
    content = open("resume.txt", "r").read()
    resume = b.ExtractResume(content)
    print_resume(resume)


if __name__ == "__main__":
    main()
