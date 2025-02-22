# Contribute to xrcs

Everyone is welcome to contribute, and we value everybody's contribution. Code
contributions are not the only way to help the community. Answering questions, helping
others, and improving the documentation are also immensely valuable.

**This guide was heavily inspired by the awesome [transformers guide to contributing](https://github.com/scikit-learn/scikit-learn/blob/main/CONTRIBUTING.md).**

## Ways to contribute

There are several ways you can contribute to xrcs:

* Fix outstanding issues with the existing code.
* Submit issues related to bugs or desired new features.
* Implement new features.
* Contribute to the examples or to the documentation.

## Fixing outstanding issues

If you notice an issue with the existing code and have a fix in mind, feel free to [start contributing](#create-a-pull-request) and open a Pull Request!

## Submitting a bug-related issue or feature request

Do your best to follow these guidelines when submitting a bug-related issue or a feature request. It will make it easier for us to come back to you quickly and with good feedback.

### Did you find a bug?

The xrcs app aims to be robust and reliable.

Before you report an issue, we would really appreciate it if you could **make sure the bug was not already reported** (use the search bar on GitHub under Issues).

### Do you want a new feature?

If there is a new feature you'd like to see in xrcs, please open an issue and describe:

1. What is the *motivation* behind this feature? Is it related to a problem or frustration with the app? Is it something you worked on and think it could benefit the community and the users?

   Whatever it is, we'd love to hear about it!

2. Describe your requested feature in as much detail as possible. The more you can tell us about it, the better we'll be able to help you.
3. Provide a *code snippet* that demonstrates the features usage.

If your issue is well written we're already 80% of the way there by the time you create it.

## Do you want to add documentation?

We're always looking for improvements to the documentation that make it more clear and accurate. Please let us know how the documentation can be improved such as typos and any content that is missing, unclear or inaccurate. We'll be happy to make the changes or help you make a contribution if you're interested!

For more details about how to generate, build, and write the documentation, take a look at the documentation [README](https://github.com/huggingface/transformers/tree/main/docs).

## Create a Pull Request

Before writing any code, we strongly advise you to search through the existing PRs or issues to make sure nobody is already working on the same thing. If you are unsure, it is always a good idea to open an issue to get some feedback.

You will need basic `git` proficiency to contribute to xrcs. While `git` is not the easiest tool to use, it has the greatest manual. Type `git --help` in a shell and enjoy! If you prefer books, [Pro Git](https://git-scm.com/book/en/v2) is a very good reference.

You'll need **Python 3.11** to contribute to xrcs. Follow the steps below to start contributing:

1. Fork the [repository](https://github.com/JanetVictorious/xrcs) by
   clicking on the **[Fork](https://github.com/JanetVictorious/xrcs/fork)** button on the repository's page. This creates a copy of the code
   under your GitHub user account.

2. Clone your fork to your local disk, and add the base repository as a remote:

   ```bash
   git clone git@github.com:<your Github handle>/xrcs.git
   cd xrcs
   git remote add upstream https://github.com/JanetVictorious/xrcs.git
   ```


3. Create a new branch to hold your development changes:

   ```bash
   git switch -c a-descriptive-name-for-my-changes
   ```

   🚨 **Do not** work on the `main` branch!

4. Set up a development environment by running the following command in a virtual environment:

   ```bash
   make setup-venv
   ```

   If xrcs was already installed in the virtual environment, remove
   it with `rm -rf .venv` before reinstalling.

5. Develop the features in your branch.

   As you work on your code, you should make sure the test suite
   passes. Run the tests impacted by your changes like this:

   ```bash
   make run-tests
   ```

   To test the coverage, run:

   ```bash
   make run-test-cov
   ```

   xrcs relies on `black`, `ruff`, `pylint`, and `pre-commit` to format and lint its source code
   consistently.

   To install the development hooks, run:
    ```bash
    make pre-commit-install
    ```

   After you make changes, apply automatic style corrections and code verifications
   that can't be automated in one go with:

   ```bash
   make pre-commit
   ```

   This target is also optimized to only work with files modified by the PR you're working on.

   If you prefer to run the checks one after the other, the following command applies the
   style corrections:

   ```bash
   make ruff
   ```

   If you're modifying documents under the `docs/source` directory, make sure the documentation can still be built. This check will also run in the CI when you open a pull request. To run a local check:

   ```bash
   make build-docs
   ```

   Once you're happy with your changes, add the changed files with `git add` and
   record your changes locally with `git commit`:

   ```bash
   git add modified_file.py
   git commit -m "Descriptive commit message"
   ```

   Please remember to write [good commit messages](https://chris.beams.io/posts/git-commit/) to clearly communicate the changes you made!

   To keep your copy of the code up to date with the original
   repository, rebase your branch on `upstream/branch` *before* you open a pull request or if requested by a maintainer:

   ```bash
   git pull upstream main
   ```

   Push your changes to your branch:

   ```bash
   git push -u origin a-descriptive-name-for-my-changes
   ```
6. Now you can go to your fork of the repository on GitHub and click on **Pull Request** to open a pull request. Make sure you tick off all the boxes on our [checklist](#pull-request-checklist) below. When you're ready, you can send your changes to the project maintainers for review.

7. It's ok if maintainers request changes, it happens to our core contributors
   too! So everyone can see the changes in the pull request, work in your local
   branch and push the changes to your fork. They will automatically appear in
   the pull request.

### Pull request checklist

☐ The pull request title should summarize your contribution.<br>
☐ If your pull request addresses an issue, please mention the issue number in the pull
request description to make sure they are linked (and people viewing the issue know you
are working on it).<br>
☐ To indicate a work in progress please prefix the title with `[WIP]`. These are
useful to avoid duplicated work, and to differentiate it from PRs ready to be merged.<br>
☐ Make sure existing and new tests pass.<br>
☐ If adding a new feature, also add tests for it.<br>
☐ All public methods must have informative docstrings.<br>

### Tests

Tests can be found in the [tests](./tests) folder.

We like `pytest` and `pytest-xdist` because it's faster. From the root of the
repository, specify a *path to a subfolder or a test file* to run the test:

```bash
pytest -n auto ./tests/path/to/my/testfile.py
```

### Style guide

For documentation strings, xrcs follows the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html).
