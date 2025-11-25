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
    salvate = 0

    for post in subreddit.top(time_filter='month', limit=1000):
        content = post.selftext.strip()
        if not content:
            continue  # sărim peste postări fără conținut

        byte_length = len(content.encode('utf-8'))
        if byte_length > 5000:
            continue  # prea lung

        print("\n" + "="*80)
        print(content)
        print(f"TITLU: {post.title.strip()}\n")

        print("="*80)
        alegere = input("Păstrezi această poveste? (y/n): ").strip().lower()

        if alegere == 'y':
            results.append({
                'title': post.title.strip(),
                'content': content
            })
            salvate += 1

        if salvate == nr_povesti:
            break

    with open('stories.json', 'w', encoding='utf-8') as outfile:
        json.dump(results, outfile, ensure_ascii=False, indent=4)

    print(f"\n✅ S-au salvat {salvate} povești din r/{subreddit_name} în stories.json.")
