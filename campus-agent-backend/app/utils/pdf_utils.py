from fpdf import FPDF

def create_pdf(content: str, filename: str) -> str:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Split content into lines and add to PDF
    for line in content.splitlines():
        pdf.cell(200, 10, txt=line, ln=True)
    
    # Save the PDF to a file
    pdf.output(filename)
    return filename