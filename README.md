# Jill Box

This is an excercise in making simple turn based games through the browser like the https://jackbox.tv/ . The main difference is that the prompts will be shown as well to allow them to be played online without screen sharing.

I want to try to get a relatively simple proof of concept out using a modern stack.

Since I'm most comfortable with Python I chose it to handle the actual game logic. I decided to go with React for the frontend since it seems to have the most documentation and is well suited for this kind of single page app.

To connect them I initial thought about using flask possibly with websockets, but then I decided it would be easier to have the Python just use a websocet interface and just use some static HTTP hosting for the React.

## Game Test

This demo game example is something like Fibbage. The state machine proceeds as follows:

1. A user creates a room (Login page)
2. 3 or more users join the room (Login page)
3. A user starts the game once everyone has joined (Waiting page)
4. Loop for 3 rounds
    a. The users are shown a prompt and type in an answer (Prompt page)
    b. The users are shown each other's answers and vote for the best (Vote page)
    c. The users are shown the results for this round, and for the game so far (results page)
5. The last results page declares the overall winner and allows for a new game (results page)

## TODO
 * Disconnect/reconnect logic to stay in game
 * Prevent joining after game started
 * Clean up after end of game
 * Add logic to quit / start new game
 * Add communication of current round
 * Add some synchronization protections? Need to better understand how shared objects work in asyncio
 * Making scoring scale over rounds, prevent ties
 * Add timeouts to rounds by copying the pattern used to timeout showing results
 * Make prettier
 * Add install / run scripts
 * Further documentation
 
## Possible Future Paths
 * Look into reimplementing the Python in Rust to get some experience in that language.
 * Protobufs might be helpful to specify the message schema between server/client
 * Remove the state from the server and put it in a key/value store or DB
