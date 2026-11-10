export default function Home() {
  return (
    <main className="page-shell">
      <section className="welcome-card" aria-labelledby="page-title">
        <p className="eyebrow">Phase 03 · Full-stack 실습</p>
        <h1 id="page-title">회원관리 시스템</h1>
        <p className="subtitle">React + Next.js + TypeScript</p>

        <nav className="actions" aria-label="회원 관리 메뉴">
          <button className="button button-primary" type="button">
            회원 목록
          </button>
          <button className="button button-secondary" type="button">
            회원 등록
          </button>
        </nav>

        <div className="lesson-status">
          <p>
            <span className="status-label">현재 단계</span>
            <strong>01강 · 첫 화면 구성</strong>
          </p>
          <p>
            <span className="status-label">다음 단계</span>
            <strong>02강 · 회원 카드와 목록</strong>
          </p>
        </div>
      </section>
      <p className="footnote">화면만 먼저 구성했습니다. API와 데이터베이스는 다음 단계에서 연결합니다.</p>
    </main>
  );
}