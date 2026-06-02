"""
生成 CV 课程作业（1）线性滤波实验报告 PDF
"""
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib import rcParams
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.gridspec as gridspec
import numpy as np
from PIL import Image

rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
rcParams['axes.unicode_minus'] = False

OUTPUT_IMAGES = {
    'pyramid': 'output_1_pyramid.png',
    'noise': 'output_2_noise.png',
    'smoothing': 'output_3_smoothing.png',
    'denoising': 'output_4_denoising.png',
    'analysis': 'output_5_analysis.png',
}


def load_img(path):
    return np.array(Image.open(path))


def page_title(pdf, title, subtitle=None):
    """封面页"""
    fig = plt.figure(figsize=(8.27, 11.69))  # A4
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.72, title, transform=ax.transAxes, fontsize=28,
            fontweight='bold', ha='center', va='center')
    if subtitle:
        ax.text(0.5, 0.64, subtitle, transform=ax.transAxes, fontsize=16,
                ha='center', va='center', color='gray')

    ax.text(0.5, 0.42, '计算机视觉课程作业（1）', transform=ax.transAxes,
            fontsize=18, ha='center', va='center')
    ax.text(0.5, 0.34, '姓名：张旭尧    学号：__________', transform=ax.transAxes,
            fontsize=14, ha='center', va='center', color='#333')
    ax.text(0.5, 0.28, '日期：2026年6月', transform=ax.transAxes,
            fontsize=14, ha='center', va='center', color='#333')

    # 分割线
    ax.axhline(y=0.52, xmin=0.2, xmax=0.8, color='#1a5276', linewidth=1.5)
    ax.axhline(y=0.515, xmin=0.25, xmax=0.75, color='#2980b9', linewidth=0.8)

    pdf.savefig(fig)
    plt.close(fig)


def section_page(pdf, number, title):
    """章节分隔页"""
    fig = plt.figure(figsize=(8.27, 11.69))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.55, f'{number}', transform=ax.transAxes, fontsize=72,
            fontweight='bold', ha='center', va='center', color='#2980b9')
    ax.text(0.5, 0.42, title, transform=ax.transAxes, fontsize=24,
            fontweight='bold', ha='center', va='center')
    ax.axhline(y=0.48, xmin=0.35, xmax=0.65, color='#2980b9', linewidth=1.2)

    pdf.savefig(fig)
    plt.close(fig)


def content_page(pdf, title, sections):
    """
    文字内容页
    sections: list of (heading, body_text)
    """
    fig = plt.figure(figsize=(8.27, 11.69))
    ax = fig.add_axes([0.1, 0.08, 0.8, 0.86])
    ax.axis('off')

    y = 0.98
    # 页标题
    ax.text(0, y, title, transform=ax.transAxes, fontsize=18,
            fontweight='bold', va='top')
    ax.axhline(y=y - 0.04, xmin=0, xmax=1, color='#2980b9', linewidth=1.5)
    y -= 0.08

    for heading, body in sections:
        if y < 0.12:
            break
        if heading:
            ax.text(0, y, heading, transform=ax.transAxes, fontsize=14,
                    fontweight='bold', va='top', color='#1a5276')
            y -= 0.05
        for para in body.split('\n\n'):
            if not para.strip():
                continue
            ax.text(0.02, y, para.strip(), transform=ax.transAxes, fontsize=11,
                    va='top', linespacing=1.6, wrap=True)
            y -= 0.04 + 0.013 * para.count('\n')
        y -= 0.04

    pdf.savefig(fig)
    plt.close(fig)


def image_full_page(pdf, img_path, caption=None):
    """整页图片"""
    img = load_img(img_path)
    h, w = img.shape[:2]
    fig_h, fig_w = 11.69, 8.27  # A4 portrait
    aspect_img = w / h
    aspect_page = fig_w / (fig_h * 0.82)

    fig = plt.figure(figsize=(fig_w, fig_h))
    if aspect_img > aspect_page:
        ax_w = 0.85
        ax_h = 0.85 * w / w * fig_w / fig_h
    else:
        ax_h = 0.78
        ax_w = 0.78 * w / h * fig_h / fig_w
    ax = fig.add_axes([(1 - ax_w) / 2, (1 - ax_h) / 2 + 0.02, ax_w, ax_h])
    ax.imshow(img, cmap='gray' if img.ndim == 2 else None)
    ax.axis('off')
    if caption:
        fig.text(0.5, 0.04, caption, ha='center', fontsize=12, fontweight='bold')
    pdf.savefig(fig)
    plt.close(fig)


