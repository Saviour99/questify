from PyPDF2 import PdfReader

def extract(file:str):
    pdf = open(file, "rb")
        reader = PdfReader(pdf)
        
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            
        return page.extract_text()

            
if __name__ == "__main__":
    content = extract("supply_chain.pdf")
    print(content)