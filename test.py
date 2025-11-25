import re


def reduce_text(text):
    while len(text) > 100:
        # Caută toate cuvintele de forma #ceva la finalul stringului
        hashtags = re.findall(r'#\w+', text)
        if not hashtags:
            break  # dacă nu mai există hashtaguri, ieși
        last_hashtag = hashtags[-1]
        # elimină ultimul hashtag (doar dacă e la final sau urmat de spațiu)
        if text.endswith(' ' + last_hashtag):
            text = text[:text.rfind(' ' + last_hashtag)]
        elif text.endswith(last_hashtag):
            text = text[:text.rfind(last_hashtag)]
        else:
            text=text[:-1]
    return text


titlu="AITAH for telling a woman at the gym the truth? PART 2 #reddit #redditstories #askreddit #asshole #story #stories "
titlu=reduce_text(titlu)
print(titlu)