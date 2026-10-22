# RAG 특강 준비 — Upstage Solar / 서울시 조례 Q&A

> 준비일: 2026-10-22  
> 소속: `cyw0927/fullstack-web-course` / `practice/special/rag-solar`  
> 기준: 강사 「RAG 특강 실습 가이드(Solar)」  
> 상태: **강사 ZIP 다운로드·설치 자동화 스크립트 준비됨. 사용자 Windows 실행·API 호출은 미검증.**


## 중요 업데이트: 강사 Starter Kit 원본 발견 (2026-10-22)

강사 GitHub에 실제 배포 ZIP 파일이 올라온 것을 확인했습니다.

- 강사 저장소: https://github.com/GilbertMoon/policy_rag_assistant
- 원본 ZIP: https://github.com/GilbertMoon/policy_rag_assistant/blob/044f9d930c7c5b01bec07c2581a61b08b2bd136f/starter-kit-20261022T062047Z-1-001.zip
- 파일 크기: 318,392바이트 / Git blob SHA: `1ad7b50a3f261c649595249cca7836a954d32c4d`
- **주의:** 강사 저장소의 일반 소스(README)는 Gemini/MySQL 기반의 *다른 RAG 예제*입니다. 이번 Solar 강의는 루트의 `starter-kit-20261022T062047Z-1-001.zip`을 내려받아야 합니다.
- 강사 배포 ZIP 내부 파일은 이 환경에서 직접 압축 해제하지 못했으므로, 로컬 설치 스크립트가 실제 파일 목록을 검사하도록 구성했습니다.

### 강의 5번(필수 패키지 설치)까지 한 번에 준비

VS Code PowerShell에서:

```powershell
cd C:\dev\fullstack-web-course
git status
git pull --ff-only origin main
cd .\practice\special\rag-solar
.\install-lecture-starter.ps1
```

스크립트는 **강사 ZIP 다운로드 → Git SHA 검증 → `starter-kit` 폴더에 압축 해제 → 강의 필수 Python 파일 확인 → Python 가상환경 생성 → 강사 원본 `requirements.txt` 패키지 설치**를 진행합니다. 기존 `starter-kit` 폴더가 있다면 덮어쓰지 않습니다. `.downloads/`, `starter-kit/`, `.venv/`는 Git에서 제외됩니다.

PowerShell에서 스크립트 실행이 막히면 다음 명령을 사용합니다.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\install-lecture-starter.ps1
```

여기서 `Bypass`는 해당 PowerShell 프로세스에만 적용합니다. **강사 원본 코드임을 확인한 뒤에만 실행**하세요.

실행이 성공하면 마지막에 표시된 **실제 실습 위치**를 VS Code로 여세요. 이 과정은 API 키 발급이나 Solar API 호출은 하지 않습니다.

> **확인 범위:** 강사 ZIP 파일의 존재·크기·SHA는 원격에서 확인했지만, 사용자의 Windows 가상환경 생성 및 패키지 설치는 아직 직접 확인하지 못했습니다. 네 컴퓨터에서 명령을 실행한 뒤 결과를 확인해야 합니다.

## 이번 수업에서는 무엇을 하나요?

서울시 조례를 가져와 작은 조각(Chunk)으로 나누고, 관련 문장을 검색한 다음 Solar가 근거에 따라 답하도록 합니다. 마지막으로 답변의 근거를 확인하고 `POST /ask` API로 제공합니다.

```text
법제처 조례 수집 → 별표 Document Parse → Chunk → Embedding + Keyword 검색
→ Solar 답변 → Solar Decide 근거 검증 → FastAPI POST /ask → check.py
```

**RAG**는 질문을 받으면 먼저 문서에서 근거를 찾아 그 근거를 LLM에게 주고 답하는 방식입니다. **Chunk**는 검색하기 좋게 나눈 작은 문서 조각, **Embedding**은 문장의 의미를 숫자로 나타내는 기술입니다.

## 기존 GitHub와 로컬 경로

- GitHub: https://github.com/cyw0927/fullstack-web-course
- 기존 로컬 루트: `C:\dev\fullstack-web-course`
- 이 실습 폴더: `C:\dev\fullstack-web-course\practice\special\rag-solar`

이 경로는 기존 프론트엔드 Chapter를 수정하지 않기 위해 별도로 만든 것입니다.

## 1. 처음 실행하는 방법 (Windows PowerShell)

VS Code 터미널에서 다음을 **순서대로** 실행합니다.

```powershell
cd C:\dev\fullstack-web-course
git status
git pull --ff-only origin main
cd .\practice\special\rag-solar

