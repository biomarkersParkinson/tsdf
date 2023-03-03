.PHONY: build serve gh-deploy

# ===== Documentation =====
build:
	mkdocs build

serve:
	mkdocs serve

#gh-deploy:
#	mkdocs gh-deploy 
#
# Deployment is now managed automatically via GitHub actions