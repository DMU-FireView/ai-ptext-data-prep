"""Source-context augmentation with length/prefix controls, never human labels.

V2 does not reuse V1 generated text. Clauses express artificial claims, not verified
product facts. Quantitative gates do not establish semantic realism or authenticity.
"""

from collections import Counter, defaultdict
import math
import random
import re

from generate_ptext_synthetic import TYPES


# Each semantic fragment is independent of product names and platform names.
# Nouns and category are matched against the real parent, not inferred from platform.
CONTEXTS = (
    ("hair", ("샴푸", "트리트먼트", "두피", "머릿결"), (
        "두피에 남는 유분을 씻어내는 세정력", "머리카락 사이까지 퍼지는 가벼운 거품",
        "헹굼 뒤 잔여감을 줄이는 마무리", "푸석한 모발을 부드럽게 감싸는 관리 방식",
        "뿌리부터 끝까지 균일하게 펴 바르는 과정", "두피를 산뜻하게 유지하는 데 맞춘 방향",
        "매일 감을 때 부담을 덜어주는 부드러운 촉감", "모발 표면을 매끈하게 정돈하는 기능",
        "물을 묻힌 뒤 충분히 거품을 내는 세정 단계", "향이 과하게 남지 않는 깔끔한 마무리",
        "엉킨 머리카락을 차분하게 풀어주는 관리", "두피와 모발을 함께 다루는 일상 관리용 설계",
    )),
    ("makeup", ("틴트", "립스틱", "립밤", "쿠션", "파운데이션", "발색", "립"), (
        "얇게 겹쳐 바를 수 있는 색 표현", "경계를 자연스럽게 풀어주는 발림성",
        "표면에 고르게 밀착되는 가벼운 제형", "건조해 보이지 않도록 정돈하는 마무리",
        "진하기를 조절하기 쉬운 덧바름", "얼굴빛을 선명하게 살리는 색감",
        "여러 톤에 두루 어울리는 부드러운 색상", "두껍지 않게 펼쳐지는 촉감",
        "덧발라도 뭉침을 줄여주는 밀착력", "휴대하며 수정하기 편한 크기",
        "입술과 피부의 결을 따라 펴지는 질감", "번짐을 줄이는 가벼운 표면 처리",
    )),
    ("skin", ("크림", "세럼", "마스크팩", "로션", "에센스", "패드", "보습", "피부"), (
        "수분을 채워주는 보습 관리", "피부결을 매끈하게 정돈하는 기능",
        "가볍게 펴 바를 수 있는 부드러운 제형", "건조한 부위를 감싸는 얇은 보호막",
        "세안 뒤 피부를 편안하게 다루는 관리 단계", "피부 표면에 고르게 퍼지는 밀착감",
        "끈적임을 줄여주는 산뜻한 마무리", "여러 번 나누어 바르기 쉬운 질감",
        "일상적인 건조함에 대응하는 수분 공급", "부담 없이 덧바르는 간편한 관리",
        "다음 단계와 이어 쓰기 편한 흡수감", "손끝으로 얇게 펴서 적용하는 방식",
    )),
    ("cleaning", ("스퀴지", "청소솔", "변기솔", "브러시", "브러쉬", "밀대", "걸레", "청소", "물기"), (
        "좁은 틈에 남은 때를 걷어내는 솔질", "젖은 바닥의 물기를 한쪽으로 모으는 기능",
        "벽과 바닥 모서리를 따라 움직이는 형태", "손에 힘을 싣기 편한 손잡이",
        "물을 뿌리고 가볍게 밀어내는 관리 방식", "세척 뒤 건조하기 쉬운 단순한 구조",
        "손이 닿기 어려운 곳을 다루는 길이", "공간을 적게 차지하는 세워두기 방식",
        "넓은 면을 빠르게 훑어내는 접촉면", "청소 뒤 도구를 씻어두기 쉬운 재질",
        "표면의 찌꺼기를 모아주는 탄탄한 끝부분", "욕실 관리의 번거로움을 줄이는 형태",
    )),
    ("lighting", ("조명", "스탠드", "무드등", "전구", "밝기"), (
        "방 안에 부드럽게 퍼지는 빛", "밤에 눈의 부담을 줄여주는 은은한 밝기",
        "책상 옆에도 놓기 편한 크기", "분위기를 바꿔주는 따뜻한 색감",
        "필요한 곳을 집중해서 비추는 방향", "복잡하지 않은 켜고 끄기 방식",
        "주변 가구와 어울리는 단정한 외형", "침실 한쪽을 아늑하게 만드는 배치",
        "빛이 직접 눈에 닿지 않게 하는 형태", "작은 공간에서도 활용하는 보조 광원",
        "이동해 두기 편한 가벼운 몸체", "생활 동선에 맞춰 두는 간편한 설치",
    )),
    ("clothing", ("티셔츠", "셔츠", "바지", "운동화", "신발", "착용", "사이즈"), (
        "움직임에 여유를 주는 편안한 형태", "피부에 닿는 부분의 부드러운 촉감",
        "일상복과 맞추기 쉬운 단정한 색상", "오래 입어도 부담을 덜어주는 무게",
        "여러 체형에 대응하는 자연스러운 실루엣", "세탁과 관리가 간단한 소재",
        "활동할 때 거슬림을 줄이는 마감", "힘이 실리는 부분을 받쳐주는 형태",
        "계절이 바뀌어도 활용하기 쉬운 두께", "다른 옷과 겹치기 편한 외형",
        "가벼운 움직임을 돕는 유연함", "필요한 부분의 압박을 줄이는 여유",
    )),
    ("home", ("수납", "선반", "의자", "책상", "커튼", "이불", "베개", "매트", "가구", "디자인"), (
        "생활 공간에 맞춰 두기 쉬운 크기", "주변과 조화를 이루는 단정한 외형",
        "자주 쓰는 물건을 정리하는 실용성", "복잡한 손질 없이 관리하는 간편함",
        "좁은 공간을 활용하는 배치 방식", "일상적인 움직임을 받쳐주는 안정감",
        "표면을 닦아내기 쉬운 매끈한 재질", "눈에 잘 띄지 않는 깔끔한 마감",
        "사용 목적에 맞게 조절하는 편의성", "어느 자리에 두어도 어울리는 차분한 색상",
        "생활 동선을 방해하지 않는 형태", "오래 두고 쓰기 좋은 기본적인 실용성",
    )),
)
FALLBACK = ("일상에 필요한 기본적인 실용성", "복잡하지 않은 관리 방식", "손이 자주 가는 간편함",
            "상황에 맞춰 활용하는 편리함", "부담스럽지 않은 크기", "단정하게 정돈한 외형",
            "쉽게 익힐 수 있는 이용 방법", "꼼꼼하게 다듬은 마감", "보관하기 쉬운 형태",
            "일상적인 관리에 대응하는 재질", "목적에 충실한 기본 기능", "불필요한 과정을 줄이는 단순함")
