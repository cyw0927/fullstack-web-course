# Chapter 15 최종 검증·제출 체크리스트

> 기록일: 2026-10-22
>
> **범위:** 수업자료에 명시된 Book Explorer 사전 통합 실습과, 이를 응용한 Member Management 개인 프로젝트 **준비판**.
> Chapter 15 본 과제의 정확한 요구사항·공식 API·제출 지침은 아직 전달되지 않았습니다. 공식 명세를 확인하기 전까지 최종 과제 제출 완료로 표시하지 않습니다.

## 1. 현재 구현과 증거

| 항목 | 실제 완료 상태 |
| --- | --- |
| Book Explorer 검색(GET), 목록, 상세, 도서 등록 요청(POST), UI 상태 | 구현 완료 |
| Member Management 조회(GET), 검색, 상세, 회원 등록 요청(POST), UI 상태 | 학습용 준비판 구현 완료 |
| HTML / CSS / JavaScript 파일의 책임 분리 | 완료 |
| 검색/등록 submit 이벤트 리스너 중복 방지 | 코드 확인 |
| API Response 확인, DOM 표시, 빈 값·오류 경로 | 모의 응답 테스트 통과 |
| 순수 Node.js 테스트 53개 | **53/53 통과** (모의 DOM/fetch 사용) |
| 실제 Live Server + Chrome Network GET/POST | **아직 사용자 브라우저에서 미검증** |
| 실제 외부 API 서버의 응답 성공 및 Status 기록 | **미검증** |
| Chapter 15 공식 개인과제 명세 일치 여부 | **본 과제 지침 수령 전까지 미확정** |

자동 검사 재실행:

```powershell
cd C:devullstack-web-course
node practice/phase01/chapter15/tests/run-tests.cjs
```

> Node.js가 설치되어 있을 때만 실행할 수 있습니다. Live Server로 사이트를 여는 데 Node.js는 필요하지 않습니다.

## 2. Book Explorer — 실제 브라우저 검증

```text
practice/phase01/chapter15-prepractice/index.html
```

1. VS Code에서 위 HTML을 **Live Server**로 열고 F12 → **Network** 탭을 선택합니다.
2. 검색어 **javascript**를 입력하고 검색을 누릅니다.
3. **search.json** 요청에서 다음을 직접 확인합니다.
   - [ ] Request Method: **GET**
   - [ ] URL의 `q=javascript`, `limit=10`, `fields=...`
   - [ ] 실제 Status Code (값 기록: _____)
   - [ ] Response / Preview에서 `docs` 배열 확인
   - [ ] 검색 목록과 책 클릭 시 상세 보기 동작 확인
4. 제목 **Clean Code**, 저자 **Robert C. Martin**을 입력하고 **등록 요청**을 누릅니다.
5. **posts** 요청을 선택해 확인합니다.
   - [ ] Request Method: **POST**
   - [ ] Payload: `{"title":"Clean Code","author":"Robert C. Martin"}`
   - [ ] 실제 Status Code (값 기록: _____)
   - [ ] Response (예: ID 등 서버가 돌려준 데이터)
   - [ ] 성공/실패 화면 메시지 확인

**Loading 테스트:** Network → Throttling을 잠시 Slow 3G로 바꾼 뒤 검색하고, 확인 후 No throttling으로 복구합니다.

**Empty 테스트:** F12 → Console에서 아래를 직접 실행합니다. (새로고침하면 원래 상태로 되돌아갑니다.)

```javascript
books = [];
renderBooks();
```

- [ ] "검색 결과가 없습니다."가 표시됨

**Error 테스트:** Network → Throttling → **Offline**으로 전환한 뒤 검색을 실행합니다. 실패 메시지와 Console Error를 확인하고 다시 **No throttling**으로 복구합니다.

- [ ] "도서를 불러오지 못했습니다."가 표시됨
- [ ] 브라우저를 정상 네트워크 설정으로 복구함
- [ ] 예상하지 못한 Console 오류가 없음

실제 Open Library는 공개 API이고 요청 제한(429)이나 일시적 장애의 영향을 받습니다. 이런 경우 Network의 실패 응답과 내 JavaScript 오류를 구분해야 합니다.

## 3. Member Management — 실제 브라우저 검증

```text
practice/phase01/chapter15/index.html
```

1. Live Server로 실행한 뒤 F12 → Network를 열고 **회원 조회**를 누릅니다.
2. **users** 요청의 GET Method / 실제 Status Code / JSON 배열을 확인합니다.
3. 이름 또는 이메일로 검색하고 결과가 좁혀지는지 확인합니다.
4. 회원을 클릭해 ID, 이름, 사용자명, 이메일, 도시 등을 확인합니다.
5. 이름 **홍길동**, 사용자명 **hong123**, 이메일 **hong@example.com**을 입력해 등록 요청합니다.
6. POST Method, JSON Payload, 실제 Status Code, Response를 확인합니다.

체크:
- [ ] GET의 Status 값: _____
- [ ] 검색 결과·상세 화면 동작 확인
- [ ] POST의 Status 값: _____
- [ ] POST Payload의 name / username / email 확인
- [ ] 정상 등록 요청 후 성공 안내 표시
- [ ] 실제 저장 여부와 POST 성공 응답의 차이 이해
- [ ] 존재하지 않는 검색어 입력 시 Empty 안내 표시
- [ ] Offline 상태에서 검색 요청 시 Error 안내 표시
- [ ] 테스트 종료 후 네트워크 복구 및 Console 확인

학습용 회원 API 문서: https://jsonplaceholder.dev/api/users

## 4. 제출 전 마지막 확인

- [x] 기존 수업 실습 폴더를 덮어쓰지 않고 별도 경로에 작성
- [x] GET/POST, 이벤트, 데이터 처리, DOM 렌더링을 코드로 구현
- [x] 모의 응답 자동 검사 53개 통과
- [x] 검증 방법, 코드의 책임 분리, API 사용 주의사항 기록
- [ ] 실제 브라우저 실행 및 Network 스크린샷 확보
- [ ] GET/POST 실제 Status Code를 위 표에 기록
- [ ] 강의 본 과제 지침과 비교 후 필요한 수정 반영
- [ ] 강사가 요구한 제출 형식 및 폴더 경로 최종 확인

**제출용 GitHub 경로:**
- Book Explorer: https://github.com/cyw0927/fullstack-web-course/tree/main/practice/phase01/chapter15-prepractice
- Member Management 준비판: https://github.com/cyw0927/fullstack-web-course/tree/main/practice/phase01/chapter15

**주의:** 위 링크는 실제 파일이 있는 경로이고, 본 과제 평가나 실측 검증 통과를 보증하지 않습니다.
