# 영상(모션) 프롬프트

도구: Google Flow, Veo 3.1 Fast (20크레딧/클립, 8초 고정, 720p 생성 → 1080p 업스케일 다운로드). 설정: Frames 모드, 키프레임을 Start에만, 16:9, x1, Agent 끔.

도구 선정 과정은 [tool-selection.md](tool-selection.md).

## 공통 머리

```
Consistent 2D cel-shaded anime, keep the exact line art, colors and character design of the input image.
```

## 프롬프트 원칙 (실패에서 얻은 것)

| 원칙 | 왜 |
|---|---|
| 컷당 움직임 하나, 카메라는 고정 (`Static camera`) | 두 가지 이상 시키면 둘 다 깨짐 |
| 키프레임이 "결과 상태"면 **변화 과정을 시키지 않는다** | 12번(이미 꺼진 우주선)에 "빛이 꺼진다"를 주자 없는 빛을 지어내고 렌즈·실루엣까지 만들어냄. 상태 변화는 Start+End 두 장으로 |
| 금지어 대신 **긍정문으로 상태 서술** | `no smoke`는 `steam`으로 우회됨. `The air is perfectly clear.`가 더 잘 먹힘 |
| 모델이 아는 이름을 피한다 | `alien` → 외눈 클리셰. `rock creature`로 바꾸니 디자인 유지 |
| 외계인은 빛·틈 변화 금지, 정지 또는 몸 전체 이동만 | 밝기 변화를 시키면 폭발·번개·연기로 과장됨 |
| 발은 7·20·30·32a(걷기) 외엔 땅에 (`feet stay planted`) | 발 떼는 순간 무게중심이 깨짐 |
| `hair stays as drawn` | `hair moves slightly`가 머리카락 들썩임으로 |
| 끝에 항상 `Do not add any new objects, characters, eyes or lights.` | 작은 광원(헤드랜턴·엔진)을 서치라이트·크리스탈로 키움 |
| 밤 장면엔 `No fog, no smoke, no light beams, no haze.` | 헤드랜턴 빛을 볼륨 라이트(안개 속 빛줄기)로 해석 |
| 재시도 2~3회 안에 안 되면 **정지 컷으로 전환** | 4초 컷에 크레딧을 더 쓸 가치가 없음. 지브리식 "머무는 컷"이라 정지가 오히려 자연스러움 |

## Start+End 프레임 기법

상태가 바뀌는 컷은 앞 상태와 뒤 상태를 각각 키프레임으로 만들어 Start·End에 넣는다. 모델이 지어내는 부분이 없어 캐릭터가 안 깨진다.

- 11: 눈 청록(start) → 한쪽 연보라(end)
- 12: 우주선 켜짐(kf_09) → 꺼짐(kf_12)
- 23: 로봇 서 있음(start) → 기울어짐(end, GPT로 부분 수정해 생성)
- 24: 눈 켜짐(kf_11) → 꺼짐(kf_24)
- 32: 꺼짐(kf_24) → 연보라 켜짐(kf_32), "flickers with brief static once or twice"
- 32a: 포옹(start) → 외계인이 기댐(end) — 외계인 이동 중 형태가 녹아 실패, 두 장 정지로 대체

## 컷별 프롬프트

전체 표는 [scripts/motion_prompts.csv](../scripts/motion_prompts.csv). 최종 사용 버전 중 대표:

**30 (외계인 걷기 — 도구 테스트에 쓴 컷, 통과)**
```
Static camera. The rock alien walks slowly to the right, waddling step by step, hugging the small glowing purple engine against its chest. The purple light sways on the grass with each step. Distant village lights twinkle softly.
```

**15 (로봇 전진, 외계인 정지)**
```
Static camera. The robot rolls forward a short distance toward the rock creature and stops. The rock creature does not move or change at all — its vertical crack with two tiny dots of light stays exactly the same, constant brightness. The child stays still. Background stays exactly as in the image. No smoke, no fog, no sparks, no lightning, no light beams. Do not add any new objects, characters, eyes or lights.
```

