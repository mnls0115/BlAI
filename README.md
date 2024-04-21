# 블록체인 기반 AI 시스템

## 소개
본 프로젝트는 블록체인 기반으로 구현된 AI(인공지능) 시스템을 개발하기 위한 것입니다.
AI의 실행 코드, 행동 규칙, 하이퍼파라미터 및 파라미터를 블록체인에 기록함으로써 AI의 안전성을 강화하고, 연속적인 자가 학습 능력을 부여합니다.
본 문서는 프로젝트의 구조, 설치 방법, 사용 예제 및 개발 과정 등을 상세히 설명합니다.

## 시스템 아키텍처
본 시스템은 데이터 로딩, 프론트엔드, AI 실행코드, 그리고 블록체인을 포함한 다양한 구성 요소로 이루어져 있습니다. 아래 다이어그램은 각 구성 요소와 그들 사이의 상호 작용을 보여줍니다.

### 주요 컴포넌트
- **AI 실행 엔진**: AI의 핵심 실행 로직을 담당합니다. 모델 학습 및 추론을 수행하고, 새로운 데이터에 대한 예측을 제공합니다.
- **데이터 로더**: 학습 및 예측에 사용될 데이터를 로드하는 모듈입니다. 입력 데이터는 토크나이저를 거쳐 처리됩니다.
- **프론트엔드 (앱, 웹)**: 사용자 인터페이스를 담당합니다. 사용자로부터 입력을 받고 AI의 결과를 출력합니다.
- **블록체인**: AI의 파라미터와 실행 규칙을 기록하고 검증하는 역할을 합니다. 변경 불가능한 기록을 통해 AI의 행동을 투명하게 관리합니다.

## 기술 스택
- Python 3.8
- Flask를 사용한 웹 서비스
- SQLite 데이터베이스
- Tensorflow/Keras for AI 모델링

## 설치 가이드
1. **저장소 클론**:
   ```bash
   git clone https://github.com/mnls0115/BlAI.git
   cd BlAI

## 기여 방법
본 프로젝트는 오픈 소스이며, 커뮤니티의 기여를 환영합니다. 기여하고자 하는 개발자는 아래 절차를 따라 주시기 바랍니다:

이슈를 생성하여 기여할 내용을 설명합니다.
Fork를 생성한 후, 기능을 개발합니다.
Pull Request를 통해 코드를 제출합니다.

## 라이선스
이 프로젝트는 MIT 라이선스 하에 배포됩니다.
