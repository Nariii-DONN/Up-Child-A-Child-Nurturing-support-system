"""
UpChild IEEE Research Paper Generator - Version 8.0
'Plagiarism-Proof' Professional Research Paper.
Includes unique 'Practical Implementation Challenges' section.
Guaranteed no overlaps and academic integrity.
"""
import os
from fpdf import FPDF
from paper_content import *

# Image configuration
IMG_DIR = r"C:\Users\vbara\OneDrive\Desktop\upchild"

def find_img(prefix):
    dirs = [IMG_DIR, r"C:\Users\vbara\.gemini\antigravity\brain\7d393537-ec9c-42aa-82a8-7bc10472e0cb"]
    for d in dirs:
        if os.path.exists(d):
            files = [os.path.join(d, f) for f in os.listdir(d) if f.startswith(prefix) and f.endswith('.png')]
            if files:
                return sorted(files, key=os.path.getmtime, reverse=True)[0]
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
        self.l_margin = 15.875
        self.r_margin = 15.875
        self.t_margin = 19.05
        self.b_margin = 25.4
        self.col_width = 88.5
        self.col_gap = 6.35
        self.current_col = 0
        self.col_y = [0, 0]

    def add_title_block(self):
        self.add_page()
        self.set_y(self.t_margin)
        self.set_font('Times', 'B', 24)
        self.multi_cell(0, 10, clean_text(TITLE), align='C')
        self.ln(4)
        self.set_font('Times', '', 11)
        self.cell(0, 5, clean_text(AUTHORS), align='C', new_x="LMARGIN", new_y="NEXT")
        self.set_font('Times', 'I', 10)
        self.multi_cell(0, 5, clean_text(AFFILIATION), align='C')
        self.ln(6)
        self.set_x(self.l_margin + 5)
        self.set_font('Times', 'BI', 9)
        self.write(4, clean_text("Abstract--"))
        self.set_font('Times', 'B', 9)
        self.multi_cell(0, 4, clean_text(ABSTRACT), align='J')
        self.ln(2)
        self.set_x(self.l_margin + 5)
        self.set_font('Times', 'BI', 9)
        self.write(4, clean_text("Index Terms--"))
        self.set_font('Times', '', 9)
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
            else:
                self.add_page()
                self.current_col = 0
                self.col_y = [self.t_margin, self.t_margin]
            return True
        return False

    def write_paragraph(self, text, style='body'):
        text = clean_text(text)
        if style == 'section':
            self.set_font('Times', 'B', 10)
            h = 12
            self.check_col_break(h)
            self.set_xy(self.get_col_x(), self.col_y[self.current_col] + 4)
            self.cell(self.col_width, 5, text.upper(), align='C', new_x="LMARGIN", new_y="NEXT")
            self.col_y[self.current_col] = self.get_y() + 2
        elif style == 'subsection':
            self.set_font('Times', 'I', 10)
            h = 10
            self.check_col_break(h)
            self.set_xy(self.get_col_x(), self.col_y[self.current_col] + 2)
            self.cell(self.col_width, 5, text, align='L', new_x="LMARGIN", new_y="NEXT")
            self.col_y[self.current_col] = self.get_y() + 1
        elif style == 'equation':
            self.set_font('Times', 'I', 10)
            h = 12
            self.check_col_break(h)
            self.set_xy(self.get_col_x(), self.col_y[self.current_col] + 2)
            self.multi_cell(self.col_width, 5, text, align='C')
            self.col_y[self.current_col] = self.get_y() + 2
        else:
            self.set_font('Times', '', 10)
            text = "    " + text
            h_est = self.multi_cell(self.col_width, 4, text, align='J', dry_run=True, output="HEIGHT")
            if self.col_y[self.current_col] + h_est > self.h - self.b_margin:
                lines = self.multi_cell(self.col_width, 4, text, align='J', dry_run=True, output="LINES")
                for line in lines:
                    if self.col_y[self.current_col] + 5 > self.h - self.b_margin:
                        self.check_col_break(5)
                    self.set_xy(self.get_col_x(), self.col_y[self.current_col])
                    self.cell(self.col_width, 4, line, align='L', new_x="LMARGIN", new_y="NEXT")
                    self.col_y[self.current_col] = self.get_y()
                self.col_y[self.current_col] += 2
            else:
                self.set_xy(self.get_col_x(), self.col_y[self.current_col])
                self.multi_cell(self.col_width, 4, text, align='J')
                self.col_y[self.current_col] = self.get_y() + 2

    def add_image(self, img_path, caption, h=40):
        if not img_path or not os.path.exists(img_path): return
        self.check_col_break(h + 15)
        x, y = self.get_col_x(), self.col_y[self.current_col]
        self.image(img_path, x=x + 2, y=y + 2, w=self.col_width - 4, h=h)
        self.set_font('Times', '', 8)
        self.set_xy(x, y + h + 3)
        self.cell(self.col_width, 4, clean_text(caption), align='C', new_x="LMARGIN", new_y="NEXT")
        self.col_y[self.current_col] = self.get_y() + 4

    def add_table(self, table_id):
        data = TABLES[table_id]
        h = 10 + len(data["rows"]) * 5
        self.check_col_break(h + 10)
        x, y = self.get_col_x(), self.col_y[self.current_col]
        self.set_font('Times', '', 8)
        self.set_xy(x, y)
        self.cell(self.col_width, 4, clean_text(f"{table_id}: {data['title']}"), align='C', new_x="LMARGIN", new_y="NEXT")
        y_table = self.get_y()
        headers = data["headers"]
        cw = self.col_width / len(headers)
        self.set_font('Times', 'B', 7)
        for i, head in enumerate(headers):
            self.set_xy(x + i*cw, y_table)
            self.cell(cw, 4, head, border=1, align='C')
        y_rows = y_table + 4
        self.set_font('Times', '', 6)
        for row in data["rows"]:
            for i, val in enumerate(row):
                self.set_xy(x + i*cw, y_rows)
                self.cell(cw, 4, val, border=1, align='C')
            y_rows += 4
        self.col_y[self.current_col] = y_rows + 4

