# Jill Box

This is an excercise in making simple turn based games through the browser like the https://jackbox.tv/ . The main difference is that the prompts will be shown as well to allow them to be played online without screen sharing.

I want to try to get a relatively simple proof of concept out using a modern stack.

Since I'm most comfortable with Python I chose it to handle the actual game logic. I decided to go with React for the frontend since it seems to have the most documentation and is well suited for this kind of single page app.

To connect them I initial thought about using flask possibly with websockets, but then I decided it would be easier to have the Python just use a websocet interface and just use some static HTTP hosting for the React.

Later I might look into reimplementing the Python in Rust to get some experience in that language.