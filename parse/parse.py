from pdftxt import convert_pdf_to_txt
from indexer import return_index

def main():
  data_path = 'parse/resumes/'
  input_path = data_path + 'fResume.pdf'
  output_path = 'parse/outputtext.txt'
  convert_pdf_to_txt(input_path, output_path)
  indexed = return_index(output_path)
  # print(indexed)
  return indexed

if __name__ == "__main__":
  main()