check:
	black --check ghcli
	mypy ghcli
	flake8 --count ghcli
	pylint ghcli

.PHONY: check
