.PHONY: build serve gh-deploy

# ===== Documentation =====
build:
	mkdocs build

serve:
	mkdocs serve

gh-deploy:
	mkdocs gh-deploy 