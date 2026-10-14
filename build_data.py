"""Generate courseforphd/data.js from verified, hand-curated records + scraped IU history.

Every entry carries only facts seen in a primary source (handbook / bulletin / course
catalog / registrar archive). Anything not found is marked None and rendered as
"공개 자료로 확인 불가".
"""
import json
import io
import re

IU_JSON = "iu_instructors.json"
OUT = "data.js"

iu_hist_raw = json.load(io.open(IU_JSON, encoding="utf-8"))


def clean_name(n):
    n = re.sub(r"^(WEB|ARR)\s+", "", n).strip()
    return n


def iu_history(code):
    out = []
    for row in iu_hist_raw.get(code, []):
        names = []
        for n in row["instructors"]:
            n = clean_name(n)
            if n and n not in names:
                names.append(n)
        out.append({"term": row["term"], "names": names})
    return out


def c(code, title, cr, desc_en, desc_ko, **kw):
    d = {"code": code, "title": title, "cr": cr, "descEn": desc_en, "descKo": desc_ko}
    d.update(kw)
    return d


NO_DESC = None

# ---------------------------------------------------------------- FSU
FSU_SRC_24 = "FSU ISLT PhD Handbook 2024-25 (updated 2024-08-16)"
FSU_SRC_26 = "FSU ISLT PhD Handbook 2026-27 (updated 2026-08-17)"
FSU_BULL = "FSU Graduate Bulletin 2024-25 (course descriptions)"