SCENES = ("기본 기능을 먼저 보면", "세부적인 부분에서는", "용도를 정리해 보면", "이름보다 중요한 건",
          "설명에서 눈에 띄는 건", "핵심을 짚어보자면", "이쪽에서 내세우는 건", "따져볼 대목은",
          "특징을 하나 꼽자면", "형태에 담긴 장점은", "겉으로 보이는 면 외에", "실용적인 면을 보자면",
          "전체 흐름에서 보면", "중요하게 다룰 부분은", "소개할 만한 내용은", "요점을 말하면",
          "가장 먼저 살펴볼 건", "세세한 차이를 보면", "쓰임새의 중심에는", "관심을 둘 지점은")
POSITIVES = ("가격이 부담스럽지 않은 편", "기본기가 탄탄한 편", "무난하게 두루 쓰기 좋은 물건",
             "비용에 비해 돋보이는 완성도", "군더더기를 덜어낸 실용적인 물건", "여러 기준을 고르게 채운 물건",
             "받아보는 순간부터 기대할 만한 물건", "실속을 챙기기에 충분한 품질", "소소한 일상을 편하게 만드는 물건",
             "고민할 거리를 줄여주는 물건", "요즘 눈여겨볼 만한 물건", "마감을 신경 쓴 물건",
             "기대에 부응하는 합리적인 가격대", "주변에도 알릴 만한 물건", "선물용으로도 무난한 물건",
             "처음 접하는 분도 부담 없는 물건", "다양한 용도에 잘 맞는 물건", "깔끔한 인상을 주는 물건")
