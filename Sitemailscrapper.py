import re
import requests
from urllib.parse import urljoin

# web sitesi adresi
url = "https://www.ornek.org/a-dan-z-ye-firmalar"

# web sitesinden tüm e-posta adreslerini topla
def get_emails(url):
    # web sitesine bağlan
    response = requests.get(url)

    # HTML içeriğini al
    content = response.text

    # e-posta adreslerini ara ve listeye ekle
    emails = re.findall(r'[\w\.-]+@[\w\.-]+', content)
    return emails

# tüm e-posta adreslerini al
emails = []

# başlangıç sayfasını işleme al
page_emails = get_emails(url)
emails.extend(page_emails)

# tüm linkleri al ve linklerdeki e-postaları al
response = requests.get(url)
content = response.text
links = re.findall(r'href="(.*?)"', content)

for link in links:
    # bağlantı adresini tamamlama
    link = urljoin(url, link)

    # "firma.php" içeren sayfaları işleme al
    if "firma.php" in link:
        # e-posta adreslerini al
        page_emails = get_emails(link)
        
        # aynı mail adreslerini listeye ekleme
        for email in page_emails:
            if email not in emails:
                emails.append(email)

# e-posta adreslerini yazdır ve dosyaya kaydet
with open('emails.txt', 'w') as f:
    for email in emails:
        print(email)
        f.write(email + '\n')