fsu_courses = {
    "EME5601": c("EME 5601", "Introduction to Instructional Systems", 3,
                 "An overview of systems theory applied to instructional systems development, including principles and procedures for developing total instructional systems; the systematic approach to instructional design, the contexts in which it is applied, and the roles of instructional systems professionals.",
                 "교수체제 개발에 적용되는 체제 이론의 개관. 교수체제 전체를 개발하는 원리와 절차, 체계적 교수설계 접근, 그 적용 맥락, 교수체제 전문가의 역할을 다룸.",
                 descSrc=FSU_BULL),
    "EME5603": c("EME 5603", "Introduction to Systematic Instructional Design", 3,
                 "An introduction to the systematic design of instruction. Includes practical experience in developing and evaluating instructional materials.",
                 "교수의 체계적 설계 입문. 교수 자료를 개발·평가해 보는 실습 경험 포함.",
                 descSrc=FSU_BULL),
    "EME6677": c("EME 6677", "Advanced Instructional Design and Development", 3,
                 "Prerequisites: EDP 5216 and EME 5603. Explores theory and research that serve as the foundation for current and emerging instructional design practice; aimed at students who have already mastered basic ID and learning-theory knowledge.",
                 "선수과목: EDP 5216, EME 5603. 현재·신흥 교수설계 실천의 토대가 되는 이론과 연구를 탐구하는 고급 과목. 기초 교수설계·학습이론을 이미 익힌 대학원생 대상.",
                 descSrc=FSU_BULL),
    "EDP5216": c("EDP 5216", "Theories of Learning & Instruction (catalog: Theories of Learning and Cognition in Instruction)", 3,
                 "Focuses on applications of prominent contemporary theories of learning, cognition, and information processing to instructional settings.",
                 "대표적인 현대 학습·인지·정보처리 이론을 수업 장면에 적용하는 데 초점.",
                 descSrc=FSU_BULL),
    "EME5608": c("EME 5608", "Trends & Issues in Instructional Design", 3,
                 "An overview of the field of instructional design and technology. Includes historical perspective, research findings, and current issues and trends.",
                 "교수설계·교육공학 분야 개관. 역사적 관점, 연구 결과, 현재의 쟁점과 동향 포함.",
                 descSrc=FSU_BULL),
    "EDF5400": c("EDF 5400", "Basic Descriptive & Inferential Statistics Applications", "3 (2026-27) / 4 (2024-25)",
                 NO_DESC, None,
                 note="2024-25 핸드북·학교 카탈로그는 4학점, 2026-27 핸드북은 3학점으로 표기. 'if needed'(필요 시) 과목. 이번 조사에서 해당 과목의 공식 설명문은 확인하지 못함."),
    "EDF5401": c("EDF 5401", "General Linear Model Applications", 3,
                 "Prerequisite: EDF 5400. General linear model applications including multiple regression, ANOVA, ANCOVA, aptitude-treatment-interaction analysis, and other techniques.",
                 "선수과목: EDF 5400. 다중회귀, ANOVA, ANCOVA, 적성-처치 상호작용 분석 등 일반선형모형 응용.",
                 descSrc=FSU_BULL),
    "EDF5481": c("EDF 5481", "Methods of Educational Research", 3,
                 "A survey of selected types of educational research and appropriate related techniques; emphasis on criteria of validity.",
                 "선별된 교육연구 유형과 관련 기법을 개관하며 타당도 기준을 강조.",
                 descSrc=FSU_BULL),
    "EME5632": c("EME 5632", "Qualitative Research in ISLT", 3,
                 NO_DESC, None,
                 note="2026-27 핸드북에만 등장(EDF 5464와 택1). 2024 대학원 학칙집에서 과목 설명을 찾지 못함."),
    "EDF5464": c("EDF 5464", "Qualitative Research and Evaluation Methods", 3,
                 "Explores the foundations and basic methodological approaches to qualitative research in education (and, more broadly, the social sciences).",
                 "교육(더 넓게는 사회과학) 질적연구의 기초와 기본적 방법론적 접근을 탐구.",
                 descSrc=FSU_BULL),
    "EDF6499": c("EDF 6499", "Discourse and Conversation Analysis", 3,
                 "Prepares students to use discourse and conversation analysis techniques in their research.",
                 "연구에서 담화분석·대화분석 기법을 활용할 수 있도록 준비시킴.",
                 descSrc=FSU_BULL),
    "EME6694": c("EME 6694", "Academic Publishing in ISLT", 3,
                 "Addresses the academic publishing process and prepares students to disseminate research results at conferences and through academic journals and books.",
                 "학술 출판 과정을 다루며 학회·학술지·단행본을 통한 연구 성과 확산을 준비시킴. (카탈로그 제목: Academic Publishing in Instructional Systems and Learning Design)",
                 descSrc=FSU_BULL),
    "EME6060": c("EME 6060", "Collaborative Research in ISLT", "3–6",
                 NO_DESC, None,
                 note="2026-27 핸드북에 명시. 2024-25 핸드북에는 'EME6xxx Collaborative Research in ISLT'로 번호 미정 표기. 공식 과목 설명문은 확인하지 못함."),
    "EME6635": c("EME 6635", "Seminar in Advanced Instructional Systems Problems", 3,
                 "Prerequisites: EDG 6362 and EDF 5489. Offered periodically; addresses special topics not covered in other courses. May be repeated to a maximum of 6 credit hours.",
                 "선수과목: EDG 6362, EDF 5489. 간헐적으로 개설되며 다른 과목에서 다루지 않는 특수 주제를 다룸. 최대 6학점까지 반복 수강 가능.",
                 descSrc=FSU_BULL),
    "EDG6362": c("EDG 6362", "Instructional Systems Research Seminar", 3,
                 "Heightens students' awareness of the critical issues in instructional systems; examines how research methodologies have been used to study these issues, how research programs and theories are honed, and defines programmatic areas of disciplined inquiry.",
                 "교수체제의 핵심 쟁점에 대한 인식을 높임. 연구방법이 이 쟁점 연구에 어떻게 쓰였는지, 연구 프로그램·이론이 어떻게 정련되는지 살피고 체계적 탐구 영역을 규정.",
                 descSrc=FSU_BULL),
    "EDG6363": c("EDG 6363", "Research on Learning, Instruction, & Performance Systems", 3,
                 "Gives students hands-on experience applying research methods to address problems and answer questions in ISLT.",
                 "ISLT의 문제와 질문에 연구방법을 직접 적용해 보는 실습형 경험 제공.",
                 descSrc=FSU_BULL),
    "EME6665": c("EME 6665", "Synthesis, Analysis, and Argumentation in Instructional Systems Research", "3–6",
                 "Prerequisite: EDG 6362. Covers tools, techniques, and procedures for finding, synthesizing, analyzing, and summarizing research on past and ongoing topics in Instructional Systems. May be repeated to a maximum of 6 credit hours.",
                 "선수과목: EDG 6362. 교수체제 분야의 과거·진행 중 연구를 찾고 종합·분석·요약하는 도구와 절차를 다룸. 최대 6학점 반복 수강 가능.",
                 descSrc=FSU_BULL),
}

FSU_NO_SYL = {"status": "none", "note": "FSU 학적처(Registrar)는 강의계획서를 보관·공개하지 않으며, 각 개설 학과에 요청하도록 안내함. 공개된 공식 실라버스를 찾지 못함."}
FSU_NO_INSTR = {"status": "unavailable",
                "note": "학기별 담당 교수 이력은 공식 공개 자료에서 확인하지 못함. ISLT 교수진 명단은 아래 '교수진' 참조."}
for k, v in fsu_courses.items():
    v["syllabi"] = []
    v["syllabusNote"] = FSU_NO_SYL["note"]
    v["instructors"] = FSU_NO_INSTR

def pick(keys):
    return [fsu_courses[k] for k in keys]

