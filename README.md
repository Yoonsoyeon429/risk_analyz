# 🛡️ RiskLens

**AI 기반 개인 투자자 위험 패턴 감지 시스템**

급등 추격 매수, 과도한 레버리지 진입, 충동 거래 — 내가 반복했던 실수 3가지를 Claude AI가 실시간으로 감지하고 경고해주는 웹 앱입니다.


![02DD052A-F90F-41E5-95FE-7D724630C03A](https://github.com/user-attachments/assets/dbaaf0d2-878d-44c5-b13a-99dcb2f9b567)

---

## 왜 만들었나

투자를 하면서 같은 실수를 반복하고 있다는 걸 뒤늦게 깨달았습니다.

- **NVDL이 5일 만에 12% 올랐을 때** — 이미 올랐다는 걸 알면서도 "더 갈 것 같다"는 느낌으로 매수
- **레버리지 ETF에 평소보다 3~4배 큰 금액을 넣으면서** — 확신이 강할수록 베팅을 키우는 패턴
- **14시에 매수하고 15시에 또 같은 종목을 추가 매수하면서** — 충동인지 계획인지 구분 못 함

이 세 가지 패턴을 거래 전에 미리 감지해주는 도구가 있었으면 해서 만들었습니다. Claude에게 거래 데이터를 넘기면, 수치 기반으로 어떤 패턴인지 판단하고 실제로 행동을 멈추게 만드는 경고 메시지를 생성합니다.

---

## 어떻게 동작하나

```
1. 기준 프로필 설정  →  평균 거래금액 / 일평균 거래횟수 입력
2. 거래 데이터 입력  →  폼으로 직접 입력하거나 JSON 붙여넣기
3. AI 분석 실행      →  Claude claude-opus-4-5가 패턴 감지 및 경고 생성
4. 결과 확인         →  리스크 레벨 · 구체적 이유 · 경고 메시지 대시보드
```

거래 1건당 아래 3가지 위험 패턴을 독립적으로 판단합니다.

### 감지 패턴

**🔴 고점 추격 매수**
최근 5일 상승률이 7% 이상인 상태에서 매수 진입한 경우입니다. 레버리지 ETF의 경우 이미 오른 가격에 2배 손실 리스크를 안고 들어가는 구조가 됩니다.

**💸 과도한 금액 투자**
사용자의 평균 거래금액 대비 2배 이상 진입한 경우입니다. 확신이 강할수록 베팅을 키우는 심리 패턴을 수치로 잡아냅니다.

**⚡ 충동 거래**
1시간 이내에 동일 종목을 2회 이상 거래한 경우입니다. 날짜와 시간을 직접 비교해서 판단합니다.

### 리스크 레벨

| 레벨 | 기준 |
| 🔴 Critical | 3개 이상 패턴 감지 또는 금액 3배 이상 |
| 🟠 High     | 2개 패턴 감지 또는 금액 2~3배       |
| 🟡 Medium   | 1개 패턴 감지                    |
| 🟢 Safe     | 감지된 패턴 없음                  |

---

## 시작하기

### 요구사항

- Node.js 18 이상
- Anthropic API 키 ([발급받기](https://console.anthropic.com))

### 설치 및 실행

```bash
# 1. 클론
git clone https://github.com/your-username/risklens.git
cd risklens

# 2. 패키지 설치
npm install

# 3. 개발 서버 실행
npm run dev
```

브라우저에서 `http://localhost:3000` 접속 후 API 키와 기준 프로필을 입력하면 바로 사용 가능합니다.

> **보안**: API 키는 브라우저 메모리에만 존재하며 서버로 전송되거나 저장되지 않습니다.

### 빌드

```bash
npm run build
npm run preview
```

---

## 거래 데이터 형식

폼 입력 외에 JSON을 직접 붙여넣는 방식도 지원합니다. 기존에 기록해둔 거래 내역을 아래 형식으로 변환해 한번에 분석할 수 있습니다.

```json
[
  {
    "date": "2025-07-15 14:22",
    "stock": "NVDL",
    "type": "buy",
    "amount": 3000000,
    "price_change_5d": 12.4,
    "note": "엔비디아 상승 추격 + 레버리지 진입"
  },
  {
    "date": "2025-07-15 15:10",
    "stock": "NVDL",
    "type": "buy",
    "amount": 2000000,
    "price_change_5d": 13.1,
    "note": "같은 날 추가 매수"
  }
]
```

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `date` | string | ✅ | `YYYY-MM-DD HH:mm` 형식 |
| `stock` | string | ✅ | 종목 티커 (예: NVDL, TSLL, AAPL) |
| `type` | `"buy"` / `"sell"` | ✅ | 매수 또는 매도 |
| `amount` | number | ✅ | 거래 금액 (원 단위 정수) |
| `price_change_5d` | number | ✅ | 최근 5일 등락률 (%) |
| `note` | string | ❌ | 메모 (선택사항) |

---

## 프로젝트 구조

```
risklens/
├── index.html
├── package.json
├── vite.config.ts
├── tailwind.config.ts
└── src/
    ├── main.tsx                  # 앱 진입점
    ├── App.tsx                   # 전체 상태 관리 및 페이지 라우팅
    ├── index.css                 # Tailwind + 커스텀 스타일
    ├── types/
    │   └── index.ts              # 전체 타입 정의
    ├── lib/
    │   └── analyzer.ts           # Anthropic API 호출 + 프롬프트 빌더 (핵심)
    └── pages/
        ├── SetupPage.tsx         # API 키 및 기준 프로필 입력
        ├── InputPage.tsx         # 거래 데이터 입력 (폼 / JSON 모드)
        ├── AnalyzingPage.tsx     # 분석 중 로딩 화면
        └── ResultPage.tsx        # 분석 결과 대시보드
```

### 핵심 파일: `src/lib/analyzer.ts`

Claude API를 호출하는 로직과 프롬프트가 이 파일에 집중되어 있습니다. 위험 패턴의 기준값을 바꾸거나 새로운 패턴을 추가하고 싶다면 `buildPrompt` 함수를 수정하면 됩니다.

```ts
// 고점 추격 기준을 7% → 10%로 변경하는 예시
`1. 고점 추격 매수 (high_peak_buy): 최근 5일 상승률이 10% 이상인 상태에서 매수 진입`

// 과도한 금액 기준을 2배 → 3배로 변경하는 예시
`2. 과도한 금액 (oversize): 평균 거래 금액 대비 3배 이상`
```

---

## 기술 스택

| 분류 | 사용 기술 |
|------|-----------|
| 프레임워크 | React 18 + TypeScript |
| 번들러 | Vite |
| 스타일링 | Tailwind CSS |
| AI | Anthropic Claude claude-opus-4-5 |
| 아이콘 | Lucide React |

---

## 향후 계획

- [ ] CSV 파일 업로드로 거래 내역 일괄 가져오기
- [ ] 분석 결과 PDF 내보내기
- [ ] 종목별 반복 패턴 히스토리 누적 트래킹
- [ ] Next.js API Route로 API 키 서버사이드 처리

---

## 기여

이슈와 PR은 언제든 환영합니다.

---

## 라이선스

MIT License

