import React, { useState,useEffect } from "react";
import Button from "components/CustomButtons/Button.js";
import Snackbar from '@material-ui/core/Snackbar';
import MuiAlert from '@material-ui/lab/Alert';
function Alert(props) {
  return <MuiAlert elevation={6} variant="filled" {...props} />;
}

export default function Waiting(props) {
  const [users, setUsers] = useState([]);
  const [error, setError] = useState("");


  useEffect(() => {
    props.client.onmessage = (message) => {
      var data = JSON.parse(message['data']);
      console.log(message);
      if (data['type'] === 'user_update') {
        setUsers(data['users'])
      } else if (data['type'] === 'error') {
        setError(data['msg'])
      } else {
        props.setCurPage({'page': "prompt", 'user': props.user, 'room': props.room, 'prompt': data['prompt'] })
      }
    };
  });

  
  const handleClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }

    setError("");
  };

  function validateStart() {
    return users.length > 1;
  }

  function handleStart(event) {
    props.client.send(JSON.stringify({
      type: "start_room",
      room: props.room
    }));
  }

  const players = users.map((item, key) =>
        <li key={key}>{item}</li>
    );

  return (
    <div className="Waiting">
      <h1>Waiting to start room <span style={{fontWeight:"bold"}}>{props.room}</span></h1>
      <h2>Welcome {props.user}</h2>
      <h3>Other Players:</h3>
      <ul>
          {players}
      </ul>
      <Button color="success" disabled={!validateStart()} onClick={handleStart}>
        Start Game
      </Button>
      <Snackbar open={error.length > 0} autoHideDuration={6000} onClose={handleClose}>
      <Alert onClose={handleClose} severity="error">
        This is a success message!
      </Alert>
      </Snackbar>
    </div>
  );
}
