"""Build the public CV: python3 scripts/build_cv.py (requires reportlab).

Layout follows FrancisXZhang_NIW_CV.pdf. Education, skills, talks, service,
and training use that supplied CV; recent publications come from index.html.
"""
from html import escape, unescape
from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    HRFlowable, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer,
    Table, TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'files' / 'Francis_Xiatian_Zhang_CV.pdf'
OUTPUT.parent.mkdir(exist_ok=True)
WIDTH = A4[0] - 144
LINK_COLOUR = '#c00083'
styles = {
    'name': ParagraphStyle('name', fontName='Times-Roman', fontSize=19, leading=24, alignment=TA_CENTER, spaceAfter=8),
    'contact': ParagraphStyle('contact', fontName='Times-Roman', fontSize=10, leading=12, alignment=TA_CENTER),
    'body': ParagraphStyle('body', fontName='Times-Roman', fontSize=10.3, leading=12.1, spaceAfter=3),
    'section': ParagraphStyle('section', fontName='Times-Bold', fontSize=12, leading=15, spaceBefore=9, spaceAfter=3, keepWithNext=True),
    'bullet': ParagraphStyle('bullet', fontName='Times-Roman', fontSize=10.3, leading=12.1, leftIndent=11, firstLineIndent=0, bulletIndent=0, spaceAfter=2),
    'publication': ParagraphStyle('publication', fontName='Times-Roman', fontSize=9.7, leading=11.5, leftIndent=10, bulletIndent=0, spaceAfter=6),
    'date': ParagraphStyle('date', fontName='Times-Italic', fontSize=10.3, leading=12.1, alignment=2),
}


def p(text, style='body', bullet=False):
    return Paragraph(text, styles[style], bulletText='•' if bullet else None)


def link(url, label):
    return f'<a href="{escape(url, quote=True)}" color="{LINK_COLOUR}">{escape(label)}</a>'


def heading(title):
    return [p(title, 'section'), HRFlowable(width='100%', thickness=0.5, color=colors.black, spaceAfter=4)]


def entry(title, date, details=(), italic=False):
    tag = 'i' if italic else 'b'
    row = Table([[p(f'<{tag}>{title}</{tag}>'), p(date, 'date')]], colWidths=[WIDTH * .67, WIDTH * .33])
    row.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    return KeepTogether([row] + [p(text, 'bullet', True) for text in details] + [Spacer(1, 3)])


def page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 10)
    canvas.drawCentredString(A4[0] / 2, 28, str(doc.page))
    canvas.restoreState()


story = [
    p('Francis Xiatian Zhang', 'name'),
    p('Email: ' + link('mailto:francis.zhang@ed.ac.uk', 'francis.zhang@ed.ac.uk') + ' | ' +
      link('mailto:francis.xiatian.zhang@outlook.com', 'francis.xiatian.zhang@outlook.com'), 'contact'),
    p('Personal Website: ' + link('https://francisxzhang.github.io/', 'francisxzhang.github.io'), 'contact'),
    p('LinkedIn: ' + link('https://www.linkedin.com/in/francis-xiatian-zhang/', 'linkedin.com/in/francis-xiatian-zhang'), 'contact'),
    p('Google Scholar: ' + link('https://scholar.google.com/citations?user=R04bvhAAAAAJ&hl=en', 'scholar.google.com/citations?user=R04bvhAAAAAJ') +
      ' | ' + link('https://github.com/FrancisXZhang', 'GitHub'), 'contact'),
    Spacer(1, 3),
    *heading('Education'),
    entry('Durham University, UK', 'Oct. 2021 – May 2025', [
        'PhD in Computer Science. Research: geometric representations for clinical video analysis, surgical workflow anticipation, and endoscopic video understanding.',
        'Supervisors: Dr Hubert P. H. Shum and Dr Noura Al Moubayed.',
    ], italic=True),
    entry("King’s College London, UK", 'Sep. 2020 – Sep. 2021', [
        'MRes in Healthcare Technologies — Distinction.',
        'Project: Extracting Novel Cardiovascular Risk Factors from Routine CT Volumes.',
    ], italic=True),
    entry('University of Southampton, UK', 'Sep. 2019 – Sep. 2020', [
        'MSc in Statistics with Applications in Medicine — Distinction.',
    ], italic=True),
    entry('Beijing University of Chinese Medicine, China', 'Sep. 2014 – Jul. 2019', [
        'Bachelor of Medicine — Upper Second-Class Honours.',
    ], italic=True),
    *heading('Research Statement'),
    p('I work on robot vision, particularly perception and navigation for robotic bronchoscopy. My current research combines geometric modelling and deep learning for depth estimation, visual odometry, and airway segmentation. I am interested in how robots recover 3D structure and motion from images, and how this information can support reliable navigation in challenging environments.'),
    *heading('Relevant Experience'),
    entry('Research Associate, University of Edinburgh, UK', 'Nov. 2024 – Present', [
        'Robot vision for bronchoscopic navigation: depth estimation, airway segmentation, visual odometry, and failure diagnosis. PI: Dr Mohsen Khadem.',
        'Collaborative work on continuum robot simulation and objective bronchoscopy skill assessment.',
    ]),
    entry('Research Assistant, Durham University, UK', 'Oct.–Nov. 2023;<br/>Jul.–Sep. 2024', [
        'Edge Computing and Analytics 2.0: teaching model training, ONNX export, and deployment through Python APIs. PI: Dr Anish Jindal.',
    ]),
    entry('Demonstrator, Durham University, UK', 'Nov. 2021 – Jun. 2024', [
        'Laboratory teaching in robotics, data science, programming, and text mining; instruction with Python, MATLAB, NVIDIA Jetson, and Puzzlebot.',
    ]),
    entry('Research Assistant, Northumbria University, UK', 'Apr. 2022 – Jul. 2022', [
        'Pose-based assessment of CPR skills; multi-camera data collection with nursing students and staff. PI: Dr Merryn Constable.',
    ]),
    *heading('Awards'),
    p('<b>2026:</b> ICRA Best Paper Award in Medical Robotics, for ' + link('https://arxiv.org/abs/2607.05162', 'Geometry-Aware Visual Odometry for Bronchoscopic Navigation via High-Gain Observer Fusion') + ' (co-author).'),
    p('<b>2020:</b> Dean’s List Award for Outstanding Achievement, University of Southampton.'),
    PageBreak(),
    *heading('Main Publications'),
    p('Selected publications in robotics, computer vision, and biomedical engineering. Full list: ' +
      link('https://scholar.google.com/citations?user=R04bvhAAAAAJ&hl=en', 'Google Scholar') + '.'),
]

