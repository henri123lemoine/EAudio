import requests
from bs4 import BeautifulSoup
import urllib.parse
import re


def get_text(url: str, save_path: str=None, print_bool: bool=False) -> str:
    """
    :param url: the url of the text
    :param save_path: the path to save the text to; if None, it won't save it
    :param print_bool: whether to print the text
    :return: the text
    """
    parsed_link = urllib.parse.urlparse(url)
    if parsed_link.netloc == "www.lesswrong.com":
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
        page = requests.get(url, headers=headers).text
    elif parsed_link.netloc == "www.alignmentforum.org" or parsed_link.netloc == "forum.effectivealtruism.org":
        page = requests.get(url).text
    
    soup = BeautifulSoup(page, "html.parser")

    title = soup.find("a", {"class": "PostsPageTitle-link"}).text.replace(":", "-").replace("/", "_").replace("\\", "_").replace("<", "(").replace(">", ")").replace("*", "").replace("?", "").replace("|", "#")
    authors = ", ".join([t.text for t in soup.find_all("span", {"class": "PostsAuthors-authorName"})])
    read_time = soup.find("span", {"class": "PostsPagePostHeader-wordCount"}).text
    date = soup.find("span", {"class": "PostsPageDate-date"}).text
    tags = "Tags: " + ", ".join([t.text for t in soup.find("span", {"class": "FooterTagList-root"}).find_all("span", {"class": "FooterTag-name"})])
    raw_text = soup.find("div", {"class": "PostsPage-postContent instapaper_body ContentStyles-base content ContentStyles-postBody"}).find_all(["p", "li", "h1", "h2", "h3", "h4", "h5", "h6"])

    text = ""
    for t in raw_text:
        if t.name == "li":
            text += f"- {t.text}\n"
        if t.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            text += f"\n<{t.text}>\n"
        if t.name == "p":
            text += f"{t.text}\n"

    text = f"{title}, by {authors}\nPosted on {date} - {read_time}\n{tags}\n\n{text}"

    if print_bool:
        print(text)
    
    if save_path is not None:
        with open(f"{save_path}/{title}.txt", "w", encoding="utf-8") as f:
            f.write(text)
    
    # Modifications: they should each make it easier to listen to the audio; DM me on discord if you have any suggestions for other modifications
    mod_dict = {"/": "slash", "arxiv": "archive", "arXiv": "archive"}
    pattern_dict = {r"(~)(\d+)": r"roughly \2", r"([A-Z]{2,})": lambda x: ".".join(x.group(1)) + "."}
    # ~400 -> roughly 400; "AIGS" -> "A.I.G.S."

    for k, v in mod_dict.items():
        text = text.replace(k, v)
    for k, v in pattern_dict.items():
        text = re.sub(k, v, text)

    return text