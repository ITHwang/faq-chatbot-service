## to-do
- [x] poetry
- [x] ruff
- [x] typing
- [x] Concurrency and async / await
- [ ] fastapi
- [ ] inference using LlamaIndex and openai api
- [ ] integrate with streamlit
- [ ] integrate with alignai
- [ ] docker
- [ ] deploy on AWS
- [ ] git action

## poetry cheatsheet
- poetry new {project name}
- poetry init

- poetry add {package name}
    - poetry add {package name} --group(-G) {group name}
- poetry install 
    - poetry install --with, --without, --only {group name}
    - poetry install --sync # dependency synchronization
    - poetry install --extras(-E) {package name}
- poetry update
- poetry remove {package name} --group {group name}

- poetry shell
- source {path_to_venv}/bin/activate
    - poetry env info --path

- poetry exit
- poetry deactivate

- poetry show {package name}
    - poetry show --tree

## FastAPI
- [FastAPI vs Flask](https://www.turing.com/kb/fastapi-vs-flask-a-detailed-comparison)
- [Concurrency and async / await](https://fastapi.tiangolo.com/async)
- [Concurrency vs Parallelism](https://oxylabs.io/blog/concurrency-vs-parallelism)
- [Blocking vs Non-blocking vs Sync vs Async](https://developer.ibm.com/articles/l-async)

## AWS
- [Concurrency Compared: AWS Lambda, AWS App Runner, and AWS Fargate](https://nathanpeck.com/concurrency-compared-lambda-fargate-app-runner)
- [Tutorial: Building a serverless chat app with a WebSocket API, Lambda and DynamoDB](https://docs.aws.amazon.com/apigateway/latest/developerguide/websocket-api-chat-app.html)
- [How to Stand Up FastAPI on Lambda with Docker](https://jacobsolawetz.medium.com/how-to-stand-up-fastapi-on-lambda-with-docker-299609323e40)

## LlamaIndex
- Steps for building an LLM application
    1. Using LLMs
        - `from llama_index.llms import OpenAI`
        - `from llama_index.agent import OpenAIAgent`
        - By default LlamaIndex uses `gpt-3.5-turbo`
    2. Loading data from external sources
        - `from llama_index.core import SimpleDirectoryReader`
        - `from llama_index.core.node_parser import SentenceSplitter`
    3. Indexing and Embedding
        - By default LlamaIndex uses `text-embedding-ada-002`
        - `from llama_index.core import VectorStoreIndex`
    4. Storing
        - `from llama_index.core import StorageContext, load_index_from_storage`
    5. Querying
        - `from llama_index.core import get_response_synthesizer`
        - `from llama_index.core.retrievers import VectorIndexRetriever`
        - `from llama_index.core.query_engine import RetrieverQueryEngine`
        - `from llama_index.core.postprocessor import SimilarityPostprocessor`
        - [Build your own OpenAI Agent](https://docs.llamaindex.ai/en/stable/examples/agent/openai_agent)
        - [Chat Engine - OpenAI Agent Mode](https://docs.llamaindex.ai/en/stable/examples/chat_engine/chat_engine_openai)
        - [OpenAI Agent with Query Engine Tools](https://docs.llamaindex.ai/en/stable/examples/agent/openai_agent_with_query_engine)

## Other References
- [SEC Insights](https://github.com/run-llama/sec-insights)