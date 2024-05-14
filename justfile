set dotenv-load := false

# Show all available recipes
@_default:
  just --list --unsorted
  just api/
  just docs/

###############
# Environment #
###############

export API_PY_VERSION := `just api/py-version`

# Create `.env.` files from `.env.template` files
env name="":
  #!/usr/bin/env bash
  IFS=',' read -a NAMES <<< {{ if name == "" { "api,db" } else { name } }}
  for name in "${NAMES[@]}"; do
    echo "Generating ${name}/.env from ${name}/.env.template..."
    tail -n+3 "${name}/.env.template" > "${name}/.env"
  done
  echo "Done."

########
# Lint #
########

# Setup pre-commit as a Git hook
precommit:
  #!/usr/bin/env bash
  set -eo pipefail
  if [ -z "$SKIP_PRE_COMMIT" ] && [ ! -f ./pre-commit.pyz ]; then
    echo "Getting latest release..."
    curl \
      --silent \
      ${GITHUB_TOKEN:+ --header "Authorization: Bearer ${GITHUB_TOKEN}"} \
      --output latest.json \
      https://api.github.com/repos/pre-commit/pre-commit/releases/latest
    URL=$(grep -o 'https://.*\.pyz' -m 1 latest.json)
    rm latest.json
    echo "Downloading pre-commit from $URL..."
    curl \
      --silent \
      --fail \
      --location `# follow redirects, else cURL outputs a blank file` \
      --output pre-commit.pyz \
      ${GITHUB_TOKEN:+ --header "Authorization: Bearer ${GITHUB_TOKEN}"} \
      "$URL"
    echo "Installing pre-commit hooks..."
    python3 pre-commit.pyz install -t pre-push -t pre-commit
    echo "Done."
  else
    echo "Skipped pre-commit installation."
  fi

# Run pre-commit to lint and reformat files
lint hook="" *files="": precommit
  python3 pre-commit.pyz run {{ hook }} {{ if files == "" { "--all-files" } else { "--files" } }}  {{ files }}

##########
# Docker #
##########

# It is recommended to run Docker Compose commands using `just dc` recipe so
# that necessary env vars are populated where needed. For example, to build the
# API service, `just dc build api` works but `docker compose build api` fails.

# Run `docker compose` commands
dc *args:
  docker compose {{ args }}

# Build Docker services
build *args:
  just dc build {{ args }}

# Bring all Docker services up
up *args:
  just dc up -d {{ args }}

###########
# Aliases #
###########

alias l := lint

alias b := build
alias u := up
