"""Synthetic text tests only: no review files are read or Excel outputs written."""

from pathlib import Path
import sys

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import extract_ptext_candidates as candidates


REPLACEMENT = "PRODUCT_DESCRIPTION_REPLACEMENT"
NO_USE = "NO_USE_ASSERTIVE_RECOMMENDATION"
DESCRIPTION_HN = "DESCRIPTION_HARD_NEGATIVE"
DESCRIPTION = "핵심 성분을 함유해 보습을 부여하는 크림입니다."


@pytest.fixture(autouse=True)
def forbid_excel(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("These tests must not access Excel files")
    monkeypatch.setattr(candidates, "load_workbook", forbidden)
    monkeypatch.setattr(candidates, "Workbook", forbidden)


@pytest.mark.parametrize("text", [
    DESCRIPTION,
    "칙칙한 피부톤과 잡티를 관리하면서 피부에 생기를 더하는 브라이트닝 마스크입니다.",
    "탄력 저하와 건조함을 함께 관리하고 싶은 분들을 위한 시트 마스크입니다. "
    "핵심 성분으로 순도 98% 저분자 비건 콜라겐을 담아 피부에 탄력감과 보습을 부여하는 데 좋아서 자주 구매해요",
])
def test_product_description(text):
    result = candidates.pattern_features(text, [])
    assert REPLACEMENT in result
    assert DESCRIPTION_HN not in result
    assert len(result[REPLACEMENT]) >= 3


@pytest.mark.parametrize("text", [
    "비건 제품을 샀는데 저는 마음에 들어요.",
    "추천드립니다", "꼭 사세요", "장점: 좋아요\n단점: 없어요",
    "메디힐", "체험단", "광고", "SNS에서 보고 구매했어요",
    "만족합니다", "재구매", "별점 5점", "길기만 한 후기입니다. " * 100,
])
def test_isolated_signals_do_not_trigger_new_reasons(text):
    result = candidates.pattern_features(text, [])
    assert not {REPLACEMENT, NO_USE, DESCRIPTION_HN}.intersection(result)


@pytest.mark.parametrize("experience", [
    "사용해보니 제 피부가 덜 건조했어요.",
    "2주 동안 사용했어요. 보습이 좋았어요.",
    "세탁 후 색이 빠졌어요.",
    "저는 민감한 피부라 따가웠어요.",
])
def test_description_with_strong_experience(experience):
    result = candidates.pattern_features(DESCRIPTION + " " + experience, [])
    assert DESCRIPTION_HN in result
    assert REPLACEMENT not in result
    assert any("직접 경험=" in feature for feature in result[DESCRIPTION_HN])


def test_satisfaction_alone_is_not_strong_experience():
    result = candidates.pattern_features(DESCRIPTION + " 만족합니다.", [])
    assert REPLACEMENT in result
    assert DESCRIPTION_HN not in result


@pytest.mark.parametrize("context,feature", [
    ("배송은 빨랐어요.", "구체적 배송 경험"),
    ("저는 민감성 피부입니다.", "개인 상황"),
])
def test_delivery_and_personal_context_are_not_product_use(context, feature):
    text = context + " " + DESCRIPTION
    result = candidates.pattern_features(text, [])
    assert REPLACEMENT in result
    assert DESCRIPTION_HN not in result
    # The legacy HARD_NEGATIVE still accepts these EXPERIENCE categories.
    legacy = candidates.pattern_features("추천받아서 구매했어요. " + text, [])
    assert feature in legacy["HARD_NEGATIVE"]
    assert REPLACEMENT in legacy
    assert DESCRIPTION_HN not in legacy


@pytest.mark.parametrize("experience", [
    "사용해봤습니다. 세정 후 개운했습니다.",
    "사용해보았습니다.", "써봤습니다.", "써봤어요.",
    "사용중입니다.", "사용 중입니다.",
    "꾸준히 사용중", "꾸준히 사용 중",
    "꾸준히 구매해서 사용중인 제품입니다.",
    "사용하고 있습니다.", "사용하고 있어요.",
    "지금 일주일째 사용중인데", "지금 일주일 째 사용중인데",
    "3일째 사용", "2주째 사용", "2개월째 사용",
    "첫 사용감부터 개운했습니다.", "첫 사용 후 잔여감이 없어요.",
    "사용 후에는 두피가 개운하게 마무리돼요.",
    "사용 후 두피가 답답하지 않고 개운해요.",
    "사용하고나서 고민이 사라졌어요.",
    "샴푸 후 머릿결이 뻣뻣하지 않아서 마음에 들었어요.",
])
def test_expanded_strong_experience_routes_to_description_hard_negative(experience):
    result = candidates.pattern_features(DESCRIPTION + " " + experience, [])
    assert DESCRIPTION_HN in result
    assert REPLACEMENT not in result


@pytest.mark.parametrize("weak", [
    "만족합니다", "좋아요", "추천합니다", "재구매", "유명템", "체험단",
    "광고", "메디힐", "마음에 들어요", "아직 안 써봤어요",
    "아직 안 사용해봤어요", "아직 못 써봤습니다",
])
def test_weak_or_unused_expressions_do_not_replace_strong_experience(weak):
    result = candidates.pattern_features(DESCRIPTION + " " + weak, [])
    assert REPLACEMENT in result
    assert DESCRIPTION_HN not in result


@pytest.mark.parametrize("prefix", [
    "아직 써보지는 못했지만", "아직 사용해보지 못했지만", "아직 써보지 못했어요",
    "아직 사용 전이에요", "아직 안 써봤어요", "써보진 않았어요",
    "사용해보진 않았어요", "아직 개봉 전이에요", "아직 사용은 안 해봤어요",
    "아직 먹어보지 못했어요", "아직 입어보지 못했어요", "아직 신어보지 못했어요",
])
def test_no_use_with_recommendation(prefix):
    result = candidates.pattern_features(prefix + " 추천드립니다!!", [])
    assert NO_USE in result
    assert any(feature.startswith("미사용=") for feature in result[NO_USE])
    assert any("추천" in feature for feature in result[NO_USE])


@pytest.mark.parametrize("assertion", [
    "유용할 거 같아요", "효과가 있을 것 같아요", "좋을 것 같습니다", "도움이 될 것 같아요",
])
def test_no_use_with_future_utility(assertion):
    assert NO_USE in candidates.pattern_features("아직 안 써봤어요. " + assertion, [])


@pytest.mark.parametrize("text", [
    "아직 안 써봤어요", "아직 개봉 전입니다", "써보니 편했어요. 추천드립니다!",
    "사용해보니 만족합니다. 꼭 사세요.",
])
def test_no_use_needs_both_signals(text):
    assert NO_USE not in candidates.pattern_features(text, [])


@pytest.mark.parametrize("text,reason,features", [
    ("용량: 100ml / 소재: 면 / 색상: 파랑", "PRODUCT_COPY",
     ["서로 다른 스펙 키워드 3개 이상 + 항목형 나열", "키워드=색상,소재,용량"]),
    ("장점: 편해요\n단점: 비싸요", "STRUCTURED_INFO", ["명시적 후기 항목=단점,장점"]),
    ("꼭 사세요", "PROMOTIONAL_CTA", ["꼭 사세요"]),
    ("추천받아서 구매했어요. 만족해요", "HARD_NEGATIVE", ["추천받아 구매", "만족 경험"]),
])
def test_existing_reason_evidence_is_preserved(text, reason, features):
    assert candidates.pattern_features(text, [])[reason] == features


@pytest.mark.parametrize("text", ["만족해요", "추천받아서 샀어요", "추천할 만해요"])
def test_existing_negative_cases(text):
    assert "HARD_NEGATIVE" not in candidates.pattern_features(text, [])
    assert "PROMOTIONAL_CTA" not in candidates.pattern_features(text, [])


def test_raw_repetition_and_original_content_unchanged():
    text = "이 상품은 실제로 사용해 보니 아주 편리했습니다."
    frame = pd.DataFrame({"content": [text, text, text.replace(" ", "\n"), "최고예요", "최고예요"]})
    original = frame.copy(deep=True)
    result = candidates.repetition_features(frame)
    assert set(result) == {0, 1, 2}
    assert "원문 동일 2행" in result[0]
    assert "공백·줄바꿈 정리 후 동일 3행" in result[2]
    pd.testing.assert_frame_equal(frame, original)


@pytest.mark.parametrize("content", [None, "", " \n ", 123])
def test_existing_content_exclusions(content):
    assert candidates.pattern_features(content, []) == {}
