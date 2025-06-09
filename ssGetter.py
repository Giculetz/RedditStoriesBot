from playwright.sync_api import sync_playwright
import praw

# Configurare praw pentru Reddit (exemplu)
reddit = praw.Reddit(
    client_id="QGdCFtHEuz-06ew8HwuOPA",
    client_secret="_kjzljdxMm00UkkWOuHLv6z61hlGeA",
    user_agent="Reddit Stories",
)

def capture_reddit_post_screenshot(url, output_path):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # browser headless
        page = browser.new_page()
        page.goto(url)

        # Așteaptă să se încarce postarea (poți ajusta selectorul)
        page.wait_for_selector("div[data-test-id='post-content']", timeout=10000)

        # Selectează elementul postării
        post_element = page.query_selector("div[data-test-id='post-content']")

        if post_element:
            post_element.screenshot(path=output_path)
            print(f"Screenshot salvat la {output_path}")
        else:
            print("Postarea nu a fost găsită pe pagină.")

        browser.close()

# Obține cele mai bune 5 postări din r/stories luna asta
subreddit_name = 'stories'
posts = reddit.subreddit(subreddit_name).top(time_filter='month', limit=5)

# Ia URL-ul primei postări și fă screenshot
for i, post in enumerate(posts, start=1):
    reddit_url = "https://www.reddit.com" + post.permalink
    print(f"Post {i}: {reddit_url}")
    # output_file = f"PostImage/reddit_post_{i}.png"
    # capture_reddit_post_screenshot(reddit_url, output_file)
