import './App.scss';
import 'boxicons/css/boxicons.min.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import AppLayout from './components/layout/AppLayout';
import Blank from './pages/Blank';
import Download from './pages/Download';
import WebImage from './pages/WebImage';
import MoveFiles from './pages/MoveFiles';
import ProcessFiles from './pages/ProcessFiles';

function App() {
    return (
	<BrowserRouter>
            <Routes>
                <Route path='/' element={<AppLayout />}>
                    <Route path='/download' element={<Download />} />
                    <Route path='/move' element={<MoveFiles />} />
                    <Route path='/process' element={<ProcessFiles />} />
                    <Route path='/view' element={<WebImage />} />
                </Route>
            </Routes>
        </BrowserRouter>
    );
}

export default App;
