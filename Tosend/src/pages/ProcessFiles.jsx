import { useState } from 'react';
import ReactDOM from "react-dom";
import App1 from "../App1.js";

const ProcessFiles = () => {
	
	const [name, setName] = useState("");
	const [userProcessType, setProcessType] = useState("");
	const [userStartDate, setStartDate] = useState("");
	const [userEndDate, setEndDate] = useState("");
	
	let logInfo = [];
	logInfo = name.split("...");
			
	const callNodeJSServer = () => {
		
		
		
		//var url = `http://localhost:3001?startDate=${userStartDate}&endDate=${userEndDate}&task=download`;
		
		
		var url = "";
		if (userProcessType=="0")
		{
			var inputInfo = {startDate: `${userStartDate}`, endDate: `${userEndDate}`, task: "process0"}
			url =`http://localhost:3001?startDate=${userStartDate}&endDate=${userEndDate}&task=process0`;
		}
		if (userProcessType=="1")
		{
			var inputInfo = {startDate: `${userStartDate}`, endDate: `${userEndDate}`, task: "process1"}
			url =`http://localhost:3001?startDate=${userStartDate}&endDate=${userEndDate}&task=process1`;
		}
		if (userProcessType=="2")
		{
			var inputInfo = {startDate: `${userStartDate}`, endDate: `${userEndDate}`, task: "process2"}
			url =`http://localhost:3001?startDate=${userStartDate}&endDate=${userEndDate}&task=process2`;
		}
		if (userProcessType=="3")
		{
			var inputInfo = {startDate: `${userStartDate}`, endDate: `${userEndDate}`, task: "process3"}
			url =`http://localhost:3001?startDate=${userStartDate}&endDate=${userEndDate}&task=process3`;
		}
		
		console.log(url)
		fetch(url)
		.then(res => res.json())
		.then(data => setName(data.name));
		
		console.log(name);
		
		
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
	<table>
	<th>
	<h3>Process Type&nbsp;</h3>
	<br/>
	</th>
	<td><select name="userProcessType" id="userProcessType" action="processTypeSelection()" onChange={(e) => setProcessType(e.target.value)}>
		<option value="Select" selected="">Select</option>
		<option value="0" selected="">All of the below</option>
		<option value="1" selected="">RGB</option>
		<option value="2" selected="">MNDWI and polygonized shapefile</option>
		<option value="3" selected="">NDTI</option>
		</select>
	</td>	
	</table>
	<br/>
	<br/>
	<button onClick={() => callNodeJSServer()}>Process Files</button>
	
	<br/>
	<br/>
	{logInfo.map(item => (
					<p key={item}>{item}</p>
				))}
				
	</>
	
	)
};

export default ProcessFiles;
