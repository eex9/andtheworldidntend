import marko
import pdfkit
import os
import json
from pypdf import PdfWriter

dirname = os.path.dirname(__file__)

def markdown_to_html(path:str) -> str:
    author = None
    title = None
    reading = True
    out = ""
    
    with open(path, "r") as file:
        lines = file.readlines()
        for line in lines:
            if not reading:
                if (line == "---\n"):
                    reading = True
                    out = f"# {title if title != None else ''}\n{f'By {author}' if author != None else ''}\n"
                    continue
                elif (line.startswith("author:")):
                    line = line.removeprefix("author: ")
                    author = line
                elif (line.startswith("title:")):
                    line = line.removeprefix("title: ")
                    title = line
            elif reading:
                if ((lines.index(line) == 0) & (line == "---\n")):
                    reading = False
                    continue
                out += f"{line}\n"
    return f'{marko.convert(out)}'

def html_to_pdf(html:str, path:str) -> None:
    pdfkit.from_string(html, path, css=f"{dirname}/zine_pages/html/style.css")

def merge_html_onepage(html1:str, html2:str) -> str:
    return f'<div class="row">\n<div class="column">{html1}</div>\n<div class="column">{html2}</div>\n</div>'

def merge_pdfs_from_html_onepage(html1:str, html2:str, path) -> None:
    html = merge_html_onepage(html1, html2)
    pdfkit.from_string(html, path, options={"orientation": "landscape"}, css=f"{dirname}/zine_pages/html/style.css")

def main():
    with open(f"{dirname}/page_order.json", "r") as config:
        config_file = json.load(config)
        pages:list = config_file.get("order", None)
        if pages == None:
            print("Could not load config. Exiting...")
            exit()
    
    html = list(markdown_to_html(f"{dirname}/zine_pages/md/{page}.md") for page in pages)
    for i in range(len(pages)):
        try:
            with open(f"{dirname}/zine_pages/html/{pages[i].split('/')[-1]}.html", "x") as file:
                file.write(html[i])
        except FileExistsError:
            print(f"Could not overwrite file: {dirname}/zine_pages/html/{pages[i].split('/')[-1]}.html")
            continue
        try:
            html_to_pdf(html[i], f"{dirname}/zine_pages/pdf/single_pages/{pages[i].split('/')[-1]}.pdf")
        except OSError:
            print(f"Could not convert file {dirname}/zine_pages/html/{pages[i].split('/')[-1]}.html to pdf format:\nFile might have links")
    
    print("Please check over all files and ensure they fit on one page. PDFs will be updated from HTML upon continue.")
    input("Press enter when ready. Press CTRL+C to exit.")
    for i in range(len(pages)):
        pdfkit.from_file(f"{dirname}/zine_pages/html/{pages[i].split('/')[-1]}.html", f"{dirname}/zine_pages/pdf/single_pages/{pages[i].split('/')[-1]}.pdf")
    
    if (len(html)%2!=0):
        html.insert(-1, "")
    for i in range(int(len(html)/2)):
        if (i % 2 == 1):
            merge_pdfs_from_html_onepage(html[i], html[len(html)-i-1], f"{dirname}/zine_pages/pdf/full_pages/page_{i+1}.pdf")
        else:
            merge_pdfs_from_html_onepage(html[len(html)-i-1], html[i], f"{dirname}/zine_pages/pdf/full_pages/page_{i+1}.pdf")
    merger = PdfWriter()
    for pdf in os.listdir(f"{dirname}/zine_pages/pdf/full_pages"):
        merger.append(f"{dirname}/zine_pages/pdf/full_pages/{pdf}")
    merger.write(f"{dirname}/zine_pages/pdf/full.pdf")
    merger.close()

def test():
    with open(f"{dirname}/zine_pages/md/organizing_and_direct_action.md") as file:
        print(file.readlines())

if __name__ == "__main__":
    main()