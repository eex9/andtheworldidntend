import marko
import pdfkit
import os
import json
from pypdf import PdfMerger

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
                    out = f"# {title if title != None else ''}\n{'By', author if author != None else ''}\n"
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
    return f'<style>\n.column{{\nfloat: left;\nwidth: 50%;\n}}\n</style>\n{marko.convert(out)}'

def html_to_pdf(html:str, path:str) -> None:
    pdfkit.from_string(html, path, options={"enable-local-file-access": ""})

# this method sucks but i dont feel like writing it any other way rn. someone else do it
def merge_html_onepage(html1:str, html2:str) -> str:
    out = '<style>.column {float: left;width: 50%;}</style>\n"<div class="row">\n<div class="column">'
    out += html1.strip(".column{ float: left; width: 50%; }")
    out += '</div>\n<div class="column">'
    out += html2.strip(".column{ float: left; width: 50%; }")
    out += '</div>\n</div>'
    return out

def merge_pdfs_from_html_onepage(html1:str, html2:str, path) -> None:
    html = merge_html_onepage(html1, html2)
    pdfkit.from_string(html, path, options={"enable-local-file-access": ""})

def main():
    with open("./page_order.json", "r") as config:
        config_file = json.load(config)
        pages:list = config_file.get("order", None)
        if pages == None:
            print("Could not load config. Exiting...")
            exit()
    
    html = list(markdown_to_html(f"./zine_pages/md/{page}") for page in pages)
    for i in range(len(pages)):
        try:
            with open(f"./zine_pages/html/{pages[i].split('/')[-1][:pages[i].rindex('.')]}.html", "x") as file:
                file.write(html[i])
        except FileExistsError:
            print(f"Could not overwrite file: ./zine_pages/html/{pages[i].split('/')[-1][:pages[i].rindex('.')]}.html")
            continue
        try:
            html_to_pdf(html[i], f"./zine_pages/pdf/single_pages/{pages[i].split('/')[-1][:pages[i].rindex('.')]}.pdf")
        except OSError:
            print(f"Could not convert file ./zine_pages/html/{pages[i].split('/')[-1][:pages[i].rindex('.')]}.html to pdf format:\nFile might have links")
    
    print("Please check over all files and ensure they fit on one page. PDFs will be updated from HTML upon continue.")
    input("Press enter when ready. Press CTRL+C to exit.")
    for i in range(len(pages)):
        pdfkit.from_file(f"./zine_pages/html/{pages[i].split('/')[-1][:pages[i].rindex('.')]}.html", f"./zine_pages/pdf/single_pages/{pages[i].split('/')[-1][:pages[i].rindex('.')]}.pdf")
    
    if (len(html)%2!=0):
        html.insert(-1, "")
    for i in range(int(len(html)/2)):
        merge_pdfs_from_html_onepage(html[i], html[len(html)-i-1], f"./zine_pages/pdf/full_pages/page_{i+1}.pdf")
    merger = PdfMerger()
    for pdf in os.listdir("./zine_pages/pdf/full_pages"):
        merger.append(f"./zine_pages/pdf/full_pages/{pdf}")
    merger.write("./zine_pages/pdf/full.pdf")
    merger.close()

def test():
    with open(f"./zine_pages/html/test.html", "+w") as file:
        file.write(markdown_to_html("./zine_pages/md/test.md"))

if __name__ == "__main__":
    main()