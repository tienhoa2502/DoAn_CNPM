import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse
from collections import Counter
import threading
# URL cần crawl
url = "https://hoayeuthuong.com"


def count_words(url, phrase):
    # Tách cụm từ thành các từ riêng lẻ
    response = requests.get(url)
    html_content = response.content

    # Sử dụng BeautifulSoup để parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    mywords = ""
    elements = elements = soup.find_all(["title", "p", "h1", "h2", "h3", "h4",
                                         "h5", "h6", "a", "span", "div", "section", "article", "img",
                                         "li", "td", "th", "label", "meta", "blockquote", "figcaption",
                                         "q", "table", "tr", "dd", "dt", "dl", "time", "figcaption", "em",
                                         "strong", "b", "i", "u", "s", "code", "pre", "small","option"])
    for element in elements:
        mywords += element.get_text().replace("\n", "").replace("\t", "").replace("\r", "")
        attributes = ["alt", "content", "href", "name", "property", "src", "title"]
        for attribute in attributes:
            if attribute in element.attrs:
                mywords += " " + element[attribute]

    myword_counts = []
    def count_myword(keywords,mywords):
        for keyword in keywords:
            mywords = mywords.lower()
            count = mywords.count(keyword.lower())
            myword_counts.append({
                'word': keyword.lower(),
                'count': count
            })
    result = []
    def get_top10(mywords):
        # Tách cụm từ thành các từ riêng lẻ
        words = mywords.split()
        
        # Đếm số lần xuất hiện của từng từ
        word_counts = Counter(words)
        # Lấy 10 từ xuất hiện nhiều nhất
        top_10_words = word_counts.most_common(10)
        
        # Chuyển đổi kết quả thành danh sách từ điển
        result.extend([{'word': word, 'count': count} for word, count in top_10_words])
    # Tạo các luồng
    thread1 = threading.Thread(target=count_myword(keywords,mywords))
    thread2 = threading.Thread(target=get_top10(mywords))
    
    # Bắt đầu chạy các luồng
    thread1.start()
    thread2.start()
    
    # Đợi cho đến khi các luồng hoàn thành
    thread1.join()
    thread2.join()
    
    return result,myword_counts


list_daVao = []
def get_links(level,url):
    # Tạo danh sách dữ liệu để lưu href và title của các thẻ <a>
    data_list = []
    if level >= 1:
        if url not in list_daVao:
            list_daVao.append(url)
            response = requests.get(url)
            html_content = response.content
        
            # Sử dụng BeautifulSoup để parse HTML
            soup = BeautifulSoup(html_content, 'html.parser')
        
            # Tìm tất cả các thẻ <a> trong HTML và lưu href và title của chúng vào danh sách dữ liệu
            for link in soup.find_all('a'):
                href = link.get('href')
                try:
                    
                    # Nếu href không phải là đường link
                    if not urlparse(href).scheme:
                        # Thêm đường link vào href
                        href = urlunparse((default_scheme, default_netloc, href, '', '', ''))
                        parsed_href = urlparse(href)
                        # Kiểm tra xem href có phải là đường dẫn (path) hay liên kết (link) không
                        if parsed_href.path and parsed_href.netloc:
                            word_count,myword_count = count_words(href,link.text)
                            childrens = get_links(level-1,href)
                            data_list.append({
                                'level': level,
                                'href': href,
                                'title': link.text,
                                'mykeywords': myword_count,
                                'words': word_count,
                                'childrens': childrens
                            })
                    else:
                        parsed_href = urlparse(href)
                        # Kiểm tra xem href có phải là đường dẫn (path) hay liên kết (link) không
                        if parsed_href.path and parsed_href.netloc:
                            word_count,myword_count = count_words(link.get('href'),link.text)
                            childrens = get_links(level-1,link.get('href'))
                            data_list.append({
                                'level': level,
                                'href': link.get('href'),
                                'title': link.text,
                                'mykeywords': myword_count,
                                'words': word_count,
                                'childrens': childrens
                            })
                    
                except:
                    continue
        else:
            return data_list
    else:
        return data_list
    return data_list

def remove_duplicate_links(data_list):
    # Duyệt qua tất cả các phần tử trong danh sách dữ liệu
    for item in data_list:
        href = item['href']
        childrens = item['childrens']
        
        # Kiểm tra xem phần tử hiện tại có phần tử con hay không
        if len(childrens) > 0:
            # Duyệt qua tất cả các phần tử con
            for child in childrens:
                child_href = child['href']
                
                # Nếu href của phần tử con trùng với href của phần tử cha
                if child_href == href:
                    # Loại bỏ phần tử con khỏi danh sách
                    childrens.remove(child)
            
            # Gọi đệ quy để loại bỏ các phần tử con của phần tử hiện tại
            remove_duplicate_links(childrens)
    
    return data_list

# Đường link mặc định
parsed_url = urlparse(url)

default_scheme = parsed_url.scheme
default_netloc = parsed_url.netloc

keywords = ["Hoa sinh nhật", "hoa hồng", "hoa khai trương", "hoa chúc mừng"]

data_url = get_links(1,url)

# Lưu danh sách dữ liệu thành file JSON
filename ='TheB.json'
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(remove_duplicate_links(data_url) , f, ensure_ascii=False)
    