fsu = {
    "id": "fsu",
    "short": "FSU",
    "univ": "Florida State University",
    "program": "Instructional Systems & Learning Technologies (ISLT) — Ph.D.",
    "unit": "Anne Spencer Daves College of Education, Health, and Human Sciences",
    "yearStatus": ("2025-26 학년도 전용 PhD 핸드북은 공개 자료에서 찾지 못했습니다. "
                   "대신 바로 앞(2024-25)과 바로 뒤(2026-27) 공식 핸드북을 모두 제시합니다. "
                   "2025-26 입학·적용 기준은 프로그램 오피스 확인이 필요합니다."),
    "versions": [
        {
            "id": "v26", "label": "2026-27 핸드북 (최신)", "source": FSU_SRC_26,
            "summary": [
                "정규 이수 총학점: 81학점(핸드북 기준 일반적 경우). 석사학위 소지 시 인정에 따라 감소 가능. FSU 이수 최소 48학점(수업 24 + 학위논문 24), 최대 150학점.",
                "Focus Area: 최소 9학점(핸드북 본문은 '최소 4과목 12학점·박사 연구 세미나 1개 포함'이라 설명 — 핸드북 내 표기 차이).",
                "학위논문 최소 24학점. 박사 연구 논문(Research Paper) + 연구 도제(Research Apprenticeship) 요건: 동료심사 학회/학술지에 게재 승인된 경험연구 논문(제1 또는 제2저자), 학위논문 등록 전 완료.",
                "PhD Director: Dr. Bret Staudt Willet (핸드북 명시).",
            ],
            "groups": [
                {"title": "Instructional Systems Foundations", "credits": "15", "courses": pick(["EDP5216", "EME5603", "EME5601", "EME6677", "EME5608"])},
                {"title": "Research Foundations", "credits": "9–13", "note": "EDF5400은 필요한 경우에만. 질적연구는 EME5632 또는 EDF5464 택1.", "courses": pick(["EDF5400", "EDF5401", "EDF5481", "EME5632", "EDF5464"])},
                {"title": "Instructional Systems Inquiry Core — Fall Cycle (최소 9학점)", "credits": "18–27 (Fall+Spring 합)", "courses": pick(["EDF6499", "EME6694", "EME6060", "EME6635"])},
                {"title": "Instructional Systems Inquiry Core — Spring Cycle (최소 9학점)", "credits": "", "courses": pick(["EDG6362", "EDG6363", "EME6665"])},
                {"title": "Focus Area · Dissertation", "credits": "Focus 최소 9 · Dissertation 최소 24", "note": "특정 과목번호 지정 없음. 지도교수·위원회와 구성.", "courses": []},
            ],
        },
        {
            "id": "v24", "label": "2024-25 핸드북", "source": FSU_SRC_24,
            "summary": [
                "정규 이수 총학점: 81학점(핸드북 기준). FSU 이수 최소 48학점(수업 24 + 논문 24), 최대 150학점.",
                "Research Foundations 6–10학점(EDF5400은 4학점, 필요 시). Inquiry Core 18–24학점: Fall Cycle 최소 3과목, Spring Cycle 최소 3과목.",
                "Fall Cycle 목록에 번호 미정 과목 2개: 'EME6xxx Qualitative Analysis in ISLT', 'EME6xxx Collaborative Research in ISLT'(번호 확정 전 표기).",
                "Focus Area 최소 9학점, Dissertation 최소 24학점.",
            ],
            "groups": [
                {"title": "Instructional Systems Foundations", "credits": "15", "courses": pick(["EME5601", "EME5603", "EME6677", "EDP5216", "EME5608"])},
                {"title": "Research Foundations", "credits": "6–10", "courses": pick(["EDF5400", "EDF5401", "EDF5481"])},
                {"title": "Inquiry Core — Fall Cycle (최소 3과목)", "credits": "18–24 (합)", "note": "EME6xxx Qualitative Analysis in ISLT (3), EME6xxx Collaborative Research in ISLT (3–6): 번호 미정으로 표기됨.", "courses": pick(["EME6694", "EDF6499", "EME6635"])},
                {"title": "Inquiry Core — Spring Cycle (최소 3과목)", "credits": "", "courses": pick(["EDG6362", "EDG6363", "EME6665"])},
                {"title": "Focus Area · Dissertation", "credits": "Focus 최소 9 · Dissertation 최소 24", "courses": []},
            ],
        },
    ],
    "faculty": {
        "note": "FSU Anne's College 교수·직원 디렉터리에 ISLT로 표시된 교수 8명(2026-10 조회). 개별 과목과의 매핑은 공개 자료에서 확인하지 못함.",
        "people": [
            "Dr. Kerry Burner — Associate Teaching Professor",
            "Dr. Secil Caskurlu — Assistant Professor",
            "Dr. Gi Woong Choi — Assistant Professor",
            "Dr. Vanessa Dennen — Mack and Effie Campbell Tyner Distinguished Professor",
            "Dr. Songhee Han — Assistant Professor",
            "Dr. Allan Jeong — Associate Professor",
            "Dr. Kadir Kozan — Assistant Professor",
            "Dr. Bret Staudt Willet — Associate Professor (PhD Director)",
        ],
        "url": "https://annescollege.fsu.edu/faculty-staff?name&category=101&employment_type=41",
    },
    "sources": [
        ("ISLT PhD Handbook 2026-27 (PDF)", "https://annescollege.fsu.edu/sites/default/files/2026-08/ISLT%20PhD%20Handbook%202026-27%20v081826_1112.pdf"),
        ("ISLT PhD Handbook 2024-25 (PDF)", "https://annescollege.fsu.edu/sites/g/files/upcbnu4516/files/2024-08/ISLT%20PhD%20Handbook%202024-25%20updated%2008-16-2024.pdf"),
        ("FSU ISLT Program Overview", "https://annescollege.fsu.edu/islt"),
        ("FSU Graduate Bulletin 2024-25 (PDF, 과목 설명 출처)", "https://registrar.fsu.edu/sites/g/files/upcbnu3886/files/documents/archive-bulletin-graduate/2024_grad_bulletin.pdf"),
        ("FSU ISLT 교수진 디렉터리", "https://annescollege.fsu.edu/faculty-staff?name&category=101&employment_type=41"),
    ],
    "pdfs": [
        ("ISLT PhD Handbook 2026-27", "https://annescollege.fsu.edu/sites/default/files/2026-08/ISLT%20PhD%20Handbook%202026-27%20v081826_1112.pdf"),
        ("ISLT PhD Handbook 2024-25", "https://annescollege.fsu.edu/sites/g/files/upcbnu4516/files/2024-08/ISLT%20PhD%20Handbook%202024-25%20updated%2008-16-2024.pdf"),
        ("FSU Graduate Bulletin 2024-25 (전체 PDF, 434쪽)", "https://registrar.fsu.edu/sites/g/files/upcbnu3886/files/documents/archive-bulletin-graduate/2024_grad_bulletin.pdf"),
    ],
}

