"""Export near-duplicate candidates for human review; never label or edit reviews."""

import argparse
import math
from pathlib import Path
import sys

from openpyxl import Workbook
from openpyxl.cell import WriteOnlyCell
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Reuse the read-only loader and blank predicate without running its CLI.
from inspect_reviews import PROJECT_ROOT, is_blank, markdown_value, read_reviews


BATCH_SIZE = 128
REVIEW_FIELDS = ["platform", "product_id", "review_id", "content"]
PAIR_COLUMNS = [
    f"{field}_{side}"
    for side in ("a", "b")
    for field in ("source_excel_row", *REVIEW_FIELDS)
] + ["similarity", "same_product", "exact_duplicate", "normalized_exact"]


def threshold_value(text):
    try:
        value = float(text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("threshold는 0보다 크고 1 이하인 숫자여야 합니다.") from exc
    if not 0 < value <= 1:
        raise argparse.ArgumentTypeError("threshold 범위 오류: 0보다 크고 1 이하여야 합니다.")
    return value


def minimum_length(text):
    try:
        value = int(text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("min-length는 1 이상의 정수여야 합니다.") from exc
    if value < 1:
        raise argparse.ArgumentTypeError("min-length 오류: 1 이상의 정수여야 합니다.")
    return value


def prepare_candidates(frame, min_length):
    positions = []
    texts = []
    excluded = {"blank": 0, "non_string": 0, "short": 0}
    for position, content in enumerate(frame["content"]):
        if is_blank(content):
            excluded["blank"] += 1
        elif not isinstance(content, str):
            excluded["non_string"] += 1
        else:
            # Whitespace cleanup exists only in this independent calculation copy.
            text = " ".join(content.split())
            if len(text) < min_length:
                excluded["short"] += 1
            else:
                positions.append(position)
                texts.append(text)
    candidates = frame.iloc[positions]
    return candidates, texts, excluded


def same_product(a, b):
    # Missing product identifiers are unknown, not evidence of different products.
    if any(is_blank(value) for value in (a[1], a[2], b[1], b[2])):
        return None
    return bool(a[1] == b[1] and a[2] == b[2])


def candidate_pairs(matrix, records, threshold, texts):
    if matrix is None:
        return
    count = len(records)
    for start in range(0, count, BATCH_SIZE):
        # At most 128 x N sparse scores are held, never an N x N dense array.
        scores = cosine_similarity(
            matrix[start:start + BATCH_SIZE], matrix, dense_output=False
        ).tocsr()
        for local_index in range(scores.shape[0]):
            a_index = start + local_index
            a = records[a_index]
            left, right = scores.indptr[local_index:local_index + 2]
            for offset in range(left, right):
                b_index = scores.indices[offset]
                # Upper triangle only: no self-pairs or reversed duplicates.
                if b_index <= a_index:
                    continue
                score = min(1.0, max(0.0, float(scores.data[offset])))
                if math.isclose(score, 1.0, rel_tol=0.0, abs_tol=1e-12):
                    score = 1.0
                if score < threshold:
                    continue
                b = records[b_index]
                if a[4] == b[4]:
                    continue  # Exact raw content equality, before any cleanup.
                normalized_exact = texts[a_index] == texts[b_index]
                yield (*a, *b, score, same_product(a, b), False, normalized_exact)
        del scores


def export_pairs(path, pairs):
    counts = {"total": 0, "same": 0, "different": 0, "unknown": 0, "normalized_exact": 0}
    bins = [0] * 21
    workbook = Workbook(write_only=True)
    sheet = workbook.create_sheet("near_duplicate_pairs")
    sheet.freeze_panes = "A2"
    sheet.append(PAIR_COLUMNS)
    try:
        for pair in pairs:
            if counts["total"] >= 1_048_575:
                raise ValueError(
                    "후보가 Excel 단일 시트 한도를 초과했습니다. "
                    "threshold 또는 min-length를 높여주세요. 결과는 저장하지 않았습니다."
                )
            cells = []
            for value in pair:
                cell = WriteOnlyCell(sheet, value=value)
                if isinstance(value, str):
                    # Formula-like source strings must remain literal text.
                    cell.data_type = "s"
                cells.append(cell)
            sheet.append(cells)
            score, same, _, normalized_exact = pair[-4:]
            counts["total"] += 1
            counts["normalized_exact"] += int(normalized_exact)
            category = "unknown" if same is None else "same" if same else "different"
            counts[category] += 1
            bucket = 20 if score == 1.0 else min(19, int(score * 100) // 5)
            bins[bucket] += 1
        workbook.save(path)
    finally:
        workbook.close()
    return counts, bins


def build_report(source, total, eligible, excluded, zero_vectors, header_row,
                 header_count, skipped, threshold, min_length, counts, bins):
    try:
        display_path = source.relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        display_path = str(source)
    lines = [
        "# Near-duplicate 후보 요약", "",
        "이 결과는 사람이 확인할 후보입니다. 유사도가 높다는 이유로 조작 리뷰, 광고 리뷰, "
        "SUSPICIOUS 또는 삭제 대상으로 자동 판단하지 않습니다.",
        "상품 간 유사 후보는 향후 REPETITION / PRODUCT_COPY 검토에 참고할 수 있지만, "
        "현재 단계에서는 패턴 라벨을 부여하지 않습니다.", "",
        f"- 입력 파일: {markdown_value(display_path)}",
        f"- Reviews 유효 header 수: {header_count}, 마지막 header: Excel {header_row}행",
        f"- 공통 컬럼이 모두 빈 행 제외: {skipped}행",
        f"- threshold: {threshold}",
        f"- min_length: {min_length}", "",
        "| 항목 | 개수 |", "| --- | ---: |",
        f"| 전체 리뷰 수 | {total} |",
        f"| 유사도 분석 대상 리뷰 수 | {eligible} |",
        f"| min_length로 제외된 리뷰 수 | {excluded['short']} |",
        f"| content 빈값으로 제외된 리뷰 수 | {excluded['blank']} |",
        f"| content가 문자열이 아니어서 제외된 리뷰 수 | {excluded['non_string']} |",
        f"| 분석 대상 중 추출 가능한 n-gram이 없는 리뷰 수 | {zero_vectors} |",
        f"| near-duplicate pair 수 | {counts['total']} |",
        f"| normalized_exact pair 수 | {counts['normalized_exact']} |",
        f"| 같은 상품 내 pair 수 | {counts['same']} |",
        f"| 서로 다른 상품 간 pair 수 | {counts['different']} |",
        f"| 상품 식별 불가 pair 수 | {counts['unknown']} |", "",
        "## Similarity 구간별 개수", "",
        "구간은 반올림 전 점수의 하한 이상·상한 미만입니다. "
        "예: 0.85~0.89는 0.85 이상 0.90 미만을 뜻합니다.", "",
        "| 구간 | pair 수 |", "| --- | ---: |",
    ]
    # Include lower bins when a custom threshold is below the default 0.85.
    for index in range(20):
        if (index + 1) * 5 / 100 > threshold or index >= 17:
            lines.append(f"| {index * 5 / 100:.2f}~{(index * 5 + 4) / 100:.2f} | {bins[index]} |")
    lines += [
        f"| 1.00 | {bins[20]} |", "",
        "## 계산 및 해석 기준", "",
        "- 공통 컬럼 11개를 모두 가진 마지막 유효 header 이후만 읽습니다.",
        "- 계산용 문자열에서만 연속 공백을 정리하고 양끝 공백을 제거합니다. 최소 길이는 이 문자열의 문자 수입니다.",
        "- 소문자화 및 한글·영문·숫자·특수문자 제거는 하지 않습니다. 원문 content와 ID 값/타입은 유지합니다.",
        "- TF-IDF: analyzer=char_wb, ngram_range=(3, 5), lowercase=False, norm=l2. cosine similarity를 사용합니다.",
        f"- {BATCH_SIZE}행씩 sparse 유사도를 계산하며 전체 dense 유사도 행렬은 만들지 않습니다.",
        "- 후보도 한 행씩 Excel에 기록하며 전체 pair 목록을 메모리에 누적하지 않습니다.",
        "- raw content가 정확히 같은 pair는 제외합니다. 공백 차이 등으로 원문이 다르면 유사도 1.00 후보도 가능합니다.",
        "- 부동소수점 오차를 고려해 1과의 차이가 1e-12 이하인 유사도는 1.00으로 처리합니다.",
        "- 각 pair는 한 번만 기록하며 자기 자신과의 비교는 제외합니다. exact_duplicate는 항상 false입니다.",
        "- normalized_exact는 원문은 다르지만 공백·줄바꿈 정리 후 동일한 리뷰를 뜻합니다. prepare_candidates의 계산용 문자열이 완전히 같을 때만 true입니다.",
        "- normalized_exact는 진단용 필드이며 후보 필터링이나 자동 라벨링에 사용하지 않습니다.",
        "- same_product는 (platform, product_id) 원본 값 비교입니다. 어느 쪽이든 키가 비면 Excel에는 빈값으로 기록하고 상품 식별 불가로 별도 집계합니다.",
        "- 식별자 타입을 통일하지 않습니다. Python 비교에서 int와 float가 같게 처리될 수 있습니다.",
        "- source_excel_row_a/b는 원본 Excel 행 번호이며 a/b 필드는 각 리뷰의 원본 값입니다.",
        "- 수식 셀은 계산하지 않고 원본 수식 문자열로 읽습니다.",
        "- 짧거나 비어 있는 content는 분석 대상에서만 제외하며 원본 행을 삭제하지 않습니다.",
        "- 보고서에는 리뷰 본문을 싣지 않습니다. 원문은 로컬 결과 Excel에서 검토합니다.", "",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="거의 유사한 리뷰의 사람 검토용 후보를 찾습니다.")
    parser.add_argument("excel_path", type=Path, help="입력 Excel 경로 (읽기 전용)")
    parser.add_argument("--threshold", type=threshold_value, default=0.85, help="0 초과 1 이하 (기본: 0.85)")
    parser.add_argument("--min-length", type=minimum_length, default=15, help="계산용 content 최소 문자 수 (기본: 15)")
    parser.add_argument("--output", type=Path, default=Path("outputs/near_duplicate_pairs.xlsx"),
                        help="후보 Excel 경로 (상대경로는 PROJECT_ROOT 기준, 절대경로 허용)")
    parser.add_argument("--report", type=Path, default=Path("reports/near_duplicate_summary.md"),
                        help="요약 보고서 경로 (상대경로는 PROJECT_ROOT 기준, 절대경로 허용)")
    args = parser.parse_args()
    source = args.excel_path.expanduser().resolve()
    output = (PROJECT_ROOT / args.output.expanduser()).resolve()
    report_path = (PROJECT_ROOT / args.report.expanduser()).resolve()
    try:
        if source in (output.resolve(), report_path.resolve()):
            raise ValueError("입력 파일과 결과 경로가 같습니다. 원본 보호를 위해 중단합니다.")
        if output == report_path:
            raise ValueError("output과 report 경로가 같습니다. 서로 다른 경로를 지정해주세요.")
        frame, header_row, header_count, skipped = read_reviews(source)
        candidates, texts, excluded = prepare_candidates(frame, args.min_length)
        matrix = None
        zero_vectors = 0
        if texts:
            # Korean spacing and inflection make word tokens brittle; character
            # n-grams capture overlapping local phrases without a morphological parser.
            vectorizer = TfidfVectorizer(
                analyzer="char_wb", ngram_range=(3, 5), lowercase=False, norm="l2"
            )
            try:
                matrix = vectorizer.fit_transform(texts)
                zero_vectors = int((matrix.getnnz(axis=1) == 0).sum())
            except ValueError as exc:
                if "empty vocabulary" not in str(exc):
                    raise
                zero_vectors = len(texts)
        records = list(candidates[REVIEW_FIELDS].itertuples(index=True, name=None))
        output.parent.mkdir(parents=True, exist_ok=True)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        counts, bins = export_pairs(output, candidate_pairs(matrix, records, args.threshold, texts))
        report = build_report(
            source, len(frame), len(candidates), excluded, zero_vectors, header_row,
            header_count, skipped, args.threshold, args.min_length, counts, bins,
        )
        report_path.write_text(report, encoding="utf-8")
        print(report)
        print(f"후보 Excel: {output}\n요약 보고서: {report_path}")
    except PermissionError as exc:
        print(f"오류: 접근 권한을 확인하고 열려 있는 결과 Excel을 닫아주세요. {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"오류: near-duplicate 후보 탐지를 완료하지 못했습니다. {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
