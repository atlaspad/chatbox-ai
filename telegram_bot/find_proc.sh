#!/bin/bash

echo &(ps aux | grep $1)
