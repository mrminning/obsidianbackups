# obsidianbackups

## Install
```
# Clone
git clone https://github.com/mrminning/obsidianbackups
# Add alias
alias obsidianbackups='python ~/projects/obsidianbackups/main.py'
# Add .env file
cd obsidianbackups
touch .env
```

## Settings
Edit .env file
```text
BAT=/usr/local/bin/bat
PATTERNS= <patterns of duplicated files>-duplicated
CONFLICT=yes # Handle conflicts
OBSIDIANVAULT="/path/to/obsidian/vault"
BACKUPDIR="/path/to/obsidianbackups"
```

## Use
Run with alias or this
```
python main.py
```
