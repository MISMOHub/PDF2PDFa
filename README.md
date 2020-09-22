# PDF2PDFa
Convert PDF file with Form Fields to archivable PDF file in PDF/A format

 ##Name: PDF2PDFa
 ###Version: v0.1
 ###Description: 
 - takes PDF file with Form Fields and creates a new PDF file in PDF/A format;
 - the new PDF file is the exact copy of source PDF, except all layers are flattened for archiving purposes;
 - all Form Fileds are transferred to PDF/A Metadata;
 - if Metadata Name already exists, the Metadata will be overwritten by Field Value;
 - the new file does not preserve FDF from source PDF.

 ###Requirements:
 - Host OS: Ubuntu v18.04+
 - Python3
 - Ghostscript
   (command to install: sudo apt-get install -y ghostscript-x)

 ###Execution:
 python3 PDF2PDFa.py <source_PDF_file_name>
 ###Result: 
 a new file with file name 'pdfa_' + <source_PDF_file_name>

 ###Example:
 python3 PDF2PDFa.py Conv_1.pdf
 ###Result:
 pdfa_Conv_1.pdf