html = (ROOT / 'index.html').read_text()
research = html.split('id="publications">', 1)[1].split('<!-- The Awards Section -->', 1)[0]
publications = re.findall(r'<li data-year="(\d+)" data-venue="([^"]+)"[^>]*>(.*?)</li>', research, re.S)
assert len(publications) == 13, 'Review extraction after changing the website structure.'
venue_names = {
    'MICCAI': 'International Conference on Medical Image Computing and Computer Assisted Intervention (MICCAI)',
    'ICRA': 'IEEE International Conference on Robotics and Automation (ICRA)',
    'IEEE TNSRE': 'IEEE Transactions on Neural Systems and Rehabilitation Engineering',
    'IEEE TMRB': 'IEEE Transactions on Medical Robotics and Bionics',
    'IJCARS': 'International Journal of Computer Assisted Radiology and Surgery',
}
selected = [item for item in publications if item[1] in venue_names]
selected.sort(key=lambda item: int(item[0]), reverse=True)
for year, venue, content in selected:
    title = unescape(re.search(r'<strong>(.*?)</strong>', content, re.S).group(1))
    authors = unescape(re.sub(r'<[^>]+>', '', re.split(r'<br\s*/?>', content)[1])).strip()
    authors = escape(authors).replace('Francis Xiatian Zhang', '<b>Francis Xiatian Zhang</b>')
    links = re.findall(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', content, re.S)
    resources = ' | '.join(link(unescape(url), unescape(label)) for url, label in links)
    citation = f'{authors} ({year}). {escape(title)}. <i>{venue_names[venue]}</i>. {resources}.'
    if title.startswith('Geometry-Aware Visual Odometry'):
        citation += ' <b>Best Paper Award in Medical Robotics.</b>'
    story.append(KeepTogether([p(citation, 'publication', True)]))

story += [
    PageBreak(),
    *heading('Skills'),
    p('<b>Programming:</b> Python, MATLAB, and R; PyTorch and TensorFlow.', 'bullet', True),
    p('<b>Computer vision:</b> Depth estimation, visual odometry, segmentation, pose estimation, video analysis, and graph-based modelling.', 'bullet', True),
    p('<b>Medical imaging:</b> CT, MRI, and fMRI processing; SPM12 and FreeSurfer.', 'bullet', True),
    p('<b>Statistical modelling:</b> Bayesian statistics, general linear models, survival analysis, and clinical trial design.', 'bullet', True),
    *heading('Talks and Conference Presentations'),
    p('Application of Graph Network Analysis in the Interpretation of Medical Data and Support of Clinical Decision-Making. <i>Beijing Integrated Medicine Committee Annual Conference, Psychiatry Workshop</i>, Beijing, China, November 2023.', 'bullet', True),
    p('Correlation-Distance Graph Learning for Treatment Response Prediction from rs-fMRI. <i>ICONIP 2023</i>, Hunan, China.', 'bullet', True),
    p('Towards Graph Representation Learning-Based Surgical Workflow Anticipation. <i>IEEE-EMBS BHI 2022</i>, Ioannina, Greece.', 'bullet', True),
    *heading('Service'),
    p('<b>Research Champion, National Institute for Health and Care Research (NIHR).</b> Appointed December 2023. Contributions to inclusive trial recruitment and discussions of AI-assisted, privacy-preserving recruitment.'),
    p('<b>Peer review:</b> International Conference on Medical Image Computing and Computer Assisted Intervention (MICCAI); IEEE International Conference on Robotics and Automation (ICRA); IEEE International Symposium on Biomedical Imaging (ISBI); IEEE Transactions on Image Processing (TIP); IEEE Robotics and Automation Letters (RA-L); IEEE Transactions on Medical Imaging (TMI); and IEEE Transactions on Neural Systems and Rehabilitation Engineering (TNSRE).'),
    *heading('Training'),
    p('<b>BMVA Computer Vision Summer School 2022</b>, University of East Anglia, UK, July 2022. Computer vision lectures and laboratory sessions.', 'bullet', True),
    p('<b>Clinical Clerkship</b>, Dongfang Hospital, Beijing University of Chinese Medicine, China, July 2018 – June 2019. Supervised experience in outpatient and inpatient departments.', 'bullet', True),
]

SimpleDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=72, rightMargin=72, topMargin=47, bottomMargin=43,
    title='Francis Xiatian Zhang — Curriculum Vitae', author='Francis Xiatian Zhang',
    subject='Robot vision, medical robotics, and computer vision', pageCompression=1,
).build(story, onFirstPage=page_number, onLaterPages=page_number)
print(OUTPUT)
