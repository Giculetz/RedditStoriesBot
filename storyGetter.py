import praw
import json

reddit = praw.Reddit(
    client_id="QGdCFtHEuz-06ew8HwuOPA",
    client_secret="_kjzljdxMm00UkkWOuHLv6z61hlGeA",
    user_agent="Reddit Stories",
)

subreddit_name = 'stories'

posts = reddit.subreddit(subreddit_name).top(time_filter='month', limit=5)

results = []

for post in posts:
    results.append(
        {
            'title': post.title,
            'content': post.selftext
        }
    )

with open('stories.json', 'w',encoding='utf-8') as outfile:
    json.dump(results, outfile, ensure_ascii=False,indent=4)

print("s-a salvat 5 povesti maestre\n")