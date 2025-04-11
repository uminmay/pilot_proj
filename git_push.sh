#!/bin/bash

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check git configuration
check_git_config() {
    local git_email=$(git config user.email)
    local git_name=$(git config user.name)
    
    echo -e "${YELLOW}Current Git configuration:${NC}"
    echo -e "Name: ${GREEN}$git_name${NC}"
    echo -e "Email: ${GREEN}$git_email${NC}"
    
    read -p "Do you want to update git configuration? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter your name (press enter to keep current): " new_name
        read -p "Enter your email (press enter to keep current): " new_email
        
        if [ ! -z "$new_name" ]; then git config --global user.name "$new_name"; fi
        if [ ! -z "$new_email" ]; then git config --global user.email "$new_email"; fi
    fi
}

# Function to check if SSH key exists and is added to ssh-agent
check_ssh() {
    echo -e "${YELLOW}Checking for existing SSH keys...${NC}"
    local key_files=($(find ~/.ssh -type f -not -name "*.pub" -not -name "known_hosts" -not -name "config"))
    local num_keys=${#key_files[@]}
    
    if [ $num_keys -gt 0 ]; then
        echo -e "${GREEN}Found existing SSH keys:${NC}"
        for i in "${!key_files[@]}"; do echo "[$((i+1))] ${key_files[$i]}"; done
        read -p "Select key number (or 'n' for new key): " selection
        
        if [[ $selection =~ ^[0-9]+$ ]] && [ $selection -le $num_keys ] && [ $selection -gt 0 ]; then
            selected_key="${key_files[$((selection-1))]}"
            eval "$(ssh-agent -s)" && ssh-add "$selected_key"
            return 0
        elif [[ $selection =~ ^[Nn]$ ]]; then
            mkdir -p ~/.ssh
            echo -e "${YELLOW}Generating new SSH key...${NC}"
            read -p "Enter key name (will be created in ~/.ssh/): " key_name
            key_name=${key_name:-id_rsa}
            key_path="$HOME/.ssh/$key_name"
            
            if [ -f "$key_path" ]; then
                echo -e "${RED}Key already exists at $key_path${NC}"
                return 1
            fi
            
            ssh-keygen -t rsa -b 4096 -C "$(git config user.email)" -f "$key_path"
            eval "$(ssh-agent -s)" && ssh-add "$key_path"
            echo -e "${GREEN}Add this public key to GitHub:${NC}" && cat "${key_path}.pub"
            read -p "Press enter after adding to GitHub..."
        else
            echo -e "${RED}Invalid selection${NC}"
            return 1
        fi
    else
        echo -e "${YELLOW}No existing SSH keys found in ~/.ssh${NC}"
        echo -e "${YELLOW}Generating new SSH key...${NC}"
        mkdir -p ~/.ssh
        ssh-keygen -t rsa -b 4096 -C "$(git config user.email)" -f "$HOME/.ssh/id_rsa"
        eval "$(ssh-agent -s)" && ssh-add "$HOME/.ssh/id_rsa"
        echo -e "${GREEN}Add this public key to GitHub:${NC}" && cat "$HOME/.ssh/id_rsa.pub"
        read -p "Press enter after adding to GitHub..."
    fi
}

# Function to check if repository has commits
has_commits() {
    git rev-parse --verify HEAD >/dev/null 2>&1
    return $?
}

# Function to initialize git and handle first push
init_git() {
    local is_first_push=0
    
    if [ ! -d .git ]; then
        echo -e "${YELLOW}Git repository not initialized. Initializing...${NC}"
        git init
        is_first_push=1
        
        read -p "Enter GitHub repository URL (press enter for default): " repo_url
        git remote add origin "${repo_url:-git@github.com:uminmay/pilot_proj.git}"
        
        # Create and checkout test branch
        git checkout -b test
    fi
    return $is_first_push
}

# Function to check current branch
check_branch() {
    current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "no branch")
    if [ "$current_branch" = "main" ]; then
        echo -e "${RED}WARNING: You are on main branch!${NC}"
        read -p "Switch to test branch? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git checkout test 2>/dev/null || git checkout -b test
        else
            echo -e "${RED}Exiting to avoid pushing to main branch locally.${NC}"
            exit 1
        fi
    elif [ "$current_branch" = "no branch" ]; then
        git checkout -b test
    fi
}

# Function to check for changes
check_changes() {
    if [ -z "$(git status --porcelain)" ]; then
        echo -e "${YELLOW}No changes to commit${NC}"
        exit 0
    fi
}

# Function to get commit message
get_commit_message() {
    echo -e "${GREEN}Changes detected:${NC}"
    git status -s
    echo -e "${YELLOW}Summary of changes:${NC}"
    git diff --stat
    read -p "Enter commit message (press enter for timestamp): " commit_message
    if [ -z "$commit_message" ]; then
        echo "Update: $(date +%Y-%m-%d_%H-%M-%S)"
    else
        echo "$commit_message"
    fi
}

# Main execution
echo -e "${GREEN}Starting Git automation...${NC}"

# Initial checks
command -v git >/dev/null 2>&1 || { echo -e "${RED}Install git first${NC}"; exit 1; }
check_git_config
check_ssh

# Initialize git and check first push
init_git
is_first_push=$?

# Branch and change management
check_branch

if ! has_commits; then
    echo -e "${YELLOW}Creating initial commit...${NC}"
    git add .
    git commit -m "Initial commit"
    git push --set-upstream origin test
    echo -e "${GREEN}Repository initialized successfully!${NC}"
    exit 0
fi

check_changes

# Handle normal workflow
if [ $is_first_push -eq 0 ]; then
    echo -e "${GREEN}Pulling latest changes...${NC}"
    git pull origin $(git rev-parse --abbrev-ref HEAD)
fi

commit_message="$(get_commit_message)"
git add .
git commit -m "$commit_message"

echo -e "${GREEN}Pushing changes to test branch...${NC}"
git push origin $(git rev-parse --abbrev-ref HEAD)

echo -e "${GREEN}Successfully pushed changes to test branch. GitHub Actions will handle merging to main.${NC}"