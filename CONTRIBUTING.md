
## Contributing to Osdag

It's through your contributions that Osdag will continue to improve. You can contribute in several ways.

Take a moment to review this document in order to make the contribution process easy and effective for everyone involved.

Following these guidelines helps to communicate that you respect the time of the developers managing and developing this open source project. In return, they should reciprocate that respect in addressing your issue or assessing patches and features.

### Using the issue tracker

The issue tracker is the preferred channel for <a href= "#bugs">bug reports</a>, <a href= "#feature">features requests</a> and submitting <a href= "#pull">pull requests</a>, but please follow the below restrictions:

   * Please **do not** use the issue tracker for personal support requests (use Osdag forum or GitHub issue).

   * Please **do not** derail or troll issues. Keep the discussion on topic and respect the opinions of others.

   * Please **do not** post comments consisting solely of "+1" or "👍". Use GitHub's "reactions" feature instead. We reserve the right to delete comments which violate this rule.

### <a id="user-content-bugs" class="anchor" href="#bugs" aria-hidden="true"></a> Bug reports


A bug is a demonstrable problem that is caused by the code in the repository. Good bug reports are extremely helpful!

Guidelines for bug reports:

   * **Use the GitHub issue search —** check if the issue has already been reported.

   * **Check if the issue has been fixed —** try to reproduce it using the latest master branch in the repository.

A good bug report shouldn't leave others needing to chase you up for more information. Please try to be as detailed as possible in your report. What is your environment? What steps will reproduce the issue? What browsers and OS experience the problem? What would you expect to be the outcome? All these details will help people to fix any potential bugs.

Example:

    Short and descriptive example bug report title

    A summary of the issue and the browser/OS environment in which it occurs. If suitable, include the steps required to reproduce the bug.

        This is the first step
        This is the second step
        Further steps, etc.

    <url> - a link to the reduced test case

    Any other information you want to share that is relevant to the issue being reported. This might include the lines of code that you have identified as causing the bug, and potential solutions (and your opinions on their merits).

### <a id="user-content-feature" class="anchor" href="#bugs" aria-hidden="true"></a>Feature requests

Feature requests are welcome. But take a moment to find out whether your idea fits with the scope and aims of the project. It's up to you to make a strong case to convince the project's developers of the merits of this feature. Please provide as much detail and context as possible.

### <a id="user-content-pull" class="anchor" href="#bugs" aria-hidden="true"></a>Pull requests

Good pull requests - patches, improvements, new features - are a fantastic help. They should remain focused in scope and avoid containing unrelated commits.

Please ask first before embarking on any significant pull request (e.g. implementing features, refactoring code, porting to a different language/OS), otherwise you risk spending a lot of time working on something that the project's developers might not want to merge into the project.

Please adhere to the coding conventions used throughout a project (indentation, accurate comments, etc.).

Follow this process if you'd like your work considered for inclusion in the project:

   1. <a href= "https://help.github.com/articles/fork-a-repo/">Fork</a> the project, clone your fork, and configure the remotes:
      
       ```bash
       #Clone your fork of the repo into the current directory
       git clone https://github.com/<your-username>/<repo-name>
       #Navigate to the newly cloned directory
       cd <repo-name>
       #Assign the original repo to a remote called "upstream"
       git remote add upstream https://github.com/<upstream-owner>/<repo-name>
       ```
      
   2. If you cloned a while ago, get the latest changes from upstream:
      
       ```bash
       git checkout <dev-branch>
       git pull upstream <dev-branch>
       ```
      
   3. Create a new topic branch (off the main project development branch) to contain your feature, change, or fix:
      
       ```bash
       git checkout -b <topic-branch-name>
       ```
      
   4. Commit your changes in logical chunks. Please adhere to these <a href= "http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html">git commit message guidelines</a> or your code is unlikely be merged into the main project.

   5. Locally merge (or rebase) the upstream development branch into your topic branch:
       
       ```bash
       git pull [--rebase] upstream <dev-branch>
       ```
   
   6. Push your topic branch up to your fork:
      
       ```bash
       git push origin <topic-branch-name>
       ```
      
   7. <a href= "https://help.github.com/articles/about-pull-requests/">Open a Pull Request</a> with a clear title and description.

**IMPORTANT:** By submitting a patch, you agree to allow the project owner to license your work under the same license as that used by the project.