def dual_image_page(pdf, img1_path, img2_path, caption1, caption2, title=None):
    """两张图上下排列"""
    fig = plt.figure(figsize=(8.27, 11.69))
    if title:
        fig.suptitle(title, fontsize=16, fontweight='bold', y=0.98)

    for i, (path, cap) in enumerate([(img1_path, caption1), (img2_path, caption2)]):
        img = load_img(path)
        h, w = img.shape[:2]
        ax = fig.add_axes([0.08, 0.52 - i * 0.48, 0.84, 0.40])
        ax.imshow(img, cmap='gray' if img.ndim == 2 else None)
        ax.axis('off')
        ax.set_title(cap, fontsize=12, fontweight='bold', pad=5)

    pdf.savefig(fig)
    plt.close(fig)


def formula_page(pdf):
    """核心公式与原理"""
    fig = plt.figure(figsize=(8.27, 11.69))
    ax = fig.add_axes([0.1, 0.08, 0.8, 0.86])
    ax.axis('off')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    y = 0.96
    def add_text(text, size=12, bold=False, color='black', dy=-0.038):
        nonlocal y
        ax.text(0, y, text, transform=ax.transAxes, fontsize=size,
                fontweight='bold' if bold else 'normal', va='top', color=color,
                linespacing=1.5)
        y += dy

    add_text('核心算法公式与原理', size=20, bold=True, color='#1a5276')
    y -= 0.02
    ax.axhline(y=y, xmin=0, xmax=1, color='#2980b9', linewidth=1.2)
    y -= 0.04

    # 高斯金字塔
    add_text('1. 高斯金字塔', size=16, bold=True, color='#1a5276')
    add_text('每一层通过高斯平滑后下采样（隔行隔列）得到上一层：', size=12)
    add_text('  G_{k+1}(i,j) = Σ_m Σ_n w(m,n) * G_k(2i+m, 2j+n)', size=13, bold=True)
    add_text('其中 w(m,n) 为 5×5 高斯核，权重由二维高斯分布确定。\n'
             'cv2.pyrDown() 内部即实现上述操作：先高斯模糊再隔行采样，'
             '每层分辨率减半。\n'
             '金字塔共 4 层，L0=原始(1276×1702), L1=638×851, L2=319×425, L3=160×212。', size=12)
    y -= 0.02

    # 噪声模型
    add_text('2. 噪声模型', size=16, bold=True, color='#1a5276')
    add_text('高斯噪声：n(i,j) ~ N(μ=0, σ^2=25^2)，叠加后裁剪至 [0,255]\n'
             '  I_noisy(x,y) = clip( I(x,y) + n(x,y), 0, 255 )\n', size=12)
    add_text('椒盐噪声：随机选取 prob×N 个像素，一半置 255 (盐/白点)，一半置 0 (椒/黑点)\n'
             '  P(noise at pixel) = prob = 0.05', size=12)
    y -= 0.02

    # 平滑滤波
    add_text('3. 空间域平滑滤波', size=16, bold=True, color='#1a5276')
    add_text('均匀平滑 (Box Filter)：', size=13, bold=True)
    add_text('  g(x,y) = (1/K^2) * Σ_{i=-k}^{k} Σ_{j=-k}^{k} f(x+i, y+j)', size=13)
    add_text('  其中 K=5 为核大小，所有权重均为 1/K^2', size=12)
    y -= 0.01
    add_text('高斯平滑 (Gaussian Filter)：', size=13, bold=True)
    add_text('  g(x,y) = Σ_i Σ_j G(i,j,σ) * f(x+i, y+j)', size=13)
    add_text('  G(i,j,σ) = (1/2πσ^2) * exp(-(i^2+j^2) / (2σ^2))', size=13)
    add_text('  核大小 5×5，σ=1.0，中心权重最大，边缘权重递减', size=12)
    y -= 0.01
    add_text('中值滤波 (Median Filter)：', size=13, bold=True)
    add_text('  g(x,y) = median{ f(x+i, y+j) | i,j ∈ [-k,k] }', size=13)
    add_text('  取邻域像素的中位数而非均值，对椒盐噪声去噪效果优越', size=12)
    y -= 0.02

    # 评价指标
    add_text('4. 去噪评价方法（定性分析）', size=16, bold=True, color='#1a5276')
    add_text('本实验采用主观视觉评价：\n'
             '- 观察去噪后边缘是否清晰保留\n'
             '- 观察平坦区域噪声残留程度\n'
             '- 观察是否引入额外伪影或模糊\n'
             '- 对比不同滤波器对同种噪声的处理差异', size=12)

    pdf.savefig(fig)
    plt.close(fig)


