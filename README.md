# CV 课程作业（1）：线性滤波

Python + OpenCV 实现图像线性滤波相关内容。

## 功能

| # | 功能 | 算法 |
|---|------|------|
| 1 | 高斯金字塔 | `cv2.pyrDown()` 逐层下采样 |
| 2 | 噪声生成 | 高斯噪声 (σ=25)、椒盐噪声 (p=0.05) |
| 3 | 空间域平滑 | 均匀平滑 (均值滤波)、高斯平滑 |
| 4 | 去噪处理 | 高斯平滑去噪、中值滤波去噪 |
| 5 | 综合分析 | 3x4 子图对比展示 |

## 运行

```bash
pip install -r requirements.txt
python main.py <image_path>
```

默认使用 `test_image.png` 作为测试图像。

## 输出

| 文件 | 内容 |
|------|------|
| `output_1_pyramid.png` | 4 层高斯金字塔 |
| `output_2_noise.png` | 原始图像 + 两种噪声对比 |
| `output_3_smoothing.png` | 原始图像 + 均匀平滑 + 高斯平滑 |
| `output_4_denoising.png` | 2×3 去噪效果对比 |
| `output_5_analysis.png` | 综合分析大图 |

## 依赖

- Python 3.8+
- OpenCV (`opencv-python`)
- NumPy
- Matplotlib
