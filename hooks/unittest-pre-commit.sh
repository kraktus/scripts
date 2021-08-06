#!/bin/bash
#
# Called by "git commit" with no arguments.  The hook should
# exit with non-zero status after issuing an appropriate message if
# it wants to stop the commit.
#
# To enable this hook, rename this file to "pre-commit".

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

#Always synchronise test with commit 
git add -u;
python3 tests.py;
if [ $? -ne 0 ]
then
   echo -e "${RED}TESTS FAILED${NC}"
   exit 1
fi   iijijijijs
echo -e "${GREEN}TESTS PASSED${NC}"