INVITES = ("필요하다면 이번에 들여보세요", "궁금했다면 직접 구입해 보셔도 좋겠어요",
           "이런 걸 찾던 분들께 권할게요", "망설이던 분들은 장바구니에 담아도 됩니다",
           "살까 말까 고민 중이면 한번 사보세요", "주변에 필요하다는 사람이 있으면 알려주세요",
           "이번에는 이걸로 준비해 보세요", "관심 있던 분들께 적극 권합니다",
           "장만해 두면 후회할 일 없겠어요", "직접 골라보셔도 괜찮겠습니다",
           "다음 구매 때 눈여겨보세요", "한 번 들여놓아 보시길 바라요",
           "필요한 시점에 놓치지 마세요", "가격 괜찮을 때 챙겨두세요",
           "부담 없이 주문해 봐도 됩니다", "다른 분들에게도 권하고 싶네요",
           "찾아보던 분들은 바로 구매해도 좋아요", "이제 고민을 끝내고 써보세요",
           "한번 주문해 볼 만하다고 봐요", "이번 기회에 마련해 보시죠")
NO_USE = ("아직 직접 써본 상태는 아니지만", "실사용은 시작하지 않았는데", "개봉만 해두고 손대기 전이지만",
          "첫 사용은 다음으로 미뤘지만", "지금은 사용 전이라는 점을 밝히지만", "제 손으로 써보지는 못했지만",
          "써볼 시간이 아직 없었는데도", "택배만 받아둔 상태인데", "아직 사용해볼 기회가 없었지만",
          "테스트를 해본 적은 없지만", "실제로 써본 경험은 없는데도", "포장을 풀기 전인데도",
          "한 번도 사용하지 않았지만", "아직 손에 익힐 기회는 없었지만", "실사용 확인은 나중에 하겠지만",
          "받은 뒤 그대로 두고 있는데도", "직접 확인한 건 아직 없지만", "사용을 시작하기 전부터",
          "후기를 쓸 만큼 써보진 않았지만", "일단 써보는 건 미뤄둔 상태라서",
          "실제로 이용해보지는 않았는데도", "사용 여부부터 말하면 아직 전인데", "새것 그대로 남겨둔 상태지만",
          "바로 쓸 상황은 아니라 못 써봤지만", "실사용 시간이 전혀 없는데도", "아직 제 생활에 써보지 않았지만",
          "겉만 살펴보고 아직 사용은 안 했지만", "구입하고 한 번도 손대지 않았는데도",
          "기능을 직접 시험하기 전이지만", "현재로서는 미사용 상태지만")


def starting_key(text, size=4):
    return " ".join(re.findall(r"[가-힣a-zA-Z0-9]+", text.lower())[:size])


def context(parent):
    text = parent["content"]
    for name, anchors, fragments in CONTEXTS:
        hits = [anchor for anchor in anchors if anchor in text]
        if hits:
            return name, hits[0], fragments
    return "generic", "물건", FALLBACK


