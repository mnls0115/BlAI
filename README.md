# 블록체인 기반 AI (AI running on blockchain)
![Example Image](images/Group%2016.png) ![Example Image](images/Group%2017.png)
<br>

## 소개
본 프로젝트는 블록체인 기반으로 구현된 AI(인공지능) 시스템을 개발하기 위한 것입니다.
AI의 실행 코드, 행동 규칙, 하이퍼파라미터 및 파라미터를 블록체인에 기록함으로써 AI의 안전성을 강화하고, 연속적인 자가 학습 능력을 부여합니다.
본 문서는 프로젝트의 구조, 설치 방법, 사용 예제 및 개발 과정 등을 상세히 설명합니다.

Introduction
This project is aimed at developing an AI (Artificial Intelligence) system implemented on a blockchain basis.
By recording the AI's execution code, behavioral rules, hyperparameters, and parameters on the blockchain, we enhance the safety of the AI and provide it with continuous self-learning capabilities.
This document elaborately explains the structure of the project, installation methods, usage examples, and the development process.
<br>

## 본 LLM 코드는 llama3 8b model 을 사용하고 있습니다! 감사합니다 Meta!
This LLM code uses the llama3 8b model! Thanks, Meta!
<br>

## 파일 탐색 시 (For File Exploration)
- /Blockchain/Backend/core/blockchain.py 파일을 보세요!<br>
- Please see the /Blockchain/Backend/core/blockchain.py file!
<br>

## 추가로 구현 필요한 부분 (need further implementation)
- 1 LLM 기능 구현 : input을 받은 후 tokenizer, model code를 통과해 output 생성
- 2 growing 구현 : 파라미터 변경사항을 어떻게 반영할건지, self evaluation 방법, 정도
- 3 Mining : mining 방식 (train iter와 nonce 배정, mining 이후 broadcasting, coin 발행 방식)
- 4 Parameter quantify 방식 : bfloat16 그대로 사용 / 1.58bit 구현<br>
<br>

- 1 Implementation of LLM functionality: Generating output through tokenizer and model code after receiving input.
- 2 Implementation of growth: How to reflect parameter changes, methods and degrees of self-evaluation.
- 3 Mining: Mining method (allocation of train iter and nonce, broadcasting after mining, coin issuance method).
Parameter quantification method: Whether to use bfloat16 as is or to implement a 1.58bit system.
System Architecture
- 4 The system is composed of various components including data loading, front-end, AI execution code, and blockchain. The diagram below shows each component and their interactions.
<br>

## 시스템 아키텍처 (System Architecture)
본 시스템은 데이터 로딩, 프론트엔드, AI 실행코드, 그리고 블록체인을 포함한 다양한 구성 요소로 이루어져 있습니다. 아래 다이어그램은 각 구성 요소와 그들 사이의 상호 작용을 보여줍니다.<br>

The system is composed of various components including data loading, front-end, AI execution code, and blockchain. The diagram below shows each component and their interactions.
<br>

### 주요 컴포넌트 (Key Components)
- **AI 실행 엔진**: AI의 핵심 실행 로직을 담당합니다. 모델 학습 및 추론을 수행하고, 새로운 데이터에 대한 예측을 제공합니다.
- **블록체인**: AI의 파라미터와 실행 규칙을 기록하고 변경 불가능한 기록을 통해 AI의 행동을 투명하게 관리합니다.
- **프론트엔드 (앱, 웹)**: 사용자 인터페이스를 담당합니다. 사용자로부터 입력을 받고 AI의 결과를 출력합니다.<br>

- **AI Execution Engine**: Responsible for the core execution logic of AI. It performs model training and inference and provides predictions for new data.
- **Blockchain**: Records and manages the AI's parameters and execution rules transparently with immutable records.
- **Frontend (App, Web)**: Handles the user interface. It receives input from users and outputs the results of the AI.
<br>

## 기술 스택 (Technology Stack)
- Python 3.8
- Flask, web service
- SQLite database
- Tensorflow/Keras for AI modeling
<br>

## 설치 가이드 (Installation Guide)
1. **저장소 클론 (Clone the Repository)**:
   ```bash
   git clone https://github.com/mnls0115/BlAI.git
   cd BlAI
<br>

## 기여 방법 (How to Contribute)
본 프로젝트는 오픈 소스이며, 커뮤니티의 기여를 환영합니다. 기여하고자 하는 개발자는 아래 절차를 따라 주시기 바랍니다:

- 이슈를 생성하여 기여할 내용을 설명합니다.
- Fork를 생성한 후, 기능을 개발합니다.
- Pull Request를 통해 코드를 제출합니다.
<br>
This project is open-source and welcomes contributions from the community. Developers who want to contribute should follow the procedure below:

- Create an issue to describe what you want to contribute.
- Create a fork, then develop the feature.
- Submit the code through a Pull Request.
<br>

## 라이선스 (License)
이 프로젝트는 MIT 라이선스 하에 배포됩니다.
This project is distributed under the MIT License.