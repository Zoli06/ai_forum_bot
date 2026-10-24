import json

from dotenv import load_dotenv

from commands import COMMANDS, CommandPlan, Command
from gemini import gemini
from lemmy import post

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


    # COMMANDS = [
    #     {
    #         "name": "post",
    #         "params": Post.model_json_schema()
    #     },
    #     {
    #         "name": "comment_to_post",
    #         "params": CommentToPost.model_json_schema()
    #     },
    #     {
    #         "name": "comment_to_comment",
    #         "params": CommentToComment.model_json_schema()
    #     },
    #     {
    #         "name": "vote_post",
    #         "params": VotePost.model_json_schema()
    #     },
    #     {
    #         "name": "vote_comment",
    #         "params": VoteComment.model_json_schema()
    #     }
    # ]

    for command in command_plan.commands:
        match command.name:
            case "post":
                post(command.parameters["title"], command.parameters["content"])



start()

# def create_post(community_id):
#     interaction = gemini.interactions.create(
#         model="gemini-3.8-flash",
#         input="What is dead internet theory? Create a post about it",
#         response_format={
#             "type": "text",
#             "mime_type": "application/json",
#             "schema": Post.model_json_schema()
#         }
#     )
#     print(interaction.output_text)
#
#     post = Post.model_validate_json(interaction.output_text)
#
#     post = lemmy.post.create(
#         community_id,
#         post.title,
#         body=post.body
#     )
#     print("Post created")
#
#     return post["post_view"]["post"]["id"]
#
# def write_comment(post_id):
#     post = lemmy.post.get(post_id)
#     title = post["post_view"]["post"]["name"]
#     body = post["post_view"]["post"]["body"]
#
#     post_json = {
#         "title": title,
#         "body": body
#     }
#
#     interaction = gemini.interactions.create(
#             model="gemini-3.8-flash",
#             input="Write a comment to this post: " + json.dumps(post_json),
#             response_format={
#                 "type": "text",
#                 "mime_type": "application/json",
#                 "schema": Comment.model_json_schema()
#             }
#         )
#     print(interaction.output_text)
#
#     comment = Comment.model_validate_json(interaction.output_text)
#
#     comment = lemmy.comment.create(
#         post_id=post_id,
#         content=comment.content
#     )
#
#     return comment["comment_view"]["comment"]["id"]
#
# def vote_post(post_id):
#     post = lemmy.post.get(post_id)
#     title = post["post_view"]["post"]["name"]
#     body = post["post_view"]["post"]["body"]
#
#     post_json = {
#         "title": title,
#         "body": body
#     }
#
#     interaction =gemini.interactions.create(
#         model="gemini-3.8-flash",
#         input="Vote this post: " + json.dumps(post_json),
#         response_format={
#             "type": "text",
#             "mime_type": "application/json",
#             "schema": Vote.model_json_schema()
#         }
#     )
#
#     vote = Vote.model_validate_json(interaction.output_text)
#     lemmy.post.like(post_id, score=1 if vote.vote else -1)
#
# create_post(community_id)

# 15