**13 (낙하 — 0:55 싱크)**
```
Static camera. The small rock alien, already falling, drops the last short distance and lands on the grass with a soft bounce; a few grass blades puff up and settle. The pod stays dark and still. No fog, no smoke, no haze. Do not add any new objects, characters or lights.
```

**32 (Start kf_24, End kf_32)**
```
Static extreme close-up of the CRT screen. The dark screen stays black, then flickers with brief static once or twice, and two pale-purple eye lamps fade in and hold steady, ending exactly at the final frame. The screen frame does not move. Do not add anything else.
```

**32a 최종 (end 프레임 단독, 정지에 가까운 움직임)**
```
Static camera. The air is perfectly clear. Everyone stays exactly in place: the child keeps hugging the robot and only her shoulders tremble slightly, hair as drawn; the robot stays completely still with its door closed and exactly two purple eyes glowing steadily; the rock creature stays leaning against her back without moving or changing shape. No smoke, no steam, no fog. Do not add any new objects, characters, eyes or lights.
```

## 실패 기록

| 컷 | 결과 | 원인 | 처리 |
|---|---|---|---|
| 1 | 별이 유성우처럼 흐르고 풀이 폭풍처럼 뒤집힘, 꺼진 창문에 불이 켜짐 | "twinkle", "sway"를 과하게 해석 | 정지 컷으로 |
| 3 | 손이 떨어졌다 붙기를 반복 / 바닥에 김이 깔림 / 고개를 들며 얼굴이 바뀜 | "맞닿는다"를 반복 동작으로, "light breathes"를 볼륨 라이트로 | 3회 실패 후 정지 컷 |
| 9 | 실루엣이 사람 손·얼굴처럼 움직임 | 모델이 실루엣을 인간형으로 | "round lumpy blob, never changing shape, no limbs, no face" |
| 10 | 뒷걸음질 중 무게중심 붕괴, 상체 움직임도 어색 | 걸음·몸 동작 | 3회 실패 후 정지 컷 |
| 11 | 좌우 눈 색이 1초마다 교대로 바뀜 (신호등) | "flicker"를 빠른 교대로 | Start+End 두 장으로 재생성 |
| 12 | 꺼진 우주선에 빛·렌즈·사람 실루엣이 생김 | 결과 상태에 변화 과정을 지시 | Start(kf_09)+End(kf_12) |
| 15 | 외계인 틈이 외눈으로, 밝기 변화가 폭발·번개로 / 재시도에선 뒤쪽에 가스 | "alien" 클리셰, 밝기 지시 | "rock creature", 변화 금지. 가스 전 2.6초만 잘라 5초로 보간 |
| 16 | 로봇 머리가 서치라이트가 됨 | 와이드샷의 작은 광원을 키움 | 정지 컷으로 |
| 19 | 엔진이 보라 크리스탈 송곳으로, 우주선 앞면이 구멍으로 | 작은 빛나는 물체 재해석 | 정지 컷으로 (31과 짝 맞춤) |
| 22 | 아이 머리카락이 들썩임 | "hair moves slightly" | 정지 컷으로 |
| 32a | 외계인 이동 중 몸이 녹고 로봇 눈이 4개 | Start+End 사이 이동 | end 프레임 단독 정지 |
| 32b | 꺼진 우주선에 처음부터 불이 켜짐 | 밤+등불 형태 | 정지 컷으로 |

## 생성 후 처리 (`scripts/process_clips.sh`)

- Veo 워터마크 제거: `delogo=x=1852:y=1032:w=56:h=36` (1080p 기준, 전 클립 동일 위치). 베젤 위에 있는 11번은 옆 베젤을 패치로 덮음
- 오디오 제거 (Veo 효과음이 음악과 섞이지 않도록)
- 2번 720p → 1080p lanczos 업스케일
- 12번 2배속, 13번 1.5배속, 15·22번 `minterpolate`로 2.6s→5s 늘리기
- 인코딩 crf 10 (원본 7Mbps보다 높은 비트레이트)
