#!/bin/sh
input=$(cat)

cwd=$(echo "$input" | jq -r '.workspace.current_dir // .cwd // ""')
model=$(echo "$input" | jq -r '.model.display_name // ""')
used_pct=$(echo "$input" | jq -r '.context_window.used_percentage // empty')

# Shorten home directory to ~
short_cwd=$(echo "$cwd" | sed "s|^$HOME|~|")

# Git branch
git_branch=$(git -C "$cwd" --no-optional-locks branch --show-current 2>/dev/null)

# Line 1: directory (branch)
line1=$(printf "\033[34m%s\033[0m" "$short_cwd")
if [ -n "$git_branch" ]; then
  line1=$(printf "%s \033[33m(%s)\033[0m" "$line1" "$git_branch")
fi

# Line 2: model, context bar + percentage
line2=""
if [ -n "$model" ]; then
  line2=$(printf "\033[36m%s\033[0m" "$model")
fi

if [ -n "$used_pct" ]; then
  # Color based on usage: green <50, yellow <75, red_bright <90, red >=90
  if [ "$used_pct" -lt 50 ]; then
    bar_color="\033[32m"   # green
  elif [ "$used_pct" -lt 75 ]; then
    bar_color="\033[33m"   # yellow
  elif [ "$used_pct" -lt 90 ]; then
    bar_color="\033[91m"   # bright red
  else
    bar_color="\033[31m"   # red
  fi

  # Build a 20-char bar
  filled=$(( used_pct * 20 / 100 ))
  bar=""
  i=0
  while [ $i -lt 20 ]; do
    if [ $i -lt $filled ]; then
      bar="${bar}█"
    else
      bar="${bar}░"
    fi
    i=$(( i + 1 ))
  done
  if [ -n "$line2" ]; then
    line2=$(printf "%s ${bar_color}%s %s%%\033[0m" "$line2" "$bar" "$used_pct")
  else
    line2=$(printf "${bar_color}%s %s%%\033[0m" "$bar" "$used_pct")
  fi
fi

if [ -n "$line2" ]; then
  printf "%s\n%s" "$line1" "$line2"
else
  printf "%s" "$line1"
fi