# ---------------------------------------------------------------- IU
IU_SRC = "IU Bloomington SoE Graduate Bulletin 2025-2026 (archive)"
IU_ACAD = "IU Academic Bulletin course page"


def iu_course(code, title, cr, en, ko, hist_key, url, note=None, req=None, extra_syl=None):
    d = c(code, title, cr, en, ko, descSrc=IU_ACAD)
    d["syllabi"] = extra_syl or []
    d["syllabusNote"] = "IU 공식 사이트에서 공개된 강의계획서를 찾지 못함. 담당 학과(IST) 또는 강의 담당자에게 문의 필요."
    d["courseUrl"] = url
    if note:
        d["note"] = note
    hist = iu_history(hist_key) if hist_key else []
    if hist:
        d["instructors"] = {
            "status": "history",
            "note": ("IU 학사처 Course Browser 아카이브(공식)에 기록된 담당자. 이름은 사이트 표기 그대로(성 + 이름 이니셜). "
                     "제공 범위: 2004-05 ~ 2021년 학기. 2022학년도 이후 학기는 공개 아카이브에서 확인하지 못함."),
            "history": hist,
        }
    else:
        d["instructors"] = {"status": "unavailable", "note": "Course Browser 아카이브에서 해당 과목의 개설 기록을 찾지 못함."}
    return d


iu_r690 = iu_course("EDUC-R 690", "Application of Research Methods to Instructional Systems Technology Issues", 3,
                    "Problems of research are taken up with special emphasis on research designs for instructional systems technology. Students partake in the various aspects of a research project, including the writing of a research report. Part of the IST inquiry sequence; serves as IST's doctoral linkage course.",
                    "연구 문제를 다루되 교수체제기술(IST)에 맞는 연구설계를 특히 강조. 연구보고서 작성을 포함한 연구 프로젝트의 여러 측면에 직접 참여. IST 탐구(inquiry) 연계 과목이자 박사과정 연결(linkage) 과목.",
                    "R690", "https://academics.iu.edu/courses/bloomington/educ-r-690-application-of-research-methods-to-instructional-systems-technology-issues.html")
iu_r695 = iu_course("EDUC-R 695", "Topical Inquiry Seminar in Instructional Systems Technology (Variable Title)", "3 (×4회 = 12)",
                    "A critical examination of current inquiry in an emphasis area of instructional systems technology. Topics vary; students complete a research project; serves as an early inquiry experience for doctoral students.",
                    "교수체제기술 강조 영역의 최근 탐구에 대한 비판적 검토. 주제는 학기마다 달라지며 연구 프로젝트를 수행. 박사과정생의 초기 탐구 경험 과목. 박사과정에서는 4회 수강(12학점).",
                    "R695", "https://academics.iu.edu/courses/bloomington/educ-r-695-topical-inquiry-seminar-in-instructional-systems-technology-variable-title.html")
