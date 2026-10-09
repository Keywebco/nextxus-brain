# Orders

To start a build without the Actions screen, push a branch named `order/<anything>` that holds `.orders/order.json`:

    {"repo": "nextxus-humancodex", "who": "catalyst", "order": "plain words", "files": ["index.html"]}

Only repos on the allowed list in `.github/scripts/command_build.py` are accepted. The result is a review branch in the target repo. Nothing goes live; Roger merges.
