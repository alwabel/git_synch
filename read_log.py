#!/usr/bin/env python

import os
from subprocess import PIPE,Popen
import sys
#take a git repo path and return a list of commits ordered chronologically!
def read_log(path):
  os.chdir(path)
  result = []
  p = Popen(["git","log"],stdout=PIPE)
  for line in p.stdout:
    line = line.strip()
    if line.startswith("commit"):
      result.append([line.split(' ')[1],''])
    elif not line.startswith("Date") and not line.startswith("Author") \
      and line != "":
      result[ len(result) -1][1] =line
  return result

#position a repo to a commit
def position_repo(path,commit):
  os.chdir(path)
  result = []
  p = Popen(["git","checkout","master"],stdout=PIPE,stderr=PIPE)
  p.communicate()

  p = Popen(["git","checkout",commit],stdout=PIPE,stderr=PIPE)
  p.communicate()

def sync(source,dest):
  p = Popen(["rsync","-rva","-C",".git","--delete",source+"/",dest+"/"],stderr=PIPE)
  p.communicate()

def commit(path,msg):
  os.chdir(path)
  result = []
  p = Popen(["git","add","*"],stdout=PIPE,stderr=PIPE)
  p.communicate()
  p = Popen(["git","commit","-m",msg],stdout=PIPE,stderr=PIPE)
  print p.communicate()

def push(path):
  os.chdir(path)
  p = Popen(["git","push","origin","master"],stdout=PIPE,stderr=PIPE)
  p.communicate()

source = sys.argv[1]
dest = sys.argv[2]
result = read_log(source)

for r in reversed(result):
  print r
  position_repo(source,r[0])
  sync(source,dest)
  commit(dest,r[1])

push(dest)