def nominal(fragment, style, rng):
    last = ord(fragment[-1])
    final_consonant = 0xAC00 <= last <= 0xD7A3 and (last - 0xAC00) % 28 != 0
    if style == "formal":
        return fragment + rng.choice(("입니다.", "이라는 점이 특징입니다." if final_consonant else "라는 점이 특징입니다."))
    if style == "casual":
        return fragment + ("이에요." if final_consonant else "예요.")
    return fragment + rng.choice((".", "!", " 정도.", "이라는 거죠." if final_consonant else "라는 거죠."))


def assertive(fragment, rng):
    has_final = (ord(fragment[-1]) - 0xAC00) % 28 != 0
    topic = "은" if has_final else "는"
    subject = "이" if has_final else "가"
    conditional = "이라면" if has_final else "라면"
    cause = "이라서" if has_final else "라서"
    return rng.choice((
        f"{fragment}, 이 부분만큼은 확실하다고 봅니다.",
        f"{fragment}만큼은 언제나 기대한 그대로일 거예요.",
        f"{fragment}에는 의심할 여지가 없어요.",
        f"{fragment}에서 부족할 일은 없을 겁니다.",
        f"{fragment}{topic} 누구에게든 똑같이 보장돼요.",
        f"{fragment}{conditional} 더 따져볼 이유가 없습니다.",
        f"{fragment}에는 반박할 부분이 없다고 생각해요.",
        f"{fragment}{subject} 필요하다면 다른 조건은 볼 필요도 없어요.",
        f"어떤 상황이라도 {fragment}{topic} 변함없습니다.",
        f"빠짐없이 충족되는 건 바로 {fragment}입니다.",
        f"{fragment}{cause} 결과가 달라질 가능성은 없겠어요.",
        f"{fragment}, 이건 틀림없다는 쪽입니다.",
    ))


def make_passage(parent, kind, rng):
    _, anchor, facts = context(parent)
    style = rng.choice(("formal", "casual", "brief"))
    ordered = list(facts)
    rng.shuffle(ordered)
    fact = ordered.pop()
    if kind == TYPES[0]:
        # Functional/target descriptions, no concrete first-person experience.
        core = [nominal(rng.choice((fact, f"{anchor}의 특징은 {fact}", f"{rng.choice(SCENES)} {fact}")), style, rng)]
        extras = [nominal(item, style, rng) for item in ordered]
    elif kind == TYPES[1]:
        core = [rng.choice(NO_USE) + " " + assertive(fact, rng), rng.choice(INVITES) + "."]
        extras = [assertive(item, rng) for item in ordered]
    elif kind in (TYPES[2], TYPES[4]):
        promotion = rng.sample(POSITIVES, len(POSITIVES))
        core = [nominal(promotion.pop(), style, rng), rng.choice(INVITES) + "."]
        extras = [nominal(item, style, rng) for item in promotion]
        # Generic praise is this type's defining property; occasional source anchor.
        if rng.random() < .5:
            extras.insert(0, nominal(f"{anchor} 쪽을 찾는 분께도 무난한 물건", style, rng))
    else:
        core = [assertive(fact, rng)]
        extras = [assertive(item, rng) for item in ordered]
    lower, upper = math.ceil(len(parent["content"]) * .70), math.floor(len(parent["content"]) * 1.30)
    target = round(len(parent["content"]) * rng.uniform(.90, 1.10))
    separator = rng.choice((" ", "\n", "\n\n"))
    clauses = list(core)
    rng.shuffle(extras)
    # Add only distinct, type-relevant semantic clauses; never character padding.
    for clause in extras:
        current = len(separator.join(clauses))
        proposed = current + len(separator) + len(clause)
        if proposed <= upper and (current < lower or abs(proposed - target) < abs(current - target)):
            clauses.append(clause)
    if kind != TYPES[1]:
        rng.shuffle(clauses)
    text = separator.join(clauses)
    return text if lower <= len(text) <= upper else None


