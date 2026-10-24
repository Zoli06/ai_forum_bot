import json

from dotenv import load_dotenv

from commands import COMMANDS, CommandPlan, Command
from gemini import gemini
from lemmy import post, comment_to_post, comment_to_comment

load_dotenv()

def start():


    model_input = (
    f"""
    Your task is to deny the dead internet theory.
    Interact on a forum and act like a human while and convince people that all interaction is human.
    You can send multiple commands.
    Available commands: {json.dumps(COMMANDS)}
    """
    )

    interaction = gemini.interactions.create(
        model="gemini-3.8-flash",
        input=model_input,
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": CommandPlan.model_json_schema()
        }
    )

    command_plan = CommandPlan.model_validate_json(interaction.output_text)

    for command in command_plan.commands:
        match command.name:
            case "post":
                post(command.parameters["title"], command.parameters["body"])
            case "comment_to_post":
                comment_to_post(command.parameters["post_id"], command.parameters["content"])
            case "comment_to_comment":
                comment_to_comment(command.parameters["post_id"], command.parameters["comment_id"], command.parameters["content"])
            case _:
                print("ezt mar ti csinaljatok")

start()
