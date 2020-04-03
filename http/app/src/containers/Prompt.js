import React, { useState,useEffect } from "react";
import { Button, FormGroup, FormControl, FormLabel } from "react-bootstrap";
import Quote from "components/Typography/Quote.js";

export default function Prompt(props) {
  const [answer, setAnswer] = useState("");
  const [error, setError] = useState("");
  const [waiting, setWaiting] = useState(false);

  useEffect(() => {
    props.client.onmessage = (message) => {
      var data = JSON.parse(message['data']);
      console.log(message);
      if (data['type'] === 'error') {
        setError(data['msg'])
        setWaiting(false)
      } else {
        props.setCurPage({page: "vote", user: props.user, room: props.room, answers: data['answers'] })
      }
    };
  });

  function validateAnswer() {
    return answer.length > 0 && !waiting;
  }

  function handleSubmit(event) {
    event.preventDefault();
    setWaiting(true)
    props.client.send(JSON.stringify({
      type: "submit_prompt",
      room: props.room,
      user: props.user,
      answer: answer
    }));
  }

  return (
    <div className="Prompt">
      <h1>Fill in the blank</h1>
      <Quote text={props.prompt} />
      <form onSubmit={handleSubmit}>
        <FormGroup controlId="answer" size="large">
            <FormLabel >Answer</FormLabel >
            <FormControl
              value={answer}
              autoComplete="off"
              disabled={waiting}
              onChange={e => setAnswer(e.target.value)}
              type="user"
            />
        </FormGroup>
        <Button block size="large" disabled={!validateAnswer()} type="submit">
          Submit answer
        </Button>
      </form>
      <hr />
      <h1>{error}</h1>
    </div>
  );
}
