import React, { useState, useEffect } from "react";
import "./Results.css";

export default function Results(props) {
  const [gameOver, setGameOver] = useState(false);

  useEffect(() => {
    props.client.onmessage = (message) => {
      var data = JSON.parse(message['data']);
      console.log(message);
      if (data['type'] === 'game_done') {
        setGameOver(true)
      } else {
        props.setCurPage({'page': "prompt", 'user': props.user, 'room': props.room, 'prompt': data['prompt'] })
      }
    };
  });


  const earned = Object.keys(props.results['earned']).map((key) =>
        <li key={"earned-"+key}>{key + '-' + props.results['earned'][key]}</li>
    );

  var total_scores = props.results['total']
  const total = Object.keys(total_scores).map((key) =>
    <li key={"total-"+key}>{key + '-' + total_scores[key]}</li>
  );
  const winner = Object.keys(total_scores).reduce(function(a, b){ return total_scores[a] > total_scores[b] ? a : b });

  return (
    <div className="Results">
      <h1>Results</h1>
      <h2>Answer was: {props.results['answer']}</h2>
      {gameOver &&
        <h2>
          Player {winner} wins!
        </h2>
      }
      <h2>Earned</h2>
      <ul>
          {earned}
      </ul>
      <h2>Total</h2>
      <ul>
          {total}
      </ul>
    </div>
  );
}
