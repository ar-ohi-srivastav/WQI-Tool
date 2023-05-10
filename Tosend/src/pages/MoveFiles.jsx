import { useState } from 'react';
import ReactDOM from "react-dom";
import App1 from "../App1.js";

const MoveFiles = () => {
	//const [userStartDate, setStartDate] = useState("");
	//const [userEndDate, setEndDate] = useState("");
	const [name, setName] = useState("");
		let j = 0;
		
	let logInfo = [];
	logInfo = name.split("...");
	j = logInfo.length;

	const callNodeJSServer = () => {
		
		//var inputInfo = {startDate: `${userStartDate}`, endDate: `${userEndDate}`, task: "download"}
		
		var url = `http://localhost:3001?task=moveToLocal`;
		console.log(url)
		fetch(url)
		.then(res => res.json())
		.then(data => setName(data.name));
		
		console.log(name);		
	}
    return (
	<>
	<div></div>
	<button onClick={() => callNodeJSServer()}>Move Files to local drive</button>
	<br/>
	<br/>
	{logInfo.map(item => (
					<p key={item}>{item}</p>
				))}
	</>
	)
};

export default MoveFiles;
