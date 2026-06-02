"""
CV课程作业（1）：线性滤波
实现：高斯金字塔、噪声生成、均匀平滑、高斯平滑、中值滤波
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import rcParams

# 中文字体配置
rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
rcParams['axes.unicode_minus'] = False


def load_image(path, gray=True):
    """加载图像，可选转为灰度图"""
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"无法加载图像: {path}")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if gray:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return img


# ==================== 1. 高斯金字塔 ====================

def gaussian_pyramid(img, levels=4):
    """
    构建高斯金字塔
    每一层通过高斯模糊 + 下采样得到
    """
    pyramid = [img]
    current = img.copy()
    for i in range(levels - 1):
        current = cv2.pyrDown(current)
        pyramid.append(current)
    return pyramid


def show_pyramid(pyramid):
    """子图显示高斯金字塔"""
    n = len(pyramid)
    fig, axes = plt.subplots(1, n, figsize=(4 * n, 4))
    for i, (ax, img) in enumerate(zip(axes, pyramid)):
        ax.imshow(img, cmap='gray')
        ax.set_title(f'第{i}层 ({img.shape[1]}x{img.shape[0]})', fontsize=11)
        ax.axis('off')
    fig.suptitle('高斯金字塔 (Gaussian Pyramid)', fontsize=14, fontweight='bold')
    plt.tight_layout()
    return fig


# ==================== 2. 噪声生成 ====================

def add_gaussian_noise(img, mean=0, sigma=25):
    """添加高斯噪声"""
    noise = np.random.normal(mean, sigma, img.shape).astype(np.float32)
    noisy = img.astype(np.float32) + noise
    noisy = np.clip(noisy, 0, 255).astype(np.uint8)
    return noisy


def add_salt_pepper_noise(img, prob=0.05):
    """添加椒盐噪声"""
    noisy = img.copy()
    h, w = img.shape
    n_pixels = h * w

    # 盐噪声 (白色)
    n_salt = int(n_pixels * prob / 2)
    salt_coords = (np.random.randint(0, h, n_salt),
                   np.random.randint(0, w, n_salt))
    noisy[salt_coords] = 255

    # 椒噪声 (黑色)
    n_pepper = int(n_pixels * prob / 2)
    pepper_coords = (np.random.randint(0, h, n_pepper),
                     np.random.randint(0, w, n_pepper))
    noisy[pepper_coords] = 0

    return noisy


# ==================== 3. 平滑滤波 ====================

def uniform_smoothing(img, kernel_size=5):
    """均匀平滑（均值滤波）"""
    return cv2.blur(img, (kernel_size, kernel_size))


def gaussian_smoothing(img, kernel_size=5, sigma=1.0):
    """高斯平滑"""
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), sigma)


def median_filtering(img, kernel_size=5):
    """中值滤波"""
    return cv2.medianBlur(img, kernel_size)


# ==================== 结果可视化 ====================

def show_noise_results(original, gaussian_noisy, sp_noisy):
    """显示原始图像和加噪结果"""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    images = [
        (original, '原始图像'),
        (gaussian_noisy, '高斯噪声 (σ=25)'),
        (sp_noisy, '椒盐噪声 (prob=0.05)'),
    ]
    for ax, (img, title) in zip(axes, images):
        ax.imshow(img, cmap='gray')
        ax.set_title(title, fontsize=12)
        ax.axis('off')
    fig.suptitle('噪声生成对比', fontsize=14, fontweight='bold')
    plt.tight_layout()
    return fig


def show_smoothing_results(original, uniform, gaussian):
    """显示原图及平滑结果"""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    images = [
        (original, '原始图像'),
        (uniform, '均匀平滑 (5x5)'),
        (gaussian, '高斯平滑 (5x5, σ=1)'),
    ]
    for ax, (img, title) in zip(axes, images):
        ax.imshow(img, cmap='gray')
        ax.set_title(title, fontsize=12)
        ax.axis('off')
    fig.suptitle('空间域平滑滤波', fontsize=14, fontweight='bold')
    plt.tight_layout()
    return fig


def show_denoising_results(gaussian_noisy, gs_denoised, median_denoised_g,
                           sp_noisy, gs_sp_denoised, median_denoised_sp):
    """显示去噪结果对比（2行3列）"""
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    # 第一行：高斯噪声去噪
    for ax, (img, title) in zip(axes[0], [
        (gaussian_noisy, '高斯噪声图像'),
        (gs_denoised, '高斯平滑去噪 (5x5)'),
        (median_denoised_g, '中值滤波去噪 (5x5)'),
    ]):
        ax.imshow(img, cmap='gray')
        ax.set_title(title, fontsize=11)
        ax.axis('off')

    # 第二行：椒盐噪声去噪
    for ax, (img, title) in zip(axes[1], [
        (sp_noisy, '椒盐噪声图像'),
        (gs_sp_denoised, '高斯平滑去噪 (5x5)'),
        (median_denoised_sp, '中值滤波去噪 (5x5)'),
    ]):
        ax.imshow(img, cmap='gray')
        ax.set_title(title, fontsize=11)
        ax.axis('off')

    fig.suptitle('噪声去除效果对比', fontsize=14, fontweight='bold')
    plt.tight_layout()
    return fig


# ==================== 主流程 ====================

def main(image_path):
    # 加载图像
    img = load_image(image_path, gray=True)
    print(f"图像尺寸: {img.shape}")

    # ---- 1. 高斯金字塔 ----
    pyramid = gaussian_pyramid(img, levels=4)
    fig1 = show_pyramid(pyramid)
    fig1.savefig('output_1_pyramid.png', dpi=150, bbox_inches='tight')
    print("1/5 高斯金字塔完成")

    # ---- 2. 添加噪声 ----
    img_gaussian_noise = add_gaussian_noise(img, sigma=25)
    img_sp_noise = add_salt_pepper_noise(img, prob=0.05)
    fig2 = show_noise_results(img, img_gaussian_noise, img_sp_noise)
    fig2.savefig('output_2_noise.png', dpi=150, bbox_inches='tight')
    print("2/5 噪声生成完成")

    # ---- 3. 平滑滤波 ----
    img_uniform = uniform_smoothing(img, kernel_size=5)
    img_gaussian_smooth = gaussian_smoothing(img, kernel_size=5, sigma=1.0)
    fig3 = show_smoothing_results(img, img_uniform, img_gaussian_smooth)
    fig3.savefig('output_3_smoothing.png', dpi=150, bbox_inches='tight')
    print("3/5 空间域平滑完成")

    # ---- 4. 噪声图像去噪 ----
    # 高斯噪声 → 高斯平滑
    gs_on_gaussian = gaussian_smoothing(img_gaussian_noise, kernel_size=5, sigma=1.0)
    # 高斯噪声 → 中值滤波
    median_on_gaussian = median_filtering(img_gaussian_noise, kernel_size=5)
    # 椒盐噪声 → 高斯平滑
    gs_on_sp = gaussian_smoothing(img_sp_noise, kernel_size=5, sigma=1.0)
    # 椒盐噪声 → 中值滤波
    median_on_sp = median_filtering(img_sp_noise, kernel_size=5)

    fig4 = show_denoising_results(
        img_gaussian_noise, gs_on_gaussian, median_on_gaussian,
        img_sp_noise, gs_on_sp, median_on_sp
    )
    fig4.savefig('output_4_denoising.png', dpi=150, bbox_inches='tight')
    print("4/5 去噪处理完成")

    # ---- 5. 综合分析 ----
    fig5 = comprehensive_analysis(img, img_gaussian_noise, img_sp_noise,
                                  img_uniform, img_gaussian_smooth,
                                  gs_on_gaussian, median_on_gaussian,
                                  gs_on_sp, median_on_sp)
    fig5.savefig('output_5_analysis.png', dpi=150, bbox_inches='tight')
    print("5/5 综合分析完成")

    plt.show()
    print("所有结果已保存为 PNG 文件")


def comprehensive_analysis(original, gauss_noisy, sp_noisy,
                           uniform, gauss_smooth,
                           gs_on_gauss, median_on_gauss,
                           gs_on_sp, median_on_sp):
    """综合分析大图"""
    fig = plt.figure(figsize=(18, 12))

    positions = [
        (original, '原始图像', 0),
        (uniform, '均匀平滑 (5x5)', 1),
        (gauss_smooth, '高斯平滑 (5x5, σ=1)', 2),
        (gauss_noisy, '高斯噪声 (σ=25)', 4),
        (gs_on_gauss, '高斯平滑去噪', 5),
        (median_on_gauss, '中值滤波去噪', 6),
        (sp_noisy, '椒盐噪声 (p=0.05)', 8),
        (gs_on_sp, '高斯平滑去噪', 9),
        (median_on_sp, '中值滤波去噪', 10),
    ]

    for img, title, idx in positions:
        ax = fig.add_subplot(3, 4, idx + 1)
        ax.imshow(img, cmap='gray')
        ax.set_title(title, fontsize=10)
        ax.axis('off')

    # 添加行标签
    fig.text(0.02, 0.78, '平滑滤波', fontsize=12, fontweight='bold',
             va='center', rotation=90)
    fig.text(0.02, 0.50, '高斯噪声\n去噪对比', fontsize=12, fontweight='bold',
             va='center', rotation=90)
    fig.text(0.02, 0.22, '椒盐噪声\n去噪对比', fontsize=12, fontweight='bold',
             va='center', rotation=90)

    fig.suptitle('线性滤波综合分析', fontsize=16, fontweight='bold')
    plt.tight_layout(rect=[0.05, 0, 1, 0.96])
    return fig


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        # 默认：使用 OpenCV 内置示例图
        path = cv2.samples.findFile('lena.jpg')
        if path is None:
            print("请提供图像路径: python main.py <image_path>")
            print("或放置 lena.jpg 到当前目录")
            sys.exit(1)
    main(path)
