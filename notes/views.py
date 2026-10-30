from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.html import escape

from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


def create_demo_notes(topic, subject, detail_level, language):
    """
    Temporary demo notes.
    Gemini AI will replace this function in a later step.
    """

    if language == 'Hindi':
        introduction = (
            f"{topic} {subject} का एक महत्वपूर्ण विषय है। "
            "इस विषय को समझने के लिए इसकी परिभाषा, मुख्य विचार "
            "और उदाहरणों पर ध्यान दें।"
        )
        key_points = [
            "विषय की मूल परिभाषा और अर्थ समझें।",
            "मुख्य अवधारणाओं और उनके बीच के संबंधों को पहचानें।",
            "महत्वपूर्ण सूत्रों और उदाहरणों का अभ्यास करें।",
            "परीक्षा से पहले मुख्य बिंदुओं को दोहराएँ।",
        ]
        conclusion = "इन बिंदुओं को पढ़ें और अपनी पाठ्यपुस्तक के उदाहरणों से अभ्यास करें।"

    elif language == 'Marathi':
        introduction = (
            f"{topic} हा {subject} मधील एक महत्त्वाचा विषय आहे. "
            "हा विषय समजून घेण्यासाठी त्याची व्याख्या, मुख्य संकल्पना "
            "आणि उदाहरणे समजून घ्या."
        )
        key_points = [
            "विषयाची मूलभूत व्याख्या आणि अर्थ समजून घ्या.",
            "मुख्य संकल्पना आणि त्यांच्यातील संबंध ओळखा.",
            "महत्त्वाची सूत्रे आणि उदाहरणांचा सराव करा.",
            "परीक्षेपूर्वी महत्त्वाचे मुद्दे पुन्हा वाचा.",
        ]
        conclusion = "या मुद्द्यांचा अभ्यास करा आणि पाठ्यपुस्तकातील उदाहरणांचा सराव करा."

    else:
        introduction = (
            f"{topic} is an important topic in {subject}. "
            "To understand it, focus on its definition, key concepts "
            "and relevant examples."
        )
        key_points = [
            "Understand the basic definition and meaning of the topic.",
            "Identify the main concepts and how they are connected.",
            "Practise important formulas and examples, where applicable.",
            "Revise the key points before your examination.",
        ]
        conclusion = (
            "Review these points and practise examples from your textbook "
            "to strengthen your understanding."
        )

    notes = [
        {
            'heading': 'Introduction',
            'content': introduction,
        },
        {
            'heading': 'Key Points',
            'content': key_points,
        },
        {
            'heading': 'Conclusion',
            'content': conclusion,
        },
    ]

    if detail_level == 'Detailed':
        notes.append({
            'heading': 'Study Suggestions',
            'content': [
                'Read the topic carefully from your textbook.',
                'Write the important definitions in your own words.',
                'Solve practice questions related to the topic.',
            ],
        })

    return notes


def get_form_data(request):
    topic = request.POST.get('topic', '').strip()
    subject = request.POST.get('subject', 'Other').strip()
    detail_level = request.POST.get('detail_level', 'Standard')
    language = request.POST.get('language', 'English')

    allowed_subjects = [
        'Mathematics', 'Science', 'Physics', 'Chemistry',
        'Biology', 'Computer Science', 'English', 'Other'
    ]
    allowed_details = ['Short', 'Standard', 'Detailed']
    allowed_languages = ['English', 'Hindi', 'Marathi']

    if subject not in allowed_subjects:
        subject = 'Other'

    if detail_level not in allowed_details:
        detail_level = 'Standard'

    if language not in allowed_languages:
        language = 'English'

    return topic, subject, detail_level, language


@login_required(login_url='/accounts/login/')
def home(request):
    context = {
        'page_title': 'AI Notes Generator',
        'subjects': [
            'Mathematics', 'Science', 'Physics', 'Chemistry',
            'Biology', 'Computer Science', 'English', 'Other'
        ],
        'languages': ['English', 'Hindi', 'Marathi'],
        'detail_levels': ['Short', 'Standard', 'Detailed'],
    }

    if request.method == 'POST':
        topic, subject, detail_level, language = get_form_data(request)

        if topic:
            context.update({
                'topic': topic,
                'selected_subject': subject,
                'selected_detail': detail_level,
                'selected_language': language,
                'notes': create_demo_notes(
                    topic, subject, detail_level, language
                ),
            })
        else:
            context['error'] = 'Please enter a topic or syllabus.'

    return render(request, 'notes/home.html', context)


@login_required(login_url='/accounts/login/')
def download_pdf(request):
    if request.method != 'POST':
        return HttpResponse('Please submit the notes form to download a PDF.', status=405)

    topic, subject, detail_level, language = get_form_data(request)

    if not topic:
        return HttpResponse('A topic is required to create the PDF.', status=400)

    notes = create_demo_notes(topic, subject, detail_level, language)

    buffer = BytesIO()
    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'NotesTitle',
        parent=styles['Title'],
        textColor=colors.HexColor('#554be8'),
        alignment=TA_CENTER,
        spaceAfter=12,
    )
    heading_style = ParagraphStyle(
        'NotesHeading',
        parent=styles['Heading2'],
        textColor=colors.HexColor('#554be8'),
        spaceBefore=12,
        spaceAfter=6,
    )
    body_style = styles['BodyText']

    story = [
        Paragraph('LearnAble-AI Study Notes', title_style),
        Paragraph(f"<b>Topic:</b> {escape(topic)}", body_style),
        Paragraph(f"<b>Subject:</b> {escape(subject)}", body_style),
        Spacer(1, 12),
    ]

    for section in notes:
        story.append(Paragraph(escape(section['heading']), heading_style))

        content = section['content']

        if isinstance(content, list):
            for point in content:
                story.append(Paragraph(
                    '&bull; ' + escape(point),
                    body_style
                ))
                story.append(Spacer(1, 5))
        else:
            story.append(Paragraph(escape(content), body_style))

        story.append(Spacer(1, 8))

    document.build(story)
    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="learnable-ai-notes.pdf"'
    return response