iu_r711 = iu_course("EDUC-R 711", "Readings in Instructional Technology", 3,
                    "Selected advanced readings in instructional technology and related fields with guidance from members of the IST faculty.",
                    "IST 교수진의 지도 아래 교수공학 및 관련 분야의 선별된 고급 문헌을 읽는 과목.",
                    "R711", "https://academics.iu.edu/courses/bloomington/educ-r-711-readings-in-instructional-technology.html")
iu_y502 = iu_course("EDUC-Y 502", "Intermediate Statistics Applied to Education", 3,
                    None, None, "Y502", "https://academics.iu.edu/courses/bloomington/educ-y-502-intermediate-statistics-applied-to-education.html",
                    note="공식 카탈로그에 과목 설명이 기재돼 있지 않음(3학점, 반복 수강 불가).")
iu_y521 = iu_course("EDUC-Y 521", "Methodological Approaches to Educational Inquiry", 3,
                    "Introduction to the various methodological approaches to the conduct of social sciences inquiry in general and educational inquiry in particular. Focus on the epistemological implications of methodological choices.",
                    "사회과학 및 교육 탐구 수행을 위한 다양한 방법론적 접근 입문. 방법론 선택이 갖는 인식론적 함의에 초점.",
                    "Y521", "https://academics.iu.edu/courses/bloomington/educ-y-521-methodological-approaches-to-educational-inquiry.html")
iu_y611 = iu_course("EDUC-Y 611", "Qualitative Inquiry in Education", 3,
                    "Examination of qualitative approaches to educational inquiry (e.g. case study, naturalistic inquiry, educational anthropology, educational connoisseurship and criticism). Exploration of methods for collecting and analyzing qualitative data, criteria for field studies, and approaches to writing up field studies.",
                    "교육 질적 탐구 접근(사례연구, 자연주의적 탐구, 교육인류학, 교육비평 등) 검토. 질적 자료 수집·분석 방법, 현장연구의 기준, 현장연구 보고서 작성 방법을 탐구.",
                    "Y611", "https://academics.iu.edu/courses/bloomington/educ-y-611-qualitative-inquiry-in-education.html")
iu_r795 = iu_course("EDUC-R 795", "Dissertation Proposal Preparation", 3,
                    "For the development of a dissertation proposal in Instructional Systems Technology. Consent of a dissertation director or prospective director required; students should be finished or nearly finished with program coursework. (1–3 credits, repeatable.)",
                    "IST 학위논문 계획서 개발을 위한 과목. 논문 지도교수(예정자)의 동의 필요. 프로그램 수업을 마쳤거나 거의 마친 단계에서 수강. (1–3학점, 반복 가능)",
                    "R795", "https://soegrbul.sites.iu.edu/courses/index.html")
iu_r795["descSrc"] = IU_SRC
iu_r795["instructors"] = {"status": "unavailable", "note": "개별 지도 형태의 과목. Course Browser에는 2004-05, 2005년 가을 기록만 있고 최근 기록은 확인하지 못함."}
iu_r799 = iu_course("EDUC-R 799", "Doctoral Dissertation in Instructional Systems Technology", 12,
                    "For Ph.D., reflects the ability to conduct an original piece of research. (Catalog: 1–15 credits, repeatable.)",
                    "Ph.D.의 경우 독창적 연구를 수행하는 능력을 보여주는 학위논문 과목. (카탈로그: 1–15학점, 반복 가능)",
                    None, "https://soegrbul.sites.iu.edu/courses/index.html")
iu_r799["descSrc"] = IU_SRC
iu_r799["instructors"] = {"status": "unavailable", "note": "개인 지도교수가 담당하는 논문 과목으로 공개 학기 이력이 없음."}

