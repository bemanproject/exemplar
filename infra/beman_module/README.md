# beman_module.py

<!-- SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception -->

## What is this script?

beman_module.py provides some of the features of `git submodule`, adding child git
repositories to a parent git repository, but unlike with `git submodule`, the entire child
repo is directly checked in, so only maintainers, not users, need to run this script. The
command line interface mimics `git submodule`'s.

## How do I add a beman_module to my repository?

The first `beman_module` you should add is this repository, `infra/`, which you can
bootstrap by running:

<!-- markdownlint-disable MD013 -->
```sh
curl -s https://raw.githubusercontent.com/bemanproject/infra/refs/heads/main/beman_module/beman_module.py | python3 - add https://github.com/bemanproject/infra.git
```

Once that's added, you can run the script from `infra/beman_module/beman_module.py`.

## How do I update a beman_module to the latest trunk?

You can run `beman_module.py update --remote` to update all beman_modules to latest trunk,
or e.g. `beman_module.py update --remote infra` to update only a specific one.

## How does it work under the hood?

Along with the files from the child repository, it creates a dotfile called
`.beman_module`, which looks like this:

```ini
[beman_module]
remote=https://github.com/bemanproject/infra.git
commit_hash=9b88395a86c4290794e503e94d8213b6c442ae77
```

## How do I update a beman_module to a specific commit or change the remote URL?

You can edit the corresponding lines in the `.beman_module` file and run
`beman_module.py update` to update the state of the beman_module to the new
`.beman_module` settings.

## How can I make CI ensure that my beman_modules are in a valid state?

Add this job to your CI workflow:

```yaml
  beman_modules-test:
    runs-on: ubuntu-latest
    name: "Check beman_modules for consistency"
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: beman_modules consistency check
        run: |
          (set -o pipefail; ./infra/beman_module/beman_module.py status | grep -qvF '+')
```

This will fail if the contents of any beman_module don't match what's specified in the
`.beman_module` file.
