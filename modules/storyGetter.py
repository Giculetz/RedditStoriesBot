import praw
import json

sub_redits = ['stories', 'AITAH', 'nosleep', 'tifu']

def story_getter(nr_povesti, sub_index):
    reddit = praw.Reddit(
        client_id="QGdCFtHEuz-06ew8HwuOPA",
        client_secret="_kjzljdxMm00UkkWOuHLv6z61hlGeA",
        user_agent="Reddit Stories",
    )

    subreddit_name = sub_redits[sub_index]
    subreddit = reddit.subreddit(subreddit_name)

    results = []
    count = 0

    # Iterăm peste un număr mare de postări (de ex. 1000) ca să avem destule valide
    for post in subreddit.top(time_filter='month', limit=1000):
        content = post.selftext.strip()
        if not content:
            continue  # Sărim peste postările fără text (ex: doar titlu sau linkuri)

        byte_length = len(content.encode('utf-8'))
        if byte_length > 5000:
            continue  # Prea lung

        results.append({
            'title': post.title.strip(),
            'content': content
        })
        count += 1

        if count == nr_povesti:
            break

    with open('stories.json', 'w', encoding='utf-8') as outfile:
        json.dump(results, outfile, ensure_ascii=False, indent=4)

    print(f"S-au salvat {count} povești din r/{subreddit_name} (max 5000 bytes fiecare).")

