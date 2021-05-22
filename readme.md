Basic Express Site
==================

Source code example for [A simple website in node.js with express, jade and stylus](http://www.clock.co.uk/blog/a-simple-website-in-nodejs-with-express-jade-and-stylus) article.

Build
-----

./build_docker.sh

This will download all dependancies into a docker image ```alpine/basic_website ```

Run
---

./run_docker.sh

This will put you into the docker container and will bring in your local copy of the repo. Any changes made to you local files will be reflected in the container and vise-versa

You might need to run ```npm install``` to get the latest node-modules

To start the webserver use ```node app.js```

Open `http://localhost:3000` to access the boiler plate website.