def analysis_text():
    """返回各章节的分析文本"""
    return {
        'pyramid': [
            ('金字塔构建原理', (
                '高斯金字塔是图像多尺度表示的基础工具。本实验使用 cv2.pyrDown() 逐层构建 4 层金字塔。'
                '每层先经过 5×5 高斯核平滑以消除混叠，再进行隔行隔列下采样，分辨率长宽各减半。\n\n'
                '从输出结果可以看出，随着层数增加，图像逐渐变小变模糊：L0 为原始 1276×1702 分辨率，'
                'L1 降至 638×851，L2 为 319×425，L3 仅 160×212。细节信息（如发丝、衣物纹理）在高层中'
                '基本不可见，仅保留图像整体结构。金字塔在 SIFT 特征检测、图像融合等任务中有广泛应用。'
            )),
        ],
        'noise': [
            ('噪声模型分析', (
                '本实验模拟两种典型图像噪声：\n\n'
                '（1）高斯噪声 (σ=25)：由电子器件热噪声、光照不足等引起，在图像上表现为服从正态分布的'
                '随机亮度波动。σ=25 产生较明显的颗粒感，细看可见画面整体泛白雾状噪点，符合模拟传感器'
                '在低光照条件下的噪声特性。\n\n'
                '（2）椒盐噪声 (p=0.05)：模拟传输过程中的数据丢失或传感器坏点，表现为随机分布的黑白点。'
                '5% 的噪声密度已明显影响视觉质量，黑色和白色噪点随机散布，与高斯噪声的"雾状"噪点'
                '形态完全不同。\n\n'
                '两种噪声代表了不同的退化模型：高斯噪声影响每个像素（加性噪声），而椒盐噪声只影响'
                '部分像素（脉冲噪声）。对这两种噪声的去噪策略应当不同。'
            )),
        ],
        'smoothing': [
            ('平滑滤波对比', (
                '均匀平滑（5×5 Box Filter）和高斯平滑（5×5, σ=1.0）均属于线性低通滤波器：\n\n'
                '均匀平滑给邻域内 25 个像素相同权重 1/25，等价于一个矩形窗卷积。这种方式对边缘和'
                '平坦区域一视同仁，导致边缘同样被模糊——从输出图可以看到边缘明显钝化。\n\n'
                '高斯平滑按距离分配权重：中心像素权重最大，边缘像素权重递减（由 σ=1.0 控制衰减速度）。'
                '这种设计更符合人眼对中心像素更敏感的特性，因此边缘保留略优于均匀平滑。\n\n'
                '总体而言，高斯平滑在抑制噪声和保留边缘之间取得了更好的平衡，这是它比均值滤波更常用'
                '的原因。但从视觉上看，两者的模糊程度差异不大，都需要在核大小和模糊程度之间权衡。'
            )),
        ],
        'denoising': [
            ('高斯噪声去噪', (
                '对高斯噪声（第一行），两种去噪方法效果差异显著：\n\n'
                '- 高斯平滑去噪（中图）：能够有效降低噪声方差，图像整体变得干净平滑。但由于线性滤波'
                '本质上是加权平均，它在"抹平"噪声的同时也模糊了边缘和纹理细节，可以看到图像整体'
                '柔和但细节丢失。\n\n'
                '- 中值滤波去噪（右图）：对高斯噪声效果不理想，因为高斯噪声影响每个像素，取中位数'
                '并不能有效区分"噪声像素"和"正常像素"。图像仍保留较多噪声，且出现轻微块状伪影。\n\n'
                '结论：对于高斯噪声，高斯平滑优于中值滤波。'
            )),
            ('椒盐噪声去噪', (
                '对椒盐噪声（第二行），两种方法的优劣完全相反：\n\n'
                '- 高斯平滑去噪（中图）：效果很差。线性滤波将黑白噪点"涂抹"到周围区域，形成灰黑色'
                '污渍状伪影。这是因为它试图用邻域均值替代极端值（0 或 255），而邻域中混入的噪点'
                '会污染正常像素。\n\n'
                '- 中值滤波去噪（右图）：效果极好。中值滤波取邻域像素排序后的中间值，黑白噪点作为'
                '极端值总是排在两端，中位数必然是正常像素值。因此椒盐噪声被精准剔除，图像几乎恢复'
                '原状，边缘保留也非常出色。\n\n'
                '结论：对于椒盐噪声，中值滤波远优于高斯平滑。这体现了非线性滤波处理脉冲噪声的优势。'
            )),
        ],
        'summary': [
            ('实验总结', (
                '本实验通过实现高斯金字塔、噪声生成、空间域平滑滤波和去噪处理，系统对比了不同线性'
                '滤波和非线性滤波算法的特性与适用场景。\n\n'
                '核心发现：\n'
                '1. 高斯金字塔通过反复平滑+下采样实现多尺度表示，每层分辨率减半，信息量递减。\n'
                '2. 高斯噪声和椒盐噪声是两种完全不同的退化模型，需要不同的去噪策略。\n'
                '3. 线性滤波器（均匀平滑、高斯平滑）对高斯噪声有效，但对椒盐噪声无效甚至有害。\n'
                '4. 非线性滤波（中值滤波）对脉冲噪声（椒盐）有卓越的去噪效果，能精准剔除极端值\n'
                '   而不模糊图像。\n'
                '5. 所有空间域滤波都面临"噪声抑制 vs 边缘保留"的根本性折衷——更大的核去噪更好\n'
                '   但模糊更多，这是图像处理中普遍存在的 trade-off。\n\n'
                '实验环境：Python 3 + OpenCV 4.8 + NumPy + Matplotlib，测试图像为 1276×1702 真实照片。'
            )),
        ],
    }


