import requests
from bs4 import BeautifulSoup
import urllib.parse
from datetime import datetime
import re
import markdownify
import markdownify
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class Text:
    def __init__(self, url: str, path=None, max_attempts: int=5):
        self.url = url
        self.path = path
        self.max_attempts = max_attempts

        self.title = None
        self.author = None
        self.date = None
        self.string = None

        self.parsed_link = urllib.parse.urlparse(url)
        
        if path:
            self.get_info_txt()
        elif self.parsed_link.netloc == 'www.lesswrong.com' or self.parsed_link.netloc == 'www.alignmentforum.org' or self.parsed_link.netloc == 'forum.effectivealtruism.org':
            self.get_text_lw_eaf_af()
        elif self.parsed_link.netloc == 'www.gwern.net':
            self.get_info_gwern()
        elif '.'.join(self.parsed_link.netloc.split('.')[1:]) == 'substack.com':
            self.get_info_substack()
        elif self.parsed_link.netloc == 'arbital.com':
            self.get_info_arbital()
        else:
            print(f'URL {url} is not yet supported. Using default technique, format might be off.')
            self.get_info_default()
        
    def get_text_lw_eaf_af(self):
        if self.parsed_link.netloc == 'www.lesswrong.com':
            headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
            self.page = requests.get(self.url, headers=headers).text
        else:
            self.page = requests.get(self.url).text
        self.soup = BeautifulSoup(self.page, 'html.parser')

        self.title = self.soup.h1.string
        self.header = self.soup.find("div", {"class": "PostsPagePostHeader-secondaryInfo"})
        self.author = self.header.find("a", {"class": "UsersNameDisplay-userName"}).text
        self.date = self.header.find("span", {"class": "PostsPageDate-date"}).text.split()
        months = {'Jan': 'January', 'Feb': 'February', 'Mar': 'March', 'Apr': 'April', 'May': 'May', 'Jun': 'June', 'Jul': 'July', 'Aug': 'August', 'Sep': 'September', 'Oct': 'October', 'Nov': 'November', 'Dec': 'December'}
        self.date = f"{months[self.date[1]]} {self.date[0]}, {self.date[2]}"

        self.tags = self.soup.find("span", {"class": "FooterTagList-root"}).find_all("span", {"class": "FooterTag-name"})
        self.tags = ", ".join([t.text for t in self.tags])

        self.body = self.soup.find("span", {"class": "commentOnSelection"})
        
        a_tags = self.body.find_all("a")
        for element in a_tags:
            element.replace_with(element.text)
        
        self.body = markdownify.markdownify(str(self.body), heading_style='atx')

        if self.parsed_link.netloc == 'www.lesswrong.com':
            self.site = "LessWrong dot com"
        elif self.parsed_link.netloc == 'www.alignmentforum.org':
            self.site = "the Alignment Forum"
        elif self.parsed_link.netloc == 'forum.effectivealtruism.org':
            self.site = "the Effective Altruism Forum"
        
        self.outro = f"""This was '{self.title}' by {self.author}. Thank you for listening."""

        self.string = f"<speak>{self.title}, by {self.author}.\n---\nPosted on {self.site} on {self.date}\n---\nTags: {self.tags}\n---\n{self.body}\n---\n{self.outro}</speak>"

    def get_info_gwern(self):
        self.page = requests.get(self.url).text
        self.soup = BeautifulSoup(self.page, 'html.parser')

        self.title = self.soup.h1.string        
        self.author = "Gwern Branwen"
        dates = self.soup.find(id="page-date-range").text.split('???')
        start_date = datetime.strptime(dates[0], '%Y-%m-%d')
        end_date = datetime.strptime(dates[1], '%Y-%m-%d')
        start_month = start_date.strftime('%B')
        end_month = end_date.strftime('%B')
        self.date = f"Written from {start_month} {start_date.day}, {start_date.year}, to {end_month} {end_date.day}, {end_date.year}."

        self.body = self.soup.find("div", {"id": "markdownBody", "class": "markdownBody"})
        
        to_delete = self.body.find_all(id=['see-also', 'external-links', 'appendix', 'appendices', 'footnotes', 'backlinks-section', 'link-bibliography-section', 'similars-section']) + self.body.find_all('noscript')
        for element in to_delete:
            element.decompose()
        
        bold_elements = self.body.find_all(['b', 'strong'])
        italic_elements = self.body.find_all(['i', 'em'])
        sup_tags = self.body.find_all('sup')
        blockquotes = self.body.find_all('blockquote')
        a_tags = self.body.find_all('a')

        

        for element in a_tags:
            element.replace_with(element.text)
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
        
        
        self.markdown = markdownify.markdownify(str(self.body), heading_style='atx')
        self.markdown = self.markdown.replace('*', '').replace('#', '')
            
        self.outro = f"""This was '{self.title}' by {self.author}. Thank you for listening."""

        self.string = f"<speak>{self.title}, by {self.author}.\n---\n{self.date}\n---\n{self.markdown}\n---\n{self.outro}</speak>"

    def get_info_substack(self):
        self.page = requests.get(self.url).text
        self.soup = BeautifulSoup(self.page, 'html.parser')

        self.header = self.soup.find("div", {"class": "post-header"})
        self.title = self.header.h1.string
        self.subtitle = self.header.h3.string
        self.author = self.soup.find("a", {"class": "navbar-title-link"}).text
        self.date = self.header.time.text
        if self.date.split()[-1] != 'ago':
            self.date = f"on {self.date}"

        self.body = self.soup.find("div", {"class": "body markup"})

        a_tags = self.body.find_all('a')
        for element in a_tags:
            element.replace_with(element.text)
        blockquote_tags = self.body.find_all('blockquote')
        for element in blockquote_tags:
            quote_text = "\n".join([paragraph.text for paragraph in element.find_all("p")])
            element.replace_with(f"Quote.\n{quote_text}\nUnquote.\n")
        img_tags = self.body.find_all("div", {"class": "captioned-image-container"})
        for element in img_tags:
            caption = element.find("figcaption")
            if caption:
                caption = caption.text
                element.replace_with(f"Image caption: {caption}\n")
            else:
                element.replace_with("Image.\n")
        self.markdown = markdownify.markdownify(str(self.body), heading_style='atx')

        self.markdown = self.markdown.replace('*', '').replace('#', '')
        
        self.outro = f"""This was '{self.title}' by {self.author}. Thank you for listening."""

        self.string = f"<speak>\nTitle: {self.title}.\n{self.subtitle}.\nPosted on {self.author} {self.date}.\n{self.markdown}\n{self.outro}\n</speak>"

    def get_info_arbital(self):
        
        print(f"This does not work with high consistency. If it doesn't work, try again in a few minutes.")

        options = webdriver.ChromeOptions()
        options.add_argument('start-maximized')
        options.add_argument('disable-infobars')
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("excludeSwitches",["enable-automation"])

        driver = webdriver.Chrome(chrome_options=options)

        for i in range(self.max_attempts):
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//span[@class='ng-binding ng-scope']"))
                )
                self.title = element.text
                self.soup = BeautifulSoup(driver.page_source, 'html.parser')
                break
            except Exception:
                print(f"Attempt {i+1} failed. Retrying...")
                time.sleep(1)
        driver.close()

        self.body = self.soup.find("div", {"class": "lens-text-container"})

        a_tags = self.body.find_all("a")
        for a in a_tags:
            a.replace_with(a.text)
        caption = self.body.find("div", {"class": "md-caption ng-scope"})
        caption.decompose()
        answers = self.body.find_all("div", {"class": "hidden-text display-none"})
        for answer in answers:
            answer.replace_with(f"Press pause to think of an answer....{'tic....tock....'*4}.........Answer: {answer.text}")
        sup = self.body.find_all("span", {"class": "markdown-note ng-isolate-scope"})
        for element in sup:
            element.decompose()

        self.markdown = markdownify.markdownify(str(self.body), heading_style="ATX")
        self.markdown = self.markdown.replace('*', '').replace('#', '')

        outro = f"""This was '{self.title}'. Thank you for listening."""

        self.string = f"<speak>\n{self.markdown}\n{outro}\n</speak>"

    def get_info_txt(self):
        self.title = self.path.split('/')[-1].split('.')[0]
        with open(self.path, 'r', encoding='utf-8') as f:
            self.string = f.read()
    
    def get_info_default(self):
        self.page = requests.get(self.url).text
        self.soup = BeautifulSoup(self.page, 'html.parser')
        
        try:
            self.soup = self.soup.find("body")
        except:
            pass
        
        a_tags = self.soup.find_all('a')
        for element in a_tags:
            element.replace_with(element.text)
        
        self.markdown = markdownify.markdownify(str(self.soup), heading_style='atx')
        self.markdown = self.markdown.replace('*', '').replace('#', '')
        
        try:
            self.title = self.soup.title.string
        except:
            self.title = "Untitled"
        
        self.string = f"<speak>\n{self.title}.\n{self.markdown}\n</speak>"
        
    def __str__(self):
        return self.string


