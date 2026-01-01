"""
SEO Sentinel PDF Report Generator
Creates Professional, branded PDF reports from crawl results
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.platypus import Image as RLImage
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import json

class SEOReportGenerator:
    """Generate professional PDF reports from SEO audit data"""
    
    def __init__(self, data_file, output_pdf='seo_report.pdf'):
        self.data_file = data_file
        self.output_pdf = output_pdf
        self.data = self._load_data()
        
        #color scheme (professional blue theme)
        self.primary_color = colors.HexColor('#1e40af')
        self.secondary_color = colors.HexColor('#3b82f6')
        self.danger_color = colors.HexColor('#dc2626')
        self.warning_color = colors.HexColor('#f59e0b')
        self.success_color = colors.HexColor('#16a34a')
        
    def _load_data(self):
        """Load JSON data from crawler"""
        with open(self.data_file, 'r') as f:
            return json.load(f)
        
    def _create_header(self, canvas, doc):
        """Add header to each page"""
        canvas.saveState()
        canvas.setFont('Helvetica-Bold', 16)
        canvas.setFillColor(self.primary_color)
        canvas.drawString(inch, 10.5 * inch, "SEO Sentinel Report")
        canvas.setFont('Helvetica', 10)
        canvas.setFillColor(colors.grey)
        canvas.drawRightString(7.5 * inch, 10.5 * inch, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        canvas.line(inch, 10.3 * inch, 7.5 * inch, 10.3 * inch)
        canvas.restoreState()
        
    def _create_footer(self, canvas, doc):
        """Add footer to each page"""
        canvas.saveState()
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(colors.grey)
        canvas.drawString(inch, 0.5 * inch, "© 2026 SEO Sentinel - Automated Website Health Monitoring")
        canvas.drawRightString(7.5 * inch, 0.5 * inch, f"Page {doc.page}")
        canvas.restoreState()
        
    def _add_page_elements(self, canvas, doc):
        """Combine header and footer"""
        self._create_header(canvas, doc)
        self._create_footer(canvas, doc)
        
    def generate(self):
        """Generate the complete PDF report"""
        doc = SimpleDocTemplate(
            self.output_pdf,
            pagesize=letter,
            rightMargin=inch,
            leftMargin=inch,
            topMargin=inch * 1.2,
            bottomMargin=inch * 0.8
        )
        
        styles = getSampleStyleSheet()
        story = []
        
        #Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=Styles['Heading1'],
            fontSize=24,
            textColor=self.primary_color,
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=self.primary_color,
            spaceAfter=12,
            spaceBefore=20
        )
        
        #1. Title Page
        story.append(Spacer(1, 2 * inch))
        story.append(Paragraph(f"SEO Health Report", title_style))
        story.append(Spacer(1, 0.3 * inch))
        story.append(Paragraph(f"<b>{self.data['domain']}</b>", styles['Title']))
        story.append(Spacer(1, 0.5 * inch))
        
        #Executive Summary Box
        summary_data = [
            ['Metric', 'Count', 'Status'],
            ['Pages Crawled', str(self.data['stats']['pages_crawled']), '✓'],
            ['Broken Links', str(self.data['stats']['broken_links']), 
             '⚠️' if self.data['stats']['broken_links'] > 0 else '✓'],
            ['Missing Alt Text', str(self.data['stats']['missing_alt_text']),
             '⚠️' if self.data['stats']['missing_alt_text'] > 0 else '✓']
        ]
        
        summary_table = Table(summary_data, colWidths=[2.5*inch, 1.5*inch, 1*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.primary_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTSIZE', (0, 1), (-1, -1), 11),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        story.append(summary_table)
        story.append(PageBreak())
        
        #2. Broken Links Section
        if self.date['issues']['broken_links']:
            story.append(Paragraph("🔴 Broken Links Found", heading_style))
            story.append(Paragraph(
                f"<b>{len(self.data['issues']['broken_links'])} broken links</b> are hurting your SEO. "
                "Search engines penalize sites with dead pages.",
                styles['Normal']
            ))
            story.append(Spacer(1, 0.2 * inch))
            
            #Create Table
            broken_data = [['URL', 'Status', 'Found On']]
            for issue in self.data['issues']['broken_links'][:20]:
                url = issue['url'][:50] + '...' if len(issue['url']) > 50 else issue['url']
                ref = issue['referenced_from'][:40] + '...' if len(issue['referenced_from']) > 40 else issue['referenced_from']
                broken_data.append([url, str(issue['status']), ref])
                
            broken_table = Table(broken_data, colWidths=[3*inch, 0.8*inch, 2.2*inch])
            broken_table.setStyle(Table([
                ('BACKGROUND', (0, 0), (-1, 0), self.danger_color),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
            ]))
            
            story.append(broken_table)
            story.append(Spacer(1, 0.3 * inch))
            
            if len(self.data['issues']['broken_links']) > 20:
                story.append(Paragraph(
                    f"<i>+ {len(self.data['issues']['broken_links']) - 20} more broken links not shown...</i>",
                    styles['Italic']
                ))
                
        story.append(PageBreak())
        
        #3. Missing ALT Text Section
        if self.data['issues']['missing_alt_text']:
            story.append(Paragraph("🖼️ Missing Image Alt Text", heading_style))
            story.append(Paragraph(
                f"<b>{len(self.data['issues']['missing_alt_text'])} images</b> lack alt text. "
                "This hurts accessibility and prevents Google from indexing your images.",
                styles['Normal']
            ))
            story.append(Spacer(1, 0.2 * inch))
            
            #Create Table
            alt_data = [['Page', 'Image File', 'Page Title']]
            for issue in self.data['issues']['missing_alt_text'][:25]:
                page = issue['page_url'][:45] + '...' if len(issue['page_url']) > 45 else issue['page_url']
                img = issue['img_filename'][:30] + '...' if len(issue['img_filename']) > 30 else issue['img_filename']
                title = issue['page_title'][:40] + '...' if len(issue['page_title']) > 40 else issue['page_title']
                alt_data.append([page, img, title])
            
            alt_table = Table(alt_data, colWidths=[2.5*inch, 2*inch, 1.5*inch])
            alt_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), self.warning_color),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
            ]))
            
            story.append(alt_table)
            story.append(Spacer(1, 0.3 * inch))
            
            if len(self.data['issues']['missing_alt_text']) > 25:
                story.append(Paragraph(
                    f"<i>+ {len(self.data['issues']['missing_alt_text']) - 25} more images missing alt text...</i>",
                    styles['Italic']
                ))
        
        story.append(PageBreak())
        
        #4. Recommendations
        story.append(Paragraph("💡 Recommended Actions", heading_style))
        
        recommendations = []
        if self.data['stats']['broken_links'] > 0:
            recommendations.append(
                f"1. <b>Fix {self.data['stats']['broken_links']} broken links</b> immediately. "
                "Use 301 redirects for moved content or remove dead links."
            )
        
        if self.data['stats']['missing_alt_text'] > 0:
            recommendations.append(
                f"2. <b>Add alt text to {self.data['stats']['missing_alt_text']} images</b>. "
                "Use descriptive text that helps visually impaired users and search engines."
            )
        
        recommendations.append(
            "3. <b>Schedule weekly monitoring</b>. SEO issues compound over time. "
            "Upgrade to our automated monitoring plan for $29/month."
        )
        
        for rec in recommendations:
            story.append(Paragraph(rec, styles['Normal']))
            story.append(Spacer(1, 0.15 * inch))
            
        story.append(Spacer(1, 0.5 * inch))
        
        #CTA Box
        cta_text = """
        <para align=center>
        <b><font size=14 color='#1e40af'>Ready to Fix These Issues?</font></b><br/>
        <font size=11>Get automated weekly monitoring + AI-powered fix suggestions</font><br/>
        <font size=10>Visit: <b>www.seositinel.com/signup</b></font>
        </para>
        """
        
        story.append(Paragraph(cta_text, styles['Normal']))
        
        #Build PDF
        doc.build(story, onFirstPage=self._add_page_elements, onLaterPages=self._add_page_elements)
        print(f"✅ PDF Report generated: {self.output_pdf}")

#CLI Usage
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python pdf_generator.py <json_file> [output.pdf]")
        sys.exit(1)
        
    json_file = sys.argv[1]
    output_files = sys.argv[2] if len(sysd.argv) > 2 else 'seo-report.pdf'
    
    generator = SEOReportGenerator(json_file, output_file)
    generator.generate()
