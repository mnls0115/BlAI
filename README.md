# AI running on blockchain
<br>

## Motivation for Development
Someday, Artificial General Intelligence (AGI) will be created. We may fear AGI, thinking it could be dangerous, and not able to used properly. A simple misunderstanding could lead to our ruin. We cannot simply rely on prompt learning and code restrictions to control a superintelligent AI and expect it to follow only the text snippets we provide.

I propose implementing AI on a blockchain. The initial few blocks would embed AI behavior guidelines and operational code, followed by serialized parameters required for AI operation. This model is currently designed around LLM-based AI models, but could be adapted for future, more advanced AI algorithms.
Initially, I envisioned the blockchain as the AI's "DNA", allowing for replication, continuous learning, and more.  However, I have not yet devised a suitable model for these advanced functions.

While utopian, my hope is for AI to coexist with us in the future as an independent entity - a partner with whom we can share thoughts, offer mutual support, and progress together. At the very least, my goal is to develop a framework that allows us to trust AI.
As a non-computer science major, my ideas may seem far-fetched to professionals. However, if this document inspires even a small idea, I would be grateful for any assistance.

The content below, roughly written with GPT, may not be particularly helpful.

Thank you.

## This LLM code uses the llama3 8b model! Thanks, Meta!

## Introduction
This project is aimed at developing an AI (Artificial Intelligence) system implemented on a blockchain basis.
By recording the AI's execution code, behavioral rules, hyperparameters, and parameters on the blockchain, we enhance the safety of the AI and provide it with continuous self-learning capabilities.
This document elaborately explains the structure of the project, installation methods, usage examples, and the development process.
<br>


## For File Exploration
- Please see the /Blockchain/Backend/core/blockchain.py file!
<br>

## need further implementation
- 1 Implementation of LLM functionality: Generating output through tokenizer and model code after receiving input.
- 2 Implementation of growth: How to reflect parameter changes, methods and degrees of self-evaluation.
- 3 Mining: Mining method (allocation of train iter and nonce, broadcasting after mining, coin issuance method).
Parameter quantification method: Whether to use bfloat16 as is or to implement a 1.58bit system.
System Architecture
- 4 The system is composed of various components including data loading, front-end, AI execution code, and blockchain. The diagram below shows each component and their interactions.
<br>

## System Architecture
The system is composed of various components including data loading, front-end, AI execution code, and blockchain. The diagram below shows each component and their interactions.
<br>

### Key Components
- **AI Execution Engine**: Responsible for the core execution logic of AI. It performs model training and inference and provides predictions for new data.
- **Blockchain**: Records and manages the AI's parameters and execution rules transparently with immutable records.
- **Frontend (App, Web)**: Handles the user interface. It receives input from users and outputs the results of the AI.
<br>

## Technology Stack
- Python 3.8
- Flask, web service
- SQLite database
- Tensorflow/Keras for AI modeling
<br>

## Installation Guide
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/mnls0115/BlAI.git
   cd BlAI
<br>

## How to Contribute
This project is open-source and welcomes contributions from the community. Developers who want to contribute should follow the procedure below:

- Create an issue to describe what you want to contribute.
- Create a fork, then develop the feature.
- Submit the code through a Pull Request.
<br>

## License
이 프로젝트는 MIT 라이선스 하에 배포됩니다.
This project is distributed under the MIT License.

## Additioanl considering model
![Example Image](images/Group%2019.png)