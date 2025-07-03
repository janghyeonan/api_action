# Python API Docker Testing with GitHub Actions

GitHub Actions를 사용하여 Docker 컨테이너에서 Python API를 테스트하는 샘플 프로젝트입니다.

## 🚀 프로젝트 개요

이 프로젝트는 다음과 같은 기능을 제공합니다:
- FastAPI 기반의 REST API 서버
- Docker 컨테이너화된 환경
- GitHub Actions를 통한 자동화된 CI/CD 파이프라인
- pytest를 사용한 API 테스트

## 📁 프로젝트 구조

```
프로젝트-루트/
├── .github/
│   └── workflows/
│       └── api-test.yml          # GitHub Actions 워크플로우
├── app/
│   └── main.py                   # FastAPI 애플리케이션
├── tests/
│   └── test_api.py               # API 테스트 케이스
├── Dockerfile                    # API 서버용 Docker 이미지
├── Dockerfile.test               # 테스트용 Docker 이미지
├── requirements.txt              # Python 의존성
├── docker-compose.yml            # Docker Compose 설정
└── README.md                     # 이 파일
```

## 🛠️ 기술 스택

- **언어**: Python 3.9
- **프레임워크**: FastAPI
- **테스트**: pytest
- **컨테이너**: Docker
- **CI/CD**: GitHub Actions

## 🔧 로컬 개발 환경 설정

### 1. 가상환경 설정 및 의존성 설치

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 가상환경 활성화 (macOS/Linux)
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
```

### 2. API 서버 실행

```bash
# 직접 실행
python app/main.py

# 또는 uvicorn 사용
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. API 테스트

```bash
# 테스트 실행
pytest tests/ -v

# 또는 직접 실행
python tests/test_api.py
```

## 🐳 Docker 사용법

### 1. Docker로 API 서버 실행

```bash
# Docker 이미지 빌드
docker build -t api-test:latest .

# 컨테이너 실행
docker run -d -p 8000:8000 --name api-container api-test:latest

# 컨테이너 정지 및 제거
docker stop api-container
docker rm api-container
```

### 2. Docker Compose 사용

```bash
# 서비스 시작 (API 서버 + 테스트)
docker-compose up --build

# 백그라운드 실행
docker-compose up -d

# 서비스 정지
docker-compose down
```

## 🧪 API 엔드포인트

### 기본 엔드포인트

- `GET /` - 루트 엔드포인트
- `GET /health` - 헬스 체크
- `GET /users/{user_id}` - 사용자 조회
- `POST /users` - 사용자 생성

### 사용 예시

```bash
# 헬스 체크
curl http://localhost:8000/health

# 사용자 조회
curl http://localhost:8000/users/123

# 사용자 생성
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com", "age": 30}'
```

## 🔄 GitHub Actions 워크플로우

코드를 `main` 또는 `develop` 브랜치에 푸시하거나 Pull Request를 생성하면 자동으로 다음 단계가 실행됩니다:

1. **코드 체크아웃**: 저장소 코드를 가져옴
2. **Docker 설정**: Docker Buildx 설정
3. **이미지 빌드**: API 서버 Docker 이미지 빌드
4. **컨테이너 실행**: API 서버 컨테이너 시작
5. **헬스 체크**: API 서버가 정상적으로 시작될 때까지 대기
6. **테스트 실행**: pytest를 사용한 API 테스트 실행
7. **정리**: 컨테이너 정지 및 제거

## 🧪 테스트 케이스

현재 구현된 테스트 케이스:

- ✅ 헬스 체크 엔드포인트 테스트
- ✅ 루트 엔드포인트 테스트
- ✅ 사용자 조회 엔드포인트 테스트
- ✅ 사용자 생성 엔드포인트 테스트
- ✅ 잘못된 사용자 ID 처리 테스트

## 📝 개발 가이드

### 새로운 엔드포인트 추가

1. `app/main.py`에 새로운 엔드포인트 추가
2. `tests/test_api.py`에 해당 테스트 케이스 추가
3. 필요한 경우 `requirements.txt`에 의존성 추가

### 환경 변수 설정

환경 변수가 필요한 경우:

```bash
# .env 파일 생성
echo "DATABASE_URL=sqlite:///./test.db" > .env
```

Docker에서 환경 변수 사용:

```dockerfile
ENV DATABASE_URL=sqlite:///./test.db
```

## 🚨 문제 해결

### 일반적인 문제들

1. **포트 충돌**: 8000 포트가 이미 사용 중인 경우
   ```bash
   # 다른 포트 사용
   docker run -p 8080:8000 api-test:latest
   ```

2. **테스트 실패**: API 서버가 완전히 시작되지 않은 경우
   ```bash
   # 더 긴 대기 시간 설정
   timeout 60 bash -c 'until curl -f http://localhost:8000/health; do sleep 2; done'
   ```

3. **Docker 권한 문제**: 
   ```bash
   # Docker 그룹에 사용자 추가
   sudo usermod -aG docker $USER
   ```

## 📄 라이센스

이 프로젝트는 MIT 라이센스하에 제공됩니다.

## 🤝 기여하기

1. 이 저장소를 포크합니다
2. 새로운 기능 브랜치를 생성합니다 (`git checkout -b feature/new-feature`)
3. 변경사항을 커밋합니다 (`git commit -am 'Add new feature'`)
4. 브랜치에 푸시합니다 (`git push origin feature/new-feature`)
5. Pull Request를 생성합니다

## 📞 문의

프로젝트에 대한 질문이나 제안사항이 있으시면 이슈를 등록해주세요.
