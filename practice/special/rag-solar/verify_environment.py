"""RAG 특강 준비물 확인: Python, 라이브러리, .env, 강의 Starter Kit 여부.

외부 API를 호출하거나 API 키를 출력하지 않습니다.
"""
from importlib.util import find_spec
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
PACKAGES = ["openai", "requests", "numpy", "fastapi", "uvicorn", "dotenv"]
STARTER_FILES = [
    "config.py", "fetch_ordinances.py", "parse_annex.py", "build_index.py",
    "rag.py", "app.py", "check.py", "demo.py",
    "sample_questions.json", "upstage.py",
]


def show(condition: bool, label: str) -> None:
    mark = "[OK]" if condition else "[  ]"
    print(f"{mark} {label}")


def main() -> None:
    print("=== RAG 특강 준비 점검 ===")
    print("Python:", sys.version.split()[0])
    print("프로젝트:", ROOT)
    print("\n[필수 패키지]")
    for package in PACKAGES:
        show(find_spec(package) is not None, package)

    print("\n[환경 변수]")
    env_path = ROOT / ".env"
    show(env_path.is_file(), ".env 파일 존재 (API 키 내용은 표시하지 않음)")
    show((ROOT / ".env.example").is_file(), ".env.example 템플릿 존재")

    print("\n[강사 제공 Starter Kit — 별도 배포본을 넣어야 함]")
    for filename in STARTER_FILES:
        show((ROOT / filename).is_file(), filename)
    sample_folder = ROOT / "samples"
    show(sample_folder.exists() and any(sample_folder.iterdir()), "samples/ 문서 파일")

    print("\n주의: [  ]로 표시된 Starter Kit 파일은 제공되지 않았다면 정상입니다.")
    print("이 점검은 네트워크/API 호출이나 조례 수집을 실행하지 않습니다.")


if __name__ == "__main__":
    main()
