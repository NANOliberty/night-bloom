# 도구 선정

## 영상 생성: Flow(Veo 3.1) vs Kling

같은 키프레임 2장(3번 탑뷰 하이파이브, 30번 외계인 걷기)으로 두 도구를 비교했다.

| | Flow / Veo 3.1 Fast | Kling 4.0 |
|---|---|---|
| 2D 셀셰이딩 유지 | 8초 내내 외곽선·캐릭터 유지 | 유지 |
| 프롬프트 충실도 | 지시 밖 움직임을 자주 추가 (팔을 뗐다 붙임) | 시킨 것만 정확히 ("손 유지" → 풀만 흔들림) |
| 생성 시간 | 1분 안쪽 | 약 4분 (무료 대기열) |
| 길이 | 8초 고정 | 3~30초 |
| 가격 | Google AI Pro 학생 할인 월 ₩7,300, 1,000크레딧 + 일 50 (Fast 20크레딧/클립 → 월 70클립+) | Pro 첫 달 $26, 3,000크레딧 |
| 워터마크 | 우측 하단 "Veo" 작은 글자 (ffmpeg로 제거 가능) | 유료는 없음 |

Kling이 모션 제어는 더 정확했지만, 학생 할인가와 속도 차이가 커서 Flow로 갔다. Flow의 과잉 움직임은 프롬프트 원칙(변화 과정 금지, 상태 서술)으로 대부분 막았고, 안 되는 컷은 정지로 전환했다.

같이 검토했던 것: Hailuo(H3가 출시 직후라 검증 부족), Runway($15, 오디오 없음), Higgsfield(Starter $19, Kling 3.0+Seedance 포함 — 두 모델 비교 용도로는 좋았으나 Veo는 Plus부터), fal.ai API 종량제(Kling 3.0, 75클립 약 $32, 코드로 일괄 실행 가능 — 결과를 보며 재시도하는 흐름이 아니라 보류).

가장 참고가 된 글: [AI 영상 생성툴 직접 비교 — Google Flow vs Kling vs Runway, 승자는?](https://handas.tistory.com/entry/AI-영상-생성툴-직접-비교-—-Google-Flow-vs-Kling-vs-Runway-승자는)

## 이미지 생성: ChatGPT vs Gemini Nano Banana

- ChatGPT: 단순 구도·소품 시트에 안정적. "CRT television"을 저작권으로 거부해 "boxy old monitor casing"으로 우회.
- Gemini: 복합 포즈·상호작용(31번 외계인이 로봇에 엔진 끼움)에 강함. 단, 다운로드 버튼으로 고해상도 재렌더하면 첨부한 레퍼런스가 섞여 들어오는 경우가 있어 결과를 바로 저장.

## 음악: Mureka

Suno 대신 Mureka O2. 가사 없는 드림팝 인스트루멘탈, "1:40 급락 후 2:05 복귀" 구조를 프롬프트로 지정. 허밍이 남아 인스트루멘탈 리믹스로 제거. Premier 1주 체험($2) 후 해지.

곡의 RMS·드럼 에너지를 `scripts/analyze_music.py`(librosa)로 분석해 싱크 포인트를 정했다: 0:55 드럼 강타, 1:25 클라이맥스, 1:40 급락, 2:05 복귀.

## 편집: DaVinci Resolve

정지 컷은 Dynamic Zoom(Ease In and Out), 줌아웃 컷은 Swap. 전환은 핸들이 무한인 PNG끼리만 Cross Dissolve, mp4 경계는 Fade In/Out 12프레임 또는 6프레임 블랙. 13→14 사이 블랙 6프레임으로 낙하 후 한 박자. 내보내기 YouTube 1080p 프리셋, Normalize -14 LKFS.

## 비용

| 도구 | 플랜 | 비용 |
|---|---|---|
| Mureka | Premier 1주 체험 | $2 |
| Google AI Pro (Flow/Veo, Gemini) | 학생 할인 1개월 | ₩7,300 |
| ChatGPT, Claude, DaVinci Resolve | 기존 보유 / 무료 | 0 |
| **합계** | | **약 ₩10,000** |
