\# Tutor Buddy: Adaptive AI Learning Agent



\## Overview

Tutor Buddy is an interactive learning assistant that adapts its teaching style to the user's expertise. Unlike standard chatbots that give generic answers, this agent changes its personality—explaining concepts simply for beginners or diving into technical optimization for experts.



I built this for the "Agents for Good" track to solve a common problem in self-study: tutorials are either too hard for new students or too slow for experienced devs.



\## Live Demo

https://tutor-buddy-app.onrender.com



\## What It Does

The application uses a multi-agent workflow to guide the user through a subject:



1\.  \*\*Syllabus Generation:\*\* You pick a subject (e.g., Python), and it generates a structured roadmap of topics.

2\.  \*\*Adaptive Teaching:\*\*

&nbsp;   \* \*\*Beginner Mode:\*\* Uses analogies and simple language (e.g., "Imagine a variable is a box").

&nbsp;   \* \*\*Expert Mode:\*\* Focuses on memory management, time complexity, and edge cases.

3\.  \*\*Active Verification:\*\* After every lesson, the "Examiner Agent" generates a unique 3-question quiz to test understanding before moving on.



\## How It Works (Architecture)

The system is built on \*\*Streamlit\*\* and uses \*\*Google Gemini 2.5 Flash\*\* for the logic. It uses a modular design where different "prompts" act as specialized agents:



\* \*\*Agent A (The Architect):\*\* Breaks down broad subjects into JSON-formatted syllabi.

\* \*\*Agent B (The Professor):\*\* Holds the logic for "Persona Switching." It checks the user's selected level in the Session State and dynamically adjusts the system prompt.

\* \*\*Agent C (The Grader):\*\* Generates quizzes in strict JSON format. It also performs "fuzzy matching" on answers, so if a user is technically correct but the string doesn't match perfectly, they still get the point.



!\[Architecture Diagram](architecture.png)



\## Tech Stack

\* \*\*Python 3.11\*\*

\* \*\*Streamlit\*\* (Frontend UI \& State Management)

\* \*\*Google Gemini API\*\* (Model: `gemini-2.5-flash`)

\* \*\*Pandas\*\* (Data display)



\## Setup \& Installation

To run this locally:



1\.  \*\*Clone the repo:\*\*

&nbsp;   ```bash

&nbsp;   git clone \[https://github.com/bhuwneshdanu/Tutor-Buddy.git](https://github.com/bhuwneshdanu/Tutor-Buddy.git)

&nbsp;   cd Tutor-Buddy

&nbsp;   ```



2\.  \*\*Install dependencies:\*\*

&nbsp;   ```bash

&nbsp;   pip install -r requirements.txt

&nbsp;   ```



3\.  \*\*Set up API Key:\*\*

&nbsp;   \* Create a `.env` file in the root folder.

&nbsp;   \* Add your key: `GOOGLE\_API\_KEY=your\_key\_here`



4\.  \*\*Run the app:\*\*

&nbsp;   ```bash

&nbsp;   streamlit run app.py

&nbsp;   ```



\## Future Improvements

\* \*\*PDF Export:\*\* Allow users to download the generated notes as a PDF.

\* \*\*Code Execution:\*\* Integrate a code sandbox so users can run Python snippets directly in the browser.

\* \*\*Voice Mode:\*\* Add Text-to-Speech for an audio tutoring experience.



---

\*Submitted for the Google AI Agents Intensive Capstone 2025.\*

