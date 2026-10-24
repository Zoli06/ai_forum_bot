from typing import Any

from pydantic import BaseModel, Field


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