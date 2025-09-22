[tool.poetry]
name = "pro-scanner"
version = "5.1.3"
description = "A modern, production-ready OSINT username reconnaissance tool."
authors = ["Cyberzilla <cyberzilla@example.com>"]
license = "MIT"
readme = "README.md"
repository = "https://github.com/FJ-cyberzilla/pro_scanner.git"

[tool.poetry.dependencies]
python = "^3.10"
httpx = "^0.27.0"
rich = "^13.7.1"
pyyaml = "^6.0.1"
aiosqlite = "^0.20.0"

# This section is crucial for development and for the Dockerfile
# It specifies that this project itself is a dependency, pulled from its Git repository
[tool.poetry.group.dev.dependencies]
pro-scanner = { git = "https://github.com/FJ-cyberzilla/pro_scanner.git" }

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