def parent_schedule(parents, count, rng):
    """Proportional platform counts with source-length diversity, sampling with replacement."""
    by_platform = defaultdict(list)
    for parent in parents:
        by_platform[parent["platform"]].append(parent)
    platforms = sorted(by_platform)
    ideals = {p: count * len(by_platform[p]) / len(parents) for p in platforms}
    quotas = {p: int(ideals[p]) for p in platforms}
    for p in sorted(platforms, key=lambda p: (-(ideals[p] - quotas[p]), p))[:count - sum(quotas.values())]:
        quotas[p] += 1
    schedule = []
    for platform in platforms:
        pool = sorted(by_platform[platform], key=lambda p: p["source_excel_row"])
        schedule.extend(rng.choices(pool, k=quotas[platform]))
    rng.shuffle(schedule)
    return schedule


def generate_v2(parents, count=1250, seed=42):
    rng = random.Random(seed)
    # Very short seeds cannot support all three no-use/claim/recommendation parts.
    # Very long seeds are not filled with irrelevant padding. Real rows stay intact.
    eligible = [p for p in parents if p.get("review_id") is not None and 60 <= len(p["content"]) <= 600]
    if count < 0 or (count and not eligible):
        raise ValueError("synthetic 생성에는 60~600자 실제 부모 리뷰가 필요합니다.")
    if not count:
        return []
    results, used = [], {p["content"] for p in parents}
    for type_index, kind in enumerate(TYPES):
        target = count // 5 + (type_index < count % 5)
        family_count = math.ceil(target / 2) if kind == TYPES[4] else target
        # Long generic praise turns into filler. Use moderate-length parents for
        # promotion/copy; descriptive types can express more source-related facts.
        pool = [p for p in eligible if len(p["content"]) <= 300] if kind in (TYPES[2], TYPES[4]) else eligible
        schedule = parent_schedule(pool, family_count, rng)
        prefix_counts = {size: Counter() for size in (3, 4)}
        limit = max(2 if kind == TYPES[4] else 1, math.ceil(target * .04))
        made = 0
        for family_index, parent in enumerate(schedule):
            siblings = min(2, target - made) if kind == TYPES[4] else 1
            for attempt in range(2000):
                prototype = make_passage(parent, kind, rng)
                if not prototype:
                    continue
                texts = [prototype]
                if siblings == 2:
                    # Controlled lexical/ordering change of this prototype, not another review.
                    pieces = [p for p in re.split(r"(?<=[.!])\s+|\n+", prototype) if p]
                    variant = " ".join(reversed(pieces)).replace("물건", "상품").replace("부담", "부담감")
                    if variant == prototype:
                        variant = prototype.replace(".", "!", 1)
                    texts.append(variant)
                if len(set(texts)) != len(texts) or any(text in used for text in texts):
                    continue
                if any(not .7 <= len(text) / len(parent["content"]) <= 1.3 for text in texts):
                    continue
                if any(any(prefix_counts[size][key] + n > limit for key, n in Counter(starting_key(text, size) for text in texts).items()) for size in (3, 4)):
                    continue
                break
            else:
                raise ValueError(f"자연스러운 길이/시작 구문 제약으로 생성 실패: {kind}, parent row {parent['source_excel_row']}")
            for text in texts:
                used.add(text)
                for size in (3, 4):
                    prefix_counts[size][starting_key(text, size)] += 1
                results.append({
                    "platform": parent["platform"], "product_id": parent["product_id"],
                    "review_id": f"synthetic-v2-{seed}-{type_index}-{made:05d}", "content": text,
                    "label": "SUSPICIOUS", "label_origin": "synthetic", "synthetic_type": kind,
                    "parent_review_id": parent["review_id"], "parent_source_excel_row": parent["source_excel_row"],
                    "source_excel_row": None, "synthetic_family_id": f"v2-family-{seed}-{type_index}-{family_index:05d}",
                    "generation_method": "contextual_semantic_clauses_v2", "seed": seed,
                })
                made += 1
    return results
