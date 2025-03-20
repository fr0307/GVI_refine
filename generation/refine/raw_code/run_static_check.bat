@echo off
echo Starting Cppcheck and Flawfinder analysis...

echo Running Cppcheck on original code...
cppcheck --enable=all --xml ./original --output-file=cppcheck-original.xml

echo Running Cppcheck on refined code...
cppcheck --enable=all --xml ./refined --output-file=cppcheck-refined.xml

echo Running Flawfinder on original code...
flawfinder -m 0 --csv ./original > flawfinder-original.csv

echo Running Flawfinder on refined code...
flawfinder -m 0 --csv ./refined > flawfinder-refined.csv

echo Analysis completed.
pause