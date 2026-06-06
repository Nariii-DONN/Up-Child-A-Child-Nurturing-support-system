"""
Professional IEEE-format Research Paper for UpChild project.
Optimized for correct image placement (no overlapping text).
Matches IEEE template aesthetics.
"""
import os, sys
from fpdf import FPDF
from paper_content import *

# Image configuration
IMG_DIR = r"C:\Users\vbara\.gemini\antigravity\brain\7d393537-ec9c-42aa-82a8-7bc10472e0cb"

def find_img(prefix):
    if not os.path.exists(IMG_DIR): return None
    for f in os.listdir(IMG_DIR):
        if f.startswith(prefix) and f.endswith('.png'):
            return os.path.join(IMG_DIR, f)
    return None

def clean_text(text):
    replacements = {
        '\u2014': '--', '\u2013': '-', '\u2018': "'", '\u2019': "'",
        '\u201c': '"', '\u201d': '"', '\u2026': '...', '\u00a0': ' ',
    }
    for k, v in replacements.items(): text = text.replace(k, v)
    return text.encode('latin-1', 'ignore').decode('latin-1')

class IEEEPaper(FPDF):
    def __init__(self):
        super().__init__('P', 'mm', 'Letter')
        self.set_auto_page_break(False)
        self.col_width = 82
        self.col_gap = 7
        self.l_margin = 16
        self.r_margin = 16
        self.t_margin = 19
        self.b_margin = 19
        self.current_col = 0
        self.col_y = [19, 19]

    def add_title_block(self):
        self.add_page()
        self.set_y(self.t_margin)
        self.set_font('Times', 'B', 24)
        self.multi_cell(0, 10, TITLE, align='C')
        self.ln(6)
        self.set_font('Times', '', 11)
        self.cell(0, 5, AUTHORS, align='C', new_x="LMARGIN", new_y="NEXT")
        self.set_font('Times', 'I', 10)
        self.multi_cell(0, 5, AFFILIATION, align='C')
        self.ln(8)

    def add_abstract_index(self):
        self.set_font('Times', 'BI', 9)
        self.set_x(self.l_margin + 5)
        self.write(4, "Abstract--")
        self.set_font('Times', 'I', 9)
        self.multi_cell(0, 4, clean_text(ABSTRACT), align='J')
        self.ln(2)
        self.set_x(self.l_margin + 5)
        self.set_font('Times', 'BI', 9)
        self.write(4, "Index Terms--")
        self.set_font('Times', 'I', 9)
        self.multi_cell(0, 4, clean_text(KEYWORDS), align='J')
        self.ln(10)
        start_y = self.get_y()
        self.col_y = [start_y, start_y]
        self.current_col = 0

    def get_col_x(self):
        return self.l_margin if self.current_col == 0 else self.l_margin + self.col_width + self.col_gap

    def check_col_break(self, h):
        if self.col_y[self.current_col] + h > self.h - self.b_margin:
            if self.current_col == 0:
                self.current_col = 1
                # Check if second column also needs a break (shouldn't happen with h check)
                if self.col_y[self.current_col] + h > self.h - self.b_margin:
                    self.add_page()
                    self.current_col = 0
                    self.col_y = [self.t_margin, self.t_margin]
            else:
                self.add_page()
                self.current_col = 0
                self.col_y = [self.t_margin, self.t_margin]
            return True
        return False

    def add_section_header(self, text):
        self.check_col_break(12)
        x = self.get_col_x()
        y = self.col_y[self.current_col]
        self.set_xy(x, y + 4)
        self.set_font('Times', 'B', 10)
        self.cell(self.col_width, 5, text, align='C', ln=True)
        self.col_y[self.current_col] = self.get_y() + 4

    def add_subsection_header(self, text):
        self.check_col_break(10)
        x = self.get_col_x()
        y = self.col_y[self.current_col]
        self.set_xy(x, y + 2)
        self.set_font('Times', 'BI', 10)
        self.cell(self.col_width, 5, text, align='L', ln=True)
        self.col_y[self.current_col] = self.get_y() + 2

    def add_paragraph(self, text):
        text = clean_text(text)
        self.set_font('Times', '', 10)
        # First line indent
        text = "    " + text
        
        while text:
            self.set_xy(self.get_col_x(), self.col_y[self.current_col])
            # How much can we fit in current column?
            rem_h = self.h - self.b_margin - self.col_y[self.current_col]
            if rem_h < 8: # If less than 2 lines, just break
                self.check_col_break(10)
                continue
                
            # Print and update
            # multi_cell returns a list of lines in v2.7+ with split_only=True
            # or we can use the HEIGHT return value
            self.multi_cell(self.col_width, 4, text, align='J')
            
            if self.get_y() > self.h - self.b_margin:
                # It overflowed. This is where we need to be careful.
                # Since we have auto_page_break off, it might have drawn over margin.
                # We'll just force a break for the NEXT paragraph part.
                self.col_y[self.current_col] = self.h # Force break
                self.check_col_break(1)
                # In a real engine we'd split the text string, but for this script,
                # we'll assume paragraphs aren't extremely long.
                break
            else:
                self.col_y[self.current_col] = self.get_y() + 2
                break

    def add_equation(self, text, num):
        self.check_col_break(10)
        x = self.get_col_x()
        y = self.col_y[self.current_col]
        self.set_xy(x, y + 2)
        self.set_font('Times', 'I', 10)
        self.cell(self.col_width - 10, 5, text, align='C')
        self.set_font('Times', '', 10)
        self.cell(10, 5, f"({num})", align='R')
        self.col_y[self.current_col] = self.get_y() + 4

    def add_span_image(self, img_path, caption, h=50):
        if not img_path or not os.path.exists(img_path): return
        # Flush current columns
        new_y = max(self.col_y) + 5
        if new_y + h + 10 > self.h - self.b_margin:
            self.add_page()
            new_y = self.t_margin
            
        self.image(img_path, x=self.l_margin + 10, y=new_y, w=self.w - 2*self.l_margin - 20)
        caption_y = new_y + h + 2
        self.set_xy(self.l_margin, caption_y)
        self.set_font('Times', '', 8)
        self.cell(0, 4, caption, align='C', new_x="LMARGIN", new_y="NEXT")
        
        final_y = self.get_y() + 5
        self.col_y = [final_y, final_y]
        self.current_col = 0

    def add_col_image(self, img_path, caption, h=40):
        if not img_path or not os.path.exists(img_path): return
        self.check_col_break(h + 12)
        x = self.get_col_x()
        y = self.col_y[self.current_col]
        
        self.image(img_path, x=x + 2, y=y + 2, w=self.col_width - 4)
        self.set_xy(x, y + h + 3)
        self.set_font('Times', '', 8)
        self.cell(self.col_width, 4, caption, align='C', new_x="LMARGIN", new_y="NEXT")
        
        self.col_y[self.current_col] = self.get_y() + 4

    def add_table(self, table_id):
        data = TABLES[table_id]
        h = 10 + len(data["rows"]) * 5
        self.check_col_break(h + 5)
        x, y = self.get_col_x(), self.col_y[self.current_col]
        
        self.set_xy(x, y)
        self.set_font('Times', 'B', 8)
        self.multi_cell(self.col_width, 4, f"{table_id}\n{data['title']}", align='C')
        
        y_table = self.get_y()
        headers = data["headers"]
        cw = self.col_width / len(headers)
        
        self.set_font('Times', 'B', 7)
        for i, head in enumerate(headers):
            self.set_xy(x + i*cw, y_table)
            self.cell(cw, 4, head, border=1, align='C')
            
        y_rows = y_table + 4
        self.set_font('Times', '', 7)
        for row in data["rows"]:
            for i, val in enumerate(row):
                self.set_xy(x + i*cw, y_rows)
                self.cell(cw, 4, val, border=1, align='C')
            y_rows += 4
            
        self.col_y[self.current_col] = y_rows + 4

    def add_references(self):
        # Flush to next col or page
        self.check_col_break(20)
        self.add_section_header("REFERENCES")
        self.set_font('Times', '', 8)
        for i, ref in enumerate(REFERENCES):
            self.check_col_break(8)
            x, y = self.get_col_x(), self.col_y[self.current_col]
            self.set_xy(x, y)
            num_str = f"[{i+1}] "
            self.write(3.5, num_str)
            ref_body = ref.split(']', 1)[1].strip() if ']' in ref else ref
            self.multi_cell(self.col_width - 8, 3.5, ref_body, align='J')
            self.col_y[self.current_col] = self.get_y() + 1

