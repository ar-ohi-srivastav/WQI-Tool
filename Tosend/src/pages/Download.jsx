import { useState } from 'react';
import ReactDOM from "react-dom";
import App1 from "../App1.js";

const Download = () => {
	const [userStartDate, setStartDate] = useState("");
	const [userEndDate, setEndDate] = useState("");
	const [name, setName] = useState("");
	
	let j = 0;
		
	let logInfo = [];
	logInfo = name.split("...");
		j = logInfo.length;
		
	
	const callNodeJSServer = () => {
		
		var inputInfo = {startDate: `${userStartDate}`, endDate: `${userEndDate}`, task: "download"}
		
		var url = `http://localhost:3001?startDate=${userStartDate}&endDate=${userEndDate}&task=download`;
		console.log(url)
		fetch(url)
		.then(res => res.json())
		.then(data => setName(data.name));
		
		console.log(name);
		
		//alert(myMarkdownFile);
		//fetch(myMarkdownFile)
		//	.then(response => response.text())
		//	.then(text => setText(text));
		//alert("logtext is : " , logtext);
		//alert(text);
		//ReactDOM.render(
			//		<App1 inputData={ inputInfo }/> ,
				//		document.getElementById('root')
			//);
		//root.render(<App1 inputData={ inputInfo }/>);	
		
	}
    return (
	<>
	
	<div></div>
	 		<h3>Enter your Start Date:</h3>
				<input 
					type="date" 
					value={userStartDate}
					onChange={(e) => setStartDate(e.target.value)}
				/>
		<br/>	
		<h3>Enter your End Date:</h3>
				<input 
					type="date" 
					value={userEndDate}
					onChange={(e) => setEndDate(e.target.value)}
				/>
			<br/><br/>			
    	
	<button onClick={() => callNodeJSServer()}>Download to google drive</button>
	
	<br/>
	<br/>
		
	{logInfo.map(item => (
					<p key={item}>{item}</p>
				))}
				
	</>
	
	)
};

export default Download;