python --version
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
.\.venv\Scripts\python.exe verify_environment.py
```

**주의:** 이미 `.env`가 있다면 `Copy-Item`은 생략하세요. 기존 값은 절대로 덮어쓰지 않습니다. `git pull` 전 `git status`에 수정 중인 파일이 있다면 먼저 확인하세요.

같은 작업을 한번에 해 주는 `setup.ps1`도 포함했습니다. PowerShell 실행 정책이 막히면 위의 수동 명령을 사용하면 됩니다. `.venv` 활성화는 필수가 아니며, 위 예시는 해당 환경의 Python을 직접 실행합니다.

## 2. 키 준비 — 사용자 본인이 해야 하는 단계

강의 가이드에 따르면 https://console.upstage.ai 에서 API Key를 발급합니다. `.env` 파일 안에 아래 형식으로 적습니다.

```dotenv
UPSTAGE_API_KEY=up_발급받은실제값
LAW_OC=test
```

- 실습용 `LAW_OC=test`는 강의자료에 제시된 초기값입니다. 대회/실사용은 법제처 OPEN API에서 개인 OC 발급이 필요할 수 있습니다.
- **실제 Upstage 키는 이 대화, 스크린샷, 소스 코드, GitHub에 올리지 마세요.** 키가 담긴 `.env`는 `.gitignore`로 제외했습니다.
- Upstage Studio(https://studio.upstage.ai)의 Agent 생성, HWP 업로드, 결제/크레딧 관련 작업은 해당 계정에서 진행해야 합니다.

## 3. 강사 Starter Kit을 받으면 어디에 두나요?

강의에서 말한 Starter Kit은 현재 업로드된 **가이드와 별개의 실제 코드**입니다. Starter Kit이 전달되면 다음 파일들을 이 폴더에 배치합니다.

```text
rag-solar/
├─ .env.example          # 이 저장소에서 준비함
├─ .gitignore            # 키와 생성물 업로드 방지
├─ requirements.txt      # 기본 패키지만 임시로 정리함
├─ setup.ps1             # Windows 설치 보조
├─ verify_environment.py # 준비 여부 확인
├─ config.py             # 아래부터 강사 제공 Starter Kit 필요
├─ fetch_ordinances.py
├─ parse_annex.py
├─ build_index.py
├─ rag.py
├─ app.py
├─ check.py
├─ demo.py
├─ sample_questions.json
├─ upstage.py
├─ samples/              # 강사 샘플 HWP/PDF
└─ README.md             # 여기 있는 안내 + 강사 원본 설명 비교
```

강사가 배포한 `requirements.txt`, `.env.example`, `README.md`가 다른 경우 **덮어쓰기 전에 비교**하세요. 특히 Python 파일, 원본 조례 데이터, 샘플 HWP/PDF는 이 준비 단계에서 임의로 만들어 채우지 않았습니다.

## 4. Starter Kit을 받은 다음 실행하는 수업 순서

강의에서 제시한 명령을 모아 뒀습니다. **아직 Starter Kit이 없으면 실행하면 안 됩니다.**

```powershell
python -X utf8 fetch_ordinances.py
python -X utf8 parse_annex.py
python -X utf8 build_index.py
python -X utf8 check.py --retrieval
python -X utf8 check.py
uvicorn app:app --host 127.0.0.1 --port 8000
```

서버를 켰다면 브라우저에서 `http://127.0.0.1:8000/health`를 확인하고, 새 터미널에서 `python -X utf8 check.py --url http://127.0.0.1:8000/ask`를 실행합니다. 강의의 예시 성능 수치는 **강사가 제시한 기준선**이며, 아직 사용자 환경에서 측정한 성과가 아닙니다.

## 5. 진행 체크리스트

- [x] 기존 GitHub 프로젝트 안에 별도 특강 폴더 마련
- [x] 기본 패키지 목록 정리 (`requirements.txt`)
- [x] 보안 파일 제외 (`.gitignore`)
- [x] `.env.example` 제공 (실제 키 없음)
- [x] Windows 설치 방법 및 준비 점검 코드 제공
- [ ] 사용자의 로컬에서 Git pull 및 Python 설치 실행
- [ ] 강사 Starter Kit 실제 소스 받기
- [ ] Upstage API Key 발급 및 `.env`에 개인적으로 입력
- [ ] Upstage Studio에서 Parse/Extract 확인
- [ ] 법제처 조례 6종 수집과 별표 Parse
- [ ] Chunk / Embedding / 검색 / RAG 검증
- [ ] FastAPI 구동 및 셀프 채점

**이 README는 비전공자 학습용 안내서입니다.** 먼저 준비 상태를 눈으로 확인하고, 실제 수업이 진행되는 순서대로 함께 따라가면 됩니다.
