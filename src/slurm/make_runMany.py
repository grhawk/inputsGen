#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
# Project:  inputsGen
# FileName: make_runMany
# Creation: Jun 17, 2015
#

"""Example Google style docstrings.

This module demonstrates documentation as specified by the `Google Python
Style Guide`_. Docstrings may extend over multiple lines. Sections are created
with a section header and a colon followed by a block of indented text.

Example:
  Examples can be given using either the ``Example`` or ``Examples``
  sections. Sections support any reStructuredText formatting, including
  literal blocks::

      $ python example_google.py

Section breaks are created by simply resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Attributes:
  module_level_variable (int): Module level variables may be documented in
    either the ``Attributes`` section of the module docstring, or in an
    inline docstring immediately following the variable.

    Either form is acceptable, but the two should not be mixed. Choose
    one convention to document module level variables and be consistent
    with it.

.. _Google Python Style Guide:
   http://google-styleguide.googlecode.com/svn/trunk/pyguide.html

"""

# Try determining the version from git:
try:
    import subprocess
    git_v = subprocess.check_output(['git', 'describe'])
except subprocess.CalledProcessError:
    git_v = 'Not Yet Tagged!'


__author__ = 'Riccardo Petraglia'
__credits__ = ['Riccardo Petraglia']
__updated__ = "2015-06-18"
__license__ = 'GPLv2'
__version__ = git_v
__maintainer__ = 'Riccardo Petraglia'
__email__ = 'riccardo.petraglia@gmail.com'
__status__ = 'development'

class runManyDftbScript(object):
    def __init__(self, nreps=1, title='dftbJob'):

        self.script_file = """#!/bin/bash

dftb_sessions={nreps}

TMPFILE=submit.$$

function start_dftb() {{
    touch RUNNING.lock
    cp -f ../dftb_in.hsd .
    sed s/pippopluto_title/{title}-$1/g ../dftb.dftbp.sh > $TMPFILE; mv $TMPFILE dftb.dftbp.sh
    sbatch dftb.dftbp.sh
}}

for i in `seq 1 $dftb_sessions`; do
    name=`printf 'S-%03i' $i`
    if [[ -e $name ]]; then
        echo "Directory $name exists, checking if used.."
        cd $name
        if [[ `ls RUNNING.lock &>/dev/null; echo $?` -ne 0 ]]; then
            echo "Not used... restarting dftb+"
            start_dftb $i
        else
            echo "Directory $name already used"
        fi
        cd ..
    else
        echo "Creating $name and starting dftb+"
        mkdir $name
        cd $name
        start_dftb $i
        cd ..
    fi
done
""".format(nreps=nreps, title=title)
        self.write()

    def write(self):
        return self.script_file

if __name__ == '__main__':
    script = runManyDftbScript(nreps=10, title='test').write()
    print(script)
