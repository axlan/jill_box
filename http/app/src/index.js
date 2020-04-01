import React, { useState, useEffect } from "react";
import ReactDOM from 'react-dom';
import './index.css';
import Login from "./containers/Login";
import Waiting from "./containers/Waiting";
import { w3cwebsocket as W3CWebSocket } from "websocket";


const client = new W3CWebSocket('ws://192.168.1.110:5000');




export default function ViewMutex(props) {
  const [curPage, setCurPage] = useState({"page": "join"});
  useEffect(() => {
    client.onopen = () => {
      console.log('WebSocket Client Connected');
    };
    client.onmessage = (message) => {
      console.log(message);
    };
  }, []);
  console.log(curPage);
  switch(curPage['page']) {
    case "waiting":
      return <Waiting setCurPage={setCurPage} client={client} user={curPage['user']} room={curPage['room']}  />
    case "join":
    default:
      return <Login setCurPage={setCurPage} client={client}/>
  }


}

// ========================================

ReactDOM.render(
  <ViewMutex />,
  document.getElementById('root')
);
