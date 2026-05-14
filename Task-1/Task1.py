import requests
import json

url = "https://jsonplaceholder.typicode.com/posts"
required_keys = {"userId", "id", "title", "body"}

response = requests.get(url)

assert response.status_code == 200, f"Expected 200, got {response.status_code}"
print(f"Status code: {response.status_code} - OK")

posts = response.json()

# check each post has the expected keys
for post in posts:
    missing = required_keys - post.keys()
    if missing:
        print(f"Post {post['id']} is missing keys: {missing}")

print(f"Schema validation passed for all {len(posts)} posts")

with open("first_5_posts.json", "w") as f:
    json.dump(posts[:5], f, indent=4)

print("Saved first 5 posts to first_5_posts.json")