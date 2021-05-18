FROM alpine:3.9

RUN apk --no-cache add bash bash-doc bash-completion

# Create user
ARG USER=user
ARG HOME=/home/$USER
RUN addgroup -S docker
RUN adduser -D -g "" -h $HOME -G docker $USER

RUN chown -R user /home/$USER/

# Give the user a password
RUN echo user:user | chpasswd

# Nice tools to have
RUN apk --no-cache add bash-completion nano net-tools iputils less vim emacs 
RUN apk --no-cache add py-pip python3-dev 
RUN apk --no-cache add wget

# To enable ssh
RUN apk --no-cache add openssh-server openssh-client

# Install git

RUN apk --no-cache add git

WORKDIR /home/user

USER user

# Make the command line look nice
RUN echo 'export PS1="\u@\h:\w\$\[\e]0;\u@\h: \w\a\] "' >> ~/.bashrc

# Install git linter
RUN git clone https://github.com/magicmonty/bash-git-prompt.git ~/.bash-git-prompt --depth=1 && \
    echo "GIT_PROMPT_ONLY_IN_REPO=1" >> ~/.bashrc && \
    echo "source ~/.bash-git-prompt/gitprompt.sh" >> ~/.bashrc
