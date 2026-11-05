# Orders

Builds are started by hand only: Actions tab, "Command build", Run workflow. Fill in the site, the order in plain words, and the files to change.

The old way (pushing a branch named `order/<anything>` holding `.orders/order.json`) was removed so no agent can start builds in a loop. Pushing such a branch now does nothing.

Only repos on the allowed list in `.github/scripts/command_build.py` are accepted. The result is a review branch in the target repo. Nothing goes live; Roger merges.
