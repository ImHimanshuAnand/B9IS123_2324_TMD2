#!/bin/bash

echo "HELLO from test1.sh"
echo "This script(TEST1) is about to run another script."

sh ./test2.sh
echo "This script(TEST2) has just run another script."