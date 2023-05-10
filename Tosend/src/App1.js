import React from "react"

class App1 extends React.Component {
	constructor(props){
		super(props);
		this.state = {
			inputStartDate : props.inputData.startDate,
			inputEndDate : props.inputData.endDate,
			inputTask : props.inputData.task,
			name : ""
		}
	}
 		
	componentDidMount() {
		var url = `http://localhost:3001?startDate=${this.state.inputStartDate}&endDate=${this.state.inputEndDate}&task=${this.state.inputTask}`
		console.log(url)
		fetch(url)
		.then(res => res.json())
		//.then(data => this.setState({name1 : JSON.parse(data.name)})
		.then(data => this.setState({name : data.name}))
	}
  
    render() {
		const name1 = (this.state.name).split(" ");
		const count = name1[2];
		const name2 = [];
		const name3 = [];
		const drv_str = "GoogleDrive..."
		//for (let i=0;i<count;i++)
		//	name2[i] = name1[i+14];
		//Include the below section in the render() section
		//including here as this does not work in <body> section
		//<ol>
		//	{name2.map(item => (
		//		<li key={item}>{item}</li>
		//	))}
		//</ol>
		const j = 15+parseInt(count);
		let count_drv_str = 0;
		for (let i=j;i<name1.length;i++) {
			if (name1[i]==drv_str) {
				let tmp_str = "";
				for (let k=0;k<=7;k++)
					tmp_str += name1[i-7+k]+" ";
				name3[count_drv_str]=tmp_str;
				count_drv_str++;
			}
		}
		return (
			<body>
				<h3>start date is {this.state.inputStartDate}</h3>
				<h3>end date is {this.state.inputEndDate}</h3>
				<h3>task requested is {this.state.inputTask}</h3>
				<h2>Log information from Server is </h2>
	  
				<p>Number of image collections with cloud cover &lt; 10% between {this.state.inputStartDate} and {this.state.inputEndDate} = {count}</p>
				
				{name3.map(item => (
					<p key={item}>{item}</p>
				))}
				
				<p>Check the <b><a href="https://code.earthengine.google.com/tasks" target="_blank">link</a></b> for download status</p>

			</body>
		)
	}
}

export default App1
