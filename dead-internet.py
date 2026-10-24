from typing import Literal, Any

from pydantic import BaseModel, Field
from pythorhead import Lemmy
from google import genai
import json

class Post(BaseModel):
    title: str = Field(description="The title of the post")
    body: str = Field(description="The body of the post. Typically between 10-50 words long.")
    
class CommentToPost(BaseModel):
    post_id: str = Field(description="The id of the post")
    content: str = Field(description="The text of the comment")

class CommentToComment(BaseModel):
    comment_id: str = Field(description="The id of the comment")
    content: str = Field(description="The text of the comment")

class VotePost(BaseModel):
    post_id: str = Field(description="The id of the post")
    vote: bool = Field(description="True if upvoted, False if downvoted")

class VoteComment(BaseModel):
    post_id: str = Field(description="The id of the comment")
    vote: bool = Field(description="True if upvoted, False if downvoted")

COMMANDS = [
    {
        "name": "post",
        "params": Post.model_json_schema()
    },
    {
        "name": "comment_to_post",
        "params": CommentToPost.model_json_schema()
    },
    {
        "name": "comment_to_comment",
        "params": CommentToComment.model_json_schema()
    },
    {
        "name": "vote_post",
        "params": VotePost.model_json_schema()
    },
    {
        "name": "vote_comment",
        "params": VoteComment.model_json_schema()
    }
]

class Command(BaseModel):
    name: str = Field(description="The name of the command")
    parameters: dict[str, Any]

class CommandPlan(BaseModel):
    commands: list[Command] = Field(
        min_length=3,
        max_length=8,
        description=(
            "A sequence of 3 to 8 commands. "
            "Include multiple independent actions when appropriate."
        )
    )

gemini = genai.Client(
    api_key="***"
)

#### Lemmy

lemmy = Lemmy("https://lemmy.cs-z.hu")
lemmy.log_in("FaZoltan", "almafa1234")
print("Logged in")

community_id = lemmy.discover_community("dead_internet")
print("Community ID: ", community_id)

def get_comments(post_id):
    result = []
    comments = lemmy.comment.list(post_id=post_id)
    print(json.dumps(comments))

    for comment in comments:
        result.append({
          "id": comment["comment"]["id"],
          "path": comment["comment"]["path"],
          "content": comment["comment"]["content"],
          "score": comment["counts"]["score"]
        })

    return result

def get_latest_posts(community_id):
    result = []
    posts = lemmy.post.list(community_id, limit=10)

    for post in posts:
        result.append({
            "id": post["post"]["id"],
            "name": post["post"]["name"],
            "body": post["post"]["body"],
            "score": post["counts"]["score"],
            "comments": get_comments(post["post"]["id"])
        })

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

    print(command_plan)

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