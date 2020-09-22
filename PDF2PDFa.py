#!/usr/bin/env python

# Name: PDF2PDFa
# v0.1
# Description: 
# - takes PDF file with Form Fields and creates a new PDF file in PDF/A format;
# - the new PDF file is the exact copy of source PDF, except all layers are flattened for archiving purposes;
# - all Form Fileds are transferred to PDF/A Metadata;
# - if Metadata Name already exists, the Metadata will be overwritten by Field Value;
# - the new file does not preserve FDF from source PDF.
#
# Requirements:
# - Host OS: Ubuntu v18.04+
# - Python3
# - Ghostscript
#   (command to install: sudo apt-get install -y ghostscript-x)
#
# Execution:
# python3 PDF2PDFa.py <source_PDF_file_name>
# Result: 
# a new file with file name 'pdfa_' + <source_PDF_file_name>
#
# Example:
# python3 PDF2PDFa.py Conv_1.pdf
# Result:
# pdfa_Conv_1.pdf
#

import os
import argparse
import subprocess
from pdfrw import PdfReader, PdfWriter, PdfName, PdfDict, errors


def args_parse():
    args_parser = argparse.ArgumentParser(description='PDF2PDFa Converter')
    args_parser.add_argument(
        'file_path', type=str, help='Path to pdf file'
    )
    return args_parser


# Get Form Fields as a PdfDict from FDF
def get_form_fields_from_fdf(pdf_file_path):
    try:
        pdf_reader = PdfReader(pdf_file_path)
    except errors.PdfParseError:
        print(f'File \'{pdf_file_path}\' not found please specify full path')
        return None
    try:
        # Check if PDF has Form Fields and if we can read them
        pdf_form_fields = pdf_reader.Root.AcroForm.Fields
    except AttributeError:
        print(f'File \'{pdf_file_path}\' no Form Fields')
        return None

    # Create an empty PdfDict to collect Form Fields and Values
    pdf_metadata = PdfDict()

    # Define list of Form Fields to be ignored from transfer to PdfDict
    # For example: field Sig
    ignore_fields = ('/Sig',)

    # Load Form Fields into PdfDict
    for field in pdf_form_fields:
        if field.FT not in ignore_fields:
            field_name = field.T
            if field_name is not None:
                key_name = PdfName(field_name.decode())
                pdf_metadata[key_name] = field.V
    return pdf_metadata


def convert_pdf2pdfa(pdf_file_path):
    # For conversion we use Linux standard Ghostscript
    ghost_script_exec = [
        'gs',
        '-dPDFA=1',
        '-dBATCH',
        '-dNOPAUSE',
        '-sProcessColorModel=DeviceRGB',
        '-sDEVICE=pdfwrite',
        '-sPDFACompatibilityPolicy=2'
    ]
    cwd = os.getcwd()
    path, file_name = os.path.split(pdf_file_path)
    pdfa_file_path = os.path.join(path, f'pdfa_{file_name}')
    os.chdir(os.path.dirname(pdf_file_path))
    try:
        subprocess.check_output(
            ghost_script_exec + [
                '-sOutputFile=' + pdfa_file_path,
                pdf_file_path
            ]
        )
    except subprocess.CalledProcessError as error:
        raise RuntimeError(
            f'Command \'{error.cmd}\' return with error '
            f'(code {error.returncode}): {error.output}'
        )
    else:
        os.chdir(cwd)
    return pdfa_file_path


def update_pdfa_metadata(pdfa_file_path, pdf_metadata):
    try:
        pdfa_reader = PdfReader(pdfa_file_path)
    except errors.PdfParseError:
        print(
            f'File \'{pdfa_file_path}\' does not exist metadata will not be '
            f'updated'
        )
    else:
        # If Field Name already exist in Metadata,
        # the original Field Value will be overwritten with Form Field
        for key, value in pdf_metadata.items():
            pdfa_reader.Info[key] = value

        PdfWriter().write(pdfa_file_path, pdfa_reader)


def main(pdf_file_path):
    absolute_pdf_file_path = os.path.abspath(pdf_file_path)
    pdf_metadata = get_form_fields_from_fdf(absolute_pdf_file_path)
    if pdf_metadata:
        pdfa_file_path = convert_pdf2pdfa(absolute_pdf_file_path)
        update_pdfa_metadata(pdfa_file_path, pdf_metadata)
        return pdfa_file_path


if __name__ == '__main__':
    parser = args_parse()
    file_path = parser.parse_args().file_path
    main(file_path)