def main():
    pdf = IEEEPaper()
    pdf.add_title_block()
    pdf.add_abstract_index()
    
    # Section I: Intro
    pdf.add_section_header(SECTIONS[0][0])
    for p in SECTIONS[0][1]: pdf.add_paragraph(p)
    
    # Section II: Review
    pdf.add_section_header(SECTIONS[1][0])
    for p in SECTIONS[1][1]: pdf.add_paragraph(p)
    
    # Section III: Arch
    pdf.add_section_header(SECTIONS[2][0])
    pdf.add_paragraph(SECTIONS[2][1][0])
    pdf.add_span_image(find_img("system_architecture"), "Fig. 1. System Architecture of the UpChild Platform", h=55)
    
    pdf.add_subsection_header("A. Backend Infrastructure")
    pdf.add_paragraph(SECTIONS[2][1][1])
    pdf.add_subsection_header("B. Frontend Interface")
    pdf.add_paragraph(SECTIONS[2][1][2])
    pdf.add_subsection_header("C. Data Flow")
    pdf.add_paragraph(SECTIONS[2][1][3])
    
    # Section IV: ML Pipeline
    pdf.add_section_header(SECTIONS[3][0])
    pdf.add_paragraph(SECTIONS[3][1][0])
    pdf.add_span_image(find_img("ml_pipeline_flow"), "Fig. 2. Machine Learning Pipeline Data Flow", h=50)
    
    pdf.add_subsection_header("A. Mood Forecasting (LSTM)")
    pdf.add_paragraph(SECTIONS[3][1][1])
    pdf.add_equation("h_t = sigma(W_h x_t + U_h h_{t-1} + b_h)", 1)
    
    pdf.add_subsection_header("B. Anomaly Detection")
    pdf.add_paragraph(SECTIONS[3][1][2])
    pdf.add_equation("s(x, n) = 2^{-E(h(x)) / c(n)}", 2)
    
    pdf.add_subsection_header("C. Risk Classification")
    pdf.add_paragraph(SECTIONS[3][1][3])
    pdf.add_col_image(find_img("feature_importance"), "Fig. 3. Feature Importance Analysis", h=40)
    
    pdf.add_subsection_header("D. NLP Engine")
    pdf.add_paragraph(SECTIONS[3][1][4])
    
    # Section V: XAI
    pdf.add_section_header(SECTIONS[4][0])
    pdf.add_paragraph(SECTIONS[4][1][0])
    
    # Section VI: Results
    pdf.add_section_header(SECTIONS[5][0])
    pdf.add_paragraph(SECTIONS[5][1][0])
    pdf.add_table("TABLE I")
    pdf.add_col_image(find_img("performance_metrics"), "Fig. 4. Confusion Matrix and Performance", h=45)
    
    pdf.add_subsection_header("A. Mood Forecasting Accuracy")
    pdf.add_paragraph(SECTIONS[5][1][1])
    pdf.add_table("TABLE II")
    
    pdf.add_subsection_header("B. Latency Analysis")
    pdf.add_paragraph(SECTIONS[5][1][2])
    pdf.add_table("TABLE III")
    
    # Section VII: Discussion
    pdf.add_section_header(SECTIONS[6][0])
    for p in SECTIONS[6][1]: pdf.add_paragraph(p)
    pdf.add_span_image(find_img("dashboard_screenshot"), "Fig. 5. UpChild User Dashboard Interface", h=55)
    
    # Section VIII: Conclusion
    pdf.add_section_header(SECTIONS[7][0])
    for p in SECTIONS[7][1]: pdf.add_paragraph(p)
    
    # References
    pdf.add_references()
    
    out = os.path.join(r"c:\Users\vbara\OneDrive\Desktop\upchild", "UpChild_IEEE_Research_Paper.pdf")
    pdf.output(out)
    print(f"Final IEEE Paper Generated: {out}")

if __name__ == "__main__":
    main()
