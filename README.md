## to-do
- [x] poetry
- [x] ruff
- [x] typing
- [x] Concurrency and async / await
- [ ] fastapi
- [ ] inference using semantic kernel and openai api
- [ ] integrate with streamlit
- [ ] docker
- [ ] deploy on GCP
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

