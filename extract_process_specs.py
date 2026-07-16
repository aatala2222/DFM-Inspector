"""
Extract text from Process Specs PDF files to analyze design criteria
"""
import os
import PyPDF2
from pathlib import Path

def extract_pdf_text(pdf_path):
    """Extract text from a PDF file"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
            return text
    except Exception as e:
        return f"Error reading {pdf_path}: {str(e)}"

def main():
    process_specs_dir = "Process Specs"
    
    # Key design guideline files to extract
    key_files = [
        "930-00164_R01 DESIGN GUIDELINE, THERMOPLASTIC INJECTION MOLDING.pdf",
        "930-00166_R01 DESIGN GUIDELINE, HIGH PRESSURE DIE CAST AND GRAVITY CAST PERMANENT MOLD.pdf",
        "930-00172_R01 DESIGN GUIDELINE, SHEET METAL.pdf",
        "960-00169_R01 DESIGN GUIDELINE, WELDMENTS.pdf",
        "CNC_Machining_DFM_Guidelines.docx"
    ]
    
    output_dir = "extracted_specs"
    os.makedirs(output_dir, exist_ok=True)
    
    print("Extracting Process Specification Documents...")
    print("=" * 70)
    
    for filename in os.listdir(process_specs_dir):
        if filename.endswith('.pdf') and 'DESIGN GUIDELINE' in filename.upper():
            pdf_path = os.path.join(process_specs_dir, filename)
            print(f"\nProcessing: {filename}")
            
            text = extract_pdf_text(pdf_path)
            
            # Save extracted text
            output_filename = filename.replace('.pdf', '.txt')
            output_path = os.path.join(output_dir, output_filename)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"SOURCE: {filename}\n")
                f.write("=" * 70 + "\n\n")
                f.write(text)
            
            print(f"  ✓ Extracted {len(text)} characters")
            print(f"  ✓ Saved to: {output_path}")
    
    print("\n" + "=" * 70)
    print(f"✓ Extraction complete. Files saved to '{output_dir}/' folder")

if __name__ == "__main__":
    main()