iu = {
    "id": "iu",
    "short": "IUB",
    "univ": "Indiana University Bloomington",
    "program": "Instructional Systems Technology (IST) — Ph.D.",
    "unit": "School of Education · Department of Learning, Design, and Adult Education",
    "yearStatus": "2025-26 School of Education Graduate Bulletin(아카이브)의 Ph.D. in Instructional Systems Technology 페이지 기준으로 확인했습니다. 2026-27 현행 페이지의 학점·필수과목 구조도 동일하게 확인했습니다.",
    "versions": [
        {
            "id": "v2526", "label": "2025-26 Graduate Bulletin", "source": IU_SRC,
            "summary": [
                "총 90학점. Major 42 + Inquiry 9 + Minor 12 + Foundation 6 + Elective 6 + Dissertation 15.",
                "Major 42 = IST Core 18 (R690, R695×4, R711) + IST Electives 24(박사 자문위원회가 승인하는 IST 대학원 과목; 특정 과목 지정 없음).",
                "Inquiry 9학점은 위원회 승인 시 inquiry 정책에 따라 대체 가능.",
                "Minor 12학점: 주전공과 보완적이어야 하며 전공(IST) 과목은 사용 불가. 학제간·개별 minor는 Request for Individualized Minor eDoc 승인 필요.",
                "Foundation 6학점: IST 외 교육대학 과목(주로 교육심리·교육기초). Elective 6학점: 위원회가 승인한 대학원 과목.",
            ],
            "groups": [
                {"title": "IST Core (Major)", "credits": "18", "courses": [iu_r690, iu_r695, iu_r711]},
                {"title": "IST Electives (Major)", "credits": "24", "note": "특정 과목 미지정 — 박사 자문위원회가 승인하는 IST 대학원 과목.", "courses": []},
                {"title": "Inquiry Requirements", "credits": "9", "note": "위원회 승인 하에 inquiry 정책에 따른 대체 가능. 승인된 inquiry 과목 목록은 IU 교육대학 사이트 참조.", "courses": [iu_y502, iu_y521, iu_y611]},
                {"title": "Minor", "credits": "12", "note": "특정 과목 미지정.", "courses": []},
                {"title": "Foundation", "credits": "6", "note": "IST 외 교육대학 과목(교육심리·교육기초 등). 특정 과목 미지정.", "courses": []},
                {"title": "Electives", "credits": "6", "note": "위원회 승인 대학원 과목.", "courses": []},
                {"title": "Dissertation", "credits": "15", "courses": [iu_r795, iu_r799]},
            ],
        }
    ],
    "faculty": {
        "note": "현 IST 교수진 명단·과목 매핑은 이번 조사에서 확인하지 못했습니다. 아래 '담당 이력'은 IU 학사처 아카이브(2004-05~2021)에 기재된 이름 그대로입니다.",
        "people": [],
        "url": "https://education.indiana.edu/programs/instructional-systems-technology.html",
    },
    "sources": [
        ("Ph.D. in IST — 2025-26 Graduate Bulletin (archive)", "https://soegrbul.sites.iu.edu/archive/2025-2026/program-requirements/ist/phd-in-instructional-systems-technology.html"),
        ("Ph.D. in IST — 현행(2026-27) Graduate Bulletin", "https://soegrbul.sites.iu.edu/program-requirements/ist/phd-in-instructional-systems-technology.html"),
        ("IU 교육대학 승인 inquiry 과목", "https://education.indiana.edu/students/graduates/approved-coreinquiry-courses.html"),
        ("IU 학사처 Course Browser (담당 이력 출처)", "https://utilities.registrar.indiana.edu/course-browser/"),
        ("IU Academic Bulletin — 과목 페이지 (예: R 711)", "https://academics.iu.edu/courses/bloomington/educ-r-711-readings-in-instructional-technology.html"),
        ("IU SoE Graduate Bulletin — 과목 목록", "https://soegrbul.sites.iu.edu/courses/index.html"),
    ],
    "pdfs": [],
}

# ---------------------------------------------------------------- PSU
PSU_SRC = "Penn State Graduate Bulletin 2025-2026 (archive)"
PSU_DESC = "Penn State University Bulletin — LDT course descriptions"
PSU_NO_INSTR = {"status": "unavailable",
                "note": "학기별 담당 교수 이력은 공식 공개 자료에서 확인하지 못함(Penn State Schedule of Courses/프로그램 오피스 문의 필요). LDT 교수진 명단은 아래 참조."}


def psu(code, title, cr, en, ko, syl_slug=None, note=None, prereq=None):
    d = c(code, title, cr, en, ko, descSrc=PSU_DESC)
    if prereq:
        d["prereq"] = prereq
    d["syllabi"] = []
    if syl_slug:
        base = "https://courses.worldcampus.psu.edu/welcome/%s/001" % syl_slug
        d["syllabi"] = [
            {"label": "샘플 실라버스 PDF (2026-10-14 저장본)", "url": "syllabi/PSU_%s_sample_syllabus.pdf" % syl_slug.upper(), "local": True},
            {"label": "원문 HTML (Penn State)", "url": base + "/common/wrapsyllabus"},
            {"label": "강의 개요 페이지", "url": base},
        ]
        d["syllabusNote"] = ("Penn State World Campus가 공개한 대표(예시) 실라버스입니다. 페이지 자체가 "
                             "'일정·과제·자료는 예시이며 확정본은 개강 3–4주 전 온라인 카탈로그 확인'이라고 명시합니다. "
                             "PDF는 원문 HTML 페이지를 2026-10-14에 그대로 인쇄 저장한 사본이며(저작권은 Penn State), 담당 교수는 표기돼 있지 않습니다.")
    else:
        d["syllabusNote"] = "공개된 공식 실라버스를 찾지 못함."
    d["instructors"] = PSU_NO_INSTR
    if note:
        d["note"] = note
    return d


