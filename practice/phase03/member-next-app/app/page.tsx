import MemberWorkspace from "../components/MemberWorkspace";

export default function HomePage() {
  return (
    <main className="admin-page">
      <header className="admin-header">
        <div className="admin-brand"><span className="admin-brand-mark" aria-hidden="true">M</span> MEMBER SPACE <span className="admin-brand-divider" /> <span className="admin-brand-sub">회원 관리</span></div>
        <div className="admin-header-content">
          <p className="admin-eyebrow">MEMBER MANAGEMENT <span>·</span> PHASE 03</p>
          <h1>회원 관리 시스템</h1>
          <p className="admin-description">회원 정보를 한곳에서 검색하고 관리하세요.</p>
        </div>
      </header>
      <MemberWorkspace />
    </main>
  );
}
