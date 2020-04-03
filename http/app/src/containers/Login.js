import React, { useState,useEffect } from "react";
import { Container, Row, Col  } from "react-bootstrap";
import CustomInput from "components/CustomInput/CustomInput.js";
import Button from "components/CustomButtons/Button.js";
import Snackbar from '@material-ui/core/Snackbar';
import MuiAlert from '@material-ui/lab/Alert';
import Box from '@material-ui/core/Box';
function Alert(props) {
  return <MuiAlert elevation={6} variant="filled" {...props} />;
}

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

  function validateRoom() {
    return room.length === 4 && RegExp('^[a-zA-Z]+$').test(room);
  }

  function validateJoin() {
    return room.length === 4 && RegExp('^[a-zA-Z]+$').test(room) && user.length > 0;
  }

  function validateCreate() {
    return user.length > 0;
  }


  function handleJoin(event) {
    event.preventDefault();
    props.client.send(JSON.stringify({
      type: "join_room",
      user: user,
      room: room
    }));
  }

  const handleClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }

    setError("");
  };

  function handleCreate(event) {
    event.preventDefault();
    props.client.send(JSON.stringify({
      type: "create_room",
      user: user
    }));
  }

  return (
    <div>
    <Container>
      <Row>
        <Col>
          <Box border={1}>
            <form onSubmit={handleJoin}>
              <CustomInput
                autoFocus
                id="room_input"
                success = {validateRoom()}
                error= {room.length >= 4 && !validateRoom()}
                inputProps={{
                  placeholder: "Enter Room Code",
                  autoComplete: "off",
                  onChange: (e) => setRoom(e.target.value)
                }}
                formControlProps={{
                  fullWidth: false
                }}s
              />
              <CustomInput
                id="user_input"
                success = {validateCreate()}
                inputProps={{
                  placeholder: "Enter Your Name",
                  onChange: (e) => setUser(e.target.value)
                }}
                formControlProps={{
                  fullWidth: false
                }}
              />
              <Button color="success" disabled={!validateJoin()} type="submit">
                Join Room
              </Button>
            </form>
          </Box>
        </Col>
        <Col>
          <Box border={1}>
            <form onSubmit={handleCreate}>
            <CustomInput
                  id="user_input2"
                  success = {validateCreate()}
                  inputProps={{
                    placeholder: "Enter Your Name",
                    onChange: (e) => setUser(e.target.value)
                  }}
                  formControlProps={{
                    fullWidth: false
                  }}
                />
              <Button color="success" disabled={!validateCreate()} type="submit">
                Create Room
              </Button>
            </form>
          </Box>
        </Col>
      </Row>
    </Container>
    <Snackbar open={error.length > 0} autoHideDuration={6000} onClose={handleClose}>
      <Alert onClose={handleClose} severity="error">
        This is a success message!
      </Alert>
    </Snackbar>
  </div>
  );
}
