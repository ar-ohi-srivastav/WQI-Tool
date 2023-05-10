import { useState } from 'react';
import ReactDOM from "react-dom";
import App1 from "../App1.js";

const WebImage = () => {
 
 var img_str = "";
  
 const [userImageDate, setImageDate] = useState("");
 const [userImageType, setImageType] = useState("");
 
 
 
 const imageDateArray = userImageDate.split("-");
 img_str += "LC08_145049_";
 img_str += imageDateArray[0];
  img_str += imageDateArray[1];
   img_str += imageDateArray[2];

 
var img_folder = img_str;
 if (userImageType=="RGB")
	img_str += "_crop_rgb_b5b4b3.jpg"
 if (userImageType=="MNDWI")
		img_str += "_crop_mndwi.jpg"
 if (userImageType=="MNDWI_reclassified")
		img_str += "_crop_mndwi_reclass.jpg"
if (userImageType=="MNDWI_histogram")
	img_str += "_crop_mndwi_histogram.jpg"
if (userImageType=="NDTI")
	img_str += "_crop_ndti_masked.jpg"
if (userImageType=="NDTI_reclass")
	img_str += "_crop_ndti_reclass.jpg"
if (userImageType=="Water Body Polygon")
	img_str += "_crop_mndwi_reclass_water_body_polygon.jpg"
console.log(img_str);
console.log(process.env.PUBLIC_URL + '/images/'+img_folder+'/'+img_str);
 const showImages = () => {
	 alert("img_str" , img_str);
 }
 return (
 <>
 <body>
		<div></div>
		<table>
		<th>
	 		<h3>Enter Date:&nbsp;</h3>
		</th>
		<td>
				<input 
					type="date" 
					value={userImageDate}
					onChange={(e) => setImageDate(e.target.value)}
				/>
		</td>
		<th>	
		<h3>&nbsp;&nbsp;&nbsp;&nbsp;Image Type&nbsp; </h3>
		</th>
		<td><select name="userImageType" id="userImageType" action="imageTypeSelection()" onChange={(e) => setImageType(e.target.value)}>
			<option value="Select" selected="">Select</option>
			<option value="RGB" selected="">RGB</option>
			<option value="MNDWI" selected="">MNDWI</option>
			<option value="MNDWI_histogram" selected="">MNDWI_histogram</option>
			<option value="MNDWI_reclassified" selected="">MNDWI_reclassified</option>
			<option value="NDTI" selected="">NDTI</option>
			<option value="NDTI_reclass" selected="">NDTI_reclass</option>
			<option value="Water Body Polygon" selected="">Water Body Polygon</option>
			</select>
		</td>	
		</table>
	<br/>
	<br/>
 	
	<img src={process.env.PUBLIC_URL + '/images/'+img_folder+'/'+img_str} alt="image_not_found"/>
	
	</body>
</>
);
}
export default WebImage