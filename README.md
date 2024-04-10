## to-do
- [x] poetry
- [x] ruff

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