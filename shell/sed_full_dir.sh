#!/usr/bin/env/ bash


# https://stackoverflow.com/a/35607711
grep -l "@nyu.edu" ./ |xargs sed -i "s/@nyu.edu/@harvard.edu/g"

# https://stackoverflow.com/a/6759339
find ./ -type f -exec sed -i -e 's/apple/orange/g' {} \;

