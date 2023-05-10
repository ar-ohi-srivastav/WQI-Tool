import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';

ReactDOM.render(
    <React.StrictMode>
		<>
		<div className='navbar' align="left"><h1 >Landsat based image processing</h1>
          </div>
		</>
        <App />
    </React.StrictMode>,
    document.getElementById('root')
);