def build_report():
    pdf = PdfPages('CV_作业1_线性滤波_实验报告.pdf')

    # 封面
    page_title(pdf, '线性滤波实验报告',
               '高斯金字塔 · 噪声生成 · 平滑滤波 · 去噪处理')

    # === 一、实验概述 ===
    section_page(pdf, '一', '实验概述')

    content_page(pdf, '实验目的与内容', [
        ('实验目的', (
            '1. 理解图像金字塔的多尺度表示原理，掌握高斯金字塔的构建方法。\n'
            '2. 理解常见图像噪声的数学模型，掌握高斯噪声和椒盐噪声的生成方法。\n'
            '3. 掌握空间域线性平滑滤波（均匀平滑、高斯平滑）的实现与对比。\n'
            '4. 掌握中值滤波去噪原理，对比线性和非线性方法对不同噪声的去噪效果。\n'
            '5. 培养图像处理实验的分析与报告撰写能力。'
        )),
        ('实验内容', (
            '本实验使用 Python + OpenCV 实现以下五个模块：\n'
            '（1）高斯金字塔：使用 cv2.pyrDown() 构建 4 层金字塔并显示。\n'
            '（2）噪声生成：生成高斯噪声图像 (σ=25) 和椒盐噪声图像 (prob=0.05)。\n'
            '（3）空间域平滑：对原始图像分别应用均匀平滑和高斯平滑 (5×5 核)。\n'
            '（4）去噪处理：分别用高斯平滑和中值滤波对两种噪声图像去噪，对比分析。\n'
            '（5）综合分析：将上述结果汇总为 3×4 综合对比大图。'
        )),
    ])

    # 核心公式
    formula_page(pdf)

    # === 二、高斯金字塔 ===
    section_page(pdf, '二', '高斯金字塔')

    image_full_page(pdf, OUTPUT_IMAGES['pyramid'],
                    caption='图1  高斯金字塔（4层，逐层下采样）')

    texts = analysis_text()
    content_page(pdf, '结果分析', texts['pyramid'])

    # === 三、噪声生成 ===
    section_page(pdf, '三', '噪声生成')

    image_full_page(pdf, OUTPUT_IMAGES['noise'],
                    caption='图2  原始图像与两种噪声对比（高斯噪声 σ=25，椒盐噪声 prob=0.05）')

    content_page(pdf, '结果分析', texts['noise'])

    # === 四、空间域平滑 ===
    section_page(pdf, '四', '空间域平滑滤波')

    image_full_page(pdf, OUTPUT_IMAGES['smoothing'],
                    caption='图3  原始图像与均匀平滑、高斯平滑对比（5×5 核）')

    content_page(pdf, '结果分析', texts['smoothing'])

    # === 五、去噪处理 ===
    section_page(pdf, '五', '去噪处理')

    image_full_page(pdf, OUTPUT_IMAGES['denoising'],
                    caption='图4  去噪效果对比（上：高斯噪声去噪，下：椒盐噪声去噪）')

    content_page(pdf, '高斯噪声去噪分析', texts['denoising'][:1])
    content_page(pdf, '椒盐噪声去噪分析', texts['denoising'][1:])

    # === 六、综合分析 ===
    section_page(pdf, '六', '综合分析')

    image_full_page(pdf, OUTPUT_IMAGES['analysis'],
                    caption='图5  线性滤波综合分析（3×4 子图）')

    # === 七、总结 ===
    section_page(pdf, '七', '实验总结')

    content_page(pdf, '总结与展望', texts['summary'])

    # === 附录：代码结构 ===
    section_page(pdf, '附录', '核心代码结构')

    content_page(pdf, '代码架构说明', [
        ('模块划分', (
            'load_image(path, gray=True)      — 图像加载与灰度转换\n'
            'gaussian_pyramid(img, levels=4)   — 高斯金字塔构建\n'
            'add_gaussian_noise(img, σ=25)     — 高斯噪声生成\n'
            'add_salt_pepper_noise(img, p=0.05)— 椒盐噪声生成\n'
            'uniform_smoothing(img, ksize=5)   — 均匀平滑（cv2.blur）\n'
            'gaussian_smoothing(img, ksize=5)  — 高斯平滑（cv2.GaussianBlur）\n'
            'median_filtering(img, ksize=5)    — 中值滤波（cv2.medianBlur）\n'
            'comprehensive_analysis(...)        — 3×4 综合分析大图'
        )),
        ('关键参数', (
            '- 高斯金字塔层数：4 层\n'
            '- 高斯噪声标准差 σ = 25\n'
            '- 椒盐噪声密度 prob = 0.05\n'
            '- 平滑滤波核大小：5×5\n'
            '- 高斯平滑 σ = 1.0\n'
            '- 中值滤波核大小：5×5\n'
            '- 测试图像：真实照片 1276×1702\n'
            '- 所有输出图像保存为 150 DPI PNG 格式'
        )),
        ('依赖库', (
            '- OpenCV (opencv-python>=4.8.0) — 图像处理核心\n'
            '- NumPy (>=1.24.0) — 数值运算与噪声生成\n'
            '- Matplotlib (>=3.7.0) — 可视化与图表绘制\n'
            '- Python 3.8+ 运行环境'
        )),
    ])

    pdf.close()
    print('报告已生成: CV_作业1_线性滤波_实验报告.pdf')


if __name__ == '__main__':
    build_report()
