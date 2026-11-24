# team11-project

# hilite

형광펜으로 표시한 필기 사진을 읽기 좋게 보정하고, 노란 형광펜 부분만 모아 시험 전 복습용 이미지로 만들어 주는 파이썬 패키지입니다.

## 1. What it does

`hilite`는 노란 형광펜 표시가 있는 필기나 유인물 컬러 사진 한 장을 받아 이미지 두 장을 만듭니다.

1. **보정한 전체 문서**: 밝기와 대비를 조절해 글씨를 읽기 쉽게 만든 이미지
2. **복습용 이미지**: 형광펜으로 표시한 부분만 여백을 두고 잘라, 원본에 나온 순서대로 위에서 아래로 붙인 이미지

첫 버전은 사진 한 장과 노란색 형광펜 한 색만 지원합니다. 글자는 이미지 그대로 두며 글자 인식(OCR)은 하지 않습니다.

자세한 기획은 [docs/proposal.md](https://github.com/11-ERICA/team11-project/blob/main/docs/proposal.md)에 있습니다.

## 2. Installation

Python 3.10 이상이 필요합니다.

수업 기간에는 TestPyPI에 올려 둔 버전을 설치합니다.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ hilite==0.1.0
```

`--extra-index-url`은 Pillow 같은 의존성을 진짜 PyPI에서 받아 오게 합니다.

개발에 참여하려면 저장소를 내려받아 편집 모드로 설치합니다.

```bash
git clone https://github.com/11-ERICA/team11-project.git
cd team11-project
pip install -e .
```

## 3. Quick start

```python
from hilite import load_image, find_highlights, enhance_document, crop_regions, make_review_sheet

image = load_image("notes.jpg")            # 형광펜 표시가 있는 컬러 사진
boxes = find_highlights(image)             # [(left, top, right, bottom), ...] 위→아래 순서
clean = enhance_document(image)            # 원본과 같은 크기의 보정본
clean.save("enhanced.png")                 # 보정한 전체 문서 저장
crops = crop_regions(clean, boxes, margin=10)
make_review_sheet(crops, "review.png")     # 형광펜 부분을 모은 복습용 이미지 저장
```

## 4. Dependencies

| import 이름 | PyPI 패키지 | 라이선스 |
|---|---|---|
| `PIL` | Pillow | MIT-CMU |

이 목록은 `pyproject.toml`의 `dependencies`와 같습니다. 함수 본문을 구현하면서 새로 import하는 패키지(예: numpy)는 이 표와 `pyproject.toml`에 함께 추가합니다. 모든 의존성은 우리 프로젝트의 MIT 라이선스와 함께 배포할 수 있습니다.

## 5. Tests

테스트는 [pytest](https://docs.pytest.org/)로 작성했고 `tests/` 폴더에 있습니다. 저장소를 내려받은 뒤, 저장소 루트에서 아래 두 명령을 실행합니다.

```bash
pip install -e . pytest
pytest
```

모든 테스트가 통과하면 마지막 줄에 `N passed`가 나옵니다. 테스트용 이미지는 코드 안에서 만들고, 파일은 pytest가 만드는 임시 폴더에만 저장하므로 저장소에 새 파일이 생기지 않습니다.

함수를 새로 구현하거나 고칠 때는 같은 PR에서 `tests/test_core.py`에 테스트를 추가합니다. docstring의 Examples·Raises 항목마다 테스트를 하나씩 두는 것이 기준입니다.

PR을 올리거나 main에 push하면 GitHub Actions(`.github/workflows/tests.yml`)가 같은 테스트를 자동으로 실행하고, 결과는 PR 아래 Checks에 표시됩니다.

## 6. Documentation

함수별 설명(API 페이지)을 포함한 전체 문서는 아래 사이트에 있습니다. docstring에서 자동으로 만들어집니다.
https://11-erica.github.io/team11-project/

- 함수별 설명(API): https://11-erica.github.io/team11-project/api/

## 7. Release

TODO (later in this course)

## 8. Team

| 이름 | GitHub | 맡은 함수 |
|---|---|---|
| 뭉흐오르길우수흐자르갈 | [@Usukhjargal111](https://github.com/Usukhjargal111) | `load_image` |
| 빌구대이 | [@oblgudei-spec](https://github.com/oblgudei-spec) | `find_highlights` |
| 윤정민 | [@yj-min-i](https://github.com/yj-min-i) | `enhance_document` |
| 송지우 | [@songsongjiwoo](https://github.com/songsongjiwoo) | `crop_regions` |
| 심여진 | [@yeojin1115-eng](https://github.com/yeojin1115-eng) | `make_review_sheet` |

함께 일하는 규칙: [docs/team-rules.md](https://github.com/11-ERICA/team11-project/blob/main/docs/team-rules.md)

**AI 사용**: 초안 작성과 리뷰에 AI 도구를 사용합니다. 모든 PR의 "AI use" 칸에 어떤 도구를, 어디에, 어떻게 썼는지와 그 뒤에 직접 고친 내용을 적습니다.

## 9. License

MIT 라이선스입니다.  [LICENSE](https://github.com/11-ERICA/team11-project/blob/main/LICENSE)를 보세요.