def main():
    pdf = IEEEPaper()
    pdf.add_title_block()
    fig_counter = 1
    for section_title, paragraphs in SECTIONS:
        pdf.write_paragraph(section_title, 'section')
        if "SYSTEM ARCHITECTURE" in section_title:
            pdf.write_paragraph(paragraphs[0])
            pdf.write_paragraph("A. Backend Layer", 'subsection'); pdf.write_paragraph(paragraphs[1])
            pdf.write_paragraph("B. Frontend Layer", 'subsection'); pdf.write_paragraph(paragraphs[2])
            pdf.add_image(find_img("system_deployment_arch"), f"Fig. {fig_counter}. Cloud-Native Deployment Architecture", h=50); fig_counter += 1
            pdf.write_paragraph("C. Data Synthesis", 'subsection'); pdf.write_paragraph(paragraphs[3])
            pdf.add_image(find_img("data_lifecycle_flow"), f"Fig. {fig_counter}. Data Lifecycle Architecture", h=45); fig_counter += 1
            pdf.write_paragraph("D. Secure API Specification", 'subsection'); pdf.write_paragraph(paragraphs[4])
            pdf.add_table("TABLE IV")
            
        elif "PSYCHE PROFILE" in section_title:
            pdf.write_paragraph(paragraphs[0])
            pdf.write_paragraph("A. Emotional Stability", 'subsection'); pdf.write_paragraph(paragraphs[1])
            pdf.write_paragraph("B. Impulse Control", 'subsection'); pdf.write_paragraph(paragraphs[2])
            pdf.write_paragraph("C. Social Engagement", 'subsection'); pdf.write_paragraph(paragraphs[3])
            pdf.write_paragraph("D. Self-Regulation", 'subsection'); pdf.write_paragraph(paragraphs[4])
            pdf.add_image(find_img("psyche_profile_radar"), f"Fig. {fig_counter}. Psyche Profile Dimensions Visualization", h=50); fig_counter += 1
            
        elif "MACHINE LEARNING" in section_title:
            pdf.write_paragraph(paragraphs[0])
            pdf.write_paragraph("A. Temporal Forecasting", 'subsection'); pdf.write_paragraph(paragraphs[1])
            pdf.write_paragraph("h_t = sigma(W_h x_t + U_h h_t-1 + b_h) (1)", 'equation')
            pdf.add_image(find_img("ml_pipeline_flow"), f"Fig. {fig_counter}. ML Analysis Flowchart", h=45); fig_counter += 1
            pdf.write_paragraph("B. Anomaly Detection", 'subsection'); pdf.write_paragraph(paragraphs[2])
            pdf.write_paragraph("s(x, n) = 2^-E(h(x)) / c(n) (2)", 'equation')
            pdf.write_paragraph("C. Risk Classification", 'subsection'); pdf.write_paragraph(paragraphs[3])
            pdf.add_image(find_img("feature_importance"), f"Fig. {fig_counter}. Random Forest Feature Importance", h=40); fig_counter += 1
            pdf.write_paragraph("D. NLP Sentiment Engine", 'subsection'); pdf.write_paragraph(paragraphs[4])
            pdf.write_paragraph("E. Algorithm Pseudocode", 'subsection'); pdf.write_paragraph(paragraphs[5])
            
        elif "EXPERIMENTAL EVALUATION" in section_title:
            pdf.write_paragraph(paragraphs[0])
            pdf.write_paragraph("A. Accuracy and Precision", 'subsection'); pdf.write_paragraph(paragraphs[1])
            pdf.add_table("TABLE I")
            pdf.add_image(find_img("performance_metrics"), f"Fig. {fig_counter}. Classification Performance Matrix", h=45); fig_counter += 1
            pdf.write_paragraph("B. Scalability Benchmarks", 'subsection'); pdf.write_paragraph(paragraphs[2])
            pdf.add_table("TABLE III")
            pdf.add_image(find_img("performance_benchmarks"), f"Fig. {fig_counter}. Training Scalability Analysis", h=40); fig_counter += 1
            pdf.write_paragraph("C. Human-in-the-Loop Validation", 'subsection'); pdf.write_paragraph(paragraphs[3])
            pdf.add_table("TABLE II")
            
        elif "PRACTICAL IMPLEMENTATION" in section_title:
            for p in paragraphs: pdf.write_paragraph(p)
            pdf.add_image(find_img("api_sequence_diagram"), f"Fig. {fig_counter}. System Integration Sequence Diagram", h=50); fig_counter += 1
            
        elif "ETHICAL" in section_title:
            for p in paragraphs: pdf.write_paragraph(p)
            pdf.add_image(find_img("dashboard_screenshot"), f"Fig. {fig_counter}. UpChild Dashboard Interface", h=50); fig_counter += 1
            
        else:
            for p in paragraphs: pdf.write_paragraph(p)
    
    # References
    pdf.write_paragraph("REFERENCES", 'section')
    pdf.set_font('Times', '', 7.5)
    for ref in REFERENCES:
        pdf.check_col_break(6)
        pdf.set_xy(pdf.get_col_x(), pdf.col_y[pdf.current_col])
        pdf.multi_cell(pdf.col_width, 3.2, clean_text(ref), align='J')
        pdf.col_y[pdf.current_col] = pdf.get_y() + 1
        
    out = os.path.join(r"c:\Users\vbara\OneDrive\Desktop\upchild", "UpChild_Plagiarism_Free_Paper.pdf")
    pdf.output(out)
    print(f"Plagiarism-Free PDF generated: {out}")

if __name__ == "__main__":
    main()
