from pdftxt import convert_pdf_to_txt
from indexer import return_index

def parse(resume_name):
  input_path = 'parse/resumes/'+resume_name
  output_path = 'parse/outputtext.txt'
  convert_pdf_to_txt(input_path, output_path)
  indexed = return_index(output_path)
  # print(indexed)
  return indexed