psu_core = [
    psu("LDT 527", "Designing Constructivist Learning Environments", 3,
        "Designing learning environments based on constructivist principles of learning that provide modeling, coaching, and scaffolding.",
        "모델링·코칭·스캐폴딩을 제공하는 구성주의 학습 원리 기반 학습환경 설계.", "ldt527"),
    psu("LDT 581", "Theoretical Foundations of Learning, Design, and Technology", 3,
        "Analysis of theoretical foundations of the instructional systems (systems and cybernetics, communications, cognitive psychology, sociological, constructivist, ecological) for doctoral students.",
        "교수체제의 이론적 토대(체제·사이버네틱스, 커뮤니케이션, 인지심리, 사회학적, 구성주의, 생태학적 관점) 분석. 박사과정생 대상.",
        "ldt581", prereq="Ph.D. 또는 D.Ed. candidacy"),
    psu("LDT 583", "Survey of Research in Learning Sciences and Technology", 3,
        "Analysis and evaluation of research in domains of learning sciences and technology. Reviews the empirical research literature from the Learning Sciences and Technology fields. (Cross-listed with SCIED 583.)",
        "학습과학·기술 분야 연구의 분석과 평가. 학습과학·기술 분야의 경험적 연구 문헌을 검토. (SCIED 583과 교차개설)"),
]
psu_comp = [
    psu("LDT 505", "Integrating Mobile Technologies into Learning Environments", 3,
        "Research on learning with mobile computers and models for mobile computer integration for K-12 schools, community organizations, and universities.",
        "모바일 컴퓨터를 활용한 학습 연구와 K-12 학교·지역 기관·대학에서의 모바일 통합 모형.", "ldt505"),
    psu("LDT 550", "Learning Design Studio", "3 (최대 12)",
        "Examines a range of skills, processes, and theories for designing and developing interactive educational materials.",
        "상호작용적 교육 자료를 설계·개발하기 위한 다양한 기술·과정·이론을 탐구.", "ldt550"),
    psu("LDT 586", "Diffusion and Adoption of Innovations and Change", 3,
        "Understanding change process in educational contexts, comparing various models, tailoring them to individual needs, and creating personalized model of change.",
        "교육 맥락의 변화 과정을 이해하고 여러 모형을 비교하며 개인 필요에 맞게 조정해 자신만의 변화 모형을 만듦."),
    psu("LDT 544", "Video for Instruction, Training, and Research", 3,
        "Theory, design models, and methodologies supporting the use of video in a variety of learning environments.",
        "다양한 학습환경에서 비디오를 활용하기 위한 이론·설계 모형·방법론.", prereq="INSYS 447"),
    psu("LDT 549", "Current Topics in Emerging Technologies", 3,
        "An in-depth seminar on the instructional and training design implications of specific new technologies as they emerge.",
        "새로 등장하는 특정 기술이 교수·훈련 설계에 주는 함의를 심층 다루는 세미나."),
    psu("LDT 574", "Applied Qualitative Research for Work Practice, Innovation, and Systems Design", 3,
        "Investigates qualitative research paradigms and methodologies; develops skills in use of ethnographic methods in work practice, innovation and systems design.",
        "질적연구 패러다임과 방법론을 탐구하고, 업무 실천·혁신·시스템 설계에서의 민족지적 방법 활용 기술을 기름.", prereq="ADTED 550"),
    psu("LDT 575", "Designing Experimental Research in Learning, Design, and Technology", 3,
        "Designing research studies in Learning, Design, and Technology of a quantitative and experimental nature, which results in a research proposal.",
        "학습·설계·기술 분야의 양적·실험적 연구를 설계하고 그 결과로 연구계획서를 작성."),
    psu("LDT 576", "Design-based Research Methods, Applications for Educational Research", 3,
        "The course focuses on design-based research methods in education.",
        "교육 분야 설계기반연구(design-based research) 방법에 초점."),
    psu("LDT 832", "Designing e-learning Within Course Management Systems", 3,
        "Practical design of instructor-facilitated online lessons taking advantage of the affordances and within the constraints of course management systems.",
        "교수자 촉진형 온라인 수업을 학습관리시스템의 특성과 제약 안에서 실제로 설계.", "ldt832"),
]
psu_594 = psu("LDT 594", "Research Topics", "1–18 (박사: 9학점 필수)",
              "Supervised student activities on research projects identified on an individual or small group basis.",
              "개인 또는 소집단 단위로 정한 연구 프로젝트를 지도받아 수행하는 활동.")

