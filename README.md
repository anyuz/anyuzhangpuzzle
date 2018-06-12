# Insight DevOps Engineering Systems Puzzle

## Table of Contents
1. [Understanding the puzzle](README.md#understanding-the-puzzle)
2. [Bugs & Fix](README.md#bugs & fix)
3. [Refactoring](README.md#refactoring)
4. [Summary of thoughts](README.md# summary of thoughts)


# Understanding the puzzle

We highly recommend that you take a few dedicated minutes to read this README in its entirety before starting to think about potential solutions. You'll probably find it useful to review the codebase and understand the system at a high-level before attempting to find specific bugs.

# Bugs & Fix

>> docker-compose up

Starting systems-puzzle_db_1 ... done
Starting systems-puzzle_flaskapp_1 ... done
Starting systems-puzzle_nginx_1    ... error

ERROR: for systems-puzzle_nginx_1  Cannot start service nginx: driver failed programming external connectivity on endpoint systems-puzzle_nginx_1 (95a4aa1c0f4b1fa48f6c58752c1a7323301aefc433d98188eb0590b1c5809d7f): Error starting userland proxy: Bind for 0.0.0.0:80: unexpected error (Failure EADDRINUSE)

ERROR: for nginx  Cannot start service nginx: driver failed programming external connectivity on endpoint systems-puzzle_nginx_1 (95a4aa1c0f4b1fa48f6c58752c1a7323301aefc433d98188eb0590b1c5809d7f): Error starting userland proxy: Bind for 0.0.0.0:80: unexpected error (Failure EADDRINUSE)
ERROR: Encountered errors while bringing up the project.

Trial: turn off firewall (fail)
-->port 80 on host is used

Fix1: change ports: 80:8080 to 8080:80

----------------------------------------

>> docker-compose up
access localhost:8080 returns bad gateway error

"Containers connected to the same user-defined bridge network automatically expose all ports to each other, and no ports to the outside world. "
add "expose: 80"
---> can access but not configured correctly

----------------------------------------


## Refactoring
* Don't schedule your interview until you've worked on the puzzle 
* To submit your entry please use the link you received in your systems puzzle invitation
* You will only be able to submit through the link one time
* For security, we will not open solutions submitted via files
* Use the submission box to enter the link to your GitHub repo or Bitbucket ONLY
* Link to the specific repo for this project, not your general profile
* Put any comments in the README inside your project repo

## Summary of thoughts



