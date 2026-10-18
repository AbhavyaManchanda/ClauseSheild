"""
create_sample_contract.py - Generates a realistic sample predatory freelance agreement (PDF)
to test ClauseShield's clause auditing capabilities.
"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_sample_pdf(output_path="sample_predatory_contract.pdf"):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=54,
        leftMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        alignment=1,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=14
    )
    heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=10,
        spaceAfter=4
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#334155"),
        spaceAfter=8
    )

    story = []

    story.append(Paragraph("MASTER INDEPENDENT CONTRACTOR AGREEMENT", title_style))
    story.append(Paragraph("This Independent Contractor Agreement (the \"Agreement\") is entered into as of October 1, 2026, by and between Apex Global Solutions LLC (\"Client\"), and Jane Doe (\"Contractor\").", body_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("1. Services and Deliverables", heading_style))
    story.append(Paragraph("Contractor agrees to perform software development, UI design, and related technical consulting services as specified in Exhibit A attached hereto.", body_style))

    story.append(Paragraph("2. Scope of Work and Revisions (Predatory Clause)", heading_style))
    story.append(Paragraph("Contractor shall perform all revisions and modifications requested by Client until Client expresses complete, subjective satisfaction with the final deliverable. Contractor shall not charge any additional fees for revisions, regardless of the number of rounds requested or whether the requests deviate from initial specifications.", body_style))

    story.append(Paragraph("3. Intellectual Property Assignment (Predatory Clause)", heading_style))
    story.append(Paragraph("Contractor irrevocably assigns and transfers to Client all right, title, and interest in and to all works of authorship, designs, source code, inventions, and ideas developed during this engagement immediately upon creation, irrespective of whether Contractor has been paid or compensated. Contractor agrees that all pre-existing tools, libraries, utility frameworks, and proprietary algorithms utilized in the work become the exclusive property of Client. Contractor expressly waives all moral rights and agrees never to display, reference, or publish the deliverables in Contractor's professional portfolio or website.", body_style))

    story.append(Paragraph("4. Payment Terms & Conditions (Predatory Clause)", heading_style))
    story.append(Paragraph("Client shall remit payment to Contractor on a Net 90 basis following final receipt of corresponding funds from Client's third-party customer (\"Pay-When-Paid\"). Client reserves the unilateral right to withhold payment or deduct penalties at its sole discretion if it deems work delayed. No late interest, penalties, or collection costs shall apply to overdue accounts.", body_style))

    story.append(Paragraph("5. Non-Compete and Exclusivity (Predatory Clause)", heading_style))
    story.append(Paragraph("During the term of this Agreement and for a period of twenty-four (24) months following termination for any reason, Contractor shall not directly or indirectly provide software engineering, design, or consulting services to any business, entity, or person engaged in digital technology anywhere worldwide.", body_style))

    story.append(Paragraph("6. Indemnification and Limitation of Liability (Predatory Clause)", heading_style))
    story.append(Paragraph("Contractor agrees to indemnify, defend, and hold harmless Client, its officers, directors, employees, and affiliates from and against any and all claims, liabilities, losses, damages, legal fees, and lost commercial profits arising out of or related to the deliverables. Contractor's liability under this Agreement shall be uncapped and unlimited. Client's maximum total aggregate liability to Contractor under any theory of law shall not exceed Ten US Dollars ($10.00).", body_style))

    story.append(Paragraph("7. Termination", heading_style))
    story.append(Paragraph("Client may terminate this Agreement at any time with or without cause upon immediate written notice, without obligation to compensate Contractor for work performed prior to notice.", body_style))

    story.append(Spacer(1, 15))
    story.append(Paragraph("IN WITNESS WHEREOF, the parties hereto have executed this Agreement.", body_style))

    doc.build(story)
    print(f"Sample predatory contract successfully generated at: {output_path}")

if __name__ == "__main__":
    generate_sample_pdf()

