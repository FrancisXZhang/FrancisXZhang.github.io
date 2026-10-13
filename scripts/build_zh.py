"""Build index-zh.html from index.html: python3 scripts/build_zh.py.

Translate the surrounding website while preserving English publication entries.
Update the corresponding translation when changing English prose; an unmatched
translation raises an error so the Chinese page cannot silently become stale.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'index.html'
OUTPUT = ROOT / 'index-zh.html'

TRANSLATIONS = [
    ('<title>Francis Xiatian Zhang</title>', '<title>张夏天 | Francis Xiatian Zhang</title>'),
    ('<h1>Francis Xiatian Zhang</h1>', '<h1>张夏天（Francis Xiatian Zhang）</h1>'),
    ('Francis Xiatian Zhang, Research Associate at the University of Edinburgh, working on robot vision, 3D perception, and visual navigation.',
     '张夏天（Francis Xiatian Zhang），爱丁堡大学研究员，研究方向为机器人视觉、三维感知与视觉导航。'),
    ('aria-label="Website language"', 'aria-label="网站语言"'),
    ('>Home</a>', '>首页</a>'),
    ('>News</a>', '>动态</a>'),
    ('>Projects</a>', '>项目</a>'),
    ('>Research</a>', '>研究</a>'),
    ('>Awards</a>', '>获奖</a>'),
    ('>Experience</a>', '>经历</a>'),
    ('>Grants</a>', '>科研资助</a>'),
    ('title="close side menu"', 'title="关闭侧边菜单"'),
    ('alt="profile photo"', 'alt="个人照片"'),
    ('I am a Research Associate at the University of Edinburgh working on robot vision, with interests in 3D perception, motion estimation, and visual navigation. My research combines geometric modelling and deep learning, with recent work on depth estimation, visual odometry, and segmentation for medical robotics and bronchoscopic navigation. I received my PhD from Durham University, where I studied geometric representations for clinical video analysis. More broadly, I am interested in how robots use visual information to understand their surroundings and navigate reliably, and I am open to research and engineering opportunities in robotic perception and applied computer vision.',
     '我目前在爱丁堡大学担任研究员（Research Associate），研究方向为机器人视觉，主要关注三维感知、运动估计与视觉导航。我的研究结合几何建模与深度学习，近期工作包括深度估计、视觉里程计和分割，并将这些方法应用于医疗机器人与支气管镜导航。我在杜伦大学获得计算机科学博士学位，博士期间研究临床视频分析中的几何表示。更广泛地，我希望探索机器人如何利用视觉信息理解周围环境并实现可靠导航，也期待机器人感知与计算机视觉领域的研究和工程合作机会。'),
    ('>CV (PDF)</a>', '>简历（英文 PDF）</a>'),
    ('>Email</a>', '>个人邮箱</a>'),
    ('>Academic Email</a>', '>学术邮箱</a>'),
    ('> University Profile </a>', '> 大学主页 </a>'),
    ('>Google Scholar</a>', '>谷歌学术</a>'),
    ('<h2>News</h2>', '<h2>动态</h2>'),
    ('Our paper', '我们的论文'),
    ('received the <strong>ICRA 2026 Best Paper Award in Medical Robotics</strong>.',
     '获得了 <strong>ICRA 2026 医疗机器人最佳论文奖</strong>。'),
    ('was selected as a finalist for the <a href="https://2026.ieee-icra.org/awards/"><strong>ICRA 2026 Best Paper Award in Medical Robotics</strong></a>.',
     '入围 <a href="https://2026.ieee-icra.org/awards/"><strong>ICRA 2026 医疗机器人最佳论文奖</strong></a>。'),
    ('— accepted at <strong>MICCAI 2026</strong>.', '——被 <strong>MICCAI 2026</strong> 接收。'),
    ('— accepted.', '——已接收。'),
    ('Three papers at <strong>ICRA</strong> —', '三篇论文被 <strong>ICRA</strong> 接收：'),
    ('Two papers at <strong>MICCAI 2025</strong> —', '两篇论文被 <strong>MICCAI 2025</strong> 接收：'),
    ('(accepted)', '（已接收）'),
    ('(early accepted)', '（提前接收）'),
    ('I officially received approval for my PhD thesis—finally a formal PhD now!', '博士论文正式获批，顺利获得博士学位。'),
    ('I passed my PhD viva with minor corrections. Examiners:', '通过博士论文答辩，仅需小幅修改。答辩考官：'),
    ('I began serving as a Research Associate at the <strong>University of Edinburgh</strong>', '开始在<strong>爱丁堡大学</strong>担任研究员（Research Associate）'),
    ('I began working as a Research Assistant on the project', '开始担任研究助理，参与项目'),
    ('>Dataset</a>', '>数据集</a>'),
    ('<h2>Recent Projects</h2>', '<h2>近期项目</h2>'),
    ('<strong>ICRA 2026 · Best Paper Award in Medical Robotics</strong>', '<strong>ICRA 2026 · 医疗机器人最佳论文奖</strong>'),
    ('aria-label="View RGB and depth results from the visual odometry paper"', 'aria-label="查看视觉里程计论文中的 RGB 图像与深度结果"'),
    ('aria-label="Bronchoscopy frame with detected lumens and estimated camera heading"', 'aria-label="支气管镜图像中的气道腔口检测与相机朝向估计"'),
    ('aria-label="Corresponding estimated airway depth map"', 'aria-label="对应的气道深度估计图"'),
    ('>Depth</span>', '>深度</span>'),
    ('Combines depth-based airway geometry with high-gain observer fusion to improve bronchoscopic tracking and reduce trajectory drift.',
     '结合基于深度的气道几何信息与高增益观测器融合，改善支气管镜视觉跟踪并降低轨迹漂移。'),
    ('My contribution: provided the depth-perception foundation through <a href="#brea-depth">BREA-Depth</a>, supporting lumen localization and geometric heading estimation.',
     '我的贡献：通过 <a href="#brea-depth">BREA-Depth</a> 提供深度感知基础，支持气道腔口定位和几何朝向估计。'),
    ('Reduced absolute trajectory error by over 50% compared with baseline visual odometry pipelines in ex-vivo lung experiments.',
     '在离体肺实验中，相比对照视觉里程计方法，绝对轨迹误差降低超过 50%。'),
    ('>Award</a>', '>奖项</a>'),
    ('I design and build applied machine learning systems for safety-critical and data-constrained domains, with an emphasis on end-to-end pipelines: data curation, model training, evaluation, and deployment-ready inference. My work spans geometry-aware perception, temporal and graph-based modeling, and reproducible tooling that produces integration-friendly outputs (e.g., depth, graphs, structured predictions) for downstream systems. If you’d like to collaborate, please reach out at',
     '我面向对安全性要求较高、数据有限的应用场景开展机器学习研究，关注从数据整理、模型训练和评估到推理部署的完整流程。我的工作涉及几何感知、时序建模和图学习，并提供可复现的工具，为后续系统输出深度、图结构和其他结构化预测。如有合作意向，欢迎联系'),
    ('(primary) or', '（个人邮箱）或'),
    ('(academic).', '（学术邮箱）。'),
    ('alt="Airway segmentation before and after FDRAS: nnUNet input and refined output on AeroPath"', 'alt="FDRAS 气道分割修复前后对比：AeroPath 数据上的 nnUNet 输入与修复输出"'),
    ('Diagnoses and repairs structural failures in chest CT airway segmentations, using predicted error maps to guide targeted corrections.',
     '诊断并修复胸部 CT 气道分割中的结构性错误，通过预测误差图指导有针对性的修正。'),
    ('Localizes boundary discrepancies and disconnected branches with geometric and tree-level connectivity error maps.',
     '利用几何误差图和树结构连通性误差图，定位边界偏差及断裂分支。'),
    ('Provides a trained checkpoint, training and inference scripts, and error-map visualization tools.',
     '提供预训练模型、训练与推理脚本，以及误差图可视化工具。'),
    ('>Paper</a>', '>论文</a>'),
    ('alt="TCM-AQA61 dataset examples showing acupuncture and Tuina training from first-person and third-person views"', 'alt="TCM-AQA61 数据集中的针灸与推拿训练示例，包含第一人称和第三人称视角"'),
    ('Assesses acupuncture and Tuina training skills by combining visual and pose features, learning from first-person and third-person videos while requiring only a third-person view at inference.',
     '结合视觉与姿态特征评估针灸和推拿训练技能。训练阶段同时使用第一人称与第三人称视频，推理阶段仅需第三人称视角。'),
    ('Introduces two synchronized dual-view datasets with expert annotations from 61 participants for each task.',
     '构建两个同步双视角数据集，每项任务包含 61 名参与者，并由专家提供标注。'),
    ('Provides training and inference code, sample videos, and demonstrations of skill assessment.',
     '提供训练与推理代码、示例视频和技能评估演示。'),
    ('alt="BREA-Depth airway depth illustration"', 'alt="BREA-Depth 气道深度估计示例"'),
    ('Publishes ready-to-run inference code for bronchoscopic navigation research stacks, adapting foundation models to bronchoscopy footage so downstream perception modules inherit reliable depth.',
     '提供可直接运行的支气管镜导航深度推理代码，将基础模型适配到支气管镜视频，为后续感知模块提供可靠的深度信息。'),
    ('Produces stable depth estimates that downstream planners can use for CT-to-video alignment and collision checks.',
     '生成稳定的深度估计，可用于后续规划中的 CT 与视频对齐及碰撞检测。'),
    ('Pipeline: synthetic airway renderer → domain adaptation → depth inference package → evaluation harness, all versioned so surgical robotics teams can reproduce deployments.',
     '流程包括合成气道渲染、域适配、深度推理和评估工具，并通过版本管理支持手术机器人研究团队复现实验与部署。'),
    ('alt="Adaptive graph learning visualization"', 'alt="自适应图学习可视化"'),
    ('Turns live tool detections into actionable workflow forecasts so scrub nurses and displays know what to prepare next.',
     '利用实时手术器械检测预测后续工作流程，为器械准备与信息展示提供参考。'),
    ('Continuously re-learns instrument relationships from spatial cues to surface impending steps minutes ahead.',
     '根据空间线索持续更新器械之间的关系，提前预测后续手术步骤。'),
    ('Prototype pipeline: detector feed → spatial graph builder → anticipation head → dashboard concept, with warning throttling heuristics and fallbacks when detections drop.',
     '原型流程包括器械检测、空间图构建、流程预测和信息展示，并考虑了提示频率控制与检测缺失时的处理。'),
    ('alt="DAEVI depth-aware inpainting visualization"', 'alt="DAEVI 深度感知视频修复示例"'),
    ('Provides a depth-aware inpainting toolkit that teams can run locally to clean surgeon video archives prior to research sharing or dataset release.',
     '提供可在本地运行的深度感知视频修复工具，用于研究共享或数据集发布前的手术视频处理。'),
    ('Accepts raw video plus masks and returns temporally consistent fills, ready for downstream training or review.',
     '输入原始视频与掩膜，输出时间一致的视频修复结果，供后续模型训练或审阅使用。'),
    ('Bundled training/inference scripts with deterministic preprocessing and checkpoints so biomedical researchers can rerun inpainting and compare outputs to their own reference sets.',
     '提供训练与推理脚本、确定性的预处理流程和模型权重，便于生物医学研究人员复现修复结果并进行比较。'),
    ('<h2>Research</h2>', '<h2>研究</h2>'),
    ('My research focuses on <strong>Computer-assisted Intervention</strong>, <strong>Medical Robotics</strong>, and <strong>Vision-based Skill Assessment</strong>. Below are selected publications, including recent collaborations in biomedical engineering and medical robotics. A complete list of my publications can be found on my <a href="https://scholar.google.com/citations?user=R04bvhAAAAAJ&hl=en">Google Scholar</a> page.',
     '我的研究涉及<strong>计算机辅助介入</strong>、<strong>医疗机器人</strong>和<strong>基于视觉的技能评估</strong>。以下为部分代表性论文，包括近年来在生物医学工程与医疗机器人领域的合作工作。完整论文列表请见我的<a href="https://scholar.google.com/citations?user=R04bvhAAAAAJ&hl=en">谷歌学术</a>主页。'),
    ('aria-label="Browse papers by keyword"', 'aria-label="按关键词浏览论文"'),
    ('>All selected work</button>', '>全部精选论文</button>'),
    ('>Robotics</button>', '>机器人</button>'),
    ('>Computer Vision</button>', '>计算机视觉</button>'),
    ('>Medical Imaging</button>', '>医学影像</button>'),
    ('data-template="{count} papers · {topic}"', 'data-template="{count} 篇论文 · {topic}"'),
    ('<h2>Awards</h2>', '<h2>获奖</h2>'),
    ('2026, ICRA Best Paper Award in Medical Robotics', '2026，ICRA 医疗机器人最佳论文奖'),
    ('Awarded to', '获奖论文：'),
    (', co-authored with Mohammadreza Kasaei, Feng Li, Farshid Alambeigi, Kevin Dhaliwal and Mohsen Khadem.', '；与 Mohammadreza Kasaei、Feng Li、Farshid Alambeigi、Kevin Dhaliwal 和 Mohsen Khadem 合作完成。'),
    ("2020, Dean's List Award for Outstanding Achievement,", '2020，院长优秀表现奖（Dean’s List Award），'),
    ('>Mathematics Science, Faculty of Social Sciences, University of Southampton</a>', '>南安普顿大学社会科学学院数学学科</a>'),
    ('<h2>Experience</h2>', '<h2>经历</h2>'),
    ('Research Associate at <a href="https://www.ed.ac.uk/">The University of Edinburgh</a>, 11/2024-.', '研究员（Research Associate），<a href="https://www.ed.ac.uk/">爱丁堡大学</a>，2024 年 11 月至今。'),
    ('Develops deep learning visual navigation prototypes for robotic bronchoscopy—airway segmentation, geometric graph construction, and failure-aware inference evaluated on recorded clinical video streams.',
     '开发面向机器人支气管镜的深度学习视觉导航原型，涉及气道分割、几何图构建和错误感知推理，并在已采集的临床视频上进行评估。'),
    ('Research Assistant at <a href="https://www.durham.ac.uk/">Durham University</a>, 10/2023-11/2023;7/2024-9/2024.', '研究助理，<a href="https://www.durham.ac.uk/">杜伦大学</a>，2023 年 10–11 月；2024 年 7–9 月。'),
    ('Delivered the Edge Computing and Analytics 2.0 course by teaching end-to-end model workflows—from training to ONNX export and deployment through Python APIs with lightweight GUIs.',
     '参与 Edge Computing and Analytics 2.0 课程教学，涵盖模型训练、ONNX 导出，以及通过 Python API 和轻量图形界面进行部署的完整流程。'),
    ('Demonstrator at <a href="https://www.durham.ac.uk/">Durham University</a>, 11/2021-6/2024.', '教学助理，<a href="https://www.durham.ac.uk/">杜伦大学</a>，2021 年 11 月至 2024 年 6 月。'),
    ('Led weekly lab support for Computational Thinking, Data Science, Programming for Data Science, and Text Mining modules—debugging starter code, clarifying marking rubrics, and routing stubborn tooling issues to instructors.',
     '为计算思维、数据科学、数据科学编程和文本挖掘课程提供每周实验辅导，协助代码调试、解释评分标准，并与任课教师共同处理工具使用问题。'),
    ('Student Helper at <a href="https://www.durham.ac.uk/">Durham University</a>, 08/2022-09/2022.', '学生助理，<a href="https://www.durham.ac.uk/">杜伦大学</a>，2022 年 8–9 月。'),
    ('Handled visiting speaker transport, couch bookings, and leisure tours around Durham Castle for the 21st ACM SIGGRAPH/Eurographics Symposium on Computer Animation',
     '为第 21 届 ACM SIGGRAPH/Eurographics 计算机动画研讨会协助安排嘉宾交通、大巴预订和杜伦城堡参观'),
    ('Research Assistant at <a href="https://www.northumbria.ac.uk/">Northumbria University</a>, 04/2022-07/2022.', '研究助理，<a href="https://www.northumbria.ac.uk/">诺森比亚大学</a>，2022 年 4–7 月。'),
    ('Set up multi-camera capture, collected nursing simulation footage, and led training of the automatic rating system that turned pose-estimation outputs into competency scores.',
     '搭建多摄像机采集系统，收集护理模拟训练视频，并训练基于姿态估计的自动技能评分系统。'),
    ('PI:', '项目负责人：'),
    ('<h2>Grants Involved</h2>', '<h2>科研资助</h2>'),
    ('<strong>U-care: Deep Ultraviolet Light Therapies</strong>', '<strong>U-care：深紫外光治疗</strong>'),
    ('Research Associate, EPSRC Grant:', '研究员（Research Associate），EPSRC 项目经费：'),
    ('Funded by UKRI, 2021–2026 (I joined in 2024)', 'UKRI 资助，2021–2026 年（本人于 2024 年加入）'),
    ('<strong>Course Development in Edge Computing and Analytics 2.0</strong>', '<strong>边缘计算与分析 2.0 课程开发</strong>'),
    ('Research Assistant, UK-Egypt Trans-National Education (TNE) Grant:', '研究助理，英国–埃及跨国教育（TNE）项目经费：'),
    ('Funded by the British Council, UK, 2022–2024', '英国文化教育协会资助，2022–2024 年'),
    ('<strong>Pose Estimation for Health Professional Education: Development of an Objective Computerized Approach for Measuring and Assessing Technical Competencies in Nursing</strong>',
     '<strong>面向卫生专业教育的姿态估计：开发客观的计算机方法以测量和评估护理技术能力</strong>'),
    ('Research Assistant, Northumbria University Application Seed Funding Scheme:', '研究助理，诺森比亚大学应用研究种子基金项目经费：'),
    ('Funded by Northumbria University, UK, 2022', '英国诺森比亚大学资助，2022 年'),
    ('Thanks to Yunhe Wang, who kindly shared the open-source code for the website template I used', '感谢 Yunhe Wang 分享本网站所用模板的开源代码'),
    ('Powered by', '基于'),
]


def build():
    source = SOURCE.read_text(encoding='utf-8')
    start = source.index('    <div class="publication-group">')
    end = source.index('  <p class="w3-small">* = co-first author.</p>', start)
    entries = source[start:end]
    # Only translate the headings; all citation content stays in English.
    entries = entries.replace('<div class="publication-group">', '<div class="publication-group" lang="en">')
    entries = entries.replace('<h4> Conference Papers:</h4>', '<h4 lang="zh-Hans">会议论文</h4>')
    entries = entries.replace('<h4> Journal Papers:</h4>', '<h4 lang="zh-Hans">期刊论文</h4>')
    placeholder = '<!-- PUBLICATION_ENTRIES -->'
    page = source[:start] + placeholder + source[end:]
    # Translate the full research introduction before the shared Scholar label.
    ordered = sorted(TRANSLATIONS, key=lambda pair: len(pair[0]), reverse=True)
    for english, chinese in ordered:
        pattern = r'\s+'.join(re.escape(word) for word in english.split())
        page, matches = re.subn(pattern, lambda match: chinese, page)
        if not matches:
            raise ValueError(f'Update Chinese translation for changed text: {english}')
    page = page.replace('lang="en" xml:lang="en"', 'lang="zh-Hans" xml:lang="zh-Hans"')
    page = page.replace('hreflang="en" aria-current="page">English', 'hreflang="en">English')
    page = page.replace('hreflang="zh-Hans">中文', 'hreflang="zh-Hans" aria-current="page">中文')
    page = page.replace('* = co-first author.', '* 表示共同第一作者。')
    # Localize connecting words and punctuation around the English news titles.
    for english, chinese in [
        ('</a>, <a', '</a>、<a'),
        ('</a>, and <a', '</a>，以及 <a'),
        ('</a> ——已接收。', '</a>。'),
        ('（已接收） and <a', '（已接收），以及 <a'),
        ('</a> and <a', '</a> 和 <a'),
        ('（提前接收）.', '（提前接收）。'),
        ('</strong>:', '</strong>：'),
        ('</a>.', '</a>。'),
    ]:
        page = page.replace(english, chinese)
    page = page.replace(placeholder, entries)
    page = page.replace('<!DOCTYPE html>', '<!DOCTYPE html>\n<!-- Generated by scripts/build_zh.py; edit the English source and translations. -->', 1)
    OUTPUT.write_text(page, encoding='utf-8')
    print(OUTPUT)


if __name__ == '__main__':
    build()
