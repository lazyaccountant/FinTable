import PyPDF2
import tempfile

def io_to_pdf(bytes_io):
    # Assuming 'pdf_bytes' is your BytesIO object containing PDF data
    pdf_bytes = bytes_io  # Your PDF data

    # Create a PDFFileReader object to read the PDF from the BytesIO
    pdf_reader = PyPDF2.PdfFileReader(pdf_bytes, strict=False)

    # Create a PDFFileWriter object to write the PDF to a temporary file
    pdf_writer = PyPDF2.PdfFileWriter()

    # Iterate through the pages of the PDF and add them to the PDFFileWriter
    for page_num in range(pdf_reader.getNumPages()):
        page = pdf_reader.getPage(page_num)
        pdf_writer.addPage(page)

    # Create a temporary file to save the PDF
    temp_pdf_file = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)

    # Write the PDF data from the PDFFileWriter to the temporary file
    with open(temp_pdf_file.name, "wb") as temp_pdf:
        temp_pdf_file = pdf_writer.write(temp_pdf)

    return temp_pdf_file

"""# Write the PDF data from the PDFFileWriter to the temporary file
with open(temp_pdf_file.name, "wb") as temp_pdf:
    pdf_writer.write(temp_pdf)

# Now you can process the temporary PDF file as needed
# ...

# Close and remove the temporary file when you're done
temp_pdf_file.close()
os.remove(temp_pdf_file.name)"""