import json
import os

from dotenv import load_dotenv
from pythorhead import Lemmy

load_dotenv()

lemmy = Lemmy("https://lemmy.cs-z.hu")
print(os.getenv("PASSWORD"))
lemmy.log_in(os.getenv("LEMMY_USERNAME"), os.getenv("LEMMY_PASSWORD"))
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

def post(community_id, title, body):
    post = lemmy.post.create(
        community_id,
        title,
        body=body
    )
    print("Post created")

    return post["post_view"]["post"]["id"]

def comment_to_post(post_id, comment):
    comment = lemmy.comment.create(
        post_id=post_id,
        content=comment.content
    )

    return comment["comment_view"]["comment"]["id"]

def comment_to_comment(post_id, comment_id, comment):
    comment = lemmy.comment.create(
        post_id=post_id,
        parent_id=comment_id,
        content=comment
    )


