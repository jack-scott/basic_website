FROM alpine:3.9

RUN apk --no-cache add bash bash-doc bash-completion

# Create user
ARG USER=user
ARG HOME=/home/$USER
RUN addgroup -S docker
RUN adduser -D -g "" -h $HOME -G docker $USER

RUN chown -R user /home/$USER/

# install sudo
RUN apk --no-cache add sudo

# Give the user a password
RUN echo user:user | chpasswd

# Add the user to sudoers
RUN echo "$USER ALL=(ALL) ALL" > /etc/sudoers.d/$USER && chmod 0440 /etc/sudoers.d/$USER

# Nice tools to have
RUN apk --no-cache add bash-completion nano net-tools iputils less vim emacs 
RUN apk --no-cache add py-pip python3-dev 
RUN apk --no-cache add wget

# To enable ssh
RUN apk --no-cache add openssh-server openssh-client

# Install git
RUN apk --no-cache add git

# install npm 
RUN apk add --update nodejs npm

# This is also bad practice, need to work out how to fix the npm permissions
RUN chown -R $USER /usr/lib/node_modules

WORKDIR /home/user
USER user

# Make the command line look nice
RUN echo 'export PS1="\u@\h:\w\$\[\e]0;\u@\h: \w\a\] "' >> ~/.bashrc

# Install git linter
RUN git clone https://github.com/magicmonty/bash-git-prompt.git ~/.bash-git-prompt --depth=1 && \
    echo "GIT_PROMPT_ONLY_IN_REPO=1" >> ~/.bashrc && \
    echo "source ~/.bash-git-prompt/gitprompt.sh" >> ~/.bashrc

#I think this might be causing permissions errors
USER root
RUN npm install nodemon -g
USER user

# This is kind of a hacky fix to repair the permissions at the end
USER root
RUN chown -R $USER .config
# increases the number of file system changes that can be tracked
RUN echo "fs.inotify.max_user_watches=524288" | tee -a /etc/sysctl.conf
USER user

# install python tools

RUN pip install --user requests

