from piston_mini_client import SocketError
import urllib2
from BeautifulSoup import BeautifulSoup
import errno


def main():
    with open("./PaperTopics", 'r') as f:
        for line in f:
            print(line)
            if line.__contains__(" "):
                topic = line.replace(" ", "%20").strip()
            else:
                topic = line.strip()

            url = "http://export.arxiv.org/api/query?search_query=all:"+str(topic)+"&start=51&max_results=100"

            page=urllib2.urlopen(url)
            soup = BeautifulSoup(page.read())
            entries=soup.findAll('entry')
            for entry in entries:
                pdf_name = entry.title.text.replace(" ", "_").replace("\n","").replace('/',"_")
                pdf = entry.find('link', {'title':'pdf'})['href']
                print(pdf_name)
                download_file(pdf, pdf_name)

def download_file(download_url, pdf_name):
    try:
        response = urllib2.urlopen(download_url)
    except SocketError as e:
        if e.errno != errno.ECONNRESET:
            raise # Not error we are looking for
        pass # Handle error here.
    file = open("./CSPapers/"+pdf_name, 'w')
    file.write(response.read())
    file.close()
    print("Completed")

if __name__ == "__main__":
    main()