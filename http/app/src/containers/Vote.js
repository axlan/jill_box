import React, { useState, useEffect, Fragment } from "react";
import "./Vote.css";

export default function Vote(props) {
  const [selected, setSelected] = useState(-1);
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
        props.setCurPage({page: "results", user: props.user, room: props.room, results: data['results'] })
      }
    };
  });


  const answersBoxes = props.answers['answers'].map((answer, i) => (
    <Fragment key={'answer' + i}>
      <input 
        type="radio"
        name={'' + i}
        disabled={waiting}
        checked={selected === i}
        onChange={e => {
          setSelected(i);
          setWaiting(true);
          props.client.send(JSON.stringify({
            type: "submit_vote",
            room: props.room,
            user: props.user,
            vote: i
          }));
        }}
      />
      {answer}
    </Fragment>
  ));

  return (
    <div className="Vote">
      <h1>Choose the best answer</h1>
      <h2>{props.answers['prompt']}</h2>
      {answersBoxes}
      <hr />
      <h1>{error}</h1>
    </div>
  );
}
