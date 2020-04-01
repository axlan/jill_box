import React, { useState,useEffect } from "react";
import { Button, FormGroup, FormControl, FormLabel  } from "react-bootstrap";
import "./Login.css";

export default function Login(props) {
  const [room, setRoom] = useState("");
  const [user, setUser] = useState("");
  const [error, setError] = useState("");


  useEffect(() => {
    props.client.onmessage = (message) => {
      var data = JSON.parse(message['data']);
      if (data['type'] === 'error') {
        setError(data['msg'])
      } else {
        props.setCurPage({'page': "waiting", 'user': data['user'], 'room': data['room']})
      }
    };
  });

  function validateJoin() {
    return room.length === 4 && RegExp('^[a-zA-Z]+$').test(room) && user.length > 0;
  }

  function validateCreate() {
    return user.length > 0;
  }


  function handleJoin(event) {
    props.client.send(JSON.stringify({
      type: "join_room",
      user: user,
      room: room
    }));
  }

  function handleCreate(event) {
    props.client.send(JSON.stringify({
      type: "create_room",
      user: user
    }));
  }

  return (
    <div className="Login">
      <form>
        <FormGroup controlId="room" size="large">
          <FormLabel >Room code</FormLabel >
          <FormControl
            autoFocus
            value={room}
            onChange={e => setRoom(e.target.value)}
          />
        </FormGroup>
        <FormGroup controlId="user" size="large">
          <FormLabel >Name</FormLabel >
          <FormControl
            value={user}
            onChange={e => setUser(e.target.value)}
            type="user"
          />
        </FormGroup>
        <Button block size="large" disabled={!validateJoin()} onClick={handleJoin}>
          Join Room
        </Button>
      </form>
      <hr />
      <form onSubmit={handleCreate}>
        <FormGroup controlId="user" size="large">
          <FormLabel >Name</FormLabel >
          <FormControl
            value={user}
            onChange={e => setUser(e.target.value)}
            type="user"
          />
        </FormGroup>
        <Button block size="large" disabled={!validateCreate()} onClick={handleCreate}>
          Create Room
        </Button>
      </form>
      <hr />
      <h1>{error}</h1>
    </div>
  );
}
