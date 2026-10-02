# Phase 01 — Chapter 01

## 학습 목표

첫 HTML 문서를 직접 만들고 브라우저에서 실행하면서 웹의 가장 기본적인 요청 흐름을 확인합니다.

## 실습 파일

- `index.html`: 첫 번째 HTML 페이지
- `profile.html`: 자기소개 페이지

## 핵심 개념

### Browser

사용자가 웹 페이지를 보는 프로그램입니다. HTML, CSS, JavaScript를 받아 해석하고 화면에 표시합니다.

### Web Server

브라우저가 요청한 HTML, CSS, JavaScript, 이미지 같은 파일을 전달합니다.

### API Server

프론트엔드가 요청한 데이터를 처리하고 JSON 같은 형태로 응답합니다.

### Database

서비스에서 사용하는 데이터를 저장하고 조회합니다.

기본 흐름은 다음과 같이 이해할 수 있습니다.

```text
Browser
  ↓ HTTP Request
Web Server / API Server
  ↓
Database
  ↑
Web Server / API Server
  ↑ HTTP Response
Browser
```

## 실습 순서

1. VS Code에서 `index.html`을 연다.
2. Live Server로 실행한다.
3. 브라우저 주소가 `localhost` 또는 `127.0.0.1`인지 확인한다.
4. 브라우저 개발자 도구를 연다.
5. **Network** 탭에서 페이지를 새로고침한다.
6. `index.html` 또는 문서 요청을 선택한다.
7. Request Method가 **GET**인지 확인한다.
8. `profile.html`로 이동해 자기소개 페이지도 정상적으로 열리는지 확인한다.

## GET 요청이란?

브라우저가 서버에게 특정 리소스를 보내 달라고 요청할 때 사용하는 대표적인 HTTP 메서드입니다.

예를 들어 브라우저에서 `index.html`을 열면 브라우저는 웹 서버에 HTML 문서를 요청하고, 서버는 해당 문서를 응답으로 돌려줍니다.

## Git 기록 순서

로컬에서 작업할 때는 아래 흐름으로 기록할 수 있습니다.

```bash
git add .
git commit -m "feat: complete frontend basic chapter 01"
git push
```

## 완료 조건

- [x] `practice/phase01/chapter01/index.html` 작성
- [x] `profile.html` 작성
- [x] 이름/닉네임 작성
- [x] 현재 과정 `Frontend Basic` 작성
- [x] 배우고 싶은 것 3가지 작성
- [x] `Chapter 01 완료` 표시
- [ ] Live Server 실행 확인
- [ ] localhost 또는 127.0.0.1 접속 확인
- [ ] DevTools Network에서 HTML GET 요청 확인
- [x] GitHub 저장소에 파일 반영

## 정리

이번 장에서는 브라우저에서 보이는 웹 페이지가 단순히 파일을 더블클릭해서 나타나는 것이 아니라, 웹 서버에 HTTP 요청을 보내고 응답을 받아 렌더링하는 구조라는 점을 확인합니다. 이후 HTML/CSS/JavaScript와 API 통신을 배우기 위한 기초 단계입니다.
