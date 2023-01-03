import requests
from bs4 import BeautifulSoup
import urllib.parse
from datetime import datetime
import re


class Text:
    def __init__(self, url: str):
        self.url = url
        self.parsed_link = urllib.parse.urlparse(url)

        headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
        self.page = requests.get(url, headers=headers).text
        self.soup = BeautifulSoup(self.page, 'html.parser')

        self.title = None
        self.author = None
        self.date = None
        self.text = None

        if self.parsed_link.netloc == 'www.lesswrong.com' or self.parsed_link.netloc == 'www.alignmentforum.org' or self.parsed_link.netloc == 'forum.effectivealtruism.org':
            self.get_text_lw_eaf_af()
        elif self.parsed_link.netloc == 'www.gwern.net':
            self.get_info_gwern()
        elif '.'.join(self.parsed_link.netloc.split('.')[1:]) == 'substack.com':
            self.get_info_substack()
        elif self.parsed_link.netloc == 'arbital.com':
            self.get_info_arbital()
        else:
            raise ValueError(f'URL {url} is not yet supported.')
        
        outro = f"""This was '{self.title}' by {self.author}. You can find the original post at {self.url}."""
        self.text = f"{self.text}\n\n{outro}"

    def get_text_lw_eaf_af(self):
        self.title = self.soup.find("a", {"class": "PostsPageTitle-link"}).text
        self.author = re.sub(r',([^,]*)$', r' and\1', ", ".join([t.text for t in self.soup.find_all("span", {"class": "PostsAuthors-authorName"})]))
        self.date = self.soup.find("span", {"class": "PostsPageDate-date"}).text
        tags = "Tags: " + ", ".join([t.text for t in self.soup.find("span", {"class": "FooterTagList-root"}).find_all("span", {"class": "FooterTag-name"})])
        raw_text = self.soup.find("div", {"class": "PostsPage-postContent instapaper_body ContentStyles-base content ContentStyles-postBody"}).find_all(["p", "li", "h1", "h2", "h3", "h4", "h5", "h6"])
        text = "\n".join([t.text for t in raw_text])

        self.title = self.title.replace("\n", "").replace(":", "-").replace("/", "_").replace("\\", "_").replace("<", "(").replace(">", ")").replace("*", "").replace("?", "").replace("|", "#")
        self.text = f"{self.title}, by {self.author} on {self.parsed_link.netloc}\nPosted on {self.date}\nTags: {tags}\n\n{text}"

    def get_info_gwern(self):
        self.title = self.soup.h1.string        
        self.author = "Gwern Branwen"
        dates = self.soup.find(id="page-date-range").text.split('–')
        start_date = datetime.strptime(dates[0], '%Y-%m-%d')
        end_date = datetime.strptime(dates[1], '%Y-%m-%d')
        start_month = start_date.strftime('%B')
        end_month = end_date.strftime('%B')
        self.date = f"Written from {start_month} {start_date.day}, {start_date.year}, to {end_month} {end_date.day}, {end_date.year}."

        body = self.soup.find("div", {"id": "markdownBody", "class": "markdownBody"})

        bold_elements = body.find_all(['b', 'strong'])
        italic_elements = body.find_all(['i', 'em'])
        sup_tags = body.find_all('sup')
        blockquotes = body.find_all('blockquote')

        to_delete = body.find_all(id=['see-also', 'external-links', 'appendix', 'appendices', 'footnotes', 'backlinks-section', 'link-bibliography-section', 'similars-section']) + body.find_all('noscript')

        for element in bold_elements:
            element.replace_with('**' + element.text + '**')
        for element in italic_elements:
            element.replace_with('*' + element.text + '*')
        for element in sup_tags:
            element.decompose()
        for i,element in enumerate(blockquotes):
            if i == 0:
                element.replace_with('Abstract' + element.text)
                continue
            element.replace_with('Quote.' + element.text + 'Unquote.')
        for element in to_delete:
            element.decompose()
            
        self.title = self.title.replace("\n", "").replace(":", "-").replace("/", "_").replace("\\", "_").replace("<", "(").replace(">", ")").replace("*", "").replace("?", "").replace("|", "#")
        self.text = f"{self.title}, by {self.author} on {self.parsed_link.netloc}\nDate range: {self.date}\n\n{body.get_text()}"

    def get_info_substack(self):
        self.title = self.soup.title.string
        subtitle = self.soup.find("h3", {"class": "subtitle"}).string
        self.author = "Scott Alexander"
        self.date = self.soup.time.string
        body = self.soup.find("div", {"class": "body markup"})

        bold_elements = body.find_all(['b', 'strong'])
        italic_elements = body.find_all(['i', 'em'])
        sup_tags = body.find_all('sup')
        imgs = body.find_all('picture')
        code = body.find_all('code')
        titles = body.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        blockquotes = body.find_all('blockquote')

        for element in bold_elements:
            element.replace_with('**' + element.text + '**')
        for element in italic_elements:
            element.replace_with('*' + element.text + '*')
        for element in sup_tags:
            element.decompose()
        for element in imgs:
            element.replace_with("\n[IMAGE ATTACHED]\n")
        for element in code:
            element.replace_with("\n`" + element.text + "`\n")
        for element in titles:
            element.replace_with("\n" + element.text + "\n")
        for element in blockquotes:
            element.replace_with('Quote.' + element.text + 'Unquote.')

        self.title = self.title.replace("\n", "").replace(":", "-").replace("/", "_").replace("\\", "_").replace("<", "(").replace(">", ")").replace("*", "").replace("?", "").replace("|", "#")
        self.text = f"{self.title}\n{subtitle}\nby {self.author} on {self.parsed_link.netloc}\nPosted on {self.date}\n\n{body.get_text()}"

    def get_info_arbital(self):
        raise NotImplementedError("Arbital is not supported yet.")
            
    def __str__(self):
        return self.text


if __name__ == "__main__":
    # Test class

    urls_to_test = [
        "https://www.lesswrong.com/posts/vzfz4AS6wbooaTeQk/staring-into-the-abyss-as-a-core-life-skill", # Lesswrong
        "https://forum.effectivealtruism.org/posts/oGdCtvuQv4BTuNFoC/good-things-that-happened-in-ea-this-year", # EA Forum
        "https://www.alignmentforum.org/posts/JSkqkgYcyYt8oHsFi/large-language-models-can-provide-normative-assumptions-for", # Alignment Forum
        "https://www.gwern.net/Melatonin", # Gwern
        "https://astralcodexten.substack.com/p/sorry-i-still-think-i-am-right-about", # Substack
        #"https://arbital.com/p/bayes_rule", # Arbital (not supported yet)
    ]

    full_text = ""
    for url in urls_to_test:
        text = Text(url)
        full_text += str(text) + "\n"*15
    
    with open("test.txt", "w", encoding="utf-8") as f:
        f.write(full_text)

    print("Test ran successfully. Check test.txt for results.")