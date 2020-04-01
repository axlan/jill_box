import React, { useState,useEffect } from "react";
import { Button } from "react-bootstrap";
import "./Waiting.css";

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
        
      }
    };
  });

  function validateStart() {
    return users.length > 1;
  }

  function handleStart(event) {
    props.client.send(JSON.stringify({
      type: "start_room"
    }));
  }

  const players = users.map((item, key) =>
        <li key={key}>{item}</li>
    );

  return (
    <div className="Waiting">
      <h1>Waiting to start room {props.room}</h1>
      <h1>Welcome {props.user}</h1>
      <ul>
          {players}
      </ul>
      <Button block size="large" disabled={!validateStart()} onClick={handleStart}>
        Start Room
      </Button>
      <hr />
      <h1>{error}</h1>
    </div>
  );
}
