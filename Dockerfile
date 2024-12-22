FROM langchain/langgraph-api:3.11

ADD . /deps/panaai-student-agents

RUN pip install --upgrade pip

RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -c /api/constraints.txt -e /deps/*

ENV LANGSERVE_GRAPHS='{"human_loop_agent": "./src/human_loop_agent/graph.py:human_loop_agent"}'

WORKDIR /deps/panaai-student-agents