psu_prog = {
    "id": "psu",
    "short": "PSU",
    "univ": "The Pennsylvania State University",
    "program": "Learning, Design, and Technology (LDT) — Ph.D.",
    "unit": "College of Education · University Park (Ph.D.는 University Park 캠퍼스)",
    "yearStatus": "Penn State Graduate Bulletin 2025-2026 아카이브 페이지로 직접 확인했습니다. 현행 2026-27 페이지와 필수/선택 과목 구성이 동일합니다.",
    "versions": [
        {
            "id": "v2526", "label": "2025-26 Graduate Bulletin", "source": PSU_SRC,
            "summary": [
                "LDT 최소 30학점: 박사 핵심 9 + LDT 594 9 + 역량(competency) 500단계 LDT 과목 최소 12학점. 이후 추가 과목은 박사 위원회가 결정. (졸업학점 하한은 대학원 차원에서 정해져 있지 않은 역량 기반 학위.)",
                "Communication 요건: 응용통계 1과목 + (고급통계 1과목 또는 고급 질적분석 1과목). 특정 과목 지정 없음.",
                "타 학과 과목은 박사 위원회·대학원 프로그램 책임자(DGS) 승인 시 인정.",
                "거주 요건: University Park에서 풀타임 연속 2학기 이상.",
                "자격시험(Qualifying): 학사 후 18학점 이상 이수 뒤, 입학 후 3학기 이내(여름 제외) 응시 권장, LDT 교수진 승인 필요. 종합시험(Comprehensive): 모든 수업 후. 학위논문 + 최종 구술 심사.",
                "이중 전공 옵션: LDT + Comparative and International Education(CIED) 듀얼 타이틀.",
            ],
            "groups": [
                {"title": "Doctoral Core (모두 필수)", "credits": "9", "courses": psu_core},
                {"title": "Core Competency (아래 목록 등에서 선택; 목록이 전부는 아님)", "credits": "12",
                 "note": "공식 예시 경로 — 교수설계: LDT 550, 549, 832 / 학습과학·기술: LDT 505, 574, 576, 544.", "courses": psu_comp},
                {"title": "Research", "credits": "9", "courses": [psu_594]},
            ],
        }
    ],
    "faculty": {
        "note": "Penn State College of Education LDT 교수 명단(검색으로 확인한 공식 페이지 요약, 2026-10 조회) 및 Bulletin 기재 직책. 개별 과목과의 매핑은 공개 자료에서 확인하지 못함.",
        "people": [
            "Marcela Borge",
            "Tyler Hollett",
            "Madison Allen Kuyenga",
            "ChanMin Kim",
            "Susan Land",
            "Dylan Paré",
            "Natalie Annabelle Rae",
            "Priya Sharma — Director of Graduate Studies (Bulletin 기재)",
            "Heather Zimmerman — Graduate Program Head (Bulletin 기재)",
        ],
        "url": "https://ed.psu.edu/academics/departments/department-learning-and-performance-systems/ldt-faculty",
    },
    "sources": [
        ("LDT Ph.D. — 2025-26 Graduate Bulletin (archive)", "https://bulletins.psu.edu/archive/2025-2026/graduate/programs/majors/learning-design-technology/"),
        ("LDT — 현행(2026-27) Graduate Bulletin", "https://bulletins.psu.edu/graduate/programs/majors/learning-design-technology/"),
        ("LDT 과목 설명 (University Bulletin)", "https://bulletins.psu.edu/university-course-descriptions/graduate/ldt/"),
        ("LDT 과목 설명 PDF", "https://bulletins.psu.edu/university-course-descriptions/graduate/ldt/ldt.pdf"),
        ("World Campus 샘플 실라버스 — LDT 581", "https://courses.worldcampus.psu.edu/welcome/ldt581/001/common/wrapsyllabus"),
        ("LDT 교수진 (College of Education)", "https://ed.psu.edu/academics/departments/department-learning-and-performance-systems/ldt-faculty"),
        ("Penn State LDT Ph.D. 안내", "https://ed.psu.edu/phd-degree-learning-design-and-technology"),
    ],
    "pdfs": [
        ("LDT 과목 설명 PDF (University Bulletin)", "https://bulletins.psu.edu/university-course-descriptions/graduate/ldt/ldt.pdf"),
        ("LDT 학위 요건 PDF (Graduate Bulletin, 현행)", "https://bulletins.psu.edu/graduate/programs/majors/learning-design-technology/learning-design-technology_degreerequirementstext.pdf"),
    ],
}

data = {
    "asOf": "2026-10-14",
    "programs": [fsu, iu, psu_prog],
}

with io.open(OUT, "w", encoding="utf-8") as f:
    f.write("window.CFP_DATA = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n")
print("wrote", OUT)
