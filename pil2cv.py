# -*- coding: utf-8 -*-

import numpy as np

# 将PIL类的转为OpenCv类
def pil2cv(pil_image):
    pil_image.convert('RGB')
    cv_image = np.array(pil_image)
    cv_image = cv_image[:, :, ::-1].copy()
    return cv_image