if __name__ == "__main__":
    # Test class

    urls_to_test = [
        "https://www.lesswrong.com/posts/vzfz4AS6wbooaTeQk/staring-into-the-abyss-as-a-core-life-skill", # Lesswrong
        "https://forum.effectivealtruism.org/posts/oGdCtvuQv4BTuNFoC/good-things-that-happened-in-ea-this-year", # EA Forum
        "https://www.alignmentforum.org/posts/JSkqkgYcyYt8oHsFi/large-language-models-can-provide-normative-assumptions-for", # Alignment Forum
        "https://www.gwern.net/Melatonin", # Gwern
        "https://astralcodexten.substack.com/p/sorry-i-still-think-i-am-right-about", # Substack
        #"https://arbital.com/p/bayes_rule", # Arbital (doesn't work)
        "https://en.wikipedia.org/wiki/Intuitionistic_logic", # Wikipedia (doesn't work)
        "https://www.reddit.com/r/rational/comments/101em0c/d_monday_request_and_recommendation_thread/", # Reddit (doesn't work)
    ]

    full_text = ""
    for url in urls_to_test:
        print(f"Getting text for {url}")
        text = Text(url)
        full_text += str(text) + "\n"*15
        print(f"Added text for {url}")
    
    with open("test.txt", "w", encoding="utf-8") as f:
        f.write(full_text)

    print("Test ran successfully. Check test.txt for results.")