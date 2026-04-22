# How to Use This Template

To create a new Beman library, first click the "Use this template" dropdown in the
top-right and select "Create a new repository":

<table><tr><td>
  <img src="../images/use-this-template.png" width="400px">
</td></tr></table>

This will create a new repository that's an exact copy of exemplar. The next step is to
customize it for your use case.

To do so, execute the bash script `stamp.sh`. This script will prompt for parameters like
the new library's name, paper number, and description. Then it will replace your exemplar
copy with a stamped-out template containing these parameters and create a corresponding
git commit and branch:

```
$ ./stamp.sh
  [1/7] project_name (my_project_name): example_library
  [2/7] maintainer (your_github_username): your_username
  [3/7] minimum_cpp_build_version (20):
  [4/7] paper (PnnnnRr): P9999R9
  [5/7] description (Short project description.):
  [6/7] Select library_type
    1 - interface
    2 - static
    Choose from [1/2] (1):
  [7/7] Select unit_test_library
    1 - gtest
    2 - catch2
    Choose from [1/2] (1):
Switched to a new branch 'stamp'
Successfully stamped out exemplar template to the new branch 'stamp'.
Try 'git push origin stamp' to push the branch upstream,
then create a pull request.
```

From there, you can simply fill in all the remaining parts of the repository that are
labeled 'todo'.
