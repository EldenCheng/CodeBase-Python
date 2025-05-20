"""
Image comparison is particularly useful when performing image processing tasks such as exposure manipulations,
filtering, and restoration.
这几个方法看上去用来让用户查看图像不同的地方, 而不是用来为程序对比图像的
"""
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import skimage as ski

if __name__ == '__main__':
    img1_gray = ski.io.imread("Pics/desk1.JPG", as_gray=True)
    img2_gray = ski.io.imread("Pics/desk2.JPG", as_gray=True)

    # The checkerboard method alternates tiles from the first and the second images.
    # 这个画面分成一个个小方格, 然后分别把一格显示一张图片对应的位置, 旁边一格显示另一张图片的对应位置
    comp_equalized = ski.util.compare_images(img1_gray, img2_gray, method='checkerboard')

    fig = plt.figure(figsize=(8, 9))
    gs = GridSpec(3, 2)
    # chkboard = fig.add_subplot(gs[1:, :])
    # chkboard.imshow(comp_equalized, cmap='gray')
    # chkboard.set_title('Checkerboard comparison')
    # chkboard.set_axis_off()
    # fig.tight_layout()

    # The diff method computes the absolute difference between the two images.
    # 好像这个最适合平常使用, 会把不相同地方的像素保留, 相同的地方会变成黑色, 所以能造成图片不相同的地方高亮效果
    diff_rotated = ski.util.compare_images(img1_gray, img2_gray, method='diff')

    # diff = fig.add_subplot(gs[1:, :])
    # diff.imshow(diff_rotated, cmap='gray')
    # diff.set_title("Diff comparison")
    # diff.set_axis_off()
    # fig.tight_layout()

    # blend is the result of the average of the two images.
    # 约等于把两张图片叠在一起显示,
    blend_rotated = ski.util.compare_images(img1_gray, img2_gray, method='blend')

    blend = fig.add_subplot(gs[1:, :])
    blend.imshow(blend_rotated, cmap='gray')
    blend.set_title("Blend comparison")
    blend.set_axis_off()
    fig.tight_layout()

    plt.show()
