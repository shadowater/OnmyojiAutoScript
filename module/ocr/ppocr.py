import numpy as np
from paddleocr import PaddleOCR
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class BoxedResult:
    box: np.ndarray
    ocr_text: str
    score: float


class TextSystem:
    def __init__(
            self,
            use_angle_cls=False,
            box_thresh=0.6,
            unclip_ratio=1.6,
            rec_model_path=None,
            det_model_path=None,
            ort_providers=None
    ):
        self.ocr = PaddleOCR(
            use_angle_cls=use_angle_cls,
            det_db_box_thresh=box_thresh,
            det_db_unclip_ratio=unclip_ratio,
            lang='ch',
            show_log=False,
            use_gpu=False
        )
        self.box_thresh = box_thresh
        self.unclip_ratio = unclip_ratio

    def ocr_single_line(self, img: np.ndarray) -> Tuple[str, float]:
        result = self.ocr.ocr(img, cls=use_angle_cls if hasattr(self, 'use_angle_cls') else False)
        if result is None or len(result) == 0 or result[0] is None:
            return "", 0.0

        texts = []
        scores = []
        for line in result[0]:
            if line is None:
                continue
            text = line[1][0]
            score = line[1][1]
            texts.append(text)
            scores.append(score)

        if not texts:
            return "", 0.0

        combined_text = "".join(texts)
        avg_score = sum(scores) / len(scores) if scores else 0.0
        return combined_text, avg_score

    def detect_and_ocr(self, img: np.ndarray, **kwargs) -> List[BoxedResult]:
        result = self.ocr.ocr(img, cls=False)
        if result is None or len(result) == 0 or result[0] is None:
            return []

        boxed_results = []
        for line in result[0]:
            if line is None:
                continue
            box = np.array(line[0])
            text = line[1][0]
            score = line[1][1]
            boxed_results.append(BoxedResult(box=box, ocr_text=text, score=score))

        return boxed_results
